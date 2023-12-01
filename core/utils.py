import tomllib

from core import exceptions
from core.paths import SETTINGS_DIR


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
    except (FileExistsError, FileNotFoundError) as e:
        raise e
    finally:
        file.close()
