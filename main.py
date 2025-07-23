# main.py - Fixed Integration with SMS History Manager

import sys
from PyQt5.QtWidgets import QApplication

from services.settings_service import load_settings, save_settings
from services.serial_service import list_serial_ports, SerialMonitorThread, reload_sim
from services.at_service import ATService
from services.sms_service import SMSService
from services.sms_log import log_sms_inbox, log_sms_sent
from ui.ui_builder import build_main_window
from styles import MainWindowStyles, StyleUtils, GlobalColorScheme


def main():
    # 1) เริ่ม QApplication และโหลด settings
    app = QApplication(sys.argv)
    cfg = load_settings()

    # 2) สร้างหน้าต่างหลัก
    window = build_main_window()

    # 3) Apply main window style
    window.setStyleSheet(
        MainWindowStyles.get_main_window_style()
    )

    # 4) เตรียม Baudrate & Port Combos
    baud_list = ["9600", "19200", "38400", "57600", "115200"]
    window.baud_combo.clear()
    window.baud_combo.addItems(baud_list)
    window.baud_combo.setCurrentText(cfg.get("last_baudrate", "115200"))

    ports = list_serial_ports()
    devs = [p for p,_ in ports]  # สร้างตัวแปร devs
    # แสดง description ใน combo แต่เก็บค่า device เป็น data
    window.port_combo.clear()
    for device, description in ports:
        window.port_combo.addItem(description, device)  # แสดง description, เก็บ device

    last_port = cfg.get("last_port")
    if last_port in devs:
        # หา index ของ device และตั้งค่า
        index = window.port_combo.findData(last_port)
        if index >= 0:
            window.port_combo.setCurrentIndex(index)

    # 5) Apply Styles ให้ widget ย่อย (แก้ไข box-shadow)
    combo_qss = MainWindowStyles.get_at_combo_style()
    window.port_combo.setStyleSheet(combo_qss)
    window.baud_combo.setStyleSheet(combo_qss)

    window.phone_input.setStyleSheet(MainWindowStyles.get_phone_input_style())
    window.sms_input.setStyleSheet(MainWindowStyles.get_sms_input_style())
    window.res_display.setStyleSheet(MainWindowStyles.get_result_display_style())

    # Apply button styles (แก้ไข box-shadow)
    window.btn_send_at.setStyleSheet(MainWindowStyles.get_send_at_button_style())
    window.btn_send_sms.setStyleSheet(MainWindowStyles.get_send_sms_button_style())
    window.btn_refresh.setStyleSheet(MainWindowStyles.get_refresh_button_style())
    window.btn_history.setStyleSheet(MainWindowStyles.get_smslog_button_style())
    window.btn_monitor.setStyleSheet(
        StyleUtils.create_button_style(
            GlobalColorScheme.SUCCESS,
            GlobalColorScheme.SUCCESS_LIGHT,
            GlobalColorScheme.SUCCESS
        )
    )
    window.btn_recover.setStyleSheet(MainWindowStyles.get_send_at_button_style())
    window.btn_inbox.setStyleSheet(MainWindowStyles.get_smslog_button_style())
    window.btn_del_sms.setStyleSheet(MainWindowStyles.get_delete_button_style())
    window.btn_delete.setStyleSheet(MainWindowStyles.get_send_at_button_style())
    
    # Apply help button style (แก้ไข box-shadow)
    if hasattr(window, 'btn_help'):
        window.btn_help.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                           stop:0 #17a2b8, stop:1 #138496);
                color: white; 
                font-weight: 600; 
                border-radius: 4px;
                padding: 6px 12px; 
                font-size: 12px; 
                border: none;
                min-width: 60px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #138496, stop:1 #117a8b);
            }
            QPushButton:pressed {
                background: #117a8b;
                padding-top: 7px;
            }
        """)
    window.btn_clear_response.setStyleSheet(MainWindowStyles.get_clear_response_button_style())
    window.btn_hide.setStyleSheet(MainWindowStyles.get_clear_response_button_style())

    # Apply table styles
    from styles.sim_table_widget_styles import SimTableWidgetStyles
    window.sim_table_widget.setStyleSheet(SimTableWidgetStyles.create_unified_table_style())
    window.sim_table_widget.horizontalHeader().setStyleSheet(SimTableWidgetStyles.get_table_header_style())
    # ตั้งค่า header labels อีกครั้งหลังจาก apply styles
    window.sim_table_widget.setHorizontalHeaderLabels(["Telephone", "IMSI", "ICCID", "Mobile Network", "Signal"])

    # 6) ฟังก์ชันอัปเดต SIM Table
    def update_sim():
        port = window.port_combo.currentData() or window.port_combo.currentText()
        baud = int(window.baud_combo.currentText()) if window.baud_combo.currentText() else 115200
        sims = reload_sim(port, baud)
        window.sim_table_widget.set_data_with_debug(sims)
        # ตั้งค่า header labels อีกครั้ง
        window.sim_table_widget.setHorizontalHeaderLabels(["Telephone", "IMSI", "ICCID", "Mobile Network", "Signal"])

    # Connect port/baud change events
    window.port_combo.currentIndexChanged.connect(update_sim)
    window.baud_combo.currentIndexChanged.connect(update_sim)
    window.btn_refresh.clicked.connect(lambda: refresh_ports_and_update())
    
    def refresh_ports_and_update():
        """รีเฟรช port และอัพเดท SIM"""
        current_port = window.port_combo.currentData()  # ใช้ currentData แทน currentText
        ports = list_serial_ports()
        
        window.port_combo.clear()
        for device, description in ports:
            window.port_combo.addItem(description, device)
        
        # คืนค่า port เดิมถ้ายังมี
        current_devices = [device for device, _ in ports]
        if current_port in current_devices:
            index = window.port_combo.findData(current_port)
            if index >= 0:
                window.port_combo.setCurrentIndex(index)
        
        update_sim()
    
    # Initial SIM update
    update_sim()

    # 7) SerialMonitorThread
    thread = SerialMonitorThread(
        window.port_combo.currentText(),
        int(window.baud_combo.currentText()) if window.baud_combo.currentText() else 115200
    )
    thread.new_sms_signal.connect(window.on_new_sms)
    thread.at_response_signal.connect(window.on_at_response)

    # 8) AT Service แบบใหม่พร้อม History
    class EnhancedATService(ATService):
        def __init__(self, serial_thread, display_cmd, display_res, window):
            super().__init__(serial_thread, display_cmd, display_res)
            self.window = window
        
        def send(self, cmd: str):
            if not self.thread:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.warning(None, "Notice", "No serial connection")
                return
            
            # บันทึกคำสั่งลงในประวัติ
            self.window.save_command_to_history(cmd)
            
            # ส่งคำสั่งตามปกติ
            self.display_cmd(f"[COMMAND SENT] {cmd}")
            self.thread.send_command(cmd)
            self.display_res("[WAITING]...")

    at_srv = EnhancedATService(
        thread,
        window.update_at_command_display,
        window.update_at_result_display,
        window
    )
    
    window.btn_send_at.clicked.connect(
        lambda: at_srv.send(window.input_cmd())
    )

    # 9) SMS Service
    sms_srv = SMSService(
        thread,
        window.phone_input,
        window.sms_input,
        window.update_at_command_display,
        window.update_at_result_display
    )
    window.btn_send_sms.clicked.connect(sms_srv.send_sms)

    # ==================== 10) SMS HISTORY DIALOG INTEGRATION ====================
    def show_sms_history_dialog():
        """แสดง SMS History Dialog ใหม่"""
        try:
            # Import SMS Log Dialog
            from ui.dialogs.sms_log_dialog import SmsLogDialog
            
            print("🔗 Opening SMS History Dialog...")
            
            # สร้าง dialog
            dialog = SmsLogDialog(parent=window)
            
            # เชื่อมต่อ signal สำหรับส่ง SMS
            def handle_send_sms_request(phone, message):
                """จัดการเมื่อมีการขอส่ง SMS จาก dialog"""
                window.phone_input.setText(phone)
                window.sms_input.setText(message)
                window.update_response_display(
                    f"📱 Auto-filled from history: {phone} - {message[:50]}..."
                )
            
            dialog.send_sms_requested.connect(handle_send_sms_request)
            
            # แสดง dialog
            dialog.exec_()
            
            print("✅ SMS History Dialog closed successfully")
            
        except ImportError as e:
            print(f"❌ Import Error: {e}")
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(
                window, 
                "Import Error", 
                f"ไม่สามารถโหลด SMS History Dialog ได้\n\nError: {e}\n\n"
                f"กรุณาตรวจสอบไฟล์:\n"
                f"• ui/dialogs/sms_log_dialog.py\n"
                f"• styles/sms_log_dialog_styles.py"
            )
        except Exception as e:
            print(f"❌ Error opening SMS History Dialog: {e}")
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(
                window, 
                "Error", 
                f"เกิดข้อผิดพลาดในการเปิด SMS History Dialog\n\nError: {e}"
            )

    # เชื่อมต่อปุ่มประวัติ SMS กับฟังก์ชันใหม่
    def safe_disconnect_and_connect(button, new_function):
        """ตัดการเชื่อมต่อเดิมอย่างปลอดภัยและเชื่อมต่อใหม่"""
        try:
            button.clicked.disconnect()
        except TypeError:
            # ไม่มีการเชื่อมต่อเดิม - ไม่เป็นไร
            pass
        button.clicked.connect(new_function)

    # เชื่อมต่อปุ่มทั้งสอง
    safe_disconnect_and_connect(window.btn_history, show_sms_history_dialog)
    safe_disconnect_and_connect(window.btn_inbox, show_sms_history_dialog)
    
    print("🔗 SMS History Dialog integrated successfully!")

    # 11) Additional button connections
    # Delete button functionality
    def clear_at_input():
        window.clear_at_input()  # ใช้ฟังก์ชันจาก MainWindow
    
    window.btn_delete.clicked.connect(clear_at_input)
    
    # เชื่อมต่อ Enter key กับการส่ง AT command
    def on_cmd_enter():
        cmd = window.input_cmd()
        if cmd.strip():
            at_srv.send(cmd)
    
    # ตั้งค่า callback สำหรับ Enter key
    window.set_send_at_callback(on_cmd_enter)
    
    # Clear Response ปุ่มใหม่
    window.btn_clear_response.clicked.connect(lambda: window.res_display.clear())
    
    # Monitor button
    def show_monitor():
        try:
            from ui.sms_realtime_monitor import SmsRealtimeMonitor
            monitor = SmsRealtimeMonitor(
                window.port_combo.currentText(),
                int(window.baud_combo.currentText()),
                window,
                thread
            )
            monitor.show()
        except Exception as e:
            print(f"Error opening monitor: {e}")
    
    window.btn_monitor.clicked.connect(show_monitor)
    
    # Recovery button
    def show_recovery():
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(window, "SIM Recovery", "SIM Recovery feature coming soon!")
    
    window.btn_recover.clicked.connect(show_recovery)
    
    # Delete SMS button
    def delete_sms():
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(window, "Delete SMS", "Delete SMS feature coming soon!")
    
    window.btn_del_sms.clicked.connect(delete_sms)
    
    # เชื่อมต่อ Enter key กับการส่งคำสั่ง
    window.cmd_input.returnPressed.connect(on_cmd_enter)
    
    # เพิ่มฟีเจอร์ autocomplete สำหรับ AT command
    def setup_autocomplete():
        try:
            from PyQt5.QtWidgets import QCompleter
            
            # สร้าง completer จากประวัติคำสั่ง
            history_items = [window.cmd_history_combo.itemText(i) 
                           for i in range(1, window.cmd_history_combo.count())]  # ข้าม "History ▼"
            
            if history_items:
                completer = QCompleter(history_items)
                completer.setCaseSensitivity(0)  # Case insensitive
                window.cmd_input.setCompleter(completer)
                
                print(f"🔍 Autocomplete enabled with {len(history_items)} commands")
            
        except Exception as e:
            print(f"❌ Error setting up autocomplete: {e}")
    
    # เรียกใช้ autocomplete หลังจากโหลดประวัติเสร็จ
    setup_autocomplete()

    # 12) แสดงหน้าต่างและเริ่ม loop
    window.show()
    
    # แสดงข้อความต้อนรับ
    welcome_msg = """
═══════════════════════════════════════════════════════════════
🚀 SIM Management System เริ่มต้นการทำงานแล้ว!

📱 SMS History Manager (เวอร์ชันปรับปรุงใหม่!):
• ดูประวัติ SMS: คลิก "ดูประวัติ SMS" เพื่อเปิด SMS History Manager
• จัดการข้อมูล: แยกประเภท SMS เข้า/ส่ง/ล้มเหลว, เรียงลำดับ
• ส่งออกข้อมูล: Export เป็น Excel/CSV พร้อมกรองข้อมูล
• ดับเบิลคลิก: คลิกสองครั้งบนแถวเพื่อใช้ข้อมูลส่ง SMS

📋 คุณสมบัติ AT Command History:
• ประวัติคำสั่ง: ใช้ dropdown "History ▼" เพื่อเลือกคำสั่งที่เคยใช้
• Auto-complete: พิมพ์ AT command แล้วกด Ctrl+Space เพื่อดูคำแนะนำ  
• Enter to Send: กด Enter ในช่อง AT Command เพื่อส่งคำสั่งทันที
• Smart History: คำสั่งใหม่จะถูกบันทึกอัตโนมัติ (สูงสุด 50 คำสั่ง)

🔧 การใช้งาน:
1. เลือก USB Port และ Baudrate
2. พิมพ์คำสั่ง AT หรือเลือกจากประวัติ  
3. กด "Send AT", กด Enter, หรือใช้ปุ่ม "❓ Help"
4. ดูผลลัพธ์ในช่อง Response
5. จัดการ SMS ด้วย SMS History Manager

💡 คำสั่งยอดนิยม: AT, AT+CNUM, AT+CSQ, AT+CPIN?, AT+CMGF=1

═══════════════════════════════════════════════════════════════
    """
    
    window.update_response_display(welcome_msg)
    
    exit_code = app.exec_()

    # 13) บันทึก settings ก่อนปิด
    cfg["last_port"] = window.port_combo.currentData() or window.port_combo.currentText()
    cfg["last_baudrate"] = window.baud_combo.currentText()
    save_settings(cfg)

    sys.exit(exit_code)

if __name__ == "__main__":
    main()