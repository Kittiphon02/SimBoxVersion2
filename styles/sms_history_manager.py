# # styles/sms_history_manager_styles.py

# class SmsHistoryManagerStyles:
#     """Styles สำหรับ SMS History Manager"""
    
#     @staticmethod
#     def get_dialog_style():
#         """สไตล์สำหรับ dialog หลัก"""
#         return """
#             QDialog {
#                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                            stop:0 #f8f9fa, stop:1 #e9ecef);
#                 border: 3px solid #dc3545;
#                 border-radius: 12px;
#                 font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#             }
#         """
    
#     @staticmethod
#     def get_header_frame_style():
#         """สไตล์สำหรับ header frame"""
#         return """
#             QFrame {
#                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                            stop:0 #ffffff, stop:1 #f8f9fa);
#                 border: 2px solid #dee2e6;
#                 border-radius: 10px;
#                 padding: 10px;
#             }
#         """
    
#     @staticmethod
#     def get_tab_button_style():
#         """สไตล์สำหรับปุ่ม tab (แก้ไข box-shadow)"""
#         return """
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
#         """
    
#     @staticmethod
#     def get_table_style():
#         """สไตล์สำหรับตาราง"""
#         return """
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
            
#             QTableWidget::item:hover {
#                 background-color: #f8f9fa;
#             }
            
#             QScrollBar:vertical {
#                 background-color: #f1f3f4;
#                 width: 12px;
#                 border-radius: 6px;
#             }
            
#             QScrollBar::handle:vertical {
#                 background-color: #dc3545;
#                 border-radius: 6px;
#                 min-height: 20px;
#             }
            
#             QScrollBar::handle:vertical:hover {
#                 background-color: #c82333;
#             }
#         """
    
#     @staticmethod
#     def get_table_header_style():
#         """สไตล์สำหรับ header ของตาราง"""
#         return """
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
            
#             QHeaderView::section:first {
#                 border-top-left-radius: 8px;
#             }
            
#             QHeaderView::section:last {
#                 border-top-right-radius: 8px;
#                 border-right: none;
#             }
#         """
    
#     @staticmethod
#     def get_footer_frame_style():
#         """สไตล์สำหรับ footer frame"""
#         return """
#             QFrame {
#                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                            stop:0 #f8f9fa, stop:1 #e9ecef);
#                 border: 2px solid #dee2e6;
#                 border-radius: 10px;
#                 padding: 10px;
#             }
#         """
    
#     @staticmethod
#     def get_stats_label_style():
#         """สไตล์สำหรับ stats label"""
#         return """
#             QLabel {
#                 font-size: 14px;
#                 font-weight: bold;
#                 color: #2c3e50;
#                 padding: 10px 15px;
#                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                            stop:0 #ecf0f1, stop:1 #d5dbdb);
#                 border: 1px solid #bdc3c7;
#                 border-radius: 8px;
#             }
#         """
    
#     @staticmethod
#     def get_action_button_style(button_type="default"):
#         """สไตล์สำหรับปุ่ม action (แก้ไข box-shadow)"""
#         styles = {
#             "refresh": """
#                 QPushButton {
#                     background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                                stop:0 #007bff, stop:1 #0056b3);
#                     border: 2px solid #007bff;
#                     color: white;
#                     font-weight: 600;
#                     font-size: 12px;
#                     padding: 8px 16px;
#                     border-radius: 6px;
#                 }
#                 QPushButton:hover {
#                     background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                                stop:0 #0056b3, stop:1 #004085);
#                     border-color: #0056b3;
#                 }
#                 QPushButton:pressed {
#                     background-color: #004085;
#                     padding-top: 9px;
#                     padding-bottom: 7px;
#                 }
#             """,
#             "export": """
#                 QPushButton {
#                     background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                                stop:0 #28a745, stop:1 #1e7e34);
#                     border: 2px solid #28a745;
#                     color: white;
#                     font-weight: 600;
#                     font-size: 12px;
#                     padding: 8px 16px;
#                     border-radius: 6px;
#                 }
#                 QPushButton:hover {
#                     background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                                stop:0 #1e7e34, stop:1 #155724);
#                     border-color: #1e7e34;
#                 }
#                 QPushButton:pressed {
#                     background-color: #155724;
#                     padding-top: 9px;
#                     padding-bottom: 7px;
#                 }
#             """,
#             "close": """
#                 QPushButton {
#                     background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                                stop:0 #dc3545, stop:1 #c82333);
#                     border: 2px solid #dc3545;
#                     color: white;
#                     font-weight: 600;
#                     font-size: 12px;
#                     padding: 8px 16px;
#                     border-radius: 6px;
#                 }
#                 QPushButton:hover {
#                     background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
#                                stop:0 #c82333, stop:1 #a71e2a);
#                     border-color: #c82333;
#                 }
#                 QPushButton:pressed {
#                     background-color: #a71e2a;
#                     padding-top: 9px;
#                     padding-bottom: 7px;
#                 }
#             """
#         }
        
#         return styles.get(button_type, styles["default"] if "default" in styles else "")
    
#     @staticmethod
#     def get_unified_style():
#         """สไตล์รวมทั้งหมดสำหรับ SMS History Manager"""
#         return f"""
#             /* Dialog หลัก */
#             {SmsHistoryManagerStyles.get_dialog_style()}
            
#             /* Header Frame */
#             #headerFrame {{
#                 {SmsHistoryManagerStyles.get_header_frame_style().replace('QFrame', '')}
#             }}
            
#             /* Tab Buttons */
#             #tabButton {{
#                 {SmsHistoryManagerStyles.get_tab_button_style().replace('QPushButton', '')}
#             }}
            
#             /* Table */
#             #smsTable {{
#                 {SmsHistoryManagerStyles.get_table_style().replace('QTableWidget', '')}
#             }}
            
#             /* Footer Frame */
#             #footerFrame {{
#                 {SmsHistoryManagerStyles.get_footer_frame_style().replace('QFrame', '')}
#             }}
            
#             /* Stats Label */
#             #statsLabel {{
#                 {SmsHistoryManagerStyles.get_stats_label_style().replace('QLabel', '')}
#             }}
#         """

# # Helper functions สำหรับการใช้งานง่าย
# def apply_sms_history_styles(dialog):
#     """ใช้ styles กับ SMS History Manager dialog"""
#     dialog.setStyleSheet(SmsHistoryManagerStyles.get_dialog_style())
    
#     # ใช้ styles กับ components ต่างๆ
#     if hasattr(dialog, 'table'):
#         dialog.table.setStyleSheet(SmsHistoryManagerStyles.get_table_style())
#         if hasattr(dialog.table, 'horizontalHeader'):
#             dialog.table.horizontalHeader().setStyleSheet(SmsHistoryManagerStyles.get_table_header_style())
    
#     # ใช้ styles กับปุ่มต่างๆ
#     if hasattr(dialog, 'btn_refresh'):
#         dialog.btn_refresh.setStyleSheet(SmsHistoryManagerStyles.get_action_button_style("refresh"))
    
#     if hasattr(dialog, 'btn_export'):
#         dialog.btn_export.setStyleSheet(SmsHistoryManagerStyles.get_action_button_style("export"))
    
#     if hasattr(dialog, 'btn_close'):
#         dialog.btn_close.setStyleSheet(SmsHistoryManagerStyles.get_action_button_style("close"))
    
#     # ใช้ styles กับ tab buttons
#     tab_buttons = ['btn_inbox', 'btn_sent', 'btn_combined', 'btn_search']
#     for btn_name in tab_buttons:
#         if hasattr(dialog, btn_name):
#             button = getattr(dialog, btn_name)
#             button.setStyleSheet(SmsHistoryManagerStyles.get_tab_button_style())
    
#     # ใช้ styles กับ stats label
#     if hasattr(dialog, 'stats_label'):
#         dialog.stats_label.setStyleSheet(SmsHistoryManagerStyles.get_stats_label_style())
    
#     print("🎨 SMS History Manager styles applied successfully!")