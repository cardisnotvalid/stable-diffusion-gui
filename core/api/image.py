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
        
        logger.debug(f"Prompt: {self.prompt} | Seed: {seed}")
        logger.info(f"Seed: {seed}")
        
        utils.write_image(img_data, seed, self.output_format)
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
        set_config: typing.Optional[bool] = False,
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

        if set_config is True:
            config = utils.get_config()["text_to_image"]
            self.model = config.get("model", self.model)
            self.width = config.get("width", self.width)
            self.height = config.get("height", self.height)
            self.steps = config.get("steps", self.steps)
            self.scheduler = config.get("scheduler", self.scheduler)
            self.output_format = config.get("output_format", self.output_format)


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
        set_config: typing.Optional[bool] = False,
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

        if set_config is True:
            config = utils.get_config()["controlnet"]
            self.model = config.get("model", self.model)
            self.controlnet = config.get("condition", self.controlnet)
