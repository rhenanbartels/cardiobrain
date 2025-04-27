# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interface.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QRadioButton,
    QSizePolicy, QTabWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

from pyqtgraph import PlotWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1500, 1000)
        MainWindow.setMinimumSize(QSize(1500, 1000))
        font = QFont()
        font.setPointSize(12)
        font.setBold(False)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet(u"QMainWindow {\n"
"    background-color: black;\n"
"}\n"
"\n"
"\n"
"QLabel {\n"
"	color: rgb(152, 152, 152);\n"
"}\n"
"\n"
"QMenuBar {\n"
"    background-color: black;\n"
"}\n"
"\n"
"QTabWidget {\n"
"    background-color: black;\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"	background-color: rgb(20, 20, 20);\n"
"    color: rgb(152, 152, 152);\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QMenuBar::item {\n"
"	background-color: black;\n"
"    color: rgb(152, 152, 152);\n"
"    font-weight: bold;\n"
"    font-size: 120px;\n"
"}\n"
"\n"
"\n"
"QTableWidget::item {\n"
"    background-color: black;   /* Cor de fundo dos itens (c\u00e9lulas) */\n"
"    color: rgb(152, 152, 152);              /* Cor do texto das c\u00e9lulas */\n"
"}\n"
"QHeaderView::section {\n"
"    background-color: black;   /* Cor de fundo do cabe\u00e7alho */\n"
"    color: white;              /* Cor do texto do cabe\u00e7alho */\n"
"}\n"
"")
        self.menu_file_open_action = QAction(MainWindow)
        self.menu_file_open_action.setObjectName(u"menu_file_open_action")
        self.menu_save_results_action = QAction(MainWindow)
        self.menu_save_results_action.setObjectName(u"menu_save_results_action")
        self.menu_save_results_action.setEnabled(False)
        self.menu_analysis_method_frequency_band = QAction(MainWindow)
        self.menu_analysis_method_frequency_band.setObjectName(u"menu_analysis_method_frequency_band")
        self.menu_analysis_method_frequency_band.setCheckable(True)
        self.menu_analysis_method_point_estimate = QAction(MainWindow)
        self.menu_analysis_method_point_estimate.setObjectName(u"menu_analysis_method_point_estimate")
        self.menu_analysis_method_point_estimate.setCheckable(True)
        self.menu_analysis_method_ask_on_new_file = QAction(MainWindow)
        self.menu_analysis_method_ask_on_new_file.setObjectName(u"menu_analysis_method_ask_on_new_file")
        self.menu_analysis_method_ask_on_new_file.setCheckable(True)
        self.menu_analysis_method_ask_on_new_file.setChecked(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(350, 0))
        self.frame.setMaximumSize(QSize(300, 16777215))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.frame_6 = QFrame(self.frame)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMaximumSize(QSize(16777215, 60))
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.frame_6)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        self.label.setFont(font1)

        self.horizontalLayout_2.addWidget(self.label)

        self.lineEditFileName = QLineEdit(self.frame_6)
        self.lineEditFileName.setObjectName(u"lineEditFileName")
        self.lineEditFileName.setEnabled(False)
        self.lineEditFileName.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.lineEditFileName)


        self.gridLayout_5.addWidget(self.frame_6, 0, 0, 1, 1)

        self.frame_10 = QFrame(self.frame)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setMinimumSize(QSize(0, 140))
        self.frame_10.setMaximumSize(QSize(16777215, 140))
        self.frame_10.setFrameShape(QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_10)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_21 = QLabel(self.frame_10)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setFont(font1)

        self.gridLayout_6.addWidget(self.label_21, 1, 0, 1, 1)

        self.label_14 = QLabel(self.frame_10)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(180, 0))
        self.label_14.setMaximumSize(QSize(170, 16777215))
        self.label_14.setFont(font1)

        self.gridLayout_6.addWidget(self.label_14, 0, 0, 1, 1)

        self.radioButtonSimulatedCoherence = QRadioButton(self.frame_10)
        self.radioButtonSimulatedCoherence.setObjectName(u"radioButtonSimulatedCoherence")
        self.radioButtonSimulatedCoherence.setMaximumSize(QSize(40, 16777215))
        self.radioButtonSimulatedCoherence.setStyleSheet(u"#radioButtonSimulatedCoherence {\n"
"	margin-top: 15px;\n"
"   padding-left:12px;\n"
"  margin-bottom:12px;\n"
"}\n"
"")
        self.radioButtonSimulatedCoherence.setChecked(True)
        self.radioButtonSimulatedCoherence.setAutoExclusive(False)

        self.gridLayout_6.addWidget(self.radioButtonSimulatedCoherence, 1, 1, 1, 1)

        self.coherenceThreshold = QLineEdit(self.frame_10)
        self.coherenceThreshold.setObjectName(u"coherenceThreshold")
        self.coherenceThreshold.setEnabled(False)
        self.coherenceThreshold.setMinimumSize(QSize(40, 30))
        self.coherenceThreshold.setMaximumSize(QSize(40, 30))
        self.coherenceThreshold.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.coherenceThreshold, 0, 1, 1, 1)

        self.label_15 = QLabel(self.frame_10)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMaximumSize(QSize(16777215, 120))
        self.label_15.setFont(font1)
        self.label_15.setStyleSheet(u"#label_15{\n"
"	margin-top:10px\n"
"}")

        self.gridLayout_6.addWidget(self.label_15, 2, 0, 1, 1)

        self.radioButtonApplyCoherence = QRadioButton(self.frame_10)
        self.radioButtonApplyCoherence.setObjectName(u"radioButtonApplyCoherence")
        self.radioButtonApplyCoherence.setMaximumSize(QSize(40, 16777215))
        self.radioButtonApplyCoherence.setStyleSheet(u"#radioButtonApplyCoherence {\n"
"	margin-top: 15px;\n"
"   padding-left:12px;\n"
"  margin-bottom:2px;\n"
"}")
        self.radioButtonApplyCoherence.setChecked(True)
        self.radioButtonApplyCoherence.setAutoExclusive(False)

        self.gridLayout_6.addWidget(self.radioButtonApplyCoherence, 2, 1, 1, 1)


        self.gridLayout_5.addWidget(self.frame_10, 3, 0, 1, 1)

        self.frame_9 = QFrame(self.frame)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setMinimumSize(QSize(0, 40))
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.statusColor = QLineEdit(self.frame_9)
        self.statusColor.setObjectName(u"statusColor")
        self.statusColor.setEnabled(False)
        self.statusColor.setMaximumSize(QSize(14, 14))
        self.statusColor.setStyleSheet(u"#statusColor {\n"
"	background-color: rgb(0,255,0); \n"
"	color: rgb(0,255,0);\n"
"	border-radius: 4px\n"
"}")

        self.horizontalLayout_3.addWidget(self.statusColor)

        self.statusLabel = QLabel(self.frame_9)
        self.statusLabel.setObjectName(u"statusLabel")
        self.statusLabel.setMinimumSize(QSize(0, 14))
        self.statusLabel.setMaximumSize(QSize(300, 15))

        self.horizontalLayout_3.addWidget(self.statusLabel)


        self.gridLayout_5.addWidget(self.frame_9, 6, 0, 1, 1)

        self.frame_7 = QFrame(self.frame)
        self.frame_7.setObjectName(u"frame_7")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_7.sizePolicy().hasHeightForWidth())
        self.frame_7.setSizePolicy(sizePolicy)
        self.frame_7.setMinimumSize(QSize(0, 250))
        self.frame_7.setMaximumSize(QSize(16777215, 250))
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_7)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(self.frame_7)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(16777215, 120))
        self.label_2.setFont(font1)

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.windowComboBox = QComboBox(self.frame_7)
        self.windowComboBox.addItem("")
        self.windowComboBox.addItem("")
        self.windowComboBox.addItem("")
        self.windowComboBox.setObjectName(u"windowComboBox")
        self.windowComboBox.setMinimumSize(QSize(116, 30))

        self.gridLayout.addWidget(self.windowComboBox, 4, 1, 1, 1)

        self.label_3 = QLabel(self.frame_7)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(181, 0))
        self.label_3.setMaximumSize(QSize(160, 16777215))
        self.label_3.setFont(font1)

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.resamplingFrequency = QLineEdit(self.frame_7)
        self.resamplingFrequency.setObjectName(u"resamplingFrequency")
        self.resamplingFrequency.setMaximumSize(QSize(40, 30))
        self.resamplingFrequency.setLayoutDirection(Qt.LeftToRight)
        self.resamplingFrequency.setStyleSheet(u"#resamplingFrequency{\n"
"  background-color:grey;\n"
"}")
        self.resamplingFrequency.setAlignment(Qt.AlignCenter)
        self.resamplingFrequency.setReadOnly(True)

        self.gridLayout.addWidget(self.resamplingFrequency, 1, 1, 1, 1)

        self.label_20 = QLabel(self.frame_7)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFont(font1)

        self.gridLayout.addWidget(self.label_20, 3, 0, 1, 1)

        self.label_5 = QLabel(self.frame_7)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(16777215, 120))
        self.label_5.setFont(font1)

        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)

        self.label_11 = QLabel(self.frame_7)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font1)

        self.gridLayout.addWidget(self.label_11, 2, 0, 1, 1)

        self.label_24 = QLabel(self.frame_7)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setFont(font1)

        self.gridLayout.addWidget(self.label_24, 5, 0, 1, 1)

        self.interpMethodComboBox = QComboBox(self.frame_7)
        self.interpMethodComboBox.addItem("")
        self.interpMethodComboBox.addItem("")
        self.interpMethodComboBox.addItem("")
        self.interpMethodComboBox.setObjectName(u"interpMethodComboBox")
        self.interpMethodComboBox.setMinimumSize(QSize(116, 30))

        self.gridLayout.addWidget(self.interpMethodComboBox, 0, 1, 1, 1)

        self.radioButtonSmoothPSD = QRadioButton(self.frame_7)
        self.radioButtonSmoothPSD.setObjectName(u"radioButtonSmoothPSD")
        self.radioButtonSmoothPSD.setMaximumSize(QSize(40, 30))
        font2 = QFont()
        font2.setPointSize(11)
        self.radioButtonSmoothPSD.setFont(font2)
        self.radioButtonSmoothPSD.setStyleSheet(u"#radioButtonSmoothPSD{\n"
"	margin-top: 15px;\n"
"   padding-left:12px;\n"
"  margin-bottom:12px;\n"
"}\n"
"")

        self.gridLayout.addWidget(self.radioButtonSmoothPSD, 5, 1, 1, 1)

        self.overlapSize = QLineEdit(self.frame_7)
        self.overlapSize.setObjectName(u"overlapSize")
        self.overlapSize.setMinimumSize(QSize(61, 0))
        self.overlapSize.setMaximumSize(QSize(40, 30))
        self.overlapSize.setLayoutDirection(Qt.LeftToRight)
        self.overlapSize.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.overlapSize, 3, 1, 1, 1)

        self.segmentSize = QLineEdit(self.frame_7)
        self.segmentSize.setObjectName(u"segmentSize")
        self.segmentSize.setMinimumSize(QSize(61, 0))
        self.segmentSize.setMaximumSize(QSize(40, 30))
        self.segmentSize.setLayoutDirection(Qt.LeftToRight)
        self.segmentSize.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.segmentSize, 2, 1, 1, 1)


        self.gridLayout_5.addWidget(self.frame_7, 1, 0, 1, 1)

        self.frame_12 = QFrame(self.frame)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setMinimumSize(QSize(0, 50))
        self.frame_12.setFrameShape(QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_12)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.lineEditShiftCBFV = QLineEdit(self.frame_12)
        self.lineEditShiftCBFV.setObjectName(u"lineEditShiftCBFV")
        self.lineEditShiftCBFV.setMaximumSize(QSize(40, 30))
        self.lineEditShiftCBFV.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEditShiftCBFV, 0, 2, 1, 1)

        self.label_22 = QLabel(self.frame_12)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setMinimumSize(QSize(20, 0))
        self.label_22.setMaximumSize(QSize(120, 16777215))
        self.label_22.setFont(font1)
        self.label_22.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_22, 0, 1, 1, 1)


        self.gridLayout_5.addWidget(self.frame_12, 5, 0, 1, 1)

        self.frame_11 = QFrame(self.frame)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setMinimumSize(QSize(0, 230))
        self.frame_11.setFrameShape(QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_11)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_16 = QLabel(self.frame_11)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(180, 0))
        self.label_16.setMaximumSize(QSize(170, 16777215))
        self.label_16.setFont(font1)

        self.gridLayout_4.addWidget(self.label_16, 0, 0, 1, 1)

        self.lineEditEndTimeAxes = QLineEdit(self.frame_11)
        self.lineEditEndTimeAxes.setObjectName(u"lineEditEndTimeAxes")
        self.lineEditEndTimeAxes.setMinimumSize(QSize(70, 0))
        self.lineEditEndTimeAxes.setMaximumSize(QSize(50, 30))
        self.lineEditEndTimeAxes.setLayoutDirection(Qt.LeftToRight)
        self.lineEditEndTimeAxes.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEditEndTimeAxes, 3, 4, 1, 1)

        self.lineEditStartTimeAxes = QLineEdit(self.frame_11)
        self.lineEditStartTimeAxes.setObjectName(u"lineEditStartTimeAxes")
        self.lineEditStartTimeAxes.setMinimumSize(QSize(70, 0))
        self.lineEditStartTimeAxes.setMaximumSize(QSize(50, 30))
        self.lineEditStartTimeAxes.setLayoutDirection(Qt.LeftToRight)
        self.lineEditStartTimeAxes.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEditStartTimeAxes, 3, 2, 1, 1)

        self.label_19 = QLabel(self.frame_11)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMaximumSize(QSize(62, 16777215))

        self.gridLayout_4.addWidget(self.label_19, 3, 0, 1, 1)

        self.label_18 = QLabel(self.frame_11)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(10, 0))
        self.label_18.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.label_18, 3, 3, 1, 1)

        self.label_17 = QLabel(self.frame_11)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(123, 0))
        self.label_17.setMaximumSize(QSize(170, 16777210))
        self.label_17.setFont(font1)

        self.gridLayout_4.addWidget(self.label_17, 1, 0, 1, 1)

        self.bottomAxesComboBox = QComboBox(self.frame_11)
        self.bottomAxesComboBox.addItem("")
        self.bottomAxesComboBox.addItem("")
        self.bottomAxesComboBox.addItem("")
        self.bottomAxesComboBox.addItem("")
        self.bottomAxesComboBox.addItem("")
        self.bottomAxesComboBox.addItem("")
        self.bottomAxesComboBox.setObjectName(u"bottomAxesComboBox")
        self.bottomAxesComboBox.setMinimumSize(QSize(116, 30))
        self.bottomAxesComboBox.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_4.addWidget(self.bottomAxesComboBox, 1, 2, 1, 3)

        self.topAxesComboBox = QComboBox(self.frame_11)
        self.topAxesComboBox.addItem("")
        self.topAxesComboBox.addItem("")
        self.topAxesComboBox.addItem("")
        self.topAxesComboBox.addItem("")
        self.topAxesComboBox.addItem("")
        self.topAxesComboBox.addItem("")
        self.topAxesComboBox.setObjectName(u"topAxesComboBox")
        self.topAxesComboBox.setMinimumSize(QSize(116, 30))
        self.topAxesComboBox.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_4.addWidget(self.topAxesComboBox, 0, 2, 1, 3)

        self.label_13 = QLabel(self.frame_11)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(180, 0))
        self.label_13.setMaximumSize(QSize(130, 16777215))
        self.label_13.setFont(font1)

        self.gridLayout_4.addWidget(self.label_13, 2, 0, 1, 1)

        self.radioButtonShowMarkers = QRadioButton(self.frame_11)
        self.radioButtonShowMarkers.setObjectName(u"radioButtonShowMarkers")
        self.radioButtonShowMarkers.setMaximumSize(QSize(40, 16777215))

        self.gridLayout_4.addWidget(self.radioButtonShowMarkers, 2, 3, 1, 1)


        self.gridLayout_5.addWidget(self.frame_11, 4, 0, 1, 1)

        self.tabAnalysisMethod = QTabWidget(self.frame)
        self.tabAnalysisMethod.setObjectName(u"tabAnalysisMethod")
        self.tabFrequencyBand = QWidget()
        self.tabFrequencyBand.setObjectName(u"tabFrequencyBand")
        self.tabFrequencyBand.setStyleSheet(u"tabFrequencyBand {\n"
"	background-color: black;\n"
"}")
        self.horizontalLayout_4 = QHBoxLayout(self.tabFrequencyBand)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.frame_8 = QFrame(self.tabFrequencyBand)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(300, 120))
        self.frame_8.setMaximumSize(QSize(180, 120))
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_8)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_6 = QLabel(self.frame_8)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMaximumSize(QSize(80, 120))
        self.label_6.setFont(font1)

        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 1)

        self.label_10 = QLabel(self.frame_8)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_2.addWidget(self.label_10, 2, 3, 1, 1)

        self.label_7 = QLabel(self.frame_8)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(16777215, 120))
        self.label_7.setFont(font1)

        self.gridLayout_2.addWidget(self.label_7, 2, 0, 1, 1)

        self.label_9 = QLabel(self.frame_8)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMaximumSize(QSize(10, 16777215))

        self.gridLayout_2.addWidget(self.label_9, 0, 3, 1, 1)

        self.lineEditLFUpper = QLineEdit(self.frame_8)
        self.lineEditLFUpper.setObjectName(u"lineEditLFUpper")
        self.lineEditLFUpper.setMaximumSize(QSize(40, 30))
        self.lineEditLFUpper.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEditLFUpper, 2, 4, 1, 1)

        self.lineEditHFLower = QLineEdit(self.frame_8)
        self.lineEditHFLower.setObjectName(u"lineEditHFLower")
        self.lineEditHFLower.setMaximumSize(QSize(40, 30))
        self.lineEditHFLower.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEditHFLower, 3, 2, 1, 1)

        self.lineEditHFUpper = QLineEdit(self.frame_8)
        self.lineEditHFUpper.setObjectName(u"lineEditHFUpper")
        self.lineEditHFUpper.setMaximumSize(QSize(40, 30))
        self.lineEditHFUpper.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEditHFUpper, 3, 4, 1, 1)

        self.label_12 = QLabel(self.frame_8)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_2.addWidget(self.label_12, 3, 3, 1, 1)

        self.lineEditVLFUpper = QLineEdit(self.frame_8)
        self.lineEditVLFUpper.setObjectName(u"lineEditVLFUpper")
        self.lineEditVLFUpper.setMaximumSize(QSize(40, 30))
        self.lineEditVLFUpper.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEditVLFUpper, 0, 4, 1, 1)

        self.label_8 = QLabel(self.frame_8)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMaximumSize(QSize(16777215, 120))
        self.label_8.setFont(font1)

        self.gridLayout_2.addWidget(self.label_8, 3, 0, 1, 1)

        self.lineEditVLFLower = QLineEdit(self.frame_8)
        self.lineEditVLFLower.setObjectName(u"lineEditVLFLower")
        self.lineEditVLFLower.setMaximumSize(QSize(40, 30))
        self.lineEditVLFLower.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEditVLFLower, 0, 2, 1, 1)

        self.lineEditLFLower = QLineEdit(self.frame_8)
        self.lineEditLFLower.setObjectName(u"lineEditLFLower")
        self.lineEditLFLower.setMaximumSize(QSize(40, 30))
        self.lineEditLFLower.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEditLFLower, 2, 2, 1, 1)

        self.lineEditHFLower.raise_()
        self.label_9.raise_()
        self.label_7.raise_()
        self.label_8.raise_()
        self.label_10.raise_()
        self.lineEditLFLower.raise_()
        self.lineEditVLFUpper.raise_()
        self.lineEditLFUpper.raise_()
        self.label_12.raise_()
        self.lineEditVLFLower.raise_()
        self.label_6.raise_()
        self.lineEditHFUpper.raise_()

        self.horizontalLayout_4.addWidget(self.frame_8)

        self.tabAnalysisMethod.addTab(self.tabFrequencyBand, "")
        self.tabPointEstimate = QWidget()
        self.tabPointEstimate.setObjectName(u"tabPointEstimate")
        self.tabPointEstimate.setStyleSheet(u"tabPointEstimate{\n"
"	background-color: black;\n"
"}")
        self.horizontalLayout = QHBoxLayout(self.tabPointEstimate)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame_13 = QFrame(self.tabPointEstimate)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setMinimumSize(QSize(300, 120))
        self.frame_13.setMaximumSize(QSize(180, 120))
        self.frame_13.setFrameShape(QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_13)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_23 = QLabel(self.frame_13)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setMaximumSize(QSize(199, 16777215))
        self.label_23.setFont(font1)

        self.horizontalLayout_5.addWidget(self.label_23)

        self.lineEditPointEstimateFrequency = QLineEdit(self.frame_13)
        self.lineEditPointEstimateFrequency.setObjectName(u"lineEditPointEstimateFrequency")
        self.lineEditPointEstimateFrequency.setMinimumSize(QSize(0, 30))
        self.lineEditPointEstimateFrequency.setMaximumSize(QSize(50, 16777215))
        font3 = QFont()
        font3.setBold(False)
        self.lineEditPointEstimateFrequency.setFont(font3)
        self.lineEditPointEstimateFrequency.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.lineEditPointEstimateFrequency)


        self.horizontalLayout.addWidget(self.frame_13)

        self.tabAnalysisMethod.addTab(self.tabPointEstimate, "")

        self.gridLayout_5.addWidget(self.tabAnalysisMethod, 2, 0, 1, 1)

        self.tabAnalysisMethod.raise_()
        self.frame_10.raise_()
        self.frame_7.raise_()
        self.frame_6.raise_()
        self.frame_11.raise_()
        self.frame_9.raise_()
        self.frame_12.raise_()

        self.gridLayout_3.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_2)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_3)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.top_axes = PlotWidget(self.frame_3)
        self.top_axes.setObjectName(u"top_axes")

        self.verticalLayout_5.addWidget(self.top_axes)


        self.verticalLayout.addWidget(self.frame_3)

        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_4)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.bottom_axes = PlotWidget(self.frame_4)
        self.bottom_axes.setObjectName(u"bottom_axes")

        self.verticalLayout_4.addWidget(self.bottom_axes)


        self.verticalLayout.addWidget(self.frame_4)

        self.frame_5 = QFrame(self.frame_2)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(0, 150))
        self.frame_5.setMaximumSize(QSize(16777215, 200))
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.resultsTable = QTableWidget(self.frame_5)
        self.resultsTable.setObjectName(u"resultsTable")
        self.resultsTable.setStyleSheet(u"background-color: rgb(0, 0, 0);")

        self.verticalLayout_3.addWidget(self.resultsTable)


        self.verticalLayout.addWidget(self.frame_5)


        self.gridLayout_3.addWidget(self.frame_2, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1500, 19))
        self.menubar.setFocusPolicy(Qt.WheelFocus)
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuSettings = QMenu(self.menuFile)
        self.menuSettings.setObjectName(u"menuSettings")
        self.menu_analysis_method = QMenu(self.menuSettings)
        self.menu_analysis_method.setObjectName(u"menu_analysis_method")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.menu_file_open_action)
        self.menuFile.addAction(self.menuSettings.menuAction())
        self.menuFile.addAction(self.menu_save_results_action)
        self.menuSettings.addAction(self.menu_analysis_method.menuAction())
        self.menu_analysis_method.addAction(self.menu_analysis_method_frequency_band)
        self.menu_analysis_method.addAction(self.menu_analysis_method_point_estimate)
        self.menu_analysis_method.addAction(self.menu_analysis_method_ask_on_new_file)

        self.retranslateUi(MainWindow)

        self.tabAnalysisMethod.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"CardioBrain 1.1.0", None))
        self.menu_file_open_action.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.menu_save_results_action.setText(QCoreApplication.translate("MainWindow", u"Save Results", None))
        self.menu_analysis_method_frequency_band.setText(QCoreApplication.translate("MainWindow", u"Frequency Band", None))
        self.menu_analysis_method_point_estimate.setText(QCoreApplication.translate("MainWindow", u"Point Estimate", None))
        self.menu_analysis_method_ask_on_new_file.setText(QCoreApplication.translate("MainWindow", u"Ask on new File", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Filename:", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Simulated Threshold:", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Coherence Threshold:", None))
        self.radioButtonSimulatedCoherence.setText("")
        self.coherenceThreshold.setInputMask(QCoreApplication.translate("MainWindow", u"0.00", None))
        self.coherenceThreshold.setText(QCoreApplication.translate("MainWindow", u"0.5", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Apply threshold:", None))
        self.radioButtonApplyCoherence.setText("")
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"Ready", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Interp. Method:", None))
        self.windowComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Hanning", None))
        self.windowComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Hamming", None))
        self.windowComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Rectangular", None))

        self.label_3.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Resampling Freq. <span style=\" vertical-align:sub;\">(Hz)</span>:</p></body></html>", None))
        self.resamplingFrequency.setInputMask(QCoreApplication.translate("MainWindow", u"00", None))
        self.resamplingFrequency.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Overlap Size <span style=\" vertical-align:sub;\">(n)</span>:</p></body></html>", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Window:", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Segment Size <span style=\" vertical-align:sub;\">(n)</span>:</p></body></html>", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"Smooth PSD:", None))
        self.interpMethodComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))
        self.interpMethodComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Linear", None))
        self.interpMethodComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Cubic spline", None))

        self.radioButtonSmoothPSD.setText("")
        self.overlapSize.setInputMask("")
        self.overlapSize.setText(QCoreApplication.translate("MainWindow", u"512", None))
        self.segmentSize.setInputMask("")
        self.segmentSize.setText(QCoreApplication.translate("MainWindow", u"1024", None))
        self.lineEditShiftCBFV.setInputMask("")
        self.lineEditShiftCBFV.setText("")
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Shift CBFV<span style=\" vertical-align:sub;\">(s)</span>:</p></body></html>", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Top Panel:", None))
        self.lineEditEndTimeAxes.setInputMask(QCoreApplication.translate("MainWindow", u"00000.00", None))
        self.lineEditEndTimeAxes.setText(QCoreApplication.translate("MainWindow", u".", None))
        self.lineEditStartTimeAxes.setInputMask(QCoreApplication.translate("MainWindow", u"00000.00", None))
        self.lineEditStartTimeAxes.setText(QCoreApplication.translate("MainWindow", u".", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">Time </span><span style=\" font-weight:700; vertical-align:sub;\">(s)</span><span style=\" font-weight:700;\">:</span></p></body></html>", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Bottom Panel:", None))
        self.bottomAxesComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"CBFV - Signal", None))
        self.bottomAxesComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"CBFV - PSD", None))
        self.bottomAxesComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Gain", None))
        self.bottomAxesComboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"Coherence", None))
        self.bottomAxesComboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"Phase", None))
        self.bottomAxesComboBox.setItemText(5, QCoreApplication.translate("MainWindow", u"ABP x CBFV", None))

        self.topAxesComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"ABP - Signal", None))
        self.topAxesComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"ABP - PSD", None))
        self.topAxesComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Gain", None))
        self.topAxesComboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"Coherence", None))
        self.topAxesComboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"Phase", None))
        self.topAxesComboBox.setItemText(5, QCoreApplication.translate("MainWindow", u"ABP x CBFV", None))

        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Show Markers:", None))
        self.radioButtonShowMarkers.setText("")
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">VLF</span><span style=\" font-weight:700; vertical-align:sub;\"> (Hz)</span></p></body></html>", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">LF </span><span style=\" font-weight:700; vertical-align:sub;\">(Hz)</span></p></body></html>", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.lineEditLFUpper.setInputMask(QCoreApplication.translate("MainWindow", u"0.00", None))
        self.lineEditLFUpper.setText(QCoreApplication.translate("MainWindow", u"0.2", None))
        self.lineEditHFLower.setInputMask(QCoreApplication.translate("MainWindow", u"0.00", None))
        self.lineEditHFLower.setText(QCoreApplication.translate("MainWindow", u"0.2", None))
        self.lineEditHFUpper.setInputMask(QCoreApplication.translate("MainWindow", u"0.00", None))
        self.lineEditHFUpper.setText(QCoreApplication.translate("MainWindow", u"0.5", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.lineEditVLFUpper.setInputMask(QCoreApplication.translate("MainWindow", u"0.00", None))
        self.lineEditVLFUpper.setText(QCoreApplication.translate("MainWindow", u"0.07", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>HF <span style=\" vertical-align:sub;\">(Hz)</span></p></body></html>", None))
        self.lineEditVLFLower.setInputMask(QCoreApplication.translate("MainWindow", u"0.00", None))
        self.lineEditVLFLower.setText(QCoreApplication.translate("MainWindow", u"0.02", None))
        self.lineEditLFLower.setInputMask(QCoreApplication.translate("MainWindow", u"0.00", None))
        self.lineEditLFLower.setText(QCoreApplication.translate("MainWindow", u"0.07", None))
        self.tabAnalysisMethod.setTabText(self.tabAnalysisMethod.indexOf(self.tabFrequencyBand), QCoreApplication.translate("MainWindow", u"Frequency band", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"Point Frequency (Hz):", None))
        self.lineEditPointEstimateFrequency.setInputMask(QCoreApplication.translate("MainWindow", u"0.000", None))
        self.lineEditPointEstimateFrequency.setText(QCoreApplication.translate("MainWindow", u"0.100", None))
        self.tabAnalysisMethod.setTabText(self.tabAnalysisMethod.indexOf(self.tabPointEstimate), QCoreApplication.translate("MainWindow", u"Point estimate", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.menu_analysis_method.setTitle(QCoreApplication.translate("MainWindow", u"Analysis method", None))
    # retranslateUi

