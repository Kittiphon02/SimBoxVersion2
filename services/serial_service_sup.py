from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QObject
import serial
import time
import re

class SerialMonitorThread(QThread):
    new_sms_signal = pyqtSignal(str)
    at_response_signal = pyqtSignal(str)

    def __init__(self, port, baudrate):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.serial = None
        self.running = False
        self.cmt_buffer = None

    def run(self):
        """Main thread loop - ปรับปรุงการตั้งค่า SMS"""
        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout=1)
            self.running = True
            
            # ตั้งค่า SMS notification ทันทีที่เชื่อมต่อ
            self.setup_sms_notification()
            
            while self.running:
                try:
                    if self.serial.in_waiting > 0:
                        line = self.serial.readline().decode('utf-8', errors='ignore').strip()
                        if line:
                            # Debug: แสดงข้อมูลทั้งหมด
                            print(f"[SERIAL RAW] {line}")
                            self.process_received_line(line)
                    
                    time.sleep(0.1)
                    
                except Exception as e:
                    if self.running:
                        self.at_response_signal.emit(f"[SERIAL ERROR] {e}")
                    
        except Exception as e:
            self.at_response_signal.emit(f"[CONNECTION ERROR] {e}")
        finally:
            self.cleanup()

    def setup_sms_notification(self):
        """ตั้งค่า SMS notification แบบไม่ reset modem"""
        if not self.serial or not self.running:
            return

        try:
            self.at_response_signal.emit("[SMS SETUP] Setting up SMS notification...")

            # ไม่ reset modem ถี่ๆ - ลบ CFUN=0/1 ออก
            commands = [
                ("AT+CMGF=1", "Text Mode"),
                ("AT+CSCS=\"UCS2\"", "Character Set UCS2"),
                ("AT+CNMI=2,2,0,0,0", "SMS Notification Mode")
            ]
            
            for cmd, desc in commands:
                if not self.running:
                    break
                    
                self.serial.write(f"{cmd}\r\n".encode())
                time.sleep(0.5)
                self.at_response_signal.emit(f"[SMS SETUP] {desc}: {cmd}")
                    
        except Exception as e:
            self.at_response_signal.emit(f"[SMS SETUP ERROR] {e}")

    def process_received_line(self, line):
        """ประมวลผลข้อมูลที่รับมา"""
        
        # ส่งข้อมูลไปยัง UI เพียงครั้งเดียว
        if line.strip():
            self.at_response_signal.emit(line.strip())
        
        # ประมวลผล SMS และข้อมูลอื่นๆ
        try:
            self.process_sms_and_other_data(line)
        except Exception as e:
            self.at_response_signal.emit(f"[PROCESS ERROR] {e}")

    def process_sms_and_other_data(self, line):
        """ประมวลผล SMS และข้อมูลอื่นๆ ที่ไม่ใช่ AT command response"""
        
        # ตรวจสอบ CMTI notification
        if line.startswith("+CMTI:"):
            self.at_response_signal.emit(f"[SMS NOTIFICATION] {line}")
            if hasattr(self, 'read_sms_from_memory'):
                self.read_sms_from_memory(line)
            return

        # ตรวจสอบ CMT (incoming SMS) format
        if line.startswith("+CMT:"):
            self.cmt_buffer = line
            self.at_response_signal.emit(f"[SMS INCOMING] {line}")
            return
        
        # ตรวจสอบ SMS body (ถ้ามี CMT buffer)
        elif hasattr(self, 'cmt_buffer') and self.cmt_buffer:
            header = self.cmt_buffer
            body = line
            self.cmt_buffer = None
            self.at_response_signal.emit(f"[SMS BODY] {body}")
            
            try:
                if hasattr(self, 'process_sms_message'):
                    self.process_sms_message(header, body)
            except Exception as e:
                self.at_response_signal.emit(f"[SMS ERROR] {e}")

    def read_sms_from_memory(self, cmti_line):
        """อ่าน SMS จากหน่วยความจำ - ปรับปรุงการ debug"""
        try:
            import re
            
            print(f"[CMTI DEBUG] Processing: {cmti_line}")
            self.at_response_signal.emit(f"[CMTI] Processing: {cmti_line}")
            
            # แยก index จาก CMTI
            # รูปแบบ: +CMTI: "SM",index
            match = re.search(r'"SM",(\d+)', cmti_line)
            
            if match:
                index = match.group(1)
                print(f"[CMTI DEBUG] Found SMS at index: {index}")
                self.at_response_signal.emit(f"[CMTI] Reading SMS from index {index}")
                
                # ส่งคำสั่งอ่าน SMS
                cmd = f"AT+CMGR={index}"
                print(f"[CMTI DEBUG] Sending command: {cmd}")
                self.send_command(cmd)
                
            else:
                print(f"[CMTI ERROR] Could not parse index from: {cmti_line}")
                self.at_response_signal.emit(f"[CMTI ERROR] Invalid format: {cmti_line}")
                    
        except Exception as e:
            error_msg = f"[CMTI ERROR] {e}"
            print(f"[CMTI DEBUG] {error_msg}")
            self.at_response_signal.emit(error_msg)

    def process_sms_message(self, header, body):
        """ประมวลผล SMS message - แก้ไขการ decode และการส่งข้อมูล"""
        try:
            import re
            
            print(f"[SMS DEBUG] Processing SMS...")
            print(f"[SMS DEBUG] Header: {header}")
            print(f"[SMS DEBUG] Body: {body}")
            
            # แยกข้อมูลจาก header
            # รูปแบบ: +CMT: "sender_hex","","timestamp"
            match = re.match(r'\+CMT: "([^"]*)","","([^"]+)"', header)
            
            if not match:
                self.at_response_signal.emit(f"[SMS ERROR] Invalid CMT format: {header}")
                return
            
            sender_hex = match.group(1)
            timestamp = match.group(2)
            
            print(f"[SMS DEBUG] Sender hex: {sender_hex}")
            print(f"[SMS DEBUG] Message hex: {body}")
            print(f"[SMS DEBUG] Timestamp: {timestamp}")
            
            # แปลง UCS2 hex เป็น text - ใช้ฟังก์ชันที่ปรับปรุงแล้ว
            sender = self.decode_ucs2_hex_improved(sender_hex)
            message = self.decode_ucs2_hex_improved(body)
            
            print(f"[SMS DEBUG] Decoded sender: {sender}")
            print(f"[SMS DEBUG] Decoded message: {message}")
            
            # ตรวจสอบข้อมูลที่ decode แล้ว
            if not sender or sender.strip() == "":
                sender = sender_hex  # ใช้ hex เดิมถ้า decode ไม่ได้
                self.at_response_signal.emit(f"[SMS WARNING] Could not decode sender, using hex: {sender}")
            
            if not message or message.strip() == "":
                message = body  # ใช้ hex เดิมถ้า decode ไม่ได้
                self.at_response_signal.emit(f"[SMS WARNING] Could not decode message, using hex: {message}")
            
            # แสดงผลลัพธ์
            self.at_response_signal.emit(f"[SMS DECODED] From: {sender}")
            self.at_response_signal.emit(f"[SMS DECODED] Time: {timestamp}")
            self.at_response_signal.emit(f"[SMS DECODED] Message: {message}")
            
            # ตรวจสอบว่าเป็นเบอร์โทรหรือไม่
            if sender and not sender.startswith('+'):
                if sender.isdigit() and len(sender) >= 10:
                    # เพิ่ม country code ถ้าเป็นเบอร์ไทย
                    if sender.startswith('0'):
                        sender = '+66' + sender[1:]
                    elif sender.startswith('66'):
                        sender = '+' + sender
                    elif len(sender) == 9:
                        sender = '+66' + sender
            
            self.at_response_signal.emit(f"[SMS FORMATTED] Final sender: {sender}")
            
            # ส่งสัญญาณ SMS ใหม่ - ตรวจสอบ format
            sms_data = f"{sender}|{message}|{timestamp}"
            
            print(f"[SMS DEBUG] Sending signal: {sms_data}")
            self.at_response_signal.emit(f"[SMS SIGNAL] Sending: {sms_data}")
            
            # ส่งสัญญาณ
            self.new_sms_signal.emit(sms_data)
            
            self.at_response_signal.emit(f"[SMS SUCCESS] SMS signal sent successfully")
        
        except Exception as e:
            error_msg = f"[SMS ERROR] Processing failed: {e}"
            print(f"[SMS DEBUG] {error_msg}")
            self.at_response_signal.emit(error_msg)
            
            # ส่งข้อมูลดิบถ้า processing ล้มเหลว
            try:
                fallback_data = f"UNKNOWN|{body}|{timestamp if 'timestamp' in locals() else 'UNKNOWN'}"
                self.new_sms_signal.emit(fallback_data)
                self.at_response_signal.emit(f"[SMS FALLBACK] Sent raw data: {fallback_data}")
            except Exception as e2:
                self.at_response_signal.emit(f"[SMS FALLBACK ERROR] {e2}")

    def decode_ucs2_hex_improved(self, hex_str):
        """แปลง UCS2 hex string เป็น text - ปรับปรุงแล้ว"""
        if not hex_str or hex_str == '':
            return ""
            
        try:
            print(f"[DECODE DEBUG] Input hex: {hex_str}")
            
            # ลบช่องว่างและแปลงเป็น uppercase
            hex_str = hex_str.replace(" ", "").upper()
            
            # ตรวจสอบความยาว hex
            if len(hex_str) % 2 != 0:
                hex_str = hex_str + "0"  # เพิ่ม 0 ท้าย
            
            if len(hex_str) == 0:
                return ""
            
            print(f"[DECODE DEBUG] Cleaned hex: {hex_str}")
            
            # แปลงเป็น bytes
            try:
                byte_data = bytes.fromhex(hex_str)
                print(f"[DECODE DEBUG] Byte data: {byte_data}")
            except ValueError as e:
                print(f"[DECODE ERROR] Invalid hex string: {e}")
                return hex_str  # คืนค่าเดิม
            
            # ลอง decode ด้วยวิธีต่างๆ
            decode_methods = [
                ('utf-16-be', 'UTF-16 Big Endian'),
                ('utf-16-le', 'UTF-16 Little Endian'), 
                ('utf-8', 'UTF-8'),
                ('ascii', 'ASCII'),
                ('latin-1', 'Latin-1')
            ]
            
            for encoding, desc in decode_methods:
                try:
                    decoded = byte_data.decode(encoding, errors='strict')
                    # ตรวจสอบว่าผลลัพธ์สมเหตุสมผล
                    if decoded and len(decoded.strip()) > 0:
                        print(f"[DECODE SUCCESS] Method: {desc}, Result: {decoded}")
                        return decoded.strip()
                except UnicodeDecodeError:
                    continue
                except Exception as e:
                    print(f"[DECODE ERROR] {desc} failed: {e}")
                    continue
            
            # ถ้าทุกวิธีล้มเหลว ลอง decode แบบ replace errors
            try:
                decoded = byte_data.decode('utf-16-be', errors='replace')
                print(f"[DECODE FALLBACK] Using UTF-16-BE with replacement: {decoded}")
                return decoded.strip()
            except Exception:
                pass
            
            # ถ้ายังไม่ได้ ลองแปลงเป็น ASCII
            try:
                ascii_result = ""
                for i in range(0, len(byte_data), 2):
                    if i + 1 < len(byte_data):
                        # ข้าม byte แรก เอาแค่ byte ที่สอง (สำหรับ ASCII)
                        char_code = byte_data[i + 1]
                        if 32 <= char_code <= 126:  # printable ASCII
                            ascii_result += chr(char_code)
                
                if ascii_result:
                    print(f"[DECODE ASCII] Result: {ascii_result}")
                    return ascii_result
            except Exception as e:
                print(f"[DECODE ASCII ERROR] {e}")
            
            # สุดท้าย คืนค่า hex เดิม
            print(f"[DECODE FAILED] Returning original hex: {hex_str}")
            return hex_str
            
        except Exception as e:
            print(f"[DECODE CRITICAL ERROR] {e}")
            return hex_str  # คืนค่าเดิม

    def decode_ucs2_hex(self, hex_str):
        """แปลง UCS2 hex string เป็น text"""
        if not hex_str or hex_str == '':
            return ""
            
        try:
            # ลบช่องว่างและแปลงเป็น uppercase
            hex_str = hex_str.replace(" ", "").upper()
            
            # ตรวจสอบความยาว hex
            if len(hex_str) % 2 != 0:
                return hex_str  # คืนค่าเดิมถ้า hex ไม่ถูกต้อง
            
            # แปลงเป็น bytes
            byte_data = bytes.fromhex(hex_str)
            
            # ลอง decode ด้วยวิธีต่างๆ
            for encoding in ['utf-16-be', 'utf-16-le', 'utf-8']:
                try:
                    decoded = byte_data.decode(encoding, errors='strict')
                    return decoded
                except UnicodeDecodeError:
                    continue
            
            # ถ้าแปลงไม่ได้ ใช้ utf-16-be พร้อม error replacement
            return byte_data.decode('utf-16-be', errors='replace')
            
        except Exception as e:
            return hex_str  # คืนค่าเดิมถ้ามีข้อผิดพลาด
        
    def send_command(self, command):
        """ส่งคำสั่ง AT"""
        if self.serial and self.running:
            try:
                self.serial.write(f"{command}\r\n".encode())
                self.serial.flush()
            except Exception as e:
                self.at_response_signal.emit(f"[SEND ERROR] {e}")
    
    def send_raw(self, data):
        """ส่งข้อมูลดิบ"""
        if self.serial and self.running:
            try:
                self.serial.write(data)
                self.serial.flush()
            except Exception as e:
                self.at_response_signal.emit(f"[SEND RAW ERROR] {e}")
    
    def stop(self):
        """หยุดการทำงาน"""
        self.running = False
        self.wait()
    
    def cleanup(self):
        """ทำความสะอาด"""
        self.running = False
        
        if self.serial:
            try:
                self.serial.close()
            except:
                pass
            self.serial = None