import serial, serial.tools.list_ports, time
from PyQt5.QtCore import QThread, pyqtSignal
from services.sim_model import load_sim_data

def list_serial_ports():
    return [(p.device, p.description) for p in serial.tools.list_ports.comports()]

class SerialMonitorThread(QThread):
    at_response_signal = pyqtSignal(str)
    new_sms_signal     = pyqtSignal(str)

    def __init__(self, port, baudrate):
        super().__init__()
        self.port, self.baudrate = port, baudrate
        self._running = True

    def run(self):
        ser = serial.Serial(self.port, self.baudrate, timeout=1)
        while self._running:
            line = ser.readline().decode(errors="ignore").strip()
            if "|" in line:
                self.new_sms_signal.emit(line)
            else:
                self.at_response_signal.emit(line)
        ser.close()

    def stop(self):
        self._running = False

def reload_sim(port, baudrate):
    """ดึงข้อมูล SIM ใหม่"""
    sims = load_sim_data(port, baudrate)
    # ... query signal strength เพิ่มเติมถ้าต้องการ ...
    return sims
