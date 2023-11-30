import sys
import base64
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QShortcut
from core.utils import get_models
from core.paths import GUI_DIR, GUI_IMAGES
from core.api.image import TextToImage, ControlNet


W_WIDTH = 1050
W_HEIGHT = 750

I_WIDTH = 512
I_HEIGHT = 512

W_TITLE = "Image Generator"
GEN_TYPES = ("Text to Image", "ControlNet", "UpScale", "FaceFix")


class ImageGeneratorThread(QtCore.QThread):
    result_ready = QtCore.pyqtSignal(str)
    timer_out = QtCore.pyqtSignal()
    
    def __init__(
        self, 
        prompt: str, 
        model: str,
        image: str = None, 
        condition: str = None, 
        gen_type: str = "Text to Image"
    ):
        super().__init__()
        self.prompt = prompt
        self.model = model
        self.image = image
        self.condition = condition
        self.gen_type = gen_type
        
    def run(self):
        if self.gen_type == "Text to Image":
            data = TextToImage(self.prompt, model=self.model).generate_image()
        elif self.gen_type == "ControlNet" and self.image and self.condition:
            data = ControlNet(self.prompt, self.image, self.condition, model=self.model).generate_image()    
        self.result_ready.emit(data)
        self.timer_out.emit()


class MainWindow(QWidget):
    
    def __init__(self) -> None:
        super().__init__()
        
        # Window Settings
        self.setWindowTitle(W_TITLE)
        self.setMinimumSize(W_WIDTH, W_HEIGHT)
        self.setMaximumSize(W_WIDTH, W_HEIGHT)
        self.setGeometry(0, 0, W_WIDTH, W_HEIGHT)
        
        # Header Layout
        self.header_layout = QtWidgets.QVBoxLayout(self)
        self.header_layout.setSpacing(5)
        self.header_layout.setStretch(0, 3)
        self.header_layout.setStretch(1, 1)
        self.header_layout.setStretch(2, 1)
        self.header_layout.setContentsMargins(10, 10, 10, 10)
        
        # Text Layout
        text_container = QWidget()
        self.header_layout.addWidget(text_container)
        self.text_layout = QtWidgets.QHBoxLayout(text_container)
        self.text_layout.setSpacing(5)
        self.text_layout.setStretch(0, 1)
        self.text_layout.setStretch(1, 1)
        self.text_layout.setContentsMargins(0, 0, 0, 0)
        
        # Menu Layout
        menu_container = QWidget()
        self.header_layout.addWidget(menu_container)
        self.menu_layout = QtWidgets.QHBoxLayout(menu_container)
        self.menu_layout.setSpacing(5)
        self.menu_layout.setStretch(0, 1)
        self.menu_layout.setStretch(1, 1)
        self.menu_layout.setContentsMargins(0, 0, 0, 0)

        # Opts Layout
        opts_container = QWidget()
        self.header_layout.addWidget(opts_container)
        self.opts_layout = QtWidgets.QHBoxLayout(opts_container)
        self.opts_layout.setSpacing(5)
        self.opts_layout.setStretch(0, 1)
        self.opts_layout.setStretch(1, 1)
        self.opts_layout.setStretch(2, 1)
        self.opts_layout.setContentsMargins(0, 0, 0, 0)
        
        # Image Layout
        imgs_container = QWidget()
        self.header_layout.addWidget(imgs_container)
        self.imgs_layout = QtWidgets.QHBoxLayout(imgs_container)
        self.imgs_layout.setSpacing(5)
        self.imgs_layout.setStretch(0, 1)
        self.imgs_layout.setStretch(1, 1)
        self.imgs_layout.setContentsMargins(0, 0, 0, 0)
        
        # Image Opts Layout
        img_opts_container = QWidget()
        self.header_layout.addWidget(img_opts_container)
        self.img_opts_layout = QtWidgets.QHBoxLayout(img_opts_container)
        self.img_opts_layout.setSpacing(5)
        self.img_opts_layout.setStretch(0, 1)
        self.img_opts_layout.setStretch(1, 1)
        self.img_opts_layout.setContentsMargins(0, 0, 0, 0)
        
        # Prompt
        self.prompt = QtWidgets.QTextEdit()
        self.prompt.setSizePolicy(5, 5)
        self.prompt.setPlaceholderText("Prompt")
        self.text_layout.addWidget(self.prompt)
        
        # Negative Prompt
        self.nprompt = QtWidgets.QTextEdit()
        self.nprompt.setSizePolicy(5, 5)
        self.nprompt.setPlaceholderText("Negative prompt")
        self.text_layout.addWidget(self.nprompt)
        
        # Menu Buttons
        self.gen_button = QtWidgets.QPushButton()
        self.gen_button.setSizePolicy(5, 5)
        self.gen_button.setText("Generate")
        self.menu_layout.addWidget(self.gen_button)
        
        self.gen_type_button = QtWidgets.QComboBox()
        self.gen_type_button.setSizePolicy(5, 5)
        self.gen_type_button.addItems(GEN_TYPES)
        self.menu_layout.addWidget(self.gen_type_button)
        
        self.loading_movie = QtGui.QMovie(str(GUI_IMAGES.joinpath("loading.gif")))
        self.loading_movie.setScaledSize(QtCore.QSize(20, 20))
        
        self.loading_label = QtWidgets.QLabel()
        self.loading_label.setObjectName("loading_label")
        self.loading_label.setMovie(self.loading_movie)
        self.loading_label.setMaximumHeight(30)
        self.loading_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.menu_layout.insertWidget(0, self.loading_label)
        self.loading_label.hide()

        # Opts Buttons
        self.model_button = QtWidgets.QComboBox()
        self.model_button.setSizePolicy(5, 5)
        self.model_button.addItem("Models")
        self.opts_layout.addWidget(self.model_button)
        
        self.image_button = QtWidgets.QPushButton()
        self.image_button.setSizePolicy(5, 5)
        self.image_button.setText("Image")
        self.opts_layout.addWidget(self.image_button)
        
        self.condition_button = QtWidgets.QComboBox()
        self.condition_button.setSizePolicy(5, 5)
        self.condition_button.addItem("Conditions")
        self.opts_layout.addWidget(self.condition_button)
        
        # Images Labels
        self.left_img_b64 = None
        self.left_img = QtWidgets.QLabel()
        self.left_img.setFixedSize(I_WIDTH, I_HEIGHT)
        self.left_img.setSizePolicy(13, 13)
        self.left_img.setScaledContents(True)
        self.imgs_layout.addWidget(self.left_img)
        
        self.right_img_b64 = None
        self.right_img = QtWidgets.QLabel()
        self.right_img.setFixedSize(I_WIDTH, I_HEIGHT)
        self.right_img.setSizePolicy(13, 13)
        self.right_img.setScaledContents(True)
        self.imgs_layout.addWidget(self.right_img)
        
        # Image Opts Labels
        self.clear_button = QtWidgets.QPushButton()
        self.clear_button.setSizePolicy(5, 5)
        self.clear_button.setText("Clear")
        self.img_opts_layout.addWidget(self.clear_button)
        
        self.swap_imgs_button = QtWidgets.QPushButton()
        self.swap_imgs_button.setSizePolicy(5, 5)
        self.swap_imgs_button.setText("Swap Images")
        self.img_opts_layout.addWidget(self.swap_imgs_button)
        
        # Close Window
        self.close_key = QShortcut(QtGui.QKeySequence("Esc"), self)
        self.close_key.activated.connect(self.close)
        self.gen_key = QShortcut(QtGui.QKeySequence("Ctrl+G"), self)
        self.gen_key.activated.connect(self.generate_image)
        
        # Events
        self.gen_button.pressed.connect(self.generate_image)
        self.gen_type_button.currentTextChanged.connect(self.update_opts_buttons)
        self.image_button.pressed.connect(self.open_image)
        self.clear_button.pressed.connect(self.clear_imgs)
        self.swap_imgs_button.pressed.connect(self.swap_imgs)        
        
        # Startup
        with open(GUI_DIR.joinpath("ui.css")) as file: self.setStyleSheet(file.read())
        self.update_opts_buttons()
        
    def start_loading_animation(self) -> None:
        self.gen_button.hide()
        self.loading_label.show()
        self.loading_movie.start()
    
    def stop_loading_animation(self) -> None:
        self.image_thread.quit()
        self.image_thread.wait()
        self.loading_movie.stop()
        self.loading_label.hide()
        self.gen_button.setEnabled(True)
        self.gen_button.show()
    
    def generate_image(self) -> None:
        prompt = self.prompt.toPlainText().strip()
        model = self.model_button.currentText()
        gen_type = self.gen_type_button.currentText()
        
        if not prompt:
            return
        
        self.gen_button.setEnabled(False)
        self.start_loading_animation()
        
        if gen_type == "Text to Image":
            self.image_thread = ImageGeneratorThread(prompt, model)
            self.image_thread.result_ready.connect(self.update_left_image)
        elif gen_type == "ControlNet":
            image = self.left_img_b64
            condition = self.condition_button.currentText()
            self.image_thread = ImageGeneratorThread(prompt, model, image, condition, gen_type)
            self.image_thread.result_ready.connect(self.update_right_image)

        self.image_thread.timer_out.connect(self.stop_loading_animation)
        self.image_thread.start()
    
    def update_opts_buttons(self) -> None:
        models = get_models()
        curr_model = self.model_button.currentText()
        curr_type = self.gen_type_button.currentText()
        
        self.model_button.clear()
        self.condition_button.clear()
        
        if curr_type == "Text to Image":
            self.model_button.addItems(models["texttoimage"])
            self.model_button.setCurrentText(curr_model)
            self.image_button.setEnabled(False)
            self.condition_button.setEnabled(False)
        elif curr_type == "ControlNet":
            self.model_button.addItems(models["controlnet"])
            self.condition_button.addItems(models["condition"])
            self.model_button.setCurrentText(curr_model)
            self.image_button.setEnabled(True)
            self.condition_button.setEnabled(True)
        elif curr_type == "UpScale":
            self.model_button.addItems(models["upscale"])
            self.image_button.setEnabled(True)
            self.condition_button.setEnabled(False)
        else:
            self.model_button.addItems(models["facefix"])
            self.image_button.setEnabled(True)
            self.condition_button.setEnabled(False)
    
    def open_image(self) -> None:
        options = QtWidgets.QFileDialog.Options()
        filepath, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            caption="Open",
            filter="Image File (*.png;*.jpeg)",
            options=options
        )
        if filepath:
            self.update_left_image(filepath=filepath)
    
    def cvt_b64_to_pixmap(self, b64: str) -> QtGui.QPixmap:
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(QtCore.QByteArray.fromBase64(b64.encode()))
        return pixmap
    
    def update_left_image(self, b64: str = None, filepath: str = None) -> None:
        if filepath: 
            with open(filepath, "rb") as file:
                self.left_img_b64 = base64.b64encode(file.read()).decode()
            pixmap = QtGui.QPixmap(filepath)
        elif b64: 
            self.left_img_b64 = b64
            pixmap = self.cvt_b64_to_pixmap(b64)
        self.left_img.setPixmap(pixmap)
        
    def update_right_image(self, b64: str) -> None:
        self.right_img_b64 = b64
        pixmap = self.cvt_b64_to_pixmap(b64)
        self.right_img.setPixmap(pixmap)
        
    def clear_imgs(self) -> None:
        self.left_img.clear()
        self.right_img.clear()
        
    def swap_imgs(self) -> None:
        l_pixmap, r_pixmap = self.left_img.pixmap(), self.right_img.pixmap()
        if not l_pixmap or not r_pixmap: return
        l_img, r_img = l_pixmap.copy(), r_pixmap.copy()
        self.left_img.setPixmap(r_img)
        self.right_img.setPixmap(l_img)
        
        
def start_application():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())