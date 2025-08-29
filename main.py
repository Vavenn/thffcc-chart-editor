# le thffcc map editor

from lzss3 import decompress_bytes
from compress import compress_nlz11
from parser import *
from ccChartEdit import ExtractEvents, ExportEvents, ccfile
from midiTools import ExportMidi, ImportMidi

from ui import main as Ui_Main

import pathlib
current_path = pathlib.Path(__file__).parent.resolve()

Ui_Main()