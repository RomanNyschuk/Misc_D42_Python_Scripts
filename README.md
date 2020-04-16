[Device42](http://www.device42.com/) is a comprehensive data center infrastructure management software.

This repository hosts miscellaneous python scripts to interact with device42 APIs.


### Script Provided
-----------------------------
   * create_switchport_report_from_apis.py : Creates a CSV report for all switchports with 3 columns: Switch description, port name and devices
   * create_device_report_from_apis.py : Creates a CSV report for all devices with 6 columns: Name, CPU Count, Cores, CPU Speed, Memory and Hardware
   * clone_device.py    :   Create cloned devices based on an existing device

### Download and Installation
-----------------------------
To utilize the Misc_D42_Python_Scripts script, Python 3.5+ is required. The following Python Packages are required as well:

* certifi==2019.11.28
* requests==2.23.0

These can all be installed by running `pip install -r requirements.txt`.

### Usage
-----------------------------

Follow the instructions in individual scripts. Instructions have been added as comments in the scripts provided.
