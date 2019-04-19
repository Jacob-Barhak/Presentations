###############################################################################
# Copyright (C) 2019 Jacob Barhak
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
# Aaron Garrett 
# aaron.lee.garrett@gmail.com 
# http://sites.wofford.edu/garrettal/
# 
#
# Note that: 
# Jacob Barhak wrote all presentations
# Aaron Garrett collaborated on Evolutionary Computation
# Joshua Schertz is responsible for web work for ClinicalUnitMapping.Com
# 
# Special thanks to:
# Philipp Rudiger, James Bednar, and Jean-Luc Stevens for assisting with 
# panel, bokeh, and holoviews issues.
# without their support and development of pyviz visualization tools, this
# interactive presentation would not be possible.


import bokeh
import panel
import base64
import os
import sys

EmbedVideo = False
if len(sys.argv)>1:
    EmbedVideo = 'EmbedVideo' in sys.argv[1:]

ImageDir = 'Images'
CommonResourceDir = 'https://jacob-barhak.github.io/CommonResources/'
ExternalResourcesIMAG2019 = 'https://jacob-barhak.github.io/PosterIMAG2019Resources/'



def CovertFileToData(FileName):
    "Convert file to data that can be used in html"
    DataFile = open(FileName,'rb')
    Data = DataFile.read()
    DataFile.close()
    EncodedData=base64.b64encode(Data)
    return EncodedData
    

def ConstractImageLinkAnchor(Link, ImageFileName, Text, Width):
    'Constructs html to describe the png image and link it'
    EncodedImage=  CovertFileToData (ImageDir+os.sep+ImageFileName)
    RetStr = '<a title="%s" target="_blank" href="%s"><img src="data:image/png;base64,%s" alt="%s" width="%i"/> </a>'%(Text,Link,EncodedImage,Text,Width)
    return RetStr




def ObjectInlineHTML(ExtrnalFileName,Width=1200,Height=700):
    'Encodes html from a file into object'
    RetStr = '<object width="'+str(Width)+'" height="'+str(Height)+'" data="%s">Warning:%s could not be included!</object>'%(ExtrnalFileName,ExtrnalFileName)
    return RetStr

def VideoInlineHTML(ExtrnalFileName,Width=1200,Height=700, EmbedVideo = EmbedVideo):
    'Encodes html from a file into video'
    if EmbedVideo:
        ExtrnalData = CovertFileToData(ExtrnalFileName)
        RetStr = '<Video width="%i" height="%i" controls>   <source src="%s" type="video/mp4">  Warning:%s could not be included! </Video>'%(Width, Height, 'data:video/mp4;base64,'+ExtrnalData,ExtrnalFileName)
    else:
        RetStr = '<Video width="%i" height="%i" controls>   <source src="%s" type="video/mp4">  Warning:%s could not be included! </Video>'%(Width, Height, ExtrnalFileName,ExtrnalFileName)
    return RetStr

        

BokehDocument = bokeh.document.Document()


PresentationURL = panel.panel('This presentation can be accessed on the web through [This Link](https://jacob-barhak.github.io/SISO_ENGTAM2019.html)', width=600, height=600)

PresentationTitle = panel.panel('# The Reference Model for Disease Progression & Clinical Unit Standardization ', width=1000, height=80, margin = (0,0,0,0))
PresentationVenue = panel.panel("""ENGTAM Webinar 7th May 0219
""", width=200, height=40, margin = (0,0,0,0))

PresentationVenueFigure = panel.panel(ConstractImageLinkAnchor('https://www.sisostds.org/StandardsActivities/StudyGroups/ENGTAMSSG.aspx','logo_lg.png','SISO ENGTAM',200), width=200, height=40, margin = (0,0,0,0))

PresentationHeader = panel.Row ( PresentationTitle,  panel.Column(PresentationVenueFigure, PresentationVenue, margin = (0,0,0,0)), margin = (0,0,0,0) )


Section0Title = panel.panel('# Motivation: Computer Automation of Human Reasoning?', width=1000, height=40)
Section0Author = panel.panel('by: [Jacob Barhak](http://sites.google.com/site/jacobbarhak/)', width=200, height=30)

Section0Header =  panel.Row(Section0Title, Section0Author)

Section0ChronologyFigure = panel.panel(ConstractImageLinkAnchor('https://en.wikipedia.org/wiki/Computer_chess','ComputerInfluenceDiagram.png','Towards Computer Automation of Human tasks - Main sources Wikipedia Computer Chess and Wikipedia self-driving car',1000), width=1000, height=500)



Section0 = panel.Column(Section0Header, Section0ChronologyFigure)


Section2Title = panel.panel('# Generating Populations Using Evolutionary Computation', width=1000, height=40)
Section2Author = panel.panel('by: [Jacob Barhak](http://sites.google.com/site/jacobbarhak/), [Aaron Garret](http://sites.wofford.edu/garrettal/)', width=200, height=30)

Section2Header =  panel.Row(Section2Title, Section2Author)

Section2PopulationGenerationText = panel.panel("""
## Why Generate Populations?

&nbsp; * Clinical trials ** do not expose individual data ** due to privacy restrictions. 

&nbsp; * Instead trials ** publish statistics with inclusion and exclusion criteria ** such as age distribution.

&nbsp; 

&nbsp; * We create artificial populations that ** mimic these published statistics **.

&nbsp; * Tools that can help with this are the [MIcro Simulation Tool (MIST)](https://github.com/Jacob-Barhak/MIST) that uses [Inspyred](https://pythonhosted.org/inspyred/)

""", width=600, height=130)


Section2PopulationGenerationVideo1 = panel.panel(VideoInlineHTML(CommonResourceDir+'PopulationGeneration_Small.mp4',600,450), width=600, height=450)
Section2PopulationGenerationVideo2 = panel.panel(VideoInlineHTML(CommonResourceDir+'InspyredMIST_Small.mp4',600,380), width=600, height=380)

Section2PopulationGeneration = panel.Row(panel.Column(Section2PopulationGenerationText, Section2PopulationGenerationVideo2), Section2PopulationGenerationVideo1)


## The Population Generation Secion

Section2EvolutionaryComputationText = panel.panel("""## Evolutionary Computation (EC)
                                                                  
Using the [Inspyred library](https://pythonhosted.org/inspyred/) we can generate solutions that match the statistics. 

Each solution is a populations, so we are dealing with a population of populations.

&nbsp;

The EC solution walks through these main stages of a Genetic Algorithm:

&nbsp;

(1) **Generation:** A population of random solutions is generated. 

(2) **Evaluation:** Where the fitness score is calculated for each solution.

(3) **Selection:** Where the best solutions are ranked and selected to represent the next generation.

(4) **Variation:** Where mutation and crossover operators create another generation of solutions.

(5) **Termination:** where a stopping criteria is checked - if not stopped, go back to step 2.

(6) **Post termination:** the most fitting solution is considered as the answer.

""", width=600, height=400)

Section2EvolutionaryComputationVideo = panel.panel(VideoInlineHTML(CommonResourceDir+'EvolutionaryComputation_Small.mp4',600,500), width=600, height=500)

Section2EvolutionaryComputation = panel.Row(Section2EvolutionaryComputationText,Section2EvolutionaryComputationVideo)

Section2ResultsStep2Figure =  ObjectInlineHTML(CommonResourceDir+'HoloviewsPlot.html',Width=1300,Height=1000)

Section2SlideSelectorTab = panel.layout.Tabs (
                                        ('Population Generation', Section2PopulationGeneration),
                                        ('Evolutionary Computation', Section2EvolutionaryComputation),
                                      )

Section2 = panel.Column(Section2Header, Section2SlideSelectorTab)


# The Reference Model Section

Section3Title = panel.panel('# The Reference Model for Disease Progression', width=1000, height=40)
Section3Author = panel.panel('by: [Jacob Barhak](http://sites.google.com/site/jacobbarhak/)', width=200, height=30)
Section3Header = panel.Row(Section3Title,Section3Author)


Section3KeyPoints = panel.panel("""### Key Points
                                
&nbsp; * Ensemble model 

&nbsp; * Currently focuses on diabetic populations

&nbsp; * Models Cardiovascular disease and mortality processes

&nbsp; * Accumulates knowledge from:
    
&nbsp;&nbsp;&nbsp;&nbsp; - Existing models/assumptions - currently 30
    
&nbsp;&nbsp;&nbsp;&nbsp; - Observed outcomes - from 123 cohorts from 31 populations
    
&nbsp; * Focuses on summary data 

&nbsp;&nbsp;&nbsp;&nbsp; - Avoids individual data restrictions
    
&nbsp;&nbsp;&nbsp;&nbsp; - Larger merged population base
    
&nbsp; * Flexible Import from ClinicalTrials.Gov

&nbsp; * Traceable and reproducible

&nbsp; * Can map our understanding gap

&nbsp; * Output is now available online through this presentation

&nbsp; * Protected by U.S. Patent 9,858,390

&nbsp; * Uses High Performance Computing (HPC)

&nbsp; * Uses MIST as an engine - based on python

&nbsp;

## The Reference Model now validates against more populations than any other known diabetes model!
""", width=400, height=500)

Section3TheRefModelVideo = panel.panel(VideoInlineHTML(CommonResourceDir+'TheReferenceModelWithOptimize_Small.mp4',800,500), width=800, height=500)
Section3TheRefModel = panel.Row(Section3KeyPoints,Section3TheRefModelVideo)



Section3ResultsText = panel.panel("""### Results:
                                  
The top plot shows the gap of our cumulative computational understanding by showing modeling error for cohorts of clinical studies. The vertical axis is the fitness score - The error of the best model prediction. 

** Circles near the top of the plot represent outliers ** that the current model cannot explain well.

&nbsp;

The model mixture is explained at the bottom plot. The overall fitness is represented as the circle on the left. Each bar represents the influence of each model/assumption on the model for each iteration.
""", width=1200, height=150)

Section3PopulationPlot = panel.panel(ObjectInlineHTML(ExternalResourcesIMAG2019+'PopulationPlotActive.html'), width=1200, height=600)
Section3MixturePlot = panel.panel(ObjectInlineHTML(ExternalResourcesIMAG2019+'ModelMixturePlotsActive.html'), width=1200, height=600)

Section3Discussion = panel.panel("""### Discussion and Future Efforts:
                                 

The outlier population seen in the plot is most probably a modeling error related to misinterpretation of outcomes which requires human interpretation.

Such misinterpretation will be common since clinical trial reports are still not standardized and therefore there is much room for expert interpretation and the data is not yet computer comprehensible. 

Some efforts are planned to improve such modeling capabilities by:

&nbsp; * Incorporating human expert interpretation

&nbsp; * Importing more data from [ClinicalTrials.Gov](https://clinicaltrials.gov/) - with the fast growth of this database, accumulation of knowledge is easier than ever before. 

&nbsp; * Standardizing clinical trial data

&nbsp;

### Further improvement is now mostly limited by rate of standardization 


""", width=1200, height=250)

Section3Results = panel.Column(Section3ResultsText, Section3PopulationPlot, Section3MixturePlot)

Section3SlideSelectorTab = panel.layout.Tabs (
                                        ('The Reference Model', Section3TheRefModel),
                                        ('Results', Section3Results),
                                        ('Discussion', Section3Discussion),
                                      )

Section3 = panel.Column(Section3Header, Section3SlideSelectorTab)



# Clinical Unit Mapping Section

Section4Title = panel.panel('# Clinical Unit Mapping for Standardization of ClinicalTrials.Gov', width=950, height=40)

Section4Author = panel.panel('by: [Jacob Barhak](http://sites.google.com/site/jacobbarhak/) , [Joshua Schertz](https://joshschertz.com/)', width=250, height=30)
Section4Header = panel.Row(Section4Title,Section4Author)


Section4AbstractText = panel.panel("""## Introduction
                                   
&nbsp; * ClinicalTrials.Gov now accumulates information from over 300K trials.

&nbsp;&nbsp;&nbsp;&nbsp; - Over 10% of trials report results. 

&nbsp; * It is now a [U.S. Law](https://www.gpo.gov/fdsys/pkg/PLAW-110publ85/pdf/PLAW-110publ85.pdf#page=82) to upload many clinical trials to this [fast growing database](https://clinicaltrials.gov/ct2/resources/trends). 

&nbsp; * Data from this database can be extracted in XML format and used for modeling. 

&nbsp; * However, the database is based on textual input. 

&nbsp;&nbsp;&nbsp;&nbsp; - Designed for human comprehension rather than computer comprehension. 
 
&nbsp; * On 7 Feb 2019 all 34,751 trials with results had 23,733 different units

&nbsp; * Non standardized units prevent machine comprehension of stored numbers. 

&nbsp; * We created [ClinicalUnitMapping.com](https://clinicalunitmapping.com/) as a tools to help standardize the units

&nbsp;

### If units are standardized, the valuable numerical data in this database can become machine comprehensible.
""", width=500, height=250)

Section4ProcessingDiagram =  panel.panel(ConstractImageLinkAnchor('https://clinicalunitmapping.com/','ClinicalUnitProcessDiagram.png','Clinical data Processing diagram',700), width=700, height=420)

Section4Abstract = panel.Row(Section4AbstractText,Section4ProcessingDiagram)



Section4NLP = panel.panel("""### Natural Language Processing (NLP)
Units were evaluated for text proximity using::

&nbsp; * TfidfVectorizer and cosine_similarity in scikit-learn library using 3-6 character n-grams

&nbsp; * difflib.SequenceMatcher method to calculate similarity ratio

CDISC units were processed and 4008 unique units were chosen. 

A similarity matrix of size 23,733 x (23,733 + 4008) was constructed.

### Machine Learning - Clustering

To improve user experience and allow the user to see similar units bunched together. 

Unsupervised machine learning was applied using the scikit-learn Python library.

Clustering was performed multiple times with different similarity measures to create 129 clusters.

""", width=600, height=220)

Section4MachineLearningDiagram = (panel.panel(ConstractImageLinkAnchor('https://scikit-learn.org/stable/modules/generated/sklearn.cluster.MiniBatchKMeans.html','MultipleClusters.png','clustering algorithm executed multiple times',600), width=600, height=120))

Section4DiagramNLP = panel.panel(ObjectInlineHTML(ExternalResourcesIMAG2019+'UnitProximityHeatMap.html',600,600), width=600, height=600)

Section4WebSiteDevelopmentText = panel.panel("""### Web Site Development
                                             
The units were stored in a SQLite3 relational database. 

For demonstration purposes, a reduced database was used as a base for the web site.

The web site was developed using the Flask library.

An administration system allows multiple user management, enabling a collaborative mapping effort.
""", width=600, height=100)

Section4Development = panel.Row(panel.Column(Section4NLP, Section4MachineLearningDiagram, Section4WebSiteDevelopmentText),Section4DiagramNLP)




Section4KeyPoints = panel.panel("""## Solution Key Points:
                                
&nbsp; * A web site was created to allow multiple users to view and map the units

&nbsp; * The web site is accessible thought [ClinicalUnitMapping.com](https://clinicalunitmapping.com/)

#### User capabilities:

&nbsp; * The user sees similar units clustered together and can switch clusters

&nbsp; * The user can see how many times the unit is used

&nbsp; * The user can see the contexts associated with a unit

&nbsp; * The user can view clinical trials that use each unit

&nbsp; * The user can map a unit to other suggested units

&nbsp;&nbsp;&nbsp;&nbsp; - Clinical Data Interchange Standards Consortium [(CDISC)](https://www.cdisc.org/) units are suggested for mapping
    
&nbsp;&nbsp;&nbsp;&nbsp; - User can see CDISC-UCUM synonyms
    
&nbsp;&nbsp;&nbsp;&nbsp; - Close units are bunched together in display
    
&nbsp; * The user can ignore suggestions and provide their own mapping

#### Solution Construction:

&nbsp; * The solution is based on python technologies that include:
    
&nbsp;&nbsp;&nbsp;&nbsp; - Indexing
    
&nbsp;&nbsp;&nbsp;&nbsp; - Natural Language Processing (NLP)
    
&nbsp;&nbsp;&nbsp;&nbsp; - Unsupervised machine learning
    
&nbsp;&nbsp;&nbsp;&nbsp; - Visualization
    
&nbsp;&nbsp;&nbsp;&nbsp; - Database and web deployment
    
 
""", width=400, height=600)

Section4WebSiteStaticImage = panel.panel(ConstractImageLinkAnchor('https://clinicalunitmapping.com/','ClinicalUnitMappingScreenShot.png','ClinicalUnitMapping.com web site',790), width=800, height=440)

Section4KeyElements = panel.Row(Section4WebSiteStaticImage, Section4KeyPoints)



Section4Discussion = panel.panel("""### Discussion and Future Efforts
The goal is to solve the unit standardization problem. 

Once data is standardized, data that is currently machine readable will become machine comprehensible. 

Standardizing units may be only the first step. 

Current efforts are to expand this unit standardization project with the intention to work with:

&nbsp; * Unified Medical Language System [(UMLS)](https://www.nlm.nih.gov/research/umls/)

&nbsp; * Clinical Data Interchange Standards Consortium [(CDISC)](https://www.cdisc.org/)

&nbsp; * Simulation Interoperability Standards Organization [(SISO)](https://www.sisostds.org/)

""", width=1200, height=120)


Section4SlideSelectorTab = panel.layout.Tabs (
                                        ('Introduction', Section4Abstract),
                                        ('Development', Section4Development),
                                        ('ClinicalUnitMapping.com', Section4KeyElements),
                                        ('Discussion',Section4Discussion),
                                      )


Section4 = panel.Column(Section4Header, Section4SlideSelectorTab)

Section5SummaryText = panel.panel("""                     
## Summary

Python Tools have contributed significantly to exploring clinical data and will continue supporting efforts towards:
    
(1) Analyzing and visualizing healthcare data for human comprehension

(2) Automating human reasoning in health related situations

&nbsp;

### <span style="color:magenta"> We are still very far from computers replacing medical expert reasoning, yet better tools will eventually lead to a computerized personal medical assistant!
></span>
&nbsp;

### Acknowledgments: 

Many thanks to the PyViz team:

&nbsp;&nbsp;&nbsp;- Philipp Rudiger who published very useful open source code that assisted in visualization. 

&nbsp;&nbsp;&nbsp;- James Bednar who introduced the PyViz tools

&nbsp;&nbsp;&nbsp;- Jean-Luc Stevens for creating holoviews

Thanks to Matthew Rocklin for dask support.

Thanks to Deanna J. M. Isaman who first introduced me to the the idea of accumulating knowledge from clinical trial summary data. 

Thanks to John Rice for the fruitful discussions regarding standardization. 

Thanks to CDISC consortium help

Thanks to NIH persons who helped  and specifically to: 
    
&nbsp;&nbsp;&nbsp;- Nick Ide from NLM ClinicalTrials.Gov team on advice to process the site
    
&nbsp;&nbsp;&nbsp;- Erin E Muhlbradt from NCI for advice on CDISC unit data

Thanks to Blaize Berry for discussions regarding NLP

Many thanks to many other open source and Anaconda developers that supported these efforts by answering many questions.

""", width=600, height=500)
    
  
Section5Summary = panel.Row(Section5SummaryText,PresentationURL)
    

    
Section5AdditionalInfo = panel.panel("""
                              
## Reproducibility:
    
This presentation is accessible [here](https://jacob-barhak.github.io/Presentation_SISO_ENGTAM2019.html). The code that generated the presentation can be accessed [here](https://github.com/Jacob-Barhak/Presentations/tree/master/SISO_ENGTAM2019).

This presentation is generated using Python 2.7.15, panel-0.5.0, bokeh-1.1.0rc1 .

The Reference Model: The plots were created using the script ExploreOptimizationResults_2019_02_24.py on Windows 10 environment with bokeh 1.0.4 holoviews 1.11.2 on Python 2.7.14 64 bit based on simulation results executed on a 64 core compute server with Ubuntu and stored in: MIST_RefModel_2019_02_18_OPTIMIZE.zip

Clinical Unit Mapping : Code and data for this work are archived in the file: AnalyzeCT_2019_03_02.zip. Web site database was created using the database PartUnitsDB_2018_12_26.db that was created in a previous version of the code and data archived in the files: AnalyzeCT_GOV_Code_2019_01_16.zip , StudiesWithResults_Downloaded_2018_04_20.zip.

&nbsp;

## Selected publications:

&nbsp;

### Population Generation

* Inspyred library on [GitHub](https://github.com/aarongarrett/inspyred)                                 

* MIcro Simulation Tool (MIST) on [GitHub](https://github.com/Jacob-Barhak/MIST)

* J. Barhak, A. Garrett, Population Generation from Statistics Using Genetic Algorithms with MIST + INSPYRED. MODSIM World 2014, April 15 - 17, Hampton Roads Convention Center in Hampton, VA. [Paper](http://sites.google.com/site/jacobbarhak/home/MODSIM2014_MIST_INSPYRED_Paper_Submit_2014_03_10.pdf)

* J. Barhak  (2015). The Reference Model uses Object Oriented Population Generation. SummerSim 2015. Chicago IL, USA. [Paper](http://dl.acm.org/citation.cfm?id=2874946)

&nbsp;

### The Reference Model

&nbsp;

#### Selected Publications

&nbsp;

* The Reference Model on [SimTK](https://www.simtk.org/projects/therefmodel)

* J. Barhak, The Reference Model for Disease Progression uses MIST to find data fitness. PyData Silicon Valley 2014 held at Facebook Headquarters [Video](https://www.youtube.com/watch?v=vyvxiljc5vA)

* J. Barhak, A. Garrett, Population Generation from Statistics Using Genetic Algorithms with MIST + INSPYRED. MODSIM World 2014, April 15 - 17, Hampton Roads Convention Center in Hampton, VA [Paper](http://sites.google.com/site/jacobbarhak/home/MODSIM2014_MIST_INSPYRED_Paper_Submit_2014_03_10.pdf)

* J. Barhak, Object Oriented Population Generation, MODSIM world 2015. 31 Mar - 2 Apr, Virginia Beach Convention Center, Virginia Beach, VA. [Paper](http://modsimworld.org/papers/2015/Object_Oriented_Population_Generation.pdf)

* J. Barhak, The Reference Model for Disease Progression and Latest Developments in the MIST, PyTexas 2015. College Station, TX, 26-Sep-2015 [Video](https://www.youtube.com/watch?v=htGRRjia-QQ)

* J. Barhak, The Reference Model for Disease Progression Combines Disease Models. I/IITSEC 2016 28 Nov - 2 Dec Orlando Florida [Paper](http://www.iitsecdocs.com/volumes/2016)

* J. Barhak, The Reference Model Models ClinicalTrials.Gov. [SummerSim 2017 July 9-12, Bellevue, WA].(https://doi.org/10.22360/SummerSim.2017.SCSC.022)

* J. Barhak, The Reference Model: A Decade of Healthcare Predictive Analytics with Python, PyTexas 2017, Nov 18-19, 2017, Galvanize, Austin TX. [Video](https://youtu.be/Pj_N4izLmsI)

&nbsp;

#### Evolution through MSM/IMAG Posters

* J. Barhak, The Reference Model for Chronic Disease Progression. 2012 Multiscale Modeling (MSM) Consortium Meeting, October 22-23, 2012 [Poster](http://sites.google.com/site/jacobbarhak/home/SectionTheReferenceModel_IMAGE_MSM_Submit_2012_10_17.pdf)

* J. Barhak, The Reference Model for Disease Progression Sensitivity to Bio-Marker Correlation in Base Population - The Reference Model Runs with MIST Over the Cloud!  2013 IMAG Multiscale Modeling (MSM) Consortium Meeting, October 2-3, 2013 [Poster](http://sites.google.com/site/jacobbarhak/home/SectionTheReferenceModel_IMAG_MSM2013_Submit_2013_09_23.pdf)

* J. Barhak, Generating Populations for Micro Simulation from Publicly Available Data - Populations in the MIST! IMAG Multiscale Modeling (MSM) Consortium Meeting  3-4 September 2014 [Poster](http://sites.google.com/site/jacobbarhak/home/SectionPopulationGenerationMIST_IMAG_MSM2014_Upload_2014_08_31.pdf)

* J. Barhak, The Reference Model Uses Modular Population Generation! Object Oriented Population Generation on the Fly with MIST. IMAG Multiscale Modeling (MSM) Consortium Meeting  9-10 September 2015 [Poster](http://sites.google.com/site/jacobbarhak/home/SectionModularPopulationGeneration_IMAG_MSM2015_Upload_2015_09_03.pdf)

* J. Barhak, The Reference Model Interface with ClinicalTrials.Gov  , IMAG Multiscale Modeling (MSM) Consortium Meeting March 22-24, 2017 @ NIH, Bethesda, MD. [Poster](http://sites.google.com/site/jacobbarhak/home/SectionImportClinicalTrialsGov_IMAG_MSM2017_Upload_2017_03_18.pdf)

* J. Barhak, The Reference Model Visualizes Gaps in Computational Understanding of Clinical Trials, 2018 IMAG Futures Meeting March 21-22, 2018 @ NIH, Bethesda, MD. [Poster](http://sites.google.com/site/jacobbarhak/home/Section_IMAG_MSM2018_Map_Upload_2018_03_17.pdf)

* J. Barhak, The Reference Model is the most validated diabetes cardiovascular model known. MSM/IMAG meeting. IMAG Multiscale Modeling (MSM) Consortium Meeting March 6-7, 2019 @ NIH, Bethesda, MD . [Poster](https://jacob-barhak.github.io/InteractivePoster_MSM_IMAG_2019.html)


&nbsp;

### Clinical Unit Mapping

* J. Barhak, The Reference Model Models ClinicalTrials.Gov. [SummerSim 2017 July 9-12, Bellevue, WA].(https://doi.org/10.22360/SummerSim.2017.SCSC.022)

* J. Barhak, The Reference Model: A Decade of Healthcare Predictive Analytics with Python, PyTexas 2017, Nov 18-19, 2017, Galvanize, Austin TX. [Video](https://youtu.be/Pj_N4izLmsI)

* J. Barhak, C. Myers, L. Watanabe, L. Smith, M. J. Swat , Healthcare Data and Models Need Standards. Simulation Interchangeability Standards Organization (SISO) 2018 Fall Innovation Workshop.  9-14 Sep 2018 Orlando, Florida [Presentation](https://www.sisostds.org/DesktopModules/Bring2mind/DMX/API/Entries/Download?Command=Core_Download&EntryId=47969&PortalId=0&TabId=105)

* J. Barhak, Python Based Standardization Tools for ClinicalTrials.Gov. Combine 2018 . Boston University [Poster](http://co.mbine.org/system/files/COMBINE_2018_Barhak.pdf)

* J. Barhak, J. Schertz, Clinical Unit Mapping for Standardization of ClinicalTrials.Gov . MSM/IMAG meeting. IMAG Multiscale Modeling (MSM) Consortium Meeting March 6-7, 2019 @ NIH, Bethesda, MD . [Poster](https://jacob-barhak.github.io/InteractivePoster_MSM_IMAG_2019.html)

* J. Barhak, J. Schertz, Clinical Unit Mapping for Standardization of ClinicalTrials.Gov . MSM/IMAG meeting. IMAG Multiscale Modeling (MSM) Consortium Meeting March 6-7, 2019 @ NIH, Bethesda, MD . [Poster](https://jacob-barhak.github.io/InteractivePoster_MSM_IMAG_2019.html)


""", width=1200, height=1000)
    
    
    
 
Section5SlideSelectorTab = panel.layout.Tabs (

                                        ('Additional Information', Section5AdditionalInfo),
                                        ('Summary', Section5Summary),
                                        
                                        )


Section5 =  Section5SlideSelectorTab





TitleHTML = 'AnacondaCon 2019 presentation by Jacob Barhak'

SectionSelectorTab = panel.layout.Tabs (
                                        ('Preface',Section0),
                                        ('(1) Modeling Populations',Section2),
                                        ('(2) The Reference Model',Section3),
                                        ('(3) ClinicalUnitMapping.com',Section4),
                                        ('(4) Summary',Section5),
                                        )
   


                               
                                        
Presentation = panel.Column(PresentationHeader, SectionSelectorTab)
Presentation.save('Presentation_SISO_ENGTAM2019.html')       

