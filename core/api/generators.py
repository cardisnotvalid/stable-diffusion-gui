import typing
import requests

from core import exceptions
from core.logger import logger
from core.constants import URLs
from core.utils import get_api_key
from core.api.key import GetimgReger


class BaseRequest:
    def get_headers(self) -> typing.Dict[str, str]:
        return {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {get_api_key()}"
        }

    def get_payload(self) -> typing.Union[typing.Dict[str, str], typing.Dict]:
        payload = {}
        for key, value in self.__dict__.items():
            if value is not None:
                payload[key] = value
        return payload

    def check_response(self, response: requests.Response) -> typing.Optional[bool]:
        resp_json = response.json()

        if resp_json.get("error"):
            error_code = resp_json["error"]["code"]
            
            if error_code == "quota_exceeded":
                GetimgReger().write_api_key()
                return True
            else:            
                raise exceptions.ResponseErrorCode(error_code)


class BaseGenerator(BaseRequest):
    def __init__(self) -> None:
        super().__init__()

    def generate_image(self) -> typing.Tuple[str, int]:
        payload = self.get_payload()
        headers = self.get_headers()
        
        response = requests.post(self.BASE_URL, json=payload, headers=headers)
        
        if self.check_response(response) is True:
            return self.generate_image()
        
        imgb64, seed, _ = response.json().values()
        logger.info(f"Seed: {seed}")
        return imgb64, seed


class TextToImage(BaseGenerator):
    BASE_URL = URLs.TEXT_TO_IMAGE

    def __init__(
        self,
        prompt: str,
        model: typing.Optional[str] = None,
        negative_prompt: typing.Optional[str] = None,
        width: typing.Optional[int] = None,
        height: typing.Optional[int] = None,
        steps: typing.Optional[int] = None,
        guidance: typing.Optional[float] = None,
        seed: typing.Optional[int] = None,
        scheduler: typing.Optional[str] = None,
        output_format: typing.Optional[str] = "png",
    ) -> None:
        super().__init__()
        
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


class ControlNet(BaseGenerator):
    BASE_URL = URLs.CONTROL_NET
    
    def __init__(
        self,
        prompt: str,
        image: str,
        condition: typing.Optional[str] = "canny-1.1",
        model: typing.Optional[str] = None,
        negative_prompt: typing.Optional[str] = None,
        width: typing.Optional[int] = None,
        height: typing.Optional[int] = None,
        steps: typing.Optional[int] = None,
        guidance: typing.Optional[float] = None,
        seed: typing.Optional[int] = None,
        scheduler: typing.Optional[str] = None,
        output_format: typing.Optional[str] = "png",
    ) -> None:
        super().__init__()
        
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
            

class UpScale(BaseGenerator):
    BASE_URL = URLs.UP_SCALE
    
    def __init__(
        self,
        image: str,
        model: typing.Optional[str] = None,
        scale: typing.Optional[int] = 4,
        output_format: typing.Optional[str] = "png",
    ) -> None:
        super().__init__()
        
        self.model = model
        self.image = image
        self.scale = scale
        self.output_format = output_format
        
        logger.debug(self.get_payload())
        logger.info("[UpScale] Image processing in progress")


class FaceFix(BaseGenerator):
    BASE_URL = URLs.FACE_FIX
    
    def __init__(
        self,
        image: str,
        model: typing.Optional[str] = None,
        output_format: typing.Optional[str] = "png",
    ) -> None:
        super().__init__()
        
        self.model = model
        self.image = image
        self.output_format = output_format
        
        logger.debug(self.get_payload())
        logger.info("[FaceFix] Image processing in progress")