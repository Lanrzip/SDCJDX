from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class TitleBar(QWidget):
    def __init__(self, parent):
        super(TitleBar, self).__init__()
        self.win = parent
        self.init_window()

    def init_window(self):
        self.isPressed = False
        self.setFixedHeight(25)
        self.init_views()
        pass

    def init_views(self):
        self.icon_label = QLabel(self)
        self.title_label = QLabel(self)

        self.min_button = QPushButton(self)
        self.close_button = QPushButton(self)
        self.min_button.setObjectName('control_button')
        self.close_button.setObjectName('control_button')

        self.min_button.setFixedSize(25, 25);
        self.close_button.setFixedSize(25, 25);

        self.icon_label.setFixedSize(30, 30);
        self.title_label.setFixedHeight(25);

        self.icon_label.setAlignment(Qt.AlignCenter);
        self.title_label.setAlignment(Qt.AlignCenter);

        self.icon_label.setPixmap(QPixmap('res/crapp.png').scaled(self.icon_label.size() - QSize(10, 10)))
        self.min_button.setIcon(QIcon('res/mini.png'));
        self.close_button.setIcon(QIcon('res/close.png'));

        self.min_button.clicked.connect(self.minimize_window)
        self.close_button.clicked.connect(self.close_window)

        self.lay = QHBoxLayout(self)
        self.setLayout(self.lay)

        self.lay.setSpacing(0)
        self.lay.setContentsMargins(0, 0, 0, 0)

        self.lay.addWidget(self.icon_label)
        self.lay.addWidget(self.title_label)
        self.lay.addWidget(self.min_button)
        self.lay.addWidget(self.close_button)

    def minimize_window(self):
        self.win.showMinimized()

    def close_window(self):
        self.win.close()

    def set_title(self, str):
        self.title_label.setText(str)

    def mousePressEvent(self, event):
        self.isPressed = True
        self.startPos = event.globalPos()
        return QWidget().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.isPressed = False
        return QWidget().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.isPressed:
            if self.win.isMaximized:
                self.win.showNormal()

            movePos = event.globalPos() - self.startPos
            self.startPos = event.globalPos()
            self.win.move(self.win.pos() + movePos)

        return QWidget().mouseMoveEvent(event)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     win = TitleBar(None)
#     win.show()
#     sys.exit(app.exec_())
#     pass
