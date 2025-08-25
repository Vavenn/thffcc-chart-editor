
from PySide6.QtWidgets import (
    QApplication, QPushButton, QSizePolicy, QWidget, QLineEdit, QLabel, 
    QVBoxLayout, QTextEdit, QGridLayout, QGroupBox, QHBoxLayout, QTableWidget,
    QTableWidgetItem
)
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, QSettings, QEvent)
from PySide6.QtGui import (QBrush, QColor)
from matplotlib.pylab import f
import sys
import os
import csv

from ccChartEdit import ccfile

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.are_paths_valid = False
        self.rippath = None
        self.modpath = None

        self.current_ccfile = None

        self.main_layout = QHBoxLayout()
        self.left_panel = QVBoxLayout()



        self.group_input_paths = QGroupBox("Input Paths")
        self.group_input_paths.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.left_panel.addWidget(self.group_input_paths, stretch=0)

        self.layout_input_paths = QVBoxLayout()
        self.group_input_paths.setLayout(self.layout_input_paths)

        self.label_input_rip_files = QLabel("Ripped Files:")
        self.textinput_rip_files = QLineEdit()
        self.label_input_mod = QLabel("Modified Files:")
        self.textinput_mod = QLineEdit()

        self.button_set_input_paths = QPushButton("Set Input Paths")
        self.button_set_input_paths.clicked.connect(self.set_input_paths)

        self.layout_input_paths.addWidget(self.label_input_rip_files)
        self.layout_input_paths.addWidget(self.textinput_rip_files)
        self.layout_input_paths.addWidget(self.label_input_mod)
        self.layout_input_paths.addWidget(self.textinput_mod)
        self.layout_input_paths.addWidget(self.button_set_input_paths)


        # Add a read-only QTextEdit for feedback
        self.feedback_box = QTextEdit()
        self.feedback_box.setReadOnly(True)
        self.feedback_box.setPlaceholderText("")
        self.feedback_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.left_panel.addWidget(self.feedback_box, stretch=1)
        self.main_layout.addLayout(self.left_panel)
        self.feedback_box.setText(" . . . ")



    # Create a QWidget to contain the song selection layout and set its max width
        self.song_selection_widget = QWidget()
        self.song_selection_widget.setMaximumWidth(300)
        self.layout_song_selection = QVBoxLayout(self.song_selection_widget)

        self.main_layout.addWidget(self.song_selection_widget)

        self.chart_list = QTableWidget()

        self.chart_list.setColumnCount(2)
        self.chart_list.setColumnWidth(0, 300)
        self.chart_list.hideColumn(1)
        self.chart_list.setSelectionMode(QTableWidget.SingleSelection)
        self.chart_list.horizontalHeader().setVisible(False)
        self.chart_list.verticalHeader().setVisible(False)
        self.chart_list.setStyleSheet("QTableWidget::item:selected { background-color: rgba(100, 100, 100, 155); }")
        self.chart_list.setSelectionBehavior(QTableWidget.SelectRows)

        self.layout_song_selection_top = QVBoxLayout()
        self.layout_song_selection.addLayout(self.layout_song_selection_top)

        self.button_select_chart = QPushButton("Select Chart")
        self.button_select_chart.pressed.connect(self.load_chart_data)
        self.layout_song_selection_top.addWidget(self.button_select_chart)
        self.layout_song_selection.addWidget(self.chart_list)


        self.layout_chart_data = QGridLayout()


        #self.only_int = QIntValidator()


        self.label_chart_type_flag = QLabel("xMS Flag")
        self.layout_chart_data.addWidget(self.label_chart_type_flag, 0, 0)
        self.chart_type_flag = QLineEdit()
        self.layout_chart_data.addWidget(self.chart_type_flag, 0, 1)

        self.label_param2 = QLabel("Unknown 2:")
        self.layout_chart_data.addWidget(self.label_param2, 1, 0)
        self.chart_param2 = QLineEdit()
        self.layout_chart_data.addWidget(self.chart_param2, 1, 1)

        self.label_param3 = QLabel("Unknown 3:")
        self.layout_chart_data.addWidget(self.label_param3, 2, 0)
        self.chart_param3 = QLineEdit()
        self.layout_chart_data.addWidget(self.chart_param3, 2, 1)

        self.label_param4 = QLabel("Unknown 4:")
        self.layout_chart_data.addWidget(self.label_param4, 3, 0)
        self.chart_param4 = QLineEdit()
        self.layout_chart_data.addWidget(self.chart_param4, 3, 1)

        self.label_param5 = QLabel("Unknown 5:")
        self.layout_chart_data.addWidget(self.label_param5, 4, 0)
        self.chart_param5 = QLineEdit()
        self.layout_chart_data.addWidget(self.chart_param5, 4, 1)

        self.label_param6 = QLabel("Unknown 6:")
        self.layout_chart_data.addWidget(self.label_param6, 5, 0)
        self.chart_param6 = QLineEdit()
        self.layout_chart_data.addWidget(self.chart_param6, 5, 1)

        self.label_param7 = QLabel("Unknown 7:")
        self.layout_chart_data.addWidget(self.label_param7, 6, 0)
        self.chart_param7 = QLineEdit()
        self.layout_chart_data.addWidget(self.chart_param7, 6, 1)

        self.label_param8 = QLabel("Unknown 8:")
        self.layout_chart_data.addWidget(self.label_param8, 7, 0)
        self.chart_param8 = QLineEdit()
        self.layout_chart_data.addWidget(self.chart_param8, 7, 1)

        self.label_param9 = QLabel("Unknown 9:")
        self.layout_chart_data.addWidget(self.label_param9, 8, 0)
        self.chart_param9 = QLineEdit()
        self.layout_chart_data.addWidget(self.chart_param9, 8, 1)

        self.label_param10 = QLabel("Unknown 10:")
        self.layout_chart_data.addWidget(self.label_param10, 9, 0)
        self.chart_param10 = QLineEdit()
        self.layout_chart_data.addWidget(self.chart_param10, 9, 1)

        self.main_layout.addLayout(self.layout_chart_data)
        self.label_param4 = QLabel("Unknown 4:")
        self.layout_chart_data.addWidget(self.label_param4, 3, 0)

        self.chart_param4 = QLineEdit()
        self.layout_chart_data.addWidget(self.chart_param4, 3, 1)

        self.main_layout.addLayout(self.layout_chart_data)

        self.retrieve_settings()




    def load_chart_data(self):
        selected = self.chart_list.currentRow()
        if selected < 0:
            self.feedback("No chart selected.")
            return
        # Get the fileid from the hidden column 1
        fileid_item = self.chart_list.item(selected, 1).text()
        self.current_ccfile = ccfile(
            "trigger002.bytes.lz",
            self.rippath,
            fileid_item,
            self.modpath
        )

    
        try:
            data = self.current_ccfile.read()
            self.chart_type_flag.setText(str(int.from_bytes(data[:4], "little")))
            self.chart_param2.setText(str(int.from_bytes(data[4:8], "little")))
            self.chart_param3.setText(str(int.from_bytes(data[8:12], "little")))
            self.chart_param4.setText(str(int.from_bytes(data[12:16], "little")))
            self.chart_param5.setText(str(int.from_bytes(data[16:20], "little")))
            self.chart_param6.setText(str(int.from_bytes(data[20:24], "little")))
            self.chart_param7.setText(str(int.from_bytes(data[24:28], "little")))
            self.chart_param8.setText(str(int.from_bytes(data[28:32], "little")))
            self.chart_param9.setText(str(int.from_bytes(data[32:36], "little")))
            self.chart_param10.setText(str(int.from_bytes(data[36:40], "little")))
        except Exception as e:
            self.feedback(f"Failed to load chart data: {e}")


    def set_input_paths(self):
        ripped_files = self.textinput_rip_files.text()
        modified_files = self.textinput_mod.text()

        # path verification
        if not ripped_files or not modified_files:
            self.feedback("Input path cannot be empty.")
            return
        if ripped_files == modified_files:
            self.feedback("Ripped and Modified paths cannot be the same.")
            return
        if not os.path.exists(ripped_files):
            self.feedback("Ripped Files path does not exist.")
            return
        if not os.path.exists(modified_files):
            self.feedback("Modified Files path does not exist.")
            return

        if os.path.exists(f"{ripped_files}/romfs"):
            ripped_files = f"{ripped_files}/romfs"

        if not ripped_files.endswith("romfs"):
            self.feedback("Ripped Files must be or contain a 'romfs' folder.")
            return

        self.feedback(f"Ripped Files: {ripped_files}\nModified Files: {modified_files}")
        #store paths using QSettings
        settings = QSettings("Vaven", "ThffccChartEditor")
        settings.setValue("ripped_files", ripped_files)
        settings.setValue("modified_files", modified_files)
        self.are_paths_valid = True
        self.modpath = modified_files
        self.rippath = ripped_files
        self.get_chart_list()

    def feedback(self, message):
        prev_text = self.feedback_box.toPlainText()
        self.feedback_box.setText(message + "\n" + prev_text)

    def retrieve_settings(self):
        settings = QSettings("Vaven", "ThffccChartEditor")
        ripped_files = settings.value("ripped_files", "")
        modified_files = settings.value("modified_files", "")
        self.textinput_rip_files.setText(ripped_files)
        self.textinput_mod.setText(modified_files)
        self.feedback("Settings retrieved.")
        self.set_input_paths()

    def get_chart_list(self):
        if not self.are_paths_valid:
            self.feedback("Invalid paths. Please set valid input paths.")
            return

        self.feedback("Getting chart list...")
        self.chart_list.clearContents()

        try:
            with open(f"{self.rippath}/table/MusicTable.csv", "r", newline="", encoding="utf-16-le") as f:
                reader = csv.reader(f)
                rows = list(reader)
                self.chart_list.setRowCount(len(rows))
                for i, row in enumerate(rows):

                    name = row[7] if len(row) > 6 else ""
                    fileid = row[0] if len(row) > 0 else ""
                    nameitem = QTableWidgetItem(name)
                    if "BMS" in fileid:
                        nameitem.setBackground(QBrush(QColor(100, 45, 45)))
                    if "FMS" in fileid:
                        nameitem.setBackground(QBrush(QColor(45, 100, 45)))
                    if "EMS" in fileid:
                        nameitem.setBackground(QBrush(QColor(45, 45, 100)))
                    self.chart_list.setItem(i, 0, nameitem)
                    fileiditem = QTableWidgetItem(fileid)
                    self.chart_list.setItem(i, 1, fileiditem)
                self.feedback("Chart list retrieved successfully.")
        except Exception as e:
            self.feedback(f"Error retrieving chart list: {e}")
            self.chart_list.setRowCount(0)

def main():
    

    app = QApplication(sys.argv)
    window = QWidget()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.setLayout(ui.main_layout)
    window.resize(1200, 800)
    window.show()
    sys.exit(app.exec())
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

