import base64
import typing
import tomllib

from core import exceptions
from core.api.key import GetimgReger
from core.paths import SETTINGS_DIR, IMG_DIR


class HTTPTools:
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

    def check_response(self, response) -> None:
        resp_json = response.json()

        if resp_json.get("error"):
            error_code = resp_json["error"]["code"]
            
            if error_code == "quota_exceeded":
                GetimgReger().write_api_key()
            else:            
                raise exceptions.ResponseErrorCode(error_code)


def get_api_key() -> str:
    filepath = SETTINGS_DIR.joinpath("api.key")
    file = open(filepath)
    try:
        api_key = file.read()
        assert api_key, exceptions.NoApiKey
        return api_key
    except (FileExistsError, FileNotFoundError):
        raise exceptions.NoFileWithApiKey
    finally:
        file.close()


def get_models() -> str:
    filepath = SETTINGS_DIR.joinpath("models.toml")
    file = open(filepath, "rb")
    try:
        models = tomllib.load(file)
        return models
    except (FileExistsError, FileNotFoundError):
        raise exceptions.NoFileWithApiKey
    finally:
        file.close()


def write_image(img_data: bytes, seed: int, output_format: str) -> None:
    filepath = IMG_DIR.joinpath(f"{seed}.{output_format}")
    with open(filepath, "wb") as file:
        file.write(base64.b64decode(img_data))