import serial, serial.tools.list_ports, time
from PyQt5.QtCore import QThread, pyqtSignal
from services.sim_model import load_sim_data

def list_serial_ports():
    """ดึงรายการ serial ports พร้อม description ที่กรองแล้ว"""
    ports = []
    for p in serial.tools.list_ports.comports():
        # ทำความสะอาด description โดยลบข้อมูลที่ไม่จำเป็น
        clean_description = clean_port_description(p.description, p.device)
        ports.append((p.device, clean_description))
    
    return ports

def clean_port_description(description, device):
    """ทำความสะอาด port description"""
    if not description:
        return device
    
    # ลบข้อความที่ไม่ต้องการ
    unwanted_parts = [
        "(", ")",           # วงเล็บ
        "Incorporated",     # ชื่อบริษัท
        "Inc.",
        "Ltd.",
        "Corporation",
        "Corp.",
        "Technologies",
        "Tech.",
        "Communication",
        "Comm.",
        "Limited",
        "Co.",
        "Company"
    ]
    
    # ลบส่วนที่ไม่ต้องการ
    cleaned = description
    for unwanted in unwanted_parts:
        cleaned = cleaned.replace(unwanted, "")
    
    # ลบช่องว่างซ้ำ และทำความสะอาด
    cleaned = " ".join(cleaned.split())
    
    # ลบจุดและช่องว่างที่เหลือ
    cleaned = cleaned.replace("..", ".").replace("  ", " ").strip()
    
    # ถ้าความยาวเกิน 40 ตัวอักษร ให้ตัดให้สั้นลง
    if len(cleaned) > 40:
        # หาคำสำคัญ
        if "AT PORT" in cleaned.upper():
            cleaned = extract_key_info(cleaned, "AT PORT")
        elif "USB" in cleaned.upper():
            cleaned = extract_key_info(cleaned, "USB")
        elif "MODEM" in cleaned.upper():
            cleaned = extract_key_info(cleaned, "MODEM")
    
    return f"{device} - {cleaned}" if cleaned and cleaned != device else device

def extract_key_info(description, keyword):
    """แยกข้อมูลสำคัญจาก description"""
    upper_desc = description.upper()
    
    # หาตำแหน่งของ keyword
    keyword_pos = upper_desc.find(keyword)
    if keyword_pos == -1:
        return description[:30] + "..." if len(description) > 30 else description
    
    # เอาส่วนที่มี keyword และข้อมูลรอบๆ
    start = max(0, keyword_pos - 10)
    end = min(len(description), keyword_pos + len(keyword) + 15)
    
    result = description[start:end].strip()
    
    # ลบคำที่ไม่สำคัญ
    result = result.replace("Simcom", "").replace("HS-USB", "").strip()
    result = " ".join(result.split())  # ลบช่องว่างซ้ำ
    
    return result if result else description[:25]

class SerialMonitorThread(QThread):
    at_response_signal = pyqtSignal(str)
    new_sms_signal     = pyqtSignal(str)

    def __init__(self, port, baudrate):
        super().__init__()
        self.port, self.baudrate = port, baudrate
        self._running = True

    def run(self):
        ser = serial.Serial(self.port, self.baudrate, timeout=1)
        while self._running:
            line = ser.readline().decode(errors="ignore").strip()
            if "|" in line:
                self.new_sms_signal.emit(line)
            else:
                self.at_response_signal.emit(line)
        ser.close()

    def stop(self):
        self._running = False

def reload_sim(port, baudrate):
    """ดึงข้อมูล SIM ใหม่"""
    sims = load_sim_data(port, baudrate)
    # ... query signal strength เพิ่มเติมถ้าต้องการ ...
    return sims
