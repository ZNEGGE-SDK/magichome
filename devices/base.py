import time


class MagicHomeDevice(object):
    def __init__(self, data, api):
        self.api = api
        self.data = data
        self.obj_id = data.get("deviceId")
        self.obj_type = data.get("model")
        self.obj_name = data.get("deviceName")
        self.dev_type = data.get("deviceType")
        self.icon = data.get("icon")
        self.unique_id = data.get("deviceId")
        self.actions = data.get("actions")

    def name(self):
        return self.obj_name

    def state(self):
        if self.data.get("properties") != None:
            for properties in self.data.get("properties"):
                if properties.get("name") == "powerstate":
                    return properties.get("value")
        return False

    def device_type(self):
        return self.dev_type

    def object_id(self):
        return self.obj_id

    def object_type(self):
        return self.obj_type

    def available(self):
        if self.data.get("properties") != None:
            for properties in self.data.get("properties"):
                if properties.get("name") == "status":
                    return False
        return True

    def unique_id(self):
        return self.unique_id
        
    def actions(self):
        return self.actions

    def iconurl(self):
        return self.icon

    def update(self):
        time.sleep(3)
        success, response = self.api.device_control(
            self.obj_id, "Query", namespace="Query"
        )
        if success:
            self.data = response
            return True
        return
