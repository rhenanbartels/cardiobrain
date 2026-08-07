import unittest

import numpy as np

from filters.hampel import hampel_filter


class HampelFilterTests(unittest.TestCase):
    def test_preserves_signal_without_outliers(self):
        signal = np.arange(20, dtype=float)

        filtered_signal = hampel_filter(signal, threshold=5)

        np.testing.assert_array_equal(filtered_signal, signal)

    def test_linearly_interpolates_short_internal_artifact(self):
        signal = np.arange(20, dtype=float)
        signal[10] = 1000.0

        filtered_signal = hampel_filter(signal, threshold=5)

        np.testing.assert_allclose(filtered_signal, np.arange(20, dtype=float))

    def test_linearly_interpolates_two_consecutive_artifacts(self):
        signal = np.arange(20, dtype=float)
        signal[10:12] = 1000.0

        filtered_signal = hampel_filter(signal, threshold=5)

        np.testing.assert_allclose(filtered_signal, np.arange(20, dtype=float))

    def test_leaves_artifact_segment_longer_than_three_samples_unchanged(self):
        signal = np.arange(20, dtype=float)
        signal[8:12] = 1000.0

        filtered_signal = hampel_filter(signal, threshold=5)

        np.testing.assert_array_equal(filtered_signal[8:12], signal[8:12])

    def test_leaves_boundary_artifacts_unchanged(self):
        signal = np.arange(20, dtype=float)
        signal[:2] = 1000.0

        filtered_signal = hampel_filter(signal, threshold=5)

        np.testing.assert_array_equal(filtered_signal[:2], signal[:2])

    def test_rejects_non_one_dimensional_signal(self):
        signal = np.zeros((2, 2), dtype=float)

        with self.assertRaisesRegex(ValueError, "one-dimensional"):
            hampel_filter(signal, threshold=5)

    def test_rejects_non_positive_threshold(self):
        signal = np.arange(10, dtype=float)

        with self.assertRaisesRegex(ValueError, "greater than zero"):
            hampel_filter(signal, threshold=0)

    def test_accepts_empty_signal(self):
        signal = np.array([], dtype=float)

        filtered_signal = hampel_filter(signal, threshold=5)

        self.assertEqual(filtered_signal.size, 0)
        self.assertEqual(filtered_signal.dtype, signal.dtype)


if __name__ == "__main__":
    unittest.main()
