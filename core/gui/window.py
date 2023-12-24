import os
import sys
import base64
import typing

from PyQt5 import QtWidgets, QtGui, QtCore

from core.gui.ui import UI
from core.utils import get_models
from core.api.generators import TextToImage, ControlNet, UpScale, FaceFix


class ImageGeneratorThread(QtCore.QThread):
    b64_ready = QtCore.pyqtSignal(str)
    seed_ready = QtCore.pyqtSignal(str, int)
    finish = QtCore.pyqtSignal()
    
    def __init__(
        self, 
        model: str,
        prompt: typing.Optional[str] = None,
        negativePrompt: typing.Optional[str] = None,
        currentGeneratorType: str = "Text to Image",
        image: typing.Optional[str] = None,
        condition: typing.Optional[str] = None,
        height: typing.Optional[int] = None,
        width: typing.Optional[int] = None,
        steps: typing.Optional[int] = None,
        guidance: typing.Optional[int] = None,
        scheduler: typing.Optional[str] = None,
    ):
        super().__init__()
        
        self.prompt = prompt
        self.negativePrompt = negativePrompt
        self.model = model
        self.image = image
        self.condition = condition
        self.generatorType = currentGeneratorType
        self.height = height
        self.width = width
        self.steps = steps
        self.guidance = guidance
        self.scheduler = scheduler
        
    def run(self) -> None:
        if self.generatorType == "Text to Image":
            b64, seed = TextToImage(
                prompt=self.prompt,
                negative_prompt=self.negativePrompt,
                model=self.model,
                height=self.height,
                width=self.width,
                steps=self.steps,
                guidance=self.guidance,
                scheduler=self.scheduler
            ).generate_image()
        
        elif self.generatorType == "ControlNet":
            b64, seed = ControlNet(
                prompt=self.prompt,
                negative_prompt=self.negativePrompt,
                model=self.model,
                image=self.image,
                condition=self.condition,
                height=self.height,
                width=self.width,
                steps=self.steps,
                guidance=self.guidance,
                scheduler=self.scheduler
            ).generate_image()
        
        elif self.generatorType == "UpScale":
            b64, seed = UpScale(model=self.model, image=self.image).generate_image()
            
        elif self.generatorType == "FaceFix":
            b64, seed = FaceFix(model=self.model, image=self.image).generate_image()
        
        self.b64_ready.emit(b64)
        self.seed_ready.emit(b64, seed)
        self.finish.emit()


class MainWindow(UI):
    IMG_FOLDER = os.path.join(os.path.expanduser("~"), "Pictures")
    
    def __init__(self) -> None:
        super().__init__()
        
        self.models = get_models()
        self.imgDirectory.setText(self.IMG_FOLDER)
        
        self.init_logic()
        self.init_hotkey()
        self.setup_models()
    
    def _format_text(self, text: str) -> str:
        text = text.strip()
        text = " ".join(word for word in text.split())
        return text
    
    def _save_image(self, b64: str, seed: str) -> None:
        if not os.path.exists(self.IMG_FOLDER):
            os.makedirs(self.IMG_FOLDER)
        
        filepath = (f"{self.IMG_FOLDER}\\{seed}.png")
        with open(filepath, "wb") as file:
            file.write(base64.b64decode(b64.encode()))
    
    def init_logic(self) -> None:
        self.buttonGenerate.pressed.connect(self.generate_image)
        self.buttonGenerateType.currentTextChanged.connect(self.update_opts_buttons)
        self.buttonOpenImg.pressed.connect(self.open_image)
        self.buttonClearImgs.pressed.connect(self.clear_imgs)
        self.buttonSwapImgs.pressed.connect(self.swap_imgs)
        self.buttonImgDirectory.pressed.connect(self.set_image_dict)
    
    def init_hotkey(self) -> None:
        self.key_esc = QtWidgets.QShortcut(QtGui.QKeySequence("Esc"), self)
        self.key_gen = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Return"), self)
        self.key_clear = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+D"), self)
        self.key_swap = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+S"), self)
        self.key_prompt = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+1"), self)
        self.key_nprompt = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+2"), self)
        
        self.key_esc.activated.connect(QtWidgets.qApp.quit)
        self.key_gen.activated.connect(self.generate_image)
        self.key_clear.activated.connect(self.clear_imgs)
        self.key_swap.activated.connect(self.swap_imgs)
        self.key_prompt.activated.connect(self.prompt.setFocus)
        self.key_nprompt.activated.connect(self.negativePrompt.setFocus)
        
    def setup_models(self) -> None:
        self.buttonGenerateType.addItems(list(self.models.keys())[:-2])
        self.buttonGenerateType.setCurrentText(list(self.models.keys())[0])
    
    def start_worker(self) -> None:
        self.buttonGenerate.setEnabled(False)
        self.buttonGenerate.hide()
        self.loadingAnim.show()
        self.loadingMovie.start()
        
    def stop_worker(self) -> None:
        self.worker.quit()
        self.worker.wait()
        
        self.loadingMovie.stop()
        self.loadingAnim.hide()
        self.buttonGenerate.show()
        self.buttonGenerate.setEnabled(True)
    
    def generate_image(self) -> None:
        convertToFloat = lambda x: float(x.text()) if x.text() else None
        validateSize = lambda x: int(x) if x is not None and 256 <= x <= 1024  else None
        validateSteps = lambda x: int(x) if x is not None and 1 <= x <= 100 else None
        validateGuidance = lambda x: float(x) if x is not None and 0.0 <= x <= 20.0 else None
        
        currentGeneratorType = self.buttonGenerateType.currentText()
        prompt = self._format_text(self.prompt.toPlainText())
        negativePrompt = self._format_text(self.negativePrompt.toPlainText())
        model = self.buttonModel.currentText()
        image = self.leftImgB64
        condition = self.buttonCondition.currentText()
        height = validateSize(convertToFloat(self.inputHeight))
        width = validateSize(convertToFloat(self.inputWidth))
        steps = validateSteps(convertToFloat(self.inputSteps))
        guidance = validateGuidance(convertToFloat(self.inputGuidance))
        scheduler = self.buttonScheduler.currentText()
                
        if not prompt and currentGeneratorType not in {"UpScale", "FaceFix"}:
            return
        
        self.start_worker()
        self.worker = ImageGeneratorThread(
            model=model, 
            prompt=prompt, 
            negativePrompt=negativePrompt, 
            image=image,
            condition=condition,
            currentGeneratorType=currentGeneratorType,
            height=height,
            width=width,
            steps=steps,
            guidance=guidance,
            scheduler=scheduler,
        )
        if currentGeneratorType == "Text to Image":
            self.worker.b64_ready.connect(self.update_left_img)
        else:
            self.worker.b64_ready.connect(self.update_right_img)
        
        self.worker.seed_ready.connect(self._save_image)
        self.worker.finish.connect(self.stop_worker)
        self.worker.start()
                
    
    def update_opts_buttons(self) -> None:
        currentModel = self.buttonModel.currentText()
        currentGenerateType = self.buttonGenerateType.currentText()
        
        self.buttonScheduler.addItems(self.models["Scheduler"]["models"])
        self.buttonModel.clear()
        self.buttonModel.addItems(self.models[currentGenerateType]["models"])
        self.buttonCondition.clear()
        self.buttonCondition.addItems(self.models["Condition"]["models"])
        
        self.buttonModel.setCurrentText(currentModel)
        
        self.buttonOpenImg.setEnabled(self.models[currentGenerateType]["image"])
        self.buttonCondition.setEnabled(self.models[currentGenerateType]["condition"])
        
        if currentGenerateType in {"Text to Image", "ControlNet"}:
            self.inputWidth.setEnabled(True)
            self.inputHeight.setEnabled(True)
            self.inputSteps.setEnabled(True)
            self.inputGuidance.setEnabled(True)
            self.inputStrength.setEnabled(True)
            self.buttonScheduler.setEnabled(True)
        else:
            self.inputWidth.setEnabled(False)
            self.inputHeight.setEnabled(False)
            self.inputSteps.setEnabled(False)
            self.inputGuidance.setEnabled(False)
            self.inputStrength.setEnabled(False)
            self.buttonScheduler.setEnabled(False)

    def open_image(self) -> None:
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open", self.IMG_FOLDER, "Image File (*.png; *.jpeg; *.jpg)"
        )
        if filename:
            self.update_left_img(filename=filename)

    def convert_to_pixmap(self, b64: str) -> QtGui.QPixmap:
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(QtCore.QByteArray.fromBase64(b64.encode()))
        return pixmap

    def update_left_img(self, b64: str = None, filename: str = None) -> None:
        if filename:
            with open(filename, "rb") as f:
                self.leftImgB64 = base64.b64encode(f.read()).decode()
            pixmap = QtGui.QPixmap(filename)
        elif b64:
            self.leftImgB64 = b64
            pixmap = self.convert_to_pixmap(b64)
        if pixmap.width() < pixmap.height():
            pixmap = pixmap.scaledToHeight(pixmap.width())
        else:
            pixmap = pixmap.scaledToWidth(pixmap.height())
        self.leftImg.setPixmap(pixmap)

    def update_right_img(self, b64: str) -> None:
        self.rightImgB64 = b64
        pixmap = self.convert_to_pixmap(b64)
        self.rightImg.setPixmap(pixmap)

    def clear_imgs(self) -> None:
        self.leftImg.clear()
        self.rightImg.clear()
        
    def swap_imgs(self) -> None:
        try:
            left_img = self.leftImg.pixmap().copy()
            right_img = self.rightImg.pixmap().copy()
        except AttributeError:
            return
        self.leftImg.setPixmap(right_img)
        self.rightImg.setPixmap(left_img)
        
    def set_image_dict(self) -> None:
        folder_name = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Open Directory", self.IMG_FOLDER, QtWidgets.QFileDialog.ShowDirsOnly | QtWidgets.QFileDialog.DontResolveSymlinks
        )
        if folder_name:
            return self.update_img_dict(folder_name)
    
    def update_img_dict(self, folder_name: str) -> None:
        self.imgDirectory.setText(folder_name)
        self.IMG_FOLDER = folder_name

        
def start_app() -> None:
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
