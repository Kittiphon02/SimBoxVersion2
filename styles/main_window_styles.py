class MainWindowStyles:
    """สไตล์สำหรับหน้าต่างหลัก - โทนสีแดงทางการ (Clean Version)"""
    
    # ==================== COLOR PALETTE ====================
    COLORS = {
        'primary': '#dc3545',
        'primary_hover': '#c82333',
        'primary_pressed': '#a71e2a',
        'success': '#198754',
        'success_hover': '#157347',
        'success_pressed': '#146c43',
        'info': '#0d6efd',
        'info_hover': '#0b5ed7',
        'info_pressed': '#0a58ca',
        'warning': '#e74c3c',
        'warning_hover': '#c0392b',
        'warning_pressed': '#a93226',
        'secondary': '#6c757d',
        'secondary_hover': '#5a6268',
        'secondary_pressed': '#495057',
        'background': '#fdf2f2',
        'surface': '#fff5f5',
        'white': '#fff',
        'text': '#212529',
        'text_muted': '#6c757d'
    }

    # ==================== MAIN WINDOW & HEADER ====================
    @staticmethod
    def get_main_window_style():
        return f"QMainWindow {{background-color: {MainWindowStyles.COLORS['background']};}}"
    
    @staticmethod
    def get_header_style():
        return """
            font-size: 28px; font-weight: 700; color: #8b1e1e;
            letter-spacing: 1px; padding-bottom: 12px;
            text-shadow: 1px 1px 2px rgba(139, 30, 30, 0.3);
        """

    # ==================== GROUP BOX STYLES ====================
    @staticmethod
    def _get_group_style(border_color):
        """Base group box style"""
        return f"""
            QGroupBox {{
                font-size: 17px; font-weight: 600; color: #722f37;
                border: 2px solid {border_color}; border-radius: 12px;
                margin-top: 12px; padding: 16px;
                background-color: {MainWindowStyles.COLORS['surface']};
                box-shadow: 0 2px 4px rgba(220, 53, 69, 0.1);
            }}
            QGroupBox:title {{
                subcontrol-origin: margin; subcontrol-position: top center;
                padding: 0 16px; color: #a91e2c; font-weight: bold;
            }}
        """
    
    @staticmethod
    def get_modem_group_style():
        return MainWindowStyles._get_group_style(MainWindowStyles.COLORS['primary'])
    
    @staticmethod
    def get_at_group_style():
        return MainWindowStyles._get_group_style('#b91d47')

    # ==================== INPUT FIELD STYLES ====================
    @staticmethod
    def _get_input_base():
        """Base input style"""
        return f"""
            font-size: 14px; border-radius: 4px;
            border: 1px solid {MainWindowStyles.COLORS['primary']};
            background-color: {MainWindowStyles.COLORS['white']};
            color: {MainWindowStyles.COLORS['text']};
        """
    
    @staticmethod
    def _get_input_states():
        """Input states (hover, focus)"""
        return f"""
            :focus {{ border: 1px solid {MainWindowStyles.COLORS['primary_pressed']}; 
                     background-color: {MainWindowStyles.COLORS['surface']}; outline: none; }}
            :hover {{ border: 1px solid {MainWindowStyles.COLORS['primary_hover']}; }}
        """
    
    @staticmethod
    def get_input_cmd_style():
        return f"""
            QLineEdit {{ {MainWindowStyles._get_input_base()} 
                        padding: 8px 12px; border: 2px solid {MainWindowStyles.COLORS['primary']};
                        border-radius: 6px; font-size: 14px; }}
            QLineEdit{MainWindowStyles._get_input_states()}
        """
    
    @staticmethod
    def get_phone_input_style():
        return f"""
            QLineEdit {{ {MainWindowStyles._get_input_base()} 
                        padding: 8px 12px; border: 2px solid {MainWindowStyles.COLORS['primary']};
                        border-radius: 6px; font-size: 14px; }}
            QLineEdit{MainWindowStyles._get_input_states()}
        """
    
    @staticmethod
    def get_sms_input_style():
        return f"""
            QTextEdit {{ {MainWindowStyles._get_input_base()} 
                        padding: 8px; font-size: 13px; 
                        border: 2px solid {MainWindowStyles.COLORS['primary']};
                        border-radius: 6px; }}
            QTextEdit{MainWindowStyles._get_input_states()}
        """

    @staticmethod
    def get_at_combo_style():
        return f"""
            QComboBox {{ {MainWindowStyles._get_input_base()} padding: 4px 8px; min-width: 150px; }}
            QComboBox{MainWindowStyles._get_input_states()}
            QComboBox::drop-down {{ border: none; background-color: {MainWindowStyles.COLORS['primary']}; 
                                   border-top-right-radius: 4px; border-bottom-right-radius: 4px; width: 20px; }}
            QComboBox::down-arrow {{ image: none; border: 2px solid white; border-top: none; 
                                    border-left: none; width: 6px; height: 6px; margin: 4px; }}
        """

    # ==================== DISPLAY AREA STYLES ====================
    @staticmethod
    def get_command_display_style():
        return f"""
            QTextEdit {{ {MainWindowStyles._get_input_base()} padding: 6px; 
                        font-family: 'Courier New', monospace; font-size: 12px;
                        color: {MainWindowStyles.COLORS['text_muted']}; 
                        max-height: 100px; min-height: 80px; }}
            QTextEdit:focus {{ border: 1px solid {MainWindowStyles.COLORS['primary_pressed']}; outline: none; }}
        """
    
    @staticmethod
    def get_result_display_style():
        return f"""
            QTextEdit {{ {MainWindowStyles._get_input_base()} padding: 8px;
                        font-family: 'Courier New', monospace; font-size: 11px;
                        color: #d63384; border: 2px solid {MainWindowStyles.COLORS['primary']};
                        border-radius: 6px; }}
            QTextEdit:focus {{ border: 2px solid {MainWindowStyles.COLORS['primary_pressed']}; outline: none; }}
        """
    
    @staticmethod
    def get_at_result_display_style():
        return MainWindowStyles.get_result_display_style()
    
    # ==================== BUTTON STYLES ====================
    @staticmethod
    def _get_button_base():
        """Base button style"""
        return """
            color: white; font-weight: 600; border-radius: 4px;
            padding: 6px 12px; font-size: 13px; border: none; min-width: 80px;
        """
    
    @staticmethod
    def _create_button_style(color, hover_color, pressed_color, min_width=80):
        """Create button style with colors"""
        return f"""
            QPushButton {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {color}, stop:1 {hover_color});
                          {MainWindowStyles._get_button_base()} min-width: {min_width}px; }}
            QPushButton:hover {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {hover_color}, stop:1 {pressed_color});
                                box-shadow: 0 2px 4px rgba(0,0,0,0.3); }}
            QPushButton:pressed {{ background: {pressed_color}; padding-top: 7px; }}
        """
    
    @staticmethod
    def get_send_at_button_style():
        return MainWindowStyles._create_button_style(
            MainWindowStyles.COLORS['primary'],
            MainWindowStyles.COLORS['primary_hover'],
            MainWindowStyles.COLORS['primary_pressed']
        )
    
    @staticmethod
    def get_send_sms_button_style():
        return MainWindowStyles._create_button_style(
            MainWindowStyles.COLORS['success'],
            MainWindowStyles.COLORS['success_hover'],
            MainWindowStyles.COLORS['success_pressed']
        )
    
    @staticmethod
    def get_refresh_button_style():
        return MainWindowStyles._create_button_style(
            MainWindowStyles.COLORS['warning'],
            MainWindowStyles.COLORS['warning_hover'],
            MainWindowStyles.COLORS['warning_pressed'], 100
        )
    
    @staticmethod
    def get_smslog_button_style():
        return MainWindowStyles._create_button_style(
            MainWindowStyles.COLORS['info'],
            MainWindowStyles.COLORS['info_hover'],
            MainWindowStyles.COLORS['info_pressed']
        )
    
    @staticmethod
    def get_delete_button_style():
        return MainWindowStyles._create_button_style(
            MainWindowStyles.COLORS['primary'],
            '#bb2d3b', '#b02a37'
        )
    
    @staticmethod
    def get_clear_response_button_style():
        return f"""
            QPushButton {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                          stop:0 {MainWindowStyles.COLORS['secondary']}, stop:1 {MainWindowStyles.COLORS['secondary_hover']});
                          color: white; border-radius: 4px; padding: 4px 8px; border: none;
                          font-weight: 500; font-size: 12px; min-width: 60px; }}
            QPushButton:hover {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 {MainWindowStyles.COLORS['secondary_hover']}, stop:1 {MainWindowStyles.COLORS['secondary_pressed']}); }}
            QPushButton:pressed {{ background: {MainWindowStyles.COLORS['secondary_pressed']}; }}
        """

    # ==================== TABLE STYLES ====================
    @staticmethod
    def get_table_style():
        return """
            QTableWidget {
                font-family: 'Arial', sans-serif; font-size: 14px; border-radius: 6px;
                background: #fff; gridline-color: #dee2e6; border: 1px solid #dee2e6;
                selection-background-color: #e3f2fd; selection-color: #1976d2;
                alternate-background-color: #f8f9fa;
            }
            QTableWidget::item {
                padding: 8px; border-bottom: 1px solid #dee2e6; border-right: 1px solid #dee2e6;
            }
            QTableWidget::item:selected { background-color: #e3f2fd; color: #1976d2; font-weight: 500; }
            QTableWidget::item:hover { background-color: #f5f5f5; color: #333; }
        """
    
    @staticmethod
    def get_table_header_style():
        return f"""
            QHeaderView::section {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {MainWindowStyles.COLORS['primary']}, stop:1 {MainWindowStyles.COLORS['primary_hover']});
                font-size: 16px; font-weight: bold; padding: 10px; border: none;
                border-right: 1px solid #b02a37; color: white; text-align: center;
            }}
            QHeaderView::section:hover {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {MainWindowStyles.COLORS['primary_hover']}, stop:1 {MainWindowStyles.COLORS['primary_pressed']}); }}
            QHeaderView::section:pressed {{ background: {MainWindowStyles.COLORS['primary_pressed']}; }}
        """

    # ==================== UTILITY METHOD ====================
    @staticmethod
    def apply_main_window_style(win):
        """Apply main window style to window"""
        win.setStyleSheet(MainWindowStyles.get_main_window_style())