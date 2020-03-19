import time

from magichome.devices.base import MagicHomeDevice


class MagicHomeSwitch(MagicHomeDevice):
    def state(self):
        if self.data.get("properties") != None:
            for properties in self.data.get("properties"):
                if properties.get("name") == "powerstate":
                    isTrue = properties.get("value") == "true"
                    return isTrue
        return False

    def turn_on(self):
        self.api.device_control(self.obj_id, "TurnOn", "")

    def turn_off(self):
        self.api.device_control(self.obj_id, "TurnOff", "")

    # bug fix
    def update(self):
        """Avoid get cache value after control."""
        time.sleep(3)
        # devices = self.api.discovery()
        # if not devices:
        #     return
        # for device in devices:
        #     if device['id'] == self.obj_id:
        #         self.data = device['data']
        #         return True
        success, response = self.api.device_control(
            self.obj_id, "Query", namespace="Query"
        )
        if success:
            self.data = response
            return True
        return
