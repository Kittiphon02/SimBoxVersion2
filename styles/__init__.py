# styles/__init__.py

# Import เฉพาะ modules ที่มีจริง
try:
    from .main_window_styles import MainWindowStyles
    print("✅ MainWindowStyles imported successfully")
except ImportError as e:
    print(f"❌ Warning: MainWindowStyles not found - {e}")
    MainWindowStyles = None

try:
    from .sim_table_widget_styles import SimTableWidgetStyles  
    print("✅ SimTableWidgetStyles imported successfully")
except ImportError as e:
    print(f"❌ Warning: SimTableWidgetStyles not found - {e}")
    SimTableWidgetStyles = None

try:
    from .sms_log_dialog_styles import SmsLogDialogStyles
    print("✅ SmsLogDialogStyles imported successfully")
except ImportError as e:
    print(f"❌ Warning: SmsLogDialogStyles not found - {e}")
    SmsLogDialogStyles = None

try:
    from .loading_widget_styles import LoadingWidgetStyles
    print("✅ LoadingWidgetStyles imported successfully")
except ImportError as e:
    print(f"❌ Warning: LoadingWidgetStyles not found - {e}")
    LoadingWidgetStyles = None

# สร้าง StyleUtils และ GlobalColorScheme แบบ inline เพื่อความเข้ากันได้
class GlobalColorScheme:
    """Global Color Scheme สำหรับ UI"""
    PRIMARY = "#dc3545"
    PRIMARY_LIGHT = "#f8d7da" 
    PRIMARY_DARK = "#c82333"
    
    SUCCESS = "#198754"
    SUCCESS_LIGHT = "#d1e7dd"
    SUCCESS_DARK = "#157347"
    
    INFO = "#0dcaf0"
    INFO_LIGHT = "#cff4fc"
    INFO_DARK = "#087990"
    
    WARNING = "#ffc107"
    WARNING_LIGHT = "#fff3cd"
    WARNING_DARK = "#ff8800"
    
    DANGER = "#dc3545"
    DANGER_LIGHT = "#f8d7da"
    DANGER_DARK = "#b02a37"
    
    LIGHT = "#f8f9fa"
    DARK = "#212529"
    SECONDARY = "#6c757d"

class StyleUtils:
    """Utility class สำหรับสร้าง styles"""
    
    @staticmethod
    def create_button_style(bg_color, hover_color, pressed_color):
        """สร้าง button style แบบ gradient"""
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 {bg_color}, stop:1 {StyleUtils.darken_color(bg_color, 0.1)});
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 {hover_color}, stop:1 {StyleUtils.darken_color(hover_color, 0.1)});
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }}
            QPushButton:pressed {{
                background: {pressed_color};
                padding-top: 9px;
            }}
        """
    
    @staticmethod
    def darken_color(color, factor=0.1):
        """ทำให้สีเข้มขึ้น"""
        color_map = {
            "#dc3545": "#c82333",
            "#198754": "#157347",
            "#0dcaf0": "#087990", 
            "#ffc107": "#ff8800",
            "#6c757d": "#545b62"
        }
        return color_map.get(color, color)

print("🔧 Style modules initialization completed")

# Export ทุกอย่างที่มี
__all__ = ['StyleUtils', 'GlobalColorScheme']
if MainWindowStyles:
    __all__.append('MainWindowStyles')
if SimTableWidgetStyles:
    __all__.append('SimTableWidgetStyles')
if SmsLogDialogStyles:
    __all__.append('SmsLogDialogStyles')
if LoadingWidgetStyles:
    __all__.append('LoadingWidgetStyles')