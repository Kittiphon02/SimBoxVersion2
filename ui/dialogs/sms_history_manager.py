# # ui/dialogs/sms_history_manager.py

# import os
# import csv
# import json
# from datetime import datetime, timedelta
# from pathlib import Path
# from PyQt5.QtWidgets import (
#     QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
#     QPushButton, QLabel, QButtonGroup, QFileDialog, QMessageBox,
#     QHeaderView, QAbstractItemView, QSizePolicy, QWidget, QFrame
# )
# from PyQt5.QtCore import Qt, QTimer
# from PyQt5.QtGui import QFont, QPalette, QColor

# class SmsHistoryManager(QDialog):
#     """SMS History Manager - Advanced SMS Log Viewer"""
    
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.parent_window = parent
#         self.current_view = "inbox"  # inbox, sent, all
#         self.sms_data = {
#             "inbox": [],
#             "sent": [],
#             "all": []
#         }
#         self.setup_ui()
#         self.load_all_sms_data()
#         self.refresh_table()
        
#     def setup_ui(self):
#         """ตั้งค่า UI ตามแบบที่ต้องการ"""
#         self.setWindowTitle("📱 SMS History Manager | ประวัติข้อความ")
#         self.setModal(True)
#         self.resize(1000, 700)
#         self.setMinimumSize(800, 600)
        
#         # Main layout
#         main_layout = QVBoxLayout(self)
#         main_layout.setSpacing(15)
#         main_layout.setContentsMargins(20, 20, 20, 20)
        
#         # Header section with buttons
#         header_frame = self.create_header_section()
#         main_layout.addWidget(header_frame)
        
#         # Table section
#         self.table = self.create_table_widget()
#         main_layout.addWidget(self.table)
        
#         # Footer section
#         footer_frame = self.create_footer_section()
#         main_layout.addWidget(footer_frame)
        
#         # Apply styles
#         self.apply_styles()
        
#     def create_header_section(self):
#         """สร้างส่วน header พร้อมปุ่มต่างๆ"""
#         header_frame = QFrame()
#         header_frame.setFixedHeight(80)
#         header_layout = QHBoxLayout(header_frame)
#         header_layout.setContentsMargins(10, 10, 10, 10)
#         header_layout.setSpacing(15)
        
#         # Tab buttons
#         self.btn_group = QButtonGroup()
        
#         self.btn_inbox = QPushButton("📥 ประวัติข้อความเข้า")
#         self.btn_sent = QPushButton("📤 SMS Send")
#         self.btn_combined = QPushButton("📊 เรียงลำดับ")
#         self.btn_search = QPushButton("🔍 รายการค้าหาล่าสุด (ใหม่)")
        
#         # Add buttons to group
#         buttons = [self.btn_inbox, self.btn_sent, self.btn_combined, self.btn_search]
#         for i, btn in enumerate(buttons):
#             self.btn_group.addButton(btn, i)
#             btn.setCheckable(True)
#             btn.setFixedHeight(50)
#             header_layout.addWidget(btn)
        
#         # Set default selection
#         self.btn_inbox.setChecked(True)
        
#         # Connect signals
#         self.btn_inbox.clicked.connect(lambda: self.switch_view("inbox"))
#         self.btn_sent.clicked.connect(lambda: self.switch_view("sent"))
#         self.btn_combined.clicked.connect(lambda: self.switch_view("combined"))
#         self.btn_search.clicked.connect(lambda: self.switch_view("search"))
        
#         return header_frame
    
#     def create_table_widget(self):
#         """สร้าง table widget สำหรับแสดงข้อมูล SMS"""
#         table = QTableWidget()
#         table.setColumnCount(4)
#         table.setHorizontalHeaderLabels(["📅 DATE", "🕐 TIME", "📞 PHONE", "💬 MESSAGE"])
        
#         # Table settings
#         table.setAlternatingRowColors(True)
#         table.setSelectionBehavior(QAbstractItemView.SelectRows)
#         table.setSelectionMode(QAbstractItemView.MultiSelection)
#         table.setSortingEnabled(True)
#         table.setShowGrid(True)
#         table.setGridStyle(Qt.SolidLine)
        
#         # Header settings
#         header = table.horizontalHeader()
#         header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # DATE
#         header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # TIME
#         header.setSectionResizeMode(2, QHeaderView.Fixed)             # PHONE
#         header.setSectionResizeMode(3, QHeaderView.Stretch)           # MESSAGE
        
#         # Set column widths
#         table.setColumnWidth(2, 150)  # PHONE column
        
#         # Vertical header
#         table.verticalHeader().setDefaultSectionSize(35)
#         table.verticalHeader().setVisible(False)
        
#         return table
    
#     def create_footer_section(self):
#         """สร้างส่วน footer พร้อมปุ่มและสถิติ"""
#         footer_frame = QFrame()
#         footer_frame.setFixedHeight(60)
#         footer_layout = QHBoxLayout(footer_frame)
#         footer_layout.setContentsMargins(10, 10, 10, 10)
#         footer_layout.setSpacing(15)
        
#         # Statistics label
#         self.stats_label = QLabel("📊 รายการทั้งหมด: 0")
#         self.stats_label.setStyleSheet("""
#             QLabel {
#                 font-size: 14px;
#                 font-weight: bold;
#                 color: #2c3e50;
#                 padding: 8px 15px;
#                 background-color: #ecf0f1;
#                 border-radius: 6px;
#             }
#         """)
#         footer_layout.addWidget(self.stats_label)
        
#         footer_layout.addStretch()
        
#         # Action buttons
#         self.btn_refresh = QPushButton("🔄 Refresh")
#         self.btn_export = QPushButton("📁 Export")
#         self.btn_close = QPushButton("❌ Close")
        
#         action_buttons = [self.btn_refresh, self.btn_export, self.btn_close]
#         for btn in action_buttons:
#             btn.setFixedSize(100, 40)
#             footer_layout.addWidget(btn)
        
#         # Connect signals
#         self.btn_refresh.clicked.connect(self.refresh_data)
#         self.btn_export.clicked.connect(self.export_data)
#         self.btn_close.clicked.connect(self.close)
        
#         return footer_frame
    
#     def apply_styles(self):
#         """ใช้ styles แบบใหม่"""
#         try:
#             # Import styles
#             from styles.sms_history_manager_styles import apply_sms_history_styles
#             apply_sms_history_styles(self)
#             print("🎨 SMS History Manager styles applied successfully!")
#         except ImportError:
#             # Fallback styles ถ้าไม่มี styles file
#             self.apply_fallback_styles()
    
#     def apply_fallback_styles(self):
#         """Fallback styles ถ้าไม่มี styles file"""
#         dialog_style = """
#             QDialog {
#                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                            stop:0 #f8f9fa, stop:1 #e9ecef);
#                 border: 3px solid #dc3545;
#                 border-radius: 12px;
#                 font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#             }
            
#             QFrame {
#                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                            stop:0 #ffffff, stop:1 #f8f9fa);
#                 border: 2px solid #dee2e6;
#                 border-radius: 10px;
#                 padding: 10px;
#             }
            
#             QPushButton {
#                 font-size: 13px;
#                 font-weight: 600;
#                 padding: 12px 20px;
#                 border: 2px solid #dc3545;
#                 border-radius: 8px;
#                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                            stop:0 #ffffff, stop:1 #f8f9fa);
#                 color: #dc3545;
#                 min-height: 25px;
#             }
            
#             QPushButton:hover {
#                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                            stop:0 #fff5f5, stop:1 #ffebee);
#                 border-color: #c82333;
#                 box-shadow: 0 2px 4px rgba(220, 53, 69, 0.2);
#             }
            
#             QPushButton:checked {
#                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                            stop:0 #dc3545, stop:1 #c82333);
#                 color: white;
#                 border-color: #a71e2a;
#             }
            
#             QPushButton:pressed {
#                 background-color: #a71e2a;
#                 border-color: #85191f;
#                 padding-top: 13px;
#                 padding-bottom: 11px;
#             }
            
#             QTableWidget {
#                 background-color: white;
#                 border: 2px solid #dee2e6;
#                 border-radius: 10px;
#                 gridline-color: #e9ecef;
#                 font-size: 12px;
#                 font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#                 selection-background-color: #fff5f5;
#                 selection-color: #dc3545;
#                 alternate-background-color: #f8f9fa;
#             }
            
#             QTableWidget::item {
#                 padding: 10px 8px;
#                 border-bottom: 1px solid #e9ecef;
#                 border-right: 1px solid #f1f3f4;
#             }
            
#             QTableWidget::item:selected {
#                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                            stop:0 #fff5f5, stop:1 #ffebee);
#                 color: #dc3545;
#                 border: 1px solid #dc3545;
#             }
            
#             QHeaderView::section {
#                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                            stop:0 #dc3545, stop:1 #c82333);
#                 color: white;
#                 font-weight: bold;
#                 font-size: 14px;
#                 padding: 15px 10px;
#                 border: none;
#                 border-right: 1px solid #a71e2a;
#                 border-bottom: 2px solid #a71e2a;
#             }
            
#             QHeaderView::section:hover {
#                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                            stop:0 #c82333, stop:1 #a71e2a);
#             }
#         """
        
#         # Apply button-specific styles
#         button_styles = {
#             self.btn_refresh: """
#                 QPushButton {
#                     background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                                stop:0 #007bff, stop:1 #0056b3);
#                     border: 2px solid #007bff;
#                     color: white;
#                 }
#                 QPushButton:hover {
#                     background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                                stop:0 #0056b3, stop:1 #004085);
#                     border-color: #0056b3;
#                 }
#             """,
#             self.btn_export: """
#                 QPushButton {
#                     background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                                stop:0 #28a745, stop:1 #1e7e34);
#                     border: 2px solid #28a745;
#                     color: white;
#                 }
#                 QPushButton:hover {
#                     background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                                stop:0 #1e7e34, stop:1 #155724);
#                     border-color: #1e7e34;
#                 }
#             """,
#             self.btn_close: """
#                 QPushButton {
#                     background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                                stop:0 #dc3545, stop:1 #c82333);
#                     border: 2px solid #dc3545;
#                     color: white;
#                 }
#                 QPushButton:hover {
#                     background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                                stop:0 #c82333, stop:1 #a71e2a);
#                     border-color: #c82333;
#                 }
#             """
#         }
        
#         self.setStyleSheet(dialog_style)
        
#         for btn, style in button_styles.items():
#             btn.setStyleSheet(style)
    
#     def load_all_sms_data(self):
#         """โหลดข้อมูล SMS ทั้งหมดจากไฟล์ต่างๆ"""
#         try:
#             # โหลดข้อมูล SMS เข้า
#             self.sms_data["inbox"] = self.load_sms_from_file("sms_inbox_log.csv", "inbox")
            
#             # โหลดข้อมูล SMS ส่ง
#             self.sms_data["sent"] = self.load_sms_from_file("sms_sent_log.csv", "sent")
            
#             # รวมข้อมูลทั้งหมดและเรียงตามเวลา
#             all_data = self.sms_data["inbox"] + self.sms_data["sent"]
#             all_data.sort(key=lambda x: x[0], reverse=True)  # เรียงตามวันที่ล่าสุด
#             self.sms_data["combined"] = all_data
            
#             # สำหรับ search ใช้ข้อมูลล่าสุด 50 รายการ
#             self.sms_data["search"] = all_data[:50] if all_data else []
            
#             print(f"📱 Loaded SMS data: Inbox={len(self.sms_data['inbox'])}, Sent={len(self.sms_data['sent'])}")
            
#         except Exception as e:
#             print(f"❌ Error loading SMS data: {e}")
#             QMessageBox.warning(self, "Error", f"ไม่สามารถโหลดข้อมูล SMS ได้: {e}")
    
#     def load_sms_from_file(self, filename, sms_type):
#         """โหลดข้อมูล SMS จากไฟล์ CSV"""
#         try:
#             # ลองหาไฟล์ในหลายที่
#             possible_paths = [
#                 os.path.join("log", filename),
#                 os.path.join(".", "log", filename),
#                 filename
#             ]
            
#             # เพิ่มการสนับสนุน network path จาก settings
#             try:
#                 from services.sms_log import get_log_file_path
#                 network_path = get_log_file_path(filename)
#                 possible_paths.insert(0, network_path)
#             except:
#                 pass
            
#             file_path = None
#             for path in possible_paths:
#                 if os.path.exists(path):
#                     file_path = path
#                     break
            
#             if not file_path:
#                 print(f"⚠️ SMS log file not found: {filename}")
#                 return []
            
#             data = []
#             with open(file_path, 'r', encoding='utf-8-sig') as f:
#                 reader = csv.reader(f)
#                 headers = next(reader, None)  # ข้าม header
                
#                 for row in reader:
#                     if len(row) >= 3:
#                         try:
#                             # Parse datetime
#                             datetime_str = row[0].strip('"')
#                             if ',' in datetime_str:
#                                 date_part, time_part = datetime_str.split(',', 1)
#                             else:
#                                 # ถ้าไม่มี comma แสดงว่าเป็นรูปแบบ ISO
#                                 dt = datetime.fromisoformat(datetime_str.replace('T', ' '))
#                                 date_part = dt.strftime("%d/%m/%Y")
#                                 time_part = dt.strftime("%H:%M:%S")
                            
#                             phone = row[1].strip().strip('"')
#                             message = row[2].strip().strip('"')
#                             status = row[3].strip().strip('"') if len(row) > 3 else ""
                            
#                             # เพิ่มประเภท SMS
#                             display_status = f"[{sms_type.upper()}] {status}" if status else f"[{sms_type.upper()}]"
                            
#                             data.append([
#                                 date_part,
#                                 time_part,
#                                 phone,
#                                 message,
#                                 display_status
#                             ])
                            
#                         except Exception as e:
#                             print(f"⚠️ Error parsing row: {row} - {e}")
#                             continue
            
#             print(f"📄 Loaded {len(data)} records from {filename}")
#             return data
            
#         except Exception as e:
#             print(f"❌ Error loading {filename}: {e}")
#             return []
    
#     def switch_view(self, view_type):
#         """เปลี่ยนมุมมองตามปุ่มที่เลือก"""
#         self.current_view = view_type
#         self.refresh_table()
        
#         # อัปเดตสีปุ่ม
#         view_names = {
#             "inbox": "📥 ข้อความเข้า",
#             "sent": "📤 ข้อความส่ง", 
#             "combined": "📊 รวมทั้งหมด",
#             "search": "🔍 ล่าสุด (50 รายการ)"
#         }
        
#         print(f"🔄 Switched to view: {view_names.get(view_type, view_type)}")
    
#     def refresh_table(self):
#         """รีเฟรชตารางข้อมูล"""
#         try:
#             data = self.sms_data.get(self.current_view, [])
            
#             self.table.setRowCount(len(data))
            
#             for row_idx, row_data in enumerate(data):
#                 for col_idx in range(4):  # DATE, TIME, PHONE, MESSAGE
#                     item = QTableWidgetItem(str(row_data[col_idx]))
#                     item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Read-only
                    
#                     # กำหนดสีตามประเภท
#                     if len(row_data) > 4 and "[SENT]" in row_data[4]:
#                         item.setBackground(QColor("#e8f5e8"))  # เขียวอ่อนสำหรับ sent
#                     elif len(row_data) > 4 and "[INBOX]" in row_data[4]:
#                         item.setBackground(QColor("#e8f0ff"))  # น้ำเงินอ่อนสำหรับ inbox
                    
#                     self.table.setItem(row_idx, col_idx, item)
            
#             # อัปเดตสถิติ
#             self.update_statistics()
            
#             # เรียงข้อมูลตามวันที่ล่าสุด
#             self.table.sortItems(0, Qt.DescendingOrder)
            
#         except Exception as e:
#             print(f"❌ Error refreshing table: {e}")
#             QMessageBox.warning(self, "Error", f"ไม่สามารถรีเฟรชตารางได้: {e}")
    
#     def update_statistics(self):
#         """อัปเดตสถิติการแสดงผล"""
#         try:
#             current_count = len(self.sms_data.get(self.current_view, []))
#             total_inbox = len(self.sms_data.get("inbox", []))
#             total_sent = len(self.sms_data.get("sent", []))
#             total_all = total_inbox + total_sent
            
#             view_names = {
#                 "inbox": f"📥 ข้อความเข้า: {current_count}",
#                 "sent": f"📤 ข้อความส่ง: {current_count}",
#                 "combined": f"📊 รวมทั้งหมด: {current_count}",
#                 "search": f"🔍 ล่าสุด: {current_count}"
#             }
            
#             stats_text = f"{view_names.get(self.current_view, f'รายการ: {current_count}')} | รวม: เข้า {total_inbox}, ส่ง {total_sent}, ทั้งหมด {total_all}"
#             self.stats_label.setText(stats_text)
            
#         except Exception as e:
#             self.stats_label.setText("📊 ไม่สามารถคำนวณสถิติได้")
#             print(f"❌ Error updating statistics: {e}")
    
#     def refresh_data(self):
#         """รีเฟรชข้อมูลทั้งหมด"""
#         try:
#             self.load_all_sms_data()
#             self.refresh_table()
            
#             QMessageBox.information(self, "Success", "✅ รีเฟรชข้อมูลเรียบร้อยแล้ว!")
            
#         except Exception as e:
#             QMessageBox.warning(self, "Error", f"❌ ไม่สามารถรีเฟรชข้อมูลได้: {e}")
    
#     def export_data(self):
#         """ส่งออกข้อมูลปัจจุบัน"""
#         try:
#             data = self.sms_data.get(self.current_view, [])
            
#             if not data:
#                 QMessageBox.warning(self, "Warning", "ไม่มีข้อมูลให้ส่งออก")
#                 return
            
#             # เลือกไฟล์ปลายทาง
#             filename, _ = QFileDialog.getSaveFileName(
#                 self,
#                 "ส่งออกข้อมูล SMS",
#                 f"sms_export_{self.current_view}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
#                 "CSV Files (*.csv);;All Files (*)"
#             )
            
#             if filename:
#                 with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
#                     writer = csv.writer(f)
                    
#                     # เขียน header
#                     writer.writerow(["Date", "Time", "Phone", "Message", "Type"])
                    
#                     # เขียนข้อมูล
#                     for row in data:
#                         writer.writerow(row)
                
#                 QMessageBox.information(self, "Success", f"✅ ส่งออกข้อมูลเรียบร้อยแล้ว!\n\nไฟล์: {filename}\nจำนวน: {len(data)} รายการ")
        
#         except Exception as e:
#             QMessageBox.warning(self, "Error", f"❌ ไม่สามารถส่งออกข้อมูลได้: {e}")

# # Integration with main UI
# def integrate_with_main_window(main_window):
#     """เชื่อมต่อกับหน้าต่างหลัก"""
    
#     def show_sms_history_manager():
#         """แสดง SMS History Manager"""
#         try:
#             dialog = SmsHistoryManager(main_window)
#             dialog.exec_()
#         except Exception as e:
#             print(f"❌ Error opening SMS History Manager: {e}")
#             QMessageBox.warning(main_window, "Error", f"ไม่สามารถเปิด SMS History Manager ได้: {e}")
    
#     # เชื่อมต่อกับปุ่มประวัติ SMS
#     if hasattr(main_window, 'btn_history'):
#         main_window.btn_history.clicked.disconnect()  # ตัดการเชื่อมต่อเดิม
#         main_window.btn_history.clicked.connect(show_sms_history_manager)
    
#     # เชื่อมต่อกับปุ่ม SMS inbox ถ้ามี
#     if hasattr(main_window, 'btn_inbox'):
#         main_window.btn_inbox.clicked.disconnect()  # ตัดการเชื่อมต่อเดิม
#         main_window.btn_inbox.clicked.connect(show_sms_history_manager)
    
#     print("🔗 SMS History Manager integrated with main window")

# # Example usage
# if __name__ == "__main__":
#     import sys
#     from PyQt5.QtWidgets import QApplication
    
#     app = QApplication(sys.argv)
    
#     # สร้าง dialog แบบ standalone
#     dialog = SmsHistoryManager()
#     dialog.show()
    
#     sys.exit(app.exec_())