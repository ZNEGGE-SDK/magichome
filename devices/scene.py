from magichome.devices.base import MagicHomeDevice


class MagicHomeScene(MagicHomeDevice):
    def avaliable(self):
        return True

    def activate(self):
        self.api.device_control(self.obj_id, "Activate", "")

    def update(self):
        return True
