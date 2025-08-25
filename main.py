# le thffcc map editor
from ast import dump
from math import pi
import shutil
import os
import matplotlib.pyplot as plt

from lzss3 import decompress_bytes
from compress import compress_nlz11
from parser import *
from ccChartEdit import ExtractEvents, ExportEvents, ccfile
from midiTools import ExportMidi, ImportMidi

from ui import main as Ui_Main

import pathlib
current_path = pathlib.Path(__file__).parent.resolve()

# base_path = "C:/Users/pc/3D Objects/DS - 3DS/romfs"
# mod_base_path = "C:/Users/pc/AppData/Roaming/Citra/load/mods/00040000000FCA00/romfs"

# midi_to_import = "C:/Users/pc/Desktop/wha chart thffcc.mid"

# loaded_map = "0800_BMS_007" # the extreme

# #loaded_map = "1100_BMS_005" # fighters of the crystal



    



# music_data_file = ccfile("music.bcsar")
# music_audio_file = ccfile("music.dspadpcm.bcstm")
# nm_chart_file = ccfile("trigger000.bytes.lz")
# em_chart_file = ccfile("trigger001.bytes.lz")
# um_chart_file = ccfile("trigger002.bytes.lz")


def bytes_to_binary(data):
    return ''.join(format(byte, '08b') for byte in data)

def make_backup(file):
    shutil.copy(file, f"{file}.bak")

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


# test_data = current_file.read()
# dump_path = f"{current_path}/{loaded_map} - {(current_file.name.replace('.lz', '.bin'))}"
# with open(dump_path, "wb") as dummy_file:
#     dummy_file.write(test_data)





# current_file.write(test_data)

# outmidi = ExportMidi(Events, current_path / "exportedeee.mid")

# imported_events = ImportMidi(midi_to_import)
# em_chart_file.write(ExportEvents(imported_events))

Ui_Main()