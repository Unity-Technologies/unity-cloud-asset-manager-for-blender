import ctypes
from .Models import Interop_Exception
from .utils import _load_lib
import json


class Assets:

    __response_without_serialization = [
        "COMPLETION"
    ]

    def __init__(self):
        self.__lib = _load_lib()

        self.__lib.UploadFile.restype = ctypes.c_char_p
        self.__lib.AssetsDispose.restype = ctypes.c_char_p

    def upload_file(self, token, org_id, project_id, asset_id, path):
        address = self.__lib.UploadFile(token, org_id, project_id, asset_id, path)
        completion = self.__get_response_content(address)
        return completion

    def dispose(self):
        address = self.__lib.AssetsDispose()
        completion = self.__get_response_content(address)
        return completion

    def __get_response_content(self, address):
        interop_response_json = ctypes.string_at(address).decode('utf-8')
        response_json = json.loads(interop_response_json)
        content_type = response_json.get("ContentType")
        content = response_json.get("Content")
        is_successful = response_json.get("IsSuccessful")
        if content_type == "EXCEPTION" and not is_successful:
            interop_exception = Interop_Exception()
            interop_exception.load_from_json(content)
            raise interop_exception
        if content_type in self.__response_without_serialization:
            return content
        else:
            interop_exception = Interop_Exception()
            interop_exception.Message = f"The response content type {content_type} is not supported"
            raise interop_exception
