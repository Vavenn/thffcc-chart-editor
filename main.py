# le thffcc map editor
from ast import dump
import shutil
import os
import matplotlib.pyplot as plt

from lzss3 import decompress_bytes
from compress import compress_nlz11
from parser import *
from ccChartEdit import ExtractEvents, ExportEvents
from midiTools import ExportMidi, ImportMidi

import matplotlib.pyplot as plt


import pathlib
current_path = pathlib.Path(__file__).parent.resolve()

base_path = "C:/Users/pc/3D Objects/DS - 3DS/romfs"
mod_base_path = "C:/Users/pc/AppData/Roaming/Citra/load/mods/00040000000FCA00/romfs"

midi_to_import = "C:/Users/pc/Desktop/wha chart thffcc.mid"

loaded_map = "0800_BMS_007" # the extreme

#loaded_map = "1100_BMS_005" # fighters of the crystal


class ccfile:
    def __init__(self, name):
        self.name = name
        self.path_original = f"{base_path}/music/{loaded_map}/{name}"
        self.path_backup = f"{base_path}/music/{loaded_map}/{name}.bak"
        self.path_modw = f"{mod_base_path}/music/{loaded_map}/{name}"
        self.path_modw_folder = f"{mod_base_path}/music/{loaded_map}"
        self.path_mod = self.path_modw
        if not os.path.exists(self.path_mod):
            self.path_mod = self.path_original

    def __str__(self):
        return f"{self.name} at {self.path_original}"

    def read(self):
        with open(self.path_backup, "rb") as f:
            bytes = f.read()
            return decompress_bytes(bytes)

    def readMod(self):
        with open(self.path_mod, "rb") as f:
            bytes = f.read()
            return decompress_bytes(bytes)

    def write(self, data, compress_nlz11 = True):
        # create a "loaded_map" folder if nonexistent
        os.makedirs(self.path_modw_folder, exist_ok=True)
        with open(self.path_modw, "wb") as f:
            if compress_nlz11:
                compress_nlz11(data, f)
            else:
                f.write(data)

    def checkBackup(self):
        if not os.path.exists(self.path_backup):
            print(f"Backup not found for {self.name}, creating one.")
            shutil.copy(self.path_original, self.path_backup)

    def basePath(self):
        return self.path_original
    
    def modPath(self):
        return self.path_mod


music_data_file = ccfile("music.bcsar")
music_audio_file = ccfile("music.dspadpcm.bcstm")
nm_chart_file = ccfile("trigger000.bytes.lz")
em_chart_file = ccfile("trigger001.bytes.lz")
um_chart_file = ccfile("trigger002.bytes.lz")

files = [
    music_data_file,
    music_audio_file,
    nm_chart_file,
    em_chart_file,
    um_chart_file
    ]

def bytes_to_binary(data):
    return ''.join(format(byte, '08b') for byte in data)

def make_backup(file):
    shutil.copy(file, f"{file}.bak")

def retrieve_backup():
    shutil.copy(f"{music_data_file}.bak", music_data_file)
    shutil.copy(f"{music_audio_file}.bak", music_audio_file)
    shutil.copy(f"{nm_chart_file}.bak", nm_chart_file)
    shutil.copy(f"{em_chart_file}.bak", em_chart_file)
    shutil.copy(f"{um_chart_file}.bak", um_chart_file)

for file in files:
    file.checkBackup()

def scramble_bytes(data, start_byte, end_byte):
    scrambled_data = bytearray(data)
    for i in range(start_byte, end_byte):
        if scrambled_data[i] != 0:
            scrambled_data[i] = (scrambled_data[i] + 1) % 256  # Simple increment scramble
    return scrambled_data

def zero_bytes(data, start_byte, end_byte):
    zeroed_data = bytearray(data)
    for i in range(start_byte, end_byte):
        zeroed_data[i] = 0  # Set bytes to zero
    return zeroed_data

def increment(data, byte, amount):
    incremented_data = bytearray(data)
    incremented_data[byte] = (incremented_data[byte] + amount) % 256
    return incremented_data

def diff(file):
    original_data = bytearray(file.read())
    modified_data = bytearray(file.readMod())

    out = []
    for i in range(min(len(original_data), len(modified_data))):
        if original_data[i] != modified_data[i]:
            out.append(modified_data[i])
        else:
            out.append(-1)

    #trim extra -1s
    while out and out[-1] == -1:
        out.pop()

    return out


current_file = um_chart_file

test_data = current_file.read()
dump_path = f"{current_path}/{loaded_map} - {(current_file.name.replace('.lz', '.bin'))}"
print(dump_path)
with open(dump_path, "wb") as dummy_file:
    dummy_file.write(test_data)

Events = ExtractEvents(test_data)

lanes = [event.lane for event in Events]
time = [event.time for event in Events]
event_types = [event.event_type for event in Events]

plt.figure(figsize=(10, 4))

colors = {
    "tap": "red",
    "hold start": "green",
    "hold end": "green",
    "hold slide": "blue",
    "slide": "yellow",
    "unknown": "black",
    # Add more event types and colors as needed
}





plt.gca().invert_yaxis()
point_colors = [colors.get(et, "black") for et in event_types]
plt.scatter(time, lanes, s=10, c=point_colors)


plt.tight_layout()
# plt.show()

# current_file.write(test_data)

# outmidi = ExportMidi(Events, current_path / "exportedeee.mid")

imported_events = ImportMidi(midi_to_import)
em_chart_file.write(ExportEvents(imported_events))