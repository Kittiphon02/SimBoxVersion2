class SimTableWidgetStyles:
    """สไตล์สำหรับ SIM Table Widget - ปรับให้เหมือนรูปที่ 2"""
    
    # ==================== MAIN TABLE STYLES ====================
    @staticmethod
    def get_table_style():
        """Table Style ปรับให้เหมือนรูปที่ 2"""
        return """
            QTableWidget {
                font-family: 'Arial', sans-serif;
                font-size: 14px;
                border: none;
                background: #fff;
                gridline-color: #fff;
                selection-background-color: #e3f2fd;
                selection-color: #1976d2;
                alternate-background-color: #f8f9fa;
                outline: none;
            }
            QTableWidget::item {
                padding: 12px 8px;
                border: none;
                border-right: 1px solid #dee2e6;
                border-bottom: 1px solid #dee2e6;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
                font-weight: 500;
            }
            QTableWidget::item:hover {
                background-color: #f5f5f5;
                color: #333;
            }
        """
    
    @staticmethod
    def get_table_header_style():
        """Table Header Style - ปรับให้เหมือนรูปที่ 2 (ตัวเลข 1-5)"""
        return """
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #dc3545, stop:1 #c82333);
                font-size: 18px;
                font-weight: bold;
                padding: 12px;
                border: none;
                border-right: 1px solid #fff;
                color: white;
                text-align: center;
                min-height: 35px;
            }
            QHeaderView::section:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #c82333, stop:1 #a71e2a);
            }
            QHeaderView::section:pressed {
                background: #a71e2a;
            }
            QHeaderView::section:first {
                border-top-left-radius: 8px;
            }
            QHeaderView::section:last {
                border-top-right-radius: 8px;
                border-right: none;
            }
        """

    # ==================== CELL DATA STYLES ====================
    @staticmethod
    def get_empty_cell_style():
        """Empty Cell Style - เซลล์ว่างเหมือนรูปที่ 2"""
        return """
            QTableWidgetItem {
                color: #6c757d;
                text-align: center;
                font-size: 16px;
                font-weight: normal;
            }
        """
    
    @staticmethod
    def get_error_cell_style():
        """Error Cell Style - เซลล์แสดงข้อผิดพลาด"""
        return """
            QTableWidgetItem {
                color: #dc3545;
                text-align: center;
                font-size: 14px;
                font-weight: 500;
            }
        """
    
    @staticmethod
    def get_unknown_cell_style():
        """Unknown Cell Style - เซลล์แสดงสถานะไม่ทราบ"""
        return """
            QTableWidgetItem {
                color: #6c757d;
                text-align: center;
                font-size: 14px;
                font-weight: normal;
            }
        """

    # ==================== ROW STATE STYLES ====================
    @staticmethod
    def get_row_normal_style():
        """Row Normal Style - แถวปกติ"""
        return """
            QTableWidget::item {
                background-color: #fff;
                border-bottom: 1px solid #dee2e6;
            }
        """
    
    @staticmethod
    def get_row_alternate_style():
        """Row Alternate Style - แถวสลับสี"""
        return """
            QTableWidget::item {
                background-color: #f8f9fa;
                border-bottom: 1px solid #dee2e6;
            }
        """
    
    @staticmethod
    def get_row_selected_style():
        """Row Selected Style - แถวที่เลือก"""
        return """
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
                font-weight: 500;
                border: 1px solid #2196f3;
            }
        """
    
    @staticmethod
    def get_row_hover_style():
        """Row Hover Style - แถวเมื่อ hover"""
        return """
            QTableWidget::item:hover {
                background-color: #f5f5f5;
                color: #333;
                font-weight: 400;
            }
        """

    # ==================== SCROLLBAR STYLES ====================
    @staticmethod
    def get_vertical_scrollbar_style():
        """Vertical Scrollbar Style - แถบเลื่อนแนวตั้ง"""
        return """
            QScrollBar:vertical {
                background-color: #f8f9fa;
                width: 12px;
                border-radius: 6px;
                border: 1px solid #dee2e6;
            }
            QScrollBar::handle:vertical {
                background-color: #6c757d;
                border-radius: 5px;
                min-height: 20px;
                margin: 1px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #495057;
            }
            QScrollBar::handle:vertical:pressed {
                background-color: #343a40;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }
        """
    
    @staticmethod
    def get_horizontal_scrollbar_style():
        """Horizontal Scrollbar Style - แถบเลื่อนแนวนอน"""
        return """
            QScrollBar:horizontal {
                background-color: #f8f9fa;
                height: 12px;
                border-radius: 6px;
                border: 1px solid #dee2e6;
            }
            QScrollBar::handle:horizontal {
                background-color: #6c757d;
                border-radius: 5px;
                min-width: 20px;
                margin: 1px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #495057;
            }
            QScrollBar::handle:horizontal:pressed {
                background-color: #343a40;
            }
            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                width: 0px;
            }
            QScrollBar::add-page:horizontal,
            QScrollBar::sub-page:horizontal {
                background: none;
            }
        """

    # ==================== CONTEXT MENU STYLES ====================
    @staticmethod
    def get_context_menu_style():
        """Context Menu Style - เมนูคลิกขวา"""
        return """
            QMenu {
                background-color: #fff;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 2px;
            }
            QMenu::item {
                background-color: transparent;
                padding: 6px 12px;
                color: #212529;
                border-radius: 2px;
            }
            QMenu::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QMenu::item:pressed {
                background-color: #bbdefb;
            }
            QMenu::separator {
                height: 1px;
                background-color: #dee2e6;
                margin: 2px 8px;
            }
        """

    # ==================== TOOLTIP STYLES ====================
    @staticmethod
    def get_tooltip_style():
        """Tooltip Style - คำแนะนำเครื่องมือ"""
        return """
            QToolTip {
                background-color: #212529;
                color: white;
                border: 1px solid #495057;
                border-radius: 4px;
                padding: 5px 8px;
                font-size: 12px;
                opacity: 220;
            }
        """

    # ==================== UTILITY METHODS ====================
    @staticmethod
    def get_carrier_colors():
        """ส่งคืนสีสำหรับผู้ให้บริการ"""
        return {
            'AIS': '#28a745',
            'DTAC': '#007bff', 
            'TRUE': '#dc3545',
            'Unknown': '#6c757d'
        }
    
    @staticmethod
    def get_signal_strength_colors():
        """สีสำหรับระดับสัญญาณ"""
        return {
            'excellent': '#28a745',  # เขียว
            'good': '#17a2b8',       # ฟ้า
            'fair': '#ffc107',       # เหลือง
            'poor': '#fd7e14',       # ส้ม
            'no_signal': '#6c757d',  # เทา
            'error': '#dc3545'       # แดง
        }
    
    @staticmethod
    def get_status_icons():
        """ส่งคืนไอคอนสำหรับสถานะต่างๆ"""
        return {
            'error': '❌',
            'unknown': '❓',
            'no_signal': '📶',
            'connecting': '🔄',
            'connected': '✅'
        }
    
    @staticmethod
    def create_unified_table_style():
        """สร้างสไตล์รวมสำหรับตาราง"""
        main_style = SimTableWidgetStyles.get_table_style()
        header_style = SimTableWidgetStyles.get_table_header_style()
        scrollbar_v = SimTableWidgetStyles.get_vertical_scrollbar_style()
        scrollbar_h = SimTableWidgetStyles.get_horizontal_scrollbar_style()
        
        return f"""
            {main_style}
            {scrollbar_v}
            {scrollbar_h}
        """