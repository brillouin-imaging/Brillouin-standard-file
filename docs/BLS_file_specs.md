# Proposal for version 0.1 of the BLS file format

## General description:
The BLS file format is designed to store Brillouin spectral data along with the results of its analysis.
While it supports the storage of individual spectra acquired under different conditions, its primary focus is on Brillouin microscopy images.
Brillouin microscopy is a hyperspectral imaging technique, where each pixel in the final 3D image corresponds to a full spectrum. 
Individual spectra are arranged in a flattened structure within the '/data_{n}/PSD' array.
In this format, the first dimension represents the spatial position, while the second dimension contains the spectral information.
The mapping of these spectra to a 3D image is done through the '/data_{n}/Scanning/Cartesian_visualization' array.
Additionally, the '/data_{n}' groups enable the storage of multiple acquisitions, referred to as time points.
These time points are not limited to conventional time-lapse imaging but can also represent variations in experimental conditions, such as temperature, osmolarity, or other environmental factors.

## General features:
- The terminology used in this document is the one of [Zarr](https://zarr-specs.readthedocs.io/en/latest/v3/core/index.html#concepts-and-terminology), even though these specifications only define the structure of the file and are thus not restricted to Zarr
- The specification defines the minimum set of groups/arrays/attributes that must be implemented. More can be added while still complying with the specs
- The exact name of the fields defined by the specification must be used (case sensitive)
- Avoid using symbols that are special characters in popular languages (e.g. '(', '=', '+', etc.) in names of arrays/attributes
- Compression and filters to individual arrays can be used
- If supported by the underlaying storage, links to internal groups/arrays can be used instead of duplicating the data, if needed
- Datetimes must be represented as a string in [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) format
- For arrays that require units an attribute named 'units' that contains the name of the units as a string must be attached to the array; if an attribute (e.g. named 'attribute_x') needs units, one must add another attribute called 'attribute_x_units' at the same hierarchical level and store the name of the unit as a string
- Enums should be stored as string (but preferably the library used to generate the BLS file should still expose enums to the user, to avoids typos in the name of the elements)

## Structure:
|   /

|   /Brillouin\_data

|   ---- /Metadata (defined in ['BLS_file_metadata'](BLS_file_metadata.md))

|   ---- /Data_{n}

|   ---- ---- /PSD

|   ---- ---- /Frequency

|   ---- ---- /Raw\_data (optional)

|   ---- ---- ---- /Index [1D int]

|   ---- ---- ---- /{r}

|   ---- ---- /Scanning

|   ---- ---- ---- /Spatial\_map (optional)

|   ---- ---- ---- ---- /x [1D float] (optional)

|   ---- ---- ---- ---- /y [1D float] (optional)

|   ---- ---- ---- ---- /z [1D float] (optional)

|   ---- ---- ---- /Cartesian\_visualization [3D int]

|   ---- ---- /Parameters [2D (or more) float] (optional)

|   ---- ---- /Timestamp [1D float] (optional)

|   ---- ---- /Analysis\_{m}

|   ---- ---- ---- /Shift\_AS\_{p} [1D (or more) float]

|   ---- ---- ---- /Shift\_S\_{p} [1D (or more) float] (optional)

|   ---- ---- ---- /Width\_AS\_{p} [1D (or more) float]

|   ---- ---- ---- /Width\_S\_{p} [1D (or more) float] (optional)

|   ---- ---- ---- /Amplitude\_AS\_{p} [1D (or more) float]

|   ---- ---- ---- /Amplitude\_S\_{p} [1D (or more) float] (optional)

|   ---- ---- ---- /Offset\_AS\_{p} [1D (or more) float]

|   ---- ---- ---- /Offset\_S\_{p} [1D (or more) float] (optional)

|   ---- ---- ---- /Fit\_error\_AS\_{p} (optional) (same for Stokes)

|   ---- ---- ---- ---- /R2 [1D (or more) float]

|   ---- ---- ---- ---- /RMSE [1D (or more) float]

|   ---- ---- ---- ---- /Cov_matrix [3D (or more) float]

|   ---- ---- /Calibration (optional)

|   ---- ---- ---- /Index [1D int]

|   ---- ---- ---- /{c} [1D (or more) float]

## Detailed description of the content of the file:
- **‘/’** (root group) must have the following attributes:
  - **‘BLS_version’ [string]**: version of the specification that the current file is complying with (e.g. ‘0.1’); the version must follow the conventions of [semantic versioning](https://semver.org/)
  - **‘SubTypeID’ [uint32]**: identifier of the specific subtype BLS file that is being used. ID 0x00000000 to 0x7FFFFFFF have to be agreed upon and defined on the specifications, while 0x80000000 to 0xFFFFFFFF are free to use as custom subtypes; default is 0
  - **‘Authors’ [string]** (optional): information about the authors of the file (e.g. name, contact, etc...)
  - **‘Lab’ [string]** (optional): information about lab and/or institute where the data was generated
  
All the following groups are inside the ‘/Brillouin\_data’ group:
- **‘/Data_{n}’** (group) containing the data of the current timepoint; it doesn’t need to be necessarily a timepoint in a timelapse, it could also be a measurement at different temperature or whatever fits under the concept of subsequent measurements under different conditions (defined in the ‘Conditions’ attribute). It can have any of the attributes defined in ‘Metadata’ (if different), with the naming style ‘GroupName.AttributeName’; specifically, defining the ‘Experiment.Datetime’ attribute is recommended. If the BLS contains only a single timepoint, this group must still be defined and called ‘Data_0’. Additionally it might have the following attributes:
  - **‘Conditions_name’ [string]** (optional): contains as many elements as parameters that are varied experimentally. If used ‘Conditions_name_units’ should be also defined
  - **‘Conditions’ [string]** (optional): the values for the parameters used to acquired the data contained in this specific '/Data_{n}' group
- **‘/Data_{n}/PSD’ [float]**: 2D (or more) array where the first dimension corresponds to the number of spatial positions in the sample (*N\_points*) and the second dimension contains the spectral information. Optionally can have more dimensions, when for each voxel in the sample multiple spectra are acquired (e.g. angle resolved measurements); the new dimensions must be inserted in-between (i.e. the “voxels” and spectral dimensions must always be the first and the last, to make the broadcast of the ‘Frequency’ array easier) 
- **‘/Data_{n}/Frequency’ [float]**: it must have the same size as ‘PSD’ or fewer dimensions; in the latter case it will be broadcasted to the size of ‘PSD’ (starting from the right), similarly to [Numpy broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html); e.g. if ‘Frequency’ is 1D  and ‘PSD’ is 2D, ‘Frequency’ must have the same length as the second dimension of ‘PSD’ (in this case the result of broadcasting is assuming that the frequency axis is the same for all the spatial positions). 
- **‘/Data_{n}/Raw\_data’** (optional group):  
  - **‘Index’ [int]**: zero-based index (<*N\_points*) which associates the first dimension of the ‘PSD’ array to ‘/Data_{n}/Raw\_data/{r}’ (the idea being that the same raw data can be used to generate multiple spectra, for example in the line-scanning)
  - **‘{r}’** (optional group or array): the actual content depends on the technique; it might be better defined for a specific ‘SubTypeID'.
- **‘/Data_{n}/Scanning/Spatial\_map’** (optional): group containing the 1D float arrays (with length *N\_points*) ‘x’, ‘y’ and ‘z’ which refer to the coordinates on the sample at which the spectrum was acquired; if any of the ‘x’, ‘y’ and ‘z’ arrays is omitted it is considered filled with zeros. The units must be attached to the ‘Spatial\_map’ and not to the individual ‘x’, ‘y’, ‘z’ arrays (i.e. the units are the same for all 3 arrays). If ‘Cartesian\_visualization’ is defined, ‘Spatial\_map’ can be omitted
- **‘/Data_{n}/Scanning/Cartesian\_visualization’ [3D int]** contains an index which associates the position in the 3D grid to the first dimension in ‘PSD’ (thus obviously the index must be smaller than *N\_points*). The order of dimensions is ZYX and the 3 dimensions must always be present, where the unused dimensions can be set to 1. If the scanning is done in non-cartesian coordinates -1 can be included to fill the "empty" pixels

  It must also contains the following attributes:
    - **‘element_size’ [float]**: array with 3 elements containing the pixel size for z, y, x 
    - **‘element_size_units’ [string]**: string containing the units for all the dimensions in element_size (e.g. 'um') 
  
  N.B. in principle, the 3D grid could be reconstructed from the array '/Scanning/Spatial\_map' (if present), but it is good to have it always defined to avoid computing the assignments of spectra to 3D coordinates every time and also to allow for different way for reconstructing the image (in case it is useful) 
- **‘/Data_{n}/Parameters’ [float]** (optional): in case ‘PSD’ has more than 2 dimensions (let’s call the number of dimensions of ‘PSD’ *n\_PSD*), ‘Parameters’ must have *n\_PSD-1* dimensions, where the first *n\_PSD-2* dimensions correspond to the parameters at which the spectra were acquired and the last one contains *n\_PSD-2* elements storing the actual values of the parameters (e.g. for an angle-resolved measurement the angle at which the spectrum was acquired). It must also have the following attributes:
    - **‘Name’ [string]**: a 1D array with size *n\_PSD*-2 containing the names of the parameters including the unit (e.g. ‘Angle_deg’)
- **‘/Data_{n}/Timestamp’ [float]** (optional): milliseconds from the beginning of the experiment, as defined in the ‘datetime’ attribute of the current ‘Data_{n}’ group (if defined, or arbritary otherwise) when the current spectrum was acquired
- **‘/Data_{n}/Analysis\_{m}’** (group) contains the results of the analysis on the spectral data; the index 'm' allows for the case of multiple pipelines being performed on the same data (in that case a group for each of them must be created). It contains the following arrays. All arrays must be 1D with the length *N\_points*. The arrays containing the parameters extracted from the spectra (i.e. Shift\_AS\_{i}, etc.) can have more dimensions, in order to match the dimensions in the PSD array. They can optionally have both the results for anti-Stokes and Stokes, in case both are present (the raccomandation is to use the average between the two, when displaying the image). Note that the way one should think about the PSD array and the arrays in 'Analysis\_{m}' is like a table containing a list of voxels acquired in the sample with their corresponding Brillouin shift, width, etc.
  - **‘Shift\_AS\_{p}’ [float]**: p=0,… if multiple peaks are fitted
  - **‘Width\_AS\_{p}’ [float]**: p=0,… if multiple peaks are fitted
  - **‘Amplitude\_AS\_{p}’ [float]**: p=0,… if multiple peaks are fitted
  - **‘Offset\_AS\_{p}’ [float]**: p=0,… if multiple peaks are fitted
  - **‘Fit\_error\_AS\_{p}’** (optional group) containing the following arrays:
    - **‘RMSE’ [float]** (optional)
    - **‘R2’ [float]** (optional)
    - **‘Cov_matrix’ [float]** (optional): the last two dimensions define the matrix
  - Additional optional arrays 
  
  It also contains the following attributes:
  - **‘Fit\_model’ [enum:{other, Lorentzian, DHO, Voigt}]**
  - **‘Corrections’ [string]**: text describing any corrections that is applied to the fitted data (e.g. for NA broadening, deconvolution, etc.)
  
- **‘/Data_{n}/Calibration’** (optional group) it contains the following arrays; N.B. if the whole calibration group (or an indivual {m} array) is the same as one in another Data_{n}, one could create a reference to that instead of repeating the data; that implies that, when writing to the file, one must be careful if there are multiple links pointing at the same object:
  - **‘Index’ [int]**: zero-based index which associates the first dimension of the ‘PSD’ array to ‘/Data_{n}/Calibration/{c}’ (the idea being that, if multiple calibration spectra are acquired while imaging, we need to know which calibration data is used for the current spectrum)
  - **‘{c}’ [float]**: a 1D array containing the c-th calibration spectrum (in relation to ‘/Data_{n}/Calibration/index’); in case there are multiple calibration materials (or reference frequency, e.g. in case of EOMs) the name of the array must be ‘c:j’, where j=0,… correspond to one material (frequency); it can optionally have an attribute **‘Timestamp’ [float]** corresponding to the milliseconds elapsed from ‘/Data_{n}/Calibration/Datetime’

  It also contains the following attributes:
  - **‘Description’ [string]** (optional): it describes how the calibration is performed
  - **‘Temperature’ [float]** (optional): the temperature of the calibration material (if relevant)
  - **‘Datatime’ [string]** (optional): a [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) representation of the time when the (first) calibration spectrum was acquired
  - **‘Shift\_m’ [string]** (optional): Brillouin shift of the m-th calibration material (or frequency); the name must be ‘Shift\_0’ in case a single material is used.
  - **‘FSR’ [float]** (optional): The free spectral range of the spectrometer (in case it is a parameter that is used for calibration)