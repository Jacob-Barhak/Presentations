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
import numpy
import holoviews
import pandas

holoviews.extension('bokeh')

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


PresentationURL = panel.panel(ConstractImageLinkAnchor('https://jacob-barhak.github.io/Presentation_GE_Healthcare2019.html','GE_Healthcare2019.png','View this presentation on the web',550), width=550, height=550)

PresentationTitle = panel.panel("""# The Reference Model and Associated Technologies Towards Computational Accumulation of Medical Knowledge
""", width=850, height=90, margin = (0,100,0,0))
PresentationVenue = panel.panel("""GE Healthcare Sepsis Journal Club 20th August 2019
""", width=210, height=20, margin = (0,0,0,0))

PresentationVenueFigure = panel.panel(ConstractImageLinkAnchor('https://www.gehealthcare.com/','ge-healthcare-logo.png','GE Healthcare',200), width=200, height=70, margin = (0,0,0,0))

PresentationHeader = panel.Row ( PresentationTitle,  panel.Column(PresentationVenueFigure, PresentationVenue, margin = (0,0,0,0)), margin = (0,0,0,0) )


Section0Title = panel.panel('## Motivation: Computer Automation of Human Reasoning', width=1000, height=20)
Section0Author = panel.panel('by: [Jacob Barhak](http://sites.google.com/site/jacobbarhak/)', width=200, height=20)

Section0Header =  panel.Row(Section0Title, Section0Author, margin = (0,0,0,0))

Section0ChronologyFigure = panel.panel(ConstractImageLinkAnchor('https://en.wikipedia.org/wiki/Computer_chess','ComputerInfluenceDiagram.png','Towards Computer Automation of Human tasks - Main sources Wikipedia Computer Chess and Wikipedia self-driving car',980), width=1058, height=595)



Section0 = panel.Column(Section0Header, Section0ChronologyFigure)


Section1Title = panel.panel('## Generating Populations Using Evolutionary Computation', width=950, height=20)
Section1Author = panel.panel('by: [Jacob Barhak](http://sites.google.com/site/jacobbarhak/), [Aaron Garret](http://sites.wofford.edu/garrettal/)', width=200, height=40)

Section1Header =  panel.Row(Section1Title, Section1Author, margin = (0,0,0,0))

Section1PopulationGenerationText = panel.panel("""## Why Generate Populations?

* Clinical trials ** do not expose individual data ** due to privacy restrictions.
* Instead trials ** publish statistics with inclusion & exclusion criteria ** such as age distribution.
* We create artificial populations that **mimic these published statistics**.
* Tools that can help with this are the [MIcro Simulation Tool (MIST)](https://github.com/Jacob-Barhak/MIST) that uses [Inspyred](https://pythonhosted.org/inspyred/)
""", width=600, height=110)


Section1PopulationGenerationVideo1 = panel.panel(VideoInlineHTML(CommonResourceDir+'PopulationGeneration_Small.mp4',600,450), width=600, height=450)
Section1PopulationGenerationVideo2 = panel.panel(VideoInlineHTML(CommonResourceDir+'InspyredMIST_Small.mp4',600,380), width=600, height=360)

Section1PopulationGeneration = panel.Row(panel.Column(Section1PopulationGenerationText, Section1PopulationGenerationVideo2), Section1PopulationGenerationVideo1)


## The Population Generation Section

Section1EvolutionaryComputationText = panel.panel("""## Evolutionary Computation (EC)
                                                                  
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

Section1EvolutionaryComputationVideo = panel.panel(VideoInlineHTML(CommonResourceDir+'EvolutionaryComputation_Small.mp4',600,500), width=600, height=450)

Section1EvolutionaryComputation = panel.Row(Section1EvolutionaryComputationText,Section1EvolutionaryComputationVideo, margin = (0,0,0,0))

Section1SlideSelectorTab = panel.layout.Tabs (
                                        ('Population Generation', Section1PopulationGeneration),
                                        ('Evolutionary Computation', Section1EvolutionaryComputation),
										margin = (0,0,0,0),
                                      )

Section1 = panel.Column(Section1Header, Section1SlideSelectorTab, margin = (0,0,0,0))






Section2Title = panel.panel('## Microsimulation by Example - Building a Sepsis Model Prototype', width=950, height=20)
Section2Author = panel.panel('by: [Jacob Barhak](http://sites.google.com/site/jacobbarhak/)', width=200, height=40)

Section2Header =  panel.Row(Section2Title, Section2Author, margin = (0,0,0,0))

ModelAndDisclaimer = panel.panel('[Click for Model & hover for Disclaimer](https://github.com/Jacob-Barhak/Presentations/tree/master/GE_Healthcare2019 "This Sepsis Model is a prototype assembled quickly to demonstrate modeling capabilities using familiar terminology - more effort is needed for a proper model")', width=50)


Section2MIST_Text = panel.panel("""### MIcro Simulation Tool (MIST)

* Microsimulation in a nutshell = simulation of a population, one individual at a time 
* [MIcro Simulation Tool (MIST)](https://github.com/Jacob-Barhak/MIST):
	* Free software 
    * Allows creating, executing, and maintaining microsimulation models
	* Supports population generation with Evolutionary Computation
	* Supports model definition as state transitions and rules
	* Supports simulation in High Performance Computing Environment
    * MIST Runs over the cloud !
	* Provides a Domain Specific Language (DSL) based on Python
	* Has a Graphic User Interface to help design
	* Provides a report system to simulate results
	* Supports reproducible results

* MIST was used to model a very initial prototype of Sepsis
""", width=560, height=110)

Section2MIST_Image = ConstractImageLinkAnchor('https://github.com/Jacob-Barhak/MIST','MIST_ScreenShot.png','MIST Screen Shot',640)  

Section2MIST = panel.Row(Section2MIST_Text,Section2MIST_Image, margin = (0,0,0,0))


Section2SepsisModelDiagram = panel.panel("""### Sepsis Model Prototype - Model Diagram

""" + ConstractImageLinkAnchor('https://github.com/Jacob-Barhak/Presentations/tree/master/GE_Healthcare2019','SepsisDiagram.png','Sepsis Model Diagram',900) 

, width=1150, height=110)

Section2SepsisModelTransitions = panel.panel("""### Sepsis Model Prototype - Transitions

|From           | To               | Probability (daily)                             |  Comments                                                         |
|:--------------|:-----------------|:------------------------------------------------|:------------------------------------------------------------------|
| NoSIRS        | SIRS             | 0.234                                           | The incidence of SIRS after PCNL was [23.4%](http://dx.doi.org/10.1111/j.1442-2042.2008.02170.x). we assume that all procedures have a similar rate and the probability is daily. |
| SIRS          | NoSIRS           | 0.54 / (1 + Gr(Lactate,2) *4.2)                 | A crude initial assumption is that all patient respond to treatment [54%](http://dx.doi.org/10.1007/s10877-014-9653-8). We assume that this is daily probability of improvement. We assume that maximum improvement happens if Lactate is normalized - the odds ratio is [5.2 according to Table 2](http://dx.doi.org/10.1378/chest.12-0878) - it is modeled as 1+4.2 if Lactate is normalized. |
| NoSepsis      | Sepsis           | Or(0.15 * (0.125+ 0.875 * SIRS), Ge(Lactate,2)) | [15%](http://dx.doi.org/10.1016/j.jcrc.2016.11.037) develop sepsis in the hospital. We assume this is the base daily probability that we modified. Also SIRS used to be associated with Sepsis yet did not detect [1/8 severe sepsis events](https://doi.org/10.1016/j.mpaic.2018.11.009) So we coded the need to have SIRS as 7/8 * 0.15 plus a constant probability of 1/8 * 0.15. Also [Lactate of 2 or more](https://doi.org/10.1016/j.mpaic.2018.11.009) defines Sepsis 3 so we introduce it to the equation.  |
| Sepsis        | NoSepsis         | 0.54 / (1 + Gr(Lactate,2) *4.2)                 | We assume all probabilities of getting better are the same. See SIRS to No SIRS. | 
| Sepsis        | SevereSepsis     | 0.072                                           | According to [Figure 1 in day 2 there are 7.2% worsening](https://doi.org/10.1016/j.chest.2018.03.058) - for simplicity we assume this means moving to the next stage and we assume its the daily probability. | 
| SevereSepsis  | Sepsis           | 0.54 / (1 + Gr(Lactate,2) *4.2)                 | We assume all probabilities of getting better are the same. See SIRS to No SIRS. |
| SevereSepsis  | SepticShock      | 0.109                                           | According to [Figure 1 in day 2 there are 10.9% worsening](https://doi.org/10.1016/j.chest.2018.03.058) - for simplicity we assume this means moving to the next stage and we assume its the daily probability. |
| SepticShock   | SevereSepsis     | 0.54 / (1 + Gr(Lactate,2) *4.2)                 | We assume all probabilities of getting better are the same. See SIRS to No SIRS. |
| SepticShock   | SepticDeath      | (0.15 * 0.504+0.85 * 0.293)                     | According to [fig 2:  29.3%/50.4%](http://dx.doi.org/10.1016/j.jcrc.2016.11.037) for on arrival shock/ hospital developed. Since only [15%](http://dx.doi.org/10.1016/j.jcrc.2016.11.037) developed sepsis in hospital we add it to the equation.  |
""", width=1150, height=110)

Section2SepsisModelInitialPopulation = panel.panel("""### Sepsis Model Prototype - Initial Population
| Parameter      | Distribution             | Formula                          | Comment                                                 |
|:---------------|:-------------------------|----------------------------------|:--------------------------------------------------------|
| Age            | 67(15)                   | 67+CappedGaussian3*15            | From [Figure 1 Sepsis column](https://doi.org/10.1016/j.chest.2018.03.058). Note that numbers do not match other numbers in paper |
| Male           | 51%                      | Bernoulli(0.51)                  | From [Table 1 Male Row Sepsis Column](https://doi.org/10.1016/j.chest.2018.03.058) |
| NoSIRS         | 1-SIRS                   | 1-SIRS                           | Complementary to SIRS |
| SIRS           | 90%                      | Bernoulli(0.9)                   | From [Wikipedia](https://en.wikipedia.org/wiki/Systemic_inflammatory_response_syndrome) "... nearly all (>90%) of patients admitted to the ICU meet the SIRS criteria." |
| SepsisLevel    | 281 No Sepsis, 343 Sepsis, 192 Severe, 246 Shock,from 1062 | Table([[Uniform(0,1),[0.0, 0.2645951035781544, 0.5875706214689266, 0.768361581920904, 1.0]]], [0,1,2,3] ) | Extracted from [Figure 1](https://doi.org/10.1016/j.chest.2018.03.058)   |
| NoSpesis       | According to SepsisLevel | Eq(SepsisLevel,0)                | See SepsisLevel 0 |
| Sepsis         | According to SepsisLevel | Eq(SepsisLevel,1)                | See SepsisLevel 1 |
| SevereSepsis   | According to SepsisLevel | Eq(SepsisLevel,2)                | See SepsisLevel 2 |
| SepticShock    | According to SepsisLevel | Eq(SepsisLevel,3)                | See SepsisLevel 3 |
| Lactate        | 4.7(3.3)                 | Max(0,Min(18,Gaussian(4.7,3.3))) | Extracted from [table 1](https://doi.org/10.1016/j.annemergmed.2009.08.014) , mmol/L assumed. Upper bound of 18 was extracted from [figure 1](https://doi.org/10.1186/2110-5820-3-12)  , lower bound of 0 is assumed since lab value should be positive. | 

|Objective Filter | Objective Statistics | Objective Function | Objective Target | Objective Weight |
|:----------------|:---------------------|:-------------------|:-----------------|:-----------------|
| 1               | Lactate              | MEAN               | 4.7              | 1                |
| 1               | Lactate              | STD                | 3.3              | 0.1              |
""", width=1150, height=110)

Section2SepsisModelRules = panel.panel("""### Sepsis Model Prototype - Simulations

Simulations also contain the following rules:

| Phase | Parameter           |   Criteria                                                                        |     Formula                             |   Comment    |
|:------|---------------------|-----------------------------------------------------------------------------------|-----------------------------------------|--------------|
| 0     | ProperTreatment     |   1                                                                               | 1   or  0  depending on simulation      | 1 is used for simulations with proper treatment and 0 is used for simulations with bad treatment. | 
| 1     | Lactate             |   1                                                                               | Max(0,Min(18,Lactate+CappedGaussian3))  |  We assume lactate generally changes randomly. According to the example in [Figure 4](https://doi.org/10.1186/2110-5820-3-12) largest swing is 3.5 or -4 daily. As an approximation an STD of 1 is assumed and a cap of 3 . Upper bound of 18 was extracted from [figure 1](https://doi.org/10.1186/2110-5820-3-12)  , lower bound of 0 is assumed since lab value should be positive.
| 1     | Lactate             |   ProperTreatment*Or(Sepsis_Entered, SevereSepsis_Entered,SepticShock_Entered)    | Max(0,Lactate*1.7/4.7)                  | If Proper Treatment is administered A drop from 4.7 to 1.7 in lactate was observed according to [table 2](http://dx.doi.org/10.1164/rccm.200912-1918OC) , we make sure the number remains positive. |

#### The following simulations were executed:


**1.** Model with treatment

**2.** Model with treatment while using Evolutionary Computation to generate the initial population

**3.** Model without proper treatment while using Evolutionary Computation to generate the initial population
""", width=1150, height=110)

Section2SepsisModelResults1Text = panel.panel("""### Sepsis Model Prototype - Results - Initial Population Distribution

Simulation results reports generated by MIST can be accessed through these links: [Model with treatment](https://github.com/Jacob-Barhak/Presentations/tree/master/GE_Healthcare2019/Model/Sepsis_Report.txt), [Model with treatment and EC](https://github.com/Jacob-Barhak/Presentations/tree/master/GE_Healthcare2019/Model/Sepsis_EC_Report.txt) , [Model with Bad treatment and EC](https://github.com/Jacob-Barhak/Presentations/tree/master/GE_Healthcare2019/Model/Sepsis_EC_BAD-Treat_Report.txt)

#### Histograms of Lactate in Generated Populations per Simulation

""", width=1150, height=130)



ModelDir = 'Model'+os.sep

DataFiles = ['SimulationResultExport.csv','SimulationResultExportWithEC.csv','SimulationResultExportBadTreatmentWithEC.csv']
PlotTitles = ['Proper treatment No EC','Proper treatment & Evolutionary Computation', 'Bad treatment & Evolutionary Computation']

Histograms = None
for (DataFile,PlotTitle) in zip(DataFiles, PlotTitles):
    Data = pandas.read_csv(ModelDir+DataFile)
    InitialPopulationLactateData = list(Data[Data.Time==0].Lactate)
    LactateMean = numpy.mean(InitialPopulationLactateData)
    LactateSTD = numpy.std(InitialPopulationLactateData)
    Frequences, Edges = numpy.histogram(InitialPopulationLactateData, bins = 60, range = (0,15), density = False)
    Histogram = holoviews.Histogram((Edges, Frequences)).redim.label(x='Lactate mmol/L' ,  Frequency = 'Count').opts(tools = ['hover'], title = PlotTitle, ylim =(0,25), height=350 , width=350 )    
    Stats = holoviews.Spikes([LactateMean - LactateSTD, LactateMean, LactateMean + LactateSTD]).redim.label(x='Lactate mmol/L (Mean +- STD)').opts(tools = ['hover'], color = 'red', spike_length=20)
    CombinedPlot = (Stats*Histogram)    
    if Histograms is None:
        Histograms = CombinedPlot
    else:
        Histograms = Histograms + CombinedPlot
    Histograms.opts(toolbar = None)



Section2SepsisModelResults1 =   panel.Column(Section2SepsisModelResults1Text,Histograms)
    

Section2SepsisModelResults2Text = panel.panel("""### Sepsis Model Prototype - Results - Mortality     

Simulation results reports generated by MIST can be accessed through these links: [Model with treatment](https://github.com/Jacob-Barhak/Presentations/tree/master/GE_Healthcare2019/Model/Sepsis_Report.txt), [Model with treatment and EC](https://github.com/Jacob-Barhak/Presentations/tree/master/GE_Healthcare2019/Model/Sepsis_EC_Report.txt) , [Model with Bad treatment and EC](https://github.com/Jacob-Barhak/Presentations/tree/master/GE_Healthcare2019/Model/Sepsis_EC_BAD-Treat_Report.txt)

#### Histograms of Mortality per Simulation

""", width=1150, height=130)


Histograms = None
for (DataFile,PlotTitle) in zip(DataFiles, PlotTitles):
    Data = pandas.read_csv(ModelDir+DataFile)
    TimeRangeSize = 60 
    InitialPopulationLactateData = list(Data[Data.Death_Entered==1].Time)
    Frequences, Edges = numpy.histogram(InitialPopulationLactateData, bins = [0.5 + Enum for Enum in range(TimeRangeSize+1)], density = False)
    
    FrequenceBars = [ (Time+1, Count) for (Time,Count) in enumerate(Frequences)] 
    AccumualtedFrequenceBars =  [ (Time+1, sum(Frequences[:Time+1])) for Time in range(TimeRangeSize)] 
    Bars = holoviews.Histogram(FrequenceBars).redim.label(x='Death Day' ,  Frequency = 'Death this day').opts( tools = ['hover'], color='blue', alpha=0.8, title = PlotTitle, ylim =(0,100), height=350 , width=350 ) #, fontsize={ 'xticks': 5})
    AccumualtedBars = holoviews.Histogram(AccumualtedFrequenceBars).redim.label(x='Death Day' ,  Frequency = 'Cumulative deaths').opts( tools = ['hover'], color='red' , alpha=0.2)  #, fontsize={ 'xticks': 5})
    CombinedPlot = (AccumualtedBars * Bars)    
    if Histograms is None:
        Histograms = CombinedPlot
    else:
        Histograms = Histograms + CombinedPlot
    Histograms.opts(toolbar = None)


Section2SepsisModelResults2 =   panel.Column(Section2SepsisModelResults2Text,Histograms)


Section2SepsisModelSummary = panel.panel("""## Sepsis Model Prototype - Discussion

The Sepsis model demonstrates how a population can be modeled for related disease processes
It was shown how:
    
* initial conditions can effect final outcomes
* parameters such as treatment can be modeled
* different disease processes can interact

After more development such a model can be used as a [digital twin](https://en.wikipedia.org/wiki/Digital_twin) to help practitioners

* Recall that an individual is a population of size 1 
* Therefore such a population model can be used to predict outcomes in an individual
* Known Biomarkers can be modeled and unknown Biomarkers can be assumed

Issues with the current model:
    
* Based on minimal amount of data - more knowledge needs to be accumulated
* The model is not validated against other known observations
* Assumptions made during modeling may not fit reality

[The Reference Model](https://simtk.org/projects/therefmodel) technology addresses these issues and will be shown with regards to diabetes.

""", width= 1150, height=250)


Section2SlideSelectorTab = panel.layout.Tabs (
                                        ('MIST', Section2MIST),
                                        ('Sepsis Model Diagram', panel.Row(Section2SepsisModelDiagram, ModelAndDisclaimer, margin = (0,0,0,0))),
                                        ('Sepsis Model Transitions', panel.Row(Section2SepsisModelTransitions, ModelAndDisclaimer, margin = (0,0,0,0))),
                                        ('Sepsis Initial Population', panel.Row(Section2SepsisModelInitialPopulation, ModelAndDisclaimer, margin = (0,0,0,0))),
                                        ('Sepsis Simulations', panel.Row(Section2SepsisModelRules, ModelAndDisclaimer, margin = (0,0,0,0))),
                                        ('Sepsis Simulation Results Population', panel.Row(Section2SepsisModelResults1, ModelAndDisclaimer, margin = (0,0,0,0))),
                                        ('Sepsis Simulation Results Mortality', panel.Row(Section2SepsisModelResults2, ModelAndDisclaimer, margin = (0,0,0,0))),
                                        ('Discussion', Section2SepsisModelSummary),
										margin = (0,0,0,0),
                                      )

Section2 = panel.Column(Section2Header, Section2SlideSelectorTab, margin = (0,0,0,0))











# The Reference Model Section

Section3Title = panel.panel('## The Reference Model for Disease Progression', width=1000, height=20)
Section3Author = panel.panel('by: [Jacob Barhak](http://sites.google.com/site/jacobbarhak/)', width=200, height=40)
Section3Header = panel.Row(Section3Title,Section3Author, margin = (0,0,0,0))


Section3KeyPoints = panel.panel("""### Key Points
                                
* Ensemble model 
* Currently focuses on diabetic populations
* Models Cardiovascular disease and mortality processes
* Accumulates knowledge from:
    - Existing models/assumptions - currently 30
    - Outcomes observed in 123 cohorts / 31 populations
* Focuses on summary data 
    - Avoids individual data restrictions
    - Larger merged population base
* Flexible Import from ClinicalTrials.Gov
* Traceable and reproducible
* Can map our computational understanding gap
* Output is now available online through this presentation
* Protected by U.S. Patent 9,858,390
* Uses High Performance Computing (HPC)
* Uses MIST as an engine - based on Python
&nbsp;
## The Reference Model now validates against more populations than any other known diabetes model!
""", width=400, height=500)

Section3TheRefModelVideo = panel.panel(VideoInlineHTML(CommonResourceDir+'TheReferenceModelWithOptimize_Small.mp4',800,500), width=800, height=500)
Section3TheRefModel = panel.Row(Section3KeyPoints,Section3TheRefModelVideo)

Section3ResultsText1 = panel.panel("""### Results: Model Mixture 
The overall fitness is represented as the circle on the left. Each bar represents the influence of each model/assumption on the model for each iteration.
""", width=1200, height=50)

Section3MixturePlot = panel.panel(ObjectInlineHTML(ExternalResourcesIMAG2019+'ModelMixturePlotsActive.html'), width=1200, height=600)


Section3ResultsText2 = panel.panel("""### Results: Cumulative Computational Understanding Gap
Shows modeling error for cohorts of clinical studies. The vertical axis is the fitness score - The error of the best model prediction. ** Circles near the top are outliers the model cannot explain**
""", width=1200, height=50)

Section3PopulationPlot = panel.panel(ObjectInlineHTML(ExternalResourcesIMAG2019+'PopulationPlotActive.html'), width=1200, height=600)

Section3Discussion = panel.panel("""### Discussion and Future Efforts:

The outlier population seen in the plot is most probably a modeling error related to misinterpretation of outcomes which requires human interpretation.

Such misinterpretation will be common since clinical trial reports are still not standardized and therefore there is much room for expert interpretation and the data is not yet computer comprehensible. 

Some efforts are planned to improve such modeling capabilities by:

* Incorporating human expert interpretation
* Importing more data from [ClinicalTrials.Gov](https://clinicaltrials.gov/) - with the fast growth of this database, accumulation of knowledge is easier than ever before. 
* Standardizing clinical trial data

&nbsp;

### Further improvement is now mostly limited by rate of standardization 


""", width=1200, height=250)

Section3Results1 = panel.Column(Section3ResultsText1, Section3MixturePlot)
Section3Results2 = panel.Column(Section3ResultsText2, Section3PopulationPlot)

Section3SlideSelectorTab = panel.layout.Tabs (
                                        ('The Reference Model', Section3TheRefModel),
                                        ('Results: Model Mixture', Section3Results1),
                                        ('Results: Cumulative Computational Understanding Gap', Section3Results2),
                                        ('Discussion', Section3Discussion),
										margin = (0,0,0,0),
                                      )

Section3 = panel.Column(Section3Header, Section3SlideSelectorTab)



# Clinical Unit Mapping Section

Section4Title = panel.panel('## Clinical Unit Mapping for Standardization of ClinicalTrials.Gov', width=950, height=20)

Section4Author = panel.panel('by: [Jacob Barhak](http://sites.google.com/site/jacobbarhak/) , [Joshua Schertz](https://joshschertz.com/)', width=250, height=40)
Section4Header = panel.Row(Section4Title,Section4Author, margin = (0,0,0,0))


Section4AbstractText = panel.panel("""### Introduction
* ClinicalTrials.Gov now accumulates information from over 300K trials.
    - Over 10% of trials report results.
* It is now a [U.S. Law](https://www.gpo.gov/fdsys/pkg/PLAW-110publ85/pdf/PLAW-110publ85.pdf#page=82) to upload clinical trials to this [fast growing database](https://clinicaltrials.gov/ct2/resources/trends). 
* Data from this database can be extracted in XML format towards modeling.
* However, the database is based on textual input.
    - Designed for human use and comprehension.
    - Currently not suitable for computer comprehension.
* On  12 Apr 2019 all 35,926 trials with results had 24,548 different units
* **Non standardized units prevent machine comprehension of numbers.**
&nbsp;
* We used Machine Learning and Natural Language Processing (NLP)
* We also connected to 4 unit standards / specifications towards unit mapping
* We created [ClinicalUnitMapping.com](https://clinicalunitmapping.com/) as a tools to help standardize the units
&nbsp;
#### If units are standardized, the valuable numerical data in this database can become machine comprehensible.
""", width=500, height=250)

Section4ProcessingDiagram =  panel.panel(ConstractImageLinkAnchor('https://clinicalunitmapping.com/','ClinicalUnitProcessDiagram.png','Clinical data Processing diagram',600), width=600, height=420)

Section4Abstract = panel.Row(Section4AbstractText,Section4ProcessingDiagram)


Section4KeyPoints = panel.panel("""### Solution Key Points:
* A web site was created to allow multiple users to map the units
* The web site is accessible thought [ClinicalUnitMapping.com](https://clinicalunitmapping.com/)

#### User capabilities:
* The user sees similar units clustered together
* The user can switch clusters
* The user can see how many times a unit is used
* The user can see the contexts associated with a unit
* The user can view clinical trials that use each unit
* The user can map a unit to other suggested units
    - Units suggested by machine or other users
    - User can see RTMMS / CDISC / UCUM / Unit Ontology synonyms
    - Close units are bunched together in display
* The user can ignore suggestions and provide their own mapping

#### Solution Python Technologies:
* Indexing
* Natural Language Processing (NLP)
* Unsupervised machine learning
* Visualization
* Database and web deployment
""", width=500, height=600)

Section4WebSiteStaticImage = panel.panel(ConstractImageLinkAnchor('https://clinicalunitmapping.com/','ClinicalUnitMappingScreenShot.png','ClinicalUnitMapping.com web site',700), width=700, height=440)

Section4KeyElements = panel.Row(Section4WebSiteStaticImage, Section4KeyPoints)



Section4Discussion = panel.panel("""### Discussion and Future Efforts
The goal is to solve the unit standardization problem. 

Once data is standardized, data that is currently machine readable will become machine comprehensible. 

Standardizing units may be only the first step. 

Current efforts are to expand this unit standardization project with the intention to work with:

* Unified Medical Language System [(UMLS)](https://www.nlm.nih.gov/research/umls/)
* Clinical Data Interchange Standards Consortium [(CDISC)](https://www.cdisc.org/)
* Simulation Interoperability Standards Organization [(SISO)](https://www.sisostds.org/)

""", width=1200, height=120)


Section4SlideSelectorTab = panel.layout.Tabs (
                                        ('Introduction', Section4Abstract),
                                        ('ClinicalUnitMapping.com', Section4KeyElements),
                                        ('Discussion',Section4Discussion),
										margin = (0,0,0,0),
                                      )


Section4 = panel.Column(Section4Header, Section4SlideSelectorTab)


Section5AdditionalInfo = panel.panel("""

## Reproducibility:

This presentation is accessible [here](https://jacob-barhak.github.io/Presentation_GE_Healthcare2019.html). The code that generated the presentation can be accessed [here](https://github.com/Jacob-Barhak/Presentations/tree/master/GE_Healthcare2019).

This presentation is generated using Python 2.7.16, panel-0.5.1, bokeh-1.1.0.

The Reference Model: The plots were created using the script ExploreOptimizationResults_2019_02_24.py on Windows 10 environment with bokeh 1.0.4 holoviews 1.11.2 on Python 2.7.14 64 bit based on simulation results executed on a 64 core compute server with Ubuntu and stored in: MIST_RefModel_2019_02_18_OPTIMIZE.zip

Clinical Unit Mapping : Code and data for this work are archived in the file: AnalyzeCT_2019_03_02.zip. Web site database was created using the database PartUnitsDB_2018_12_26.db that was created in a previous version of the code and data archived in the files: AnalyzeCT_GOV_Code_2019_01_16.zip , StudiesWithResults_Downloaded_2018_04_20.zip.

The Sepsis Prototype model was generated using MIST version (0.92.5.0). The model and its results and reports can be found in the [Model directory in this repository](https://github.com/Jacob-Barhak/Presentations/tree/master/GE_Healthcare2019).

&nbsp;

## Publications:
### Summary
* J. Barhak, Clinical Data Modeling with Python, AnacondaCon , Austin, Texas,  April 3-5, 2019. [Video](https://youtu.be/fQIYMf5wKGE) , [Presentation](https://jacob-barhak.github.io/AnacondaCon_2019.html) 

### Population Generation and Mircosimulation
* Inspyred library on [GitHub](https://github.com/aarongarrett/inspyred)
* MIcro Simulation Tool (MIST) on [GitHub](https://github.com/Jacob-Barhak/MIST)
* J. Barhak, A. Garrett, Population Generation from Statistics Using Genetic Algorithms with MIST + INSPYRED. MODSIM World 2014, April 15 - 17, Hampton Roads Convention Center in Hampton, VA. [Paper](http://sites.google.com/site/jacobbarhak/home/MODSIM2014_MIST_INSPYRED_Paper_Submit_2014_03_10.pdf)
* J. Barhak  (2015). The Reference Model uses Object Oriented Population Generation. SummerSim 2015. Chicago IL, USA. [Paper](http://dl.acm.org/citation.cfm?id=2874946)
### The Reference Model
#### Selected Publications
* The Reference Model on [SimTK](https://www.simtk.org/projects/therefmodel)
* J. Barhak, The Reference Model for Disease Progression uses MIST to find data fitness. PyData Silicon Valley 2014 held at Facebook Headquarters [Video](https://www.youtube.com/watch?v=vyvxiljc5vA)
* J. Barhak, A. Garrett, Population Generation from Statistics Using Genetic Algorithms with MIST + INSPYRED. MODSIM World 2014, April 15 - 17, Hampton Roads Convention Center in Hampton, VA [Paper](http://sites.google.com/site/jacobbarhak/home/MODSIM2014_MIST_INSPYRED_Paper_Submit_2014_03_10.pdf)
* J. Barhak, Object Oriented Population Generation, MODSIM world 2015. 31 Mar - 2 Apr, Virginia Beach Convention Center, Virginia Beach, VA. [Paper](http://modsimworld.org/papers/2015/Object_Oriented_Population_Generation.pdf)
* J. Barhak, The Reference Model for Disease Progression and Latest Developments in the MIST, PyTexas 2015. College Station, TX, 26-Sep-2015 [Video](https://www.youtube.com/watch?v=htGRRjia-QQ)
* J. Barhak, The Reference Model for Disease Progression Combines Disease Models. I/IITSEC 2016 28 Nov - 2 Dec Orlando Florida [Paper](http://www.iitsecdocs.com/volumes/2016)
* J. Barhak, The Reference Model Models ClinicalTrials.Gov. [SummerSim 2017 July 9-12, Bellevue, WA].(https://doi.org/10.22360/SummerSim.2017.SCSC.022)
* J. Barhak, The Reference Model: A Decade of Healthcare Predictive Analytics with Python, PyTexas 2017, Nov 18-19, 2017, Galvanize, Austin TX. [Video](https://youtu.be/Pj_N4izLmsI)
#### Evolution through MSM/IMAG Posters
* J. Barhak, The Reference Model for Chronic Disease Progression. 2012 Multiscale Modeling (MSM) Consortium Meeting, October 22-23, 2012 [Poster](http://sites.google.com/site/jacobbarhak/home/SectionTheReferenceModel_IMAGE_MSM_Submit_2012_10_17.pdf)
* J. Barhak, The Reference Model for Disease Progression Sensitivity to Bio-Marker Correlation in Base Population - The Reference Model Runs with MIST Over the Cloud!  2013 IMAG Multiscale Modeling (MSM) Consortium Meeting, October 2-3, 2013 [Poster](http://sites.google.com/site/jacobbarhak/home/SectionTheReferenceModel_IMAG_MSM2013_Submit_2013_09_23.pdf)
* J. Barhak, Generating Populations for Micro Simulation from Publicly Available Data - Populations in the MIST! IMAG Multiscale Modeling (MSM) Consortium Meeting  3-4 September 2014 [Poster](http://sites.google.com/site/jacobbarhak/home/SectionPopulationGenerationMIST_IMAG_MSM2014_Upload_2014_08_31.pdf)
* J. Barhak, The Reference Model Uses Modular Population Generation! Object Oriented Population Generation on the Fly with MIST. IMAG Multiscale Modeling (MSM) Consortium Meeting  9-10 September 2015 [Poster](http://sites.google.com/site/jacobbarhak/home/SectionModularPopulationGeneration_IMAG_MSM2015_Upload_2015_09_03.pdf)
* J. Barhak, The Reference Model Interface with ClinicalTrials.Gov  , IMAG Multiscale Modeling (MSM) Consortium Meeting March 22-24, 2017 @ NIH, Bethesda, MD. [Poster](http://sites.google.com/site/jacobbarhak/home/SectionImportClinicalTrialsGov_IMAG_MSM2017_Upload_2017_03_18.pdf)
* J. Barhak, The Reference Model Visualizes Gaps in Computational Understanding of Clinical Trials, 2018 IMAG Futures Meeting March 21-22, 2018 @ NIH, Bethesda, MD. [Poster](http://sites.google.com/site/jacobbarhak/home/Section_IMAG_MSM2018_Map_Upload_2018_03_17.pdf)
* J. Barhak, The Reference Model is the most validated diabetes cardiovascular model known. MSM/IMAG meeting. IMAG Multiscale Modeling (MSM) Consortium Meeting March 6-7, 2019 @ NIH, Bethesda, MD . [Poster](https://jacob-barhak.github.io/InteractivePoster_MSM_IMAG_2019.html)
### Clinical Unit Mapping
* J. Barhak, The Reference Model Models ClinicalTrials.Gov. [SummerSim 2017 July 9-12, Bellevue, WA].(https://doi.org/10.22360/SummerSim.2017.SCSC.022)
* J. Barhak, The Reference Model: A Decade of Healthcare Predictive Analytics with Python, PyTexas 2017, Nov 18-19, 2017, Galvanize, Austin TX. [Video](https://youtu.be/Pj_N4izLmsI)
* J. Barhak, C. Myers, L. Watanabe, L. Smith, M. J. Swat , Healthcare Data and Models Need Standards. Simulation Interchangeability Standards Organization (SISO) 2018 Fall Innovation Workshop.  9-14 Sep 2018 Orlando, Florida [Presentation](https://www.sisostds.org/DesktopModules/Bring2mind/DMX/API/Entries/Download?Command=Core_Download&EntryId=47969&PortalId=0&TabId=105)
* J. Barhak, Python Based Standardization Tools for ClinicalTrials.Gov. Combine 2018 . Boston University [Poster](http://co.mbine.org/system/files/COMBINE_2018_Barhak.pdf)
* J. Barhak, J. Schertz - Natural Language Processing and Web Tools for Mapping Units from ClinicalTrials.Gov - Simulation Interchangeability Standards Organization (SISO) 2019 Simulation Innovation Workshop.  11 - 15 February 2019 Orlando, Florida. [Presentation](https://www.sisostds.org/DigitalLibrary.aspx?Command=Core_Download&EntryId=49580) , [Paper](https://www.sisostds.org/DesktopModules/Bring2mind/DMX/API/Entries/Download?Command=Core_Download&EntryId=49686&PortalId=0&TabId=105)
* J. Barhak, J. Schertz, Clinical Unit Mapping for Standardization of ClinicalTrials.Gov . MSM/IMAG meeting. IMAG Multiscale Modeling (MSM) Consortium Meeting March 6-7, 2019 @ NIH, Bethesda, MD . [Poster](https://jacob-barhak.github.io/InteractivePoster_MSM_IMAG_2019.html)   
* J. Barhak, J. Schertz, Standardizing Clinical Data with Python . PyCon Israel 3-5 June 2019, [Video](https://youtu.be/vDXyCb60L5s) , [Presentation](https://jacob-barhak.github.io/Presentation_PyConIsrael2019.html)

""", width=1200, height=1000)




Section5SummaryText = panel.panel("""## Summary

### <span style="color:blue">We are still very far from computers replacing medical expert reasoning:</span>

* <span style="color:blue">Standardization is necessary.</span>
* <span style="color:blue">Terminology needs more attention.</span>
* <span style="color:blue">More AI tools that accumulate knowledge are needed.</span>
* <span style="color:blue">Culture should change so that domain experts will actively model.</span>

### <span style="color:blue">Afterwards a computerized medical assistant will be possible.</span>
### <span style="color:blue">Such AI will eventually performs decisions better than a certified human.</span>

### Acknowledgments: 
* Thanks to the PyViz team support: Philipp Rudiger, James Bednar, Jean-Luc Stevens
* Thanks to Deanna J. M. Isaman who first introduced me to the the idea of accumulating knowledge from clinical trial summary data. 
* Thanks to Tal Kenig for the idea behind the Sepsis model prototype
* Thanks to Ronen Ozer for making the connection
* Thanks to John Rice for the fruitful discussions regarding standardization. 
* Thanks to NIH persons who helped  and specifically to: 
    - Nick Ide from NLM ClinicalTrials.Gov team on advice to process the site
    - Erin E Muhlbradt from NCI for advice on CDISC unit data
* Thanks to Matthew Rocklin for dask support.
* Many thanks to many other open source and Anaconda developers that supported these efforts by answering many questions.
""", width=600, height=500)

Section5Summary = panel.Row(Section5SummaryText,PresentationURL)

Section5SlideSelectorTab = panel.layout.Tabs (
                                        ('Additional Information', Section5AdditionalInfo),
                                        ('Summary', Section5Summary),
										margin = (0,0,0,0),
                                        )

Section5 =  Section5SlideSelectorTab





TitleHTML = 'GE Healthcare 2019 presentation by Jacob Barhak'

SectionSelectorTab = panel.layout.Tabs (
                                        ('Preface',Section0),
                                        ('(1) Modeling Populations',Section1),
                                        ('(2) Sepsis Model Prototype',Section2),
                                        ('(3) The Reference Model',Section3),
                                        ('(4) ClinicalUnitMapping.com',Section4),
                                        ('(5) Summary',Section5),
										margin = (0,0,0,0),
                                        )
   


                               
                                        
Presentation = panel.Column(PresentationHeader, SectionSelectorTab)
from bokeh.resources import INLINE
Presentation.save('Presentation_GE_Healthcare2019.html', resources=INLINE)       

