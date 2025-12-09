import csv

import numpy
import pandas
import scipy


def open_data_file(file_path):
    open_funcs = [open_csv_file, open_data_frame]
    for func in open_funcs:
        try:
            time, abp, cbfv = func(file_path)
        except Exception:
            pass

    return time, abp, cbfv


def sniff_csv_separator(file_path):
    with open(file_path) as fobj:
        sample = fobj.read(1024)
        dialect = csv.Sniffer().sniff(sample)
        return dialect.delimiter


def open_data_frame(file_path):
    data = pandas.read_csv(file_path, sep="\t")
    return data["Time"].values, data["MABP [mmHg]"].values, data["CBFV-L [cm/s]"].values


def open_csv_file(file_path):
    sep = sniff_csv_separator(file_path)
    data = pandas.read_csv(file_path, sep=sep)
    # Remove all rows which all cells are empty strings
    data.replace(r"^\s+$", numpy.nan, inplace=True, regex=True)
    data.dropna(how="all", inplace=True)
    rri = data.iloc[:, 0].astype(float).values
    cbv = data.iloc[:, 1].astype(float).values
    abp = data.iloc[:, 2].astype(float).values
    time = numpy.cumsum(rri) - rri[0]
    return time, abp, cbv


def band_indexes(frequency, lower, upper):
    return numpy.where(numpy.logical_and(frequency >= lower, frequency < upper))[0]


def band_gain(gain, indexes):
    return numpy.nanmean(abs(gain[indexes]))


def band_phase(phase, indexes):
    return numpy.nanmean(phase[indexes]) / (2 * numpy.pi) * 360


def band_coherence(coherence, indexes):
    return numpy.nanmean(coherence[indexes])


def band_power(psd, indexes, freq_resolution):
    return 2 * numpy.nansum(psd[indexes]) * freq_resolution


def frequency_bands_results(frequency, pxx, pyy, gain, phase, coherence, options):
    indexes_vlf = band_indexes(frequency, *options["vlf"])
    indexes_lf = band_indexes(frequency, *options["lf"])
    indexes_hf = band_indexes(frequency, *options["hf"])

    return {
        "gain_vlf": band_gain(gain, indexes_vlf),
        "gain_lf": band_gain(gain, indexes_lf),
        "gain_hf": band_gain(gain, indexes_hf),
        "phase_vlf": band_phase(phase, indexes_vlf),
        "phase_lf": band_phase(phase, indexes_lf),
        "phase_hf": band_phase(phase, indexes_hf),
        "coherence_vlf": band_coherence(coherence, indexes_vlf),
        "coherence_lf": band_coherence(coherence, indexes_lf),
        "coherence_hf": band_coherence(coherence, indexes_hf),
        "psd_abp_vlf": band_power(pxx, indexes_vlf, frequency[1]),
        "psd_abp_lf": band_power(pxx, indexes_lf, frequency[1]),
        "psd_abp_hf": band_power(pxx, indexes_hf, frequency[1]),
        "psd_cbfv_vlf": band_power(pyy, indexes_vlf, frequency[1]),
        "psd_cbfv_lf": band_power(pyy, indexes_lf, frequency[1]),
        "psd_cbfv_hf": band_power(pyy, indexes_hf, frequency[1]),
    }


def welch(x, y, segment_size, overlap, window_fun, fs):
    n_windows = int((len(x) - segment_size) / (segment_size - overlap)) + 1

    frequency = numpy.arange(0, fs, fs / segment_size)
    _, pxx = scipy.signal.welch(
        x,
        fs=fs,
        window=window_fun(segment_size, sym=False),
        nperseg=segment_size,
        noverlap=overlap,
        nfft=segment_size,
        detrend=False,
        return_onesided=False,
    )
    _, pyy = scipy.signal.welch(
        y,
        fs=fs,
        window=window_fun(segment_size, sym=False),
        nperseg=segment_size,
        noverlap=overlap,
        nfft=segment_size,
        detrend=False,
        return_onesided=False,
    )

    _, pxy = scipy.signal.csd(
        x,
        y,
        fs=fs,
        window=window_fun(segment_size, sym=False),
        nperseg=segment_size,
        noverlap=overlap,
        nfft=segment_size,
        detrend=False,
        return_onesided=False,
    )

    return frequency, pxx, pyy, pxy, n_windows


def smooth(psd, smooth_factor):
    # When using filtfilt the coefficients are: [0.25, 0.5, 0.25]
    triang = [0.5, 0.5]  # White paper recommendation #13
    psd_copy = psd.copy()
    psd_copy[0] = psd[1]
    psd_filt = scipy.signal.filtfilt(triang, 1, psd_copy)
    psd_filt[0] = psd[0]
    return psd_filt


def estimate_psd(
    time,
    abp,
    cbfv,
    interp_method,
    avg_abp,
    std_abp,
    avg_cbfv,
    std_cbfv,
    fs,
    options: dict = None,
):
    # TODO: docstring
    if options is None:
        options = dict()

    coherence_thresholds = {
        3: 0.51,
        4: 0.41,
        5: 0.34,
        6: 0.29,
        7: 0.25,
        8: 0.22,
        9: 0.20,
        10: 0.18,
        11: 0.17,
        12: 0.15,
        13: 0.14,
        14: 0.13,
        15: 0.12,
        20: 0.09,
        25: 0.08,
    }
    default_options = {
        "vlf": (0.02, 0.07),
        "lf": (0.07, 0.2),
        "hf": (0.2, 0.5),
        "detrend": lambda x: x - numpy.mean(x),
        "smooth_factor": 3,
        "coherence_threshold": None,
        "coherence_thresholds": coherence_thresholds,
        "apply_coherence_threshold": True,
        "remove_negative_phase": True,
        "negative_phase_cutoff": 0.1,
        "normalize": False,
        "window": scipy.signal.windows.hann,
        "segment_size": 1024,
        "overlap": 512,
        "normalize_cbfv": False,
        "normalize_abp": False,
    }
    options = {**default_options, **options}

    abp = options["detrend"](abp)
    cbfv = options["detrend"](cbfv)

    interp_abp = interp_method(time, abp, fs)
    interp_cbfv = interp_method(time, cbfv, fs)

    if options["normalize_cbfv"]:
        cbfv = (cbfv / avg_cbfv) * 100

    if options["normalize_abp"]:
        abp = (abp / avg_abp) * 100

    frequency, pxx, pyy, pxy, n_windows, = welch(
        x=interp_abp,
        y=interp_cbfv,
        window_fun=options.get("window"),
        segment_size=options.get("segment_size"),
        overlap=options.get("overlap"),
        fs=fs,
    )

    pxx = smooth(pxx, options.get("smooth_factor"))
    pyy = smooth(pyy, options.get("smooth_factor"))
    pxy = smooth(pxy, options.get("smooth_factor"))

    gain = pxy / pxx
    coherence = pxy / (numpy.sqrt(pxx * pyy))

    if options.get("coherence_threshold") is not None:
        coherence_threshold = options.get("coherence_threshold")
    else:
        coherence_threshold = coherence_thresholds.get(n_windows, options.get("coherence_threshold"))

    # If manual threshold is disable and there is no simulated coherence value
    # for a given n_widows
    if coherence_threshold is None:
        apply_coherence_threshold = False
    else:
        apply_coherence_threshold = options.get("apply_coherence_threshold")

    if apply_coherence_threshold:
        gain[numpy.where(abs(coherence) ** 2 < coherence_threshold)[0]] = numpy.nan

    phase = numpy.angle(gain)
    if options.get("remove_negative_phase"):
        cutoff = options.get("negative_phase_cutoff")
        indexes = numpy.where(phase[numpy.where(frequency < cutoff)[0]] < 0)
        phase[indexes] = numpy.nan

    results = {
        "coherence_threshold_applied": apply_coherence_threshold,
        "n_windows": n_windows,
        "pxx": abs(pxx),
        "pyy": abs(pyy),
        "pxy": abs(pxy),
        "gain": abs(gain),
        "gain_norm": abs(gain) / avg_cbfv * 100,
        "coherence": abs(coherence) ** 2,
        "phase": phase,
        "coherence_threshold": coherence_threshold,
        "frequency": frequency,
    }
    return results


def calculate_indexes(time, abp, cbfv, fs, method="tfa", interp_method=None, options: dict = None):
    avg_abp = abp.mean()
    avg_cbfv = cbfv.mean()
    std_abp = abp.std()
    std_cbfv = cbfv.std()

    results = estimate_psd(
        time,
        abp,
        cbfv,
        interp_method,
        avg_abp,
        std_abp,
        avg_cbfv,
        std_cbfv,
        fs,
        options
    )
    results["avg_abp"] = avg_abp
    results["avg_cbfv"] = avg_cbfv
    results["std_abp"] = std_abp
    results["std_cbfv"] = std_cbfv
    if method == "frequency-band":
        results.update(
            tfa(
                results["frequency"],
                results["pxx"],
                results["pyy"],
                results["gain"],
                results["phase"],
                results["coherence"],
                results["avg_abp"],
                results["avg_cbfv"],
                options,
            )
        )
    elif method == "point-estimate":
        results.update(
            point_estimate(
                results["frequency"],
                results["pxx"],
                results["pyy"],
                results["gain"],
                results["gain_norm"],
                results["phase"],
                results["coherence"],
                options["point_estimate_frequency"],
            )
        )

    return results


def cspline(frequency, values, point_frequency):
    frequency = frequency[~numpy.isnan(values)]
    values = values[~numpy.isnan(values)]
    cs = scipy.interpolate.CubicSpline(frequency, values)
    return cs(point_frequency)


def point_estimate(frequency, pxx, pyy, gain, gain_norm, phase, coherence, point_estimate_frequency):
    results = {
        "point_estimate_frequency": point_estimate_frequency,
        "point_estimate_abp_psd": cspline(frequency, pxx, point_estimate_frequency),
        "point_estimate_cbfv_psd": cspline(frequency, pyy, point_estimate_frequency),
        "point_estimate_gain": cspline(frequency, gain, point_estimate_frequency),
        "point_estimate_gain_norm": cspline(frequency, gain_norm, point_estimate_frequency),
        "point_estimate_phase": cspline(frequency, phase, point_estimate_frequency) / (2 * numpy.pi) * 360,
        "point_estimate_coherence": cspline(frequency, coherence, point_estimate_frequency),
    }
    return results


def tfa(frequency, pxx, pyy, gain, phase, coherence, avg_abp, avg_cbfv, options=None):
    if options is None:
        options = dict()

    default_options = {
        "vlf": (0.02, 0.07),
        "lf": (0.07, 0.2),
        "hf": (0.2, 0.5),
        "normalize_cbfv": False,
        "normalize_abp": False,
    }
    options = {**default_options, **options}

    results = frequency_bands_results(
        frequency,
        pxx,
        pyy,
        gain,
        phase,
        coherence,
        options
    )
    if options["normalize_cbfv"]:
        results["gain_vlf_norm"] = results["gain_vlf"]
        results["gain_lf_norm"] = results["gain_lf"]
        results["gain_hf_norm"] = results["gain_hf"]
        results["gain_vlf"] = results["gain_vlf"] * avg_cbfv / 100
        results["gain_lf"] = results["gain_lf"] * avg_cbfv / 100
        results["gain_hf"] = results["gain_hf"] * avg_cbfv / 100
    else:
        results["gain_vlf_norm"] = results["gain_vlf"] / avg_cbfv * 100
        results["gain_lf_norm"] = results["gain_lf"] / avg_cbfv * 100
        results["gain_hf_norm"] = results["gain_hf"] / avg_cbfv * 100

    return results


def linear_interp(time, signal, fs):
    interp_time = _create_interp_time(time, fs)
    return numpy.interp(interp_time, time, signal)


def cubic_spline(time, signal, fs):
    interp_time = _create_interp_time(time, fs)
    cs = scipy.interpolate.CubicSpline(time, signal)
    return cs(interp_time)


def _create_interp_time(time, fs):
    time_resolution = 1 / float(fs)
    return numpy.arange(time[0], time[-1] + time_resolution, time_resolution)


def shift_signal(time, signal, fs, shift_seconds):
    shift_points = int(shift_seconds * fs)
    signal_shifted = numpy.roll(signal, shift_points)
    if shift_points > 0:
        signal_shifted[:shift_points] = numpy.nan
    elif shift_points < 0:
        signal_shifted[shift_points:] = numpy.nan

    return signal_shifted


def _shift_signal(time, signal, fs, shift_seconds):
    shift_points = int(shift_seconds * fs)
    signal_shifted = numpy.roll(signal, shift_points)

    interp_signal = cubic_spline(time, signal, fs)
    if shift_points > 0:
        signal_shifted[:shift_points] = interp_signal[:shift_points]
    elif shift_points < 0:
        signal_shifted[shift_points:] = interp_signal[shift_points:]

    return signal_shifted
