from PyQt6.QtCore import QObject, pyqtSignal
from main import chat

class ChatWorker(QObject):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, messages):
        super().__init__()
        self.messages = list(messages)


    def run(self):
        try:
            reply = chat(self.messages)
            self.finished.emit(reply)
        except Exception as e:
            self.error.emit(str(e))
