# Proposal for metadata in version 0.1 of the BLS file format

The following metadata are defined with the aim of making Brillouin measurements interpretable and reproducible; they are based on the [Consensus Statement on Brillouin Light Scattering Microscopy of Biological Materials](https://doi.org/10.48550/arXiv.2411.11712).
The units used the same conventions defined in the [main document](BLS_file_specs.md).

## Structure:

|   /Brillouin\_data/Metadata

|   ---- ---- /Experiment

|   ---- ---- /Optics

|   ---- ---- /Brillouin

|   ---- ---- /Acquisition

|   ---- ---- /Spectrometer

|   ---- ---- ---- /IRF [1D float] (optional)


## Detailed description of the metadata in the file:
- **‘/Experiment’** (group) has the following attributes:
  - **‘Datatime’ [string]** (optional): a [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html): time when the experiment was started 
  - **‘Temperature’ [float]** (optional): the temperature measured as close as possible to the sample
  - **‘Temperature\_uncertainty’ [float]** (optional)
  - **‘Sample’ [string]** (optional): description of the sample being imaged
  - **‘Info’ [string]** (optional): any additional description that the user can input to describe the experiment
- **‘/Optics’** (group) has the following attributes:
  - **‘Wavelength’ [float]**: wavelength of the laser used for the measurements
  - **‘Power’ [float]**: total optical power on the sample
  - **‘Resolution_x’ [float]**
  - **‘Resolution_y’ [float]**
  - **‘Resolution_z’ [float]**
  - **‘Lens\_NA’ [float]**: the numerical aperture of the lens that is used for imaging (detection)
  - **‘Lens\_NA\_illum’ [float]** (optional): the numerical aperture of the lens that is used for illumination (if different from detection) 
  - **‘Immersion\_medium’ [enum{other, air, water, oil}]**: the immersion medium used for the objective lens
  - **‘Objective\_model’ [string]** (optional): the description of the objective lens being used, including the manufacturer and magnification
  - **‘Laser\_model’ [string]** (optional)
- **‘/Brillouin’** (group) has the following attributes:
  - **‘Signal\_type’ [enum {other, spontaneous, stimulated, time\_resolved}]**
  - **‘Scattering\_angle’ [float]**: the average scattering angle (i.e. between the optical axes of the illumination and detection); 180deg corresponds to backscattering
  - **‘Phonons\_measured’ [enum{other, longitudinal-like, transverse-like, longitudinal-&transverse-like}]**
  - **‘Polarization\_probed\_analyzed’ [enum{other, V-H, H-V, H-H, V-V, V-Unpolarized, Circular-Circular}]**
  - **‘Shift_precision’ [float]**
  - **‘Width_precision’ [float]**
- **‘/Acquisition’** (group) has the following attributes:
  - **‘Scanning\_strategy’ [enum {other, point\_scanning, line\_scanning, lightsheet, time\_resolved}]**
  - **‘Acquisition\_time’ [float]**: the time that takes to acquire a single ‘unit’, which is different depending on the scanning strategy (i.e. point, line, plane, A-line, etc.)
- **‘/Spectrometer’** (group) containing the dataset:
  - **IRF [float]** (optional): a 1D array containing the impulse response function of the spectrometer. It must have an attribute ‘Frequency’ [float] (with the corresponding ‘Frequency_units’ [string]) of the same length, containing the frequency axis.  

  And the attributes:
    - **‘Type’ [enum{other, VIPA, Fabry_Perot, stimulated, heterodyne, time\_domain, impulsive}]**
    - **‘Resolution’ [float]**    
    - **‘Detector\_type’ [enum{other, EM-CCD, CCD, sCMOS, PMT, balanced, single_PD, single_APD}]** (optional)
    - **‘Detector\_model’ [string]** (optional)
    - **‘Additional filter’ [string]** (optional): description of any additional filter present in the spectrometer (e.g. vapor cell, Lyot stop, etc..)
    - **‘Confocal\_pinhole\_diameter’ [float]** (optional)
