GE Healthcare 2019 Presentation
=============================

This project generates the presentation for GE Healthcare in html format

The presentation is generated using the panel python library

The presentation also contains a prototype Sepsis model for technology demonstration purposes

Disclaimer - This Sepsis Model is a prototype assembled quickly to demonstrate modeling capabilities using familiar terminology - more effort is needed for a proper model


USAGE:
------
* python  GE_Healthcare2019.py
* The file Presentation_GE_Healthcare2019.html will be generated

To view the interactive presentation generated by this code visit:
https://jacob-barhak.github.io/Presentation_GE_Healthcare2019.html


INSTALLATION & DEPENDENCIES:
----------------------------
To install:
1. Copy the files in this repository to a directory of choice 
2. Install Anaconda from https://www.anaconda.com/download/
3. install panel: conda install panel

Dependant libraries are: panel, bokeh, some external html files are made with holoviews.



FILES:
------
* GE_Healthcare2019.py : Code that generates the presentation.
* Images : a directory containing images used to generate the presentation.
* Model : Directory Holding the Sepsis model prototype and its results and reports
    * Barhak_GE_Sepsis_Demo.zip - the Sepsis prototype model - open with [MIST](https://github.com/Jacob-Barhak/MIST)
    * Barhak_GE_Sepsis_Demo_WithResults.zip - the Sepsis prototype model after simulations with results - open with [MIST](https://github.com/Jacob-Barhak/MIST)
    * SimulationResultExport.csv - Export of simulation results for the basic scenario with treatment
    * SimulationResultExportWithEC.csv - Export of simulation results for the scenario with treatment and with Evolutionary Computation
    * SimulationResultExportBadTreatmentWithEC.csv - Export of simulation results for the scenario without proper treatment and with Evolutionary Computation
    * Sepsis_Report.txt - Report generated for the basic scenario with treatment
    * Sepsis_EC_Report.txt - Report generated for the scenario with treatment and with Evolutionary Computation
    * Sepsis_EC_BAD-Treat_Report.txt - Report generated for the scenario without proper treatment and with Evolutionary Computation

* Presentation_GE_Healthcare2019.html : The presentation file.
* License.txt : the license file


DEVELOPER CONTACT INFO:
-----------------------

Please pass questions to:


Jacob Barhak Ph.D.

jacob.barhak@gmail.com

http://sites.google.com/site/jacobbarhak/


ACKNOWLEDGEMENTS:
-----------------
Special thanks to:
* Philipp Rudiger
* James Bednar
* Jean-Luc Stevens 

They all assisted with panel, bokeh, and holoviews issues.
without their support and development of PyViz visualization tools, this interactive poster would not be possible.


LICENSE
-------
The GE Healthcare logo is used with permission from GE Healthcare group and not subject to the GPL license - please contact GE Healthcare for usage terms for the GE Healthcare logo. All other files are provided under the GPL license below.

Copyright (C) 2019 Jacob Barhak


This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.