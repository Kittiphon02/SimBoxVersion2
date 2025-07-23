# services/at_command_history_service.py

import os
import json
from datetime import datetime
from typing import List, Optional

class ATCommandHistoryService:
    """บริการจัดการประวัติคำสั่ง AT Command"""
    
    def __init__(self, history_file: str = "at_command_history.txt", max_history: int = 100):
        self.history_file = history_file
        self.max_history = max_history
        self.commands = []
        self.load_history()
    
    def load_history(self) -> List[str]:
        """โหลดประวัติจากไฟล์"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.commands = [line.strip() for line in f.readlines() if line.strip()]
                print(f"📋 Loaded {len(self.commands)} AT commands from history")
            else:
                # สร้างประวัติเริ่มต้น
                self.commands = self.get_default_commands()
                self.save_history()
                print(f"📋 Created default AT command history with {len(self.commands)} commands")
                
            return self.commands.copy()
            
        except Exception as e:
            print(f"❌ Error loading AT command history: {e}")
            self.commands = self.get_default_commands()
            return self.commands.copy()
    
    def get_default_commands(self) -> List[str]:
        """ดึงคำสั่ง AT เริ่มต้น"""
        return [
            "AT",                    # Basic AT command
            "ATI",                   # Information
            "AT+CNUM",              # Phone number
            "AT+CIMI",              # IMSI
            "AT+CCID",              # ICCID  
            "AT+CSQ",               # Signal quality
            "AT+CMGF=1",            # SMS text mode
            "AT+CPIN?",             # PIN status
            "AT+CGSN",              # Serial number
            "AT+COPS?",             # Operator selection
            "AT+CFUN=1",            # Full functionality
            "AT+CFUN=0",            # Minimum functionality
            "AT+CREG?",             # Network registration
            "AT+CGMI",              # Manufacturer
            "AT+CGMM",              # Model
            "AT+CGMR",              # Revision
            "AT+CMGL=\"ALL\"",      # List all SMS
            "AT+CMGL=\"REC UNREAD\"",  # List unread SMS
            "AT+CMGL=\"REC READ\"",    # List read SMS
            "AT+CNMI=2,2,0,0,0",    # SMS notification
            "ATE0",                 # Echo off
            "ATE1",                 # Echo on
            "AT+NETOPEN",           # Network open
            "AT+NETCLOSE",          # Network close
        ]
    
    def add_command(self, command: str) -> bool:
        """เพิ่มคำสั่งใหม่ลงในประวัติ"""
        try:
            if not command or command.strip() == "":
                return False
                
            command = command.strip().upper()
            
            # ลบคำสั่งเดิมออกถ้ามีอยู่แล้ว (เพื่อย้ายไปด้านบน)
            if command in self.commands:
                self.commands.remove(command)
            
            # เพิ่มคำสั่งใหม่ที่ด้านบน
            self.commands.insert(0, command)
            
            # จำกัดจำนวนประวัติ
            if len(self.commands) > self.max_history:
                self.commands = self.commands[:self.max_history]
            
            # บันทึกลงไฟล์
            self.save_history()
            
            print(f"📝 Added '{command}' to AT command history")
            return True
            
        except Exception as e:
            print(f"❌ Error adding command to history: {e}")
            return False
    
    def save_history(self) -> bool:
        """บันทึกประวัติลงไฟล์"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                for cmd in self.commands:
                    f.write(f"{cmd}\n")
            return True
            
        except Exception as e:
            print(f"❌ Error saving AT command history: {e}")
            return False
    
    def get_commands(self) -> List[str]:
        """ดึงรายการคำสั่งทั้งหมด"""
        return self.commands.copy()
    
    def search_commands(self, keyword: str) -> List[str]:
        """ค้นหาคำสั่งที่ตรงกับ keyword"""
        if not keyword:
            return self.commands.copy()
            
        keyword = keyword.upper()
        return [cmd for cmd in self.commands if keyword in cmd]
    
    def get_recent_commands(self, count: int = 10) -> List[str]:
        """ดึงคำสั่งล่าสุด"""
        return self.commands[:min(count, len(self.commands))]
    
    def clear_history(self) -> bool:
        """ล้างประวัติทั้งหมด"""
        try:
            self.commands = []
            if os.path.exists(self.history_file):
                os.remove(self.history_file)
            print("🗑️ AT command history cleared")
            return True
            
        except Exception as e:
            print(f"❌ Error clearing history: {e}")
            return False
    
    def export_history(self, export_file: str) -> bool:
        """ส่งออกประวัติเป็นไฟล์"""
        try:
            export_data = {
                "exported_at": datetime.now().isoformat(),
                "total_commands": len(self.commands),
                "commands": self.commands
            }
            
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            print(f"📤 AT command history exported to: {export_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error exporting history: {e}")
            return False
    
    def import_history(self, import_file: str, merge: bool = True) -> bool:
        """นำเข้าประวัติจากไฟล์"""
        try:
            if not os.path.exists(import_file):
                print(f"❌ Import file not found: {import_file}")
                return False
            
            with open(import_file, 'r', encoding='utf-8') as f:
                if import_file.endswith('.json'):
                    data = json.load(f)
                    imported_commands = data.get('commands', [])
                else:
                    # ถือว่าเป็นไฟล์ text ธรรมดา
                    imported_commands = [line.strip() for line in f.readlines() if line.strip()]
            
            if merge:
                # รวมประวัติเดิมกับใหม่
                for cmd in imported_commands:
                    if cmd not in self.commands:
                        self.commands.append(cmd)
            else:
                # แทนที่ประวัติเดิม
                self.commands = imported_commands.copy()
            
            # จำกัดจำนวน
            if len(self.commands) > self.max_history:
                self.commands = self.commands[:self.max_history]
            
            self.save_history()
            
            print(f"📥 Imported {len(imported_commands)} commands from: {import_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error importing history: {e}")
            return False
    
    def get_command_usage_stats(self) -> dict:
        """ดึงสถิติการใช้งานคำสั่ง (สำหรับอนาคต)"""
        # ในอนาคตอาจเก็บข้อมูลการใช้งานแต่ละคำสั่ง
        return {
            "total_commands": len(self.commands),
            "most_recent": self.commands[0] if self.commands else None,
            "unique_prefixes": len(set(cmd.split('+')[0] for cmd in self.commands if '+' in cmd))
        }

# ตัวอย่างการใช้งาน
if __name__ == "__main__":
    # ทดสอบการใช้งาน
    history_service = ATCommandHistoryService()
    
    print("📋 Current commands:", history_service.get_commands()[:5])
    
    # เพิ่มคำสั่งใหม่
    history_service.add_command("AT+TEST=1")
    
    # ค้นหาคำสั่ง
    search_results = history_service.search_commands("CMGF")
    print("🔍 Search results for 'CMGF':", search_results)
    
    # ส่งออกประวัติ
    history_service.export_history("at_history_backup.json")
    
    # แสดงสถิติ
    stats = history_service.get_command_usage_stats()
    print("📊 Statistics:", stats)