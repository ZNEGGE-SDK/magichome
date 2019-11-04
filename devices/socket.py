import time
from magichome.devices.base import MagicHomeDevice

class MagicHomeSocket(MagicHomeDevice):

    def state(self):
        return True
        # state = self.data.get('value')
        # if state is None:
        #     return None
        # return state
        
        
    def turn_on(self):
        print(self.obj_id)
        self.api.device_control(self.obj_id,'TurnOn','')
        
    def turn_off(self):
        print(self.obj_id)
        self.api.device_control(self.obj_id, 'TurnOff','')
    
    def update(self):
        """Avoid get cache value after control."""
        time.sleep(0.5)
        devices = self.api.discovery()
        if not devices:
            return
        for device in devices:
            if device['id'] == self.obj_id:
                self.data = device['data']
                return True
    