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
# Anselm Blumer 
# ablumer@cs.tufts.edu
# https://engineering.tufts.edu/cs/people/faculty/anselm-blumer
#
# Olaf Dammann
# olaf.dammann@tufts.edu
# https://medicine.tufts.edu/faculty/olaf-dammann
#
# Note that: 
# Jacob Barhak wrote all presentations
# Aaron Garrett collaborated on Evolutionary Computation
# Joshua Schertz is responsible for web work for ClinicalUnitMapping.Com
# Olaf Dammann & Anselm Blumer worked on Population Disease Occurrence Models
# 
# Special thanks to:
# Philipp Rudiger, James Bednar, and Jean-Luc Stevens for assisting with 
# panel, bokeh, and holoviews issues.
# without their support and development of pyviz visualization tools, this
# interactive presentation would not be possible.


import bokeh
import matplotlib
matplotlib.use('agg')
import panel
import base64
import os
import re
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



def EnhanceMarkDown(Text, Size=11, DPI=300):
    "Replaces enclosed text to images using LaTex - useful for equations"
    def MatchReplacer (MatchObj):
        "Function to replace each Latex with an image"
        EquationData = MatchObj.group(0)[3:-3]
        # we assume no $ is in the data
        SizeDataIndex = EquationData.find('$')
        if SizeDataIndex != -1:
            SizeToUse = int(EquationData[(SizeDataIndex+1):])
            EquationDataToUse = '$'+EquationData[:SizeDataIndex]+'$'
        else:
            SizeToUse = Size
            EquationDataToUse = '$'+EquationData+'$'
        print ('Processing LaTeX: ' + EquationDataToUse + ' Size: ' + str(SizeToUse))
        # Strip the token from the curly braces
        ReplacementImage = panel.pane.LaTeX(EquationDataToUse, size=SizeToUse, dpi=DPI)
        # write the image data
        ImageData = ReplacementImage._img()
        # Encode the image as html
        EncodedImage=base64.b64encode(ImageData)
        RetStr = '<img src="data:image/png;base64,%s" height="%i"/>'%(EncodedImage, SizeToUse) 
        return RetStr
    # First go over the sub string and separate LaTeX elements
    ReplacedInputString = re.sub(r'~~~.*?~~~', MatchReplacer, Text)
    return ReplacedInputString


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


PresentationURL = panel.panel(ConstractImageLinkAnchor('https://jacob-barhak.github.io/AnacondaCon_2019.html','AnacondaCon_2019_Presentation.png','View this presentation on the web',600), width=600, height=600)

PresentationTitle = panel.panel('# &nbsp; Clinical Data Modeling with Python', width=800, height=40, margin = (0,0,0,0), background='#5f259f', style = {'color':'#ffffff'})
PresentationVenue = panel.panel("""3rd - 5th
    
April 2019
""", width=200, height=40, margin = (0,0,0,0), background='#5f259f', style = {'color':'#ffffff'})

PresentationVenueFigure = panel.panel(ConstractImageLinkAnchor('https://anacondacon.io/','AnacondaConLogo.png','AnacondaCon 2019',160), width=160, height=40, margin = (0,0,0,0))

PresentationHeader = panel.Row ( PresentationTitle,  PresentationVenue, PresentationVenueFigure )


Section0Title = panel.panel('# Introduction: How Can Machines Help Improve Healthcare?', width=1000, height=30)
Section0Author = panel.panel('by: [Jacob Barhak](http://sites.google.com/site/jacobbarhak/)', width=200, height=30)

Section0Header =  panel.Row(Section0Title, Section0Author)

Section0ChronologyFigure = panel.panel(ConstractImageLinkAnchor('https://en.wikipedia.org/wiki/Computer_chess','ComputerInfluenceDiagram.png','Towards Computer Automation of Human tasks - Main sources Wikipedia Computer Chess and Wikipedia self-driving car',1000), width=1000, height=500)



Section0AnacondaText = panel.panel("""## The Role of Anaconda in this Automation Process
&nbsp;

### The work presented in this presentation is based on Anaconda and its many libraries:
&nbsp;

| &nbsp;&nbsp;&nbsp; Data Science                                      | &nbsp;&nbsp;&nbsp; Human Interfaces                        | &nbsp;&nbsp;&nbsp; Simulation Tools                          | 
|:---------------------------------------------------------------------|:-----------------------------------------------------------|:-------------------------------------------------------------|
| &nbsp;&nbsp;&nbsp; ** numpy ** - math and statistics                 | &nbsp;&nbsp;&nbsp; ** Jupyter notebook ** - user Interface | &nbsp;&nbsp;&nbsp; ** MIST ** - MIcro Simulation Tool        |
| &nbsp;&nbsp;&nbsp; ** xmllib ** - parsing XML data                   | &nbsp;&nbsp;&nbsp; ** WxPython ** - user Interface         | &nbsp;&nbsp;&nbsp; ** Inspyred ** - Evolutionary Computation |
| &nbsp;&nbsp;&nbsp; ** pandas ** - data management                    | &nbsp;&nbsp;&nbsp; ** PyQt ** - user interface             |                                                              |
| &nbsp;&nbsp;&nbsp; ** sqite3 ** - database                           | &nbsp;&nbsp;&nbsp; ** flask ** - web deployment            |                                                              |
| &nbsp;&nbsp;&nbsp; ** Difflib ** - text diff for NLP                 | &nbsp;&nbsp;&nbsp; ** matplotlib ** - visualization        |                                                              |
| &nbsp;&nbsp;&nbsp; ** scikit-learn ** - machine learning & NLP       | &nbsp;&nbsp;&nbsp; ** Bokeh ** - visualization             |                                                              |
| &nbsp;&nbsp;&nbsp; ** parser ** - creating a modeling language       | &nbsp;&nbsp;&nbsp; ** Holoviews ** - visualization         |                                                              |
| &nbsp;&nbsp;&nbsp; ** dask ** - parallelization                      | &nbsp;&nbsp;&nbsp; ** panel ** - visualization             |                                                              |

&nbsp;
&nbsp;


### Other relevant libraries not in this presentation with past and future use:
&nbsp;

** scipy ** - optimization functions

** sympy ** - symbolic math

** libsbml ** - Systems Biology Markup Language (SBML)

""", width=1000, height=40, css_classes=['td','th','table'])


SectionSelectorTab = panel.layout.Tabs (
                                        ('Motivation: Computer Automation of Human Reasoning',Section0ChronologyFigure),
                                        ('The Role of Anaconda in this Automation Process',Section0AnacondaText),
                                        )

Section0 = panel.Column(Section0Header, SectionSelectorTab)


Section1Title = panel.panel('# Intensive Care Unit Data Visualization Aided by Machine Learning', width=1000, height=30)
Section1Author = panel.panel('by: [Jacob Barhak](http://sites.google.com/site/jacobbarhak/)', width=200, height=30)


Section1Text = panel.panel("""&nbsp; * Machines help humans through Visualization Cues
                           
&nbsp; * Single patient data from Flowsheet, Lab data, and Monitor data for less than 1 day.

&nbsp; * Even a single patient for so little time generates large amounts of data that needs help visualizing.  


&nbsp; * Usupervised Machine Learning and other techniques were used to Detect outliers:
    
&nbsp;&nbsp;&nbsp;&nbsp; - Gaussian Process

&nbsp;&nbsp;&nbsp;&nbsp; - Support Vector Machine (SVM)

&nbsp;&nbsp;&nbsp;&nbsp; - DBSCAN

&nbsp;&nbsp;&nbsp;&nbsp; - Agglomerative Clustering

&nbsp;&nbsp;&nbsp;&nbsp; - Local Outlier Factor

&nbsp;&nbsp;&nbsp;&nbsp; - K Nearest Neighbors

&nbsp;&nbsp;&nbsp;&nbsp; - Filtering using a Window

&nbsp; * Voting was used to give the viewer visual cues by coloring original data and filter outliers.


""", width=1200, height=270)

Section1Plot = panel.panel(ObjectInlineHTML('https://jacob-barhak.github.io/VisualICU.html', 1300), width=1500, height=6000)


Section1Header =  panel.Row(Section1Title, Section1Author)
Section1 = panel.Column(Section1Header, Section1Text, Section1Plot)

Section2Title = panel.panel('# Population Disease Occurrence Models Using Evolutionary Computation', width=1000, height=30)
Section2Author = panel.panel('by: [Jacob Barhak](http://sites.google.com/site/jacobbarhak/), [Aaron Garret](http://sites.wofford.edu/garrettal/), [Anselm Blumer](https://engineering.tufts.edu/cs/people/faculty/anselm-blumer), [Olaf Dammann](https://medicine.tufts.edu/faculty/olaf-dammann)', width=200, height=30)

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

Section2Problem = panel.panel(EnhanceMarkDown("""
##An epidemiological problem solved by population generation. 
&nbsp;
                                              
### Population Disease Occurrence Models: Problem Definition
&nbsp;
                                      
#### Known:

Population of ~~~N=617~~~ preterm infants, where:
    
~~~P_1=32\%~~~ are with Sepsis 

~~~P_2=75\%~~~ get Oxygen 

it was observed that ~~~P_3=47\%~~~ reached the outcome of [Retinopathy of Prematurity (ROP)](https://doi.org/10.1159/000312821)

Odds ratios were: 
    
~~~O_{12} = Odds(Oxygen,Sepsis) = 2.6~~~ 

~~~O_{13} = Odds(ROP,Sepsis) = 2.8~~~

~~~O_{23} = Odds(ROP,Oxygen) = 3.6~~~


&nbsp;
#### To be solved:

A new treatment is introduced that reduces the occurrence of sepsis from ~~~P_1=32\%~~~ to a lower value ~~~P_1^* = 16\%$13~~~. 

Assuming that the odds ratios and the oxygen probability represent biological constraints that do not change, 

what would be the resulting prevalence (percentage) of ROP?                        

"""), width=1200, height=400)



# The Population Generation Secion

Section2EvolutionaryComputationText = panel.panel(EnhanceMarkDown("""## Evolutionary Computation (EC)
                                                                  
Using the [Inspyred library](https://pythonhosted.org/inspyred/) we can generate solutions that match the statistics. 

Each solution is a populations, so we are dealing with a population of populations.

&nbsp;

The EC solution walks through these main stages of a Genetic Algorithm:

&nbsp;

(1) **Generation:** A population of random solutions is generated. 

&nbsp;

(2) **Evaluation:** Where the fitness score is calculated for each solution.

&nbsp;

(3) **Selection:** Where the best solutions are ranked and selected to represent the next generation.

&nbsp;

(4) **Variation:** Where mutation and crossover operators create another generation of solutions.
    
&nbsp;

(5) **Termination:** where a stopping criteria is checked - if not stopped, go back to step 2.

&nbsp;

(6) **Post termination:** the most fitting solution is considered as the answer.

"""), width=600, height=400)

Section2EvolutionaryComputationVideo = panel.panel(VideoInlineHTML(CommonResourceDir+'EvolutionaryComputation_Small.mp4',600,500), width=600, height=500)

Section2EvolutionaryComputation = panel.Row(Section2EvolutionaryComputationText,Section2EvolutionaryComputationVideo)



Section2ResultsStep2Text = panel.panel(EnhanceMarkDown("""## Results

We executed 8 strategies, each 100 simulations on a 64 core server.

The plots below where dots represent population characteristics for a single run and solid lines represent average of the 100 simulations. 

&nbsp;

Results suggest that: When modeling the effect of a hypothetical treatment that drops sepsis from 32% to 8% of the population while keeping odds ratio constraints, 
different models show a change in ROP from **47%** to the range of **(40.9% - 47.5%)** where the most informed model reached **43%**. 

&nbsp;

Full details and discussion will be provided in the [MODSIM world 2019](http://www.modsimworld.org/) paper.

"""), width=1200, height=150)


Section2ResultsStep2Figure =  ObjectInlineHTML(CommonResourceDir+'HoloviewsPlot.html',Width=1300,Height=1000)


Section2ResultsStep2 = panel.Column(Section2ResultsStep2Text,Section2ResultsStep2Figure)


Section2SlideSelectorTab = panel.layout.Tabs (
                                        ('Population Generation', Section2PopulationGeneration),
                                        ('Evolutionary Computation', Section2EvolutionaryComputation),
                                        ('Population Disease Occurrence Models (PopDOM): Problem Definition', Section2Problem),
                                        ('PopDom: Results', Section2ResultsStep2),
                                      )

Section2 = panel.Column(Section2Header, Section2SlideSelectorTab)


# The Reference Model Section

Section3Title = panel.panel('# The Reference Model for Disease Progression', width=1000, height=30)
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

Section4Title = panel.panel('# Clinical Unit Mapping for Standardization of ClinicalTrials.Gov', width=950, height=30)

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

Thanks to Tadashi Kamio for the email correspondence that resulted in ICU visualization work. 

Thanks to the the UCI, Machine Learning Repository for making the ICU data available.

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
    
This presentation is accessible [here](https://jacob-barhak.github.io/AnacondaCon_2019.html). The code that generated the presentation can be accessed [here](https://github.com/Jacob-Barhak/Presentations/tree/master/AnacondaCon2019).

This presentation is generated using Python 2.7.15, panel 0.5.0a3, bokeh 1.1.0dev9 .

Population Disease Occurrence Models: results obtained with:
    
&nbsp;&nbsp;&nbsp;- Laptop computer with 4 cores and Windows 10 deployed by Anaconda (64-bit) with python 2.7.14, dask 0.17.2, bokeh 0.13.0, inspyred 1.0, numpy 1.14.2 , holoviews 1.10.7 

&nbsp;&nbsp;&nbsp;- Compute server with 64 cores, Linux 18.04, Anaconda (64-bit) python 2.7.15, dask 0.19.1, bokeh 0.13.0, inspyred 1.0, numpy 1.15.3, holoviews 1.10.7. The code is stored in the [GitHub repository](https://github.com/Jacob-Barhak/PopDOM)

The Reference Model: The plots were created using the script ExploreOptimizationResults_2019_02_24.py on Windows 10 environment with bokeh 1.0.4 holoviews 1.11.2 on Python 2.7.14 64 bit based on simulation results executed on a 64 core compute server with Ubuntu and stored in: MIST_RefModel_2019_02_18_OPTIMIZE.zip

Clinical Unit Mapping : Code and data for this work are archived in the file: AnalyzeCT_2019_03_02.zip. Web site database was created using the database PartUnitsDB_2018_12_26.db that was created in a previous version of the code and data archived in the files: AnalyzeCT_GOV_Code_2019_01_16.zip , StudiesWithResults_Downloaded_2018_04_20.zip.

&nbsp;

## Selected publications:

### ICU Visualization: 
    
* J. Barhak, Visualization and Pre-Processing of Intensive Care Unit Data Using Python Data Science Tools. MODSIM world 2018. 24-26 Apr. Norfolk,Virginia. [Paper](http://www.modsimworld.org/papers/2018/MODSIM_2018_Barhak.pdf) , [Presentation](http://sites.google.com/site/jacobbarhak/home/BarhakMODSIM_2018_04_25.odp)   [GitHub](https://github.com/Jacob-Barhak/VisICU) ,  [Results](https://jacob-barhak.github.io/VisualICU.html)

&nbsp;

### Population Generation

* Inspyred library on [GitHub](https://github.com/aarongarrett/inspyred)                                 

* MIcro Simulation Tool (MIST) on [GitHub](https://github.com/Jacob-Barhak/MIST)

* Olaf Dammann, Kenneth Chui, Anselm Blumer, (2018) A Causally Naive and Rigid Population Model of Disease Occurrence Given Two Non-Independent Risk Factors, Online Journal of Public Health Informatics [Paper](https://doi.org/10.5210/ojphi.v10i2.9357)

* M. Chen, A. Citil, F. McCabe, K.M. Leicht, J. Fiascone,  C.E.L. Dammann, O. Dammann , (2011). Infection, oxygen, and immaturity: interacting risk factors for retinopathy of prematurity. Neonatology. 99, 125-32.[Paper](https://doi.org/10.1159/000312821)

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
                                        ('(1) ICU Data Visualization',Section1),
                                        ('(2) Modeling Populations',Section2),
                                        ('(3) The Reference Model',Section3),
                                        ('(4) ClinicalUnitMapping.com',Section4),
                                        ('(5) Summary',Section5),
                                        )
                                        
                                        
Presentation = panel.Column(PresentationHeader, SectionSelectorTab)


DocumentForOutput = Presentation._get_root(BokehDocument)

Html = bokeh.embed.file_html(DocumentForOutput, bokeh.resources.CDN, TitleHTML)

OutFile = open('AnacondaCon_2019.html','w')
OutFile.write(Html)
OutFile.close()

