from compress import compress_nlz11
import os
import shutil
from lzss3 import decompress_bytes

header = bytearray.fromhex(
    "01 00 00 00 15 25 00 00 00 00 00 00 15 25 00 00 E0 14 00 00 BF 16 00 00 BF 16 00 00 1C 1B 00 00 DD 19 00 00 DD 01 00 00"
    )

class ccfile:
    def __init__(self, name, base_path, loaded_map,mod_base_path):
        self.name = name
        self.path_original = f"{base_path}/music/{loaded_map}/{name}"
        self.path_modw = f"{mod_base_path}/music/{loaded_map}/{name}"
        self.path_modw_folder = f"{mod_base_path}/music/{loaded_map}"
        self.path_mod = self.path_modw
        if not os.path.exists(self.path_mod):
            self.path_mod = self.path_original

    def __str__(self):
        return f"{self.name} at {self.path_original}"

    def read(self):
        with open(self.path_original, "rb") as f:
            bytes = f.read()
            return decompress_bytes(bytes)

    def readMod(self):
        with open(self.path_mod, "rb") as f:
            bytes = f.read()
            return decompress_bytes(bytes)

    def write(self, data, do_compress_nlz11 = True):
        # create a "loaded_map" folder if nonexistent
        os.makedirs(self.path_modw_folder, exist_ok=True)
        with open(self.path_modw, "wb") as f:
            if do_compress_nlz11:
                try:
                    compress_nlz11(data, f)
                    print(f"Successfully exported {self.name} at {self.path_modw}")
                except Exception as e:
                    print(f"Error compressing data for {self.name}: {e}")
            else:
                try:
                    f.write(data)
                    print(f"Successfully wrote data for {self.name} at {self.path_modw}")
                except Exception as e:
                    print(f"Error writing data for {self.name}: {e}")

    def basePath(self):
        return self.path_original
    
    def modPath(self):
        return self.path_mod

class Event:
    def __init__(self, time):
        self.time = time
        self.time_sec = time/60
        self.time_bytes = int(time).to_bytes(4, byteorder='little')
        self.type = type
        self.event_type = None
        self.direction = 0
        self.lane_bytes = (0).to_bytes(1, byteorder='little')

    def set_rotation(self, value):
        self.direction = round(value/45)
        self.rotation = self.direction*45
        self.rotation_bytes = self.rotation.to_bytes(2, byteorder='little')


    def set_lane(self, value):
        self.lane = value
        self.lane_bytes = value.to_bytes(1, byteorder='little')

    def set_type(self, value):
        match value:
            case 0:
                self.event_type = "tap"
            case 1:
                self.event_type = "slide"
            case 2:
                self.event_type = "hold start"
            case 4:
                self.event_type = "hold end"
            case 5:
                self.event_type = "hold slide"
            case _:
                self.event_type = "unknown"
        self.type_bytes = value.to_bytes(1, byteorder='little')


def BytesToEvent(bytes):
    time = bytes[0]+bytes[1]*256
    lane = bytes[12]
    event_type = bytes[4]
    extra_data = bytes[16] + bytes[17] * 256

    event = Event(time)
    event.set_lane(lane)
    event.set_type(event_type)
    event.set_rotation(extra_data)
    return event

def EventToBytes(event):
    bytes = bytearray(24)
    bytes[0:4] = event.time_bytes
    bytes[12:13] = event.lane_bytes
    bytes[4:5] = event.type_bytes
    bytes[16:18] = event.rotation_bytes
    return bytes


def ExtractEvents(raw_bytes):
    events = []
    data = raw_bytes[40:]

    for i in range(0, len(data), 24):
        chunk = data[i:i+24]
        if len(chunk) == 24:
            events.append(BytesToEvent(chunk))
    return events

def CompileEvents(events):
    compiled = bytearray()
    for event in events:
        compiled.extend(EventToBytes(event))
    return compiled

def ExportEvents(events):
    all = bytearray()
    all.extend(header)
    all.extend(CompileEvents(events))
    return all

def CreateChart(events, output_file):
    try:
        with open(output_file, "wb") as f:
            compress_nlz11(ExportEvents(events), f)
            print(f"Chart created successfully: {output_file}")
    except Exception as e:
        print(f"Error creating chart: {e}")
    return output_file