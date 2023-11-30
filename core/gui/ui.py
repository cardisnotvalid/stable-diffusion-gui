import typing
from PyQt5 import QtWidgets, QtCore, QtGui
from core.paths import GUI_CSS, GUI_IMAGES


class VLayout(QtWidgets.QVBoxLayout):
    def __init__(
        self, 
        parent: typing.Optional[QtWidgets.QWidget],
        *,
        rows: typing.Optional[int] = 1,
        spacing: typing.Optional[int] = 5,
    ) -> None:
        super().__init__(parent)
        
        for idx in range(rows): self.setStretch(idx, 1)
        self.setSpacing(spacing)
        self.setContentsMargins(10, 10, 10, 10)
        
    def addWidgets(self, *widgets: QtWidgets.QWidget) -> None:
        if len(widgets) > 1: 
            for widget in widgets: self.addWidget(widget)
        else: 
            self.addWidget(widgets[0])


class HLayout(QtWidgets.QHBoxLayout):
    def __init__(
        self, 
        parent: typing.Optional[QtWidgets.QWidget],
        *,
        columns: typing.Optional[int] = 1,
        spacing: typing.Optional[int] = 5,
    ) -> None:
        super().__init__(parent)
        
        for idx in range(columns): self.setStretch(idx, 1)
        self.setSpacing(spacing)
        self.setContentsMargins(0, 0, 0, 0)

    def addWidgets(self, *widgets: QtWidgets.QWidget) -> None:
        if len(widgets) > 1: 
            for widget in widgets: self.addWidget(widget)
        else: 
            self.addWidget(widgets[0])


class TextEdit(QtWidgets.QTextEdit):
    def __init__(
        self, 
        parent: typing.Optional[QtWidgets.QWidget] = None,
        placeholder: typing.Optional[str] = None
    ) -> None:
        super().__init__(parent)
        
        self.setSizePolicy(5, 5)
        self.setPlaceholderText(placeholder)


class Button(QtWidgets.QPushButton):
    def __init__(
        self, 
        parent: typing.Optional[QtWidgets.QWidget] = None, 
        text: typing.Optional[str] = None,
        height: typing.Optional[int] = 30,
    ) -> None:
        super().__init__(parent=parent, text=text)
        
        self.setSizePolicy(5, 5)
        self.setFixedHeight(height)


class ComboBox(QtWidgets.QComboBox):
    def __init__(
        self, 
        parent: typing.Optional[QtWidgets.QWidget] = None,
        height: typing.Optional[int] = 30,
    ) -> None:
        super().__init__(parent)
        
        self.setSizePolicy(5, 5)
        self.setFixedHeight(height)
        

class Label(QtWidgets.QLabel):
    def __init__(
        self,
        parent: typing.Optional[QtWidgets.QWidget] = None,
        text: typing.Optional[str] = None,
        width: typing.Optional[int] = None,
        height: typing.Optional[int] = None,
        image: typing.Optional[bool] = False,
    ) -> None:
        super().__init__(parent=parent)
    
        self.setObjectName(text)
        self.setContentsMargins(0, 0, 0, 0)
        
        if width: self.setFixedWidth(width)
        if height: self.setFixedHeight(height)
        if image: self.setSizePolicy(0, 0); self.setScaledContents(True)


class UI(QtWidgets.QWidget):
    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)
        
        self.setFixedSize(1050, 750)
        self.setWindowTitle("Image Generator")
        
        self.__initui__()
        
        with open(GUI_CSS.joinpath("ui.css")) as f: self.setStyleSheet(f.read())
    
    def __initui__(self) -> None:
        self.create_containers()
        self.create_layouts()
        self.create_widgets()
    
    def create_containers(self) -> None:
        self.cont_text = QtWidgets.QWidget()
        self.cont_menu = QtWidgets.QWidget()
        self.cont_opts = QtWidgets.QWidget()
        self.cont_imgs = QtWidgets.QWidget()
        self.cont_bottom = QtWidgets.QWidget()
    
    def create_layouts(self) -> None:
        self.layout_main = VLayout(self, rows=5)
        self.layout_main.setObjectName("main_layout")
        
        self.layout_text = HLayout(self.cont_text, columns=2)
        self.layout_menu = HLayout(self.cont_menu, columns=2)
        self.layout_opts = HLayout(self.cont_opts, columns=3)
        self.layout_imgs = HLayout(self.cont_imgs, columns=2)
        self.layout_bottom = HLayout(self.cont_bottom, columns=2)
        
        self.layout_main.addWidgets(
            self.cont_text, self.cont_menu, self.cont_opts, self.cont_imgs, self.cont_bottom)
    
    def create_widgets(self) -> None:
        self.prompt = TextEdit(placeholder="Prompt")
        self.nprompt = TextEdit(placeholder="Negative Prompt")
        
        self.btn_generate = Button(text="Generate")
        self.btn_generate_type = ComboBox()
        
        self.btn_model = ComboBox()
        self.btn_image = Button(text="Image")
        self.btn_condition = ComboBox()
        
        self.left_img = Label(height=512, width=512, image=True)
        self.right_img = Label(height=512, width=512, image=True)
        self.left_img_b64 = None
        self.right_img_b64 = None
        
        self.btn_clear = Button(text="Clear")
        self.btn_swap = Button(text="Swap Images")
        
        self.loading_movie = QtGui.QMovie(str(GUI_IMAGES.joinpath("loading.gif")))
        self.loading_movie.setScaledSize(QtCore.QSize(20, 20))
        
        self.loading_label = Label(text="loading_label", height=30)
        self.loading_label.setMovie(self.loading_movie)
        self.loading_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.loading_label.hide()
        
        self.layout_text.addWidgets(self.prompt, self.nprompt)
        self.layout_menu.addWidgets(self.btn_generate, self.btn_generate_type)
        self.layout_opts.addWidgets(self.btn_model, self.btn_image, self.btn_condition)
        self.layout_imgs.addWidgets(self.left_img, self.right_img)
        self.layout_bottom.addWidgets(self.btn_clear, self.btn_swap)
        self.layout_menu.insertWidget(0, self.loading_label)