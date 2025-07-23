# ui/ui_builder.py

import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QPushButton, QTextEdit, QLineEdit,
    QGroupBox, QFrame, QSizePolicy, QPlainTextEdit
)
from PyQt5.QtCore import Qt

from ui.sim_table_widget import SimTableWidget
from styles import (
    MainWindowStyles,
    SmsLogDialogStyles,
    SimTableWidgetStyles,
    StyleUtils,
    GlobalColorScheme
)

def set_button_with_size(button, width):
    """ตั้งค่าขนาดปุ่มหลังจากตั้งค่า style"""
    button.setFixedWidth(width)
    button.setFixedHeight(35)  # กำหนดความสูงเท่ากัน
    return button

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SIM Management System")
        self.resize(1100, 800)

        # ── Header ───────────────────────────────────────────────
        title = QLabel("SIM Management System")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(MainWindowStyles.get_header_style())

        # ── 1) Modem Connection Section ─────────────────────────
        modem_group = QGroupBox("Set up modem connection")
        modem_group.setStyleSheet(MainWindowStyles.get_modem_group_style())
        mg_layout = QHBoxLayout(modem_group)

        # create port and baud combo before adding to layout
        self.port_combo = QComboBox()
        self.baud_combo = QComboBox()
        self.baud_combo.addItems(["9600", "19200", "38400", "57600", "115200"])
        self.baud_combo.setCurrentText("115200")

        combo_qss = MainWindowStyles.get_at_combo_style()
        self.port_combo.setStyleSheet(combo_qss)
        self.baud_combo.setStyleSheet(combo_qss)

        self.btn_refresh = QPushButton("Refresh Ports")
        self.btn_refresh.setStyleSheet(MainWindowStyles.get_refresh_button_style())
        set_button_with_size(self.btn_refresh, 110)

        self.btn_history = QPushButton("ดูประวัติ SMS")
        self.btn_history.setStyleSheet(StyleUtils.create_button_style(
            GlobalColorScheme.INFO,
            GlobalColorScheme.INFO_LIGHT,
            GlobalColorScheme.INFO
        ))
        set_button_with_size(self.btn_history, 120)

        self.btn_monitor = QPushButton("SMS Monitor")
        self.btn_monitor.setStyleSheet(StyleUtils.create_button_style(
            GlobalColorScheme.SUCCESS,
            GlobalColorScheme.SUCCESS_LIGHT,
            GlobalColorScheme.SUCCESS
        ))
        set_button_with_size(self.btn_monitor, 110)

        self.btn_recover = QPushButton("SIM Recovery")
        self.btn_recover.setStyleSheet(MainWindowStyles.get_send_at_button_style())
        set_button_with_size(self.btn_recover, 115)

        mg_layout.addWidget(QLabel("USB Port:"))
        mg_layout.addWidget(self.port_combo)
        mg_layout.addWidget(QLabel("Baudrate:"))
        mg_layout.addWidget(self.baud_combo)
        mg_layout.addWidget(self.btn_refresh)
        mg_layout.addWidget(self.btn_history)
        mg_layout.addWidget(self.btn_monitor)
        mg_layout.addWidget(self.btn_recover)

        # ── 2) AT Command Display Section ────────────────────────
        at_group = QGroupBox("AT Command Display")
        at_group.setStyleSheet(MainWindowStyles.get_at_group_style())
        ag_layout = QVBoxLayout(at_group)

        # row1: AT Command input + DELETE + AT Result
        row1 = QHBoxLayout()
        row1.setSpacing(15)

        # AT command input
        at_cmd_container = QWidget()
        at_cmd_container.setFixedWidth(780)
        at_cmd_layout = QHBoxLayout(at_cmd_container)
        at_cmd_layout.setContentsMargins(25,10,25,10)
        at_cmd_layout.setSpacing(20)

        at_label = QLabel("AT Command:")
        at_label.setFixedWidth(100)
        at_label.setStyleSheet("font-weight: bold; color: #722f37;")
        
        # สร้าง container สำหรับ input และ dropdown
        input_container = QWidget()
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(15)
        
        self.cmd_input = QLineEdit("AT")
        self.cmd_input.setStyleSheet(MainWindowStyles.get_input_cmd_style())
        self.cmd_input.setFixedHeight(42)  # เพิ่มจาก 35 เป็น 42
        self.cmd_input.setMinimumWidth(200)  # เพิ่มบรรทัดนี้
        
        # สร้าง dropdown สำหรับประวัติคำสั่ง
        self.cmd_history_combo = QComboBox()
        # ใช้สไตล์ที่ปรับปรุงแล้วสำหรับ history dropdown
        history_style = """
            QComboBox {
                font-size: 12px;
                border: 2px solid #dc3545;
                border-radius: 4px;
                background-color: #fff5f5;
                color: #212529;
                padding: 6px 12px;
                min-width: 150px;
            }
            QComboBox:hover {
                border: 2px solid #c82333;
                background-color: #fff5f5;
            }
            QComboBox:focus {
                border: 2px solid #a71e2a;
                background-color: #fff5f5;
                outline: none;
            }
            QComboBox::drop-down {
                border: none;
                background-color: #dc3545;
                border-top-right-radius: 4px;
                border-bottom-right-radius: 4px;
                width: 24px;
            }
            QComboBox::down-arrow {
                image: none;
                border: 2px solid white;
                border-top: none;
                border-left: none;
                width: 6px;
                height: 6px;
                margin: 4px;
            }
            QComboBox QAbstractItemView {
                background-color: #fff;
                border: 2px solid #dc3545;
                border-radius: 4px;
                selection-background-color: #fff5f5;
                selection-color: #dc3545;
                font-size: 12px;
                padding: 2px;
            }
            QComboBox QAbstractItemView::item {
                padding: 6px 10px;
                border-bottom: 1px solid #f0f0f0;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #fff5f5;
                color: #dc3545;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #dc3545;
                color: white;
            }
        """
        self.cmd_history_combo.setStyleSheet(history_style)
        self.cmd_history_combo.setFixedHeight(42)
        self.cmd_history_combo.setFixedWidth(220)
        self.cmd_history_combo.addItem("History ▼")
        
        # โหลดประวัติจากไฟล์
        self.load_at_command_history()
        
        # เชื่อมต่อ signal เมื่อเลือกคำสั่งจาก dropdown
        self.cmd_history_combo.currentTextChanged.connect(self.on_history_selected)
        
        input_layout.addWidget(self.cmd_input, 1)
        input_layout.addWidget(self.cmd_history_combo)
        

        self.btn_delete = QPushButton("DELETE")
        self.btn_delete.setStyleSheet(MainWindowStyles.get_send_at_button_style())
        self.btn_delete.setFixedHeight(42)
        self.btn_delete.setFixedWidth(80)

        # เพิ่มปุ่ม Help (Optional)
        self.btn_help = QPushButton("❓ Help")
        self.btn_help.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                           stop:0 #17a2b8, stop:1 #138496);
                color: white; font-weight: 600; border-radius: 4px;
                padding: 6px 12px; font-size: 12px; border: none;
                min-width: 60px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #138496, stop:1 #117a8b);
                box-shadow: 0 2px 4px rgba(0,0,0,0.3);
            }
            QPushButton:pressed {
                background: #117a8b;
                padding-top: 7px;
            }
        """)
        self.btn_help.setFixedHeight(42)
        self.btn_help.setFixedWidth(100)

        at_cmd_layout.addWidget(at_label)
        at_cmd_layout.addWidget(input_container, 1)
        at_cmd_layout.addWidget(self.btn_delete)
        at_cmd_layout.addWidget(self.btn_help)

        self.at_result_display = QTextEdit()
        self.at_result_display.setStyleSheet(MainWindowStyles.get_result_display_style())
        self.at_result_display.setFixedHeight(35)
        # ทำให้ AT result display เป็น read-only
        self.at_result_display.setReadOnly(True)
        self.at_result_display.setPlaceholderText("AT command results...")

        row1.addWidget(at_cmd_container)
        ag_layout.addLayout(row1)
        ag_layout.addSpacing(10)

        # prepare action buttons for row2
        self.btn_send_at  = QPushButton("Send AT")
        self.btn_send_sms = QPushButton("Send SMS")
        self.btn_inbox    = QPushButton("SMS inbox")
        self.btn_del_sms  = QPushButton("Delete SMS")
        
        # Apply styles and set sizes for action buttons
        button_configs = [
            (self.btn_send_at,  MainWindowStyles.get_send_at_button_style(), 120),
            (self.btn_send_sms, MainWindowStyles.get_send_sms_button_style(), 120),
            (self.btn_inbox,    StyleUtils.create_button_style(
                                   GlobalColorScheme.INFO,
                                   GlobalColorScheme.INFO_LIGHT,
                                   GlobalColorScheme.INFO), 120),
            (self.btn_del_sms,  MainWindowStyles.get_delete_button_style(), 120)
        ]
        
        for btn, style, width in button_configs:
            btn.setStyleSheet(style)
            set_button_with_size(btn, width)

        # row2: SMS + Telephone + Actions + AT Log  |  Response
        row2 = QHBoxLayout()
        row2.setContentsMargins(0, 10, 0, 0)
        row2.setSpacing(15)

        # left side
        left_container = QWidget()
        left_container.setFixedWidth(550)
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(0,0,0,0)
        left_layout.setSpacing(10)

        left_layout.addWidget(QLabel("SMS messages:",
            **{"styleSheet":"font-weight:bold; color:#722f37; margin-bottom:5px;"}))
        self.sms_input = QTextEdit()
        self.sms_input.setPlaceholderText("Enter the message to send...")
        self.sms_input.setStyleSheet(MainWindowStyles.get_sms_input_style())
        self.sms_input.setFixedHeight(50)
        left_layout.addWidget(self.sms_input)

        left_layout.addWidget(QLabel("Telephone number:",
            **{"styleSheet":"font-weight:bold; color:#722f37; margin-bottom:5px;"}))
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter destination number...")
        self.phone_input.setStyleSheet(MainWindowStyles.get_phone_input_style())
        self.phone_input.setFixedHeight(35)
        left_layout.addWidget(self.phone_input)

        btn_box = QHBoxLayout()
        btn_box.setContentsMargins(0, 0, 0, 0)
        btn_box.setSpacing(20)
        # จัดกึ่งกลาง: เติม stretch ก่อนและหลัง
        btn_box.addStretch(1)
        btn_box.addWidget(self.btn_send_at)
        btn_box.addWidget(self.btn_send_sms)
        btn_box.addWidget(self.btn_inbox)
        btn_box.addWidget(self.btn_del_sms)
        btn_box.addStretch(1)
        left_layout.addLayout(btn_box)

        # AT Command Log - ปรับแต่งให้ใช้สไตล์เดียวกับช่องอื่น ──────────────────
        left_layout.addWidget(
            QLabel("AT Command Log:",
                **{"styleSheet":
                    "font-weight:bold; color:#722f37; margin-top:10px; margin-bottom:5px;"})
        )
        
        # เปลี่ยนจาก QPlainTextEdit เป็น QTextEdit และใช้สไตล์เดียวกับ input อื่น ๆ
        self.cmd_display = QTextEdit()
        self.cmd_display.setPlaceholderText(
            "The AT commands sent will be displayed here..."
        )
        # ใช้สไตล์เดียวกับ input field อื่น ๆ แทนที่จะเป็น result display
        self.cmd_display.setStyleSheet(MainWindowStyles.get_sms_input_style())
        
        # บังคับอ่านอย่างเดียว ห้ามพิมพ์
        self.cmd_display.setReadOnly(True)
        
        # ปรับขนาดตามต้องการ
        self.cmd_display.setFixedWidth(550)
        self.cmd_display.setFixedHeight(65)
        
        # ซ่อน scrollbar ถ้าต้องการ
        self.cmd_display.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.cmd_display.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        left_layout.addWidget(self.cmd_display)
        left_layout.addStretch()

        # right side: Response - ปรับแต่งให้เป็น read-only
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0,0,0,0)
        right_layout.setSpacing(5)

        h = QHBoxLayout()
        h.addWidget(QLabel("Response:",
                    **{"styleSheet":"font-weight:bold; color:#722f37;"}))
        self.btn_hide = QPushButton("Hide")
        self.btn_hide.setStyleSheet(MainWindowStyles.get_clear_response_button_style())
        self.btn_hide.setFixedSize(60,25)
        h.addWidget(self.btn_hide)
        h.addStretch()
        right_layout.addLayout(h)

        # Response Display - ทำให้เป็น read-only และปรับสไตล์
        self.res_display = QTextEdit()
        self.res_display.setStyleSheet(MainWindowStyles.get_result_display_style())
        self.res_display.setFixedHeight(250)
        # ทำให้ Response display เป็น read-only (แสดงข้อมูลอย่างเดียว)
        self.res_display.setReadOnly(True)
        # เพิ่ม placeholder text เพื่อแสดงว่าเป็นช่องแสดงผล
        self.res_display.setPlaceholderText("Response data will be displayed here...")
        right_layout.addWidget(self.res_display)

        self.btn_clear_response = QPushButton("Clear Response")
        self.btn_clear_response.setStyleSheet(
            MainWindowStyles.get_clear_response_button_style()
        )
        self.btn_clear_response.setFixedSize(120,25)
        self.btn_clear_response.clicked.connect(self.res_display.clear)
        right_layout.addWidget(self.btn_clear_response, alignment=Qt.AlignRight)
        right_layout.addStretch()

        # place left/right in row2
        row2.addWidget(left_container, 0, Qt.AlignTop)
        row2.addWidget(right_container, 1, Qt.AlignTop)
        ag_layout.addLayout(row2)

        # ── 3) SIM Table ─────────────────────────────────────────
        self.sim_table_widget = SimTableWidget([])
        self.sim_table_widget.setStyleSheet(SimTableWidgetStyles.get_table_style())
        self.sim_table_widget.setHorizontalHeaderLabels(["Telephone", "IMSI", "ICCID", "Mobile Network", "Signal"])

        # ── Main layout ─────────────────────────────────────────
        central = QWidget()
        main_layout = QVBoxLayout(central)
        main_layout.addWidget(title)
        main_layout.addWidget(modem_group)

        # เพิ่มระยะห่าง
        main_layout.addSpacing(20)
        main_layout.addLayout(ag_layout)

        main_layout.addWidget(at_group)
        main_layout.addWidget(self.sim_table_widget)
        self.setCentralWidget(central)

        # connect signals
        self.btn_history.clicked.connect(self.show_sms_history_dialog)
        self.btn_inbox.clicked.connect(self.show_sms_history_dialog)
        self.btn_hide.clicked.connect(self.toggle_response_display)
        self.btn_help.clicked.connect(self.show_at_command_helper)
        
        # เชื่อมต่อ Enter key กับการส่งคำสั่ง AT
        self.cmd_input.returnPressed.connect(self.on_enter_pressed)

    def toggle_response_display(self):
        """ซ่อน/แสดง Response display"""
        if self.res_display.isVisible():
            self.res_display.hide()
            self.btn_hide.setText("Show")
        else:
            self.res_display.show()
            self.btn_hide.setText("Hide")

    def show_log_dialog(self, log_file=None):
        """แสดง SMS log dialog แบบเก่า (fallback)"""
        try:
            from ui.dialogs.sms_log_dialog import SmsLogDialog
            path = log_file or "log/sms_inbox_log.csv"
            dlg = SmsLogDialog(path)
            dlg.setStyleSheet(SmsLogDialogStyles.get_dialog_style())
            dlg.exec_()
        except Exception as e:
            print(f"Error opening old SMS log dialog: {e}")

    def show_sms_history_dialog(self):
        """แสดง SMS History Dialog ใหม่ - ใช้ใน ui_builder"""
        try:
            from ui.dialogs.sms_log_dialog import SmsLogDialog
            
            print("🔗 Opening SMS History Dialog from UI Builder...")
            
            # สร้าง dialog
            dialog = SmsLogDialog(parent=self)
            
            # เชื่อมต่อ signal สำหรับส่ง SMS
            def handle_send_sms_request(phone, message):
                """จัดการเมื่อมีการขอส่ง SMS จาก dialog"""
                self.phone_input.setText(phone)
                self.sms_input.setText(message)
                self.update_response_display(
                    f"📱 Auto-filled from SMS History: {phone} - {message[:50]}..."
                )
            
            dialog.send_sms_requested.connect(handle_send_sms_request)
            
            # แสดง dialog
            result = dialog.exec_()
            
            print(f"✅ SMS History Dialog closed with result: {result}")
            
        except ImportError as e:
            print(f"❌ Import Error in UI Builder: {e}")
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(
                self, 
                "Import Error", 
                f"ไม่สามารถโหลด SMS History Dialog ได้\n\nError: {e}\n\n"
                f"กรุณาตรวจสอบไฟล์:\n"
                f"• ui/dialogs/sms_log_dialog.py\n"
                f"• styles/sms_log_dialog_styles.py"
            )
        except Exception as e:
            print(f"❌ Error in UI Builder SMS History Dialog: {e}")
            import traceback
            traceback.print_exc()
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(
                self, 
                "Error", 
                f"เกิดข้อผิดพลาดในการเปิด SMS History Dialog\n\nError: {e}"
            )

    def show_at_command_helper(self):
        """แสดงหน้าต่าง AT Command Helper"""
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "AT Command Helper", 
                               "📋 AT Command Helper\n\n" +
                               "คำสั่งยอดนิยม:\n" +
                               "• AT - ทดสอบการเชื่อมต่อ\n" +
                               "• AT+CNUM - ดูเบอร์โทร\n" +
                               "• AT+CSQ - ดูระดับสัญญาณ\n" +
                               "• AT+CPIN? - ดูสถานะ SIM\n" +
                               "• AT+CMGF=1 - เปิดโหมด SMS")

    def input_cmd(self):
        """ดึงคำสั่ง AT จาก input field"""
        return self.cmd_input.text().strip()

    def on_enter_pressed(self):
        """จัดการเมื่อกด Enter ในช่อง AT Command"""
        # ส่ง signal ไปยัง main.py เพื่อส่งคำสั่ง
        if hasattr(self, '_send_at_callback'):
            self._send_at_callback()

    def set_send_at_callback(self, callback):
        """ตั้งค่า callback สำหรับส่ง AT command"""
        self._send_at_callback = callback

    def update_at_command_display(self, text):
        """อัปเดตการแสดงคำสั่ง AT ที่ส่ง"""
        self.cmd_display.append(text)
        # เลื่อน cursor ไปล่างสุดเสมอ
        cursor = self.cmd_display.textCursor()
        cursor.movePosition(cursor.End)
        self.cmd_display.setTextCursor(cursor)
        
        # บันทึกคำสั่งลงในประวัติถ้าเป็นการส่งคำสั่ง
        if "[COMMAND SENT]" in text:
            try:
                # แยกคำสั่งออกจากข้อความ
                import re
                match = re.search(r'\[COMMAND SENT\]\s*(.+)', text)
                if match:
                    command = match.group(1).strip()
                    self.save_command_to_history(command)
            except Exception as e:
                print(f"❌ Error extracting command from: {text} - {e}")

    def update_at_result_display(self, text):
        """อัปเดตผลลัพธ์ AT command (ช่องเล็กด้านบน)"""
        self.at_result_display.append(text)
        # เลื่อน cursor ไปล่างสุดเสมอ
        cursor = self.at_result_display.textCursor()
        cursor.movePosition(cursor.End)
        self.at_result_display.setTextCursor(cursor)

    def update_response_display(self, text):
        """อัปเดตการแสดงการตอบสนองทั้งหมด (ช่องใหญ่ด้านขวา)"""
        self.res_display.append(text)
        # เลื่อน cursor ไปล่างสุดเสมอ
        cursor = self.res_display.textCursor()
        cursor.movePosition(cursor.End)
        self.res_display.setTextCursor(cursor)

    def on_new_sms(self, sms):
        """จัดการ SMS ใหม่ที่เข้ามา"""
        self.update_response_display(f"[SMS] {sms}")

    def on_at_response(self, resp):
        """จัดการการตอบสนองจาก AT command"""
        self.update_response_display(f"[AT] {resp}")
    
    def load_at_command_history(self):
        """โหลดประวัติ AT command จากไฟล์"""
        try:
            history_file = "at_command_history.txt"
            
            if os.path.exists(history_file):
                with open(history_file, 'r', encoding='utf-8') as f:
                    commands = [line.strip() for line in f.readlines() if line.strip()]
                
                # เพิ่มคำสั่งลงใน dropdown (ไม่รวม item แรกที่เป็น "History ▼")
                for cmd in commands:
                    if cmd and cmd not in [self.cmd_history_combo.itemText(i) for i in range(self.cmd_history_combo.count())]:
                        self.cmd_history_combo.addItem(cmd)
                        
                print(f"📋 Loaded {len(commands)} AT commands from history")
            else:
                # สร้างไฟล์ประวัติเริ่มต้นถ้ายังไม่มี
                default_commands = [
                    "AT", "ATI", "AT+CNUM", "AT+CIMI", "AT+CCID", "AT+CSQ",
                    "AT+CMGF=1", "AT+CPIN?", "AT+CGSN", "AT+COPS?", "AT+CFUN=1",
                    "AT+CREG?", "AT+CNMI=2,2,0,0,0", "AT+CMGL=\"ALL\"", "ATE0", "ATE1"
                ]
                
                for cmd in default_commands:
                    self.cmd_history_combo.addItem(cmd)
                
                # บันทึกไฟล์ประวัติเริ่มต้น
                with open(history_file, 'w', encoding='utf-8') as f:
                    for cmd in default_commands:
                        f.write(f"{cmd}\n")
                        
                print(f"📋 Created default AT command history with {len(default_commands)} commands")
                
        except Exception as e:
            print(f"❌ Error loading AT command history: {e}")
            # เพิ่มคำสั่งพื้นฐานถ้าเกิดข้อผิดพลาด
            basic_commands = ["AT", "ATI", "AT+CNUM", "AT+CIMI", "AT+CSQ"]
            for cmd in basic_commands:
                self.cmd_history_combo.addItem(cmd)
    
    def on_history_selected(self, selected_text):
        """จัดการเมื่อเลือกคำสั่งจากประวัติ"""
        if selected_text and selected_text != "History ▼":
            self.cmd_input.setText(selected_text)
            # รีเซ็ตกลับไปที่ "History ▼"
            self.cmd_history_combo.setCurrentIndex(0)
            # แสดงข้อความใน response
            self.update_response_display(f"📋 Selected from history: {selected_text}")
    
    def save_command_to_history(self, command):
        """บันทึกคำสั่งใหม่ลงในประวัติ"""
        try:
            if not command or command.strip() == "":
                return
                
            command = command.strip().upper()  # แปลงเป็นตัวพิมพ์ใหญ่
            history_file = "at_command_history.txt"
            
            # อ่านประวัติปัจจุบัน
            existing_commands = []
            if os.path.exists(history_file):
                with open(history_file, 'r', encoding='utf-8') as f:
                    existing_commands = [line.strip() for line in f.readlines() if line.strip()]
            
            # เพิ่มคำสั่งใหม่ถ้ายังไม่มี
            if command not in existing_commands:
                existing_commands.append(command)
                
                # จำกัดจำนวนประวัติไม่เกิน 50 คำสั่ง
                if len(existing_commands) > 50:
                    existing_commands = existing_commands[-50:]
                
                # บันทึกกลับลงไฟล์
                with open(history_file, 'w', encoding='utf-8') as f:
                    for cmd in existing_commands:
                        f.write(f"{cmd}\n")
                
                # เพิ่มลงใน dropdown ถ้ายังไม่มี
                combo_items = [self.cmd_history_combo.itemText(i) for i in range(self.cmd_history_combo.count())]
                if command not in combo_items:
                    self.cmd_history_combo.addItem(command)
                
                print(f"📝 Added '{command}' to AT command history")
                
        except Exception as e:
            print(f"❌ Error saving command to history: {e}")

    def clear_at_input(self):
        """ล้างช่อง AT Command และคืนค่าเริ่มต้น"""
        self.cmd_input.clear()
        self.cmd_input.setText("AT")
        self.update_response_display("🗑️ AT Command input cleared")

def build_main_window():
    return MainWindow()