from __future__ import annotations

import numpy as np


WINDOW_SIZE = 9
HAMPEL_PASSES = 2
MAX_INTERPOLATED_BEATS = 3
MAD_TO_STANDARD_DEVIATION = 1.4826


def _hampel_mask(
    signal: np.ndarray,
    window_size: int,
    threshold: float,
) -> np.ndarray:
    """Detect samples that exceed their local MAD-based threshold."""
    half_window = window_size // 2
    detected_mask = np.zeros(signal.size, dtype=bool)
    for sample_index, sample_value in enumerate(signal):
        start_index = max(0, sample_index - half_window)
        end_index = min(signal.size, sample_index + half_window + 1)
        local_values = signal[start_index:end_index]
        local_median = float(np.median(local_values))
        median_absolute_deviation = float(
            np.median(np.abs(local_values - local_median))
        )
        robust_scale = MAD_TO_STANDARD_DEVIATION * median_absolute_deviation
        deviation = abs(float(sample_value) - local_median)
        detected_mask[sample_index] = (
            deviation > threshold * robust_scale
        )
    return detected_mask


def _contiguous_segments(mask: np.ndarray) -> list[tuple[int, int]]:
    """Return marked segments as inclusive-start, exclusive-end pairs."""
    segments = []
    start_index: int | None = None
    for sample_index, is_marked in enumerate(mask):
        if is_marked and start_index is None:
            start_index = sample_index
        elif not is_marked and start_index is not None:
            segments.append((start_index, sample_index))
            start_index = None
    if start_index is not None:
        segments.append((start_index, len(mask)))
    return segments


def _interpolate_segments(
    signal: np.ndarray,
    outlier_mask: np.ndarray,
) -> np.ndarray:
    """Linearly interpolate short, interior outlier segments."""
    corrected_signal = signal.copy()
    for start_index, end_index in _contiguous_segments(outlier_mask):
        segment_length = end_index - start_index
        if segment_length > MAX_INTERPOLATED_BEATS:
            continue
        if start_index == 0 or end_index == signal.size:
            continue
        corrected_signal[start_index:end_index] = np.linspace(
            corrected_signal[start_index - 1],
            corrected_signal[end_index],
            segment_length + 2,
        )[1:-1]
    return corrected_signal


def _pass_mask(
    signal: np.ndarray,
    window_size: int,
    threshold: float,
    use_derivative: bool,
) -> tuple[np.ndarray, np.ndarray]:
    """Combine amplitude and abrupt-transition detections."""
    amplitude_mask = _hampel_mask(signal, window_size, threshold)
    if not use_derivative or signal.size <= 1:
        return amplitude_mask, amplitude_mask

    derivative = np.diff(signal)
    derivative_mask = _hampel_mask(derivative, window_size, threshold)
    transition_mask = np.zeros(signal.size, dtype=bool)
    transition_mask[:-1] |= derivative_mask
    transition_mask[1:] |= derivative_mask
    detected_mask = amplitude_mask | transition_mask
    correction_mask = amplitude_mask.copy()
    for start_index, end_index in _contiguous_segments(transition_mask):
        if not amplitude_mask[start_index:end_index].any():
            correction_mask[start_index:end_index] = True
    return detected_mask, correction_mask


def hampel_filter(signal: np.ndarray, threshold: float) -> np.ndarray:
    """Detect artifacts and linearly correct short segments in a 1-D signal.

    The filter uses a nine-sample window, amplitude and first-difference
    detection, and up to two passes. Segments longer than three samples or at a
    signal boundary are detected but left unchanged.
    """
    signal = np.asarray(signal, dtype=float)
    if signal.ndim != 1:
        raise ValueError("signal must be a one-dimensional NumPy array.")
    if signal.size == 0:
        return signal.copy()
    if threshold <= 0:
        raise ValueError("threshold must be greater than zero.")

    corrected_signal = signal.copy()
    for _pass_number in range(HAMPEL_PASSES):
        detected_mask, correction_mask = _pass_mask(
            corrected_signal,
            WINDOW_SIZE,
            threshold,
            use_derivative=True,
        )
        if not detected_mask.any():
            break
        corrected_signal = _interpolate_segments(
            corrected_signal,
            correction_mask,
        )
    return corrected_signal


__all__ = ["hampel_filter"]
