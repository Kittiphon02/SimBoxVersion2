import time
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QMessageBox
from PyQt5.QtCore import QTimer
from styles.loading_widget_styles import LoadingWidgetStyles
from ui.loading_widget import LoadingWidget
from services.log_service import log_sms_sent

class SMSService:
    def __init__(self, serial_thread, phone_input, sms_input, display_cmd, display_res):
        self.thread = serial_thread
        self.phone_input = phone_input
        self.sms_input = sms_input
        self.display_cmd = display_cmd
        self.display_res = display_res

    def send_sms(self):
        number = self.phone_input.text().strip()
        text   = self.sms_input.toPlainText().strip()
        if not (self.thread and number and text):
            QMessageBox.warning(None, "Notice", "Please check connection, number and message")
            return
        dlg = QDialog()
        dlg.setStyleSheet(LoadingWidgetStyles.get_dialog_style())
        dlg.setModal(True)
        dlg.setWindowTitle("Sending SMS…")
        w = LoadingWidget()
        w.finished.connect(lambda ok: self._on_finish(ok, dlg, number, text))
        layout = QVBoxLayout(dlg)
        layout.addWidget(w)
        dlg.show()
        w.start_sending()
    
    def _on_finish(self, success, dlg, number, text):
        if success:
            log_sms_sent(number, text, status="Sent")
        else:
            log_sms_sent(number, text, status="Failed")
        QTimer.singleShot(500, dlg.accept)
