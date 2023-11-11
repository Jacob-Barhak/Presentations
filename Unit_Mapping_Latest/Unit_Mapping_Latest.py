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
import re

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

def ExtractReferencesDict(ReferenceText):
    "Create Reference Dictionary from Text"
    Lines = ReferenceText.split("\n")
    RefDict = {}
    for Line in Lines:
        CandidateNumber = Line.split('.')[0]
        try:
            Number = int(CandidateNumber)
        except:
            Number = None
        if Number:
            NumberStr = str(Number)
            LineText = Line[1+len(NumberStr):].strip()
            ReplacedLineText = LineText.replace('<','').replace('>','')
            LineComponents = LineText.split()
            LineLink = ""
            for LineComponent in LineComponents:
                if LineComponent.startswith("<http") and LineComponent.endswith(">"):
                    # collect the first element
                    LineLink = LineComponent[1:-1]
                    break
            if LineLink == "":
                print "Check Reference :" + Line
            RefDict[NumberStr] = (LineLink, ReplacedLineText)
    return RefDict



def FixReferences(RefDict, Text):
    'Add Links to Reference'
    def ReplaceWith(matchobj):
        ToBeRepalced = matchobj.group(0)
        RefNumber = ToBeRepalced[1:-1]
        (RefLink, RefText) = RefDict[RefNumber]
        ReplaceText = '<a href="%s" title="%s" target= "_blank">%s</a>' % (RefLink, RefText, ToBeRepalced)
        return ReplaceText
    ReplacedText = re.sub("\[\d\]|\[\d\d\]", ReplaceWith, Text)
    return ReplacedText




BokehDocument = bokeh.document.Document()


TitleHTML = 'ClinicalUnitMapping.Com Takes a Small Step Towards Machine Comprehension of Clinical Trial Data'
SavedFileName = 'Unit_Mapping_Latest.html'
PublishURL = 'https://www.clinicalunitmapping.com/show/'+SavedFileName
CodePublishURL = 'https://github.com/Jacob-Barhak/Presentations/tree/master/Unit_Mapping_Latest'
QRCodeFileName = 'New_Unit_Mapping_Latest.png'


PresentationURL = panel.panel(ConstractImageLinkAnchor(PublishURL,QRCodeFileName,'View this presentation on the web',480), width=480, height=480)

PresentationTitle = panel.panel('# ClinicalUnitMapping.Com Takes a Small Step Towards Machine Comprehension of Clinical Trial Data', width=700, height=80, margin = (0,0,0,0))
PresentationVenue = panel.panel('[CAFCW23</br>Computational Approaches for Cancer Workshop</br>November 12, 2023](https://ncihub.cancer.gov/groups/cafcw/cafcw23/cafcw23_program)', width=300, height=80, margin = (0,0,0,0))
PresentationAuthors = panel.panel("By: [Jacob Barhak](http://sites.google.com/site/jacobbarhak/) </br> & [Joshua Schertz](https://joshschertz.com/)", width=120, height=80, margin = (0,0,0,0))
PresentationHeader = panel.Row ( PresentationTitle,  PresentationAuthors , PresentationVenue, margin = (0,0,0,0))


ReferencesText = """### References


1. Jason Brownlee, Your First Deep Learning Project in Python with Keras Step-by-Step, Online: <https://machinelearningmastery.com/tutorial-first-neural-network-python-keras/>
2. Jason Brownlee, How to One Hot Encode Sequence Data in Python, Online: <https://machinelearningmastery.com/how-to-one-hot-encode-sequence-data-in-python/>
3. scikit-learn, Feature extraction, Online: <https://scikit-learn.org/stable/modules/feature_extraction.html>
4. Jason Brownlee, How to Develop a Character-Based Neural Language Model in Keras, Online: <https://machinelearningmastery.com/develop-character-based-neural-language-model-keras/>
5. Francois Chollet, A ten-minute introduction to sequence-to-sequence learning in Keras< Online: <https://blog.keras.io/a-ten-minute-introduction-to-sequence-to-sequence-learning-in-keras.html>
6. Laxfed Paulacy, Convolutional Neural Networks for Sequence Processing: Part 1, Online: <https://medium.com/@jon.froiland/convolutional-neural-networks-for-sequence-processing-part-1-420dd9b500>
7. Francois Chollet, Character-level recurrent sequence-to-sequence model, Online: <https://keras.io/examples/nlp/lstm_seq2seq/>
8. Akira Takezawa,  How to implement Seq2Seq LSTM Model in Keras< Online: <https://towardsdatascience.com/how-to-implement-seq2seq-lstm-model-in-keras-shortcutnlp-6f355f3e5639>
9. Jason Brownlee, How to Develop a Seq2Seq Model for Neural Machine Translation in Keras, Online: <https://machinelearningmastery.com/define-encoder-decoder-sequence-sequence-model-neural-machine-translation-keras/>
10. Jason Brownlee, How to Develop an Encoder-Decoder Model for Sequence-to-Sequence Prediction in Keras, Online: <https://machinelearningmastery.com/develop-encoder-decoder-model-sequence-sequence-prediction-keras/>
11. Chris Burges, Tal Shaked, Erin Renshaw, Ari Lazier, Matt Deeds, Nicole Hamilton, Greg Hullender, Learning to Rank using Gradient Descent, Online: <https://icml.cc/2015/wp-content/uploads/2015/06/icml_ranking.pdf>
12. Michael A. Alcorn Github, RankNet and LambdaRank, Online: <https://github.com/airalcorn2/RankNet>
13. Github, RankNet, Online: <https://github.com/ysyyork/RankNet>
14. Baoyang Song, ,Deep Neural Network for Learning to Rank Query-Text Pairs, Online: <https://arxiv.org/pdf/1802.08988.pdf>
15. Alex Egg, Github, RankNet, Online: <https://github.com/eggie5/RankNet>
16. Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, Illia Polosukhin, Attention Is All You Need, arXiv:1706.03762 cs.CL, Online: <https://doi.org/10.48550/arXiv.1706.03762>


   
"""

RefDict = ExtractReferencesDict(ReferencesText)

print "located %i References: " % len(RefDict.keys())



Section0AbstractText = panel.panel(FixReferences(RefDict,"""# Abstract
ClinicalTrials.Gov is the database storing data from clinical trials. Many clinical trials are required to report their findings in this database according to U.S. law. On 2022-08-26 this database held 425,969 clinical trials with 55,248 trials having numeric results. However, the data is not standardized and numerical data cannot be comprehended since the units are not standardized. There were 36,752 unique units of measure compared to 2019-04-12 when there were 24,548 unique units of measure. It is an increase of 12,204 units over roughly 40 months - almost 10 new unique units of measure added per day. To use the numerical data in disease modeling, there is a need to have machine support to standardize this data. Such standardization is necessary if we wish to use such data in computational models.

[ClinicalUnitMapping.com](https://clinicalunitmapping.com/) is a web tool constructed to help standardize this data and merge it with the following standards and specifications: UCUM, RTMMS / IEEE 11073-10101, BIOUO, and CDISC. ***IEEE 11073-10101 - Adapted and reprinted with permission from IEEE. Copyright IEEE 2019.  All rights reserved.***

This presentation will discuss how python tools are used to: 1) Process and index the data, 2) Find similar units using NLP and machine learning, 3) Create a web interface to support user mapping of those units, 4) Use advanced machine learning tools such as transformers for Natural Language Processing (NLP) to drive inference and core-sets to speed up labeling and quickly setup an inference engine. 

This project is ongoing and this presentation is constantly updated for each venue. This presentation will focus on improvement of supervised learning using transformers and accelerated labeling using core-sets. The latest interactive presentation with results is accessible through: [https://www.clinicalunitmapping.com/show/Unit_Mapping_Latest.html](https://www.clinicalunitmapping.com/show/Unit_Mapping_Latest.html)

The intention is to unify unit standards and machine learning tools that will be able to map all units reported by clinical trials. With such capabilities, the data in this important clinical trials database would become machine comprehensible.

*** This is an interactive presentation - please explore the tabs above and interact with the figures - they have sliders and widgets and hover information that will allow interaction. Following the tabs in order from left to right will tell the story ***

Previous published versions of this presentation are archived and can be downloaded below: 

* [2023 SISO (Virtual) SIMposium, Sep 19-20, 2023](https://www.sisostds.org/2023SISOSIMposium.aspx) - [repository link](https://github.com/Jacob-Barhak/Presentations/blob/235208b5254f9ec63e0f30b031bdfe9956adfd2b/Unit_Mapping_Latest/Unit_Mapping_Latest.html)
* [2023 MSM Consortium Meeting - Past2Future, NIH Campus, Bethesda MD, 28-29 June 2023](https://www.imagwiki.nibib.nih.gov/imag-events/2023-MSM-Meeting) - [repository link](https://github.com/Jacob-Barhak/Presentations/blob/1efb29ee47bf776c2f966d2540f3202dcddb0089/Unit_Mapping_Latest/Unit_Mapping_Latest.html)
* [22-23 May 2023 MODSIM WORLD Norfolk, VA](https://modsimworld.org/)  - [repository link](https://github.com/Jacob-Barhak/Presentations/blob/29f8327681785c15b60d0b0013cdb614510105b1/Unit_Mapping_Latest/Unit_Mapping_Latest.html)
* Keynote at [CHRONIC DISEASES & INFECTIOUS DISEASES 24-NOV-2022, Paris, France](https://www.chronicdiseases.scientexconference.com/)   - [repository link](https://github.com/Jacob-Barhak/Presentations/blob/174bd55bfc0cc1eee4af06404353a9af5a3824f7/COVID19_Ensemble_Latest/COVID19_Ensemble_Latest.html)


"""), width=1100, height=600)


Section0SubHeader = panel.panel('## Longer Term Motivation: Computer Automation of Human Reasoning', width=900, height=20)



Section0ChronologyFigure = panel.panel(ConstractImageLinkAnchor('https://en.wikipedia.org/wiki/Computer_chess','ComputerInfluenceDiagram.png','Towards Computer Automation of Human tasks - Main sources Wikipedia Computer Chess and Wikipedia self-driving car',1000), width=1000, height=600)

Section0 = panel.Column(Section0AbstractText, Section0SubHeader, Section0ChronologyFigure)





Section1MethodText = panel.panel(FixReferences(RefDict,"""# Proposed Solution

## 1. Aggregate and index all ClinicalTrials.Gov units.

## 2. Gather auxiliary unit standards / specifications:

### - [CDISC](https://www.cdisc.org/) - Clinical Data Interchange Standards Consortium.
### - [RTMMS / IEEE](https://rtmms.nist.gov/rtmms/) - affiliated with NIST / IEEE 11073-10101.
### - [Unit Ontology](https://bioportal.bioontology.org/) from BioPortal (BIOUO).
### - [UCUM](https://unitsofmeasure.org/) - The Unified Code for Units of Measure (RTMMS / CDISC).

## 3. Use python and Machine Learning tools to:
### - Find unit proximity using unsupervised Machine Learning (ML) and Natural Language Processing (NLP).
### - Create a web site for crowd mapping of the unit corpus.
### - Create supervised learning ML technique to comprehend units.

"""), width=500, height=600)

Section1ProcessingDiagram =  panel.panel(ConstractImageLinkAnchor('https://clinicalunitmapping.com/','ClinicalUnitProcessDiagram.png','Clinical data Processing diagram',600), width=600, height=600)

Section1Method = panel.Row(Section1MethodText,Section1ProcessingDiagram)



Section1WebKeyPoints = panel.panel(FixReferences(RefDict,"""# Collaborative Unit Mapping Web Site
## [ClinicalUnitMapping.com](https://clinicalunitmapping.com/)

### - Multiple users can use the mapping tool.
### - Similar units clustered together.
### - Unit context and statistics displayed.
### - User can map units using user or machine suggested units.
### - Highlighted auxiliary units: RTMMS / CDISC / UCUM / BIOUO.
### - Supervised machine learning can infer units

"""), width=500, height=500)



Section1WebSiteStaticImage = panel.panel(ConstractImageLinkAnchor('https://clinicalunitmapping.com/','ClinicalUnitMappingScreenShot.png','ClinicalUnitMapping.com web site',600), width=600, height=550)

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



Section2_1 = panel.panel("""### Unsupervised Machine Learning - Feature Extraction

Features are used in clustering algorithms to organize close units together to aid the user.
""", width=Width, height=100, margin = (0,0,0,0))


Figure_2_1 = ObjectInlineHTML(ResourceDir + '/units_original_features.html', Width=1150, Height=500)

Section2_2 = panel.panel("""### Units Proximity and Clustering into Groups of Units""", width=Width, height=5, margin = (0,0,0,0))


Figure_2_2 = ObjectInlineHTML(ResourceDir + '/units_combined_matches_matrix.html', Width=1150, Height=550)

Section2 = panel.Column(Section2_1, Figure_2_1, Section2_2, Figure_2_2, margin = (0,0,0,0))


TableCSS = """
div.special_table + table, th, td {
  border: 1px solid blue;
  text-align: left;
}
"""

panel.extension(raw_css=[TableCSS])

Section3SupervisedMachineLearningOverview = panel.panel(FixReferences(RefDict,"""<div class="special_table"></div>
# Supervised Machine Learning Architectures

| Solution                             | Main Layers       | Accuracy            | Comments                                                                                                          | References                 |
|:-------------------------------------|:------------------|:--------------------|:------------------------------------------------------------------------------------------------------------------|:---------------------------|
| Simple Classification                | Dense             | NA                  | Simple solution, yet this problem has many classes and therefore not practical.                                   |[1], [2]                    |
| Learning to Rank - Pairwise          | CNN & Dense-Twin  | NA                  | High complexity O(N^2) difficult inference due to pairwise nature.                                                |[11], [12], [13], [14], [15]|
| Feature Classification               | LSTM / CNN        | NA                  | Can be simple and fast yet requires mapping and is sensitive.                                                     |[3]                         |
| Sequence to Sequence Preset Length   | LSTM / CNN        | 38.5% - 61.0%       | Relatively simple flexible and reliable, training reasonable, fast inference. Correction can be applied.          |[4], [6]                    |
| Sequence to Sequence Encoder/Decoder | LSTM              | 53.6% - 56.2%       | Works well for short sequences, non trivial implementation. Slow inference. Correction can be applied.            |[5], [7], [8], [9], [10]    |
| Transformers                         | Attention         | 86.9% - 87.5%       | Generative NLP Technology using encoder decoder with attention layers - generates text rather than classifies.    |[16]                          |


## Labeling

- Labeling is a time consuming tedious process.
- Mock labeling was initially used using the output of the clustering algorithm to assess algorithm accuracy.
- Actual labeling was accelerated by using core-sets using [DataHeroes](https://dataheroes.ai/).
- [ClinicalUnitMapping.com](https://clinicalunitmapping.com/) AI suggestions were used to further accelerate the manual tedious work.
- Units that belonged to standards were automatically labeled according to standards synonyms.
- Labeling and AI training were iterated.
- Unit context was considered during labeling and training.

</br>
</br>
## Training Numbers

- 41795 total unique units used in the data base.
- 36752 used in ClinicalTrials.Gov .
- 5043 units appeared in other standards and auto mapped.
- 406857 non units used to contrast units.
- 679 core-set units.
- 17203 units were labeled overall and used in training.
- 3247 target labels identified.
- 412518 / 45948 records in train / validate split.


# Inference

- After the AI was trained Inference was performed using transformers.
- Those NLP tools attempt to comprehend the text and have behavior somewhat comparable to humans.


"""), width=Width, height=1100)




def GeneratePlot(InputFile, Title, Footer):
    "Generate a plot for clusters processed"

    holoviews.extension('bokeh')    
    PlotsDict = {}
    
    ShowStatisticsForOnlyThisNumberOfFirstItems = 50
    PhaseTexts = [u'train', u'validate']
    PassTypeTexts = [u'Unit & Context',u'Unit only',u'Context only', u'Non units']
    
    PlotTypes = [('Infer Exact',True), 
                 ('Infer Close',True),  
                 ('How Close?',False),   
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

                Values = [min(Entry[PlotTypeEnum]+0,NumberOfCategories) for Entry in PredictionQualities[(PhaseText,PassTypeText)] if Entry !=None] 
                Frequences, Edges = numpy.histogram(Values, bins = Bins, density = True)
                if IsPlotTypeBoolean:
                    FrequencesToUse = Frequences
                else:
                    FrequencesToUse = [ sum(Frequences[:(Enum+1)]) for Enum in range(len(Frequences))] 
                HistogramShortTitle = holoviews.Histogram((Edges, FrequencesToUse)).redim.label(x='Quality', Frequency = ['Cumulative Proportion','Proportion'][IsPlotTypeBoolean]).opts( title = PlotTypeName, tools = ['hover'], ylim =(0,1), xlim=( Bins[0], Bins[-1]) , color = ['Blue','Red'][IsPlotTypeBoolean], height=130 , width=650-520*IsPlotTypeBoolean, toolbar = None, default_tools = [], fontsize={'title': 8, 'labels': 8, 'xticks': 6, 'yticks': 6}, xticks=LabelsX, shared_axes=False)
                PlotsDict[(PhaseText,PassTypeText,PlotTypeName)] = HistogramShortTitle

    PlotList = [  (PhaseText + ' ' + PassTypeText  , [ panel.pane.HoloViews(PlotsDict[(PhaseText,PassTypeText,PlotTypeName)]) for (PlotTypeName,IsPlotTypeBoolean) in (PlotTypes)]) for PhaseText in PhaseTexts for PassTypeText in PassTypeTexts ] 
    CombinedList = [panel.panel(Title,height=50, margin = (0,0,0,0))]
    for (PlotTitle,PlotRows) in PlotList:
        CombinedList.append(panel.panel('#### '+PlotTitle,height=30, margin = (0,0,0,0)))
        CombinedList.append(panel.Row(*PlotRows, margin = (0,0,0,0)))
    CombinedList.append(panel.panel(Footer,height=10, margin = (0,0,0,0)))
    ConstrcutedGrid = panel.Column(*CombinedList, margin = (0,0,0,0))
    return ConstrcutedGrid


Section4SupervisedMachineLearningHeader = panel.panel("#Transformers Neural Network Training and Validation Results", width=Width, height=55)
Section4SupervisedMachineLearningFooter = 'Rows show input scenarios: unit / context / both for training and validation. </br>Columns show different accuracy metrics. </br><span style="color:red">Red = initial inference accuracy</span>.  </br><span style="color:Blue">Blue = accuracy after correction of inference while looking up multiple close units. </span>'

Section4SupervisedMachineLearningResults1 = GeneratePlot('Summary_stats_new_train.pckl', 'Transformers were trained with inputs of units only, contexts only, and both.',Section4SupervisedMachineLearningFooter)

# uncomment to save only the histograms
# Section4SupervisedMachineLearningResults1.save('histograms.html)

Section4 = panel.Column(Section4SupervisedMachineLearningHeader,Section4SupervisedMachineLearningResults1, margin = (0,0,0,0))



Section5ShowTheSite = panel.panel(FixReferences(RefDict,"""
# Explore the AI on the Website
<object width="1150" height="650" data="https://clinicalunitmapping.com/">Warning: web site could not be included!</object>

"""), width=Width, height=500)


Section5 = Section5ShowTheSite


Section6SummaryText = panel.panel(FixReferences(RefDict,"""# Summary
We created AI and web tools that support standardizing units of measure.

* The methodology can be used for other standardization tasks.

With such tools it will be possible for machines to:

* Recognize medical units, even if misspelled.
* Comprehend medical units.
* Comprehend quantities and numbers associated with units.

Such AI will replace many tedious human tasks.

Future work will focus on improving supervised learning.

Publications available at: [ClinicalUnitMapping.com/about](https://clinicalunitmapping.com/about) .

"""), width=600, height=600)

Section6Summary = panel.Row(Section6SummaryText,PresentationURL, margin = (0,0,0,0))

Section6AdditionalInfo = panel.panel("""

## Reproducibility:

This presentation is accessible [here](%s). The code that generated the presentation can be accessed [here](%s). This presentation is generated using Python 2.7.16, panel-0.8.0, holoviews 1.12.7, bokeh-1.4.0.
Code for ingestion and clustering are archived in the file: AnalyzeCT_2022_11_19.zip. AI and web site database were created using the code in AnalyzeCT_Full_2023_10_01.zip. 
Clinical Trials data archived in AllPublicXML_2022_08_26.zip. Bio Ontology Units downloaded on 2019_04_09, CDISC data downloaded on 2019_03_30 , RTMMS units downloaded on 2019_03_24 . 
Tensorflow 2.10 and transformers 4.26.1 was used for Neural Network execution in Python 3.10.9 environment. DataHeroes 0.2 was used for core-set calculations



### Conflict of Interest Statement:
Payment/services info: Dr. Barhak reports non-financial support and other from Rescale, and MIDAS Network, other from Amazon AWS, Microsoft Azure, MIDAS network, other from The COVID tracking project at the Atlantic, other from John Rice and Jered Hodges. 
Financial relationships: Jacob Barhak declare(s) employment from MacroFab, United Solutions, B. Well Connected health. The author had a contract with U.S. Bank / Apexon, MacroFab, United Solutions, and B. Well during the work. However, none of these companies had influence on the modeling work reported in the paper. Jacob Barhak declare(s) employment and technical support from Anaconda. The author contracted with Anaconda in the past and uses their free open source software tools. Also the author received free support from Anaconda Holoviz team and Dask teams. Intellectual property info: Dr. Barhak has a patent US Patent 9,858,390 - Reference model for disease progression issued to Jacob Barhak, and US patent 10,923,234 - Analysis and Verification of Models Derived from Clinical Trials Data Extracted from a Database.. Other relationships: During the conduct of the study; personal fees from United Solutions, personal fees from B. Well Connected health, personal fees and non-financial support from Anaconda, outside the submitted work.  . However, despite all support, Dr. Barhak is solely responsible for decisions made for this publication and is responsible for its contents.
"""%
(PublishURL,CodePublishURL), width=Width, height=800)


Section6 =  panel.Column(Section6Summary,Section6AdditionalInfo, margin = (0,0,0,0))



Section11_1  = panel.panel(FixReferences(RefDict,"""
### Acknowledgments: 

* *** IEEE 11073-10101 - Adapted and reprinted with permission from IEEE. </br>Copyright IEEE 2019. All rights reserved.***

* Thanks to Government individuals for useful information: 
    - Nick Ide (Formerly NIH/NLM)
    - Erin E Muhlbradt (NIH/NCI) 
    - John Garguilo (NIST)
    - Grace Peng (NIH/NIBIB) 

* Thanks to these people for useful tips on units, NLP, and standardization:
    - John Rice
    - Paul Schluter
    - Tipton Cole
    - Rocky Reston
    - Andrew Simms
    - Becky Ruppel
    - Yuval Merchav 
    - Uri Goren
    - Ari Bornstein
    - Ryan Baxley
    - Bhargav Srinivasa Desikan 
    - Blaize Berry

"""), width=int(Width * 0.5), height=None)

Section11_2  = panel.panel(FixReferences(RefDict,"""
The above logos acknowledge help provided by these organizations. The logos do not imply any other connection other than a large thank you.


Special Thanks to Anaconda and HoloViz and especially these team members of the HoloViz Team:

* Philipp Rudiger
* James Bednar
* Jean-Luc Stevens 

Thanks to those who hosted me / my computing equipment:

* John Rice
* Jeff Pape
* Boris and Halina Barhak (my parents)


"""), width=int(Width * 0.5), height=None)

AnacondaLogoURL = panel.panel(ConstractImageLinkAnchor('https://www.anaconda.com/','AnacondaLogo.png','Anaconda web site',100), width=100, height=50)
HoloVizLogoURL = panel.panel(ConstractImageLinkAnchor('https://holoviz.org/','HolovizLogo.png','Holoviz web site',150), width=150, height=50)
DataHeroesURL = panel.panel(ConstractImageLinkAnchor('https://dataheroes.ai/','dataheroes.png','dataheroes web site',200), width=200, height=50)

Logos = panel.Row( AnacondaLogoURL, HoloVizLogoURL, DataHeroesURL, margin = (0,0,0,0))

Section11 = panel.Row( Section11_1, panel.Column(Logos, Section11_2, ), margin = (0,0,0,0))





SectionSelectorTab = panel.layout.Tabs (
                                        ('Preface',Section0),
                                        ('Solution Outline', Section1),
                                        ('Unsupervised Machine Learning', Section2),

                                        ('Supervised Machine Learning', Section3SupervisedMachineLearningOverview),
                                        ('Training', Section4),
                                        ('Explore the AI', Section5),
                                        
                                        ('Summary', Section6),
                                        ('Acknowledgments', Section11),
                                        margin = (0,0,0,0), 
                                        )
                                        
Presentation = panel.Column(PresentationHeader, SectionSelectorTab)
Presentation.save(SavedFileName, resources=INLINE, title=TitleHTML)       

