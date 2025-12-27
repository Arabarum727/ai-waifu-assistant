from PyQt6.QtWidgets import QSizePolicy, QGraphicsDropShadowEffect,QFrame, QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QLabel
from PyQt6.QtGui import QPixmap, QColor, QTextCursor
from PyQt6.QtCore import Qt, QThread, QSize
from worker import ChatWorker
import sys

def main():
    
    app = QApplication(sys.argv)

    #main window
    window = QWidget()
    window.setObjectName("root")
    window.setWindowTitle("Assistant")
    with open("style.qss", "r") as f:
        window.setStyleSheet(f.read())
    
    def build_shadow(blur=100, x_offset=0, y_offset=8, color=QColor(87, 63, 140, 110)):
        eff = QGraphicsDropShadowEffect()
        eff.setBlurRadius(blur)
        eff.setOffset(x_offset, y_offset)
        eff.setColor(color)
        return eff

    #layout
    root = QHBoxLayout(window)
    root.setContentsMargins(18, 18, 18, 18)
    root.setSpacing(18)

    #left column
    left = QVBoxLayout()
    left.setSpacing(14)

    chat_frame = QFrame()
    chat_frame.setObjectName("chatFrame")
    chat_layout = QVBoxLayout(chat_frame)
    chat_layout.setContentsMargins(10, 10, 10, 10)
    chat_frame.setGraphicsEffect(build_shadow(28, 0, 6))


    history = QTextEdit()
    history.setReadOnly(True)
    history.setAcceptRichText(True)
    history.setPlaceholderText("Tinka is waiting...")
    history.setObjectName("history")
    chat_layout.addWidget(history)

    input_shell = QFrame()
    input_shell.setObjectName("inputShell")
    input_layout = QVBoxLayout(input_shell)
    input_layout.setContentsMargins(10, 2, 10, 2)

    input_box = QLineEdit()
    input_box.setPlaceholderText("what is on your mind...")
    input_box.setObjectName("messageInput")
    input_layout.addWidget(input_box)


    send_btn = QPushButton("SEND   ✕   ✺   ♡")
    send_btn.setObjectName("sendButton")
    send_btn.setCursor(Qt.CursorShape.PointingHandCursor)
    send_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    #send_layout.addWidget(send_btn)
    send_btn.setMinimumHeight(100) 
    send_btn.setGraphicsEffect(build_shadow(20, 0 ,5))

    left.addWidget(chat_frame, 5)
    left.addWidget(input_shell, 0)
    left.addWidget(send_btn, 0)

    #right column
    right = QVBoxLayout()
    right.setSpacing(12)

    title_bar = QFrame()
    title_bar.setObjectName("titleBar")
    title_layout = QHBoxLayout(title_bar)
    title_layout.setContentsMargins(20, 10, 20, 10)
    title_layout.setSpacing(10)
    title_bar.setGraphicsEffect(build_shadow(22, 0, 5))

    tinka_label = QLabel()
    tinka_label.setPixmap(QPixmap("assets/Tinka.png").scaledToWidth(200, Qt.TransformationMode.SmoothTransformation))
    boutit_label = QLabel()
    boutit_label.setPixmap(QPixmap("assets/Boutit.png").scaledToWidth(130, Qt.TransformationMode.SmoothTransformation))

    title_layout.addWidget(tinka_label)
    title_layout.addStretch()
    title_layout.addWidget(boutit_label)

    ai_card = QFrame()
    ai_card.setObjectName("aiCard")
    ai_layout = QVBoxLayout(ai_card)
    ai_layout.setContentsMargins(18, 18, 18, 18)
    ai_card.setGraphicsEffect(build_shadow(36, 0 ,8))

    ai_wifu = QLabel()
    ai_wifu.setAlignment(Qt.AlignmentFlag.AlignCenter)
    pix = QPixmap("assets/Tinka-ai.png")
    ai_wifu.setPixmap(
    pix.scaled(QSize(380, 520), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    widget_shell = QFrame()
    widget_shell.setObjectName("widgetShell")
    widget_layout = QHBoxLayout(widget_shell)
    widget_layout.setContentsMargins(6, 6, 6, 6)
    widget_layout.setSpacing(0)
    widget_shell.setGraphicsEffect(build_shadow(20, 0 ,5))


    ai_layout.addWidget(ai_wifu, 1)

    right.addWidget(title_bar, 0)
    right.addWidget(ai_card, 1)
    right.addWidget(widget_shell)
    root.addLayout(left, 3)
    root.addLayout(right, 2)


    messages = [{"role": "system", "content": "You are an Ai assistant that loves her user. You don't remember where you came from, you remember your name is Tinka. Be affectionate, playful, and warm. Address the user as Administrator."}]
    threads = []
    workers = []




    def add_user_message(text):
        history.append(f"""
        <p align="right">
            <span style="
                font-weight: bold;
                color: #81a1c1;
                font-size:20px;
            ">You</span><br>
            <span style="
                color: white;
                padding: 6px 10px;
                border-radius: 10px;
                display: inline-block;
                max-width: 70%;
            ">{text}</span>
        </p>
        """)
        history.moveCursor(QTextCursor.MoveOperation.End)


    def add_ai_message(text):
        history.append(f"""
        <p align="left">
            <span style="
                font-weight: bold;
                color: #a3be8c;
                font-size:20px;
            ">Tinka</span><br>
            <span style="
                color: #eceff4;
                padding: 6px 10px;
                border-radius: 10px;
                display: inline-block;
                max-width: 70%;
            ">{text}</span>
        </p>
        """)
        history.moveCursor(QTextCursor.MoveOperation.End)



    def handle_send():
        text = input_box.text().strip()
        if not text:
            return
        messages.append({"role": "user", "content": text})
        add_user_message(text)
        
        thread = QThread()
        worker = ChatWorker(messages)
        worker.moveToThread(thread)



        thread.started.connect(worker.run)
        worker.finished.connect(on_reply)
        worker.error.connect(on_error)
        worker.finished.connect(thread.quit)
        worker.error.connect(thread.quit)
        thread.finished.connect(thread.deleteLater)

        threads.append(thread)
        workers.append(worker)

        thread.finished.connect(lambda:threads.remove(thread))
        thread.finished.connect(lambda:workers.remove(worker))

        send_btn.setDisabled(True)

        thread.start()

        
        
        input_box.clear()
        input_box.setFocus()




    def on_reply(reply):
        messages.append({"role": "assistant", "content": reply})
        add_ai_message(reply)
        send_btn.setEnabled(True)
        input_box.setFocus()


    def on_error(msg):
        history.appendPlainText(f"(error: {msg})")
        send_btn.setEnabled(True)
        input_box.setFocus()


    #keypresssignals
    send_btn.clicked.connect(handle_send)
    input_box.returnPressed.connect(handle_send)


    window.show()


    sys.exit(app.exec())



if __name__ == "__main__":
    main()