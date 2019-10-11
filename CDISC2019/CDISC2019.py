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


import bokeh
import panel
import base64
import os
import sys
import collections
import holoviews
import numpy
import pickle
from bokeh.resources import INLINE
from matplotlib.cm import  PuBu, PuRd, Greens

EmbedVideo = False
if len(sys.argv)>1:
    EmbedVideo = 'EmbedVideo' in sys.argv[1:]
    
Width = 1100

ImageDir = 'Images'
DataDir = 'Data'
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

def ObjectInlineHTML(ExtrnalFileName,Width=Width,Height=700):
    'Encodes html from a file into object'
    RetStr = '<object width="'+str(Width)+'" height="'+str(Height)+'" data="%s">Warning:%s Not Accesible!</object>'%(ExtrnalFileName,ExtrnalFileName)
    return RetStr

def VideoInlineHTML(ExtrnalFileName,Width=Width,Height=700, EmbedVideo = EmbedVideo):
    'Encodes html from a file into video'
    if EmbedVideo:
        ExtrnalData = CovertFileToData(ExtrnalFileName)
        RetStr = '<Video width="%i" height="%i" controls>   <source src="%s" type="video/mp4">  Warning:%s could not be included! </Video>'%(Width, Height, 'data:video/mp4;base64,'+ExtrnalData,ExtrnalFileName)
    else:
        RetStr = '<Video width="%i" height="%i" controls>   <source src="%s" type="video/mp4">  Warning:%s could not be included! </Video>'%(Width, Height, ExtrnalFileName,ExtrnalFileName)
    return RetStr



BokehDocument = bokeh.document.Document()

PresentationURL = panel.panel(ConstractImageLinkAnchor('https://jacob-barhak.github.io/Poster_CDISC2019.html','CDISC_2019_Poster.png','View this presentation on the web',480), width=480, height=480)

PresentationTitle = panel.panel('# Clinical Unit Mapping with Multiple Standards', width=600, height=55, margin = (0,0,0,0))
PresentationVenue = panel.panel("""[Jacob Barhak](http://sites.google.com/site/jacobbarhak/) , [Joshua Schertz](https://joshschertz.com/) <br>
2019 CDISC U.S. Interchange, 16 - 17 October 2019 
""", width=400, height=20, margin = (0,0,0,0))

PresentationVenueFigure = panel.panel(ConstractImageLinkAnchor('https://www.cdisc.org/2019-cdisc-us-interchange','logo.png','2019 CDISC U.S. Interchange',90), width=100, height=50, margin = (0,0,0,0))

PresentationHeader = panel.Row ( PresentationTitle,  PresentationVenue, PresentationVenueFigure, margin = (0,0,0,0) )


#Section0Title = panel.panel('## Motivation: Computer Automation of Human Reasoning?', width=1000, height=20)
#Section0Author = panel.panel('by: [Jacob Barhak](http://sites.google.com/site/jacobbarhak/)', width=200, height=40)
#
#Section0Header =  panel.Row(Section0Title, Section0Author, margin = (0,0,0,0))

#Section0ChronologyFigure = panel.panel(ConstractImageLinkAnchor('https://en.wikipedia.org/wiki/Computer_chess','ComputerInfluenceDiagram.png','Towards Computer Automation of Human tasks - Main sources Wikipedia Computer Chess and Wikipedia self-driving car',1000), width=1000, height=500)



#Section0 = panel.Column(Section0Header, Section0ChronologyFigure)



Section1AbstractText = panel.panel("""# About ClinicalTrials.Gov
## ClinicalTrials.Gov now accumulates information from over 300K trials with over 10% reporting results.
## It is now a [U.S. Law](https://www.gpo.gov/fdsys/pkg/PLAW-110publ85/pdf/PLAW-110publ85.pdf#page=82) to upload clinical trials to this [fast growing database](https://clinicaltrials.gov/ct2/resources/trends). 
## Data from this database can be extracted in XML format towards modeling.
## However, the database uses textual input that is suitable for human use rather than computer comprehension.

# The Standardization Problem:
## Non standardized units prevent machine comprehension of stored numbers.

|     Time    | Number of Trial with Results | Unique Units |
|:-----------:|:----------------------------:|:------------:|
| 20 Apr 2018 |            30,763            |    21,094    |
|  7 Feb 2019 |            34,751            |    23,733    |
| 12 Apr 2019 |            35,926            |    24,548    |    

### If units are standardized, the valuable numerical data in this database can become machine comprehensible.
""", width=Width, height=500)


Section1MethodText = panel.panel("""# Proposed Solution

## 1. Aggregate and index all ClinicalTrials.Gov units

## 2. Gather auxiliary unit standards / specifications:

### - [CDISC](https://www.cdisc.org/) - Clinical Data Interchange Standards Consortium
### - [RTMMS](https://rtmms.nist.gov/rtmms/) - affiliated with NIST / IEEE / ISO
### - [Unit Onthology](https://bioportal.bioontology.org/) from BioPortal
### - [UCUM](https://unitsofmeasure.org/) - The Unified Code for Units of Measure (RTMMS / CDISC)

## 3. Use python tools to:
### - Link between units using Machine Learning and NLP
### - Create a web site for crowd mapping of the unit corpus
### - Create supervised learning technique to comprehend units

## 4. In the future this mapping will allow machines to comprehend units
""", width=500, height=450)

Section1ProcessingDiagram =  panel.panel(ConstractImageLinkAnchor('https://clinicalunitmapping.com/','ClinicalUnitProcessDiagram.png','Clinical data Processing diagram',600), width=600, height=420)

Section1Method = panel.Row(Section1MethodText,Section1ProcessingDiagram)

Section1 = panel.Column(Section1AbstractText,Section1Method)

Section2NLP = panel.panel("""# Natural Language Processing (NLP)

## Units were evaluated for text proximity.

## Overall 24,548 Units were compared to each other. 
## 5729 unique auxiliary units from standards were also compared. 

## A similarity matrix was constructed.

## However, it was not sorted and similar units were apart. 

## Unsupervised machine learning was applied to aid user experience and bunch units together.

## Clustering was performed multiple times with different similarity measures to create 130 clusters.



""", width=600, height=480)

#Section2MachineLearningDiagram = (panel.panel(ConstractImageLinkAnchor('https://scikit-learn.org/stable/modules/generated/sklearn.cluster.MiniBatchKMeans.html','MultipleClusters.png','clustering algorithm executed multiple times',500), width=500, height=240))

def GenerateProximityMap():
    "Generate the proximity map"
    DataFile = open(DataDir+os.sep+'UnitProximityHeatMap_Data.pckl','rb')
    Data = pickle.load(DataFile)
    DataFile.close()
    holoviews.extension('bokeh')
    UnitHeatMap = holoviews.HeatMap(Data).opts(title = 'Zoom on Proximity Matrix Before Clustering')
    Hover = bokeh.models.HoverTool(
                        tooltips=[
                                    ("Unit 1", "@x"),
                                    ("Unit 2", "@y"),
                                    ("Proximity", "@z"),
                                 ]
                        )
    UnitHeatMap.opts(tools=[Hover], cmap = 'BuPu' , colorbar=True, toolbar=None, width=600, height=600, xrotation=90, ticks_text_font_size = 5, labelled=[])
    PanelOut = panel.pane.HoloViews(UnitHeatMap, width=600, height=600)
    return PanelOut

def LoadFullMatrixComponent(FileName, Title, ColorMap, PlotHeight, PlotWidth):
    "load larger matrix components and build an object with options"
    DataFile = open(DataDir+os.sep+FileName,'rb')
    HoloviewsObject = pickle.load(DataFile)
    DataFile.close()
    HoloviewsObject.opts(cmap=ColorMap, title = Title, xaxis=None, yaxis=None,  height=PlotHeight, width=PlotWidth, tools=['hover'], toolbar = None, axiswise=True)
    return HoloviewsObject
    

#Section2DiagramNLP = panel.panel(ObjectInlineHTML(ExternalResourcesIMAG2019+'UnitProximityHeatMap.html',700,700), width=600, height=600)
Section2DiagramNLP = GenerateProximityMap()


Section2BeforeMat = LoadFullMatrixComponent('UnitClusterImage__400_linear_max_-99_Mat.pckl','Proximity Matrix Before Clustering',PuBu,400,400)
Section2BeforeDist = LoadFullMatrixComponent('UnitClusterImage__400_linear_max_-99_Dist.pckl','Distance Before Clustering',Greens,50,400)
Section2BeforeBar = LoadFullMatrixComponent('UnitClusterImage__400_linear_max_-99_Bar.pckl','Cluster Number Before Clustering',PuRd,50,400)
Section2Before = panel.Column(Section2BeforeMat,Section2BeforeDist,Section2BeforeBar, margin = (0,0,0,0))

Section2AfterMat = LoadFullMatrixComponent('UnitClusterImage_Permuted_400_linear_max_-99_Mat.pckl','Proximity Matrix After Clustering',PuBu,400,400)
Section2AfterDist = LoadFullMatrixComponent('UnitClusterImage_Permuted_400_linear_max_-99_Dist.pckl','Distance After Clustering',Greens,50,400)
Section2AfterBar = LoadFullMatrixComponent('UnitClusterImage_Permuted_400_linear_max_-99_Bar.pckl','Cluster Number After Clustering',PuRd,50,400)
Section2After = panel.Column(Section2AfterMat,Section2AfterDist,Section2AfterBar, margin = (0,0,0,0))

Section2 = panel.Row(panel.Column(Section2NLP,Section2DiagramNLP), panel.Column( Section2Before, Section2After))


Section3KeyPoints = panel.panel("""# Collaborative Unit Mapping Web Site
### The web site is accessible using [ClinicalUnitMapping.com](https://clinicalunitmapping.com/)

## Developments:
### The Web site uses the SQLite3 database and the Flask library
### A reduced database was used for demonstration purposes
### An administration system allows multiple user management

## User support:
### Similar units clustered together and user can switch clusters
### Unit context and statistics displayed
### User can map units using user or machine  suggested units
### Highlighted auxiliary units: RTMMS / CDISC / UCUM / Unit Ontology 
""", width=500, height=480)



Section3WebSiteStaticImage = panel.panel(ConstractImageLinkAnchor('https://clinicalunitmapping.com/','ClinicalUnitMappingScreenShot.png','ClinicalUnitMapping.com web site',600), width=600, height=440)

Section3WebSiteObject = panel.panel(ObjectInlineHTML('https://clinicalunitmapping.com/', Width=Width, Height=600), width=Width, height=600)

Section3KeyElements = panel.Row(Section3WebSiteStaticImage, Section3KeyPoints)

Section3Assembled = panel.Column(Section3KeyElements, Section3WebSiteObject)




Section4SupervisedMachineLearningOverview = panel.panel("""# Supervised Machine Learning - Deep Learning 

## An artificial neural network was created to automate unit mapping through suggestion

## The neural network can suggest closest standardized unit mapping for a new unit, specifically:

### &nbsp;&nbsp;&nbsp;&nbsp;1. Suggesting corrections for units that are misspelled

### &nbsp;&nbsp;&nbsp;&nbsp;2. Suggesting standard units to a user if a mapping is already known

### &nbsp;&nbsp;&nbsp;&nbsp;3. Keeping the human knowledge on units in a computer comprehensible form

## Difficulties:
### &nbsp;&nbsp;&nbsp;&nbsp;- There are too many target units to use ordinary classification
### &nbsp;&nbsp;&nbsp;&nbsp;- Many units map to the same result so the translation is many to one rather than one to one
### &nbsp;&nbsp;&nbsp;&nbsp;- Data distribution is unbalanced with many examples for some mapping
### &nbsp;&nbsp;&nbsp;&nbsp;- Context of units has a large vocabulary 
### &nbsp;&nbsp;&nbsp;&nbsp;- Training data is limited - although growing in time

## Suggested Solution Neural Network Features:
### &nbsp;&nbsp;&nbsp;&nbsp;- Units are encoded as character sequences while context is encoded using embedding 
### &nbsp;&nbsp;&nbsp;&nbsp;- Supports multiple Sequence to Sequence networks - including Encoder Decoder architecture
### &nbsp;&nbsp;&nbsp;&nbsp;- Mainly LSTM / CNN network layers supplemented by Embedding / Dense
### &nbsp;&nbsp;&nbsp;&nbsp;- Noise is added to unit input to simulate spelling errors
### &nbsp;&nbsp;&nbsp;&nbsp;- The neural network input can include unit / context or both
### &nbsp;&nbsp;&nbsp;&nbsp;- Unit cluster is used to narrow possible results
### &nbsp;&nbsp;&nbsp;&nbsp;- Validation data set was split so that at least one example of target mapping is known
### &nbsp;&nbsp;&nbsp;&nbsp;- String sequence proximity is used to deduce possible mapping

## Neural Network Training:
### The neural network was trained using mock data based on proximity deduced from heuristics based on unsupervised learning. 
### The training data mapped 24,548 units to 6,891 mock interpretations that simulate possible future mapping.
### Post-processing was applied after training to deduce what is the predicted unit accuracy.
### Closest units with a certain distance from prediction were explored for accuracy.
### Multiple distance metrics were used to deduce closest unit to predicted string.




""", width=Width, height=250)




def GeneratePlot(Title):
    "Generate a plot for clusters processed"

    holoviews.extension('bokeh')    
    PlotsDict = {}
    
    DuplicateAndMaskDataInputsLevel = [True,True,True]
    ShowStatisticsForOnlyThisNumberOfFirstItems = 10
    PhaseTexts = ['Training', 'Validation']
    PassTypeTexts = ['Unit & Context','Unit Only','Context Only']
    
    PlotTypes = [('Predict Exact',True), 
                 ('Predict Close',True),  
                 ('Distance First Metric',False),   
                 ('Distance Second Metric',False),   
                 ('Distance Best Metric',False),    
                 ('Distance Combined Metric',False),   
                  ]
    PredictionQualities = collections.defaultdict(list)
    TempFile = open(DataDir+os.sep+'SummaryStats_Last_ClusterBatch_1.pckl','rb')
    (PredictionQualities) = pickle.load(TempFile)
    TempFile.close()
        
    for (IsValidationPass, PhaseText) in enumerate(PhaseTexts):
        for PassTypeNumber in range(sum(DuplicateAndMaskDataInputsLevel)):
            PassTypeText = PassTypeTexts[PassTypeNumber]
            for (PlotTypeEnum,(PlotTypeName,IsPlotTypeBoolean)) in enumerate(PlotTypes):  
                if IsPlotTypeBoolean:
                    NumberOfCategories = 2
                    Bins = [-0.5,0.5,1.5]
                    LabelsX = [(0,'Miss'),(1,'Hit')]
                else:
                    NumberOfCategories = ShowStatisticsForOnlyThisNumberOfFirstItems
                    Bins = [Entry-0.5 for Entry in list(range(NumberOfCategories+2))]
                    LabelsX = [ (int(Bin+0.5),int(Bin+0.5)) for Bin in Bins ] 
                    LabelsX[0] = (0,'Exact')
                    LabelsX[-1] = (NumberOfCategories,str(NumberOfCategories)+'+')

                Values = [min(Entry[PlotTypeEnum]+0,NumberOfCategories) for Entry in PredictionQualities[(IsValidationPass,PassTypeNumber)] if Entry !=None] 
                Frequences, Edges = numpy.histogram(Values, bins = Bins, density = True)
                if IsPlotTypeBoolean:
                    FrequencesToUse = Frequences
                else:
                    FrequencesToUse = [ sum(Frequences[:(Enum+1)]) for Enum in range(len(Frequences))] 
                HistogramShortTitle = holoviews.Histogram((Edges, FrequencesToUse)).redim.label(x='Quality', Frequency = ['Cumulative Proportion','Proportion'][IsPlotTypeBoolean]).opts( title = PlotTypeName, tools = ['hover'], ylim =(0,1), color = ['Blue','Red'][IsPlotTypeBoolean], height=140 , width=230-100*IsPlotTypeBoolean, toolbar = None, fontsize={'title': 8, 'labels': 8, 'xticks': 6, 'yticks': 6}, xticks=LabelsX)    
                PlotsDict[(PhaseText,PassTypeText,PlotTypeName)] = HistogramShortTitle

    PlotList = [  (PhaseText + ' ' + PassTypeText  , [ panel.pane.HoloViews(PlotsDict[(PhaseText,PassTypeText,PlotTypeName)]) for (PlotTypeName,IsPlotTypeBoolean) in (PlotTypes)]) for PhaseText in PhaseTexts for PassTypeText in PassTypeTexts[:sum(DuplicateAndMaskDataInputsLevel)] ] 
    CombinedList = [panel.panel(Title,height=135, margin = (0,0,0,0))]
    for (PlotTitle,PlotRows) in PlotList:
        CombinedList.append(panel.panel('#### '+PlotTitle,height=35, margin = (0,0,0,0)))
        CombinedList.append(panel.Row(*PlotRows, margin = (0,0,0,0)))
    ConstrcutedGrid = panel.Column(*CombinedList, margin = (0,0,0,0), linked_axes=False)
    return ConstrcutedGrid



Section4SupervisedMachineLearningResults = GeneratePlot("""# Neural Network Training and Validation Results 
Rows show scenarios where inputs include unit / context / both unit and context. Columns show different comparison metrics.
 
<span style="color:red">Red= first prediction attempt accuracy</span>.  <span style="color:Blue">Blue = prediction quality with multiple close units. </span>
""")




Section5SummaryText = panel.panel("""# Summary
### <span style="color:magenta">We created tools necessary to merge units of measure standards.</span>
### <span style="color:magenta">With such tools is will be possible for machines to:</span>
### <span style="color:magenta">- Recognize medical units, even if misspelled</span>
### <span style="color:magenta">- Comprehend medical units</span>
### <span style="color:magenta">- Comprehend numbers associated with units</span>
### <span style="color:magenta">Such AI will eventually replace tedious human tasks.</span>

## Future Work
### - Perform human mapping of units using ClinicalUnitMapping.Com
### - Apply the supervised machine learning tools to the mapped units
### - Add the supervised learning API to ClinicalUnitMapping.Com 
### - Contribute to [(UMLS)](https://www.nlm.nih.gov/research/umls/), [(CDISC)](https://www.cdisc.org/), [(SISO)](https://www.sisostds.org/)
""", width=600, height=480)

Section5Summary = panel.Row(Section5SummaryText,PresentationURL, margin = (0,0,0,0))


Section5AdditionalInfo = panel.panel("""
## Acknowledgments: 
* Many thanks to the PyViz team: Philipp Rudiger, James Bednar, Jean-Luc Stevens.
* Thanks to John Rice for the fruitful discussions regarding standardization
* Thanks to government persons who helped and specifically to: 
    - Nick Ide from NIH/NLM ClinicalTrials.Gov team on advice to process the site
    - Erin E Muhlbradt from NIH/NCI for advice on CDISC unit data
    - John Garguilo from NIST for information on RTMMS
* Thanks to Paul Schluter for information about RTMMS and the IEEE unit standard
* Thanks for Tipton Cole, Rocky Reston, Andrew Simms for useful directions
* Thanks to Yuval Merchav Uri Goren, Ari Bornstein for NLP advise 

## Reproducibility:

This presentation is accessible [here](https://jacob-barhak.github.io/Poster_CDISC2019.html). The code that generated the presentation can be accessed [here](https://github.com/Jacob-Barhak/Presentations/tree/master/CDISC2019). This presentation is generated using Python 2.7.16, panel-0.5.1, bokeh-1.1.0.
Code and data for this work are archived in the file: AnalyzeCT_2019_05_13.zip. Web site database was created using the database PartUnitsDB_2019_05_13.db Supplemental code archived in the files: AnalyzeCT_Images_2019_10_10.zip, AnalyzeCT_Code_2019_05_15.zip. 
Clinical Trials data archived in StudiesWithResults_Downloaded_2019_04_12.zip. Bio Ontology Units downloaded on 2019_04_09, CDISC data downloaded on 2019_03_30 , RTMMS units downloaded on 2019_03_24 .  
Tensorflow 2.0.0 was used for Neural Network execution in Python 3.7.4 environment . This tensorflow version is unstable, so results presented may not be reproducible. Execution transcript was saved in the file:AnalyzeCT_TF2_LargeMod__Seq2Seq_MinimalWorkingWithContext_2019_10_03.zip

## Publications:

* J. Barhak, The Reference Model Models ClinicalTrials.Gov. [SummerSim 2017 July 9-12, Bellevue, WA](https://doi.org/10.22360/SummerSim.2017.SCSC.022)
* J. Barhak, The Reference Model: A Decade of Healthcare Predictive Analytics with Python, PyTexas 2017, Nov 18-19, 2017, Galvanize, Austin TX. [Video](https://youtu.be/Pj_N4izLmsI)
* J. Barhak, C. Myers, L. Watanabe, L. Smith, M. J. Swat , Healthcare Data and Models Need Standards. Simulation Interchangeability Standards Organization (SISO) 2018 Fall Innovation Workshop.  9-14 Sep 2018 Orlando, Florida [Presentation](https://www.sisostds.org/DesktopModules/Bring2mind/DMX/API/Entries/Download?Command=Core_Download&EntryId=47969&PortalId=0&TabId=105)
* J. Barhak, Python Based Standardization Tools for ClinicalTrials.Gov. Combine 2018 . Boston University [Poster](http://co.mbine.org/system/files/COMBINE_2018_Barhak.pdf)
* J. Barhak, J. Schertz, Clinical Unit Mapping for Standardization of ClinicalTrials.Gov . MSM/IMAG meeting. IMAG Multiscale Modeling (MSM) Consortium Meeting March 6-7, 2019 @ NIH, Bethesda, MD . [Poster](https://jacob-barhak.github.io/InteractivePoster_MSM_IMAG_2019.html)
* J. Barhak, Clinical Data Modeling with Python, AnacondaCon , Austin, Texas,  April 3-5, 2019. [Video](https://youtu.be/fQIYMf5wKGE) , [Presentation](https://jacob-barhak.github.io/AnacondaCon_2019.html) 
* J. Barhak, J. Schertz, Standardizing Clinical Data with Python . PyCon Israel 3-5 June 2019, [Video](https://youtu.be/vDXyCb60L5s)  [Presentation](https://jacob-barhak.github.io/Presentation_PyConIsrael2019.html) 
""", width=Width, height=600)



Section5 =  panel.Column(Section5Summary,Section5AdditionalInfo, margin = (0,0,0,0))



TitleHTML = 'CDISC 2019 poster by Jacob Barhak & Joshua Schertz'


SectionSelectorTab = panel.layout.Tabs (
                                        ('Preface',Section1),
                                        ('NLP and Unsupervised Machine Learning', Section2),
                                        ('ClinicalUnitMapping.com', Section3Assembled),
                                        ('Supervised Machine Learning', Section4SupervisedMachineLearningOverview),
                                        ('Preliminary Results', Section4SupervisedMachineLearningResults),
                                        ('Summary', Section5),
                                        margin = (0,0,0,0), 
                                        )
                                        
Presentation = panel.Column(PresentationHeader, SectionSelectorTab)
Presentation.save('Poster_CDISC2019.html', resources=INLINE, title=TitleHTML)       

