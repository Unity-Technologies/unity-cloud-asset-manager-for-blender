import ctypes
import json
from json import JSONEncoder
from .Models import Interop_Model_Base, User_Info, Asset_Info, Interop_Exception
from ctypes import *
from enum import Enum
from .utils import _load_lib


class Interop:

    __interop_response_map: dict[str, Interop_Model_Base] = {
        "USERINFO" : User_Info(),
        "ASSETINFO" : Asset_Info()
    }

    __interop_response_without_serialization = [
        "TOKEN",
        "STATE",
        "COMPLETION"
    ]

    __AUTHENTICATION_CALLBACK = CFUNCTYPE(None, c_int)

    class Authentication_State(Enum):
        AWAITING_INITIALIZATION = 0
        LOGGED_IN = 1
        LOGGED_OUT = 2
        AWAITING_LOGIN = 3
        AWAITING_LOGOUT = 4

    def __init__(self):
        self.__lib = _load_lib()

        self.__lib.Initialize.restype = ctypes.c_char_p
        self.__lib.Login.restype = ctypes.c_char_p
        self.__lib.CancelLogin.restype = ctypes.c_char_p
        self.__lib.Logout.restype = ctypes.c_char_p
        self.__lib.GetAccessToken.restype = ctypes.c_char_p
        self.__lib.GetUserInfo.restype = ctypes.c_char_p
        self.__lib.CreateAsset.restype = ctypes.c_char_p
        self.__lib.CancelCreateAsset.restype = ctypes.c_char_p
        self.__lib.SubscribeToAuthenticationState.restype = ctypes.c_char_p
        self.__lib.UnSubscribeFromAuthenticationState.restype = ctypes.c_char_p
        self.__lib.GetAuthenticationState.restype = ctypes.c_char_p
        self.__lib.Dispose.restype = ctypes.c_char_p

        self.__authentication_state_callbacks = []

    def initialize(self):
        address = self.__lib.Initialize()
        completion = self.__get_response_content(address)
        return completion

    def login(self):
        address = self.__lib.Login()
        access_token = self.__get_response_content(address)
        return access_token
    
    def cancel_login(self):
        address = self.__lib.CancelLogin()
        completion = self.__get_response_content(address)
        return completion

    def logout(self, clear_cache: bool):
        address = self.__lib.Logout(clear_cache)
        completion = self.__get_response_content(address)
        return completion

    def get_access_token(self):
        address = self.__lib.GetAccessToken()
        access_token = self.__get_response_content(address)
        return access_token

    def get_user_info(self):
        address = self.__lib.GetUserInfo()
        user_info = self.__get_response_content(address)
        return user_info

    def create_asset(self, asset_name):
        asset_name_bytes = bytes(asset_name, 'utf-8')
        asset_name_buffer = create_string_buffer(asset_name_bytes)
        address = self.__lib.CreateAsset(asset_name_buffer)
        asset_info = self.__get_response_content(address)
        return asset_info
    
    def cancel_create_asset(self):
        address = self.__lib.CancelCreateAsset()
        completion = self.__get_response_content(address)
        return completion

    def subscribe_to_authentication_state(self, callback):
        self.__authentication_state_callbacks.append(callback)
        # If it is the first callback, create the main auth_callback listener and subscribe it to interop library
        if len(self.__authentication_state_callbacks) == 1:
            self.auth_callback = self.__AUTHENTICATION_CALLBACK(self.__auth_callback_method)
            address = self.__lib.SubscribeToAuthenticationState(self.auth_callback)
            completion = self.__get_response_content(address)
            if not completion:
                self.__authentication_state_callbacks.pop()
            return completion
        return True

    def unsubscribe_from_authentication_state(self, callback):
        if callback not in self.__authentication_state_callbacks:
            return False
        self.__authentication_state_callbacks.remove(callback)
        if len(self.__authentication_state_callbacks) == 0:
            address = self.__lib.UnSubscribeFromAuthenticationState(self.auth_callback)
            completion = self.__get_response_content(address)
            return completion
        return True

    def get_authentication_state(self):
        address = self.__lib.GetAuthenticationState()
        state = self.__get_response_content(address)
        return self.Authentication_State(state)

    def dispose(self):
        address = self.__lib.Dispose()
        completion = self.__get_response_content(address)
        return completion

    def __auth_callback_method(self, state):
        for callback in self.__authentication_state_callbacks:
            callback(self.Authentication_State(state))

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
        if content_type in self.__interop_response_without_serialization:
            return content
        else:
            return_object = self.__interop_response_map.get(content_type)
            return_object.load_from_json(content)
            return return_object

class ModelEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
