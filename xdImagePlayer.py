import os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMenu

class xdImagePlayer(QtWidgets.QDialog):
    def __init__(self, path, interval):
        super().__init__()
        self.path = path
        self.interval = interval
        self.timer = QtCore.QTimer(self)
        self.images = {}
        self.images_path = []
        self.current_image_index = 0
        self.is_full_screen = False  # new variable to store full-screen state
        self.load_images()
        self.preload_images()
        self.setup_ui()
        self.show_image()
        self.setup_context_menu()

    def setup_context_menu(self):
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        self.context_menu = QMenu(self)
        play_action = self.context_menu.addAction("Play")
        pause_action = self.context_menu.addAction("Pause")
        prev_action = self.context_menu.addAction("Previous")
        next_action = self.context_menu.addAction("Next")
        play_action.triggered.connect(self.start_timer)
        pause_action.triggered.connect(self.stop_timer)
        prev_action.triggered.connect(self.show_prev_image)
        next_action.triggered.connect(self.show_next_image)

    def load_images(self):
        self.images_path = []
        for root, dirs, files in os.walk(self.path):
            for filename in files:
                if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
                    filepath = os.path.join(root, filename)
                    self.images_path.append(filepath)
                    #print("filepath added: " + filepath)

    def unload_images(self):
        to_be_del_index = self.current_image_index - 10
        if to_be_del_index in self.images and self.images[to_be_del_index] != None:
            del self.images[to_be_del_index]
            self.images[to_be_del_index] = None

    def preload_images(self):
        end_index = min(len(self.images_path) - 1, self.current_image_index + 10)
        for i in range(self.current_image_index, end_index):
            if (i not in self.images) or (self.images[i] == None):
                self.images[i] = QtGui.QImage(self.images_path[i])

    def setup_ui(self):
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.label = QtWidgets.QLabel()
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setMinimumSize(200, 200)

    def show_image(self):
        if not self.images[self.current_image_index]:
            self.preload_images()
        image = self.images[self.current_image_index]

        if self.is_full_screen:
            dialog_size = self.screen().size()
        else:
            dialog_size = self.size()
            
        width_factor = dialog_size.width() / image.width()
        height_factor = dialog_size.height() / image.height()
        factor = min(width_factor, height_factor)
        self.label.clear()
        scaled_image = image.scaled(image.width() * factor, image.height() * factor, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        pixmap = QtGui.QPixmap.fromImage(scaled_image)
        self.label.setPixmap(pixmap)

        if not self.is_full_screen:
            total_images = len(self.images)
            current_image_path = os.path.abspath(self.images_path[self.current_image_index])
            current_image_name = QtCore.QFileInfo(current_image_path).fileName()
            print(f"{current_image_name} ({self.current_image_index + 1}/{total_images})")

        self.preload_images()
        del image, scaled_image, pixmap
        self.unload_images()

    def start_timer(self):
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.show_next_image)
        self.timer.start(int(self.interval * 1000))

    def stop_timer(self):
        self.timer.stop()

    def show_context_menu(self, pos):
        self.context_menu.exec_(self.mapToGlobal(pos))

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.show_prev_image()
        else:
            self.show_next_image()
        self.stop_timer()
        
    def show_next_image(self):
        self.current_image_index += 1
        if self.current_image_index >= len(self.images):
            self.current_image_index = 0
        self.show_image()
        
    def show_prev_image(self):
        self.current_image_index -= 1
        if self.current_image_index < 0:
            self.current_image_index = len(self.images) - 1
        self.show_image()

    def toggle_full_screen(self):
        if not self.is_full_screen:
            self.setStyleSheet("background-color:black;")
            self.label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            self.showFullScreen()
        else:
            self.setStyleSheet("")
            self.label.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            self.showNormal()
        self.is_full_screen = not self.is_full_screen
        self.show_image()

    def mouseDoubleClickEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.toggle_full_screen()
        super().mouseDoubleClickEvent(event)
        self.show_image()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()
            
    def resizeEvent(self, event):
        self.show_image()

# Define the path to play images from
path = "."  # This specifies the current directory

# Define the interval between image displays (in seconds)
interval = 0.4

app = QtWidgets.QApplication([])
player = xdImagePlayer(path, interval)
player.show()
app.exec_()
