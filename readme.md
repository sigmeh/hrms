<h4>hrms</h4>

<h5> HRMS is a high resolution analytical toolkit for processing mass spectrometry data. </h5>



![hrms_sample](/media/hrms_sample.png)


Usage:

	$ python start_hrms.py

Checks for active local webserver. 
Loads `hrms.html` in browser window (default).
 
Raw CSV files (from Thermo Xcalibur software) should be placed into the 'data_files' folder. 
Files can be opened from the `Files` button. 

`Format Data`: formats and saves csv data in usable form. 

`Show Full`: visualizes spectral data in the viewing window. 

Zoom functionality: use the mouse to draw a box over the desired part of the spectrum. 

`Find Ru`: automates peak selection processes by scanning the data for ruthenium's characteristic isotopic signatures. 

`Analyze Peak`: (in progress) utilizes a user-defined fragment list to facilitate more accurate compositional analysis. 



