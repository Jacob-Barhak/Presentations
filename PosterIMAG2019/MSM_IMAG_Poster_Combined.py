###############################################################################
# Copyright (C) 2019 Jacob Barhak & Joshua Schertz
# 
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###############################################################################
#
# Feel free to contact the authors
# --
# Jacob Barhak Ph.D.
# jacob.barhak@gmail.com
# http://sites.google.com/site/jacobbarhak/
# 
# Joshua Schertz
# Joshschertz3@gmail.com 
# https://joshschertz.com/
#
# Note that: 
# Jacob Barhak wrote the first poster
# Jacob Barhak and Joshua Schertz wrote the text for the second poster
# 
# Special thanks to:
# Philipp Rudiger, James Bednar, and Jean-Luc Stevens for assisting with 
# panel, bokeh, and holoviews issues.
# without their support and development of pyviz visualization tools, this
# interactive poster would not be possible.


import panel
import bokeh
import base64
import os

ResourceDir = 'Resources'
ExternalResources = 'https://jacob-barhak.github.io/PosterIMAG2019Resources/'

def ConstractImageLinkAnchor(Link, ImageFileName, Text, Width):
    'Constructs html to describe the png image and link it'
    ImageFile = open(ResourceDir+os.sep+ImageFileName,'rb')
    ImageData = ImageFile.read()
    ImageFile.close()
    EncodedImage=base64.b64encode(ImageData)
    RetStr = '<a title="%s" target="_blank" href="%s"><img src="data:image/png;base64,%s" alt="%s" width="%i"/> </a>'%(Text,Link,EncodedImage,Text,Width)
    return RetStr


def ObjectInlineHTML(ExtrnalFileName,Width=1200,Height=700):
    'Encodes html from a file into object'
    RetStr = '<object width="'+str(Width)+'" height="'+str(Height)+'" data="%s">Warning:%s could not be included!</object>'%(ExtrnalFileName,ExtrnalFileName)
    return RetStr
        

BokehDocument = bokeh.document.Document()


PosterCode = panel.panel(ConstractImageLinkAnchor('https://github.com/Jacob-Barhak/Presentations/tree/master/PosterIMAG2019','MSM_IMAG_2019_PosterCode.png','Download the code that generated this poster',100), width=100, height=100)
PosterURL = panel.panel(ConstractImageLinkAnchor('https://jacob-barhak.github.io/InteractivePoster_MSM_IMAG_2019.html','MSM_IMAG_2019_Poster.png','View this poster on the web',100), width=100, height=100)

# The Reference Model Poster

Poster1Title = panel.panel('# The Reference Model is the Most Validated Diabetes Cardiovascular Model Known', width=1200, height=20)
Poster1AuthorName = panel.panel('by: Jacob Barhak', width=1200, height=20)
Poster1AuthorLink = ConstractImageLinkAnchor('http://sites.google.com/site/jacobbarhak/','JacobBarhak_QR_Code.png','Jacob Barhak',30)
Poster1Author = panel.Row(Poster1AuthorLink, Poster1AuthorName)
Poster1Venue = panel.panel('2019 IMAG Multiscale Modeling Consortium (MSM) Meeting 6-7 March 2019', width=1200, height=10)
Poster1NutShell = panel.panel("""## The Reference Model accumulates knowledge from many models and observed outcomes imported from ClinicalTrials.Gov - It now validates against more populations than any other known model!
""", width=1200, height=40)
Poster1Abstract = panel.panel("""### Abstract:
The Reference Model is an ensemble model that accumulates knowledge from multiple other models and validates this knowledge against multiple populations. After connecting to [ClinicalTrials.Gov](https://clinicaltrials.gov/) it has been growing rapidly and has reached the point where it validates against more populations than any other known diabetes model. It currently contains 30 risk models that cooperate and compete and assemble the best model that fits 123 cohorts from 31 populations. This year there was an increase in the number of cohort downloaded from [ClinicalTrials.Gov](https://clinicaltrials.gov/), yet more importantly the cumulative computational gap of knowledge can now be explored interactively via the web. This gap of knowledge shows the difference between the model predication and the results for each clinical trial cohort. The Reference Model accumulates models and data, so being able to show this gap for accumulated knowledge represents our limits to model diabetes. If [ClinicalTrials.Gov](https://clinicaltrials.gov/) would be better standardized, it would be even easier to import data. More data can help narrow this gap that can now be calculated and visualized. Such improvements may lead in the long run for better models that may be used for decision making now reserved for humans. However, to allow such advanced modeling, [ClinicalTrials.Gov](https://clinicaltrials.gov/) data requires standardization.
""", width=1200, height=120)
Poster1TheRefModelDiagram = panel.panel(ConstractImageLinkAnchor('https://simtk.org/projects/therefmodel','TheRefModelDiagram.png','The Reference Model',800), width=800, height=280)
Poster1KeyPoints = panel.panel("""## The Reference Model
* Ensemble model 
* Accumulates knowledge from:
    * Existing models 
    * Observed outcomes
* Focuses on summary data 
    * Avoids individual data restrictions
    * Larger merged population base
* Flexible Import from ClinicalTrials.Gov
* Applicable for other disease processes
* Traceable and reproducible
* Can map our understanding gap
* Currently focuses on diabetic populations
* Output is now available online through this poster
* Protected by U.S. Patent 9,858,390
""", width=400, height=280)
Poster1TheRefModel = panel.Row(Poster1KeyPoints,Poster1TheRefModelDiagram)

Poster1WhatIsNew = panel.panel("""## What is new this year?
* The model imported new populations this year from [ClinicalTrials.Gov](https://clinicaltrials.gov/). 
    * The number of populations/cohorts increased this year from 21 with 91 cohorts to 31 with 123 cohorts. 
    * This number of cohorts is far beyond the previous largest validation of a Diabetes model published - the [Archimedes model](http://care.diabetesjournals.org/content/26/11/3102.long) which reported 18 trials with 74 exercises. 
* Visualization was improved and now interactive visualization of results
    * Users can explore more parameters by hovering over populations
    * Users can explore the populations by changing size of marker and color of marker using predetermined selections
    * Users can explore the optimization of mixture of models using a slider
""", width=1200, height=150)

Poster1Results = panel.panel("""### Results:
Below are simulation results. The top plot shows the gap of our cumulative computational understanding by showing modeling error for cohorts of clinical studies. Each column of circles represents a different study. The vertical axis is the fitness score calculated for the model mixture at a specific iteration. Each circle represents a cohort. The circles at the bottom represent populations that the models used explain better than others. Circles near the top of the plot represent outliers that the current model cannot explain well.
The model mixture is explained at the bottom plot that shows the model mixture during the optimization process that calculates the best model mixture. The circle at the left represent the overall fitness being optimized. Each bar represents the contribution of each model. Models of the same color represent different risk equations and assumptions that cooperate during optimization to explain the same phenomenon. The iteration slider allows exploring the model mixture. When moving the slider, one will see some models loose influence and other gain influence. The best model mixture is seen when the iteration slider is at the highest number.  
""", width=1200, height=120)

Poster1PopulationPlot = panel.panel(ObjectInlineHTML(ExternalResources+'PopulationPlotActive.html'), width=1200, height=600)
Poster1MixturePlot = panel.panel(ObjectInlineHTML(ExternalResources+'ModelMixturePlotsActive.html'), width=1200, height=600)

Poster1Discussion = panel.panel("""### Discussion and Future Efforts:
Although there are visible outliers, the term validation in the context of this model is correct. The Reference Model is a validation model aimed at validating multiple models against as much clinical data as can be accumulated. The fitness score represents a calculated difference between multiple modeled and observed outcomes for 1000 individuals. The average fitness reached in this simulation is 50/1000 which is larger than the 32/1000 published last year - indicating that the 10 populations added this year worsened our computational comprehension gap. It means we need better explanations.
The outlier population seen in the plot is most probably a modeling error related to misinterpretation of outcomes in the [PROactive study follow up clinical trial](https://clinicaltrials.gov/ct2/show/results/NCT02678676). The trial has only one outcome reported aggregating many other outcomes which requires interpretation.
Such misinterpretation will be common since clinical trial reports are still not standardized and therefore there is much room for expert interpretation and the data is not yet computer comprehensible. 
Some efforts are planned to improve such modeling capabilities by:
* Incorporating human expert interpretation
* Standardizing clinical trial data - see the accompanying poster for initial steps
* importing more data from [ClinicalTrials.Gov](https://clinicaltrials.gov/) - with the fast growth of this database, accumulation of knowledge is easier than ever before.
""", width=1200, height=120)


Poster1Technology = panel.panel("""### Technology:
The Python programming language is the main technological enabler behind the model. The new visualization through a web browser is possible using the holoviews library that allows plotting and user interaction with the data. The Reference Model itself runs simulations using the MIcro Simulation Tool (MIST) that runs simulations in parallel on multiple machines on multiple CPUs . It is possible to run those simulations on the Amazon Elastic Compute Cloud. The free Anaconda Python distribution is used to handle all the packages needed and some versions of MIST are available for download under General Public License.
""", width=1100, height=80)
Poster1TechnologyLink = ConstractImageLinkAnchor('https://github.com/Jacob-Barhak/MIST','MISTgithub.png','MIcro Simulation Tool (MIST)',100)
Poster1Technology = panel.Row(Poster1Technology,Poster1TechnologyLink)
   
Poster1ReproducibilityText = panel.panel("""### Reproducibility:
The plots in the poster were created using the script ExploreOptimizationResults_2019_02_24.py on Windows 10 environment with bokeh 1.0.4 holoviews 1.11.2 on Python 2.7.14 64 bit based on simulation results executed on a 64 core compute server with Ubuntu and stored in: MIST_RefModel_2019_02_18_OPTIMIZE.zip
This poster can be accessed and reproduced by code accessible through the QR Images on the left.
""", width=1000, height=60)


Poster1Reproducibility = panel.Row(PosterURL,PosterCode,Poster1ReproducibilityText)
Poster1Acknowledgments = panel.panel("""### Acknowledgments: 
Thanks to Deanna J. M. Isaman who first introduced me to the the idea of accumulating knowledge from clinical trial summary data. Many thanks to Philipp Rudiger who published open source code that assisted in visualization that proved very useful. Many thanks to James Bednar who introduced holoviews that allows easy visualization of this data and to Jean-Luc Stevens for creating holoviews.  
The author has no affiliation to ClinicalTrials.Gov which is an NIH project and just used here for data extraction. 
""", width=1200, height=80)
Poster1References1 = panel.panel("""### Selected Publications:""", width=150, height=100)
Poster1References2 = panel.panel("""### Previous MSM/IMAG Posters:""", width=150, height=100)

Poster1Ref11 = panel.panel(ConstractImageLinkAnchor('https://www.youtube.com/watch?v=vyvxiljc5vA','YouTubePyData2014.png','J. Barhak, The Reference Model for Disease Progression uses MIST to find data fitness. PyData Silicon Valley 2014 held at Facebook Headquarters',50), width=50, height=50)
Poster1Ref12 = panel.panel(ConstractImageLinkAnchor('http://sites.google.com/site/jacobbarhak/home/MODSIM2014_MIST_INSPYRED_Paper_Submit_2014_03_10.pdf','MIST_INSPYRED_MODSIM2014Paper.png','J. Barhak, A. Garrett, Population Generation from Statistics Using Genetic Algorithms with MIST + INSPYRED. MODSIM World 2014, April 15 - 17, Hampton Roads Convention Center in Hampton, VA.',50), width=50, height=50)
Poster1Ref13 = panel.panel(ConstractImageLinkAnchor('http://modsimworld.org/papers/2015/Object_Oriented_Population_Generation.pdf','ObjectOrientedPopulationGenerationMODSIM2015.png','J. Barhak, Object Oriented Population Generation, MODSIM world 2015. 31 Mar - 2 Apr, Virginia Beach Convention Center, Virginia Beach, VA.',50), width=50, height=50)
Poster1Ref14 = panel.panel(ConstractImageLinkAnchor('https://www.youtube.com/watch?v=htGRRjia-QQ','PyTexas2015.png','J. Barhak, The Reference Model for Disease Progression and Latest Developments in the MIST, PyTexas 2015. College Station, TX, 26-Sep-2015',50), width=50, height=50)
Poster1Ref15 = panel.panel(ConstractImageLinkAnchor('http://www.iitsecdocs.com/volumes/2016','IITSECPaper.png','J. Barhak, The Reference Model for Disease Progression Combines Disease Models. I/IITSEC 2016 28 Nov - 2 Dec Orlando Florida.',50), width=50, height=50)
Poster1Ref16 = panel.panel(ConstractImageLinkAnchor('https://doi.org/10.22360/SummerSim.2017.SCSC.022','SummerSim2017.png','J. Barhak, The Reference Model Models ClinicalTrials.Gov. SummerSim 2017 July 9-12, Bellevue, WA.',50), width=50, height=50)
Poster1Ref17 = panel.panel(ConstractImageLinkAnchor('https://youtu.be/Pj_N4izLmsI','PyTexas2017.png','J. Barhak, The Reference Model: A Decade of Healthcare Predictive Analytics with Python, PyTexas 2017, Nov 18-19, 2017, Galvanize, Austin TX.',50), width=50, height=50)
Poster1Ref21 = panel.panel(ConstractImageLinkAnchor('http://sites.google.com/site/jacobbarhak/home/PosterTheReferenceModel_IMAGE_MSM_Submit_2012_10_17.pdf','MSM_IMAG_2012_Poster.png','J. Barhak, The Reference Model for Chronic Disease Progression. 2012 Multiscale Modeling (MSM) Consortium Meeting, October 22-23, 2012',50), width=50, height=50)
Poster1Ref22 = panel.panel(ConstractImageLinkAnchor('http://sites.google.com/site/jacobbarhak/home/PosterTheReferenceModel_IMAG_MSM2013_Submit_2013_09_23.pdf','MSM_IMAG_2013_Poster.png','J. Barhak, The Reference Model for Disease Progression Sensitivity to Bio-Marker Correlation in Base Population - The Reference Model Runs with MIST Over the Cloud!  2013 IMAG Multiscale Modeling (MSM) Consortium Meeting, October 2-3, 2013',50), width=50, height=50)
Poster1Ref23 = panel.panel(ConstractImageLinkAnchor('http://sites.google.com/site/jacobbarhak/home/PosterPopulationGenerationMIST_IMAG_MSM2014_Upload_2014_08_31.pdf','MSM_IMAG_2014_Poster.png','J. Barhak, Generating Populations for Micro Simulation from Publicly Available Data - Populations in the MIST! IMAG Multiscale Modeling (MSM) Consortium Meeting  3-4 September 2014.',50), width=50, height=50)
Poster1Ref24 = panel.panel(ConstractImageLinkAnchor('http://sites.google.com/site/jacobbarhak/home/PosterModularPopulationGeneration_IMAG_MSM2015_Upload_2015_09_03.pdf','MSM_IMAG2015_Poster.png','J. Barhak, The Reference Model Uses Modular Population Generation! Object Oriented Population Generation on the Fly with MIST. IMAG Multiscale Modeling (MSM) Consortium Meeting  9-10 September 2015',50), width=50, height=50)
Poster1Ref25 = panel.panel(ConstractImageLinkAnchor('http://sites.google.com/site/jacobbarhak/home/PosterImportClinicalTrialsGov_IMAG_MSM2017_Upload_2017_03_18.pdf','MSM_IMAG2017_Poster.png','J. Barhak, The Reference Model Interface with ClinicalTrials.Gov  , IMAG Multiscale Modeling (MSM) Consortium Meeting March 22-24, 2017 @ NIH, Bethesda, MD.',50), width=50, height=50)
Poster1Ref26 = panel.panel(ConstractImageLinkAnchor('http://sites.google.com/site/jacobbarhak/home/Poster_IMAG_MSM2018_Map_Upload_2018_03_17.pdf','MSM_IMAG_2018_Poster.png','J. Barhak, The Reference Model Visualizes Gaps in Computational Understanding of Clinical Trials, 2018 IMAG Futures Meeting March 21-22, 2018 @ NIH, Bethesda, MD',50), width=50, height=50)

Poster1References =  panel.Row(Poster1References1, Poster1Ref11, Poster1Ref12, Poster1Ref13, Poster1Ref14, Poster1Ref15, Poster1Ref16, Poster1Ref17, Poster1References2, Poster1Ref21, Poster1Ref22, Poster1Ref23, Poster1Ref24, Poster1Ref25, Poster1Ref26)

Poster1 = panel.Column(Poster1Title ,Poster1Author, Poster1Venue, Poster1NutShell, Poster1Abstract, Poster1TheRefModel, Poster1WhatIsNew, Poster1Results, Poster1PopulationPlot, Poster1MixturePlot, Poster1Discussion, Poster1Technology, Poster1Reproducibility, Poster1Acknowledgments, Poster1References)

# Clinical Unit Mapping Poster

Poster2Title = panel.panel('# Clinical Unit Mapping for Standardization of ClinicalTrials.Gov', width=1200, height=20)
Poster2AuthorNames = panel.panel('by: Jacob Barhak and Joshua Schertz', width=440, height=20)
Poster2AuthorLink1 = ConstractImageLinkAnchor('http://sites.google.com/site/jacobbarhak/','JacobBarhak_QR_Code.png','Jacob Barhak',30)
Poster2AuthorLink2 = ConstractImageLinkAnchor('https://joshschertz.com/','JoshWeb.png','Joshua Schertz',30)
Poster2Author = panel.Row(Poster2AuthorLink1, Poster2AuthorLink2, Poster2AuthorNames)
Poster2Venue = panel.panel('2019 IMAG Multiscale Modeling Consortium (MSM) Meeting 6-7 March 2019', width=500, height=10)
Poster2NutShell = panel.panel("""## Units in ClinicalTrials.Gov are not standardized, ClincialUnitMapping.com provides a solution
""", width=500, height=30)
Poster2AbstractText = panel.panel("""### Abstract:
ClinicalTrials.Gov now accumulates information from over quarter of a million trials with over 10% recording trial results. It is now a [U.S. Law](https://www.gpo.gov/fdsys/pkg/PLAW-110publ85/pdf/PLAW-110publ85.pdf#page=82) to upload many clinical trials to this fast growing database. Data from this database can be extracted in XML format and used for modeling. The Reference Model, for example, extracts population baseline statistics and trial results. However, the database is based on textual input and although scrutinized by humans, it is currently designed for human comprehension rather than computer comprehension. Specifically, non standardized units prevent machine comprehending associated numbers. On 7 Feb 2019 all 34,751 trials with results were downloaded and unit fields were indexed and analyzed. There were 23,733 different units detected. This is a clear sign that standardization is required. We used some machine learning and Natural Language Processing algorithms to organize the data for easier processing by humans. We then created the web site: ClinicalUnitMapping.com to help standardize the units so that many models can process data in this valuable database. If units are standardized, the valuable numerical data in this database can become machine comprehensible.
""", width=500, height=250)

Poster2ProcessingDiagram =  panel.panel(ConstractImageLinkAnchor('https://clinicalunitmapping.com/','ClinicalUnitProcessDiagram.png','Clinical data Processing diagram',700), width=700, height=420)

Poster2Abstract = panel.Row(panel.Column (Poster2Author, Poster2Venue, Poster2NutShell, Poster2AbstractText),Poster2ProcessingDiagram)


Poster2KeyPoints = panel.panel("""## Solution Key Points:
* A web site was created to allow multiple users to view and map the units
* The web site is accessible thought [ClinicalUnitMapping.com](https://clinicalunitmapping.com/)
#### User capabilities:
* The user sees similar units clustered together and can switch clusters
* The user can see how many times the unit is used
* The user can see the contexts associated with a unit
* The user can view clinical trials that use each unit
* The user can map a unit to other suggested units
    * Clinical Data Interchange Standards Consortium [(CDISC)](https://www.cdisc.org/) units are suggested for mapping
    * User can see CDISC-UCUM synonyms
    * Close units are bunched together in display
* The user can ignore suggestions and provide their own mapping
#### Solution Construction:
* The solution is based on python technologies that include:
    * Indexing
    * Natural Language Processing (NLP)
    * Unsupervised machine learning
    * Visualization
    * Database and web deployment
 
""", width=400, height=400)

Poster2WebSiteStaticImage = panel.panel(ConstractImageLinkAnchor('https://clinicalunitmapping.com/','ClinicalUnitMappingScreenShot.png','ClinicalUnitMapping.com web site',780), width=800, height=400)

Poster2KeyElements = panel.Row(Poster2WebSiteStaticImage, Poster2KeyPoints)


Poster2NLP = panel.panel("""### Natural Language Processing (NLP)
Units were evaluated for text proximity using two techniques developed in the Python programming language, including:

* TfidfVectorizer and cosine_similarity in scikit-learn library using 3-6 character n-grams
* difflib.SequenceMatcher method to calculate similarity ratio

CDISC units were processed and 4008 unique units were chosen. A similarity matrix of size 23,733 x (23,733 + 4008) was constructed. The similarity to the right shows the most used units.

### Machine Learning - Clustering
To improve user experience and allow the user to see similar units bunched together, unsupervised machine learning was applied using MiniBatchKMeans from the scikit-learn Python library.

Clustering was performed multiple times with different variations of the similarity matrix. Each unit was classified according to combined clusters considering each run - thus creating a splintering effect that ensured close units stay close. Then small clusters were eliminated by reattaching their units to the closest unit in a larger cluster. Ultimately, 129 clusters were created.
""", width=600, height=250)

Poster2MachineLearningDiagram = (panel.panel(ConstractImageLinkAnchor('https://scikit-learn.org/stable/modules/generated/sklearn.cluster.MiniBatchKMeans.html','MultipleClusters.png','clustering algorithm executed multiple times',600), width=600, height=150))

Poster2DiagramNLP = panel.panel(ObjectInlineHTML(ExternalResources+'UnitProximityHeatMap.html',600,600), width=600, height=600)

Poster2WebSiteDevelopmentText = panel.panel("""### Web Site Development
The units were stored in a SQLite3 relational database. For demonstration purposes, a reduced database of only a few clusters was used as a base for the web site.
The web site was developed using the Python Flask library and was deployed in a DigitalOcean instance.
An administration system allows the management of multiple users, enabling a collaborative mapping effort.
""", width=600, height=100)

Poster2Development = panel.Row(panel.Column(Poster2NLP, Poster2MachineLearningDiagram, Poster2WebSiteDevelopmentText),Poster2DiagramNLP)

Poster2WebSite = panel.panel(ObjectInlineHTML('https://clinicalunitmapping.com/'), width=1200, height=700)

Poster2Discussion = panel.panel("""### Discussion and Future Efforts
The goal is to solve the unit standardization problem, so that numbers can be imported easily into computer models and automated conversion to units of choice would be easy. Currently such calculations involve manual intervention and are a source of possible error. Once data is standardized, data that is currently machine readable will become machine comprehensible. Since ClinicalTrials.Gov is the largest database of clinical trials known, tapping into the knowledge stored there has great potential, and standardizing units may be only the first step. Current efforts are to expand this unit standardization project with the intention to contribute to Unified Medical Language System [(UMLS)](https://www.nlm.nih.gov/research/umls/) through contribution to Clinical Data Interchange Standards Consortium [(CDISC)](https://www.cdisc.org/)  with collaboration with  Simulation Interoperability Standards Organization [(SISO)](https://www.sisostds.org/). 
""", width=1200, height=120)

Poster2ReproducibilityText = panel.panel("""### Reproducibility:
Code and data for this work are archived in the file: AnalyzeCT_2019_03_02.zip. Web site database was created using the database PartUnitsDB_2018_12_26.db that was created in a previous version of the code and data archived in the files: AnalyzeCT_GOV_Code_2019_01_16.zip , StudiesWithResults_Downloaded_2018_04_20.zip.
This poster can be accessed and reproduced by code accessible through the QR Images on the left.
""", width=400, height=100)
Poster2Acknowledgments = panel.panel("""### Acknowledgments: 
* Thanks to CDISC consortium help
* Thanks to NIH persons who helped and specifically to: 
    * Nick Ide from NLM ClinicalTrials.Gov team on advice to process the site
    * Erin E Muhlbradt from NCI for advice on CDISC unit data
""", width=600, height=80)
    

Poster2ReferencesTitle = panel.panel("""### Selected Publications:""", width=150, height=50)    

Poster2Ref11 = panel.panel(ConstractImageLinkAnchor('https://doi.org/10.22360/SummerSim.2017.SCSC.022','SummerSim2017.png','J. Barhak, The Reference Model Models ClinicalTrials.Gov. SummerSim 2017 July 9-12, Bellevue, WA.',50), width=50, height=50)
Poster2Ref12 = panel.panel(ConstractImageLinkAnchor('https://youtu.be/Pj_N4izLmsI','PyTexas2017.png','J. Barhak, The Reference Model: A Decade of Healthcare Predictive Analytics with Python, PyTexas 2017, Nov 18-19, 2017, Galvanize, Austin TX.',50), width=50, height=50)
Poster2Ref13 = panel.panel(ConstractImageLinkAnchor('https://www.sisostds.org/DesktopModules/Bring2mind/DMX/API/Entries/Download?Command=Core_Download&EntryId=47969&PortalId=0&TabId=105','SISO_2018.png','Jacob Barhak, Chris Myers, Leandro Watanabe, Lucian Smith, Maciek Jacek Swat , Healthcare Data and Models Need Standards. Simulation Interchangeability Standards Organization (SISO) 2018 Fall Innovation Workshop.  9-14 Sep 2018 Orlando, Florida.',50), width=50, height=50)
Poster2Ref14 = panel.panel(ConstractImageLinkAnchor('http://co.mbine.org/system/files/COMBINE_2018_Barhak.pdf','COMBINE_2018.png','Jacob Barhak, Python Based Standardization Tools for ClinicalTrials.Gov. Combine 2018 . Boston University. October 8-12, 2018.',50), width=50, height=50)
Poster2Ref15 = panel.panel(ConstractImageLinkAnchor('https://www.sisostds.org/DigitalLibrary.aspx?Command=Core_Download&EntryId=49580','SISO_SIW2019.png','Jacob Barhak, Josh Schertz - Natural Language Processing and Web Tools for Mapping Units from ClinicalTrials.Gov - Simulation Interchangeability Standards Organization (SISO) 2019 Simulation Innovation Workshop.  11 - 15 February 2019 Orlando, Florida.',50), width=50, height=50)

Poster2References =  panel.Row(Poster2ReferencesTitle, Poster2Ref11, Poster2Ref12, Poster2Ref13, Poster2Ref14, Poster2Ref15)


Poster2ReproducibilityAndAcknowledgments = panel.Row(PosterURL,PosterCode,Poster2ReproducibilityText,panel.Column(Poster2Acknowledgments,Poster2References))

Poster2 = panel.Column(Poster2Title, Poster2Abstract, Poster2KeyElements, Poster2Development, Poster2WebSite, Poster2Discussion, Poster2ReproducibilityAndAcknowledgments)

TitleHTML = 'MSM/IMAG 2019 meeting Interactive Poster'

PosterSelectorTab = panel.layout.Tabs (
                                        ('Poster 1: The Reference Model is the Most Validated Diabetes Cardiovascular Model Known',Poster1),
                                        ('Poster 2: Clinical Unit Mapping for Standardization of ClinicalTrials.Gov',Poster2),
                                      )

DocumentForOutput = PosterSelectorTab._get_root(BokehDocument)

Html = bokeh.embed.file_html(DocumentForOutput, bokeh.resources.CDN, TitleHTML)

OutFile = open('InteractivePoster_MSM_IMAG_2019.html','w')
OutFile.write(Html)
OutFile.close()

