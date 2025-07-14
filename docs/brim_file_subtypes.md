# Definition of subtypes and features in version 0.1 of the brim file format

The idea behind defining subtypes is that specific techniques might define additional groups, arrays or attributes (generally called 'features') to store data and metadata which is specific for that technique.

For example a double VIPA spectrometer might define a way to store the raw data (consisting of a camera image for each spectrum), together with the parameters used to reconstruct the spectra from there.

As a general rule:
- a new subtype should be definied in this file
- the definition should include a short description of the intended use
- the definition **must** consist of a list of features defined in this file 

Forcing new subtype to make use of existing (or newly defined) features, allows existing softwares to interpret the additional features, even if they don't recognize the new subtype.

## Subtypes:

### Double_VIPA_Spectrometer

It is indended for storing data generated with a double VIPA spectrometer. It defines the storage of the raw data (consisting of a camera image for each spectrum), together with the parameters used to reconstruct the spectra from there.
It includes:
- group_x
- array_x1
- array_x2
- attribute_y


## Features:

### group_x
A group under ‘/Data_{n}/Raw\_data’ named XX and containing XX
### array_x1
An array with shape N1,N2 containing xx
### array_x1
An array with shape N3,N4 containing xx
### attribute_y
An attributed which can be linked to xx and yy and contains...
