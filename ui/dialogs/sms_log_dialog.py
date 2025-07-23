from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QLineEdit,
    QPushButton, QLabel, QComboBox, QGroupBox, QSizePolicy, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QTextEdit, QFileDialog,
    QDateEdit, QCheckBox, QFrame, QSpacerItem
)
from PyQt5.QtCore import Qt, QEvent, QDate, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor
import sys, os, csv, time, re
from datetime import datetime, timedelta
from styles import SmsLogDialogStyles
import json
from pathlib import Path
import portalocker

def get_log_directory_from_settings():
    """ดึง log directory จาก settings.json"""
    try:
        from services.sms_log import get_log_directory
        return get_log_directory()
    except Exception as e:
        print(f"Error getting log directory: {e}")
        return "./log"

_cfg_path = Path(__file__).parent / "settings.json"
try:
    LOG_DIR = Path(get_log_directory_from_settings())
except:
    LOG_DIR = Path(__file__).parent / "log"

# def ensure_dir_for_file(filepath: Path):
#         """สร้างโฟลเดอร์ให้ filepath ถ้ายังไม่มี"""
#         folder = filepath.parent
#         if not folder.exists():
#             folder.mkdir(parents=True, exist_ok=True)

#         return filepath

class SmsLogDialog(QDialog):
    """หน้าต่างประวัติ SMS ที่เน้นตารางเป็นหลัก (แบบง่าย) - โทนสีแดงทางการ"""
    send_sms_requested = pyqtSignal(str, str)
    last_export_dir = None

    def __init__(self, filter_phone=None, parent=None):
        super().__init__(parent)
        
        # ==================== 1. INITIALIZATION ====================
        self.filter_phone = filter_phone
        self.all_data = []
        
        # ตั้งค่าหน้าต่าง
        self.setWindowTitle("📱 SMS History Manager | ประวัติข้อความ")
        self.resize(1000, 700)
        
        # สร้าง UI และเชื่อมต่อ signals
        self.setup_simplified_ui()
        self.setup_connections()
        self.apply_styles()  # ใช้สไตล์ใหม่
        
        # โหลดข้อมูลเริ่มต้น
        self.load_log()
        
        # เชื่อมต่อ double click event
        self.table.cellDoubleClicked.connect(self.handle_row_double_clicked)

    # ==================== 2. UI SETUP ====================
    def setup_simplified_ui(self):
        """ตั้งค่า UI แบบง่าย เหลือแค่การเลือกรายการล่าสุดหรือเก่ากว่า"""
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # ส่วนควบคุมแบบง่าย
        control_section = self.create_simple_control_section()
        layout.addWidget(control_section)
        
        # Table section (ขยายใหญ่สุด)
        table_section = self.create_maximized_table_section()
        layout.addWidget(table_section, stretch=20)
        
        # Footer section
        footer = self.create_footer_section()
        layout.addWidget(footer)

    def create_simple_control_section(self):
        """สร้างส่วนควบคุมแบบง่าย"""
        control_widget = QWidget()
        
        hlayout = QHBoxLayout()
        hlayout.setSpacing(15)
        hlayout.setContentsMargins(15, 10, 15, 10)
        
        # ป้าย "ประเภท"
        label_history = QLabel("📂 ประเภท:")
        hlayout.addWidget(label_history)

        # ComboBox เลือกประเภท SMS
        self.combo = QComboBox()
        self.combo.addItems(["📤 SMS Send", "📥 SMS Inbox", "📥 SMS Fail"])
        self.combo.setFixedWidth(150)
        self.combo.setFixedHeight(32)
        self.combo.currentIndexChanged.connect(self.load_log)
        hlayout.addWidget(self.combo)

        hlayout.addSpacing(30)

        # การเรียงลำดับ
        sort_label = QLabel("🔄 เรียงลำดับ:")
        hlayout.addWidget(sort_label)
        
        self.sort_combo = QComboBox()
        self.sort_combo.addItems([
            "รายการล่าสุด (ใหม่)",
            "รายการเก่ากว่า (เก่า)"
        ])
        self.sort_combo.setFixedWidth(200)
        self.sort_combo.setFixedHeight(32)
        self.sort_combo.currentIndexChanged.connect(self.apply_sort_filter)
        hlayout.addWidget(self.sort_combo)

        hlayout.addStretch()
        
        control_widget.setLayout(hlayout)
        # control_widget.setMaximumHeight(60)
        
        # จัดเก็บ reference สำหรับ styling
        self.control_widget = control_widget
        self.label_history = label_history
        self.sort_label = sort_label
        
        return control_widget

    def create_maximized_table_section(self):
        """สร้าง table section ที่ใหญ่ที่สุด"""
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(['📅 DATE', '🕐 TIME', '📱 PHONE', '💬 MESSAGE'])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # วันที่
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # เวลา
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # เบอร์โทร
        header.setSectionResizeMode(3, QHeaderView.Stretch)  # ข้อความ (ขยายเต็ม)
        
        self.table.setMinimumHeight(500)
        self.table.verticalHeader().setDefaultSectionSize(45)
        self.table.cellDoubleClicked.connect(self.handle_row_double_clicked)

        return self.table

    def create_footer_section(self):
        """สร้าง footer section"""
        footer_widget = QWidget()
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_layout.setContentsMargins(5, 5, 5, 5)
        
        # Status label
        self.status_label = QLabel("📊 รายการทั้งหมด: 0")
        btn_layout.addWidget(self.status_label)
        
        btn_layout.addStretch()
        
        # ปุ่มต่างๆ
        btn_refresh = self.create_button("🔄 Refresh", 120)
        btn_refresh.clicked.connect(self.load_log)
        btn_layout.addWidget(btn_refresh)

        btn_export = self.create_button("📊 Export", 120)
        btn_export.clicked.connect(self.export_to_excel)
        btn_layout.addWidget(btn_export)
        
        btn_close = self.create_button("❌ Close", 120)
        btn_close.clicked.connect(self.close)
        btn_layout.addWidget(btn_close)
        
        footer_widget.setLayout(btn_layout)
        footer_widget.setMaximumHeight(60)
        
        # จัดเก็บ reference สำหรับ styling
        self.footer_widget = footer_widget
        self.btn_refresh = btn_refresh
        self.btn_export = btn_export
        self.btn_close = btn_close
        
        return footer_widget

    def create_button(self, text, width=None):
        """สร้างปุ่มสไตล์เดียวกัน"""
        button = QPushButton(text)
        if width:
            button.setFixedWidth(width)
        button.setFixedHeight(40)
        return button

    def apply_styles(self):
        """ใช้สไตล์ใหม่โทนสีแดงทางการ"""
        # Dialog main style
        self.setStyleSheet(SmsLogDialogStyles.get_dialog_style())
        
        # Control section
        self.control_widget.setStyleSheet(SmsLogDialogStyles.get_control_section_style())
        self.label_history.setStyleSheet(SmsLogDialogStyles.get_control_label_style())
        self.sort_label.setStyleSheet(SmsLogDialogStyles.get_control_label_style())
        
        # ComboBoxes
        self.combo.setStyleSheet(SmsLogDialogStyles.get_combo_box_style())
        self.sort_combo.setStyleSheet(SmsLogDialogStyles.get_combo_box_style())
        
        # Table styles
        self.table.setStyleSheet(SmsLogDialogStyles.get_table_style())
        self.table.horizontalHeader().setStyleSheet(SmsLogDialogStyles.get_table_header_style())
        
        # Status label
        self.status_label.setStyleSheet(SmsLogDialogStyles.get_status_label_style())
        
        # Footer
        self.footer_widget.setStyleSheet(SmsLogDialogStyles.get_footer_style())
        
        # Buttons
        self.btn_refresh.setStyleSheet(SmsLogDialogStyles.get_info_button_style())
        self.btn_export.setStyleSheet(SmsLogDialogStyles.get_success_button_style())
        self.btn_close.setStyleSheet(SmsLogDialogStyles.get_danger_button_style())

    def setup_connections(self):
        """เชื่อมต่อ signals แบบง่าย"""
        # เชื่อมต่อ ComboBox เรียงลำดับกับฟังก์ชันเรียงลำดับ
        self.sort_combo.currentIndexChanged.connect(self.apply_sort_filter)

    # ==================== 3. UTILITY FUNCTIONS ====================
    def darken_color(self, color, factor=0.2):
        """ทำให้สีเข้มขึ้น"""
        return SmsLogDialogStyles.darken_color(color, factor)

    def normalize_phone(self, phone):
        """ปรับรูปแบบเบอร์โทร"""
        phone = phone.replace('-', '').replace(' ', '')
        if phone.startswith('+66'):
            phone = phone[3:]
        elif phone.startswith('66'):
            phone = phone[2:]
        return phone.lstrip('0')

    def parse_date_from_string(self, date_str):
        """แปลงข้อความวันที่เป็น datetime object"""
        try:
            if ',' in date_str:
                date_part, time_part = date_str.split(',')
                y, m, d = date_part.split('/')
                year = int(y)
                year += 2000 if year < 100 else 0
                return datetime.strptime(f"{year:04d}-{m}-{d} {time_part}", "%Y-%m-%d %H:%M:%S")
            else:
                return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except:
            return None

    def update_status_label(self):
        """อัพเดทข้อความสถานะ"""
        try:
            total_items = self.table.rowCount()
            # ตรวจสอบว่าเป็นข้อความ "ไม่มีข้อมูล" หรือไม่
            if total_items == 1:
                first_item = self.table.item(0, 0)
                if first_item and ("ไม่มี" in first_item.text() or "🔍" in first_item.text()):
                    total_items = 0
            
            self.status_label.setText(f"📊 รายการทั้งหมด: {total_items}")
        except Exception as e:
            print(f"Error updating status label: {e}")
            self.status_label.setText("📊 รายการทั้งหมด: 0")

    # ==================== 4. DATA LOADING ====================
    def load_log(self):
        """โหลดข้อมูล SMS จากไฟล์ - รองรับรูปแบบใหม่"""
        idx = self.combo.currentIndex()
        
        # ใช้ sms_log module เพื่อดึง path ที่ถูกต้อง
        try:
            from services.sms_log import get_log_file_path
            filename = "sms_sent_log.csv" if idx != 1 else "sms_inbox_log.csv"
            log_path = get_log_file_path(filename)
            
            # Debug: แสดงการใช้ path
            if '\\\\' in log_path or '//' in log_path:
                print(f"[SMS LOG DIALOG] Using network path: {log_path}")
            else:
                print(f"[SMS LOG DIALOG] Using local path: {log_path}")
                
        except Exception as e:
            print(f"Error getting log file path: {e}")
            # Fallback ถ้า function ไม่มี
            filename = "sms_sent_log.csv" if idx != 1 else "sms_inbox_log.csv"
            log_path = os.path.join("log", filename)
        
        self.all_data = []

        if not os.path.isfile(log_path):
            self.table.setRowCount(1)
            self.table.setItem(0, 0, QTableWidgetItem("📂 ไม่มีไฟล์ log"))
            self.table.setItem(0, 1, QTableWidgetItem(""))
            self.table.setItem(0, 2, QTableWidgetItem(""))
            self.table.setItem(0, 3, QTableWidgetItem("กรุณาส่ง SMS ก่อนเพื่อสร้างข้อมูล"))
            for col in range(4):
                it = self.table.item(0, col)
                it.setTextAlignment(Qt.AlignCenter)
                it.setForeground(QColor(127, 140, 141))
            self.update_status_label()
            return

        # ส่วนที่เหลือของฟังก์ชันเหมือนเดิม...
        try:
            with open(log_path, encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)  # ข้าม header

                for row in reader:
                    if idx == 1:
                        # Inbox pad ให้ครบ 3 คอลัมน์
                        dt_str, phone, message = (row + ["", ""])[:3]
                        phone = self.normalize_phone(phone) 
                        status = ""
                        # parse inbox date/time
                        dt_str = dt_str.strip('"')

                        # 1) ถ้า CSV เก็บเป็น ISO "YYYY-MM-DD HH:MM:SS"
                        m = re.match(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})$", dt_str)
                        if m:
                            dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
                            date = dt.strftime("%d/%m/%Y")
                            time = dt.strftime("%H:%M:%S")
                            datetime_obj = dt
                        # 2) ฟอร์แมตเก่าสไตล์ GSM CMT: "YY/MM/DD,HH:MM:SS+TZ"
                        elif "," in dt_str:
                            dpart, tpart = dt_str.split(",", 1)
                            tpart = tpart.split("+",1)[0]  # ตัด +TZ ออก
                            yy, mm, dd = map(int, dpart.split("/"))
                            yyyy = yy + 2000 if yy < 100 else yy
                            date = f"{dd:02d}/{mm:02d}/{yyyy}"
                            time = tpart.strip()
                            try:
                                datetime_obj = datetime.strptime(
                                    f"{yyyy}-{mm:02d}-{dd:02d} {time}",
                                    "%Y-%m-%d %H:%M:%S"
                                )
                            except:
                                datetime_obj = None
                        else:
                            # fallback
                            date, time, datetime_obj = dt_str, "", None
                    else:
                        # Send or Fail pad ให้ครบ 4 คอลัมน์
                        dt_str, phone, message, status = (row + ["", "", ""])[:4]
                        # parse outbox date/time
                        try:
                            dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
                            date = dt.strftime("%d/%m/%Y")
                            time = dt.strftime("%H:%M:%S")
                            datetime_obj = dt
                        except:
                            date, time, datetime_obj = dt_str, "", None

                    # กรองตามเบอร์ถ้ามี
                    if self.filter_phone and phone != self.filter_phone:
                        continue
                    # กรณี Fail ให้เอาเฉพาะ status != "Sent"
                    if idx == 2:
                        if not re.search(r'(fail|ล้มเหลว)', status, flags=re.IGNORECASE):
                            continue

                    self.all_data.append({
                        'date': date,
                        'time': time,
                        'phone': phone,
                        'message': message,
                        'datetime': datetime_obj,
                        'status': status
                    })

        except Exception as e:
            self.table.setRowCount(1)
            self.table.setItem(0, 0, QTableWidgetItem("❌ เกิดข้อผิดพลาด"))
            self.table.setItem(0, 1, QTableWidgetItem(""))
            self.table.setItem(0, 2, QTableWidgetItem(""))
            self.table.setItem(0, 3, QTableWidgetItem(f"ไม่สามารถอ่านไฟล์ได้: {e}"))
            for col in range(4):
                it = self.table.item(0, col)
                it.setTextAlignment(Qt.AlignCenter)
                it.setForeground(QColor(231, 76, 60))
            return

        print(f"Loaded {len(self.all_data)} records from {log_path}")  # Debug
        self.apply_sort_filter()

    # ==================== 5. DATA FILTERING & SORTING ====================
    def apply_sort_filter(self):
        """ใช้ฟิลเตอร์การเรียงลำดับ"""
        try:
            if not self.all_data:
                print("No data to sort")  # Debug
                return
                
            print(f"Sorting data, count: {len(self.all_data)}, sort index: {self.sort_combo.currentIndex()}")  # Debug
            
            # ไม่ต้องกรองอะไร แค่เรียงลำดับ
            filtered_data = self.all_data.copy()
            idx = self.combo.currentIndex()
            filtered_data = self.all_data.copy()
            # ถ้าเป็น SMS Fail ให้กรองเฉพาะที่ status ไม่ใช่ "Sent"
            if idx == 2:
                filtered_data = [d for d in filtered_data if d.get('status','').lower() != 'sent']
            
            # เรียงลำดับตามที่เลือก
            if self.sort_combo.currentIndex() == 0:  # รายการล่าสุด (ใหม่ → เก่า)
                filtered_data.sort(key=lambda x: x['datetime'] or datetime.min, reverse=True)
                print("Sorted: latest first")  # Debug
            else:  # รายการเก่ากว่า (เก่า → ใหม่)
                filtered_data.sort(key=lambda x: x['datetime'] or datetime.min, reverse=False)
                print("Sorted: oldest first")  # Debug
            
            self.display_filtered_data(filtered_data)
            self.update_status_label()
            
        except Exception as e:
            print(f"Error applying sort filter: {e}")
            import traceback
            traceback.print_exc()

    # ==================== 6. TABLE DISPLAY ====================
    def display_filtered_data(self, data):
        """แสดงข้อมูลที่กรองแล้วในตาราง"""
        self.table.setRowCount(0)
        
        if not data:
            self.table.setRowCount(1)
            self.table.setItem(0, 0, QTableWidgetItem("🔍 ไม่มีข้อมูล"))
            self.table.setItem(0, 1, QTableWidgetItem(""))
            self.table.setItem(0, 2, QTableWidgetItem(""))
            self.table.setItem(0, 3, QTableWidgetItem("ยังไม่มีประวัติ SMS ในประเภทนี้"))
            
            # จัดให้ข้อความอยู่กลาง
            for col in range(4):
                item = self.table.item(0, col)
                if item:
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setForeground(QColor(127, 140, 141))  # สีข้อความเป็นสีเทา
            return
            
        for row_idx, item in enumerate(data):
            self.table.insertRow(row_idx)
            
            # วันที่
            date_item = QTableWidgetItem(item['date'])
            date_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row_idx, 0, date_item)
            
            # เวลา
            time_item = QTableWidgetItem(item['time'])
            time_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row_idx, 1, time_item)
            
            # เบอร์โทร
            phone_item = QTableWidgetItem(item['phone'])
            phone_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row_idx, 2, phone_item)
            
            # ข้อความ
            message_item = QTableWidgetItem(item['message'])
            message_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(row_idx, 3, message_item)
            
            # เพิ่มสีสันให้แถว
            if row_idx % 2 == 0:
                # ตั้งค่า background color สำหรับแถวที่เป็นเลขคู่
                for col in range(4):
                    item = self.table.item(row_idx, col)
                    if item:
                        item.setBackground(QColor(248, 249, 250))  # สีพื้นหลังเป็นสีเทาอ่อน

    # ==================== 7. EVENT HANDLERS ====================
    def handle_row_double_clicked(self, row, col):
        """จัดการเมื่อมีการ double click บนแถว"""
        phone_item = self.table.item(row, 2)
        msg_item = self.table.item(row, 3)
        if phone_item and msg_item:
            phone = phone_item.text()
            message = msg_item.text()
            self.send_sms_requested.emit(phone, message)
        self.accept()

    def on_row_double_clicked(self, row, col):
        """จัดการเมื่อมีการ double click บนแถว (อีกวิธี)"""
        # ดึงค่าเบอร์กับข้อความจากตาราง
        phone = self.table.item(row, 2).text()
        message = self.table.item(row, 3).text()
        # ส่งสัญญาณกลับไปหน้า main
        self.send_sms_requested.emit(phone, message)
        # ปิด dialog
        self.accept()

    # ==================== 8. EXPORT FUNCTIONS ====================
    def export_to_excel(self):
        """Export ข้อมูลที่แสดงอยู่ไปยัง Excel"""
        try:
            import pandas as pd
        except ImportError:
            QMessageBox.warning(
                self, 
                "📊 Export Error", 
                "❌ ต้องติดตั้ง pandas ก่อน\n\nรันคำสั่ง: pip install pandas"
            )
            return
        
        row_count = self.table.rowCount()
        if row_count == 0 or (row_count == 1 and not self.table.item(0, 0)):
            QMessageBox.information(
                self, 
                "📊 Export", 
                "⚠️ กรุณาเลือกข้อมูลที่จะ Export ก่อน"
            )
            return
        
        data = []
        headers = ['วันที่', 'เวลา', 'เบอร์โทร', 'ข้อความ']
        
        for row in range(row_count):
            row_data = []
            empty_row = True
            for col in range(4):
                item = self.table.item(row, col)
                txt = item.text() if item else ''
                if txt and "ไม่มี" not in txt and "🔍" not in txt and "❌" not in txt:
                    empty_row = False
                row_data.append(txt)
            if not empty_row:
                data.append(row_data)
        
        if not data:
            QMessageBox.information(
                self, 
                "📊 Export", 
                "⚠️ ไม่มีข้อมูลให้ Export"
            )
            return
        
        df = pd.DataFrame(data, columns=headers)
        
        # เลือกโฟลเดอร์ default ให้เป็น log folder บน share ถ้ามี
        if SmsLogDialog.last_export_dir and os.path.exists(SmsLogDialog.last_export_dir):
            initial_dir = SmsLogDialog.last_export_dir
        elif LOG_DIR.exists():
            initial_dir = str(LOG_DIR)
        else:
            initial_dir = os.path.join(os.path.expanduser("~"), "Desktop")
        
        # สร้างชื่อไฟล์
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sms_type = "sent" if self.combo.currentIndex() == 0 else "inbox"
        filename = f"sms_{sms_type}_log_{timestamp}.xlsx"
        
        path, _ = QFileDialog.getSaveFileName(
            self,
            "📊 Export to Excel",
            os.path.join(initial_dir, filename),
            "Excel Files (*.xlsx);;CSV Files (*.csv);;All Files (*)"
        )
        
        if not path:
            return
        
        SmsLogDialog.last_export_dir = os.path.dirname(path)
        
        try:
            if path.endswith('.csv'):
                df.to_csv(path, index=False, encoding='utf-8-sig')
            else:
                df.to_excel(path, index=False)
                
            QMessageBox.information(
                self, 
                "✅ Export สำเร็จ", 
                f"📊 Export ข้อมูลเรียบร้อยแล้ว!\n\n"
                f"📁 ไฟล์: {os.path.basename(path)}\n"
                f"📂 ตำแหน่ง: {os.path.dirname(path)}\n"
                f"📋 จำนวนรายการ: {len(data)} รายการ"
            )
        except Exception as e:
            QMessageBox.critical(
                self, 
                "❌ Export Error", 
                f"💥 Export ไม่สำเร็จ!\n\n"
                f"ข้อผิดพลาด: {str(e)}\n\n"
                f"กรุณาตรวจสอบ:\n"
                f"• ไฟล์ไม่ได้เปิดอยู่ในโปรแกรมอื่น\n"
                f"• มีสิทธิ์เขียนไฟล์ในโฟลเดอร์นั้น\n"
                f"• พื้นที่ดิสก์เพียงพอ"
            )

    # ==================== 9. WINDOW EVENT HANDLERS ====================
    def closeEvent(self, event):
        """จัดการเมื่อปิดหน้าต่าง SMS Log"""
        event.accept()
        self.deleteLater()


# ==================== MAIN EXECUTION ====================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = SmsLogDialog()
    dialog.show()
    sys.exit(app.exec_())