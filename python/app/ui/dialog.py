# -*- coding: utf-8 -*-

__author__ = "Juno Park"
__github__ = "https://github.com/junopark00"

from sgtk.platform.qt import QtCore, QtGui
from ..constants import COLORSPACE


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1300, 800)
        self.main_layout = QtGui.QVBoxLayout(Dialog)
        
        self.horizontal_layout_1 = QtGui.QHBoxLayout()
        
        self.label_path = QtGui.QLabel(Dialog)
        self.label_path.setText("Excel Path:")
        self.label_path.setFocusPolicy(QtCore.Qt.NoFocus)
        self.horizontal_layout_1.addWidget(self.label_path)
        
        self.line_edit_path = QtGui.QLineEdit(Dialog)
        self.line_edit_path.setFocusPolicy(QtCore.Qt.NoFocus)
        self.horizontal_layout_1.addWidget(self.line_edit_path)
        
        self.button_select_path = QtGui.QPushButton(Dialog)
        self.button_select_path.setText("Select")
        self.button_select_path.setFocusPolicy(QtCore.Qt.NoFocus)
        self.horizontal_layout_1.addWidget(self.button_select_path)
        
        self.button_load_path = QtGui.QPushButton(Dialog)
        self.button_load_path.setText("Load")
        self.button_load_path.setFocusPolicy(QtCore.Qt.NoFocus)
        self.horizontal_layout_1.addWidget(self.button_load_path)
        
        self.main_layout.addLayout(self.horizontal_layout_1)
        
        self.horizontal_layout_2 = QtGui.QHBoxLayout()
        
        self.button_check_all = QtGui.QPushButton(Dialog)
        self.button_check_all.setText("Check All")
        self.button_check_all.setFocusPolicy(QtCore.Qt.NoFocus)
        self.horizontal_layout_2.addWidget(self.button_check_all)
        
        self.button_uncheck_all = QtGui.QPushButton(Dialog)
        self.button_uncheck_all.setText("Uncheck All")
        self.button_uncheck_all.setFocusPolicy(QtCore.Qt.NoFocus)
        self.horizontal_layout_2.addWidget(self.button_uncheck_all)
        
        self._spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontal_layout_2.addItem(self._spacer)
        
        self.checkbox_mov_to_dpx = QtGui.QCheckBox(Dialog)
        self.checkbox_mov_to_dpx.setText("MOV to DPX")
        self.checkbox_mov_to_dpx.setFocusPolicy(QtCore.Qt.NoFocus)
        self.horizontal_layout_2.addWidget(self.checkbox_mov_to_dpx)
        
        self.checkbox_cliplib = QtGui.QCheckBox(Dialog)
        self.checkbox_cliplib.setText("ClipLib")
        self.checkbox_cliplib.setFocusPolicy(QtCore.Qt.NoFocus)
        self.horizontal_layout_2.addWidget(self.checkbox_cliplib)
        
        self.label_colorspace = QtGui.QLabel(Dialog)
        self.label_colorspace.setText("ColorSpace")
        self.label_colorspace.setFocusPolicy(QtCore.Qt.NoFocus)
        self.horizontal_layout_2.addWidget(self.label_colorspace)
        
        self.comboBox_colorspace = QtGui.QComboBox(Dialog)
        self.comboBox_items = COLORSPACE.keys()
        self.comboBox_colorspace.addItems(self.comboBox_items)
        self.comboBox_colorspace.setFocusPolicy(QtCore.Qt.NoFocus)
        self.horizontal_layout_2.addWidget(self.comboBox_colorspace)
        
        self.main_layout.addLayout(self.horizontal_layout_2)
        
        self.table_widget = QtGui.QTableWidget(Dialog)
        
        self.main_layout.addWidget(self.table_widget)
        
        self.horizontal_layout_3 = QtGui.QHBoxLayout()
        
        self.label_excel_path = QtGui.QLabel(Dialog)
        self.label_excel_path.setText("/Path/To/Excel/File.xls")
        self.label_excel_path.setFocusPolicy(QtCore.Qt.NoFocus)
        self.horizontal_layout_3.addWidget(self.label_excel_path)
        
        self.buttons_layout = QtGui.QGridLayout()
        
        # Excel
        self.frame_excel = QtGui.QFrame(Dialog)
        self.frame_excel_layout = QtGui.QHBoxLayout()
        self.frame_excel_layout.setSpacing(3)
        self.frame_excel.setLayout(self.frame_excel_layout)
        self.frame_excel.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_excel.setFrameShadow(QtGui.QFrame.Raised)
        
        self.frame_excel_title = QtGui.QLabel(Dialog)
        self.frame_excel_title.setText("Excel")
        self.frame_excel_layout.addWidget(self.frame_excel_title)
        
        self.button_excel_save = QtGui.QPushButton(Dialog)
        self.button_excel_save.setText("Save")
        self.button_excel_save.setFocusPolicy(QtCore.Qt.NoFocus)
        self.frame_excel_layout.addWidget(self.button_excel_save)
        
        self.button_excel_edit = QtGui.QPushButton(Dialog)
        self.button_excel_edit.setText("Edit")
        self.button_excel_edit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.frame_excel_layout.addWidget(self.button_excel_edit)
        
        self.buttons_layout.addWidget(self.frame_excel_title, 0, 0)
        self.buttons_layout.addWidget(self.frame_excel, 1, 0)
        
        # Validate
        self.frame_validate = QtGui.QFrame(Dialog)
        self.frame_validate_layout = QtGui.QGridLayout()
        self.frame_validate_layout.setSpacing(3)
        self.frame_validate.setLayout(self.frame_validate_layout)
        self.frame_validate.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_validate.setFrameShadow(QtGui.QFrame.Raised)
        
        self.frame_validate_title = QtGui.QLabel(Dialog)
        self.frame_validate_title.setText("Validate")
        self.frame_validate_layout.addWidget(self.frame_validate_title, 0, 0)

        self.button_validate_timecode = QtGui.QPushButton(Dialog)
        self.button_validate_timecode.setText("Timecode")
        self.button_validate_timecode.setFocusPolicy(QtCore.Qt.NoFocus)
        self.frame_validate_layout.addWidget(self.button_validate_timecode, 0, 0)
        
        self.button_validate_version = QtGui.QPushButton(Dialog)
        self.button_validate_version.setText("Version")
        self.button_validate_version.setFocusPolicy(QtCore.Qt.NoFocus)
        self.frame_validate_layout.addWidget(self.button_validate_version, 0, 1)
        
        self.button_validate_src_version = QtGui.QPushButton(Dialog)
        self.button_validate_src_version.setText("Src Version")
        self.button_validate_src_version.setFocusPolicy(QtCore.Qt.NoFocus)
        self.frame_validate_layout.addWidget(self.button_validate_src_version, 1, 0)
        
        self.button_validate_shot_for_editorial = QtGui.QPushButton(Dialog)
        self.button_validate_shot_for_editorial.setText("Shot for Editorial")
        self.button_validate_shot_for_editorial.setFocusPolicy(QtCore.Qt.NoFocus)
        self.frame_validate_layout.addWidget(self.button_validate_shot_for_editorial, 1, 1)
        
        self.buttons_layout.addWidget(self.frame_validate_title, 0, 1)
        self.buttons_layout.addWidget(self.frame_validate, 1, 1)
        
        # Action
        self.frame_action = QtGui.QFrame(Dialog)
        self.frame_action_layout = QtGui.QHBoxLayout()
        self.frame_action_layout.setSpacing(3)
        self.frame_action.setLayout(self.frame_action_layout)
        self.frame_action.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_action.setFrameShadow(QtGui.QFrame.Raised)
        
        self.frame_action_title = QtGui.QLabel(Dialog)
        self.frame_action_title.setText("Action")
        self.frame_action_layout.addWidget(self.frame_action_title)
        
        self.button_collect = QtGui.QPushButton(Dialog)
        self.button_collect.setText("Collect")
        self.button_collect.setFocusPolicy(QtCore.Qt.NoFocus)
        self.frame_action_layout.addWidget(self.button_collect)
        
        self.button_publish = QtGui.QPushButton(Dialog)
        self.button_publish.setText("Publish")
        self.button_publish.setFocusPolicy(QtCore.Qt.NoFocus)
        self.frame_action_layout.addWidget(self.button_publish)
        
        self.buttons_layout.addWidget(self.frame_action_title, 0, 2)
        self.buttons_layout.addWidget(self.frame_action, 1, 2)
        
        self.horizontal_layout_3.addLayout(self.buttons_layout)
        
        self.main_layout.addLayout(self.horizontal_layout_3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "The Current Sgtk Environment", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
