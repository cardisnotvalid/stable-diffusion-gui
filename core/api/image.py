import typing
import requests

from core import utils
from core.logger import logger


class ImageGenerator(utils.HTTPTools):
    
    def generate_image(self, width: int = None, height: int =None) -> None:
        if width: self.width = width
        if height: self.height = height
        payload, headers = self.get_payload(), self.get_headers()
        
        response = requests.post(self.BASE_URL, json=payload, headers=headers)
        self.check_response(response)
        
        img_data, seed, _ = response.json().values()
        utils.write_image(img_data, seed, self.output_format)
        
        if hasattr(self, "prompt"):
            prompt = getattr(self, "prompt")
            logger.debug(f"Prompt: {prompt}")
        logger.info(f"Seed: {seed}")
        
        return img_data


class TextToImage(ImageGenerator):
    BASE_URL = "https://api.getimg.ai/v1/stable-diffusion/text-to-image"

    def __init__(
        self,
        prompt: str,
        *,
        model: typing.Optional[str] = None,
        negative_prompt: typing.Optional[str] = None,
        width: typing.Optional[int] = None,
        height: typing.Optional[int] = None,
        steps: typing.Optional[int] = None,
        guidance: typing.Optional[float] = None,
        seed: typing.Optional[int] = None,
        scheduler: typing.Optional[
            typing.Literal["euler_a", "euler", "lms", "ddim", "dpmsolver++", "pndm"]
        ] = None,
        output_format: typing.Optional[typing.Literal["png", "jpg"]] = "png",
    ) -> None:
        self.prompt = prompt
        self.model = model
        self.negative_prompt = negative_prompt
        self.width = width
        self.height = height
        self.steps = steps
        self.guidance = guidance
        self.seed = seed
        self.scheduler = scheduler
        self.output_format = output_format
            
        logger.debug(self.get_payload())
        logger.info("[Text to Image] Image processing in progress")


class ControlNet(ImageGenerator):
    BASE_URL = "https://api.getimg.ai/v1/stable-diffusion/controlnet"
    
    def __init__(
        self,
        prompt: str,
        image: str,
        condition: typing.Literal[
            "canny-1.1", 
            "softedge-1.1",
            "mlsd-1.1",
            "normal-1.1",
            "depth-1.1",
            "openpose-1.1",
            "openpose-full-1.1",
            "scribble-1.1",
            "lineart-1.1",
            "lineart-anime-1.1",
            "mediapipeface"
        ] = "canny-1.1",
        *,
        model: typing.Optional[str] = None,
        negative_prompt: typing.Optional[str] = None,
        width: typing.Optional[int] = None,
        height: typing.Optional[int] = None,
        steps: typing.Optional[int] = None,
        guidance: typing.Optional[float] = None,
        seed: typing.Optional[int] = None,
        scheduler: typing.Optional[
            typing.Literal["euler_a", "euler", "lms", "ddim", "dpmsolver++", "pndm"]
        ] = None,
        output_format: typing.Optional[typing.Literal["png", "jpg"]] = "png",
    ) -> None:
        self.prompt = prompt
        self.image = image
        self.controlnet = condition
        self.model = model
        self.negative_prompt = negative_prompt
        self.width = width
        self.height = height
        self.steps = steps
        self.guidance = guidance
        self.seed = seed
        self.scheduler = scheduler
        self.output_format = output_format
            
        logger.debug(self.get_payload())
        logger.info("[ControlNet] Image processing in progress")
            

class UpScale(ImageGenerator):
    BASE_URL = "https://api.getimg.ai/v1/enhancements/upscale"
    
    def __init__(
        self,
        model: str,
        image: str,
        scale: int = 4,
        output_format: str = "png",
    ) -> None:
        self.model = model
        self.image = image
        self.sclae = scale
        self.output_format = output_format
        
        logger.debug(self.get_payload())
        logger.info("[UpScale] Image processing in progress")


class FaceFix(ImageGenerator):
    BASE_URL = "https://api.getimg.ai/v1/enhancements/face-fix"
    
    def __init__(
        self,
        model: str,
        image: str,
        output_format: str = "png",
    ) -> None:
        self.model = model
        self.image = image
        self.output_format = output_format
        
        logger.debug(self.get_payload())
        logger.info("[FaceFix] Image processing in progress")