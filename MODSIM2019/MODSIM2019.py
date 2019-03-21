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
# Olaf Dammann & Anselm Blumer worked on Population Disease Occurrence Models
# 
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

def CovertFileToData(FileName):
    "Convert file to data that can be used in html"
    DataFile = open(FileName,'rb')
    Data = DataFile.read()
    DataFile.close()
    EncodedData=base64.b64encode(Data)
    return EncodedData
    

def ConstractImageLinkAnchor(Link, ImageFileName, Text, Width):
    'Constructs html to describe the png image and link it'
    EncodedImage=  CovertFileToData (ImageDir + os.sep+ImageFileName)
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


#PresentationCode = panel.panel(ConstractImageLinkAnchor('https://github.com/Jacob-Barhak/Presentations/tree/master/MODSIM2019','MODSIM_2019_Code.png','Download the code that generated this Presentation',600), width=600, height=600)
PresentationURL = panel.panel(ConstractImageLinkAnchor('https://jacob-barhak.github.io/Presentation_MODSIM_2019.html','MODSIM_2019_Presentation.png','View this Presentation on the web',300), width=300, height=300)

Section0Title = panel.panel('# Population Disease Occurrence Models Using Evolutionary Computation', width=1000, height=30)
Section0Author = panel.panel('by: [Jacob Barhak](http://sites.google.com/site/jacobbarhak/), [Aaron Garret](http://sites.wofford.edu/garrettal/), [Anselm Blumer](https://engineering.tufts.edu/cs/people/faculty/anselm-blumer), [Olaf Dammann](https://medicine.tufts.edu/faculty/olaf-dammann)', width=800, height=40)

Section0VenueFigure = panel.panel(ConstractImageLinkAnchor('http://www.modsimworld.org/','MODSIM_generic.png','MODSIM world',200), width=200, height=20)

Section0VenueText = panel.panel('MODSIM World 2019 - Enabling Digital Transformation with M&S : April 22-24, 2019', width=200, height=50)
Section0Venue = panel.Column(Section0VenueFigure,Section0VenueText)

Section0Header = panel.Row ( panel.Column(Section0Title, Section0Author),  panel.Column(Section0VenueFigure,Section0VenueText) )


Section0Problem = panel.panel(EnhanceMarkDown("""
##A solution based on use of computing power to explore potential hypothesis for an epidemiological problem. 
&nbsp;
                                              
### Problem Definition
&nbsp;
                                      
#### Known:

Population of ~~~N=617~~~ preterm infants, where:
    
~~~P_1=32\%~~~ are with Sepsis 

~~~P_2=75\%~~~ get Oxygen 

it was observed that ~~~P_3=47%~~~ reached the outcome of [Retinopathy of Prematurity (ROP)](https://doi.org/10.1159/000312821)

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


   
Section0DefinitionsText = panel.panel(EnhanceMarkDown("""## Notation
                                                      
For individual ~~~k = 1..N~~~ there are 3 Boolean parameters:

(1) Sepsis ~~~X_{1k}~~~

(2) Oxygen ~~~X_{2k}~~~ 

(3) ROP ~~~X_{3k} ~~~ 

We will denote those as ~~~X_{ik}~~~

&nbsp;

The probabilities can be defined as:

~~~Pi = \# (X_{ik}=1)/N~~~ 

where ~~~\# ~~~ is the count operator

&nbsp;

The odds ratio of two parameters i,j defined by the following equation:

~~~O_{ij} = \\frac{\# (X_{ik}=1 \\; & \\; X_{jk}=1) * \# (X_{ik}=0 \\; & \\; X_{jk}=0)} {\# (X_{ik}=0 \\; & \\; X_{jk}=1) * \# (X_{ik}=1 \\; & \\; X_{jk}=0)}$29~~~

&nbsp;

Let us define Groups of similar individuals:
    
~~~G_{abc}=\{X_{1k}=a \\; & \\; X_{2k}=b \\; & \\; X_{3k}=c\}~~~

Where ~~~a,b,c~~~ are booleans that represent Sepsis, Oxygen , ROP respectively 

Therefore there are 8 groups representing all possible combinations:
    
~~~G_{000},G_{001}, G_{010}, G_{011}, G_{100},G_{101}, G_{110}, G_{111}~~~

"""), width=800, height=400)
    
Section0AnalyticalSolutionText = panel.panel(EnhanceMarkDown("""## Analytical Solution?

Using the count operator ~~~\# ~~~ we can write the following equations to solve the number of individuals in each group ~~~\# G_{abc}~~~:

(1) ~~~P_1 = (\# G_{100}+\# G_{101}+\# G_{110}+\# G_{111}) / N~~~

(2) ~~~P_2 = (\# G_{010}+\# G_{011}+\# G_{110}+\# G_{111}) / N~~~

(3) ~~~P_3 = (\# G_{001}+\# G_{101}+\# G_{011}+\# G_{111}) / N~~~

(4) ~~~O_{12} = (\# G_{110}+\# G_{111})*(\# G_{000}+\# G_{001}) / ((\# G_{010}+\# G_{011})*(\# G_{100}+\# G_{101}))~~~

(5) ~~~O_{13} = (\# G_{101}+\# G_{111})*(\# G_{000}+\# G_{010}) / ((\# G_{001}+\# G_{011})*(\# G_{100}+\# G_{110}))~~~

(6) ~~~O_{23} = (\# G_{011}+\# G_{111})*(\# G_{000}+\# G_{100}) / ((\# G_{001}+\# G_{101})*(\# G_{010}+\# G_{110}))~~~

(7) ~~~N = \# G_{000}+\# G_{001}+\# G_{010}+\# G_{011}+\# G_{100}+\# G_{101}+\# G_{110}+\# G_{111}~~~

&nbsp;

## Note that we only have 7 equations with 8 unknown measures!!!

&nbsp;

## This means that additional assumptions are needed!
"""), width=800, height=400)

Section0DefinitionsImage = panel.panel(ConstractImageLinkAnchor('','GroupDefinition.png','Spliting the population into different groups',400), width=400, height=400)

Section0Definitions = panel.Row(Section0DefinitionsText,Section0DefinitionsImage)

Section0AnalyticalSolution = panel.Row(Section0AnalyticalSolutionText,Section0DefinitionsImage)





Section0EvolutionaryComputationText = panel.panel(EnhanceMarkDown("""## Evolutionary Computation (EC)
                                                                  
Using the Inspyred library we can generate populations that match the statistics

We defined a fitness function:

&nbsp;

~~~Fitness(s) = W_1\sum |P_i - P'_i|+ W_2 \sum |O_{ij} - O'_{ij}|$18~~~

where ~~~W_1 , W_2~~~ are constants and P'_i and O'_{ij} are the probabilities and odds ratios of the candidate solutions.

&nbsp;
   
The EC solution walks through these main stages of a Genetic Algorithm:
    
(1) Generation: A population of random solutions is generated. 

(2) Evaluation: Where ~~~Fitness(s)$12~~~ is calculated for each solution ~~~s$7~~~

(3) Selection: Where the best solutions are ranked and selected to represent the next generation

(4) Variation: Where the selected solutions undergo mutation and crossover operators to create another generation using:
    
&nbsp;&nbsp;&nbsp;- Cross-over: from a pair of mother and father create two offspring solutions 
   
&nbsp;&nbsp;&nbsp;- Internal Swap mutator: swap a single parameter value ~~~i~~~ between two random individuals 
   
&nbsp;&nbsp;&nbsp;- Reroll mutator: completely reroll some individuals in the solution 
    
(5) Termination: where a stopping criteria is checked - if a stop criteria was not reached, go back to step 2

(6) Post termination, the most fitting population is considered as the answer

"""), width=800, height=400)

Section0EvolutionaryComputationVideo = panel.panel(VideoInlineHTML(CommonResourceDir + 'EvolutionaryComputation_Small.mp4',400,400), width=400, height=400)

Section0EvolutionaryComputation = panel.Row(Section0EvolutionaryComputationText,Section0EvolutionaryComputationVideo)


Section0SimpleSolution = panel.panel(EnhanceMarkDown("""## Simple Solution
                                      
Using the EC algorithm with the [Inspyred Python library](https://pythonhosted.org/inspyred/) we will try to solve the original problem in two steps:
    
(1) Generate a population that matches the original untreated population statistics using EC.

(2) Generate a population with the estimated treatment effect as a constraint while removing the constraint on the outcome.

&nbsp;

| &nbsp; Step &nbsp; | &nbsp; N &nbsp; | &nbsp; P Sepsis &nbsp; | &nbsp; P Oxygen &nbsp; | &nbsp; P ROP  &nbsp;  | &nbsp; Odds Sep/Oxy  &nbsp; | &nbsp; Odds Sep/ROP &nbsp;  | &nbsp; Odds Oxy/ROP &nbsp;  |
|:----:|:---:|:----------:|:---------:|:---------:|:---------------:|:---------------:|:---------------:|
|   1  | 617 |    0.32    |    0.75   |    0.47   |        2.6      |       2.8       |        3.6      |
|   2  | 617 |    0.16    |    0.75   |     ?     |        2.6      |       2.8       |        3.6      |

&nbsp;

Recall, however, that we have one degree of freedom and the second step adds another degree of freedom. 

Therefore many populations that fit this problem can be generated.

&nbsp;

### We need an additional assumption to have one solution!

"""), width=1200, height=400)


Section0FullSolution = panel.panel(EnhanceMarkDown("""## Full Solution
                                                     
We will add another element in the problem that was hidden so far to add more constraints. We define a division ratio between two inputs ~~~i,j~~~ which is part of an Odds ratio ~~~O_{ij}$12~~~ :
    
~~~ R_{ij} = \\frac{\#(X_{ik}=1 \\; & \\; X_{jk}=1)}{\#(X_{ik}=1 \\; & \\; X_{jk}=0)}$28~~~

&nbsp;

### Now we can define the Population Disease Occurrence Model Algorithm

** Step 1: ** Generate a population that matches the original untreated population statistics using EC. Extract invariant properties
from the solution.

** Step 2: ** Generate a population with the estimated treatment effect as a constraint while removing the constraint on the outcome and applying the invariant properties as additional constraints.

&nbsp;

Since we do not know what invariants represent the problem we can try different strategies representing assumptions.

&nbsp;

We show those strategies for target sepsis probability of 0.16.


| &nbsp; Step &nbsp; | &nbsp; N &nbsp; | &nbsp; P Sepsis &nbsp; | &nbsp; P Oxygen &nbsp; | &nbsp; P ROP  &nbsp;  | &nbsp; Odds Sep/Oxy  &nbsp; | &nbsp; Odds Sep/ROP &nbsp;  | &nbsp; Odds Oxy/ROP &nbsp;  | &nbsp; Ratio Sep/Oxy  &nbsp; | &nbsp; Ratio Sep/ROP &nbsp;  | &nbsp; Ratio Oxy/ROP &nbsp;  |
|:----:|:---:|:----------:|:---------:|:---------:|:------------:|:------------:|:------------:|:------:|:------:|:------:|
|   1  | 617 |    0.32    |    0.75   |    0.47   |      2.6     |      2.8     |      3.6     |    ?   |    ?   |    ?   |
|  2A  | 617 |    0.16    |    0.75   |     ?     |      2.6     |      2.8     |      3.6     |    ?   |    ?   |    ?   |
|  2B  | 617 |    0.16    |    0.75   |     ?     |      2.6     |      2.8     |      3.6     |    ?   |    ?   | Step 1 |
|  2C  | 617 |    0.16    |    0.75   |     ?     |      2.6     |      2.8     |      3.6     |    ?   | Step 1 |    ?   |
|  2D  | 617 |    0.16    |    0.75   |     ?     |      2.6     |      2.8     |      3.6     |    ?   | Step 1 | Step 1 |
|  2E  | 617 |    0.16    |    0.75   |     ?     |      2.6     |      2.8     |      3.6     | Step 1 |    ?   |    ?   |
|  2F  | 617 |    0.16    |    0.75   |     ?     |      2.6     |      2.8     |      3.6     | Step 1 |    ?   | Step 1 |
|  2E  | 617 |    0.16    |    0.75   |     ?     |      2.6     |      2.8     |      3.6     | Step 1 | Step 1 |    ?   |
|  2H  | 617 |    0.16    |    0.75   |     ?     |      2.6     |      2.8     |      3.6     | Step 1 | Step 1 | Step 1 |

&nbsp;

### We executed all those variations using High Performance Computing (HPC)

"""), width=1200, height=400)

Section0ResultsStep1Text = panel.panel(EnhanceMarkDown("""## Results Step 1
            
The EC algorithm 100 times, each time evolving the best solution. Recall that the solution is a population and we optimized many populations of populations

Step 1 results are summarized as follows:

&nbsp;


|Solution &nbsp; | &nbsp; N &nbsp; | &nbsp; P Sepsis &nbsp; | &nbsp; P Oxygen &nbsp; | &nbsp; P ROP  &nbsp;  | &nbsp; Odds Sep/Oxy  &nbsp; | &nbsp; Odds Sep/ROP &nbsp;  | &nbsp; Odds Oxy/ROP &nbsp;  | &nbsp; Ratio Sep/Oxy  &nbsp; | &nbsp; Ratio Sep/ROP &nbsp;  | &nbsp; Ratio Oxy/ROP &nbsp;  |
|:-------------|:---:|:----------:|:---------:|:---------:|:------------:|:------------:|:------------:|:-----:|:-----:|:-----:|
| Target       | 617 |    0.320   |   0.750   |   0.470   |     2.600    |     2.800    |     3.600    |       |       |       |
| Sol 1 (x98)  | 617 |    0.319   |   0.750   |   0.468   |     2.587    |     2.798    |     3.614    | 6.036 | 1.775 | 1.184 |
| Sol 2 (x1)   | 617 |    0.319   |   0.749   |   0.473   |     2.616    |     2.804    |     3.601    | 6.036 | 1.814 | 1.211 |
| Sol 3 (x1)   | 617 |    0.313   |   0.752   |   0.470   |     2.600    |     2.793    |     3.597    | 6.148 | 1.797 | 1.189 |
| Average      | 617 |    0.319   |   0.750   |   0.468   |     2.587    |     2.798    |     3.614    | 6.037 | 1.775 | 1.184 |

&nbsp;

### The average solution results were passed as parameters to Step 2 simulations

"""), width=1200, height=300)


Section0ResultsStep1Figure =  ObjectInlineHTML(CommonResourceDir + 'PlotAggregateResults_0.html',Width=1200,Height=6000)


Section0ResultsStep1 = panel.Column(Section0ResultsStep1Text,Section0ResultsStep1Figure)



Section0ResultsStep2Text = panel.panel(EnhanceMarkDown("""## Results Step 2

We executed the 8 strategy simulation for 12 different intervention levels, where target sepsis values starting from 0.30 to 0.08 with jumps of 0.02 . 

We show average results of 100 repetitions in a table for the the highest intervention level and the graphic output of all results.

&nbsp;

Results suggest that: When modeling the effect of a hypothetical treatment that drops sepsis from 32% to 8% of the population while keeping odds ratio constraints, 
different models show a change in ROP from **47%** to the range of **(40.9% - 47.5%)** where the most informed model reached **43%**. 

"""), width=1200, height=150)

Section0Step2ResultTable = panel.panel(EnhanceMarkDown("""#### Average results for intervention level = 12 where sepsis target = 0.08
|Strategy &nbsp;     | &nbsp; P Sepsis &nbsp; | &nbsp; P Oxygen &nbsp; | &nbsp; P ROP  &nbsp;  | &nbsp; Odds Sep/Oxy  &nbsp; | &nbsp; Odds Sep/ROP &nbsp;  | &nbsp; Odds Oxy/ROP &nbsp;  | &nbsp; Ratio Sep/Oxy  &nbsp; | &nbsp; Ratio Sep/ROP &nbsp;  | &nbsp; Ratio Oxy/ROP &nbsp;  |
|:-------------------|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
|Step 1 Ref          | 0.080 | 0.750 | 0.470 | 2.600 | 2.800 | 3.600 | 6.037 | 1.775 | 1.184 |
|A                   | 0.081 | 0.750 | 0.470 | 2.592 | 2.799 | 3.590 | 7.328 | 2.303 | 1.198 |
|B                   | 0.081 | 0.716 | 0.466 | 2.537 | 2.799 | 3.606 | 6.015 | 2.265 | 1.231 |
|C                   | 0.081 | 0.750 | 0.409 | 2.589 | 2.803 | 3.623 | 7.326 | 1.782 | 0.916 |
|D                   | 0.084 | 0.719 | 0.412 | 2.528 | 2.801 | 3.601 | 6.084 | 1.795 | 0.962 |
|E                   | 0.081 | 0.750 | 0.475 | 2.590 | 2.794 | 3.584 | 7.331 | 2.332 | 1.215 |
|F                   | 0.083 | 0.728 | 0.466 | 2.396 | 2.803 | 3.601 | 6.030 | 2.248 | 1.203 |
|G                   | 0.081 | 0.749 | 0.431 | 2.594 | 2.784 | 3.597 | 7.276 | 1.945 | 1.010 |
|H                   | 0.084 | 0.715 | 0.430 | 2.553 | 2.795 | 3.600 | 6.010 | 1.939 | 1.050 |
"""), width=1200, height=200)


Section0Step2ResultDeviationTable = panel.panel(EnhanceMarkDown("""#### Average deviations from step 1 reference for intervention level = 12 where sepsis target = 0.08 
| Strategy &nbsp; | &nbsp; P Sepsis &nbsp; | &nbsp; P Oxygen &nbsp; | &nbsp; P ROP  &nbsp;  | &nbsp; Odds Sep/Oxy  &nbsp; | &nbsp; Odds Sep/ROP &nbsp;  | &nbsp; Odds Oxy/ROP &nbsp;  | &nbsp; Ratio Sep/Oxy  &nbsp; | &nbsp; Ratio Sep/ROP &nbsp;  | &nbsp; Ratio Oxy/ROP &nbsp;  |
|:-------------------|:-----:|:------:|:------:|:------:|:------:|:------:|:------:|:-----:|:------:|
| A                  | 0.001 | 0.000  | 0.000  | -0.008 | -0.001 | -0.010 | 1.291  | 0.527 | 0.014  |
| B                  | 0.001 | -0.034 | -0.004 | -0.063 | -0.001 | 0.006  | -0.022 | 0.489 | 0.047  |
| C                  | 0.001 | 0.000  | -0.061 | -0.011 | 0.003  | 0.023  | 1.289  | 0.007 | -0.269 |
| D                  | 0.004 | -0.031 | -0.058 | -0.072 | 0.001  | 0.001  | 0.047  | 0.020 | -0.223 |
| E                  | 0.001 | 0.000  | 0.005  | -0.010 | -0.006 | -0.016 | 1.294  | 0.556 | 0.030  |
| F                  | 0.003 | -0.022 | -0.004 | -0.204 | 0.003  | 0.001  | -0.007 | 0.473 | 0.019  |
| G                  | 0.001 | -0.001 | -0.039 | -0.006 | -0.016 | -0.003 | 1.240  | 0.170 | -0.174 |
| H                  | 0.004 | -0.035 | -0.040 | -0.047 | -0.005 | 0.000  | -0.027 | 0.164 | -0.135 |

"""), width=1200, height=200)


Section0ResultsStep2Figure =  ObjectInlineHTML(CommonResourceDir + 'HoloviewsPlot.html',Width=1300,Height=1000)

Section0ResultsStep2SelectionTab = panel.layout.Tabs (
                                        ('Average Results Table' , Section0Step2ResultTable),
                                        ('Deviation from Reference Table' , Section0Step2ResultDeviationTable),
                                        ('Graphic output of all results' , Section0ResultsStep2Figure),
                                      )





Section0ResultsStep2 = panel.Column(Section0ResultsStep2Text,Section0ResultsStep2SelectionTab)


Section0Discussion = panel.panel(EnhanceMarkDown("""## Discussion
            
This solution is far from efficient and can be improved easily in multiple ways. 
However, it is better than what was available before since:
    
&nbsp;&nbsp;&nbsp;- It explores multiple hypothesis and shows solution distribution

&nbsp;&nbsp;&nbsp;- It addresses the discrete nature of this problem

&nbsp;&nbsp;&nbsp;- Efficient solution is not required for this kind of problem


&nbsp;

Following this work, the following recommendations are made:
    
&nbsp;&nbsp;&nbsp;(1) Epidemiological study results should be reported with higher precision

&nbsp;&nbsp;&nbsp;(2) Epidemiological studies should report more measurements 

&nbsp;&nbsp;&nbsp;(3) Epidemiological should provide additional possible explanations that can be added as assumptions

"""), width=1200, height=400)

   
Section0ReproducibilityText = panel.panel("""### Reproducibility:
The results for this paper were calculated on:
    
&nbsp;&nbsp;&nbsp;- Laptop computer with 4 cores and Windows 10 deployed by Anaconda (64-bit) with python 2.7.14, dask 0.17.2, bokeh 0.13.0, inspyred 1.0, numpy 1.14.2 , holoviews 1.10.7 

&nbsp;&nbsp;&nbsp;- Compute server with 64 cores, Linux 18.04, Anaconda (64-bit) python 2.7.15, dask 0.19.1, bokeh 0.13.0, inspyred 1.0, numpy 1.15.3, holoviews 1.10.7. The code is stored in the [GitHub repository](https://github.com/Jacob-Barhak/PopDOM)

The numbers used in this paper are taken from [This 2018 paper](https://doi.org/10.5210/ojphi.v10i2.9357)). Those numbers are close to the numbers in [this original 2011 work](https://doi.org/10.1159/000312821), yet are not an exact match, so the analysis in this paper should not be considered for epidemiological use without further exploration into the differences. 

This presentation is generated using Python 2.7.15, panel 0.5.0a3, bokeh 1.1.0dev9 .

The presentation is accessible through the QR code Below. The presentation code can be accessed [here](https://github.com/Jacob-Barhak/Presentations/tree/master/MODSIM2019).

""", width=1200, height=180)

Section0Reproducibility = panel.Column(Section0ReproducibilityText, PresentationURL)

Section0References = panel.panel("""### Selected Publications:

[1] [Olaf Dammann, Kenneth Chui, Anselm Blumer, (2018) A Causally Naive and Rigid Population Model of Disease Occurrence Given Two Non-Independent Risk Factors, Online Journal of Public Health Informatics]( https://doi.org/10.5210/ojphi.v10i2.9357)

[2] [Chen M, Citil A, McCabe F, Leicht, Fiascone, Dammann C.E.L., Dammann O., (2011). Infection, oxygen, and immaturity: interacting risk factors for retinopathy of prematurity. Neonatology. 99, 125-32.](https://doi.org/10.1159/000312821)

[3] [Inspyred library on GitHub](https://github.com/aarongarrett/inspyred)                                 

[4] [J. Barhak, A. Garrett, Population Generation from Statistics Using Genetic Algorithms with MIST + INSPYRED. MODSIM World 2014, April 15 - 17, Hampton Roads Convention Center in Hampton, VA.](http://sites.google.com/site/jacobbarhak/home/MODSIM2014_MIST_INSPYRED_Paper_Submit_2014_03_10.pdf)'

[5] [Barhak J. (2015). The Reference Model uses Object Oriented Population Generation. SummerSim 2015. Chicago IL, USA.](http://dl.acm.org/citation.cfm?id=2874946)

[6] [MIcro Simulation Tool (MIST](https://github.com/Jacob-Barhak/MIST)

""", width=1200, height=100)

Section0Acknowledgments = panel.panel("""### Acknowledgments: 
                                      
Many thanks to Philipp Rudiger who published open source code that assisted in visualization that proved very useful. 

Many thanks to James Bednar who introduced holoviews that allows easy visualization of this data and to Jean-Luc Stevens for creating holoviews. 

Thanks to Matthew Rocklin for dask support.
""", width=1200, height=400)
               
TitleHTML = 'MODSIM World 2019 Presentation: Population Disease Occurrence Models Using Evolutionary Computation'

SlideSelectorTab = panel.layout.Tabs (
                                        ('Problem' , Section0Problem),
                                        ('Definitions' , Section0Definitions),
                                        ('Analytical', Section0AnalyticalSolution),
                                        ('Evolutionary Computation',Section0EvolutionaryComputation),
                                        ('Simple Solution',Section0SimpleSolution),
                                        ('Full Solution',Section0FullSolution),
                                        ('Results Step 1',Section0ResultsStep1),
                                        ('Results Step 2',Section0ResultsStep2),
                                        ('Discussion',Section0Discussion),
                                        ('Reproducibility', Section0Reproducibility),
                                        ('Acknowledgments' , Section0Acknowledgments),
                                        ('References' , Section0References),
                                      )

Section0 = panel.Column(Section0Header, SlideSelectorTab)

DocumentForOutput = Section0._get_root(BokehDocument)

Html = bokeh.embed.file_html(DocumentForOutput, bokeh.resources.CDN, TitleHTML)

OutFile = open('Presentation_MODSIM_2019.html','w')
OutFile.write(Html)
OutFile.close()

