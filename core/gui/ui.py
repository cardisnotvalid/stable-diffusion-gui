import typing
from PyQt5 import QtWidgets, QtCore, QtGui
from core.paths import GUI_CSS, GUI_IMAGES

SizePolicy = QtWidgets.QSizePolicy.Policy

"""
Minimum: 1
Maximum: 4
Preferred: 5       
MinimumExpanding: 3
Expanding: 7       
Ignored: 13 
"""


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
    ) -> None:
        super().__init__(parent=parent)
    
        self.setObjectName(text)
        self.setContentsMargins(0, 0, 0, 0)
        
        if width: self.setFixedWidth(width)
        if height: self.setFixedHeight(height)


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
        self.containerPrompt = QtWidgets.QWidget()
        self.containerGenButtons = QtWidgets.QWidget()
        self.containerGenOptions = QtWidgets.QWidget()
        self.containerGenOptionals = QtWidgets.QWidget()
        self.containerImgDirectory = QtWidgets.QWidget()
        self.containerResultImgs = QtWidgets.QWidget()
        self.containerResultButtons = QtWidgets.QWidget()
    
    def create_layouts(self) -> None:
        self.layoutMain = VLayout(self, rows=5)
        self.layoutMain.setObjectName("main_layout")
        
        self.layoutPrompt = HLayout(self.containerPrompt, columns=2)
        self.layoutGenButtons = HLayout(self.containerGenButtons, columns=2)
        self.layoutGenOptions = HLayout(self.containerGenOptions, columns=3)
        self.layoutGenOptionals = HLayout(self.containerGenOptionals, columns=4)
        self.layoutImgDirectory = HLayout(self.containerImgDirectory, columns=2)
        self.layoutResultImgs = HLayout(self.containerResultImgs, columns=2)
        self.layoutResultButtons = HLayout(self.containerResultButtons, columns=2)
        
        self.layoutMain.addWidgets(
            self.containerPrompt, 
            self.containerGenButtons, 
            self.containerGenOptions,
            self.containerGenOptionals,
            self.containerImgDirectory, 
            self.containerResultImgs, 
            self.containerResultButtons
        )
    
    def create_widgets(self) -> None:
        # Prompts
        self.prompt = TextEdit(placeholder="Prompt")
        self.negativePrompt = TextEdit(placeholder="Negative Prompt")
        self.prompt.setAcceptRichText(False)
        self.negativePrompt.setAcceptRichText(False)
        self.layoutPrompt.addWidgets(self.prompt, self.negativePrompt)
        
        # Generate buttons
        self.buttonGenerate = Button(text="Generate")
        self.buttonGenerateType = ComboBox()
        self.layoutGenButtons.addWidgets(self.buttonGenerate, self.buttonGenerateType)
        
        # Generation options buttons
        self.buttonModel = ComboBox()
        self.buttonOpenImg = Button(text="Image")
        self.buttonCondition = ComboBox()
        self.layoutGenOptions.addWidgets(self.buttonModel, self.buttonOpenImg, self.buttonCondition)
        
        # Generation optionals values
        self.inputWidth = QtWidgets.QLineEdit()
        self.inputHeight = QtWidgets.QLineEdit()
        self.inputSteps = QtWidgets.QLineEdit()
        self.inputGuidance = QtWidgets.QLineEdit()
        self.inputWidth.setValidator(QtGui.QIntValidator(256, 1024, self))
        self.inputHeight.setValidator(QtGui.QIntValidator(256, 1024, self))
        self.inputSteps.setValidator(QtGui.QIntValidator(1, 100, self))
        self.inputGuidance.setValidator(QtGui.QDoubleValidator(0.0, 20.0, 1))
        self.inputHeight.setPlaceholderText("Height (256 - 1024)")
        self.inputWidth.setPlaceholderText("Width (256 - 1024)")
        self.inputSteps.setPlaceholderText("Steps (1 - 100)")
        self.inputGuidance.setPlaceholderText("Guidance (0 - 20)")
        self.layoutGenOptionals.addWidgets(self.inputWidth, self.inputHeight, self.inputSteps, self.inputGuidance)
        
        # Set image save directory
        self.buttonImgDirectory = Button(text="Image Directory")
        self.imgDirectory = Label(text="image_dict")
        self.imgDirectory.setEnabled(False)
        self.layoutImgDirectory.addWidgets(self.buttonImgDirectory, self.imgDirectory)
        self.layoutImgDirectory.setStretch(0, 1)
        self.layoutImgDirectory.setStretch(1, 5)
        
        # Generated image labels
        self.leftImgB64, self.rightImgB64 = None, None
        self.leftImg = Label(height=512, width=512)
        self.rightImg = Label(height=512, width=512)
        self.leftImg.setSizePolicy(SizePolicy.Minimum, SizePolicy.Maximum)
        self.rightImg.setSizePolicy(SizePolicy.Minimum, SizePolicy.Maximum)
        self.layoutResultImgs.addWidgets(self.leftImg, self.rightImg)
        
        # Generated image management buttons
        self.buttonClearImgs = Button(text="Clear")
        self.buttonSwapImgs = Button(text="Swap Images")
        self.layoutResultButtons.addWidgets(self.buttonClearImgs, self.buttonSwapImgs)
        
        # Generate animation
        self.loadingMovie = QtGui.QMovie(str(GUI_IMAGES.joinpath("loading.gif")))
        self.loadingMovie.setScaledSize(QtCore.QSize(20, 20))
        self.loadingAnim = Label(text="loading_label", height=30)
        self.loadingAnim.setMovie(self.loadingMovie)
        self.loadingAnim.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.loadingAnim.hide()
        self.layoutGenButtons.insertWidget(0, self.loadingAnim)