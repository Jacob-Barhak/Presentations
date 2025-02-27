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
#
# Note that: 
# Jacob Barhak wrote all presentations
# Joshua Schertz is responsible for web work for ClinicalUnitMapping.Com
# 
# Special thanks to:
# Philipp Rudiger, James Bednar, and Jean-Luc Stevens for assisting with 
# panel, bokeh, and holoviews issues.
# without their support and development of pyviz visualization tools, this
# interactive presentation would not be possible.



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


TitleHTML = 'PyCon Israel 2019 presentation by Jacob Barhak'

PresentationURL = panel.panel(ConstractImageLinkAnchor('https://jacob-barhak.github.io/Presentation_PyConIsrael2019.html','PyConIsrael2019.png','View this presentation on the web',600), width=600, height=600)

PresentationTitle = panel.panel('# Standardizing Clinical Data with Python ', width=800, height=60, margin = (0,0,0,0))
PresentationVenue = panel.panel("""[Jacob Barhak](http://sites.google.com/site/jacobbarhak/) , [Joshua Schertz](https://joshschertz.com/)

PyCon Israel 3-5 June 2019
""", width=300, height=20, margin = (0,0,0,0))

PresentationVenueFigure = panel.panel(ConstractImageLinkAnchor('https://il.pycon.org/2019/','logo_pyconil_2019.png','PyCon Israel',90), width=100, height=50, margin = (0,0,0,0))

PresentationHeader = panel.Row ( PresentationTitle,  PresentationVenue, PresentationVenueFigure, margin = (0,0,0,0) )


Section0Title = panel.panel('## Motivation: Computer Automation of Human Reasoning', width=1000, height=20)
Section0Author = panel.panel('by: [Jacob Barhak](http://sites.google.com/site/jacobbarhak/)', width=200, height=40)

Section0Header =  panel.Row(Section0Title, Section0Author, margin = (0,0,0,0))

Section0ChronologyFigure = panel.panel(ConstractImageLinkAnchor('https://en.wikipedia.org/wiki/Computer_chess','ComputerInfluenceDiagram.png','Towards Computer Automation of Human tasks - Main sources Wikipedia Computer Chess and Wikipedia self-driving car',1000), width=1000, height=500)



Section0 = panel.Column(Section0Header, Section0ChronologyFigure)



Section0QuestionAndAnswers1 = panel.panel("""# Some Predictions                                                              
## Q: When will computers automate some human medical decision tasks to allow applications such as a computerized personal doctor?  
                                                        
## A: Many tasks of line physicians are already being automated, and that will accelerate. But the "hard" areas of active physical/conversational problem-solving, are far out on the almost unforeseeable horizon at this point.
### <span style="color:green"> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Jeff Shrager, Director of Research, xCures and Adjunct Professor Symbolic Systems Program Stanford University</span>
                                                                
## A: I believe this is already happening, though not explicitly. Currently, patients often look up their symptoms on the internet with inconsistent results.  The challenge for us is to make medical knowledge accessible, understandable and accurate. 
### <span style="color:green"> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Rocky Reston, Chief Medical Informatics Officer, Saperi Systems, Inc. </span>

## A: Technically, we could certainly have a prototype in 5-10 years. The main obstacles will be ethical, professional concerns of reliability and accreditation, philosophical challenges, knowledge management.
### <span style="color:green"> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Olaf Dammann, Professor and Vice Chair, Dept. of Public Health & Community Medicine, Tufts University School of Medicine  </span>

Quoted text was extracted from email conversations and was edited to fit this presentation
                                                              
""", width=1200, height=250)


Section0QuestionAndAnswers2 = panel.panel("""# More Predictions                                                      
## Q: When will computers automate some human medical decision tasks to allow applications such as a computerized personal doctor?                                                  

## A: Probably in about a decade the technology will be mature. However, changing the culture will make adoption of such technology delay for about 8 more years.
### <span style="color:green"> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Bob Armstrong,  Executive Director of the Sentara Center for Simulation and Immersive Learning at Eastern Virginia Medical School  </span>

## A: By 2030, average income Americans will have some form of tele-medicine to diagnose them. Healthcare interventions will be prescribed by AI Expert systems with a human Doctor signature still required. Policy will trail available technology capabilities by ten years.  
### <span style="color:green"> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Richard Boyd, CEO Tanjo , Co-founder & Chair ultisim   </span>
                                                                
Quoted text was extracted from email conversations and was edited to fit this presentation                                                            
""", width=1200, height=250)



Section4AbstractText = panel.panel("""# ClinicalTrials.Gov                                   
## ClinicalTrials.Gov now accumulates information from over 300K trials with over 10% reporting results.
## It is now a [U.S. Law](https://www.gpo.gov/fdsys/pkg/PLAW-110publ85/pdf/PLAW-110publ85.pdf#page=82) to upload clinical trials to this [fast growing database](https://clinicaltrials.gov/ct2/resources/trends). 
## Data from this database can be extracted in XML format towards modeling.
## However, the database is based on textual input which is suitable for human use rather than computer comprehension.
       
## One major problem is unit standardization

|     Time    | Number of Trial with Results | Unique Units |
|:-----------:|:----------------------------:|:------------:|
| 20 Apr 2018 |            30,763            |    21,094    |
|  7 Feb 2019 |            34,751            |    23,733    |
| 12 Apr 2019 |            35,926            |    24,548    |    
    
## Non standardized units prevent machine comprehension of stored numbers.
## If units are standardized, the valuable numerical data in this database can become machine comprehensible.
""", width=1200, height=250)


Section4MethodText = panel.panel("""# Method

## 1. Aggregate and index all ClinicalTrials.Gov units                     

## 2. Gather existing unit standards / specifications:
           
### - [CDISC](https://www.cdisc.org/) - Clinical Data Interchange Standards Consortium
### - [RTMMS](https://rtmms.nist.gov/rtmms/) - affiliated with NIST / IEEE / ISO
### - [Unit Onthology](https://bioportal.bioontology.org/) from BioPortal
### - [UCUM](https://unitsofmeasure.org/) - The Unified Code for Units of Measure (RTMMS / CDISC)
                                 

## 3. Use python tools to:
### - Link between units using Machine Learning and NLP
### - Create a web site for crowd mapping of the unit corpus

## 4. In the future this mapping will allow machines to comprehend units


""", width=500, height=250)

Section4ProcessingDiagram =  panel.panel(ConstractImageLinkAnchor('https://clinicalunitmapping.com/','ClinicalUnitProcessDiagram.png','Clinical data Processing diagram',700), width=700, height=420)

Section4Method = panel.Row(Section4MethodText,Section4ProcessingDiagram)



Section4NLP = panel.panel("""# Natural Language Processing (NLP)

## Units were evaluated for text proximity using:

### difflib.SequenceMatcher method
### TfidfVectorizer & cosine_similarityfrom scikit-learn

## Overall 5729 unique Auxiliary unit were processed. 

## A similarity matrix was constructed.
### Matrix size was 24,548 x (24,548 + 5729)


""", width=600, height=220)

Section4MachineLearningDiagram = (panel.panel(ConstractImageLinkAnchor('https://scikit-learn.org/stable/modules/generated/sklearn.cluster.MiniBatchKMeans.html','MultipleClusters.png','clustering algorithm executed multiple times',1200), width=1200, height=240))

Section4DiagramNLP = panel.panel(ObjectInlineHTML(CommonResourceDir+'UnitProximityHeatMap.html',600,600), width=600, height=600)

Section4DevelopmentNLP = panel.Row(Section4NLP, Section4DiagramNLP)


Section4DevelopmentVisualizingClusteringText = panel.panel("""# Machine Learning

### To allow the user to see similar units together, scikit-learn unsupervised machine learning was used.

### Clustering was performed multiple times with different similarity measures to create 130 clusters.
                                                           
### The top images show the proximity matrix before and after clustering at different stages of the algorithm. 

### The green bars show distance from cluster centers. Dark means distant.

### The red bars show the cluster number for each unit.

### The images after clustering visually show the organizing effect of clustering.

### Such interactive visualization is possible through [PyViz technologies](http://pyviz.org/). 

""", width=300, height=600)

Section4DevelopmentVisualizingClusteringDiagram = panel.panel(ObjectInlineHTML(CommonResourceDir + 'UnitClusterImage_max_linear_400.html',900,600), width=900, height=600)


Section4DevelopmentVisualizingClustering = panel.Row(Section4DevelopmentVisualizingClusteringText, Section4DevelopmentVisualizingClusteringDiagram)




Section4KeyPoints = panel.panel("""# Web Site Key Points

### A web site was created to allow collaborative unit mapping
### The web site is accessible thought [ClinicalUnitMapping.com](https://clinicalunitmapping.com/)

## Developments:
### The units were stored in a SQLite3 relational database
### The web site was developed using the Flask library
### A reduced database was used for demonstration purposes
### An administration system allows multiple user management

## User support:
### Similar units clustered together and user can switch clusters
### Unit context and statistics displayed
### User can map units using user or machine  suggested units
### Highlighted auxiliary units: RTMMS / CDISC / UCUM / Unit Ontology 


""", width=500, height=600)

Section4WebSiteStaticImage = panel.panel(ConstractImageLinkAnchor('https://clinicalunitmapping.com/','ClinicalUnitMappingScreenShot.png','ClinicalUnitMapping.com web site',700), width=700, height=440)

Section4KeyElements = panel.Row(Section4WebSiteStaticImage, Section4KeyPoints)



Section4Discussion = panel.panel("""# Discussion and Future Efforts
## The goal is to solve the unit standardization problem. 

## Once data is standardized, data that is currently machine readable will become machine comprehensible. 

## Standardizing units may be only the first step. 

## Current efforts are to expand this unit standardization project with the intention to work with:

### - Unified Medical Language System [(UMLS)](https://www.nlm.nih.gov/research/umls/)
### - Clinical Data Interchange Standards Consortium [(CDISC)](https://www.cdisc.org/)
### - Simulation Interoperability Standards Organization [(SISO)](https://www.sisostds.org/)

""", width=1200, height=120)



Section5AdditionalInfo = panel.panel("""

## Reproducibility:

This presentation is accessible [here](https://jacob-barhak.github.io/Presentation_PyConIsrael2019.html). The code that generated the presentation can be accessed [here](https://github.com/Jacob-Barhak/Presentations/tree/master/PyConIsrael2019).

This presentation is generated using Python 2.7.16, panel-0.5.1, bokeh-1.1.0. with the exception of clustering images produced on Python 3.7.3 , numpy 1.16.3, matplotlib 3.0.3, holoviews 1.12.1, bokeh 1.1.0, panel 0.5.1.

Clinical Unit Mapping : Code and data for this work are archived in the file: AnalyzeCT_2019_05_13_Sup_2019_05_31.zip. Web site database was created using the database PartUnitsDB_2019_05_13.db ,  StudiesWithResults_Downloaded_2019_04_12.zip. 

BioPortal Unit Ontology downloaded on 2019_04_09, CDISC data downloaded on 2019_03_30 , RTMMS units downloaded on 2019_03_24 .  

&nbsp;

## Publications:

* J. Barhak, The Reference Model Models ClinicalTrials.Gov. [SummerSim 2017 July 9-12, Bellevue, WA].(https://doi.org/10.22360/SummerSim.2017.SCSC.022)
* J. Barhak, The Reference Model: A Decade of Healthcare Predictive Analytics with Python, PyTexas 2017, Nov 18-19, 2017, Galvanize, Austin TX. [Video](https://youtu.be/Pj_N4izLmsI)
* J. Barhak, C. Myers, L. Watanabe, L. Smith, M. J. Swat , Healthcare Data and Models Need Standards. Simulation Interchangeability Standards Organization (SISO) 2018 Fall Innovation Workshop.  9-14 Sep 2018 Orlando, Florida [Presentation](https://www.sisostds.org/DesktopModules/Bring2mind/DMX/API/Entries/Download?Command=Core_Download&EntryId=47969&PortalId=0&TabId=105)
* J. Barhak, Python Based Standardization Tools for ClinicalTrials.Gov. Combine 2018 . Boston University [Poster](http://co.mbine.org/system/files/COMBINE_2018_Barhak.pdf)
* J. Barhak, J. Schertz, Clinical Unit Mapping for Standardization of ClinicalTrials.Gov . MSM/IMAG meeting. IMAG Multiscale Modeling (MSM) Consortium Meeting March 6-7, 2019 @ NIH, Bethesda, MD . [Poster](https://jacob-barhak.github.io/InteractivePoster_MSM_IMAG_2019.html)
* J. Barhak, Clinical Data Modeling with Python, AnacondaCon , Austin, Texas,  April 3-5, 2019. [Video](https://youtu.be/fQIYMf5wKGE) , [Presentation](https://jacob-barhak.github.io/AnacondaCon_2019.html) 
""", width=1200, height=1000)


Section5SummaryText = panel.panel("""# Summary

## <span style="color:magenta">We are still very far from computers replacing medical expert reasoning. Yet Artificial Intelligence will eventually performs decisions better than a certified human, allowing applications such as a computerized medical assistant.</span>

## <span style="color:magenta">A major obstacle is standardization! Yet Python can help!</span>

### Acknowledgments: 
* Many thanks to the PyViz team:
    - James Bednar who introduced the PyViz tools.
    - Philipp Rudiger for great support of PyViz tools. 
    - Jean-Luc Stevens for creating holoviews.
* Thanks to John Rice for the fruitful discussions regarding standardization. 
* Thanks to CDISC consortium help
* Thanks to government persons who helped and specifically to: 
    - Nick Ide from NIH/NLM ClinicalTrials.Gov team on advice to process the site
    - Erin E Muhlbradt from NIH/NCI for advice on CDISC unit data
    - John Garguilo from NIST  for information on RTMMS
* Thanks to Paul Schluter for information about RTMMS and the IEEE unit standard
* Thanks for Tipton Cole, Rocky Reston, Andrew Simms for useful directions

""", width=600, height=500)

Section5Summary = panel.Row(Section5SummaryText,PresentationURL)



SectionSelectorTab = panel.layout.Tabs (
                                        ('Preface',Section0),
                                        ('Opinions 1', Section0QuestionAndAnswers1 ),
                                        ('Opinions 2', Section0QuestionAndAnswers2 ),
                                        ('ClinicalTrials.Gov', Section4AbstractText),
                                        ('Method', Section4Method),
                                        ('NLP', Section4DevelopmentNLP),
                                        ('Machine Learning', Section4DevelopmentVisualizingClustering),
                                        ('ClinicalUnitMapping.com', Section4KeyElements),
                                        ('Discussion',Section4Discussion),
                                        ('References', Section5AdditionalInfo),
                                        ('Summary', Section5Summary),
										margin = (0,0,0,0),
                                        )

Presentation = panel.Column(PresentationHeader, SectionSelectorTab)
Presentation.save('Presentation_PyConIsrael2019.html', title = TitleHTML)       

