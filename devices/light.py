import math

from magichome.devices.base import MagicHomeDevice


class MagicHomeLight(MagicHomeDevice):
    def state(self):
        if self.data.get("properties") != None:
            for properties in self.data.get("properties"):
                if properties.get("name") == "powerstate":
                    isTrue = properties.get("value") == "true"
                    return isTrue
        return False

    def brightness(self):
        if self.data.get("properties") != None:
            for properties in self.data.get("properties"):
                if properties.get("name") == "brightness":
                    return int(int(properties.get("value")) * 255 / 100)
        elif self.data.get("brightness") != None:
            return self.data.get("brightness")
        return 100

    def _set_brightness(self, brightness):
        work_mode = self.data.get("name")
        if work_mode == "colour":
            self.data["color"]["brightness"] = brightness
        else:
            self.data["brightness"] = brightness

    def support_color(self):
        if self.data.get("actions") != None:
            for action in self.data.get("actions"):
                if action == "SetColor":
                    return True
        return False

    def support_color_temp(self):
        if self.data.get("actions") != None:
            for action in self.data.get("actions"):
                if action == "SetColorTemperature":
                    return True
        return False

    def hs_color(self):
        if self.data.get("properties") != None:
            for properties in self.data.get("properties"):
                if properties.get("name") == "color":
                    return self.color_to_hsv(properties.get("value"))
        return 0.0, 0.0

    def color_temp(self):
        if self.data.get("properties") != None:
            for properties in self.data.get("properties"):
                if properties.get("name") == "colorTemperature":
                    return properties.get("value")
        return None

    def min_color_temp(self):
        return 7000

    def max_color_temp(self):
        return 2200

    def turn_on(self):
        self.api.device_control(self.obj_id, "TurnOn", "")

    def turn_off(self):
        self.api.device_control(self.obj_id, "TurnOff", "")

    def set_brightness(self, brightness):
        value = int(brightness * 100 / 255)
        self.api.device_control(self.obj_id, "SetBrightness", value)

    def set_color(self, color):
        """Set the color of light."""
        hsv_color = {}
        hsv_color["hue"] = color[0]
        hsv_color["saturation"] = color[1] / 100
        hsv_color["brightness"] = int(int(self.brightness()) * 100 / 255)
        if hsv_color["saturation"] == 0:
            hsv_color["hue"] = 0
        h = hsv_color["hue"]
        s = hsv_color["saturation"]
        v = hsv_color["brightness"]
        rgb = self.hsv_to_color(h, s, v)
        self.api.device_control(self.obj_id, "SetColor", rgb)

    def set_color_temp(self, color_temp):
        self.api.device_control(self.obj_id, "SetColorTemperature", color_temp)

    def hsv_to_color(self, h, s, v):
        r = 0
        g = 0
        b = 0
        if s == 0:
            r = g = b = v
        else:
            sectorPos = h / 60.0
            sectorNumber = math.floor(sectorPos)
            fractionalSector = sectorPos - sectorNumber
            p = v * (1.0 - s)
            q = v * (1.0 - (s * fractionalSector))
            t = v * (1.0 - (s * (1 - fractionalSector)))
            if sectorNumber == 0:
                r = v
                g = t
                b = p
            elif sectorNumber == 1:
                r = q
                g = v
                b = p
            elif sectorNumber == 2:
                r = p
                g = v
                b = t
            elif sectorNumber == 3:
                r = p
                g = q
                b = v
            elif sectorNumber == 4:
                r = t
                g = p
                b = v
            elif sectorNumber == 5:
                r = v
                g = p
                b = q
            elif sectorNumber == 6:
                r = v
                g = p
                b = p

        red = (int)(r * 255)
        green = (int)(g * 255)
        blue = (int)(b * 255)
        return self.makeColor(
            math.floor((red / 100) + 0.5),
            math.floor((green / 100) + 0.5),
            math.floor((blue / 100) + 0.5),
        )

    def makeColor(self, r, g, b):
        rgbnum = (r << 16) | (g << 8) | b
        return rgbnum

    def color_to_hsv(self, color_number):
        b = 0x0000FF & int(color_number)
        g = 0x00FF00 & int(color_number)
        g >>= 8
        r = 0xFF0000 & int(color_number)
        r >>= 16
        rgb_arr = [r, g, b]
        max_res = max(rgb_arr)
        min_res = min(rgb_arr)
        if max_res == min_res:
            h = 360.0
        elif max_res == r:
            h = (60 * (g - b) / (max_res - min_res) + 360) % 360
        elif max_res == g:
            h = (60 * (b - r) / (max_res - min_res)) + 120
        elif max_res == b:
            h = (60 * (r - g) / (max_res - min_res)) + 240
        if max_res == 0:
            s = 0.0
        else:
            s = (max_res - min_res) / max_res
        v = max_res / 255.0
        if h == 0:
            h = 360.0
        sua = s * 100
        return h, sua
