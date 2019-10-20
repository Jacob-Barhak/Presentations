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


TitleHTML = 'MSM ML IMAG 2019 poster by Jacob Barhak & Joshua Schertz'
SavedFileName = 'Poster_MSM_ML_IMAG_2019.html'
PublishURL = 'https://jacob-barhak.github.io/'+SavedFileName
CodePublishURL = 'https://github.com/Jacob-Barhak/Presentations/tree/master/MSM_ML_IMAG2019'
QRCodeFileName = 'MSM_ML_IMAG_2019_Poster.png'

PresentationURL = panel.panel(ConstractImageLinkAnchor(PublishURL,QRCodeFileName,'View this presentation on the web',480), width=480, height=480)

PresentationTitle = panel.panel('# Supervised Learning of Units of Measure', width=600, height=55, margin = (0,0,0,0))
PresentationVenue = panel.panel("Venue: [Integrating Machine Learning with Multiscale Modeling for Biomedical, Biological, and Behavioral Systems (2019 ML-MSM)](https://www.imagwiki.nibib.nih.gov/msm-consortium/2019-ml-msm)", width=395, height=55, margin = (0,0,0,0))

#PresentationVenueFigure = panel.panel(ConstractImageLinkAnchor('https://www.imagwiki.nibib.nih.gov/msm-consortium/2019-ml-msm','NoLogo.png','Integrating Machine Learning with Multiscale Modeling for Biomedical, Biological, and Behavioral Systems (2019 ML-MSM)',140), width=100, height=55, margin = (0,0,0,0))
PresentationAuthors = panel.panel("By: [Jacob Barhak](http://sites.google.com/site/jacobbarhak/) </br> & [Joshua Schertz](https://joshschertz.com/)", width=150, height=55, margin = (0,0,0,0))

PresentationHeader = panel.Row ( PresentationTitle,  PresentationAuthors , PresentationVenue, margin = (0,0,0,0))






Section0AbstractText = panel.panel("""# Abstract
[U.S. law](https://www.gpo.gov/fdsys/pkg/PLAW-110publ85/pdf/PLAW-110publ85.pdf#page=82) requires registration of clinical trial data in [ClinicalTrials.Gov](https://clinicaltrials.gov). This NIH/NLM governed registry contributed much towards providing important modeling data information by [accumulating over 300,000 clinical trials](https://clinicaltrials.gov/ct2/resources/trends). However, despite the great effort by the government to centralize the data, the entities reporting data do not follow a predetermined standard. Therefore, numerical information entered is machine readable, yet not machine comprehensible, especially due to units being entered as free text. If a machine cannot comprehend the units, it cannot comprehend the numbers. This causes human intervention in the modeling process - slowing down modeling and the uses of this important registry.

The extent of the problem requires some machine learning, as of 12 Apr 2019, all 35,926 trials with results had 24,548 different units. The authors created solution infrastructure to address this problem. The solution includes:

1) Data extraction tools for ClinicalTrials.Gov that can index data and assemble clusters of data with unsupervised learning.

2) [ClinicalUnitMaping.Com](https://clinicalunitmapping.com) : a website for unit mapping that also demonstrates the extent of the problem.

3) A collection of existing unit standards used for medical purposes that currently holds data from CDISC, NIST / RTMMS / IEEE, Unit Ontology / Bio Portal, UCUM.

4) Supervised Machine Learning using neural networks that can predict the standardized unit given a non standard unit.

The supervised machine learning techniques are new, and their development involved many technical aspects and many attempts to solve the problem. This publication will discuss the difficulties and summarize multiple attempts, architectures, and solutions to resolve the problem.
""", width=Width, height=500)

Section0SubHeader = panel.panel('## Longer Term Motivation: Computer Automation of Human Reasoning', width=1000, height=20)

Section0ChronologyFigure = panel.panel(ConstractImageLinkAnchor('https://en.wikipedia.org/wiki/Computer_chess','ComputerInfluenceDiagram.png','Towards Computer Automation of Human tasks - Main sources Wikipedia Computer Chess and Wikipedia self-driving car',1000), width=1000, height=700)

Section0 = panel.Column(Section0AbstractText, Section0SubHeader, Section0ChronologyFigure)
   
    
    
    
Section1MethodText = panel.panel("""# Proposed Solution

## 1. Aggregate and index all ClinicalTrials.Gov units

## 2. Gather auxiliary unit standards / specifications:

### - [CDISC](https://www.cdisc.org/) - Clinical Data Interchange Standards Consortium
### - [RTMMS](https://rtmms.nist.gov/rtmms/) - affiliated with NIST / IEEE / ISO
### - [Unit Onthology](https://bioportal.bioontology.org/) from BioPortal (BIOUO)
### - [UCUM](https://unitsofmeasure.org/) - The Unified Code for Units of Measure (RTMMS / CDISC)

## 3. Use python tools to:
### - Find unit proximity using unsupervised Machine Learning and Natural Language Processing (NLP)
### - Create a web site for crowd mapping of the unit corpus
### - Create supervised learning technique to comprehend units

""", width=500, height=470)

Section1ProcessingDiagram =  panel.panel(ConstractImageLinkAnchor('https://clinicalunitmapping.com/','ClinicalUnitProcessDiagram.png','Clinical data Processing diagram',600), width=600, height=420)

Section1Method = panel.Row(Section1MethodText,Section1ProcessingDiagram)



Section1WebKeyPoints = panel.panel("""# Collaborative Unit Mapping Web Site
## The web site is accessible using [ClinicalUnitMapping.com](https://clinicalunitmapping.com/)

### - A reduced database was used for demonstration purposes
### - An administration system allows multiple user management
### - Similar units clustered together and user can switch clusters
### - Unit context and statistics displayed
### - User can map units using user or machine  suggested units
### - Highlighted auxiliary units: RTMMS / CDISC / UCUM / BIOUO
""", width=500, height=350)



Section1WebSiteStaticImage = panel.panel(ConstractImageLinkAnchor('https://clinicalunitmapping.com/','ClinicalUnitMappingScreenShot.png','ClinicalUnitMapping.com web site',500), width=500, height=440)

Section1WebKeyElements = panel.Column(Section1WebKeyPoints, Section1WebSiteStaticImage)


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
    

Section1HeaderNLP = panel.panel("""# Unit Proximity with NLP + Clustering
""", width=600, height=50)

Section1DiagramNLP = GenerateProximityMap()

Section1BeforeMat = LoadFullMatrixComponent('UnitClusterImage__400_linear_max_-99_Mat.pckl','Proximity Matrix Before Clustering',PuBu,400,400)
Section1BeforeDist = LoadFullMatrixComponent('UnitClusterImage__400_linear_max_-99_Dist.pckl','Distance Before Clustering',Greens,50,400)
Section1BeforeBar = LoadFullMatrixComponent('UnitClusterImage__400_linear_max_-99_Bar.pckl','Cluster Number Before Clustering',PuRd,50,400)
Section1Before = panel.Column(Section1BeforeMat,Section1BeforeDist,Section1BeforeBar, margin = (0,0,0,0))

Section1AfterMat = LoadFullMatrixComponent('UnitClusterImage_Permuted_400_linear_max_-99_Mat.pckl','Proximity Matrix After Clustering',PuBu,400,400)
Section1AfterDist = LoadFullMatrixComponent('UnitClusterImage_Permuted_400_linear_max_-99_Dist.pckl','Distance After Clustering',Greens,50,400)
Section1AfterBar = LoadFullMatrixComponent('UnitClusterImage_Permuted_400_linear_max_-99_Bar.pckl','Cluster Number After Clustering',PuRd,50,400)
Section1After = panel.Column(Section1AfterMat,Section1AfterDist,Section1AfterBar, margin = (0,0,0,0))

Section1ProximityTabs = panel.layout.Tabs (
                                        ('Zoomed Unit Proximity',Section1DiagramNLP),
                                        ('Before Clustering',Section1Before),
                                        ('After Clustering',Section1After),
                                        margin = (0,0,0,0), 
                                        )

Section1NLP = panel.Column(Section1HeaderNLP,Section1ProximityTabs)

Section1Bottom = panel.Row(Section1NLP, Section1WebKeyElements )

Section1 = panel.Column( Section1Method,  Section1Bottom)


TableCSS = """
div.special_table + table, th, td {
  border: 1px solid blue;
}
"""

panel.extension(raw_css=[TableCSS])

Section3SupervisedMachineLearningOverview = panel.panel("""<div class="special_table"></div>
# Supervised Machine Learning for Mapping units

## Difficulties:
- There are too many target units to use ordinary classification
- Many units map to the same result so the translation is many-to-one rather than one-to-one
- Data distribution is unbalanced with many examples for some mappings
- Context of units has a large vocabulary 
- Training data is limited - although growing in time

## Multiple Solutions Attempted
| Solution                                   | Main Layers         | Encoding            | Comments                                                                                                             | References |
|--------------------------------------------|---------------------|---------------------|----------------------------------------------------------------------------------------------------------------------|------------|                                 
| Simple Classification                      | Dense               | One Hot / Feature   | Simple solution, yet this problem has many classes and therefore not practical                                       |[1](https://machinelearningmastery.com/tutorial-first-neural-network-python-keras/), [2](https://machinelearningmastery.com/how-to-one-hot-encode-sequence-data-in-python/)     |
| Feature Classification                     | LSTM / CNN          | One Hot             | Can be simple and fast yet requires mapping and sensitive and complex features require dealing with sequences        |[3](https://scikit-learn.org/stable/modules/feature_extraction.html)          |
| Sequence to Sequence Preset Length         | LSTM / CNN          | One Hot / Embedding | Relatively simple flexible and reliable, training reasonable, and inference is reasonably fast                       |[4](https://machinelearningmastery.com/develop-character-based-neural-language-model-keras/), [5](https://blog.keras.io/a-ten-minute-introduction-to-sequence-to-sequence-learning-in-keras.html), [6](https://medium.com/@jon.froiland/convolutional-neural-networks-for-sequence-processing-part-1-420dd9b500)      |
| Sequence to Sequence Encoder/Decoder       | LSTM                | One Hot / Embedding | Works well for short sequences, non trivial implementation. However slow inference since GPU is not used in decoding |[5](https://blog.keras.io/a-ten-minute-introduction-to-sequence-to-sequence-learning-in-keras.html), [7](https://keras.io/examples/lstm_seq2seq/), [8](https://towardsdatascience.com/how-to-implement-seq2seq-lstm-model-in-keras-shortcutnlp-6f355f3e5639), [9](https://machinelearningmastery.com/define-encoder-decoder-sequence-sequence-model-neural-machine-translation-keras/), [10](https://machinelearningmastery.com/develop-encoder-decoder-model-sequence-sequence-prediction-keras/)  |
| Learning to Rank - Pairwise                | CNN + Dense Twin    | Embedding           | High complexity O(N^2) difficult inference due to pairwise nature                                                    |[11](https://icml.cc/2015/wp-content/uploads/2015/06/icml_ranking.pdf), [12](https://github.com/airalcorn2/RankNet), [13](https://github.com/ysyyork), [14](https://arxiv.org/pdf/1802.08988.pdf), [15](https://github.com/eggie5/RankNet) |     |

## Chosen Solution Implemented Sequence to Sequence Networks so the Modeler Can:
- Control:
    - switch neural network architecture 
    - decide on execution mode: New Netowrk, retrain old, or just test or plot using previously trained network
- Preprocessing:
    - add noise to input units simulating typing errors, and control noise type
    - decide if to duplicate dataset without one or more inputs to test missing unit context
- Neural Network Inputs:
    - decide if to use unit input as one hot
    - decide if to use unit input as integer for embedding
    - decide if to use unit context as input
    - decide if to add input attention to unit input when using both one hot and integer
- Training:
    - decide network layer sizes and network depth
    - decide if to use LSTM or CNN for context
    - decide if to use LSTM or CNN for Units - only LSTM in Encoder/Decoder architecture
    - set dropout rate for LSTM
    - determine input data clusters used when training - automate multiple networks for multiple clusters
- Debug:
    - request accumulated training history even when retrained
    - look inside network layers of interest during training - this is beyond tensorboard support - implemented with PyViz
- Post-Processing:
    - choose inference from between best Validation model. last trained model, or both
    - decide on verbosity of output - e.g. number of closest units to output
- More Details:
    - Mock training data mapped 24,548 units to 6,891 mock interpretations derived from clustering.
    - In addition, post processing matched char sequence output to allowed unit interpretations within the same cluster.
    - Closest units with a certain distance from prediction were explored for accuracy.
    - Multiple distance metrics were used to deduce closest unit to predicted string.
""", width=Width, height=250)




def GeneratePlot(InputFile, Title, Footer):
    "Generate a plot for clusters processed"

    holoviews.extension('bokeh')    
    PlotsDict = {}
    
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
    TempFile = open(DataDir+os.sep+InputFile,'rb')
    (PredictionQualities) = pickle.load(TempFile)
    TempFile.close()
        
    for (IsValidationPass, PhaseText) in enumerate(PhaseTexts):
        for (PassTypeNumber, PassTypeText) in enumerate(PassTypeTexts):
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
                HistogramShortTitle = holoviews.Histogram((Edges, FrequencesToUse)).redim.label(x='Quality', Frequency = ['Cumulative Proportion','Proportion'][IsPlotTypeBoolean]).opts( title = PlotTypeName, tools = ['hover'], ylim =(0,1), color = ['Blue','Red'][IsPlotTypeBoolean], height=135 , width=230-100*IsPlotTypeBoolean, toolbar = None, fontsize={'title': 8, 'labels': 8, 'xticks': 6, 'yticks': 6}, xticks=LabelsX)    
                PlotsDict[(PhaseText,PassTypeText,PlotTypeName)] = HistogramShortTitle

    PlotList = [  (PhaseText + ' ' + PassTypeText  , [ panel.pane.HoloViews(PlotsDict[(PhaseText,PassTypeText,PlotTypeName)]) for (PlotTypeName,IsPlotTypeBoolean) in (PlotTypes)]) for PhaseText in PhaseTexts for PassTypeText in PassTypeTexts ] 
    CombinedList = [panel.panel(Title,height=50, margin = (0,0,0,0))]
    for (PlotTitle,PlotRows) in PlotList:
        CombinedList.append(panel.panel('#### '+PlotTitle,height=35, margin = (0,0,0,0)))
        CombinedList.append(panel.Row(*PlotRows, margin = (0,0,0,0)))
    CombinedList.append(panel.panel(Footer,height=10, margin = (0,0,0,0)))
    ConstrcutedGrid = panel.Column(*CombinedList, margin = (0,0,0,0), linked_axes=False)
    return ConstrcutedGrid


Section4SupervisedMachineLearningHeader = panel.panel("# Neural Network Training and Validation Results For Multiple Architectures", width=Width, height=55)
Section4SupervisedMachineLearningFooter = 'Rows = input scenarios: unit / context / both. Columns = comparison metrics: <span style="color:red">Red= first prediction attempt accuracy</span>.  <span style="color:Blue">Blue = prediction quality with multiple close units. </span>'
                                                      
Section4SupervisedMachineLearningResults1 = GeneratePlot('Seq2Seq_SummaryStats_Last_Batch_1.pckl', '## Sequence to Sequence Encoder Decoder',Section4SupervisedMachineLearningFooter)
Section4SupervisedMachineLearningResults2 = GeneratePlot('UnitLSTMContextLSTM_SummaryStats_Last_Batch_1.pckl', '## Sequence to Sequence LSTM for Unit LSTM for Context',Section4SupervisedMachineLearningFooter)
Section4SupervisedMachineLearningResults3 = GeneratePlot('UnitLSTMContextCNN_SummaryStats_Last_Batch_1.pckl', '## Sequence to Sequence LSTM for Unit CNN for Context',Section4SupervisedMachineLearningFooter)
Section4SupervisedMachineLearningResults4 = GeneratePlot('UnitCNNContextCNN_SummaryStats_Last_Batch_1.pckl', '## Sequence to Sequence CNN for Unit CNN for Context',Section4SupervisedMachineLearningFooter)

Section4SupervisedMachineLearningTabs = panel.layout.Tabs (
                                        ('Encoder Decoder',Section4SupervisedMachineLearningResults1),
                                        ('LSTM Unit LSTM Context', Section4SupervisedMachineLearningResults2),
                                        ('LSTM Unit CNN Context', Section4SupervisedMachineLearningResults3),
                                        ('CNN Unit CNN Context', Section4SupervisedMachineLearningResults4),
                                        margin = (0,0,0,0), 
                                        )


Section4 = panel.Column(Section4SupervisedMachineLearningHeader,Section4SupervisedMachineLearningTabs, margin = (0,0,0,0))


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
    - Grace Peng for maitaining the IMAG community and connecting to the NLM team
* Thanks to Paul Schluter for information about RTMMS and the IEEE unit standard
* Thanks for Tipton Cole, Rocky Reston, Andrew Simms for useful directions
* Thanks to Becky Ruppel, Yuval Merchav Uri Goren, Ari Bornstein, Ryan Baxley, Bhargav Srinivasa Desikan, Blaize Berry for NLP advise 

## Reproducibility:

This presentation is accessible [here](%s). The code that generated the presentation can be accessed [here](%s). This presentation is generated using Python 2.7.16, panel-0.5.1, holoviews 1.12.3, bokeh-1.1.0.
Code and data for this work are archived in the file: AnalyzeCT_2019_05_13.zip. Web site database was created using the database PartUnitsDB_2019_05_13.db Supplemental code archived in the files: AnalyzeCT_Images_2019_10_10.zip, AnalyzeCT_Code_2019_05_15.zip. 
Clinical Trials data archived in StudiesWithResults_Downloaded_2019_04_12.zip. Bio Ontology Units downloaded on 2019_04_09, CDISC data downloaded on 2019_03_30 , RTMMS units downloaded on 2019_03_24 . Mock database used in training was ModifiedUnitsDB_Remodified.db .
Tensorflow 2.0.0 was used for Neural Network execution in Python 3.7.4 environment . This tensorflow version is unstable, so results presented may not be reproducible. PYTHONHASHSEED was set to 0. Execution transcripts were saved in the files: AnalyzeCT_TF2_LargeMod_Mixed_LSTM_Unit_LSTM_Context_NewMetric_2019_10_14.zip , AnalyzeCT_TF2_LargeMod_Seq2Seq_NewMetric_2019_10_15.zip , AnalyzeCT_TF2_LargeMod_Mixed_LSTM_Unit_CNN_Context_NewMetric_2019_10_15.zip , AnalyzeCT_TF2_LargeMod_Mixed_CNN_Unit_CNN_Context_NewMetric_2019_10_15.zip . 

## Publications:

* J. Barhak, The Reference Model Models ClinicalTrials.Gov. SummerSim 2017 July 9-12, Bellevue, WA. [Paper](https://doi.org/10.22360/SummerSim.2017.SCSC.022)
* J. Barhak, The Reference Model: A Decade of Healthcare Predictive Analytics with Python, PyTexas 2017, Nov 18-19, 2017, Galvanize, Austin TX. [Video](https://youtu.be/Pj_N4izLmsI)
* J. Barhak, C. Myers, L. Watanabe, L. Smith, M. J. Swat , Healthcare Data and Models Need Standards. Simulation Interchangeability Standards Organization (SISO) 2018 Fall Innovation Workshop.  9-14 Sep 2018 Orlando, Florida [Presentation](https://www.sisostds.org/DesktopModules/Bring2mind/DMX/API/Entries/Download?Command=Core_Download&EntryId=47969&PortalId=0&TabId=105)
* J. Barhak, Python Based Standardization Tools for ClinicalTrials.Gov. Combine 2018 . Boston University [Poster](http://co.mbine.org/system/files/COMBINE_2018_Barhak.pdf)
* J. Barhak, J. Schertz, Clinical Unit Mapping for Standardization of ClinicalTrials.Gov . MSM/IMAG meeting. IMAG Multiscale Modeling (MSM) Consortium Meeting March 6-7, 2019 @ NIH, Bethesda, MD . [Poster](https://jacob-barhak.github.io/InteractivePoster_MSM_IMAG_2019.html)
* J. Barhak, Clinical Data Modeling with Python, AnacondaCon , Austin, Texas,  April 3-5, 2019. [Video](https://youtu.be/fQIYMf5wKGE) , [Presentation](https://jacob-barhak.github.io/AnacondaCon_2019.html) 
* J. Barhak, J. Schertz, Standardizing Clinical Data with Python . PyCon Israel 3-5 June 2019, [Video](https://youtu.be/vDXyCb60L5s)  [Presentation](https://jacob-barhak.github.io/Presentation_PyConIsrael2019.html) 
* J. Barhak, J. Schertz, Clinical Unit Mapping with Multiple Standards . 2019 CDISC U.S. Interchange, [Poster](https://jacob-barhak.github.io/Poster_CDISC2019.html) 
"""%(PublishURL,CodePublishURL), width=Width, height=600)



Section5 =  panel.Column(Section5Summary,Section5AdditionalInfo, margin = (0,0,0,0))





SectionSelectorTab = panel.layout.Tabs (
                                        ('Preface',Section0),
                                        ('Solution Outline ClinicalUnitMapping.com', Section1),

                                        ('Supervised Machine Learning', Section3SupervisedMachineLearningOverview),
                                        ('Preliminary Results', Section4),
                                        ('Summary', Section5),
                                        margin = (0,0,0,0), 
                                        )
                                        
Presentation = panel.Column(PresentationHeader, SectionSelectorTab)
Presentation.save(SavedFileName, resources=INLINE, title=TitleHTML)       

