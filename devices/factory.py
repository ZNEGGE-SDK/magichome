
from magichome.devices.light import MagicHomeLight
from magichome.devices.scene import MagicHomeScene
from magichome.devices.switch import MagicHomeSwitch
from magichome.devices.socket import MagicHomeSocket
from magichome.devices.controller import MagicHomeController

def get_magichome_device(data, api):

    dev_type = data.get('deviceType')
    devices = []

    if dev_type == 'light':
        devices.append(MagicHomeLight(data, api));
    elif dev_type == 'scene':
        devices.append(MagicHomeScene(data, api));
    elif dev_type == 'switch':
        devices.append(MagicHomeSwitch(data, api));
    elif dev_type == 'socket':
        devices.append(MagicHomeSocket(data, api));
    elif dev_type == 'controller':
        devices.append(MagicHomeController(data, api));

    return devices

