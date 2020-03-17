###############################################################################
# Copyright (C) 2020 Jacob Barhak 
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
# 
#
# Note that: 
# Jacob Barhak wrote all presentations
# 
# Special thanks to:
# Philipp Rudiger, James Bednar, and Jean-Luc Stevens for assisting with 
# panel, bokeh, and holoviews issues.
# without their support and development of pyviz visualization tools, this
# interactive presentation would not be possible.


import bokeh
import holoviews
import panel
import base64
import os
import sys
from bokeh.resources import INLINE
from bokeh.palettes import Category20
from bokeh.models import HoverTool
from bokeh.models import CustomJSHover


holoviews.extension('bokeh')
panel.extension(safe_embed=True)

EmbedVideo = False
LocalFiles = True
if len(sys.argv)>1:
    EmbedVideo = 'EmbedVideo' in sys.argv[1:]
    LocalFiles = 'LocalFiles' in sys.argv[1:]
    
Width = 1100

ImageDir = 'Images'
DataDir = 'Data'
# directory to read/write html resources
ResourceDir = 'MSM_IMAG2020' 


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
    RetStr = '<object width="%i" height="%i" data="%s">Warning:%s Not Accessible!</object>'%(Width, Height, ExtrnalFileName,ExtrnalFileName)
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


TitleHTML = 'MSM IMAG 2020 poster by Jacob Barhak'
SavedFileName = 'Poster_MSM_IMAG_2020.html'
PublishURL = 'https://jacob-barhak.github.io/'+SavedFileName
CodePublishURL = 'https://github.com/Jacob-Barhak/Presentations/tree/master/MSM_IMAG2020'
QRCodeFileName = 'MSM_IMAG_2019_Poster.png'

PresentationURL = panel.panel(ConstractImageLinkAnchor(PublishURL,QRCodeFileName,'View this presentation on the web',380), width=380, height=380)

PresentationTitle = panel.panel('# The Reference Model Accumulates Knowledge with Human Interpretation', width=1100, height=40, margin = (0,0,0,0))
PresentationVenue = panel.panel('Venue: [Interagency Modeling and Analysis Group - IMAG wiki - MODELS, TOOLS & DATABASES](https://www.imagwiki.nibib.nih.gov/resources/models-tools-databases) Uploaded 16 March 2020', width=950, height=40, margin = (0,0,0,0))

PresentationAuthors = panel.panel("By: [Jacob Barhak](http://sites.google.com/site/jacobbarhak/)", width=150, height=40, margin = (0,0,0,0))

PresentationHeader = panel.Column( PresentationTitle,  panel.Row (PresentationAuthors , PresentationVenue, margin = (0,0,0,0)), margin = (0,0,0,0))






Section0AbstractText = panel.panel("""## BACKGROUND: 
#### The Reference Model for disease progression is currently the most validated diabetes cardiovascular model known world-wide. Beyond predicting disease progression, it can show our cumulative gap of computational knowledge compared to more populations than any other published model was ever validated against, and many other models are incorporated in it. This year the model was improved with the ability to include human interpretation as input.
      
## METHODS: 
#### The Reference Model is an ensemble model that accumulates knowledge from multiple sources. Until this year, the model included 1) Risk models and assumptions, 2) Summary population data in the form or baseline population statistics and observed outcomes as extracted from clinical trials - mostly from ClinicalTrials.Gov. The model then optimized the model/assumption mixture to best match a fitness function. The optimization technique improved gradient descent method, typically used in machine learning to optimize neural networks, while using parallel computing and High Performance Computing. This year the model was improved with the ability to enter human interpretation of observed outcomes. This permits including multiple explanations from potentially different experts in a way that can be optimized with other factors. This technique allows the machine to handle data that is not very well defined such as medical outcomes may have multiple definitions and hence multiple interpretations. This technique also allows including human influence in an otherwise machine dominated computational process. The Reference Model interactive visualization was improved using new HoloViz Python technologies that allow embedding interactive plots in static web pages. This allows exploring results from the viewpoints of different human interpretations.

## RESULTS:
#### The [most fitting model in 2019 has achieved a fitness score of ~50/1000](https://jacob-barhak.github.io/InteractivePoster_MSM_IMAG_2019.html). In lay terms, with some simplifying assumptions, it means that our cumulative computational knowledge gap was about 5%. Adding multiple possible human interpretations of the data representing uncertainty of the author, allowed removing a clear outlier and improving average fitness in 2020 to ~36/1000 =3.6%, roughly meaning an improvement of 1.4% in the ability of computational methods to explain observed phenomena in clinical trials. Enhanced information on methods and results will appear in [MODSIM World 2020](https://www.modsimworld.org/).
     
## CONCLUSIONS:
#### The Reference Model now includes inputs that are: facts = observed data, assumptions = models, and human interpretations = expert opinion. And the new technologies now allow more human influence on the modeling process in ways not possible before. Moreover, it allows merging human understanding with machine comprehension, thus moving away from the accusation that computer models are similar to black boxes. Now non technical human experts can add their opinions to knowledge assembled by the model towards reduction of our cumulative computational knowledge gap.
""", width=Width, height=700)



Section0TheRefModelDiagram = panel.panel(ConstractImageLinkAnchor('https://simtk.org/projects/therefmodel','TheRefModelDiagram.png','The Reference Model',700), width=600, height=250)

Section0KeyPoints = panel.panel("""## The Reference Model Key Points
* Ensemble model 
* Accumulates knowledge from:
    * Existing models 
    * Observed outcomes
    * Expert interpretations
* Focuses on summary data 
    * Avoids individual data restrictions
    * Larger merged population base
* Flexible Import from ClinicalTrials.Gov
* Traceable and reproducible
* Shows our computational knowledge gap
* Currently focuses on diabetic populations
* Uses High Performance Computing
* Protected by U.S. Patent 9,858,390
""", width=400, height=250)
    
    
Section0TheRefModel = panel.Row(Section0KeyPoints,Section0TheRefModelDiagram)    

Section0 = panel.Column( Section0AbstractText,  Section0TheRefModel)



Inf = 10000

HorizontalLimits = (2010,2035)

TextOffsetX = 1
TextOffsetY = 20

Data = {}

Data['Year'] =                [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, ]
Data['Model Count'] =         [  64,   64,  544, 1028,  Inf,  Inf,  Inf,  Inf,  Inf, ] 
Data['Populations'] =         [   4,    5,    8,    9,    9,   22,   22,   31,   31, ]
Data['Study Cohorts'] =       [  22,   34,   40,   47,   47,   91,   91,  123,  123, ]
Data['Validations'] =         [ 150,  157,  190,  224,  224,  367,  367,  471,  471, ]
Data['Eq-MI'] =               [   4,    4,    9,   10,   11,   11,   11,   11,   11, ]  
Data['Eq-Stroke'] =           [   4,    4,    9,   10,   12,   12,   12,   12,   12, ]  
Data['Eq-DeathMI'] =          [   1,    1,    2,    2,    3,    3,    3,    3,    3, ]    
Data['Eq-DeathStroke'] =      [   1,    1,    1,    1,    2,    2,    2,    2,    2, ]    
Data['Eq-Death'] =            [   1,    1,    1,    1,    2,    2,    2,    2,    2, ]    
Data['Eq-BioMarkers'] =       [   2,    2,    2,    2,    2,    2,    2,    2,    2, ]    
Data['Eq-Treatment'] =        [   2,    2,    2,    2,    2,    2,    2,    2,    2, ]    
Data['Eq-Temporal'] =         [   0,    0,    0,    2,    2,    2,    1,    1,    1, ]    
Data['Correlation'] =         [   0,    0,    0,    2,    2,    2,    2,    2,    2, ]    
Data['Interpretations'] =     [   0,    0,    0,    0,    0,    0,    0,    0,    6, ]

Topics = [ 
             ('Major',False,(
              'Model Count', 
              'Validations')) ,
             ('Populations',False,(
              'Populations', 
              'Study Cohorts', 
              'Validations')) ,
             ('Equations',True,(
              'Eq-MI', 
              'Eq-Stroke', 
              'Eq-DeathMI', 
              'Eq-DeathStroke', 
              'Eq-Death', 
              'Eq-BioMarkers', 
              'Eq-Treatment', 
              'Eq-Temporal', 
              'Correlation', 
              'Interpretations')),
           ]

Innovations =  {}
Innovations[2012] = 'The Reference Model created in {0}'
Innovations[2013] = 'MIST, HPC, Cloud Computing added in {0}'
Innovations[2014] = 'Evolutionary Computation for Population Generation added in {0}'
Innovations[2015] = 'Object Oriented Population Generation developed in {0}'
Innovations[2016] = 'Assumption Engine Cooperative Ensemble Model enabled in {0}'
Innovations[2017] = 'ClinicalTrials.Gov Interface created in {0}'
Innovations[2018] = 'Knowledge Gap Interactive Visualization possible in {0}'
Innovations[2019] = 'Interactive Visualization was improved in {0}'
Innovations[2020] = 'Human Interpretation available in {0}'
              
Colors = Category20[20]

AllDimesions = Data.keys()

VerticalDimensions = list(set(AllDimesions) - set(['Year']))
print (VerticalDimensions)

PlotDict = {}
ArrowDict = {}
MergedPlotDict = {}


def SaveFile(FileName, PlotObject, Title):
    'Save file using Holoviews mechanism'
    if FileName != '':
        print (' saving using panel and INLINE the file: ' + FileName)          
        SaveObject = panel.pane.HoloViews(PlotObject)
        SaveObject.save(FileName, resources=INLINE, title = Title, embed=True)
    else:
        print ('Skipping Save since no file was provided')


def GenerateHistoryPlots(Width,Height):
    "generate the history plots"

    # Define the custom function fot the hover tool
    MyCustom = CustomJSHover(code='''
            var value;
            var modified;
            if (value >= %i) {
                modified = "Infinite";
            } else {
                modified = value.toString();
            }
            return modified;
    '''%(Inf))
        
    MyHover1 = HoverTool(
        tooltips=[
            ( 'Year', '@Year'),
            ( 'Category', '@Category' ),
            ( 'Count', '@Count{custom}' ),  
        ],
        formatters={
            'Year' : 'numeral',   
            'Category' : 'printf',   
            '@Count' : MyCustom
        },
        point_policy="follow_mouse"            
    )    

    # Now generate a plot for each topic
    for (TopicEnum,(TopicTitle,IsStackable,TopicList)) in enumerate(Topics):
        Years = Data['Year']
        for (YearIndex,Year) in enumerate(Years):
            MaxY = 0
            BarsDict = {}
            for (VerticalDimensionEnum,VerticalDimension) in enumerate(TopicList):    
                VerticalDimensionForMaxY = [ (Entry * (Entry != Inf)) for Entry in Data[VerticalDimension] ]
                if IsStackable:
                    MaxY = MaxY + max(VerticalDimensionForMaxY)
                else:
                    MaxY = max([MaxY]+VerticalDimensionForMaxY)
                BaseList = [ ( (RunningYear, VerticalDimension), Value) if RunningYear<=Year else ((RunningYear, VerticalDimension), 0)  for (RunningYear,Value) in zip(Years , Data[VerticalDimension]) ]
                DimDict = dict( BaseList)
                BarsDict.update(DimDict)
            BasePlotsOvelayed = holoviews.Bars(BarsDict, kdims=['Year','Category'], vdims=['Count'])
            Title =  Innovations[Year].format(Year)
            BasePlotsOvelayedWithOpts = BasePlotsOvelayed.opts (xlim = HorizontalLimits, ylim = (0, MaxY*1.2), tools = [MyHover1], toolbar=None, default_tools=[], width=Width-400, height=Height, xrotation= 90, stacked = IsStackable, clone = IsStackable, title = Title, legend_position='right')
            MergedPlot = BasePlotsOvelayedWithOpts
            MergedPlotDict[(Year)] = MergedPlot   
        HoloMapPlot = holoviews.HoloMap(MergedPlotDict,kdims=['Year']).opts(toolbar=None, default_tools=[], width=Width, height=Height, shared_axes=False)
        SaveFile(ResourceDir+os.sep+'TheReferenceModelHistory_%s'%TopicTitle,HoloMapPlot,True)

GenerateHistoryPlots(Width=800, Height=350)

Section1SubHeader1 = panel.panel("""## The Reference Model History
Select a tab below to select topic of interest, then slide the year slider, and hover with mouse pointer over the plot to see advances each year interactively.
""", width=1000, height=80)



'https://jacob-barhak.netlify.com/thereferemcemodel/results_2020_01_04_visual_2020_02_08/combinedplot.html'
Section1HistoryPlot1 = panel.panel(ObjectInlineHTML(ResourceDir + '/TheReferenceModelHistory_Major.html', Width=1150, Height=400), width=1200, height=450)
Section1HistoryPlot2 = panel.panel(ObjectInlineHTML(ResourceDir + '/TheReferenceModelHistory_Populations.html', Width=1150, Height=400), width=1200, height=450)
Section1HistoryPlot3 = panel.panel(ObjectInlineHTML(ResourceDir + '/TheReferenceModelHistory_Equations.html', Width=1150, Height=400), width=1200, height=450)

Section1SelectorTab = panel.layout.Tabs (
                                        ('Overall',Section1HistoryPlot1),
                                        ('Populations', Section1HistoryPlot2),
                                        ('Equations', Section1HistoryPlot3),
                                        margin = (0,0,0,0), width=1200, height=450

                                        )


Section1WhatIsNew = panel.panel("""## What is New this year?
### Problem: 
* Outcomes of published studies are typically published as text rather than exact codes. 
* Even when published with specific definitions such as [ICD codes](https://en.wikipedia.org/wiki/International_Statistical_Classification_of_Diseases_and_Related_Health_Problems), they are hard to compare between publications due to version issues and bundled outcomes.
* Furthermore medical definitions change within time making it hard to compare data from different times. [Sepsis evolving definitions](https://arxiv.org/ftp/arxiv/papers/1609/1609.07214.pdf) is a good example.
* Outcomes with multiple definitions are rarely published like in the [RECORD study](https://clinicaltrials.gov/ct2/show/results/NCT00379769):                      

### Solution: 
* Incorporate human interpretation of outcomes as input
    - Six expert opinions were imitated by the author 
    - Opinions represent strict = no change, conservative, and liberal
    
* Integrate it with optimization with other components
    - Models, assumptions and interpretations influence on fitness are considered
    - Opinions represent strict = no change, conservative, and liberal
    - The algorithm can reject interpretations that do not match observed data 
    - The algorithm highlights the best experts
    
* This is an improvement over the [Delphi method](https://en.wikipedia.org/wiki/Delphi_method) since it includes machine learning components
    - Experts present their opinions once and the machine performs iterations
    - Easily scalable to many experts
    - Can be repeated while comparing interpretations
    - Provides a combined cumulative interpretation

""", width=Width, height=300)
    
    
Section1 = panel.Column( Section1SubHeader1, Section1SelectorTab, Section1WhatIsNew)


Section2Header = panel.panel("""## Results
                             
The 3 plots represent results obtained after 3 weeks of simulation on a 64 core machine. Interactive result exploration is possible through 3 widgets:

### Widgets:
* **Display:** controls what the circle size and circle color mean in the population validation plot. Changing this option helps visually explore the populations. 
* **Iteration:** controls which optimization iteration is displayed - the optimal results appear in iteration 30.
* **Interpretation:** shows the perspective of different possible interpretations of outcomes observed in clinical trials after correction. The "Combined" option shows the merged interpretations. Changing this widget to a numeric value shows the results from the view of a specific "expert" opinion imitated in this simulation. 

### Plots:
* **Population Validation - (upper left):** Shows each clinical trial in a different column. Each circle represents one cohort from the clinical trial. Hovering over the circle will show statistics of the modeled cohort in a pop-up window. The height of the circle represents the fitness score which is a measure of the modeling error. Low fitness means that the model agreed with trial results while high fitness represented by circles near the top represent cases where simulation results do not match observed outcomes. 
* **Convergence - (upper right):** Shows the combined wighted fitness for each iteration. The large circles represent the model without perturbation, the smaller circles represent gradient perturbations and the red wide dashes represent the mean fitness for the iteration considering all perturbations. A vertical blue line reminds the viewer of each iteration is shown in the other plots. The plot shows a clear convergence of the optimization algorithm. The converged fitness represents our cumulative knowledge gap.
* **Model Mixture - (lower left):** Each column represents a different model / assumption. The height of each bar represents the influence of this model / assumption on the ensemble model in the current iteration. Initially all models/assumptions have equal influence. Columns that their bars disappear with iteration represent  equations rejected by the model. The right most cyan bars represent assumptions contributed by different interpretations of the outcome data, Some imitated interpretations are eventually rejected.  

""", width=1000, height=500)

Section2Results = panel.panel(ObjectInlineHTML(ResourceDir+'/CombinedPlot.html', Width=1150, Height=650), width=1200, height=700)

Section2 = panel.Column( Section2Header,Section2Results)


Section5SummaryText = panel.panel("""
### Acknowledgments: 
* Thanks to the HoloViz team: Philipp Rudiger, James Bednar, Jean-Luc Stevens for interactive visualization help. 
* Thanks to Deanna J. M. Isaman who introduced the idea of accumulating knowledge from clinical studies.

### Reproducibility:
This presentation is accessible [here](%s). The code that generated the presentation can be accessed [here](%s). This presentation is generated using Python 2.7.16, panel-0.8.0, holoviews 1.12.7, bokeh-1.4.0.
Results presented in this poster were extracted from a simulation executed on a 64 core machine using Ubuntu 18.04.01 LTS with python 2.7.15 delivered by Anaconda with dask 0.19.1 supporting multi processing and MIST 0.94.6.0 as the simulation engine. The simulation results was archived under the file MIST_RefModel_2020_01_16_OPTIMIZE.zip. Formula Validation run to validate integrity was archived as MIST_RefModel_2020_01_02_FORMULA.zip. Result visualization was generated on a notebook machine using Windows 10 x64 with Python 2.7.16, Bokeh: 1.4.0, Holoviews: 1.12.7. The code/data files ExploreOptimizationResults_2020_02_07.py / ExploreOptimizationResults_2020_02_07.yaml were used to generate the visualization. Thia version of simulation contains one known error of one outcome misplacement as another out of 120 outcomes. 
"""%(PublishURL,CodePublishURL), width=700, height=400)



Section5References1 = panel.panel("""### Selected Publications:
                                  
""", width=150, height=50)
Section5References2 = panel.panel("""### Previous MSM/IMAG Posters:""", width=150, height=50)

Section5Ref11 = panel.panel(ConstractImageLinkAnchor('https://www.youtube.com/watch?v=vyvxiljc5vA','YouTubePyData2014.png','J. Barhak, The Reference Model for Disease Progression uses MIST to find data fitness. PyData Silicon Valley 2014 held at Facebook Headquarters',50), width=50, height=50)
Section5Ref12 = panel.panel(ConstractImageLinkAnchor('http://sites.google.com/site/jacobbarhak/home/MODSIM2014_MIST_INSPYRED_Paper_Submit_2014_03_10.pdf','MIST_INSPYRED_MODSIM2014Paper.png','J. Barhak, A. Garrett, Population Generation from Statistics Using Genetic Algorithms with MIST + INSPYRED. MODSIM World 2014, April 15 - 17, Hampton Roads Convention Center in Hampton, VA.',50), width=50, height=50)
Section5Ref13 = panel.panel(ConstractImageLinkAnchor('http://modsimworld.org/papers/2015/Object_Oriented_Population_Generation.pdf','ObjectOrientedPopulationGenerationMODSIM2015.png','J. Barhak, Object Oriented Population Generation, MODSIM world 2015. 31 Mar - 2 Apr, Virginia Beach Convention Center, Virginia Beach, VA.',50), width=50, height=50)
Section5Ref14 = panel.panel(ConstractImageLinkAnchor('https://www.youtube.com/watch?v=htGRRjia-QQ','PyTexas2015.png','J. Barhak, The Reference Model for Disease Progression and Latest Developments in the MIST, PyTexas 2015. College Station, TX, 26-Sep-2015',50), width=50, height=50)
Section5Ref15 = panel.panel(ConstractImageLinkAnchor('http://www.iitsecdocs.com/volumes/2016','IITSECPaper.png','J. Barhak, The Reference Model for Disease Progression Combines Disease Models. I/IITSEC 2016 28 Nov - 2 Dec Orlando Florida.',50), width=50, height=50)
Section5Ref16 = panel.panel(ConstractImageLinkAnchor('https://doi.org/10.22360/SummerSim.2017.SCSC.022','SummerSim2017.png','J. Barhak, The Reference Model Models ClinicalTrials.Gov. SummerSim 2017 July 9-12, Bellevue, WA.',50), width=50, height=50)
Section5Ref17 = panel.panel(ConstractImageLinkAnchor('https://youtu.be/Pj_N4izLmsI','PyTexas2017.png','J. Barhak, The Reference Model: A Decade of Healthcare Predictive Analytics with Python, PyTexas 2017, Nov 18-19, 2017, Galvanize, Austin TX.',50), width=50, height=50)
Section5Ref21 = panel.panel(ConstractImageLinkAnchor('http://sites.google.com/site/jacobbarhak/home/PosterTheReferenceModel_IMAGE_MSM_Submit_2012_10_17.pdf','MSM_IMAG_2012_Poster.png','J. Barhak, The Reference Model for Chronic Disease Progression. 2012 Multiscale Modeling (MSM) Consortium Meeting, October 22-23, 2012',50), width=50, height=50)
Section5Ref22 = panel.panel(ConstractImageLinkAnchor('http://sites.google.com/site/jacobbarhak/home/PosterTheReferenceModel_IMAG_MSM2013_Submit_2013_09_23.pdf','MSM_IMAG_2013_Poster.png','J. Barhak, The Reference Model for Disease Progression Sensitivity to Bio-Marker Correlation in Base Population - The Reference Model Runs with MIST Over the Cloud!  2013 IMAG Multiscale Modeling (MSM) Consortium Meeting, October 2-3, 2013',50), width=50, height=50)
Section5Ref23 = panel.panel(ConstractImageLinkAnchor('http://sites.google.com/site/jacobbarhak/home/PosterPopulationGenerationMIST_IMAG_MSM2014_Upload_2014_08_31.pdf','MSM_IMAG_2014_Poster.png','J. Barhak, Generating Populations for Micro Simulation from Publicly Available Data - Populations in the MIST! IMAG Multiscale Modeling (MSM) Consortium Meeting  3-4 September 2014.',50), width=50, height=50)
Section5Ref24 = panel.panel(ConstractImageLinkAnchor('http://sites.google.com/site/jacobbarhak/home/PosterModularPopulationGeneration_IMAG_MSM2015_Upload_2015_09_03.pdf','MSM_IMAG2015_Poster.png','J. Barhak, The Reference Model Uses Modular Population Generation! Object Oriented Population Generation on the Fly with MIST. IMAG Multiscale Modeling (MSM) Consortium Meeting  9-10 September 2015',50), width=50, height=50)
Section5Ref25 = panel.panel(ConstractImageLinkAnchor('http://sites.google.com/site/jacobbarhak/home/PosterImportClinicalTrialsGov_IMAG_MSM2017_Upload_2017_03_18.pdf','MSM_IMAG2017_Poster.png','J. Barhak, The Reference Model Interface with ClinicalTrials.Gov  , IMAG Multiscale Modeling (MSM) Consortium Meeting March 22-24, 2017 @ NIH, Bethesda, MD.',50), width=50, height=50)
Section5Ref26 = panel.panel(ConstractImageLinkAnchor('http://sites.google.com/site/jacobbarhak/home/Poster_IMAG_MSM2018_Map_Upload_2018_03_17.pdf','MSM_IMAG_2018_Poster.png','J. Barhak, The Reference Model Visualizes Gaps in Computational Understanding of Clinical Trials, 2018 IMAG Futures Meeting March 21-22, 2018 @ NIH, Bethesda, MD',50), width=50, height=50)
Section5Ref27 = panel.panel(ConstractImageLinkAnchor('https://jacob-barhak.github.io/InteractivePoster_MSM_IMAG_2019.html','MSM_IMAG_2019_Poster.png','J. Barhak, The Reference Model is the most validated diabetes cardiovascular model known. MSM/IMAG meeting. IMAG Multiscale Modeling (MSM) Consortium Meeting March 6-7, 2019 @ NIH, Bethesda, MD',50), width=50, height=50)

Section5References1 =  panel.Row(Section5References1, Section5Ref11, Section5Ref12, Section5Ref13, Section5Ref14, Section5Ref15, Section5Ref16, Section5Ref17)
Section5References2 =  panel.Row(Section5References2, Section5Ref21, Section5Ref22, Section5Ref23, Section5Ref24, Section5Ref25, Section5Ref26, Section5Ref27)


Section5SubHeader2 = panel.panel("""## Longer Term Motivation: Computer Automation of Human Reasoning
""", width=1000, height=20)

Section1Left = panel.Column(Section5References1, Section5References2, Section5SummaryText, margin = (0,0,0,0))

Section5Summary = panel.Row(Section1Left,PresentationURL, margin = (0,0,0,0))

Section5ChronologyFigure = panel.panel(ConstractImageLinkAnchor('https://en.wikipedia.org/wiki/Computer_chess','ComputerInfluenceDiagram.png','Towards Computer Automation of Human tasks - Main sources Wikipedia Computer Chess and Wikipedia self-driving car',1000), width=1000, height=700)

Section5 =  panel.Column(Section5Summary, Section5SubHeader2, Section5ChronologyFigure, margin = (0,0,0,0))

SectionSelectorTab = panel.layout.Tabs (
                                        ('Abstract',Section0),
                                        ('What is New?', Section1),
                                        ('Results', Section2),
                                        ('Additional Information', Section5),
                                        margin = (0,0,0,0), 
                                        )
                                        
Presentation = panel.Column(PresentationHeader, SectionSelectorTab)
Presentation.save(SavedFileName, resources=INLINE, title=TitleHTML)       

