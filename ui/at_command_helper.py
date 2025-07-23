# ui/at_command_helper.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QListWidget, QListWidgetItem, 
    QPushButton, QTextEdit, QSplitter, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

class ATCommandHelper(QWidget):
    """ตัวช่วยสำหรับ AT Command พร้อมคำอธิบายและตัวอย่าง"""
    
    command_selected = pyqtSignal(str)  # ส่งสัญญาณเมื่อเลือกคำสั่ง
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_command_database()
    
    def init_ui(self):
        """สร้าง UI"""
        self.setWindowTitle("AT Command Helper")
        self.setGeometry(100, 100, 800, 600)
        
        # Main layout
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("📋 AT Command Reference & Helper")
        header.setStyleSheet("""
            font-size: 18px; 
            font-weight: bold; 
            color: #dc3545; 
            padding: 10px;
            background-color: #fff5f5;
            border-radius: 8px;
            margin-bottom: 10px;
        """)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Search box
        search_layout = QHBoxLayout()
        search_label = QLabel("🔍 Search:")
        search_label.setFixedWidth(60)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type command or description...")
        self.search_input.textChanged.connect(self.filter_commands)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Splitter for main content
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Command list
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        list_header = QLabel("AT Commands")
        list_header.setStyleSheet("font-weight: bold; padding: 5px;")
        left_layout.addWidget(list_header)
        
        self.command_list = QListWidget()
        self.command_list.itemClicked.connect(self.on_command_selected)
        left_layout.addWidget(self.command_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.btn_use = QPushButton("📤 Use Command")
        self.btn_use.clicked.connect(self.use_selected_command)
        self.btn_use.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 4px;
                border: none;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        
        self.btn_copy = QPushButton("📋 Copy")
        self.btn_copy.clicked.connect(self.copy_command)
        self.btn_copy.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                border: none;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        
        button_layout.addWidget(self.btn_use)
        button_layout.addWidget(self.btn_copy)
        left_layout.addLayout(button_layout)
        
        # Right panel - Command details
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        detail_header = QLabel("Command Details")
        detail_header.setStyleSheet("font-weight: bold; padding: 5px;")
        right_layout.addWidget(detail_header)
        
        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)
        self.detail_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #dee2e6;
                border-radius: 4px;
                background-color: #f8f9fa;
                padding: 10px;
                font-family: 'Courier New', monospace;
            }
        """)
        right_layout.addWidget(self.detail_text)
        
        # Set panel sizes
        left_panel.setMaximumWidth(300)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 500])
        
        layout.addWidget(splitter)
        
        # Apply main style
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #dc3545;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #c82333;
                background-color: #fff5f5;
            }
        """)
    
    def load_command_database(self):
        """โหลดฐานข้อมูลคำสั่ง AT"""
        self.commands = {
            # Basic Commands
            "AT": {
                "description": "Basic AT command test",
                "usage": "AT",
                "response": "OK",
                "category": "Basic",
                "details": """
Basic AT command to test modem communication.

Usage: AT
Expected Response: OK

This is the most basic command to verify that the modem is responding to AT commands.
                """
            },
            
            "ATI": {
                "description": "Display product identification information",
                "usage": "ATI",
                "response": "Product info + OK",
                "category": "Information",
                "details": """
Display product identification information.

Usage: ATI
Expected Response: Product identification text followed by OK

Shows manufacturer, model, and firmware version information.
                """
            },
            
            # SIM Commands
            "AT+CPIN?": {
                "description": "Check SIM PIN status",
                "usage": "AT+CPIN?",
                "response": "+CPIN: READY",
                "category": "SIM",
                "details": """
Check the current SIM PIN status.

Usage: AT+CPIN?
Possible Responses:
- +CPIN: READY (SIM ready, no PIN required)
- +CPIN: SIM PIN (PIN required)
- +CPIN: SIM PUK (PUK required)

Essential for checking if SIM card is ready for operation.
                """
            },
            
            "AT+CIMI": {
                "description": "Get International Mobile Subscriber Identity (IMSI)",
                "usage": "AT+CIMI",
                "response": "15-digit IMSI number",
                "category": "SIM", 
                "details": """
Request the International Mobile Subscriber Identity (IMSI).

Usage: AT+CIMI
Response: 15-digit IMSI number

IMSI format: MCC(3) + MNC(2-3) + MSIN(9-10)
- MCC: Mobile Country Code
- MNC: Mobile Network Code  
- MSIN: Mobile Subscriber Identification Number

Thailand examples:
- 520-01: AIS
- 520-05: DTAC
- 520-03: TRUE
                """
            },
            
            "AT+CCID": {
                "description": "Get SIM Card Identification (ICCID)",
                "usage": "AT+CCID",
                "response": "ICCID number",
                "category": "SIM",
                "details": """
Request the Integrated Circuit Card Identifier (ICCID).

Usage: AT+CCID
Response: 19-20 digit ICCID number

ICCID is the unique identifier for the SIM card itself.
Format: IIN(7) + Account ID(variable) + Check digit(1)
                """
            },
            
            "AT+CNUM": {
                "description": "Get subscriber phone number",
                "usage": "AT+CNUM",
                "response": "+CNUM: phone number",
                "category": "SIM",
                "details": """
Request the subscriber's phone number stored on SIM.

Usage: AT+CNUM
Response: +CNUM: [name],phone_number,[type]

Note: Some SIM cards may not have the phone number stored,
resulting in an empty response.
                """
            },
            
            # Network Commands
            "AT+CSQ": {
                "description": "Signal Quality Report",
                "usage": "AT+CSQ",
                "response": "+CSQ: rssi,ber",
                "category": "Network",
                "details": """
Report signal strength and bit error rate.

Usage: AT+CSQ
Response: +CSQ: rssi,ber

RSSI (Received Signal Strength Indicator):
- 0: -113 dBm or less
- 1: -111 dBm  
- 2-30: -109 to -53 dBm
- 31: -51 dBm or greater
- 99: Unknown

BER (Bit Error Rate):
- 0-7: As RXQUAL values
- 99: Unknown
                """
            },
            
            "AT+COPS?": {
                "description": "Current network operator",
                "usage": "AT+COPS?",
                "response": "+COPS: mode,format,operator",
                "category": "Network",
                "details": """
Query current network operator selection.

Usage: AT+COPS?
Response: +COPS: mode,format,operator[,AcT]

Mode:
- 0: Automatic
- 1: Manual
- 2: Deregister
- 3: Set format only
- 4: Manual/automatic

Format:
- 0: Long alphanumeric
- 1: Short alphanumeric  
- 2: Numeric

AcT (Access Technology):
- 0: GSM
- 2: UTRAN
- 7: E-UTRAN
                """
            },
            
            "AT+CREG?": {
                "description": "Network registration status",
                "usage": "AT+CREG?",
                "response": "+CREG: n,stat",
                "category": "Network",
                "details": """
Query network registration status.

Usage: AT+CREG?
Response: +CREG: n,stat[,lac,ci]

Status (stat):
- 0: Not registered, not searching
- 1: Registered, home network
- 2: Not registered, searching
- 3: Registration denied
- 4: Unknown
- 5: Registered, roaming
                """
            },
            
            # SMS Commands
            "AT+CMGF=1": {
                "description": "Set SMS text mode",
                "usage": "AT+CMGF=1",
                "response": "OK",
                "category": "SMS",
                "details": """
Set SMS message format to text mode.

Usage: AT+CMGF=1
Response: OK

Message Formats:
- 0: PDU mode (binary)
- 1: Text mode (human readable)

Text mode is easier for basic SMS operations.
                """
            },
            
            "AT+CMGL=\"ALL\"": {
                "description": "List all SMS messages",
                "usage": "AT+CMGL=\"ALL\"",
                "response": "List of messages",
                "category": "SMS",
                "details": """
List SMS messages by status.

Usage: AT+CMGL="status"
Response: List of messages with index, status, sender, timestamp

Status options:
- "REC UNREAD": Received unread messages
- "REC READ": Received read messages  
- "STO UNSENT": Stored unsent messages
- "STO SENT": Stored sent messages
- "ALL": All messages
                """
            },
            
            "AT+CNMI=2,2,0,0,0": {
                "description": "Configure SMS notifications",
                "usage": "AT+CNMI=2,2,0,0,0",
                "response": "OK", 
                "category": "SMS",
                "details": """
Configure new SMS message indications.

Usage: AT+CNMI=mode,mt,bm,ds,bfr
Response: OK

Parameters:
- mode: 0-3 (buffer/flush settings)
- mt: 0-3 (SMS-DELIVER indication)
  - 0: No indication
  - 1: Store and indicate location
  - 2: Direct indication
  - 3: Class 3 direct indication
- bm: 0-2 (Broadcast message indication)
- ds: 0-2 (SMS-STATUS-REPORT indication)  
- bfr: 0-1 (Buffer handling)

Common setting: AT+CNMI=2,2,0,0,0 for immediate SMS notification.
                """
            },
            
            # Device Information
            "AT+CGMI": {
                "description": "Manufacturer identification",
                "usage": "AT+CGMI",
                "response": "Manufacturer name",
                "category": "Device Info",
                "details": """
Request manufacturer identification.

Usage: AT+CGMI
Response: Manufacturer name (e.g., "SIMCOM")

Returns the name of the modem manufacturer.
                """
            },
            
            "AT+CGMM": {
                "description": "Model identification", 
                "usage": "AT+CGMM",
                "response": "Model name",
                "category": "Device Info",
                "details": """
Request model identification.

Usage: AT+CGMM
Response: Model name (e.g., "SIM7600E-H")

Returns the specific model number of the modem.
                """
            },
            
            "AT+CGMR": {
                "description": "Revision identification",
                "usage": "AT+CGMR", 
                "response": "Firmware version",
                "category": "Device Info",
                "details": """
Request revision (firmware) identification.

Usage: AT+CGMR
Response: Firmware version string

Returns the firmware/software version running on the modem.
                """
            },
            
            "AT+CGSN": {
                "description": "Product serial number (IMEI)",
                "usage": "AT+CGSN",
                "response": "15-digit IMEI",
                "category": "Device Info", 
                "details": """
Request product serial number (IMEI).

Usage: AT+CGSN
Response: 15-digit IMEI number

IMEI (International Mobile Equipment Identity) uniquely identifies the device.
Format: TAC(8) + SNR(6) + Check digit(1)
                """
            },
            
            # Control Commands
            "AT+CFUN=1": {
                "description": "Set full functionality",
                "usage": "AT+CFUN=1",
                "response": "OK",
                "category": "Control",
                "details": """
Set phone functionality level.

Usage: AT+CFUN=level
Response: OK

Functionality Levels:
- 0: Minimum functionality (RF disabled)
- 1: Full functionality (default)
- 4: Disable RF transmit and receive

AT+CFUN=1 enables full modem functionality including network registration.
                """
            },
            
            "AT+CFUN=0": {
                "description": "Set minimum functionality", 
                "usage": "AT+CFUN=0",
                "response": "OK",
                "category": "Control",
                "details": """
Set minimum functionality (RF circuits disabled).

Usage: AT+CFUN=0
Response: OK

This disables RF transmit and receive circuits to save power.
Use AT+CFUN=1 to restore full functionality.
                """
            },
            
            "ATE0": {
                "description": "Disable command echo",
                "usage": "ATE0", 
                "response": "OK",
                "category": "Control",
                "details": """
Control command echo.

Usage: 
- ATE0: Disable echo
- ATE1: Enable echo

When echo is disabled, commands typed are not echoed back in the response.
                """
            },
            
            "ATE1": {
                "description": "Enable command echo",
                "usage": "ATE1",
                "response": "OK", 
                "category": "Control",
                "details": """
Control command echo.

Usage:
- ATE0: Disable echo  
- ATE1: Enable echo

When echo is enabled, commands typed are echoed back in the response.
                """
            }
        }
        
        self.populate_command_list()
    
    def populate_command_list(self, filter_text=""):
        """เติมรายการคำสั่งใน list widget"""
        self.command_list.clear()
        
        for cmd, info in self.commands.items():
            if filter_text.lower() in cmd.lower() or filter_text.lower() in info['description'].lower():
                item = QListWidgetItem()
                item.setText(f"{cmd}\n{info['description']}")
                item.setData(Qt.UserRole, cmd)
                
                # กำหนดสีตามหมวดหมู่
                category_colors = {
                    "Basic": "#17a2b8",
                    "SIM": "#dc3545", 
                    "Network": "#28a745",
                    "SMS": "#ffc107",
                    "Device Info": "#6f42c1",
                    "Control": "#fd7e14"
                }
                
                color = category_colors.get(info['category'], "#6c757d")
                item.setBackground(Qt.lightGray)
                
                self.command_list.addItem(item)
    
    def filter_commands(self, text):
        """กรองคำสั่งตามข้อความค้นหา"""
        self.populate_command_list(text)
    
    def on_command_selected(self, item):
        """เมื่อเลือกคำสั่งจากรายการ"""
        cmd = item.data(Qt.UserRole)
        if cmd in self.commands:
            self.show_command_details(cmd)
    
    def show_command_details(self, cmd):
        """แสดงรายละเอียดคำสั่ง"""
        info = self.commands[cmd]
        
        details = f"""
<h2 style="color: #dc3545;">{cmd}</h2>
<p><strong>Category:</strong> {info['category']}</p>
<p><strong>Description:</strong> {info['description']}</p>

<h3>Usage:</h3>
<pre style="background-color: #f8f9fa; padding: 10px; border-radius: 4px;">
{info['usage']}
</pre>

<h3>Expected Response:</h3>
<pre style="background-color: #e9ecef; padding: 10px; border-radius: 4px;">
{info['response']}
</pre>

<h3>Details:</h3>
<div style="background-color: #fff; padding: 10px; border-left: 4px solid #dc3545;">
{info['details'].strip()}
</div>
        """
        
        self.detail_text.setHtml(details)
        self.selected_command = cmd
    
    def use_selected_command(self):
        """ใช้คำสั่งที่เลือก"""
        if hasattr(self, 'selected_command'):
            self.command_selected.emit(self.selected_command)
            self.close()
    
    def copy_command(self):
        """คัดลอกคำสั่งไปยัง clipboard"""
        if hasattr(self, 'selected_command'):
            from PyQt5.QtWidgets import QApplication
            QApplication.clipboard().setText(self.selected_command)
            
            # แสดงข้อความแจ้งเตือน
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.information(self, "Copied", f"Command '{self.selected_command}' copied to clipboard!")

# ตัวอย่างการใช้งาน
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    helper = ATCommandHelper()
    helper.show()
    sys.exit(app.exec_())