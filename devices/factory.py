from magichome.devices.controller import MagicHomeController
from magichome.devices.light import MagicHomeLight
from magichome.devices.scene import MagicHomeScene
from magichome.devices.socket import MagicHomeSocket
from magichome.devices.switch import MagicHomeSwitch


def get_magichome_device(data, api):

    dev_type = data.get("deviceType")
    devices = []
    if dev_type == "light":
        devices.append(MagicHomeLight(data, api))
    elif dev_type == "scene":
        devices.append(MagicHomeScene(data, api))
    elif dev_type == "switch":
        devices.append(MagicHomeSwitch(data, api))
    # elif dev_type == "socket":
    #     devices.append(MagicHomeSocket(data, api))
    # elif dev_type == "controller":
    #     devices.append(MagicHomeController(data, api))
    return devices
    

def get_magichome_detail(data, api):
    devices = []
    dev_type = data.get("deviceType")
    if dev_type == "light":
        devices.append(MagicHomeLight(data, api))
        return devices
    elif dev_type == "scene":
        devices.append(MagicHomeScene(data, api))
        return devices
    elif dev_type == "switch":
        devices.append(MagicHomeSwitch(data, api))
        return devices
