from PyQt5.QtWidgets import QMessageBox

class ATService:
    def __init__(self, serial_thread, display_cmd, display_res):
        self.thread = serial_thread
        self.display_cmd = display_cmd
        self.display_res = display_res

    def send(self, cmd: str):
        if not self.thread:
            QMessageBox.warning(None, "Notice", "No serial connection")
            return
        self.display_cmd(f"[COMMAND SENT] {cmd}")
        self.thread.send_command(cmd)
        self.display_res("[WAITING]...")
