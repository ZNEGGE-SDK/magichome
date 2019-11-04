import time
from magichome.devices.base import MagicHomeDevice

class MagicHomeSwitch(MagicHomeDevice):

    def state(self):
        return True
        # state = self.data.get('state')
        # if state is None:
            # return None
        # return state
        
        
    def turn_on(self):
        self.api.device_control(self.obj_id,'TurnOn','')
        
    def turn_off(self):
        self.api.device_control(self.obj_id, 'TurnOff', '')
    
    
    # bug fix 
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
                