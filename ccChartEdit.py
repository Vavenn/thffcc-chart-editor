from compress import compress_nlz11
import os
from lzss3 import decompress_bytes

dict_mstype = {
    0: "FMS",
    1: "BMS",
    2: "EMS",
}

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
    def __init__(self, time, ms_type):
        self.time = time
        self.time_sec = time/60
        self.time_bytes = int(time).to_bytes(4, byteorder='little')
        self.event_type = None
        self.direction = 0
        self.lane_bytes = (0).to_bytes(1, byteorder='little')
        self.fms_height = 0
        self.fms_height_bytes = (0).to_bytes(1, byteorder='little')
        self.ms_type = ms_type

    def set_rotation(self, value):
        self.direction = round(value/45)
        self.rotation = self.direction*45
        self.rotation_bytes = self.rotation.to_bytes(2, byteorder='little')

    def set_fms_height(self, value):
        self.fms_height = value
        self.fms_height_bytes = value.to_bytes(1, byteorder='little')

    def set_lane(self, value):
        self.lane = value
        if self.lane == -1:
            self.lane_bytes = (0).to_bytes(1, byteorder='little')
        else:
            self.lane_bytes = value.to_bytes(1, byteorder='little')

    def set_type(self, value):
        match value:
            case 0:
                self.event_type = "tap"
            case 1:
                self.event_type = "slide"
            case 2:
                self.event_type = "hold start"
            case 3:
                self.event_type = "hold midpoint"
            case 4:
                self.event_type = "hold end"
            case 5:
                self.event_type = "hold slide"
            case _:
                self.event_type = "unknown"
        self.type_bytes = value.to_bytes(1, byteorder='little')

def MSType(byte):
    int_val = int.from_bytes(byte, "little")
    return dict_mstype.get(int_val, "unknown")

def ChunkToEvents(data):
    ms_type = MSType(data[0:4])
    body_data = data[40:]
    events = []
    for i in range(0, len(body_data), 24):
        chunk = body_data[i:i+24]
        if len(chunk) == 24:
            events.append(BytesToEvent(chunk, ms_type))
    return events

def BytesToEvent(bytes, ms_type):
    time = int.from_bytes(bytes[0:4], byteorder='little')
    event_type = int.from_bytes(bytes[4:8], byteorder='little')
    slide_rotation = int.from_bytes(bytes[16:18], byteorder='little')

    event = Event(time, ms_type)
    event.set_type(event_type)
    event.set_rotation(slide_rotation)

    if ms_type == "BMS":
        lane = int.from_bytes(bytes[12:16], byteorder='little')
        event.set_lane(lane)
        
    if ms_type == "FMS":
        height = int.from_bytes(bytes[12:16], byteorder='little')
        event.set_fms_height(height)

    if ms_type == "EMS":
        print("EMS event detected")

    return event

def EventToBytes(event, ms_type):
    bytes = bytearray(24)
    bytes[0:4] = event.time_bytes
    bytes[4:5] = event.type_bytes
    bytes[16:18] = event.rotation_bytes

    if ms_type == "BMS":
        bytes[12:13] = event.lane_bytes

    if ms_type == "FMS":
        bytes[12:13] = event.fms_height_bytes

    return bytes


def ExtractEvents(raw_bytes):
    events = ChunkToEvents(raw_bytes)
    return events

def CompileEvents(events, ms_type):
    compiled = bytearray()
    for event in events:
        compiled.extend(EventToBytes(event, ms_type))
    return compiled

def ExportEvents(events, header_data):
    all = bytearray()
    all.extend(header_data)
    ms_type = MSType(header_data[0:4])
    all.extend(CompileEvents(events, ms_type))
    return all

def CreateChart(events, output_file, header_data):
    try:
        with open(output_file, "wb") as f:
            compress_nlz11(ExportEvents(events, header_data), f)
            print(f"Chart created successfully: {output_file}")
    except Exception as e:
        print(f"Error creating chart: {e}")
    return output_file