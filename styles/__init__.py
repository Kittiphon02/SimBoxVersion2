# styles/__init__.py

# Import all style classes
from .loading_widget_styles import LoadingWidgetStyles
from .main_window_styles import MainWindowStyles
from .sim_table_widget_styles import SimTableWidgetStyles
from .sms_log_dialog_styles import SmsLogDialogStyles
from .sms_realtime_monitor_styles import SmsRealtimeMonitorStyles

# Create global color scheme and style utilities
class GlobalColorScheme:
    """โทนสีทั่วไปสำหรับแอพพลิเคชัน"""
    PRIMARY = '#dc3545'
    PRIMARY_LIGHT = '#f8d7da'
    PRIMARY_DARK = '#c82333'
    
    SUCCESS = '#198754'
    SUCCESS_LIGHT = '#d1e7dd'
    SUCCESS_DARK = '#157347'
    
    INFO = '#0d6efd'
    INFO_LIGHT = '#cfe2ff'
    INFO_DARK = '#0b5ed7'
    
    WARNING = '#ffc107'
    WARNING_LIGHT = '#fff3cd'
    WARNING_DARK = '#ffca2c'
    
    DANGER = '#dc3545'
    DANGER_LIGHT = '#f8d7da'
    DANGER_DARK = '#bb2d3b'

class StyleUtils:
    """ยูทิลิตี้สำหรับสร้างสไตล์"""
    
    @staticmethod
    def create_button_style(bg_color, hover_color, pressed_color):
        """สร้างสไตล์ปุ่มแบบทั่วไป"""
        return f"""
            QPushButton {{
                background: {bg_color};
                color: white;
                font-weight: 600;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 13px;
                border: none;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background: {hover_color};
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            }}
            QPushButton:pressed {{
                background: {pressed_color};
                padding-top: 7px;
            }}
        """
    
    @staticmethod
    def create_input_style(border_color, focus_color, bg_color='#fff'):
        """สร้างสไตล์ input แบบทั่วไป"""
        return f"""
            QLineEdit, QTextEdit {{
                font-size: 14px;
                border-radius: 4px;
                border: 1px solid {border_color};
                padding: 6px 8px;
                background-color: {bg_color};
                color: #212529;
            }}
            QLineEdit:focus, QTextEdit:focus {{
                border: 1px solid {focus_color};
                background-color: #fff5f5;
                outline: none;
            }}
            QLineEdit:hover, QTextEdit:hover {{
                border: 1px solid {border_color};
            }}
        """

# Export all classes for easy importing
__all__ = [
    'LoadingWidgetStyles',
    'MainWindowStyles', 
    'SimTableWidgetStyles',
    'SmsLogDialogStyles',
    'SmsRealtimeMonitorStyles',
    'GlobalColorScheme',
    'StyleUtils'
]