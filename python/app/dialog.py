# -*- coding: utf-8 -*-

"""
This script is the main entry point for the app.
it will create the dialog and handle the logic for the app.
"""

__author__ = "Juno Park"
__github__ = "https://github.com/junopark00"


import os
import sys
import shutil
from collections import defaultdict

import sgtk
from sgtk.platform.qt import QtCore, QtGui

from .ui.dialog import Ui_Dialog
from .excel_manager import ExcelManager
from .generate_converter import GenerateConverter
from .validate_version import ValidateVersion
from .validate_src_version import ValidateSrcVersion
from .validate_timecode import ValidateTimecode
from .validate_shot_for_editorial import ValidateShotForEditorial
from .collect import Collect
from .publish import Publish
from . import cleanup


# Set standard sgtk logger
logger = sgtk.platform.get_logger(__name__)

def show_dialog(app_instance):
    """
    Shows the main dialog window.
    """
    # import and define the dialog
    app_instance.engine.show_dialog("IO Manager", app_instance, AppDialog)
    

class AppDialog(QtGui.QWidget):
    """
    Main application dialog window
    """
    
    def __init__(self):
        """
        Constructor
        """
        QtGui.QWidget.__init__(self)
        
        logger.info("Starting IO Manager")
        
        # set up the UI
        self.ui = Ui_Dialog() 
        self.ui.setupUi(self)
        
        # set column index
        """
        This variable needs to be redefined
        according to each column in the Excel file.
        """
        self._check_column = 0
        self._thumnbail_column = 1
        self._version_column = 5
        
        # set variables
        self._app = sgtk.platform.current_bundle()
        self._sg = self._app.shotgun
        self._current_project_path = self._app.context.filesystem_locations[0]
        self._excel_path = ""
        self.colorspace = ""
        self.checked_data = {}
        self._excel_manager = ExcelManager()
        self._current_dir = os.path.dirname(__file__)
        self._temp_images = os.path.join(self._current_dir, ".temp_images")
        self._validate_version = ValidateVersion([], {}, "")
        self._validate_src_version = ValidateSrcVersion()
        self._validate_timecode = ValidateTimecode()
        self._validate_shot_for_editorial = ValidateShotForEditorial()
        self._generate_converter = GenerateConverter({}, False, False, "", "")
        self._collect = Collect()
        self._publish = Publish([], "")
        self._cleanup = cleanup
        
        # set flags and connections
        self.__flags()
        self.__connections()
        
    def __flags(self) -> None:
        """
        Set flags for the app.
        """
        self.excel_loaded = False
        
    def __connections(self) -> None:
        """
        Set connections for the app.
        """
        self.ui.button_select_path.clicked.connect(self.select_excel)
        self.ui.button_load_path.clicked.connect(self.load_excel)
        self.ui.button_check_all.clicked.connect(self.check_all)
        self.ui.button_uncheck_all.clicked.connect(self.uncheck_all)
        self.ui.button_excel_save.clicked.connect(lambda: self.save_excel(True))
        self.ui.button_excel_edit.clicked.connect(lambda: self.save_excel(False))
        self.ui.button_validate_version.clicked.connect(self.validate_version)
        self.ui.button_validate_src_version.clicked.connect(self.validate_src_version)
        self.ui.button_validate_timecode.clicked.connect(self.validate_timecode)
        self.ui.button_validate_shot_for_editorial.clicked.connect(self.validate_shot_for_editorial)
        self.ui.button_collect.clicked.connect(self.collect)
        self.ui.button_publish.clicked.connect(self.publish)
        
    def select_excel(self) -> None:
        """
        When the select button is clicked, this method is called.
        It opens a file dialog and sets the path to the selected file.
        """
        
        # Open file dialog
        self._excel_path = QtGui.QFileDialog.getOpenFileName(
            self, 
            "Select Excel File", 
            "/RAPA/plate_data", 
            "Excel Files (*.xls *.xlsx *.xlsm)"
            )[0]
        _, ext = os.path.splitext(self._excel_path)
        
        if not self._excel_path:
            return
        
        if ext not in [".xls", ".xlsx", ".xlsm"]:
            logger.error("Invalid file format. Please select an Excel file.")
            QtGui.QMessageBox.critical(
                self, 
                "Error", 
                "Invalid file format. Please select an Excel file."
                )
            return
        
        # openpyxl does not support Excel 97-2003 format
        if ext == ".xls":
            logger.warning("Excel 97-2003 format (*.xls) is not supported.")
            QtGui.QMessageBox.warning(
                self, 
                "Warning", 
                "Excel 97-2003 format (*.xls) is not supported."
                )
            return
        
        self.ui.line_edit_path.setText(self._excel_path)
        logger.info("Selected Excel file: %s" % self._excel_path)
        
    def load_excel(self) -> None:
        """
        When the load button is clicked, this method is called.
        It loads the Excel file and displays the data in the table widget.
        """
        if not self.ui.line_edit_path.text():
            logger.error("No Excel file selected.")
            QtGui.QMessageBox.critical(
                self, 
                "Error", 
                "No Excel file selected."
                )
            return
        
        if not os.path.exists(self.ui.line_edit_path.text()):
            logger.error("Excel file not found.")
            QtGui.QMessageBox.critical(
                self, 
                "Error", 
                "Excel file %s not found." % self._excel_path
                )
            return
        
        # If the Excel file is already loaded, clear the table widget
        if self.excel_loaded:
            self.ui.table_widget.clear()
            self.excel_loaded = False
            
        logger.info("Loading Excel file: %s" % self._excel_path)
        
        # Load the Excel file
        self._excel_manager.load_excel(self._excel_path)
        
        # Update the UI with the loaded data
        self.update_ui_from_excel()
        
        # Set the flag to True
        self.excel_loaded = True
        self.ui.label_excel_path.setText(self._excel_path)
    
    def update_ui_from_excel(self) -> None:
        """
        Update the UI with the loaded data.
        """
        logger.debug("Updating UI from Excel")
        # Get data from excel manager
        row_heights = self._excel_manager.row_heights
        column_widths = self._excel_manager.column_widths
        header_labels = self._excel_manager.header_labels
        cell_values = self._excel_manager.cell_values
        thumbnails = self._excel_manager.loaded_images
        
        # Set row and column count
        self.ui.table_widget.setRowCount(max(row_heights.keys()) - 1)
        self.ui.table_widget.setColumnCount(max(column_widths.keys()))
        self.ui.table_widget.setHorizontalHeaderLabels(header_labels)
        
        # Set row heights
        for row, height in row_heights.items():
            # data starts from row 2, so subtract 2
            # Set the row height to 1.6 times the original height
            self.ui.table_widget.setRowHeight(row - 2, height*1.6)
            
        # Set column widths
        for column, width in column_widths.items():
            # data starts from column 1, so subtract 1
            # Set the column width to 9 times the original width
            self.ui.table_widget.setColumnWidth(column - 1, width*9)
            
        # Set cell values
        for (row, column), value in cell_values.items():
            item = QtGui.QTableWidgetItem(value)
            # skip the header row
            self.ui.table_widget.setItem(row - 1, column, item)
                
        # Set the first column to be checkable only
        for row in range(self.ui.table_widget.rowCount()):
            item = self.ui.table_widget.item(row, self._check_column)
            if item:
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                item.setCheckState(QtCore.Qt.Unchecked)
        
        # Set thumbnail column
        for image_path in thumbnails:
            # parse the image path to get the row and column
            # ex) {self.temp_dir}/{row}_{column}.png
            filename = os.path.splitext(os.path.basename(image_path))[0]
            row, column = filename.split("_")
            q_image = QtGui.QImage(image_path)
            pixmap = QtGui.QPixmap.fromImage(q_image)

            # Get the current cell size
            cell_width = self.ui.table_widget.columnWidth(int(column) - 1)
            cell_height = self.ui.table_widget.rowHeight(int(row) - 2)

            # Scale the pixmap to fit the cell size, 
            # preserving the aspect ratio
            scaled_pixmap = pixmap.scaled(
                cell_width, 
                cell_height, 
                QtCore.Qt.KeepAspectRatio, 
                QtCore.Qt.SmoothTransformation
                )

            item = QtGui.QTableWidgetItem()
            item.setData(QtCore.Qt.DecorationRole, scaled_pixmap)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.table_widget.setItem(
                int(row) - 2, int(column) - 1, item
                )
        
        # Resize the row to fit the content
        self.ui.table_widget.resizeRowsToContents()
        
        logger.debug("UI updated from Excel")
    
    def check_all(self) -> None:
        """
        When the check all button is clicked, this method is called.
        It checks all the checkboxes in the first column.
        """
        if not self.excel_loaded:
            logger.error("No Excel file loaded.")
            QtGui.QMessageBox.critical(
                self, 
                "Error", 
                "No Excel file loaded."
                )
            return
        
        logger.debug("Checking all rows")
        
        for row in range(self.ui.table_widget.rowCount()):
            item = self.ui.table_widget.item(row, self._check_column)
            if item:
                item.setCheckState(QtCore.Qt.Checked)
                
    def uncheck_all(self) -> None:
        """
        When the uncheck all button is clicked, this method is called.
        It unchecks all the checkboxes in the first column.
        """
        if not self.excel_loaded:
            logger.error("No Excel file loaded.")
            QtGui.QMessageBox.critical(
                self, 
                "Error", 
                "No Excel file loaded."
                )
            return
        
        logger.debug("Unchecking all rows")
        
        for row in range(self.ui.table_widget.rowCount()):
            item = self.ui.table_widget.item(row, self._check_column)
            if item:
                item.setCheckState(QtCore.Qt.Unchecked)
                
    def save_excel(self, version_up: bool) -> None:
        """
        When the save or edit button is clicked, this method is called.
        It saves the Excel file as a new version.
        """
        if not self.excel_loaded:
            logger.error("No Excel file loaded.")
            QtGui.QMessageBox.critical(
                self, 
                "Error", 
                "No Excel file loaded."
                )
            return
        
        if not os.path.exists(self._excel_path):
            logger.error("Excel file not found: %s" % self._excel_path)
            QtGui.QMessageBox.critical(
                self, 
                "Error", 
                "Excel file %s not found." % self._excel_path
                )
            return
        
        if version_up:
            confirm = QtGui.QMessageBox.question(
                self, 
                "Version Up", 
                "Are you sure you want to save the Excel file as a new version?", 
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No
                )
        else:
            confirm = QtGui.QMessageBox.warning(
                self, 
                "Overwrite", 
                "Are you sure you want to overwrite the Excel file?", 
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No
                )
        
        if confirm == QtGui.QMessageBox.Yes:
            logger.debug("Saving Excel file: %s" % self._excel_path)
            
            # Get table widget data
            header_data, cell_data = self.get_table_data()
            saved_path = self._excel_manager.save_excel(
                header_data, 
                cell_data, 
                self._excel_path, 
                version_up
                )
            QtGui.QMessageBox.information(
                self, 
                "Saved", 
                "Excel file saved to %s" % saved_path
                )
            logger.debug("Excel file saved to %s" % saved_path)
        else:
            logger.debug("Save canceled.")
            
    def get_table_data(self) -> dict:
        """
        Get the data from the table widget.
        
        Returns:
            dict: Dictionary of cell values
        """
        logger.debug("Getting table data")
        
        header_data = []
        cell_data = []
        
        # Get header labels as the first row
        for column in range(self.ui.table_widget.columnCount()):
            header_item = self.ui.table_widget.horizontalHeaderItem(column)
            header_data.append(header_item.text())
            
        # Get cell values
        for row in range(self.ui.table_widget.rowCount()):
            row_data = []
            for column in range(self.ui.table_widget.columnCount()):
                item = self.ui.table_widget.item(row, column)
                if item:
                    row_data.append(item.text())
                else:
                    row_data.append("")
            cell_data.append(row_data)
        
        logger.debug("Table data retrieved")
        
        return header_data, cell_data

    def validate_version(self) -> None:
        """
        When the validate version button is clicked, this method is called.
        It gets the version from the 'Version' entity and updates UI.
        """
        if not self.excel_loaded:
            logger.error("No Excel file loaded.")
            QtGui.QMessageBox.critical(
                self, 
                "Error", 
                "No Excel file loaded."
                )
            return
        
        self.checked_data = self.get_checked_data()
        self.colorspace = self.ui.comboBox_colorspace.currentText()
        
        # get the 'Version' entity data from ShotGrid
        try:
            entity_type = "Version"
            filters = [["project", "is", self._app.context.project]]
            fields = ["code"]
            sg_data = self._sg.find(entity_type, filters, fields)
        except Exception as e:
            logger.error("Failed to get ShotGrid data: %s" % e)
            QtGui.QMessageBox.critical(
                self, 
                "Error", 
                "Failed to get ShotGrid data."
                )
            return
        
        # if no data found, set version to 1
        if not sg_data:
            logger.info("ShotGrid 'Version' entity's 'code' field not found.")
            for row in self.checked_data.keys():
                self.ui.table_widget.item(row, self._version_column).setText("1")
                self.ui.table_widget.item(row, self._version_column).setSelected(True)
            return
        
        # check if the checked data is empty
        if not self.checked_data:
            logger.error("No data checked")
            QtGui.QMessageBox.critical(
                self, 
                "Error", 
                "No data checked."
                )
            return
        
        # validate the version
        logger.debug("Validating version")
        version = ValidateVersion(
            sg_data, self.checked_data, self.colorspace
            ).validated_version
        
        # update the UI with the validated version
        for row, version in version.items():
            self.ui.table_widget.item(row, self._version_column).setText(str(version))
            self.ui.table_widget.item(row, self._version_column).setSelected(True)
        
        logger.debug("Version validated")

    def get_checked_data(self) -> dict:
        """
        Get the checked data from the table widget.
        
        Returns:
            dict: Dictionary of checked data
        """
        logger.debug("Getting checked data")
        
        checked_rows = []
        for row in range(self.ui.table_widget.rowCount()):
            item = self.ui.table_widget.item(row, 0)
            if item and item.checkState() == QtCore.Qt.Checked:
                checked_rows.append(row)
        
        checked_data = {}
        for row in checked_rows:
            row_data = {}
            for column in range(self.ui.table_widget.columnCount()):
                item = self.ui.table_widget.item(row, column)
                column_name = self.ui.table_widget.horizontalHeaderItem(column).text()
                row_data[column_name] = item.text()
            checked_data[row] = row_data
        
        logger.debug("Checked data retrieved")
        
        return checked_data
    
    def validate_src_version(self) -> None:
        """
        When the validate src version button is clicked, this method is called.
        """
        if not self.excel_loaded:
            logger.error("No Excel file loaded.")
            QtGui.QMessageBox.critical(
                self, 
                "Error", 
                "No Excel file loaded."
                )
            return
        
        self._validate_src_version = ValidateSrcVersion()
        logger.info("This button is not implemented yet.")
    
    def validate_timecode(self) -> None:
        """
        When the validate timecode button is clicked, this method is called.
        """
        if not self.excel_loaded:
            logger.error("No Excel file loaded.")
            QtGui.QMessageBox.critical(
                self, 
                "Error", 
                "No Excel file loaded."
                )
            return
        
        self._validate_timecode = ValidateTimecode()
        logger.info("This button is not implemented yet.")
    
    def validate_shot_for_editorial(self) -> None:
        """
        When the validate shot for editorial button is clicked, this method is called.
        """
        if not self.excel_loaded:
            logger.error("No Excel file loaded.")
            QtGui.QMessageBox.critical(
                self, 
                "Error", 
                "No Excel file loaded."
                )
            return
        
        self._validate_shot_for_editorial = ValidateShotForEditorial()
        logger.info("This button is not implemented yet.")
    
    def collect(self) -> None:
        """
        When the collect button is clicked, this method is called.
        """
        if not self.excel_loaded:
            logger.error("No Excel file loaded.")
            QtGui.QMessageBox.critical(
                self, 
                "Error", 
                "No Excel file loaded."
                )
            return
        
        self._collect = Collect()
        logger.info("This button is not implemented yet.")
    
    def publish(self) -> None:
        """
        When the publish button is clicked, this method is called.
        It generates the converters and executes them.
        Finally, it publishes the data to ShotGrid.
        """
        logger.info("Publishing data")
        if not self.excel_loaded:
            logger.error("No Excel file loaded.")
            QtGui.QMessageBox.critical(
                self, 
                "Error", 
                "No Excel file loaded."
                )
            return
        
        # set data
        self.checked_data = self.get_checked_data()
        self.grouped_data = self.group_data(self.checked_data)
        self.colorspace = self.ui.comboBox_colorspace.currentText()
        
        # validate data
        logger.debug("Validating data")
        self.validate_version()
        self.validate_timecode()
        self.validate_src_version()
        self.validate_shot_for_editorial()
        
        # generate converter
        logger.debug("Generating converter")
        converters = self.generate_converter()
        logger.debug("Converters: %s" % converters)
        
        # execute converter
        logger.debug("Executing converter")
        completed_converter = self._generate_converter.execute(converters)
        logger.debug("Completed converter: %s" % completed_converter)

        # publish data
        self.publish_to_shotgrid()
        
        # cleanup
        logger.debug("Cleaning up")
        if self.ui.checkbox_cliplib.isChecked():
            self._cleanup.cleanup_temp_files(completed_converter, True)
        else:
            self._cleanup.cleanup_temp_files(completed_converter, False)
        logger.debug("Cleaned up")
        
        logger.info("Publish completed")
    
    def generate_converter(self):
        """
        Generate the converter for the given dataset.
        """
        # check if MOV to DPX checkbox is checked
        if self.ui.checkbox_mov_to_dpx.isChecked():
            mov_to_dpx = True
        else:
            mov_to_dpx = False
        
        # get codec from Project entity, if not found, use default codec
        try:
            entity_type = "Project"
            filters = [["id", "is", self._app.context.project["id"]]]
            fields = ["sg_codec"]
            codec = self._sg.find_one(entity_type, filters, fields)["sg_codec"]
        except Exception as e:
            logger.error("Failed to get ShotGrid data: %s" % e)
            logger.error("Using default codec: Apple ProRes 4444")
            codec = "Apple ProRes 4444"
        
        if not self.checked_data:
            logger.error("No data checked")
            QtGui.QMessageBox.critical(
                self, 
                "Error", 
                "No data checked."
                )
            return

        script_paths = []
        for data in self.grouped_data:
            # check if retime info in the data
            # if exists, apply retime = True
            if (data["retime_start_frame"] and
                data["retime_duration"] and
                data["retime_percent"]):
                apply_retime = True
            else:
                apply_retime = False

            # generate the converter
            self._generate_converter = GenerateConverter(
                data, mov_to_dpx, apply_retime, self.colorspace, codec
                )
            self._generate_converter.set_data()
            script_path = self._generate_converter.generate()
            script_paths.append(script_path)
        
        return script_paths
            
    def group_data(self, checked_data: dict) -> list[dict]:
        """
        Group the data by seq_name and shot_name.

        Args:
            checked_data (dict): Dictionary of checked data

        Returns:
            list[dict]: List of grouped data
        """
        # group data by seq_name and shot_name
        grouped_data = defaultdict(lambda: defaultdict(list))

        # Group data by seq_name and shot_name
        for row, data in checked_data.items():
            key = (data['seq_name'], data['shot_name'])  # ex) ('seq_001', 'seq001_shot_001')
            for k, v in data.items():  # ex) (k: column_name, v: cell_value)
                if v not in grouped_data[key][k]:  # Avoid duplicates
                    grouped_data[key][k].append(v)
                else:
                    # if the value is already in the list but it's retime data, append it
                    if k in ['retime_start_frame', 'retime_duration', 'retime_percent']:
                        grouped_data[key][k].append(v)

        # Flatten the grouped data
        final_data = []
        for key, value in grouped_data.items():
            flattened = {}
            for k, v in value.items():
                if len(v) > 1:
                    flattened[k] = v
                else:
                    flattened[k] = v[0]

            # if the data is a list,
            # Get the min start frame, max end frame, and sum duration
            if (isinstance(flattened["start_frame"], list) and
                isinstance(flattened["end_frame"], list) and
                isinstance(flattened["duration"], list)):
                min_start_frame = min(list(map(int, flattened['start_frame'])))
                max_end_frame = max(list(map(int, flattened['end_frame'])))
                sum_duration = sum(list(map(int, flattened['duration'])))
                flattened['start_frame'] = min_start_frame
                flattened['end_frame'] = max_end_frame
                flattened['duration'] = sum_duration
            
            # if the data is a list,
            # Get the min just in, max just out
            if (isinstance(flattened['just_in'], list) and
                isinstance(flattened['just_out'], list)):
                min_just_in = min(list(map(int, flattened['just_in'])))
                max_just_out = max(list(map(int, flattened['just_out'])))
                flattened['just_in'] = min_just_in
                flattened['just_out'] = max_just_out
                
            # if the data is a list,
            # Get the min timecode in, max timecode out
            if (isinstance(flattened['timecode_in'], list) and
                isinstance(flattened['timecode_out'], list)):
                # set timecode to int for comparison
                tc_in_list = []
                tc_out_list = []
                for timecode in flattened['timecode_in']:
                    tc_in_list.append(int(timecode.replace(":", "")))
                for timecode in flattened['timecode_out']:
                    tc_out_list.append(int(timecode.replace(":", "")))
                    
                # restore int timecode to string
                tc_in = str(min(tc_in_list)).zfill(8)
                tc_out = str(max(tc_out_list)).zfill(8)
                timecode_in = f"{tc_in[0:2]}:{tc_in[2:4]}:{tc_in[4:6]}:{tc_in[6:]}"
                timecode_out = f"{tc_out[0:2]}:{tc_out[2:4]}:{tc_out[4:6]}:{tc_out[6:]}"
                flattened['timecode_in'] = timecode_in
                flattened['timecode_out'] = timecode_out
            
            final_data.append(flattened)
        
        return final_data
    
    def publish_to_shotgrid(self) -> None:
        """
        Publish the data to ShotGrid.
        """
        # publish data
        if not self.grouped_data:
            logger.error("No data to publish")
            QtGui.QMessageBox.critical(
                self, 
                "Error", 
                "No data to publish."
                )
            return
        self._publish = Publish(self.grouped_data, self.colorspace)
        self._publish.publish_to_shotgrid()
            
    def closeEvent(self, event):
        """
        When the dialog is closed, this method is called.
        clenup temp directory and close the dialog.
        """
        logger.info("Closing IO Manager")
        
        if not os.path.exists(self._temp_images):
            logger.debug("Temp directory not found: %s" % self._temp_images)
        else:
            shutil.rmtree(self._temp_images)
            logger.debug("Temp directory removed: %s" % self._temp_images)
            
        logger.info("IO Manager closed")
        event.accept()
        