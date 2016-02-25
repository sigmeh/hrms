HRMS is a high resolution analytical toolkit for processing data obtained from mass spectrometry experiments (with current emphasis on ruthenium-based complexes). 

The program (python 2.7) is started by navigating to the main directory in which the files are located and typing `python start_hrms.py`. 

This script checks for an active python localhost server, with the option to kill python server processes not spawned from the current directory. 
If applicable, a new server is started by calling `hrms_server.py`. 
The server is set to open the `hrms` script in a browser window, which loads `hrms.html` and the accompanying `hrms.js` and `hrms.css` files. 

CSV files (exported from Thermo Xcalibur software) are placed into the 'data_files' folder directly. 

Filenames can be manually typed or selected from a menu that calls `show_files.py`. 

The 'Format Data' function calls `format.py` to format the csv data and save it for further processing. 

The 'Show Full' function invokes `show.py` to process and visualize spectral data. Zoom functionality is achieved by drawing boxes over target areas of interest in the spectrum. 
Releasing the mouse calls `show.py` once again to process the data, save it using matplotlib, and load the new figure into the DOM. 

The 'Find Ru' function attempts to identify the locations in the spectrum where ruthenium is present, by analyzing its diagnostic isotopic distribution, and returning
the peak clusters it has found (sorted by relative intensity). 

The 'Analyze Peak' function (under development) is intended as a more fine-tuned analysis tool to identify candidate chemical constitutions based on 
presumed molecular fragments. The fragment list can be expanded by adding a Name and Formula for each new entry. The `add_frag.py` script accomplishes this by 
calculating the combined exact masses of the major isotopes for each constituent atom, saving this data, and appending the new fragment to the list. 

All python script files are located in the 'cgi-bin' folder. Mass reference and fragments files are located in the 'ref' folder. 
Example csv data is located in the 'data_files' folder. 
Javascript and css files are located in the 'static' folder. 


