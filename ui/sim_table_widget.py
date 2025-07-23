from PyQt5.QtWidgets import (
    QTableWidget, QTableWidgetItem, QPushButton, QHeaderView, 
    QMessageBox, QLabel, QHBoxLayout, QWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
import re

# ==================== IMPORT NEW STYLES ====================
from styles import SimTableWidgetStyles


class SimTableWidget(QTableWidget):
    def __init__(self, sims, history_callback=None, port_available=True):
        super().__init__(0, 5)
        # ใช้ header ตัวเลขแบบง่ายตามรูปที่ 2
        self.setHorizontalHeaderLabels(["Telephone", "IMSI", "ICCID", "Mobile Network", "Signal"])
        self.history_callback = history_callback
        self.port_available = port_available
        
        # ตั้งค่า header
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        # ใช้สไตล์ใหม่
        self.apply_styles()
        
        # สร้างข้อมูลตัวอย่างถ้าไม่มี SIM
        if not sims:
            sims = self.create_sample_data()
        
        # **เพิ่มการ debug และตั้งค่าข้อมูล**
        self.set_data_with_debug(sims)

    def apply_styles(self):
        """ใช้สไตล์ใหม่โทนสีแดงทางการ"""
        # Main table style
        self.setStyleSheet(SimTableWidgetStyles.get_table_style())
        
        # Header style
        self.horizontalHeader().setStyleSheet(SimTableWidgetStyles.get_table_header_style())
        
        # Scrollbar styles
        main_style = SimTableWidgetStyles.get_table_style()
        scrollbar_v = SimTableWidgetStyles.get_vertical_scrollbar_style()
        scrollbar_h = SimTableWidgetStyles.get_horizontal_scrollbar_style()
        
        # รวมสไตล์ทั้งหมด
        combined_style = f"""
            {main_style}
            {scrollbar_v}
            {scrollbar_h}
        """
        
        self.setStyleSheet(combined_style)

    def create_sample_data(self):
        """สร้างข้อมูลตัวอย่างสำหรับตาราง"""
        from types import SimpleNamespace
        
        return [SimpleNamespace(
            phone="-",
            imsi="-", 
            iccid="-",
            carrier="Unknown",
            signal="❌ Error"
        )]

    def set_data_with_debug(self, sims):
        """ตั้งค่าข้อมูลในตารางพร้อม debug"""
        print(f"[TABLE DEBUG] set_data_with_debug called with {len(sims) if sims else 0} SIMs")
       
        # ตั้งค่า header labels อีกครั้ง
        self.setHorizontalHeaderLabels(["Telephone", "IMSI", "ICCID", "Mobile Network", "Signal"])
    
        try:
            self.setRowCount(0)  # ลบแค่แถวข้อมูล
            self.clearContents()  # ลบเฉพาะเนื้อหา ไม่ลบ headers
            
            if not sims:
                print("[TABLE DEBUG] No SIMs provided, using sample data")
                sims = self.create_sample_data()
            
            print(f"[TABLE DEBUG] Setting table row count to {len(sims)}")
            self.setRowCount(len(sims))
            
            for row_pos, sim in enumerate(sims):
                print(f"[TABLE DEBUG] Processing SIM {row_pos}: {type(sim)}")
                
                # ตรวจสอบ attributes ของ sim
                phone = getattr(sim, 'phone', '-')
                imsi = getattr(sim, 'imsi', '-')
                iccid = getattr(sim, 'iccid', '-')
                carrier = getattr(sim, 'carrier', 'Unknown')
                signal = getattr(sim, 'signal', '❌ Error')
                
                print(f"[TABLE DEBUG] SIM {row_pos} data: phone='{phone}', imsi='{imsi}', iccid='{iccid}', carrier='{carrier}', signal='{signal}'")
                
                # **สร้าง items อย่างปลอดภัย**
                try:
                    # Column 1: Phone/Data
                    col1_item = QTableWidgetItem(str(phone) if phone is not None else '-')
                    col1_item.setTextAlignment(Qt.AlignCenter)
                    self.setItem(row_pos, 0, col1_item)
                    
                    # Column 2: IMSI/Data
                    col2_item = QTableWidgetItem(str(imsi) if imsi is not None else '-')
                    col2_item.setTextAlignment(Qt.AlignCenter)
                    self.setItem(row_pos, 1, col2_item)
                    
                    # Column 3: ICCID/Data
                    col3_item = QTableWidgetItem(str(iccid) if iccid is not None else '-')
                    col3_item.setTextAlignment(Qt.AlignCenter)
                    self.setItem(row_pos, 2, col3_item)
                    
                    # Column 4: Carrier/Status
                    col4_item = QTableWidgetItem(str(carrier) if carrier is not None else 'Unknown')
                    col4_item.setTextAlignment(Qt.AlignCenter)
                    self.setItem(row_pos, 3, col4_item)
                    
                    # Column 5: Signal/Status
                    col5_item = QTableWidgetItem(str(signal) if signal is not None else '❌ Error')
                    col5_item.setTextAlignment(Qt.AlignCenter)
                    
                    # ตั้งสีตามสถานะ
                    if "Error" in str(signal):
                        col5_item.setForeground(QColor("#dc3545"))  # แดง
                    elif "Unknown" in str(signal):
                        col5_item.setForeground(QColor("#6c757d"))  # เทา
                    
                    self.setItem(row_pos, 4, col5_item)
                    
                except Exception as e:
                    print(f"[TABLE DEBUG] Error setting items for row {row_pos}: {e}")
                    # ตั้งค่า fallback items
                    for col in range(5):
                        if not self.item(row_pos, col):
                            fallback_item = QTableWidgetItem("-")
                            fallback_item.setTextAlignment(Qt.AlignCenter)
                            self.setItem(row_pos, col, fallback_item)
                
                # ตั้งความสูงแถว
                self.setRowHeight(row_pos, 35)
            
            print(f"[TABLE DEBUG] Table population completed. Rows: {self.rowCount()}, Columns: {self.columnCount()}")
            
            # บังคับอัพเดท
            self.update()
            self.repaint()
            
        except Exception as e:
            print(f"[TABLE DEBUG] Critical error in set_data_with_debug: {e}")
            import traceback
            traceback.print_exc()

    def set_data(self, sims):
        """ตั้งค่าข้อมูลในตาราง (wrapper สำหรับ compatibility)"""
        self.set_data_with_debug(sims)

    def get_signal_bars(self, signal_text):
        """แปลงค่าสัญญาณเป็น Unicode Signal Bars"""
        if not signal_text or signal_text in ['Unknown', 'Error', 'N/A', '']:
            return "▁▁▁▁"  # No signal
        try:
            match = re.search(r'-?(\d+)', signal_text)
            if not match:
                return "▁▁▁▁"
            dbm_value = -int(match.group(1))
            if dbm_value >= -70:                
                return "▁▃▅█"  # Excellent - 4 bars
            elif dbm_value >= -85:              
                return "▁▃▅▇"  # Good - 3 bars
            elif dbm_value >= -100:             
                return "▁▃▁▁"  # Fair - 2 bars
            elif dbm_value >= -110:             
                return "▁▁▁▁"  # Poor - 1 bar (แสดงเป็น 1 bar)
            else:
                return "▁▁▁▁"  # Very Poor - No signal
        except (ValueError, AttributeError):
            return "▁▁▁▁"

    def get_signal_color(self, signal_text):
        """กำหนดสีตามความแรงสัญญาณ - เพิ่มการจัดการสถานะ No SIM"""
        try:
            # ตรวจสอบสถานะพิเศษ
            if 'No SIM' in signal_text or 'SIM Not Ready' in signal_text:
                return '#95a5a6'  # สีเทา - ไม่มีซิม
            elif 'No Network' in signal_text:
                return '#e67e22'  # สีส้ม - ไม่มีเครือข่าย
            elif 'PIN Required' in signal_text:
                return '#f39c12'  # สีเหลือง - ต้องใส่ PIN
            elif 'Error' in signal_text:
                return '#e74c3c'  # สีแดง - ข้อผิดพลาด
            elif 'Unknown' in signal_text:
                return '#95a5a6'  # สีเทา - ไม่ทราบ
            
            # ตรวจสอบ bars pattern
            if '▁▃▅█' in signal_text:
                return '#27ae60'  # เขียวสด - Excellent
            elif '▁▃▅▇' in signal_text:
                return '#2ecc71'  # เขียว - Good
            elif '▁▃▁▁' in signal_text:
                return '#f39c12'  # เหลือง/ส้ม - Fair
            elif '▁▁▁▁' in signal_text:
                if 'No Signal' in signal_text:
                    return '#e74c3c'  # แดง - ไม่มีสัญญาณ
                else:
                    return '#95a5a6'  # เทา - Poor
            else:
                # Fallback สำหรับ dBm values
                match = re.search(r'-?(\d+)', signal_text)
                if not match:
                    return '#95a5a6'
                dbm_value = -int(match.group(1))
                if dbm_value >= -70:
                    return '#27ae60'
                elif dbm_value >= -85:
                    return '#2ecc71'
                elif dbm_value >= -100:
                    return '#f39c12'
                elif dbm_value >= -110:
                    return '#e74c3c'
                else:
                    return '#95a5a6'
        except (ValueError, AttributeError):
            return '#95a5a6'  # fallback color

    def get_signal_description(self, signal_text):
        """แปลงค่าสัญญาณเป็นคำอธิบายพร้อม Unicode Signal Bars - ปรับปรุงการจัดการสถานะ"""
        try:
            # ตรวจสอบสถานะพิเศษ
            if 'No SIM' in signal_text:
                return '❌ No SIM Card'
            elif 'SIM Not Ready' in signal_text:
                return '⚠️ SIM Not Ready'
            elif 'No Network' in signal_text:
                return '📡 No Network'
            elif 'PIN Required' in signal_text:
                return '🔒 PIN Required'
            elif 'Error' in signal_text:
                return '❌ Error'
            elif 'Unknown' in signal_text:
                return '❓ Unknown'
            
            # ตรวจสอบว่ามี Unicode bars อยู่แล้วหรือไม่
            if signal_text.startswith(('▁▃▅█', '▁▃▅▇', '▁▃▁▁', '▁▁▁▁')):
                return signal_text  # ส่งคืนตามเดิมถ้ามี bars แล้ว
            
            # ถ้ายังไม่มี bars ให้เพิ่ม
            match = re.search(r'-?(\d+)', signal_text)
            if not match:
                return f'▁▁▁▁ {signal_text}'
            
            dbm_value = -int(match.group(1))
            if dbm_value >= -70:
                return f'▁▃▅█ Excellent ({signal_text})'
            elif dbm_value >= -85:
                return f'▁▃▅▇ Good ({signal_text})'
            elif dbm_value >= -100:
                return f'▁▃▁▁ Fair ({signal_text})'
            elif dbm_value >= -110:
                return f'▁▁▁▁ Poor ({signal_text})'
            else:
                return f'▁▁▁▁ Very Poor ({signal_text})'
                
        except (ValueError, AttributeError, KeyError):
            return f'▁▁▁▁ {signal_text}'  # fallback

    def update_sms_button_enable(self, port_available):
        """อัพเดทสถานะปุ่ม SMS"""
        self.port_available = port_available
        for row in range(self.rowCount()):
            btn = self.cellWidget(row, 4)
            if isinstance(btn, QPushButton):
                btn.setEnabled(port_available)

    def contextMenuEvent(self, event):
        """สร้าง context menu เมื่อคลิกขวา"""
        from PyQt5.QtWidgets import QMenu, QAction
        
        try:
            menu = QMenu(self)
            menu.setStyleSheet(SimTableWidgetStyles.get_context_menu_style())
            
            # เพิ่ม actions
            refresh_action = QAction("🔄 Refresh Signal", self)
            refresh_action.triggered.connect(self.refresh_signal_strength)
            menu.addAction(refresh_action)
            
            menu.addSeparator()
            
            view_history_action = QAction("📱 View SMS History", self)
            view_history_action.triggered.connect(self.view_selected_history)
            menu.addAction(view_history_action)
            
            send_sms_action = QAction("📤 Send SMS", self)
            send_sms_action.triggered.connect(self.send_sms_to_selected)
            menu.addAction(send_sms_action)
            
            menu.exec_(event.globalPos())
        except Exception as e:
            print(f"[TABLE DEBUG] Error creating context menu: {e}")
    
    def refresh_signal_strength(self):
        """รีเฟรชสัญญาณ (placeholder)"""
        if hasattr(self.parent(), 'refresh_signal_strength'):
            self.parent().refresh_signal_strength()
    
    def view_selected_history(self):
        """ดูประวัติของแถวที่เลือก"""
        current_row = self.currentRow()
        if current_row >= 0:
            phone_item = self.item(current_row, 0)
            if phone_item and self.history_callback:
                self.history_callback(phone_item.text())
    
    def send_sms_to_selected(self):
        """ส่ง SMS ไปยังแถวที่เลือก"""
        current_row = self.currentRow()
        if current_row >= 0:
            phone_item = self.item(current_row, 0)
            if phone_item:
                # สามารถเพิ่ม callback สำหรับส่ง SMS ได้
                print(f"Send SMS to: {phone_item.text()}")
    
    def mousePressEvent(self, event):
        """จัดการเมื่อคลิกเมาส์"""
        super().mousePressEvent(event)
        
        # เพิ่ม tooltip เมื่อ hover ที่ cell
        item = self.itemAt(event.pos())
        if item:
            # กำหนด tooltip ตามคอลัมน์
            column = item.column()
            if column == 1:  # IMSI
                item.setToolTip(f"IMSI: {item.text()}")
            elif column == 2:  # ICCID
                item.setToolTip(f"ICCID: {item.text()}")
            elif column == 4:  # Signal
                signal_widget = self.cellWidget(item.row(), column)
                if signal_widget:
                    # ดึงข้อมูลสัญญาณจาก widget
                    signal_info = self.get_signal_tooltip_info(item.row())
                    item.setToolTip(signal_info)
    
    def get_signal_tooltip_info(self, row):
        """สร้างข้อมูล tooltip สำหรับสัญญาณ"""
        try:
            # ดึงข้อมูลจาก data source
            phone_item = self.item(row, 0)
            if phone_item:
                return f"Signal strength information for {phone_item.text()}\nClick for more details"
            return "Signal strength information"
        except Exception:
            return "Signal information not available"
    
    def wheelEvent(self, event):
        """จัดการ scroll wheel event"""
        super().wheelEvent(event)
        
        # เพิ่ม smooth scrolling effect ถ้าต้องการ
        # (สามารถปรับแต่งเพิ่มเติมได้)
        
    def resizeEvent(self, event):
        """จัดการเมื่อขนาดตารางเปลี่ยน"""
        super().resizeEvent(event)
        
        # ปรับขนาดคอลัมน์ให้เหมาะสม
        header = self.horizontalHeader()
        total_width = self.width()
        
        # กำหนดสัดส่วนคอลัมน์
        if total_width > 0:
            # Phone: 15%, IMSI: 20%, ICCID: 20%, Carrier: 15%, Signal: 30%
            header.resizeSection(0, int(total_width * 0.15))  # Phone
            header.resizeSection(1, int(total_width * 0.20))  # IMSI
            header.resizeSection(2, int(total_width * 0.20))  # ICCID
            header.resizeSection(3, int(total_width * 0.15))  # Carrier
            header.resizeSection(4, int(total_width * 0.30))  # Signal