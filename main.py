import sys
import asyncio
from PyQt5.QtWidgets import QApplication, QMainWindow
from MainForMusicFinder_ui import Ui_MainWindow
from app import recognize
from PyQt5.QtCore import QThread, pyqtSignal

class RecognizeThread(QThread):
    recognition_done = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        recognition_data = loop.run_until_complete(self.recognize())
        loop.close()
        self.recognition_done.emit(recognition_data)

    async def recognize(self):
        return await recognize()


class MusicFinderApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.start_listen)

    def start_listen(self):
        self.ui.pushButton.setEnabled(False)  # Disable the button during recognition
        self.ui.textBrowser.setText("Listening...")
        self.recognize_thread = RecognizeThread()
        self.recognize_thread.recognition_done.connect(self.recognition_completed)
        self.recognize_thread.start()

    def recognition_completed(self, recognition_data):
        self.ui.pushButton.setEnabled(True)  # Re-enable the button
        self.ui.textBrowser.setText(recognition_data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MusicFinderApp()
    window.show()
    sys.exit(app.exec_())
