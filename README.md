# brim File Format Specification for Brillouin Microscopy

This repository defines and discusses a standard file format for Brillouin microscopy data.

## What Is Brillouin Microscopy?

Brillouin microscopy is a hyperspectral imaging technique that extends Brillouin spectroscopy to microscopy.
In recent years, it has seen increasing use in biomedical imaging because of its potential to assess the mechanical
properties of biological samples. For background, see reviews such as [Kabakova et al., 2024](https://doi.org/10.1038/s43586-023-00286-z)
and [Prevedel et al., 2019](https://doi.org/10.1038/s41592-019-0543-3).

Different acquisition approaches can be used (for example, spontaneous, stimulated, and time-domain), but all of them
ultimately collect a spectrum for each voxel in an image. A small set of parameters is typically extracted from each
spectrum (for example, Brillouin shift and width) and displayed as color maps.

## Why a Standard File Format?

As Brillouin data production grows across instruments, laboratories, and commercial systems, a common format becomes
essential. The goal is to store both raw and processed Brillouin spectral data, together with the metadata needed to
understand the context of each experiment.

This repository proposes a format that includes the information needed to analyze and interpret Brillouin data in a
consistent way, while remaining flexible enough to support different acquisition approaches and hardware setups.
We expect this standardization to facilitate collaboration, improve cross-study comparisons, and support broader software
development for analysis and visualization.

## Container Format

The proposed format requires a hierarchical structure and the ability to attach metadata to individual elements.

We initially considered [HDF5](https://www.hdfgroup.org/solutions/hdf5/) because it is well established for hierarchical,
self-describing data and is widely supported across scientific fields and programming languages.

However, HDF5 was not originally designed for cloud-native and parallel I/O workflows, both of which are relevant for
Brillouin spectral data. [Zarr](https://zarr.dev/), which is [inspired by principles similar to HDF5](https://medium.com/open-source-science-initiative/why-i-zarr-ee64eb7ffbf8), addresses these limitations.
Based on this and the discussion in [issue #1](https://github.com/brillouin-imaging/Brillouin-standard-file/issues/1),
we recommend Zarr as the container for `.brim` files and plan to fully support Zarr.

## Tools for Reading and Writing `.brim` Files

The following tools support `.brim` data:

- [BrimView](https://biobrillouin.org/brimview/): Web app for visualization and processing.
	Report issues at the [BrimView issue tracker](https://github.com/brillouin-imaging/BrimView/issues).
- [brimfile](https://pypi.org/project/brimfile/): Python package with a simple interface to the latest `.brim` specification.
	Report issues or request features at the [brimfile issue tracker](https://github.com/brillouin-imaging/brimfile/issues).
- [napari plugin](https://napari-hub.org/plugins/brillouin-imaging.html): Open existing `.brim` files in napari.
- [FIJI plugin](https://github.com/brillouin-imaging/brillouin-imaging-fiji): Open existing `.brim` files in FIJI.

## Repository Contents

- [docs/brim_file_specs.md](docs/brim_file_specs.md): Latest `.brim` file format specification.
- [CHANGELOG.md](CHANGELOG.md): Versioned list of specification changes.
- [examples/](examples/): Example files grouped by `.brim` version.

## Community Contributions

Community input is strongly encouraged. Suggestions for extending or refining the specification are welcome, especially
to support data from different setups and workflows.

When proposing changes, please aim to keep the format:

- self-descriptive, so data can be interpreted without additional context;
- consistently structured, so software can extract information reliably and automatically.

To contribute ideas or discuss specific topics, open an issue in the
[repository issue tracker](https://github.com/brillouin-imaging/Brillouin-standard-file/issues).
