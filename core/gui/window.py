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
        nprompt: typing.Optional[str] = None,
        generator_type: str = "Text to Image",
        image: typing.Optional[str] = None,
        condition: typing.Optional[str] = None,
    ):
        super().__init__()
        
        self.prompt = prompt
        self.npropmt = nprompt
        self.model = model
        self.image = image
        self.condition = condition
        self.generator_type = generator_type
        
    def run(self) -> None:
        if self.generator_type == "Text to Image":
            b64, seed = TextToImage(
                prompt=self.prompt,
                negative_prompt=self.npropmt,
                model=self.model,
            ).generate_image()
        
        elif self.generator_type == "ControlNet":
            b64, seed = ControlNet(
                prompt=self.prompt,
                negative_prompt=self.npropmt,
                model=self.model,
                image=self.image,
                condition=self.condition,
            ).generate_image()
        
        elif self.generator_type == "UpScale":
            b64, seed = UpScale(model=self.model, image=self.image).generate_image()
            
        elif self.generator_type == "FaceFix":
            b64, seed = FaceFix(model=self.model, image=self.image).generate_image()
        
        self.b64_ready.emit(b64)
        self.seed_ready.emit(b64, seed)
        self.finish.emit()


class MainWindow(UI):
    IMG_FOLDER = os.path.join(os.path.expanduser("~"), "Pictures")
    
    def __init__(self) -> None:
        super().__init__()
        
        self.models = get_models()
        self.image_dict.setText(self.IMG_FOLDER)
        
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
        self.btn_generate.pressed.connect(self.generate_image)
        self.btn_generate_type.currentTextChanged.connect(self.update_opts_buttons)
        self.btn_image.pressed.connect(self.open_image)
        self.btn_clear.pressed.connect(self.clear_imgs)
        self.btn_swap.pressed.connect(self.swap_imgs)
        self.btn_image_dict.pressed.connect(self.set_image_dict)
    
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
        self.key_nprompt.activated.connect(self.nprompt.setFocus)
        
    def setup_models(self) -> None:
        self.btn_generate_type.addItems(list(self.models.keys())[:-1])
        self.btn_generate_type.setCurrentText(list(self.models.keys())[0])
    
    def start_worker(self) -> None:
        self.btn_generate.setEnabled(False)
        self.btn_generate.hide()
        self.loading_label.show()
        self.loading_movie.start()
        
    def stop_worker(self) -> None:
        self.worker.quit()
        self.worker.wait()
        
        self.loading_movie.stop()
        self.loading_label.hide()
        self.btn_generate.show()
        self.btn_generate.setEnabled(True)
    
    def generate_image(self) -> None:
        curr_generator_type = self.btn_generate_type.currentText()
        
        prompt = self._format_text(self.prompt.toPlainText())
        nprompt = self._format_text(self.nprompt.toPlainText())
        model = self.btn_model.currentText()
        image = self.left_img_b64
        condition = self.btn_condition.currentText()
        
        if not prompt and curr_generator_type not in {"UpScale", "FaceFix"}:
            return
        
        self.start_worker()
        self.worker = ImageGeneratorThread(
            model=model, 
            prompt=prompt, 
            nprompt=nprompt, 
            image=image,
            condition=condition,
            generator_type=curr_generator_type,
        )
        if curr_generator_type == "Text to Image":
            self.worker.b64_ready.connect(self.update_left_img)
        else:
            self.worker.b64_ready.connect(self.update_right_img)
        
        self.worker.seed_ready.connect(self._save_image)
        self.worker.finish.connect(self.stop_worker)
        self.worker.start()
                
    
    def update_opts_buttons(self) -> None:
        curr_model = self.btn_model.currentText()
        curr_generate_type = self.btn_generate_type.currentText()
        self.btn_condition.addItems(self.models["Condition"]["models"])
        self.btn_model.clear()
        self.btn_model.addItems(self.models[curr_generate_type]["models"])
        self.btn_image.setEnabled(self.models[curr_generate_type]["image"])
        self.btn_condition.setEnabled(self.models[curr_generate_type]["condition"])
        self.btn_model.setCurrentText(curr_model)

    def open_image(self) -> None:
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open", self.IMG_FOLDER, "Image File (*.png; *.jpeg)"
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
                self.left_img_b64 = base64.b64encode(f.read()).decode()
            pixmap = QtGui.QPixmap(filename)
        elif b64:
            self.left_img_b64 = b64
            pixmap = self.convert_to_pixmap(b64)
            
        self.left_img.setPixmap(pixmap)

    def update_right_img(self, b64: str) -> None:
        self.right_img_b64 = b64
        pixmap = self.convert_to_pixmap(b64)
        self.right_img.setPixmap(pixmap)

    def clear_imgs(self) -> None:
        self.left_img.clear()
        self.right_img.clear()
        
    def swap_imgs(self) -> None:
        try:
            left_img = self.left_img.pixmap().copy()
            right_img = self.right_img.pixmap().copy()
        except AttributeError:
            return
        self.left_img.setPixmap(right_img)
        self.right_img.setPixmap(left_img)
        
    def set_image_dict(self) -> None:
        folder_name = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Open Directory", self.IMG_FOLDER, QtWidgets.QFileDialog.ShowDirsOnly | QtWidgets.QFileDialog.DontResolveSymlinks
        )
        if folder_name:
            return self.update_img_dict(folder_name)
    
    def update_img_dict(self, folder_name: str) -> None:
        self.image_dict.setText(folder_name)
        self.IMG_FOLDER = folder_name

        
def start_app() -> None:
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
