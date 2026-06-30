# Changelog

All notable changes to the `.brim` specification are documented in this file.

## v0.2

### Breaking changes
- Measurement-level metadata overrides in `/Brillouin_data/Data_{n}` are no longer expressed via flattened attributes in `Type.AttributeName` format.
- Per-spectrum timestamp storage is no longer specified as a dedicated `/Data_{n}/Timestamp` dataset.

### Added
- Optional `Metadata` attribute on `/Brillouin_data/Data_{n}` using the same nested JSON-like structure as global metadata in `/Brillouin_data`.
- Hierarchical metadata merge semantics: values in `/Data_{n}` override corresponding global values from `/Brillouin_data`.
- `_arrays` hint list for metadata objects in `/Data_{n}` `Metadata` to indicate that listed values are stored as datasets under `/Data_{n}/Metadata/...`.
- New `/Data_{n}/Metadata` group for per-position metadata arrays (for example `/Data_{n}/Metadata/Experiment/Temperature`).


### Notes for implementers
- Parsers should compute effective metadata per measurement by recursively merging global metadata with measurement-level metadata.
- For any field listed in the `_arrays` attribute of `/Data_{n}` `Metadata`, consumers should read the corresponding dataset from `/Data_{n}/Metadata/...`.
