import os
import sys
import traceback
from functools import partial
from pathlib import Path

import PySide6

dirname = os.path.dirname(PySide6.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox, QTableWidgetItem

import numpy
import scipy
import pyqtgraph as pg

from export import export_as_csv
from interface import Ui_MainWindow
from signal_processing import (
    calculate_indexes,
    cubic_spline,
    linear_interp,
    open_data_file,
    shift_signal,
)


class CustomLinearRegionItem(pg.LinearRegionItem):
    def lineMoveFinished(self):
        pass


COMBO_TWIN_INDEX = 5


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        icon_path = os.path.join("icons", "brain.png")
        self.setWindowIcon(QIcon(icon_path))
        self.setupUi(self)
        self.showMaximized()

        self.menubar.setNativeMenuBar(False)

        # Set empty analys method
        self.analysis_method = None

        # Disable axes auto range button
        self.top_axes.hideButtons()
        self.bottom_axes.hideButtons()

        # Hide vertical scroll
        self.resultsTable.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # File menu
        self.menu_file_open_action.setShortcut("Ctrl+O")
        self.menu_file_open_action.triggered.connect(self.open_file)

        # Settings menu
        self.menu_analysis_method_frequency_band.triggered.connect(
            self.set_frequency_band_analysis_method
        )
        self.menu_analysis_method_point_estimate.triggered.connect(
            self.set_point_estimate_analysis_method
        )
        self.menu_analysis_method_ask_on_new_file.triggered.connect(
            self.set_ask_on_new_file_method
        )

        # Save results menu
        self.menu_save_results_action.setShortcut("Ctrl+S")
        self.menu_save_results_action.triggered.connect(self.save_results)

        # Combo boxes
        self.topAxesComboBox.currentIndexChanged.connect(self.change_top_axes)
        self.bottomAxesComboBox.currentIndexChanged.connect(self.change_bottom_axes)

        # ROI interval
        self.lineEditStartTimeAxes.editingFinished.connect(self.update_roi_from_form)
        self.lineEditEndTimeAxes.editingFinished.connect(self.update_roi_from_form)

        # Analysis options
        # comboboxes
        self.interpMethodComboBox.currentIndexChanged.connect(self.safe_analyze)
        self.interpMethodComboBox.currentIndexChanged.connect(self.toggle_resampling_frequency)
        self.windowComboBox.currentIndexChanged.connect(self.safe_analyze)
        # textfields
        self.resamplingFrequency.editingFinished.connect(self.safe_analyze)
        self.segmentSize.editingFinished.connect(self.safe_analyze)
        self.overlapSize.editingFinished.connect(self.safe_analyze)

        self.lineEditVLFLower.editingFinished.connect(self.safe_analyze)
        self.lineEditVLFUpper.editingFinished.connect(self.safe_analyze)
        self.lineEditLFLower.editingFinished.connect(self.safe_analyze)
        self.lineEditLFUpper.editingFinished.connect(self.safe_analyze)
        self.lineEditHFLower.editingFinished.connect(self.safe_analyze)
        self.lineEditHFUpper.editingFinished.connect(self.safe_analyze)

        # Point Frequency
        self.lineEditPointEstimateFrequency.editingFinished.connect(self.update_line_roi_from_form)

        self.coherenceThreshold.editingFinished.connect(self.safe_analyze)
        self.radioButtonApplyCoherence.toggled.connect(self.safe_analyze)
        self.radioButtonSimulatedCoherence.toggled.connect(self.safe_analyze)
        self.radioButtonSimulatedCoherence.toggled.connect(self._toggle_coherence_threshold)
        self.radioButtonShowMarkers.toggled.connect(self.change_both_axes)
        self.radioButtonSmoothPSD.toggled.connect(self.safe_analyze)

        # Shift CBFV
        self.lineEditShiftCBFV.setText("0.00")
        self.lineEditShiftCBFV.editingFinished.connect(self.shift_cbfv)

        self._restart_config_variables()

    def _restart_config_variables(self):
        # Init main variables
        self.time = None
        self.region_start = None
        self.region_end = None

        # Init last opened directory
        self.last_dir = "."
        self.file_name = ""

        # Init plot config variables
        self.top_line_roi = None
        self.bottom_line_roi = None
        self.top_roi = None
        self.bottom_roi = None
        self._roi_region = None

        self._init_results_table()
        self._set_empty_table()

    def _init_results_table(self):
        # Table style
        # brush = QBrush(QColor(255, 255, 255, 255))
        # brush.setStyle(Qt.NoBrush)
        # brush1 = QBrush(QColor(44, 44, 44, 255))
        # brush1.setStyle(Qt.SolidPattern)
        # __qtablewidgetitem10 = QTableWidgetItem()
        # __qtablewidgetitem10.setBackground(brush1)
        # __qtablewidgetitem10.setForeground(brush)
        # self.resultsTable.setItem(0, 0, __qtablewidgetitem10)

        # Table data
        self.resultsTable.setRowCount(6)
        self.resultsTable.setColumnCount(7)
        self.resultsTable.setColumnWidth(0, 170)
        self.resultsTable.setColumnWidth(5, 150)
        self.resultsTable.setHorizontalHeaderLabels(self.analysis_method_table_labels)
        self.resultsTable.setVerticalHeaderLabels(("", "", "", "", "", ""))

        self.resultsTable.setItem(0, 0, QTableWidgetItem("Gain"))
        self.resultsTable.setItem(1, 0, QTableWidgetItem("Gain norm"))
        self.resultsTable.setItem(2, 0, QTableWidgetItem(u"|Coh|\u00B2"))
        self.resultsTable.setItem(3, 0, QTableWidgetItem(u"Phase (deg)"))
        self.resultsTable.setItem(4, 0, QTableWidgetItem(u"Power ABP (mmHg\u00B2)"))
        self.resultsTable.setItem(5, 0, QTableWidgetItem(u"Power CBFV ((cm/s)\u00B2)"))

        self.resultsTable.setItem(0, 5, QTableWidgetItem("Avg. ABP (mmHg)"))
        self.resultsTable.setItem(1, 5, QTableWidgetItem("Avg. CBFV (cm/s)"))
        self.resultsTable.setItem(2, 5, QTableWidgetItem("Std. ABP (mmHg)"))
        self.resultsTable.setItem(3, 5, QTableWidgetItem("Std. CBFV (cm/s)"))
        self.resultsTable.setItem(4, 5, QTableWidgetItem("# Windows"))

    def _set_empty_table(self):
        for i in range(1, 4):
            for j in range(6):
                self.resultsTable.setItem(j, i, QTableWidgetItem("-"))

        self.resultsTable.setItem(0, 6, QTableWidgetItem("-"))
        self.resultsTable.setItem(1, 6, QTableWidgetItem("-"))
        self.resultsTable.setItem(2, 6, QTableWidgetItem("-"))
        self.resultsTable.setItem(3, 6, QTableWidgetItem("-"))
        self.resultsTable.setItem(4, 6, QTableWidgetItem("-"))

    def _fill_table_results(self, results):
        # Header
        self.resultsTable.setHorizontalHeaderLabels(self.analysis_method_table_labels)
        # Descriptive results
        self.resultsTable.setItem(0, 6, QTableWidgetItem(f"{results['avg_abp']:.3f}"))
        self.resultsTable.setItem(1, 6, QTableWidgetItem(f"{results['avg_cbfv']:.3f}"))
        self.resultsTable.setItem(2, 6, QTableWidgetItem(f"{results['std_abp']:.3f}"))
        self.resultsTable.setItem(3, 6, QTableWidgetItem(f"{results['std_cbfv']:.3f}"))
        self.resultsTable.setItem(4, 6, QTableWidgetItem(f"{int(results['n_windows'])}"))

        if self.is_frequncy_band_analysis:
            self._fill_table_results_frequency_band(results)
        elif self.is_point_estimate_analysis:
            self._fill_table_results_point_estimate(results)

    def _fill_table_results_frequency_band(self, results):
        # Gain
        self.resultsTable.setItem(0, 1, QTableWidgetItem(f"{results['gain_vlf']:.3f}"))
        self.resultsTable.setItem(0, 2, QTableWidgetItem(f"{results['gain_lf']:.3f}"))
        self.resultsTable.setItem(0, 3, QTableWidgetItem(f"{results['gain_hf']:.3f}"))

        # Gain norm
        self.resultsTable.setItem(1, 1, QTableWidgetItem(f"{results['gain_vlf_norm']:.3f}"))
        self.resultsTable.setItem(1, 2, QTableWidgetItem(f"{results['gain_lf_norm']:.3f}"))
        self.resultsTable.setItem(1, 3, QTableWidgetItem(f"{results['gain_hf_norm']:.3f}"))

        # Coherence (|Coh|^2)
        self.resultsTable.setItem(2, 1, QTableWidgetItem(f"{results['coherence_vlf']:.3f}"))
        self.resultsTable.setItem(2, 2, QTableWidgetItem(f"{results['coherence_lf']:.3f}"))
        self.resultsTable.setItem(2, 3, QTableWidgetItem(f"{results['coherence_hf']:.3f}"))

        # Phase
        self.resultsTable.setItem(3, 1, QTableWidgetItem(f"{results['phase_vlf']:.3f}"))
        self.resultsTable.setItem(3, 2, QTableWidgetItem(f"{results['phase_lf']:.3f}"))
        self.resultsTable.setItem(3, 3, QTableWidgetItem(f"{results['phase_hf']:.3f}"))

        # Power ABP
        self.resultsTable.setItem(4, 1, QTableWidgetItem(f"{results['pxx_vlf']:.3f}"))
        self.resultsTable.setItem(4, 2, QTableWidgetItem(f"{results['pxx_lf']:.3f}"))
        self.resultsTable.setItem(4, 3, QTableWidgetItem(f"{results['pxx_hf']:.3f}"))

        # Power CBFV
        self.resultsTable.setItem(5, 1, QTableWidgetItem(f"{results['pyy_vlf']:.3f}"))
        self.resultsTable.setItem(5, 2, QTableWidgetItem(f"{results['pyy_lf']:.3f}"))
        self.resultsTable.setItem(5, 3, QTableWidgetItem(f"{results['pyy_hf']:.3f}"))

    def _fill_table_results_point_estimate(self, results):
        self.resultsTable.setItem(0, 1, QTableWidgetItem(f"{results['point_estimate_gain']:.3f}"))
        self.resultsTable.setItem(1, 1, QTableWidgetItem(f"{results['point_estimate_gain_norm']:.3f}"))
        self.resultsTable.setItem(2, 1, QTableWidgetItem(f"{results['point_estimate_coherence']:.3f}"))
        self.resultsTable.setItem(3, 1, QTableWidgetItem(f"{results['point_estimate_phase']:.3f}"))
        self.resultsTable.setItem(4, 1, QTableWidgetItem(f"{results['point_estimate_abp_psd']:.3f}"))
        self.resultsTable.setItem(5, 1, QTableWidgetItem(f"{results['point_estimate_cbfv_psd']:.3f}"))

    def _define_analysis_method(self):
        if self.menu_analysis_method_ask_on_new_file.isChecked():
            self._show_analysis_method_dialog()
            self._update_frequency_panel()
            return

    def _show_analysis_method_dialog(self):
        dialog = QMessageBox(self)
        dialog.setText("Select Analysis to Run")
        dialog.setWindowTitle("Choose Method | CardioBrain")
        dialog.setStyleSheet("color:white;background:black")
        frequency_band_button = dialog.addButton(
            "Frequency band",
            QMessageBox.ButtonRole.ActionRole
        )
        frequency_band_button._method = "frequency-band"
        point_estimate_button = dialog.addButton(
            "Point estimate",
            QMessageBox.ButtonRole.ActionRole
        )
        point_estimate_button._method = "point-estimate"
        dialog.buttonClicked.connect(self._dialog_button_define_analysis_method)
        dialog.exec()

    def _dialog_button_define_analysis_method(self, dialog_button):
        self.analysis_method = dialog_button._method

    def _update_info_status(self, msg, status="success"):
        green = (
            "#statusColor {\n\tbackground-color: rgb(0,255,0); \n\tcolor: rgb(0,255,0);"
            "\n\tborder-radius: 4px\n}"
        )
        red = (
            "#statusColor {\n\tbackground-color: rgb(255,0,0); \n\tcolor: rgb(255,0,0);"
            "\n\tborder-radius: 4px\n}"
        )
        if status == "error":
            self.statusColor.setStyleSheet(red)
        elif status == "success":
            self.statusColor.setStyleSheet(green)

        self.statusLabel.setText(msg)

    def _toggle_coherence_threshold(self):
        self.coherenceThreshold.setEnabled(not self.radioButtonSimulatedCoherence.isChecked())

    @property
    def is_point_estimate_analysis(self):
        return self.analysis_method == "point-estimate"

    @property
    def is_frequncy_band_analysis(self):
        # When the analysis_method is not set (None) we assume frequency band as default
        return self.analysis_method in (None, "frequency-band")

    @property
    def analysis_method_table_labels(self):
        default = ("", "VLF", "LF", "HF", "", "", "")
        return {
            "point-estimate": ("", "", "", "", "", "", ""),
        }.get(self.analysis_method, default)

    @property
    def analysis_method_export_columns(self):
        default = [
            "gain_vlf",
            "gain_lf",
            "gain_hf",
            "phase_vlf",
            "phase_lf",
            "phase_hf",
            "coherence_vlf",
            "coherence_lf",
            "coherence_hf",
            "gain_vlf_norm",
            "gain_lf_norm",
            "gain_hf_norm",
            "coherence_threshold_applied",
            "n_windows",
            "avg_abp",
            "avg_cbfv",
            "std_abp",
            "std_cbfv",
            "coherence_threshold",
        ]
        point_estimate_columns = [
            "point_estimate_gain",
            "point_estimate_gain_norm",
            "point_estimate_phase",
            "point_estimate_coherence",
            "point_estimate_frequency",
            "point_estimate_abp_psd",
            "point_estimate_cbfv_psd",
            "coherence_threshold_applied",
            "n_windows",
            "avg_abp",
            "avg_cbfv",
            "std_abp",
            "std_cbfv",
            "coherence_threshold",

        ]
        return {
            "point-estimate": point_estimate_columns,
        }.get(self.analysis_method, default)

    # TODO: create variable with big dict with config for each method
    # e.g: {"point-estimate: {"color": (127, 10, 1), "columns": ...}}
    @property
    def analysis_method_default_psd_brush(self):
        default = (127, 127, 127, 100)
        return {
            "point-estimate": (127, 127, 255, 200),
        }.get(self.analysis_method, default)

    @property
    def duration(self):
        if self.time is not None:
            return self.time[-1]
        else:
            return None

    @property
    def start_signal(self):
        if self.time is not None:
            return self.time[0]
        else:
            return None

    @property
    def vlf_range(self):
        return float(self.lineEditVLFLower.text()), float(self.lineEditVLFUpper.text())

    @property
    def lf_range(self):
        return float(self.lineEditLFLower.text()), float(self.lineEditLFUpper.text())

    @property
    def hf_range(self):
        return float(self.lineEditHFLower.text()), float(self.lineEditHFUpper.text())

    @property
    def roi_region(self):
        if self._roi_region is None:
            return [0, self.duration]
        else:
            return self._roi_region

    @property
    def line_roi_position(self):
        return float(self.lineEditPointEstimateFrequency.text())

    @property
    def coherence_threshold(self):
        threshold = None
        if not self.radioButtonSimulatedCoherence.isChecked():
            threshold = self.analysis_options["coherence_threshold"]

        return threshold

    @property
    def analysis_options(self):
        interp_methods = {
            0: linear_interp,
            1: cubic_spline,
            2: none_interp,
        }
        windows = {
            0: scipy.signal.windows.hann,
            1: scipy.signal.windows.hamming,
            2: scipy.signal.windows.boxcar,
        }
        return {
            "interp_method": interp_methods[self.interpMethodComboBox.currentIndex()],
            "resampling_frequency": int(self.resamplingFrequency.text()),
            "segment_size": int(self.segmentSize.text()),
            "overlap_size": int(self.overlapSize.text()),
            "window": windows[self.windowComboBox.currentIndex()],
            "coherence_threshold": float(self.coherenceThreshold.text()),
            "apply_coherence_threshold": self.radioButtonApplyCoherence.isChecked(),
            "smooth_psd": self.radioButtonSmoothPSD.isChecked(),
            "method": self.analysis_method,
            "point_estimate_frequency": float(self.lineEditPointEstimateFrequency.text()),
        }

    @property
    def indexes_region(self):
        return numpy.where(
            numpy.logical_and(self.time >= self._roi_region[0], self.time <= self._roi_region[1])
        )[0]

    @property
    def time_region(self):
        return self.time[self.indexes_region]

    @property
    def abp_region(self):
        return self.abp[self.indexes_region]

    @property
    def cbfv_region(self):
        return self.cbfv[self.indexes_region]

    @property
    def plot_marker(self):
        return "o" if self.radioButtonShowMarkers.isChecked() else None

    def save_file_name(self, ext):
        return f"{Path(self.file_name).stem}.{ext}"

    def _save_last_dir(self, file_name):
        self.last_dir = os.path.dirname(file_name)

    def _set_file_name(self, file_path):
        file_name = os.path.basename(file_path)
        self.lineEditFileName.setText(file_name)
        return file_name

    def _update_edit_time_ranges(self, region):
        self.lineEditStartTimeAxes.setText(f"{region[0]:.2f}")
        self.lineEditEndTimeAxes.setText(f"{region[1]:.2f}")

    def set_frequency_band_analysis_method(self):
        self.menu_analysis_method_point_estimate.setChecked(False)
        self.menu_analysis_method_ask_on_new_file.setChecked(False)
        self.analysis_method = "frequency-band"
        self._update_frequency_panel()

    def set_point_estimate_analysis_method(self):
        self.menu_analysis_method_frequency_band.setChecked(False)
        self.menu_analysis_method_ask_on_new_file.setChecked(False)
        self.analysis_method = "point-estimate"
        self._update_frequency_panel()

    def set_ask_on_new_file_method(self):
        self.menu_analysis_method_frequency_band.setChecked(False)
        self.menu_analysis_method_point_estimate.setChecked(False)
        self.analysis_method = None

    def _update_frequency_panel(self):
        methods = {"frequency-band": 0, "point-estimate": 1}
        index = methods[self.analysis_method]
        self.tabAnalysisMethod.setCurrentIndex(index)
        self.tabAnalysisMethod.setTabEnabled(index, True)
        [self.tabAnalysisMethod.setTabEnabled(i, False) for i in methods.values() if i != index]

    def open_file(self):
        self.file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select file",
            self.last_dir,
            "All Files (*);;CSV Files (*.csv);;Text Files (*.txt)",
        )
        if self.file_path:
            try:
                time, abp, cbfv = open_data_file(self.file_path)
                self._restart_config_variables()
            except Exception as exc:
                self._update_info_status(msg="Error. Could not open file", status="error")
                # TODO: improve logging and save traceback
                print(exc)
                return

            self._define_analysis_method()

            self.time = time
            self.abp = abp
            self.cbfv = cbfv
            self.fs = round(1.0 / time[1] - time[0])

            self._save_last_dir(self.file_path)

            self._update_info_status(msg="Ready", status="success")
            self.file_name = self._set_file_name(self.file_path)

            self._original_time = self.time.copy()
            self._original_abp = self.abp.copy()
            self._original_cbfv = self.cbfv.copy()

            self.plot_abp(self.top_axes)
            self.plot_cbfv(self.bottom_axes)
            self._update_edit_time_ranges(region=(0, self.duration))

            # Update signal region limit
            self.region_start = 0
            self.region_end = self.time[-1]
            self._roi_region = (self.region_start, self.region_end)

            # Signal Processing
            self.safe_analyze()

    def analyze(self):
        # Generalize this check
        if self.time is None:
            return

        fs = self.analysis_options["resampling_frequency"]
        options = {
            "vlf": self.vlf_range,
            "lf": self.lf_range,
            "hf": self.hf_range,
            "segment_size": self.analysis_options["segment_size"],
            "overlap": self.analysis_options["overlap_size"],
            "window": self.analysis_options["window"],
            "coherence_threshold": self.coherence_threshold,
            "apply_coherence_threshold": self.radioButtonApplyCoherence.isChecked(),
            "point_estimate_frequency": self.analysis_options["point_estimate_frequency"],
            "smooth_psd": self.analysis_options["smooth_psd"],
        }
        self.results = calculate_indexes(
            self.time_region,
            self.abp_region,
            self.cbfv_region,
            fs,
            self.analysis_method,
            interp_method=self.analysis_options["interp_method"],
            options=options,
        )
        self._fill_table_results(self.results)

        # Update plots
        self.change_both_axes()

    def save_results(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            caption="Save results",
            dir=os.path.join(self.last_dir, self.save_file_name(ext="csv")),
            filter="CSV files (*.csv)",
        )
        if file_path:
            export_as_csv(file_path, self.results, self.analysis_method_export_columns)

    def post_analysis(self):
        self._update_info_status(msg="Ready", status="success")
        self.menu_save_results_action.setEnabled(True)

    def safe_analyze(self):
        try:
            self.analyze()
            self.post_analysis()
            self._update_info_status(status="success", msg="Ready")
        except Exception:
            # TODO: improve logging and save it files
            msg = traceback.format_exc()
            print(msg)
            self._set_empty_table()
            self._update_info_status(msg="Error analyzing signals", status="error")

    def shift_cbfv(self):
        shift_seconds = float(self.lineEditShiftCBFV.text())
        self.cbfv = shift_signal(
            self._original_time,
            self._original_cbfv.copy(),
            fs=self.fs,
            shift_seconds=shift_seconds,
        )
        self.change_bottom_axes()
        self.analyze()

    def change_both_axes(self):
        self.change_top_axes()
        self.change_bottom_axes()

    def change_top_axes(self):
        p_plot_abp_cbfv = partial(self.plot_abp_cbfv, name="top")
        if hasattr(self, "plot_item"):
            self.top_axes.removeItem(self.plot_item)
            self.bottom_axes.removeItem(self.view_box)
        {
            0: self.plot_abp,
            1: self.plot_abp_psd,
            2: self.plot_gain,
            3: self.plot_coherence,
            4: self.plot_phase,
            COMBO_TWIN_INDEX: p_plot_abp_cbfv,
        }.get(self.topAxesComboBox.currentIndex(), lambda: None)(self.top_axes)

    def change_bottom_axes(self):
        p_plot_abp_cbfv = partial(self.plot_abp_cbfv, name="bottom")
        if hasattr(self, "plot_item"):
            self.bottom_axes.removeItem(self.plot_item)
            self.bottom_axes.removeItem(self.view_box)
        {
            0: self.plot_cbfv,
            1: self.plot_cbfv_psd,
            2: self.plot_gain,
            3: self.plot_coherence,
            4: self.plot_phase,
            5: p_plot_abp_cbfv,
        }.get(self.bottomAxesComboBox.currentIndex(), lambda: None)(self.bottom_axes)

    def update_roi_from_form(self):
        start = float(self.lineEditStartTimeAxes.text())
        end = float(self.lineEditEndTimeAxes.text())
        region = (start, end)

        self.top_roi.setRegion(region)
        self.bottom_roi.setRegion(region)
        self.safe_analyze()

    def update_line_roi_from_form(self):
        point = float(self.lineEditPointEstimateFrequency.text())
        self.top_line_roi.setPos(point)
        self.bottom_line_roi.setPos(point)
        self.safe_analyze()

    def _keep_region_boundary(self, region):
        # Do not let area outside signal
        if region[0] < self.region_start:
            region = (self.region_start, region[1])
        if region[1] > self.region_end:
            region = (region[0], self.region_end)

        return region

    def update_top_roi(self):
        region = self._keep_region_boundary(self.top_roi.getRegion())
        self._roi_region = region

        if self.bottom_roi is not None:
            self.bottom_roi.setRegion(region)

        self._update_edit_time_ranges(region)

    def update_bottom_roi(self):
        region = self._keep_region_boundary(self.bottom_roi.getRegion())
        self._keep_region_boundary(region)
        self._roi_region = region
        if self.top_roi is not None:
            self.top_roi.setRegion(region)

        self._update_edit_time_ranges(region)

    def update_top_line_roi(self):
        self._update_point_frequency_value(self.top_line_roi.getXPos())
        if self.bottom_line_roi is not None:
            self.bottom_line_roi.setPos(self.line_roi_position)

    def update_bottom_line_roi(self):
        self._update_point_frequency_value(self.bottom_line_roi.getXPos())

        if self.top_line_roi is not None:
            self.top_line_roi.setPos(self.line_roi_position)

    def add_roi(self, axes, action):
        roi = CustomLinearRegionItem(self.roi_region, pen=pg.mkPen(width=3.5))

        roi.lines[0].sigPositionChangeFinished.connect(self.safe_analyze)
        roi.lines[1].sigPositionChangeFinished.connect(self.safe_analyze)
        roi.sigRegionChangeFinished.connect(self.safe_analyze)

        roi.setZValue(-10)

        # Callback when area change.
        roi.sigRegionChanged.connect(action)
        axes.addItem(roi)
        return roi

    def plot_cbfv(self, axes):
        self.plot_time_series(
            axes,
            self.time,
            self.cbfv,
            xlabel="Time (s)",
            ylabel="CBFV (cm/s)",
            xlim=[0, self.duration],
            color="g"
        )
        self.bottom_roi = self.add_roi(self.bottom_axes, self.update_bottom_roi)

    def plot_cbfv_psd(self, axes):
        self.plot_psd(
            axes,
            self.results["frequency"],
            self.results["pyy"],  # TODO: change pyy to cbfv_psd
            vlf=self.vlf_range,
            lf=self.lf_range,
            hf=self.hf_range,
            label="PSD ((cm/s)²/Hz)",
            default_brush=self.analysis_method_default_psd_brush,
            show_frequency_bands=self.is_frequncy_band_analysis,  # TODO: this can be a config too
        )
        if self.is_point_estimate_analysis:
            self.bottom_line_roi = self.add_line_roi(axes, self.update_bottom_line_roi)

    def plot_abp(self, axes):
        self.plot_time_series(
            axes,
            self.time,
            self.abp,
            xlabel="Time (s)",
            ylabel="ABP (mmHg)",
            xlim=[0, self.duration],
            color="y"
        )
        self.top_roi = self.add_roi(self.top_axes, self.update_top_roi)

    def plot_abp_psd(self, axes):
        self.plot_psd(
            axes,
            self.results["frequency"],
            self.results["pxx"],  # TODO: change pxx to abp_psd
            vlf=self.vlf_range,
            lf=self.lf_range,
            hf=self.hf_range,
            label="PSD (mmHg²/Hz)",
            default_brush=self.analysis_method_default_psd_brush,
            show_frequency_bands=self.is_frequncy_band_analysis,
        )
        if self.is_point_estimate_analysis:
            self.top_line_roi = self.add_line_roi(axes, self.update_top_line_roi)

    def plot_gain(self, axes):
        freq = self.results["frequency"]
        self.plot_time_series(
            axes,
            freq,
            self.results["gain"],
            xlabel="Frequency (Hz)",
            ylabel="Gain",
            xlim=[0, self.hf_range[1]],
            color="g"
        )
        self._add_frequency_bands_lines(axes)

    def plot_coherence(self, axes):
        axes.addLegend()
        freq = self.results["frequency"]
        self.plot_time_series(
            axes,
            freq,
            self.results["coherence"],
            xlabel="Frequency (Hz)",
            ylabel="|Coherence|²",
            xlim=[0, self.hf_range[1]],
            color="g"
        )
        self._add_frequency_bands_lines(axes)
        # Add coherence threshold line
        threshold = self.results.get("coherence_threshold", None)
        if self.results["coherence_threshold_applied"]:
            pen_color = "r"
        else:
            pen_color = "grey"

        if self.results["coherence_threshold"] is None:
            threshold = 0.5
            pen_color = "grey"

        label = f"Threshold (={threshold:.2f})"

        axes.addLine(
            x=None,
            y=threshold,
            pen=pg.mkPen(pen_color, width=2),
            label=label,
        )

    def plot_phase(self, axes):
        freq = self.results["frequency"]
        self.plot_time_series(
            axes,
            freq,
            self.results["phase"],
            xlabel="Frequency (Hz)",
            ylabel="Phase (deg)",
            xlim=[0, self.hf_range[1]],
            color="g"
        )
        self._add_frequency_bands_lines(axes)

    def purge_multiple_axes(self, axes):
        # Do not delete twin plot if it is appearing in another axes
        top_has_twin = self.topAxesComboBox.currentIndex() == COMBO_TWIN_INDEX
        bottom_has_twin = self.bottomAxesComboBox.currentIndex() == COMBO_TWIN_INDEX
        if hasattr(self, "top_twin_plot_item") and not top_has_twin or axes is self.top_axes:
            try:
                self.top_axes.clear()
                self.top_extra_axis.hide()
                self.top_twin_plot_item.clear()
                self.top_twin_view_box.clear()
                self.top_curve_item.clear()
                self.top_twin_plot_item.legend.removeItem(self.top_curve_item)
                delattr(self, "top_twin_plot_item")
                delattr(self, "top_twin_view_box")
            except Exception:
                pass

        if (
            hasattr(self, "bottom_twin_plot_item")
            and not bottom_has_twin
            or axes is self.bottom_axes
        ):
            try:
                self.bottom_axes.clear()
                self.bottom_extra_axis.hide()
                self.bottom_twin_plot_item.clear()
                self.bottom_twin_view_box.clear()
                self.bottom_twin_plot_item.legend.removeItem(self.bottom_curve_item)
                delattr(self, "bottom_twin_plot_item")
                delattr(self, "bottom_twin_view_box")
            except Exception:
                pass

    # TODO: change name
    def plot_time_series(
        self, axes, time, signal, xlabel, ylabel, xlim, color, name=None, clear=True
    ):
        self.purge_multiple_axes(axes)
        if clear:
            axes.clear()
        axes.plot(time, signal, pen=pg.mkPen(color,  width=2), name=name, symbol=self.plot_marker)
        axes.setLabel("left", ylabel)
        axes.setLabel("bottom", xlabel)
        axes.showGrid(x=True, y=True, alpha=1.0)
        axes.setRange(xRange=xlim)

    def plot_abp_cbfv(self, axes, name):
        self.purge_multiple_axes(axes)
        axes.clear()
        axes.addLegend()

        plot_item = axes.plotItem
        plot_item.setLabels(left='axis 1')

        view_box = pg.ViewBox()
        plot_item.showAxis("right")
        plot_item.scene().addItem(view_box)
        plot_item.getAxis("right").linkToView(view_box)
        view_box.setXLink(plot_item)
        axis = plot_item.getAxis('right')
        axis.setLabel("CBFV (cm/s)")

        self.plot_time_series(
            plot_item,
            self.time,
            self.abp,
            xlabel="Time (s)",
            ylabel="ABP (mmHg)",
            xlim=[0, self.duration],
            color="y",
            name="ABP",
            clear=False
        )

        curve_item = pg.PlotCurveItem(
            self.time,
            self.cbfv,
            pen=pg.mkPen("g",  width=2),
        )
        view_box.addItem(curve_item)

        if self.plot_marker:
            markerItem = pg.ScatterPlotItem(
                self.time,
                self.cbfv,
                symbol=self.plot_marker,
                brush="#FF999C",
            )
            view_box.addItem(markerItem)

        plot_item.legend.addItem(curve_item, "CBFV")

        def update_views(plot_item, view_box, *args):
            view_box.setGeometry(plot_item.vb.sceneBoundingRect())
            view_box.linkedViewChanged(plot_item.vb, view_box.XAxis)

        p_update_views = partial(update_views, plot_item, view_box)
        p_update_views()
        plot_item.vb.sigResized.connect(p_update_views)

        if name == "top":
            self.top_twin_plot_item = plot_item
            self.top_twin_view_box = view_box
            self.top_curve_item = curve_item
            self.top_roi = self.add_roi(self.top_axes, self.update_top_roi)
            self.top_extra_axis = axis
        elif name == "bottom":
            self.bottom_twin_plot_item = plot_item
            self.bottom_twin_view_box = view_box
            self.bottom_curve_item = curve_item
            self.bottom_roi = self.add_roi(self.bottom_axes, self.update_bottom_roi)
            self.bottom_extra_axis = axis

    def _add_frequency_line(self, axes, x, ylim):
        axes.addLine(
            x=x,
            y=ylim,
            pen=pg.mkPen("w", width=2, dash=[2, 4])
        )

    def _add_frequency_bands_lines(self, axes):
        ylim = axes.getAxis("left").range
        self._add_frequency_line(axes, x=[self.vlf_range[0], self.vlf_range[0]], ylim=ylim)
        self._add_frequency_line(axes, x=[self.vlf_range[1], self.vlf_range[1]], ylim=ylim)
        self._add_frequency_line(axes, x=[self.lf_range[0], self.lf_range[0]], ylim=ylim)
        self._add_frequency_line(axes, x=[self.lf_range[1], self.lf_range[1]], ylim=ylim)
        self._add_frequency_line(axes, x=[self.hf_range[0], self.hf_range[0]], ylim=ylim)
        self._add_frequency_line(axes, x=[self.hf_range[1], self.hf_range[1]], ylim=ylim)

    def plot_psd(
        self,
        axes,
        frequency,
        psd,
        vlf,
        lf,
        hf,
        label,
        default_brush,
        show_frequency_bands=True,
    ):
        self.purge_multiple_axes(axes)

        # For aesthetic purpose, we are interpolating and resampling the PSD
        # for increased visual frequency resolution
        interp_frequency = numpy.arange(frequency[0], frequency[-1], 1 / 10000.0)
        cs = scipy.interpolate.CubicSpline(frequency, psd)
        interp_psd = cs(interp_frequency)

        indexes_vlf = numpy.where(
            numpy.logical_and(interp_frequency >= vlf[0], interp_frequency < vlf[1])
        )[0]
        indexes_lf = numpy.where(numpy.logical_and(
            interp_frequency >= lf[0], interp_frequency < lf[1])
        )[0]
        indexes_hf = numpy.where(
            numpy.logical_and(interp_frequency >= hf[0], interp_frequency < hf[1])
        )[0]

        axes.clear()
        # Total PSD
        axes.plot(
            interp_frequency,
            interp_psd,
            fillLevel=0.0,
            brush=default_brush,
        )
        axes.setRange(xRange=[0, self.hf_range[-1]])
        axes.setLabel("left", label)
        axes.setLabel("bottom", "Frequency (Hz)")
        axes.showGrid(x=True, y=True, alpha=1.0)

        # TODO: Remove this logic from this function
        if show_frequency_bands:
            # VLF
            axes.plot(
                interp_frequency[indexes_vlf],
                interp_psd[indexes_vlf],
                fillLevel=0.0,
                brush=(127, 127, 255, 200)
            )
            # LF
            axes.plot(
                interp_frequency[indexes_lf],
                interp_psd[indexes_lf],
                fillLevel=0.0,
                brush=(178, 127, 255, 200)
            )
            # HF
            axes.plot(
                interp_frequency[indexes_hf],
                interp_psd[indexes_hf],
                fillLevel=0.0,
                brush=(127, 127, 255, 200)
            )

            # Add frequency band lines
            self._add_frequency_bands_lines(axes)

    def add_line_roi(self, axes, action):
        # Add line showing the point estimate frequency
        line_roi = pg.InfiniteLine(
            self.analysis_options["point_estimate_frequency"],
            pen=pg.mkPen("r", width=3.5),
            hoverPen=pg.mkPen("w", width=3.5),
            movable=True,
            bounds=[0, self.fs / 2.0],
        )
        axes.addItem(line_roi)
        line_roi.sigPositionChanged.connect(action)
        line_roi.sigPositionChangeFinished.connect(self.safe_analyze)
        return line_roi

    def _update_point_frequency_value(self, pos):
        self.lineEditPointEstimateFrequency.setText(f"{pos:.3f}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    app.exec()
