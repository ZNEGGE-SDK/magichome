import hashlib
import json
import logging
import time
import uuid

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from magichome.devices.factory import get_magichome_device 
from magichome.devices.factory import get_magichome_detail

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.adapters.DEFAULT_RETRIES = 5
s = requests.session()
s.keep_alive = False

MAGHCHOMECLOUDURL = "https://wifij01{}.magichue.net"
DEFAULTREGION = "us"

REFRESHTIME = 60 * 60 * 12

_LOGGER = logging.getLogger(__name__)


class MagicHomeSession:

    username = ""
    password = ""
    company = ""
    platform = ""
    accessToken = ""
    refreshToken = ""
    expireTime = 0
    devices = []
    region = DEFAULTREGION
    lights = []
    switch = []
    


SESSION = MagicHomeSession()


class MagicHomeApi:
    
    def magichome_hub(self, username, password):
        SESSION.username = username
        SESSION.password = self.md5str(password)
        
        if username is None or password is None:
            raise MagicHomeApiException("Account or password is None")
        else:
            self.get_access_token()
            self.discover_devices()
            return SESSION
        
        
    
    def init(self, username, password):
        SESSION.username = username
        SESSION.password = self.md5str(password)

        if username is None or password is None:
            raise MagicHomeApiException("Account or password is None")
        else:
            self.get_access_token()
            self.discover_devices()
            return SESSION.devices

    def get_access_token(self):
        headers = {"Content-Type": "application/json;charset=UTF-8;"}
        s = requests.session()
        s.keep_alive = False
        response = requests.post(
            (MAGHCHOMECLOUDURL + "/authorizationCode/ZG001").format(SESSION.region),
            headers=headers,
            data=json.dumps(
                {
                    "username": SESSION.username,
                    "password": SESSION.password,
                    "cdpid": "ZG001",
                    "client_id": "py_Api",
                    "response_type": "",
                    "state": "state",
                    "redirect_uri": "redirect_uri",
                }
            ),
            verify=False,
        )
        response_json = response.json()

        if response_json.get("responseStatus") == "error":
            message = response_json.get("msg")
            if message == "error":
                raise MagicHomeApiException("get access token failed")
            else:
                raise MagicHomeApiException(message)

        code = response_json.get("code")

        if code == 10033:
            _LOGGER.error("MagicHome account or password don't match")
            raise MagicHomeApiException("MagicHome account or password don't match")

        s = requests.session()
        s.keep_alive = False
        responsetk = requests.post(
            (MAGHCHOMECLOUDURL + "/authorizationToken").format(SESSION.region),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "client_id": "py_Api",
                "fromApp": "ZG001",
                "grant_type": "authorization_code",
                "code": code,
            },
            verify=False,
        )
        response_tk_json = responsetk.json()

        if response_tk_json.get("responseStatus") == "error":
            message = response_tk_json.get("errorMsg")
            if message == "error":
                raise MagicHomeApiException("get access token failed")
            else:
                raise MagicHomeApiException(message)

        SESSION.accessToken = response_tk_json.get("access_token")
        SESSION.refreshToken = response_tk_json.get("refresh_token")
        SESSION.expireTime = int(time.time()) + response_tk_json.get("expires_in")

        areaCode = SESSION.accessToken[0:2]
        if areaCode == "EU":
            SESSION.region = "eu"
        elif areaCode == "CN":
            SESSION.region = "cn"
        else:
            SESSION.region = "us"

    def check_access_token(self):
        if SESSION.username == "" or SESSION.password == "":
            raise MagicHomeApiException("can not find username or password")
            return
        if SESSION.accessToken == "" or SESSION.refreshToken == "":
            self.get_access_token()
        elif SESSION.expireTime <= REFRESHTIME + int(time.time()):
            self.refresh_access_token()

    def refresh_access_token(self):
        data = "grant_type=refresh_token&refresh_token=" + SESSION.refreshToken
        s = requests.session()
        s.keep_alive = False
        response = requests.get(
            (MAGHCHOMECLOUDURL + "/authorizationToken").format(SESSION.region)
            + "?"
            + data,
            verify=False,
        )
        response_json = response.json()
        if response_json.get("responseStatus") == "error":
            raise MagicHomeApiException("refresh token failed")

        SESSION.accessToken = response_json.get("access_token")
        SESSION.refreshToken = response_json.get("refresh_token")
        SESSION.expireTime = int(time.time()) + response_json.get("expires_in")

    # Update of training equipment
    def poll_devices_update(self):
        self.check_access_token()
        return self.discover_devices()

    def discovery(self):
        response = self._request("DiscoveryDevices", "MagicHome.Python.API", None, {})
        if response is not None:
            return response
        return None

    def discover_devices(self):
        devices = self.discovery()
        if not devices:
            return None
        SESSION.devices = []

        for device in devices:
            SESSION.devices.extend(get_magichome_device(device, self))
            deviceType = device.get("deviceType")
            if deviceType == "light":
                SESSION.lights.extend(get_magichome_detail(device, self))
            elif deviceType == "switch":
                SESSION.switch.extend(get_magichome_detail(device, self))
        return devices

    def get_devices_by_type(self, dev_type):
        device_list = []
        for device in SESSION.devices:
            if device.dev_type() == dev_type:
                device_list.append(device)
        return device_list

    def get_all_devices(self):
        # lights()
        # switch()
        return SESSION.devices

    def md5str(self, str):
        m = hashlib.md5()
        s = str.encode(encoding="utf-8")
        m.update(s)
        result = m.hexdigest()
        return result

    def get_device_by_id(self, dev_id):
        for device in SESSION.devices:
            if device.object_id() == dev_id:
                return device
        return None

    #  device controller
    def device_control(self, devId, name, param="", namespace="Control"):
        if param is None:
            param = ""
        response = self._request(name, namespace, devId, param)
        
        if response and response["payload"]["errorCode"] == None:
            success = True
        else:
            success = False
        return success, response

    def _request(self, name, namespace, devId, value):

        if SESSION.accessToken is None:
            raise MagicHomeApiException("User information is invalid, please try to restart. Please note that the account and password are correct")

        headers = {"Content-Type": "application/json;charset=UTF-8;"}
        header = {"name": name, "namespace": namespace, "payloadVersion": 1}

        payload = {}
        if value != {}:
            payload = {
                "accessToken": SESSION.accessToken,
                "deviceId": devId,
                "value": value,
            }
        else:
            payload = {"accessToken": SESSION.accessToken, "deviceId": devId}

        data = {
            "header": {
                "name": name,
                "namespace": namespace,
                "payloadVersion": 1,
                "messageId": str(uuid.uuid1()),
            },
            "payload": payload,
        }
        s = requests.session()
        s.keep_alive = False
        response = requests.post(
            (MAGHCHOMECLOUDURL + "/pythonAPI/ZG001").format(SESSION.region),
            json=data,
            headers=headers,
            verify=False,
        )

        response_json = response.json()
        if name == "DiscoveryDevices":
            if "payload" in response_json:
                if "devices" in response_json["payload"]:
                    return response_json["payload"]["devices"]
            else:
                return None
        elif name == "TurnOffResponse":
            return response_json

        if response_json is not None:
            if "payload" in response_json:
                if "errorCode" in response_json["payload"]:
                    if response_json["payload"]["errorCode"] != None:
                        return None
        return response_json


class MagicHomeApiException(Exception):
    pass
