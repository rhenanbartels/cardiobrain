from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QDialogButtonBox


class AboutHampelDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            self.setPalette(parent.palette())
            self.setStyleSheet(parent.styleSheet())

        self.setWindowTitle("About the Adapted Hampel Filter")
        self.resize(700, 600)

        layout = QVBoxLayout(self)

        text_browser = QTextBrowser(self)
        text_browser.setOpenExternalLinks(True)
        text_browser.setMarkdown(HAMPEL_DESCRIPTION_MD)
        text_browser.setStyleSheet("""
            QTextBrowser {
                background-color: black;
                border: none;
                color: #b0b0b0;
            }
        """)
        layout.addWidget(text_browser)

        buttons = QDialogButtonBox(QDialogButtonBox.Close)
        buttons.rejected.connect(self.reject)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)


HAMPEL_DESCRIPTION_MD = """
# How it works

The Hampel filter is a **robust, local outlier detector**. It identifies samples
that are inconsistent with their neighbourhood and replaces them with a local
median. Unlike a conventional mean-and-standard-deviation filter, it is much
less affected by the outliers it is designed to detect.

In CardioBrain, the filter is applied to physiological signals such as **mean
arterial blood pressure (ABP)** and **cerebral blood-flow velocity (CBFV)**. Its
purpose is to reduce isolated artifacts while preserving the shape and
physiological variability of the original signal.

For each sample `x[i]`, the filter examines a centred, sliding window around
that sample. At the beginning and end of a signal, the window is shortened so
that edge samples are also evaluated.

1. **Local reference** — Calculate the median `m[i]` of the samples in the
   window.
2. **Robust spread** — Calculate the median absolute deviation (MAD):

   ```text
   MAD[i] = median(abs(x[j] - m[i]))
   ```

3. **Outlier test** — Convert the MAD to a standard-deviation-like scale and
   compare the sample with its local reference:

   ```text
   abs(x[i] - m[i]) > k * 1.4826 * MAD[i]
   ```

   A sample that satisfies this condition is marked as an artifact.
4. **Correction** — Short artifact segments are replaced by linear
   interpolation between the nearest valid samples before and after the
   segment. Segments at a signal boundary or longer than three samples are not
   interpolated.

The median and MAD make the detection decision based on the local structure of
the signal, rather than on a global average. This is particularly useful when
the signal changes over time.

## Additional transition detection

The adapted implementation also analyses the **first difference** between
consecutive samples:

```text
Delta x[i] = x[i + 1] - x[i]
```

This second check detects abrupt transitions that may not be extreme in
absolute amplitude. When a transition is classified as an outlier, the two
samples adjacent to that transition are included in the artifact mask and are
then handled by the same linear-interpolation step.

## Iterative passes

The filter can perform more than one pass. After a pass, it evaluates the
corrected signal again, allowing artifacts that were masked by a neighbouring
artifact to be detected in a later pass. Processing stops early when a pass
finds no additional outliers.

The filter uses a window of 9 samples, performs up to two passes, and analyses
both signal amplitude and abrupt transitions. The available CardioBrain presets
change the detection threshold:

| Preset | Threshold | Behaviour |
| --- | ---: | --- |
| **Light** | 7 | Most conservative; detects only the most pronounced artifacts. |
| **Medium** | 5 | Balanced sensitivity for general use. |
| **Strong** | 3 | Most sensitive; detects smaller deviations, but may also flag legitimate rapid changes. |

The names **Light**, **Medium**, and **Strong** are clear and intuitive for
users. They describe the intensity of artifact removal rather than the numeric
threshold, which is useful because a lower threshold makes the filter more
aggressive.

## What the threshold means

The threshold `k` controls how far a sample must be from its local median to
be considered an outlier:

- A **lower** threshold detects more deviations, but may remove legitimate
  physiological changes.
- A **higher** threshold is more conservative, but may leave some artifacts
  uncorrected.

The threshold is expressed in MAD-based robust units, not in ordinary global
standard deviations.

## Important considerations

- The Hampel filter is a signal-cleaning aid, not a substitute for visual or
  clinical review.
- A genuine, rapid physiological event can resemble an artifact, especially
  when the threshold is too low or the window is too short.
- The corrected output should be interpreted together with the original signal
  and the detected-artifact information whenever available.

"""
