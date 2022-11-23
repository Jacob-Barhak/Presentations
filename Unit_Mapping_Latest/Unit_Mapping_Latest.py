###############################################################################
# Copyright (C) 2019,2020,2022 Jacob Barhak
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
# without their support and development of HoloViz visualization tools, this
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
# directory to read/write html resources
ResourceDir = 'Resources' 


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
    'Encodes html from a file into a panel object'
    DataFile = open(ExtrnalFileName,'rb')
    Data = DataFile.read()
    DataFile.close()
    Figure_4 = panel.pane.HTML(Data, width=Width, height=Height, margin = (0,0,0,0))
    return Figure_4

def VideoInlineHTML(ExtrnalFileName,Width=Width,Height=700, EmbedVideo = EmbedVideo):
    'Encodes html from a file into video'
    if EmbedVideo:
        ExtrnalData = CovertFileToData(ExtrnalFileName)
        RetStr = '<Video width="%i" height="%i" controls>   <source src="%s" type="video/mp4">  Warning:%s could not be included! </Video>'%(Width, Height, 'data:video/mp4;base64,'+ExtrnalData,ExtrnalFileName)
    else:
        RetStr = '<Video width="%i" height="%i" controls>   <source src="%s" type="video/mp4">  Warning:%s could not be included! </Video>'%(Width, Height, ExtrnalFileName,ExtrnalFileName)
    return RetStr



BokehDocument = bokeh.document.Document()


TitleHTML = 'ClinicalUnitMapping.Com Takes a Small Step Towards Machine Comprehension of Clinical Trial Data'
SavedFileName = 'Unit_Mapping_Latest.html'
PublishURL = 'https://jacob-barhak.github.io/'+SavedFileName
CodePublishURL = 'https://github.com/Jacob-Barhak/Presentations/tree/master/Unit_Mapping_Latest'
QRCodeFileName = 'Unit_Mapping_Latest.png'


PresentationURL = panel.panel(ConstractImageLinkAnchor(PublishURL,QRCodeFileName,'View this presentation on the web',480), width=480, height=480)

PresentationTitle = panel.panel('# ClinicalUnitMapping.Com Takes a Small Step Towards Machine Comprehension of Clinical Trial Data', width=700, height=80, margin = (0,0,0,0))
PresentationVenue = panel.panel('[CHRONIC DISEASES & INFECTIOUS DISEASES   24-NOV-2022, Paris, France](https://www.chronicdiseases.scientexconference.com/)', width=300, height=80, margin = (0,0,0,0))
PresentationAuthors = panel.panel("By: [Jacob Barhak](http://sites.google.com/site/jacobbarhak/) </br> & [Joshua Schertz](https://joshschertz.com/)", width=120, height=80, margin = (0,0,0,0))
PresentationHeader = panel.Row ( PresentationTitle,  PresentationAuthors , PresentationVenue, margin = (0,0,0,0))






Section0AbstractText = panel.panel("""# Abstract
ClinicalTrials.Gov is the database storing data from clinical trials. Many clinical trials are required to report their findings in this database according to U.S. law. On 2022-08-26 this database held 425,969 clinical trials with 55,248 trials having numeric results. However,  the data is not standardized and numerical data cannot be comprehended since the units are not standardized.. There were 36,752 unique units of measure compared to 2019-04-12 when there were 24,548 unique units of measure. It is an increase of 12,204 units over roughly 40 months. - almost 10 new unique units of measure added per day. To use the numerical data in disease modeling, there is a need to have machine support to standardize this data 

ClinicalUnitMapping.Com is a web tool constructed to help standardize this data and merge it with the following standards and specifications: UCUM, RTMMS / IEEE 11073-10101, BIOUO, and CDISC. IEEE 11073-10101 - ***Adapted and reprinted with permission from IEEE. Copyright IEEE 2019.  All rights reserved.***

This presentation will discuss how python tools are used to 1) process and index the data, 2) find similar units using NLP and machine learning, 3) create a web interface to support user mapping of those units. 

The intention is to unify unit standards and machine learning tools that will be able to map all units reported by clinical trials. With such capabilities, the data in this important clinical trials database would become machine comprehensible.

""", width=700, height=500)


Section0SubHeader = panel.panel('## Longer Term Motivation: Computer Automation of Human Reasoning', width=900, height=20)

                                
                                
Section0ChronologyFigure = panel.panel(ConstractImageLinkAnchor('https://en.wikipedia.org/wiki/Computer_chess','ComputerInfluenceDiagram.png','Towards Computer Automation of Human tasks - Main sources Wikipedia Computer Chess and Wikipedia self-driving car',1000), width=1000, height=700)

Section0 = panel.Column(Section0AbstractText, Section0SubHeader, Section0ChronologyFigure)
   
   
    
    
    
Section1MethodText = panel.panel("""# Proposed Solution

## 1. Aggregate and index all ClinicalTrials.Gov units

## 2. Gather auxiliary unit standards / specifications:

### - [CDISC](https://www.cdisc.org/) - Clinical Data Interchange Standards Consortium
### - [RTMMS / IEEE](https://rtmms.nist.gov/rtmms/) - affiliated with NIST / IEEE 11073-10101
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



Section1WebSiteStaticImage = panel.panel(ConstractImageLinkAnchor('https://clinicalunitmapping.com/','ClinicalUnitMappingScreenShot.png','ClinicalUnitMapping.com web site',600), width=600, height=500)

Section1WebKeyElements = panel.Row(Section1WebKeyPoints, Section1WebSiteStaticImage)



def LoadHoloviewsComponent(FileName, Title, ColorMap, PlotHeight, PlotWidth):
    "load larger matrix components and build an object with options"
    DataFile = open(DataDir+os.sep+FileName,'rb')
    HoloviewsObjectTuple = pickle.load(DataFile)
    DataFile.close()
    if Title != None :
        HoloviewsObject = HoloviewsObjectTuple
        RevisedObject = HoloviewsObjectTuple.opts(cmap=ColorMap, title = Title, xaxis=None, yaxis=None,  height=PlotHeight, width=PlotWidth, tools=['hover'], toolbar = None, axiswise=True)
    elif ColorMap == None:
        HoloviewsObjectName, HoloviewsObject = HoloviewsObjectTuple
        RevisedObject = HoloviewsObject.opts(title = 'Model Accuracy', xlabel = 'Epoch', ylabel = 'Accuracy', legend_position='bottom_right', ylim=(0, 1), height=PlotHeight, tools=['hover'] , width=PlotWidth, toolbar = None)
        for (ElementKey,ElementItem) in RevisedObject.items():
            RevisedObject[ElementKey] = ElementItem.redim.label(x='Epoch',y='Accuracy').opts( tools = ['hover'])
    else:
        HoloviewsObjectName, HoloviewsObject = HoloviewsObjectTuple
        RevisedObject = HoloviewsObject.redim.label(x='Neural Unit Number ',y='Time', z= 'Value' )
        RevisedObject.opts(cmap=ColorMap, title = 'Weight Matrix ' + HoloviewsObjectName, xaxis='top', yaxis='left', height=PlotHeight, width=PlotWidth, tools=['hover'], axiswise=True, toolbar = None)
    return RevisedObject




Section1Bottom = Section1WebKeyElements 

Section1 = panel.Column( Section1Method,  Section1Bottom)

Section2_1 = panel.panel("""### Unsupervised Machine Learning - Feature Extraction""", width=Width, height=25, margin = (0,0,0,0))


Figure_2_1 = ObjectInlineHTML(ResourceDir + '/units_original_features.html', Width=1150, Height=515)

Section2_2 = panel.panel("""### Units Proximity and Clustering into Groups of Units""", width=Width, height=5, margin = (0,0,0,0))


Figure_2_2 = ObjectInlineHTML(ResourceDir + '/units_combined_matches_matrix.html', Width=1150, Height=550)

Section2 = panel.Column(Section2_1, Figure_2_1, Section2_2, Figure_2_2, margin = (0,0,0,0))


TableCSS = """
div.special_table + table, th, td {
  border: 1px solid blue;
}
"""

panel.extension(raw_css=[TableCSS])

Section3SupervisedMachineLearningOverview = panel.panel("""<div class="special_table"></div>
# Supervised Machine Learning for Mapping units

## Difficulties:
- There are too many target units to use ordinary classification while training data is limited
- Many units map to the same result so the translation is many-to-one rather than one-to-one
- Data distribution is unbalanced with many examples for some mappings

## Multiple Solutions Attempted
| Solution                             | Main Layers       | Encoding            | Comments                                                                                                          | References |
|--------------------------------------|-------------------|---------------------|-----------------------------------------------------------------------------------------------------------------|------------|                                 
| Simple Classification                | Dense             | One Hot / Feature   | Simple solution, yet this problem has many classes and therefore not practical                                    |[1](https://machinelearningmastery.com/tutorial-first-neural-network-python-keras/), [2](https://machinelearningmastery.com/how-to-one-hot-encode-sequence-data-in-python/)     |
| Feature Classification               | LSTM / CNN        | One Hot             | Can be simple and fast yet requires mapping and sensitive and complex features require dealing with sequences     |[3](https://scikit-learn.org/stable/modules/feature_extraction.html)          |
| Sequence to Sequence Preset Length   | LSTM / CNN        | One Hot / Embedding | Relatively simple flexible and reliable, training reasonable, fast inference                                      |[4](https://machinelearningmastery.com/develop-character-based-neural-language-model-keras/), [5](https://blog.keras.io/a-ten-minute-introduction-to-sequence-to-sequence-learning-in-keras.html), [6](https://medium.com/@jon.froiland/convolutional-neural-networks-for-sequence-processing-part-1-420dd9b500)      |
| Sequence to Sequence Encoder/Decoder | LSTM              | One Hot / Embedding | Works well for short sequences, non trivial implementation. Slow inference (no GPU)                               |[5](https://blog.keras.io/a-ten-minute-introduction-to-sequence-to-sequence-learning-in-keras.html), [7](https://keras.io/examples/lstm_seq2seq/), [8](https://towardsdatascience.com/how-to-implement-seq2seq-lstm-model-in-keras-shortcutnlp-6f355f3e5639), [9](https://machinelearningmastery.com/define-encoder-decoder-sequence-sequence-model-neural-machine-translation-keras/), [10](https://machinelearningmastery.com/develop-encoder-decoder-model-sequence-sequence-prediction-keras/)  |
| Learning to Rank - Pairwise          | CNN & Dense-Twin  | Embedding           | High complexity O(N^2) difficult inference due to pairwise nature                                                 |[11](https://icml.cc/2015/wp-content/uploads/2015/06/icml_ranking.pdf), [12](https://github.com/airalcorn2/RankNet), [13](https://github.com/ysyyork), [14](https://arxiv.org/pdf/1802.08988.pdf), [15](https://github.com/eggie5/RankNet) |




## Chosen Solution Implemented Sequence to Sequence Networks so the Modeler Can:
- Control:
    - switch neural network architecture 
    - decide on execution mode: New Network, retrain old, or just test or plot using previously trained network
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
    - look inside network layers of interest during training - this is beyond tensorboard support - implemented with HoloViz
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
                HistogramShortTitle = holoviews.Histogram((Edges, FrequencesToUse)).redim.label(x='Quality', Frequency = ['Cumulative Proportion','Proportion'][IsPlotTypeBoolean]).opts( title = PlotTypeName, tools = ['hover'], ylim =(0,1), color = ['Blue','Red'][IsPlotTypeBoolean], height=135 , width=230-100*IsPlotTypeBoolean, toolbar = None, fontsize={'title': 8, 'labels': 8, 'xticks': 6, 'yticks': 6}, xticks=LabelsX, shared_axes=False)    
                PlotsDict[(PhaseText,PassTypeText,PlotTypeName)] = HistogramShortTitle

    PlotList = [  (PhaseText + ' ' + PassTypeText  , [ panel.pane.HoloViews(PlotsDict[(PhaseText,PassTypeText,PlotTypeName)]) for (PlotTypeName,IsPlotTypeBoolean) in (PlotTypes)]) for PhaseText in PhaseTexts for PassTypeText in PassTypeTexts ] 
    CombinedList = [panel.panel(Title,height=50, margin = (0,0,0,0))]
    for (PlotTitle,PlotRows) in PlotList:
        CombinedList.append(panel.panel('#### '+PlotTitle,height=35, margin = (0,0,0,0)))
        CombinedList.append(panel.Row(*PlotRows, margin = (0,0,0,0)))
    CombinedList.append(panel.panel(Footer,height=10, margin = (0,0,0,0)))
    ConstrcutedGrid = panel.Column(*CombinedList, margin = (0,0,0,0))
    return ConstrcutedGrid


Section4SupervisedMachineLearningHeader = panel.panel("# Neural Network Training and Validation Results For Multiple Architectures", width=Width, height=55)
Section4SupervisedMachineLearningFooter = 'Rows = input scenarios: unit / context / both. Columns = comparison metrics: <span style="color:red">Red= first prediction attempt accuracy</span>.  <span style="color:Blue">Blue = prediction quality with multiple close units. </span>'
                                                      
Section4SupervisedMachineLearningResults1 = GeneratePlot('Seq2Seq_SummaryStats_Last_Batch_1.pckl', '## Sequence to Sequence Encoder Decoder',Section4SupervisedMachineLearningFooter)
Section4SupervisedMachineLearningResults2 = GeneratePlot('UnitLSTMContextLSTM_SummaryStats_Last_Batch_1.pckl', '## Sequence to Sequence LSTM for Unit LSTM for Context',Section4SupervisedMachineLearningFooter)
Section4SupervisedMachineLearningResults3 = GeneratePlot('UnitLSTMContextCNN_SummaryStats_Last_Batch_1.pckl', '## Sequence to Sequence LSTM for Unit CNN for Context',Section4SupervisedMachineLearningFooter)
Section4SupervisedMachineLearningResults4 = GeneratePlot('UnitCNNContextCNN_SummaryStats_Last_Batch_1.pckl', '## Sequence to Sequence CNN for Unit CNN for Context',Section4SupervisedMachineLearningFooter)


TrainingAbstract = panel.panel("""## Who Said Machine Learning is a Black Box?
## One can easily look inside using HoloViz!

* It is possible to see the training history by using interactivity.
* It is possible to view the weights of a neural network layer change during training

## HoloViz Makes the black box transparent!""", width=Width, height=200, margin = (0,0,0,0))
TrainingHistory = LoadHoloviewsComponent('history_History.pckl',None,None, 190,600)
TrainingDebug1 = LoadHoloviewsComponent('history_Layer_EncoderLSTM_bias_0.pckl',None,PuBu,600,600)
TrainingDebug2 = LoadHoloviewsComponent('history_Layer_EncoderLSTM_kernel_0.pckl',None,PuBu,600,600)
TrainingDebug3 = LoadHoloviewsComponent('history_Layer_EncoderLSTM_recurrent_kernel_0.pckl',None,PuBu,600,600)

TrainingDebugTabs = panel.layout.Tabs (
                                        ('LSTM Bias', TrainingDebug1),
                                        ('LSTM Kernel', TrainingDebug2),
                                        ('LSTM Recurrent Kernel', TrainingDebug3),
                                        margin = (0,0,0,0), 
                                        )
Training = panel.Column( TrainingAbstract, TrainingHistory, TrainingDebugTabs, margin = (0,0,0,0))

Section4SupervisedMachineLearningTabs = panel.layout.Tabs (
                                        ('Encoder Decoder',Section4SupervisedMachineLearningResults1),
                                        ('LSTM Unit LSTM Context', Section4SupervisedMachineLearningResults2),
                                        ('LSTM Unit CNN Context', Section4SupervisedMachineLearningResults3),
                                        ('CNN Unit CNN Context', Section4SupervisedMachineLearningResults4),
                                        ('Looking Inside the Black Box', Training),
                                        margin = (0,0,0,0), 
                                        )


Section4 = panel.Column(Section4SupervisedMachineLearningHeader,Section4SupervisedMachineLearningTabs, margin = (0,0,0,0))




Section6SummaryText = panel.panel("""# Summary
### We created tools necessary to merge units of measure standards.
### With such tools is will be possible for machines to:
### - Recognize medical units, even if misspelled
### - Comprehend medical units
### - Comprehend numbers associated with units
### Such AI will eventually replace tedious human tasks.
<br>
### Future work will focus on improving supervised learning
<br>
### Publications available at: [ClinicalUnitMapping.com/about](https://clinicalunitmapping.com/about)

""", width=600, height=300)

Section6Summary = panel.Row(Section6SummaryText,PresentationURL, margin = (0,0,0,0))

Section6AdditionalInfo = panel.panel("""

## Reproducibility:

This presentation is accessible [here](%s). The code that generated the presentation can be accessed [here](%s). This presentation is generated using Python 2.7.16, panel-0.8.0, holoviews 1.12.7, bokeh-1.4.0.
Code for ingestion and clustering are archived in the file: AnalyzeCT_2022_11_19.zip. Web site database was created using the database PartUnitsDB_2019_05_13.db Supplemental code archived in the files: AnalyzeCT_Images_2019_10_10.zip, AnalyzeCT_Code_2019_05_15.zip. 
Clinical Trials data archived in AllPublicXML_2022_08_26.zip and in StudiesWithResults_Downloaded_2019_04_12.zip. Bio Ontology Units downloaded on 2019_04_09, CDISC data downloaded on 2019_03_30 , RTMMS units downloaded on 2019_03_24 . Mock database used in training was ModifiedUnitsDB_Remodified.db .
Tensorflow 2.0.0 was used for Neural Network execution in Python 3.7.4 environment . This tensorflow version is unstable, so results presented may not be reproducible. PYTHONHASHSEED was set to 0. Executions archived in: AnalyzeCT_TF2_LargeMod_Mixed_LSTM_Unit_LSTM_Context_NewMetric_2019_10_14.zip , AnalyzeCT_TF2_LargeMod_Seq2Seq_NewMetric_2019_10_15.zip , AnalyzeCT_TF2_LargeMod_Mixed_LSTM_Unit_CNN_Context_NewMetric_2019_10_15.zip , AnalyzeCT_TF2_LargeMod_Mixed_CNN_Unit_CNN_Context_NewMetric_2019_10_15.zip , AnalyzeCT_TF2_Small_Mixed_LSTM_Unit_LSTM_Context_DebugPlots_2019_12_05.zip.

## Acknowledgments: 
* *** IEEE 11073-10101 - Adapted and reprinted with permission from IEEE. Copyright IEEE 2019.  All rights reserved.***
* Many thanks to the HoloViz team: Philipp Rudiger, James Bednar, Jean-Luc Stevens.
* Thanks to John Rice for the fruitful discussions regarding standardization
* Thanks to Government individuals: Nick Ide (NIH/NLM), Erin E Muhlbradt (NIH/NCI) , John Garguilo (NIST) , Grace Peng (NIH/NIBIB) 
* Thanks to Paul Schluter, Tipton Cole, Rocky Reston, Andrew Simms for useful tips on units
* Thanks to Becky Ruppel, Yuval Merchav Uri Goren, Ari Bornstein, Ryan Baxley, Bhargav Srinivasa Desikan, Blaize Berry for NLP advise 


### Conflict of Interest Statement:
Payment/services info: Dr. Barhak reports non-financial support and other from Rescale, and MIDAS Network, other from Amazon AWS, Microsoft Azure, MIDAS network, other from The COVID tracking project at the Atlantic,  other from John Rice and Jered Hodges, 
Financial relationships: Jacob Barhak declare(s) employment from MacroFab, United Solutions, B. Well Connected health. The author had a contract with U.S. Bank / Apexon, MacroFab, United Solutions, and B. Well during the work. However, none of these companies had influence on the modeling work reported in the paper. Jacob Barhak declare(s) employment and Technical Support from Anaconda. The author contracted with Anaconda in the past and uses their free open source software tools. Also the Author received free support from Anaconda Holoviz team and Dask teams. Intellectual property info: Dr. Barhak has a patent US Patent 9,858,390 - Reference model for disease progression issued to Jacob Barhak, and a patent US patent Utility application #15466535 - Analysis and Verification of Models Derived from Clinical Trials Data Extracted from a Database. Other relationships: During the conduct of the study; personal fees from United Solutions, personal fees from B. Well Connected health, personal fees and non-financial support from Anaconda, outside the submitted work; In addition, Dr. Barhak has a patent US Patent 9,858,390 - Reference model for disease progression issued to Jacob Barhak, and a US patent Number 10,923,234 - Analysis and Verification of Models Derived from Clinical Trials Data Extracted from a Database pending to Jacob Barhak and The author was engaged with a temporary team formed for a duration of the Pandemic Response Hackathon. The team consisted of Christine Mary, Doreen Darsh, Lisbeth Garassino . They supported work during the Hackathon in initial stages of this work. Many others have expressed their support in this project. This has been publicly reported here: https://devpost.com/software/improved-disease-modeling-tools-for-populations . However, despite all support, Dr. Barhak is solely responsible for modeling decisions made for this paper an is responsible for its contents.
"""%(PublishURL,CodePublishURL), width=Width, height=800)


Section6 =  panel.Column(Section6Summary,Section6AdditionalInfo, margin = (0,0,0,0))




SectionSelectorTab = panel.layout.Tabs (
                                        ('Preface',Section0),
                                        ('Solution Outline', Section1),
                                        ('Unsupervised Machine Learning', Section2),

                                        ('Supervised Machine Learning', Section3SupervisedMachineLearningOverview),
                                        ('Supervised Machine Learning Preliminary Results', Section4),
                                        
                                        ('Summary', Section6),
                                        margin = (0,0,0,0), 
                                        )
                                        
Presentation = panel.Column(PresentationHeader, SectionSelectorTab)
Presentation.save(SavedFileName, resources=INLINE, title=TitleHTML)       

