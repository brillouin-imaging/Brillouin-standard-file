# Definition of subtypes and features in version 0.2 of the brim file format

The purpose of defining subtypes is to allow specific techniques to define additional groups, arrays, or attributes (generally called "features") to store technique-specific data and metadata.

For example, a VIPA spectrometer may define a way to store raw data (a camera image for each spectrum), together with the parameters used to reconstruct spectra from those images.

As a general rule:
- a new subtype should be defined in this file
- the subtype name might include a version (e.g. "SinglePoint_VIPA_v0.1")
- the definition should include a short description of the intended use
- the definition **must** consist of a list of features defined in this file

Requiring new subtypes to use existing (or newly defined) features allows existing software to interpret those additional features, even when the subtype itself is not recognized.

## Subtypes:

### SinglePoint_VIPA_v0.1

This subtype is intended for storing data generated with a point-scanning confocal system coupled to a VIPA spectrometer. It assumes that each spectrum in the `/Data_{n}/PSD` array comes from one or more 2D camera images.

It must contain the following features:
- 2DArray_per_spectrum (array)
- Spectral_line (optional array)

## Features - groups:

## Features - arrays:

### 2DArray_per_spectrum 
Standardized storage of 2D raw camera images under `/Data_{n}/Raw_data` and/or `/Data_{n}/Calibration/Raw_data`.
The primary use case is data from a point-scanning VIPA spectrometer, but any dataset where each spectrum maps to a 2D (or 1D) raw array can use this feature.

Let each camera image have dimensions MxN (order: y, x). If the raw data are 1D, set M = 1 (i.e. the dimensions must be 1xN).

For storage under `/Data_{n}/Raw_data`, the `2DArray_per_spectrum` array must match the spatial dimensions of `/Data_{n}/PSD` (1D or 3D, depending on whether `Sparse` is true; additional PSD dimensions are not allowed). Its last two dimensions must be MxN. Optionally, it may include one extra dimension before MxN to account for repeated acquisitions of the same image that are averaged into a single spectrum.

For storage under `/Data_{n}/Calibration/Raw_data`, add {m} groups to mirror the structure in `/Data_{n}/Calibration`. Under each of these {m} groups, add a `2DArray_per_spectrum` array with the first dimension matching the first dimension of `/Data_{n}/Calibration/{m}` and the last two dimensions equal to MxN. An additional dimension may be added before MxN in the case of multiple raw spectra acquired per calibration spectrum.

### Spectral_line
An array to store the coordinates of the spectral line used to determine the 1D (uncalibrated) spectrum from the `2DArray_per_spectrum`. The last dimension must have 4 elements, corresponding to the y,x coordinates of the start and end of the line (i.e., y_start, x_start, y_end, x_end).

It can be stored under `/Data_{n}/Calibration/Raw_data/{m}`, in which case the first dimension must match the first dimension of `/Data_{n}/Calibration/Raw_data/{m}/2DArray_per_spectrum`. If the additional dimension indicating replicates is present there, it may be omitted here under the assumption that the spectral line is the same for all replicates. If the first dimension is omitted, the spectral line is assumed to be the same for all calibration spectra.

In addition, it can optionally be stored under `/Data_{n}/Analysis_{m}`; in that case it must have the same spatial dimensions as `/Data_{n}/PSD` (which may be omitted if the spectral line is the same for all spectra).

It may have an attribute `Linewidth`, which indicates the thickness of the line in pixels (if not specified, it defaults to 1).

If `Spectral_line` is not present, it is assumed to correspond to a horizontal line with the same thickness as the image height; i.e., an average along the first (vertical) dimension is performed to obtain the spectrum from the 2D array.

## Features - attributes:
