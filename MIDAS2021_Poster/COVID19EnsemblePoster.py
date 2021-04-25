###############################################################################
# The Reference Model for COVID-19 is Now a Multi-Scale Ensemble Model
# Copyright (C) 2021 Jacob Barhak 
# The work reported is protected by 2 US. Patents:
# 
# * J. Barhak, Reference model for disease progression - United States Patent 9,858,390, January 2, 2018
# * J. Barhak, Analysis and Verification of Models Derived from Clinical Trials Data Extracted from a Database, U.S. Patent Number 10,923,234, February 16, 2021
#
# Therefore attempts for reimplementation should be consulted with the author
###############################################################################
#
# Feel free to contact the author
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
# without their support and development of HoloViz visualization tools, this
# interactive paper would not be possible.



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
import re


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

def ObjectExternalHTML(ExtrnalFileName,Width=Width,Height=700):
    'Encodes html from a file into object as an external file'
    RetStr = '<object width="%i" height="%i" data="%s">Warning:%s Not Accessible!</object>'%(Width, Height, ExtrnalFileName,ExtrnalFileName)
    return RetStr


def ObjectInlineHTML(ExtrnalFileName,Width=Width,Height=700):
    'Encodes html from a file into a panel object'
    DataFile = open(ExtrnalFileName,'rb')
    Data = DataFile.read()
    DataFile.close()
    Figure_4 = panel.pane.HTML(Data, width=Width, height=Height)
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


TitleHTML = 'The Reference Model for COVID-19 is Now a Multi-Scale Ensemble Model'
SavedFileName = 'Poster_COVID19_Ensemble_2021.html'
PublishURL = 'https://jacob-barhak.github.io/'+SavedFileName
CodePublishURL = 'https://github.com/Jacob-Barhak/InteractivePapers/tree/master/MIDAS2021_Poster'
QRCodeFileName = 'COVID19_Ensemble_2021_Poster.png'

PresentationURL = panel.panel(ConstractImageLinkAnchor(PublishURL,QRCodeFileName,'View this paper on the web',380), width=380, height=380)

PresentationTitle = panel.panel('# The Reference Model for COVID-19 is Now a Multi-Scale Ensemble Model', width=Width, height=40, margin = (0,0,0,0))
PresentationVenue = panel.panel('***MIDAS Annual Meeting 2021 -  May 10 to 13*** [Online](https://midasnetwork.us/midas-network-annual-meeting-midas-2021/)', width=950, height=40, margin = (0,0,0,0))

PresentationAuthors = panel.panel("By: ***[Jacob Barhak](https://sites.google.com/view/jacob-barhak/home)***", width=600, height=40, margin = (0,0,0,0))

PresentationHeader = panel.Column( PresentationTitle,  panel.Row (PresentationAuthors , PresentationVenue, margin = (0,0,0,0)), margin = (0,0,0,0))


ReferencesText = """### References

1. The COVID tracking project at the Atlantic. (2020). Accessed: July 3, 2020: <https://covidtracking.com/>
   
2. MIDAS, Models of Infectious Disease Agent Study. Online: <https://midasnetwork.us/>
   
3. IMAG: Multiscale Modeling and Viral Pandemics. Online: <https://www.imagwiki.nibib.nih.gov/working-groups/multiscale-modeling-and-viral-pandemics>
   
4. IMAG: Interagency Modeling and Analysis Group. Online: <https://www.imagwiki.nibib.nih.gov/>
   
5. Barhak J , The Reference Model Initial Use Case for COVID-19. Cureus.  <http://dx.doi.org/10.7759/cureus.9455> , Online: <https://www.cureus.com/articles/36677-the-reference-model-an-initial-use-case-for-covid-19> . PMCID: PMC7392354 , PMID: 32760637 , Interactive Results: <https://jacob-barhak.netlify.app/thereferencemodel/results_covid19_2020_06_27/combinedplot>
   
6. CDC - COVID-19: forecasts of total deaths. (2020). Accessed: July 3, 2020: <https://www.cdc.gov/coronavirus/2019-ncov/covid-data/forecasting-us.html>
   
7. The COVID-19 Forecast Hub online: <https://covid19forecasthub.org/>
   
8. The Reich Lab at UMass-Amherst @ Github : COVID-19 Forecast Hub  <https://github.com/reichlab/covid19-forecast-hub>
   
9. N.E. Dean, A. Pastore y Piontti, Z.J. Madewell, D.A. Cummings, M.D.T. Hitchings, K. Joshi, R. Kahn, A. Vespignani, M. Elizabeth Halloran, I.M. Longini Jr., Ensemble Forecast Modeling for the Design of COVID-19 Vaccine Efficacy Trials, Vaccine (2020), doi: <https://doi.org/10.1016/j.vaccine.2020.09.031>
   
10. Ray EL, Reich NG (2018) Prediction of infectious disease epidemics via weighted density ensembles. PLoS Comput Biol 14(2): e1005910. <https://doi.org/10.1371/journal.pcbi.1005910>
   
11. David H. Wolpert , Stacked Generalization . December 1992Neural Networks 5(2):241-259,  <https://doi.org/10.1016/S0893-6080(05)80023-1>
   
12. J. Barhak, The Reference Model for Disease Progression. SciPy 2012, Austin Tx, 18-19 July 2012. Paper: <http://dx.doi.org/10.25080/Majora-54c7f2c8-007> ,  <https://github.com/Jacob-Barhak/scipy_proceedings/blob/2012/papers/Jacob_Barhak/TheReferenceModelSciPy2012.rst> , Poster: <http://sites.google.com/site/jacobbarhak/home/PosterTheReferenceModel_SciPy2012_Submit_2012_07_14.pdf> 
   
13. J. Barhak, A. Garrett, W. A. Pruett, Optimizing Model Combinations, MODSIM world 2016. 26-28 Apr, Virginia Beach Convention Center, Virginia Beach, VA. Paper: <http://www.modsimworld.org/papers/2016/Optimizing_Model_Combinations.pdf> Presentation: <http://sites.google.com/site/jacobbarhak/home/MODSIM2016_Submit_2016_04_25.pptx>
   
14. J. Barhak, The Reference Model for Disease Progression Combines Disease Models. I/IITSEC 2016 28 Nov - 2 Dec Orlando Florida. Presentation: <http://sites.google.com/site/jacobbarhak/home/IITSEC2016_Upload_2016_11_05.pptx> Paper: <http://www.iitsecdocs.com/volumes/2016> 
   
15. J. Barhak, The Reference Model: A Decade of Healthcare Predictive Analytics with Python, PyTexas 2017, Nov 18-19, 2017, Galvanize, Austin TX. Video: <https://youtu.be/Pj_N4izLmsI> Presentation: <http://sites.google.com/site/jacobbarhak/home/PyTexas2017_Upload_2017_11_18.pptx> 
   
16. J. Barhak, Reference model for disease progression - United States Patent 9,858,390, January 2, 2018 <https://patents.google.com/patent/US20140297241A1/en>
   
17. J. Barhak, Analysis and Verification of Models Derived from Clinical Trials Data Extracted from a Database, U.S. Patent Number 10,923,234, February 16, 2021 <https://patents.google.com/patent/US20170286627A1/en?inventor=barhak>
   
18. CDC, Daily Updates of Totals by Week and State Provisional Death Counts for Coronavirus Disease 2019 (COVID-19) Online: <https://www.cdc.gov/nchs/nvss/vsrr/covid19/index.htm>
   
19. Jacob Barhak, The Reference Model for Disease Progression Handles Human Interpretation, MODSIM World 2020. Paper: <https://www.modsimworld.org/papers/2020/MODSIM_2020_paper_42_.pdf>  Interactive Results: <https://jacob-barhak.netlify.app/thereferencemodel/results_2020_03_21_visual_2020_03_23/CombinedPlot.html>
   
20. Rich A, Yin  L, Johannes Ernst Gehrke, Paul  Koch, Marc  Sturm, Noemie Elhadad, Intelligible Models for HealthCare: Predicting Pneumonia Risk and Hospital 30-day Readmission. KDD '15: Proceedings of the 21th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining August 2015 Pages 1721-1730 <https://doi.org/10.1145/2783258.2788613>
   
21. Population density data provided by U.S. Census. (2020). Accessed: July 3, 2020: <https://www2.census.gov/programs-surveys/decennial/tables/2010/2010-apportionment/pop_density.csv>
   
22. United States Census Bureau: explore census data. (2020). Accessed: July 3, 2020: <https://data.census.gov/>
   
23. Barhak J, Garrett A: Evolutionary computation examples with Inspyred. PyCon Israel. 2018, Accessed: July 3, 2020: <https://youtu.be/PPpmUq8ueiY>
   
24. DHS Science and Technology: Master Question List for COVID-19 (caused by SARS-CoV-2): Weekly Report, 26 May 2020. DHS Science and Technology Directorate, USA; 2020. <https://www.dhs.gov/publication/st-master-question-list-covid-19>
   
25. Johns Hopkins Center for Health Security:  Coronaviruses: SARS, MERS, and 2019-nCoV .  Updated April 14, 2020.  <https://www.centerforhealthsecurity.org/resources/fact-sheets/pdfs/coronaviruses.pdf>
   
26. Stephen A. Lauer, Kyra H. Grantz, Qifang Bi, Forrest K. Jones, Qulu Zheng, Hannah R. Meredith, Andrew S. Azman, Nicholas G. Reich, Justin Lessler. The Incubation Period of Coronavirus Disease 2019 (COVID-19) From Publicly Reported Confirmed Cases: Estimation and Application. Annals of Internal Medicine,  <https://doi.org/10.7326/M20-0504>
   
27. Qun Li,  Xuhua Guan, Peng Wu,  Xiaoye Wang, , Lei Zhou, Yeqing Tong,  Ruiqi Ren,  Kathy S.M. Leung,  Eric H.Y. Lau, , Jessica Y. Wong,Xuesen Xing, Nijuan Xiang, , Yang Wu, Chao Li, M.P.H., Qi Chen, , Dan Li, Tian Liu, B.Med., Jing Zhao, Man Liu, Wenxiao Tu, , Chuding Chen, Lianmei Jin, Rui Yang,  Qi Wang, , Suhua Zhou,  Rui Wang, Hui Liu, , Yinbo Luo,  Yuan Liu, Ge Shao,  Huan Li, Zhongfa Tao, Yang Yang, Zhiqiang Deng,  Boxi Liu,  Zhitao Ma,  Yanping Zhang, Guoqing Shi,  Tommy T.Y. Lam,  Joseph T. Wu,  George F. Gao, Benjamin J. Cowling,  Bo Yang,  Gabriel M. Leung,  and Zijian Feng, Early Transmission Dynamics in Wuhan, China, of Novel Coronavirus-Infected Pneumonia, N Engl J Med 2020; 382:1199-1207 <https://doi.org/10.1056/NEJMoa2001316>
   
28. Ruiyun Li, Sen Pei, Bin Chen, Yimeng Song, Tao Zhang, Wan Yang, Jeffrey Shaman. Substantial undocumented infection facilitates the rapid dissemination of novel coronavirus (SARS-CoV2), Science  01 May 2020: Vol. 368, Issue 6490, pp. 489-493. doi: <https://doi.org/10.1126/science.abb3221>   web link: <https://science.sciencemag.org/content/sci/early/2020/03/13/science.abb3221.full.pdf>
   
29. Ruian Ke, Carolin Zitzmann, Ruy M. Ribeiro, Alan S. Perelson. Kinetics of SARS-CoV-2 infection in the human upper and lower respiratory tracts and their relationship with infectiousness.  medRxiv 2020.09.25.20201772; doi: <https://doi.org/10.1101/2020.09.25.20201772>
   
30. W.S. Hart, P.K. Maini, R.N. Thompson , High infectiousness immediately before COVID-19 symptom onset highlights the importance of contact tracing. medRxiv 2020.11.20.20235754; doi: <https://doi.org/10.1101/2020.11.20.20235754>

31. Jacob Barhak Github - COVID-19 Infectiousness Models from Multiple Sources <https://github.com/Jacob-Barhak/COVID19Models/tree/main/COVID19_Infectiousness_Multi>
   
32. Del Valle SY, Hyman JM, Hethcote HW, Eubank SG: Mixing patterns between age groups in social networks. Soc Networks. 2007, 29:539-554. <https://doi.org/10.1016/j.socnet.2007.04.005>
   
33. Edmunds WJ, O'Calaghan CJ, Nokes DJ: Who mixes with whom? A method to determine the contact patterns of adults that may lead to the spread of airborne infections. Proc R Soc Lond B. 1997, 264:949-957. <https://doi.org/10.1098/rspb.1997.0131>
   
34. Apple,  Mobility Trends, online:  <https://covid19.apple.com/mobility> . Data file downloaded 2020-07-11
   
35. CDC COVID-19 Response Team: Severe outcomes among patients with coronavirus disease 2019 (COVID-19) - United States, February 12-March 16, 2020. MMWR Morb Mortal Wkly Rep. 2020, 69:343-346. <https://dx.doi.org/10.15585/mmwr.mm6912e2> 
   
36. The Novel Coronavirus Pneumonia Emergency Response Epidemiology Team. The Epidemiological Characteristics of an Outbreak of 2019 Novel Coronavirus Diseases (COVID-19) - China, 2020<J>. China CDC Weekly, 2020, 2(8): 113-122. doi: <https://doi.org/10.46234/ccdcw2020.032> 
   
37. Fei Zhou,Ting Yu,Ronghui Du,Guohui Fan,Ying Liu,Zhibo Liu,Jie Xiang,Yeming Wang,Bin Song,Xiaoying Gu,Lulu Guan,Yuan Wei,Hui Li,Xudong Wu,Jiuyang Xu,Shengjin Tu,Yi Zhang,Hua Chen,Bin Cao. Clinical course and risk factors for mortality of adult inpatients with COVID-19 in Wuhan, China: a retrospective cohort study. Lancet. 2020 28 March-3 April; 395(10229): 1054-1062. Published online 2020 Mar 11. <https://doi.org/10.1016/S0140-6736(20)30566-3>
   
38. MSM Working Group on Multiscale Modeling SARS-CoV-2 infection: a cohort study performed in-silico, by Filippo Castiglione. Online:  <https://youtu.be/DUp7EwiRckc>
   
39. Filippo Castiglione, Debashrito Deb, Anurag P. Srivastava, Pietro Lio, Arcangelo Liso From infection to immunity: understanding the response to SARS-CoV2 through in-silico modeling. bioRxiv 2020.12.20.423670; doi: <https://doi.org/10.1101/2020.12.20.423670>
   
40. Jacob Barhak Github - COVID-19 mortality model by Filippo Castiglione et. al. <https://github.com/Jacob-Barhak/COVID19Models/tree/main/COVID19_Mortality_Castiglione>
   
41. Wikipedia, David Levy (chess player) <https://en.wikipedia.org/wiki/David_Levy_(chess_player)#Computer_chess_bet>
   
42. Del Valle SY, Hyman JM, Hethcote HW, Eubank SG: Mixing patterns between age groups in social networks. Soc Networks. 2007, 29:539-554. <https://doi.org/10.1016/j.socnet.2007.04.005>
   
43. Edmunds WJ, O'Calaghan CJ, Nokes DJ: Who mixes with whom? A method to determine the contact patterns of adults that may lead to the spread of airborne infections. Proc R Soc Lond B. 1997, 264:949-957. <https://doi.org/10.1098/rspb.1997.0131>


"""

RefDict = ExtractReferencesDict(ReferencesText)

print "located %i References: " % len(RefDict.keys())




Section0 = panel.panel(FixReferences(RefDict, """## ABSTRACT: 
The COVID-19 pandemic produced a large number of computational models and initiatives. Many models were aimed at forecast and parameter extraction and resulted in plenty of results, many times different than each other. One reason for differences was that the models were based on different assumptions made by modelers. Considering that humans with different views construct those models, the models themselves should be viewed as assumptions attempting to explain a phenomenon. To gain good comprehension of the phenomena observed, there is a need to combine those models.

The Reference Model for disease progression was initially a diabetes model using the approach of assembling models and validating them against different populations from clinical trials. The model performed simulation at the individual level while modeling entire populations using the MIcro-Simulation Tool (MIST) that employed High Performance Computing (HPC). A few years ago this approach created an ensemble of models that compete and cooperate and reached the achievement of being the most validated diabetes cardiovascular model known.

The Reference Model was transformed to model COVID-19 with the start of the epidemic. The model is now composed of multiple models that represent different phenomena such as models for: infectiousness, transmission, human response, and mortality. Some of those models were calculated using at different scales including cell scale, organ scale, individual scale, and population scale. The Reference Model has therefore now reached the achievement of being the first known multi-scale ensemble model for COVID-19.

*** This is an interactive poster - please explore the tabs above and interact with the figures - they have sliders and widgets and hover information that will allow interaction. Following the tabs in order from left to right will tell the story ***
"""), width=Width, height=None)



Section1_0 = panel.panel(FixReferences(RefDict,"""### Introduction
The Reference Model for disease progression was was extensively published in [12],[13],[14],[15],[19] and patented [16],[17]. With the start of the COVID-19 pandemic the modeling technology was adapted to handle infectious diseases and specifically COVID-19 in [5]. This approach was extended to construct *** the first multi-scale ensemble model for COVID-19 ***!  
"""), width=Width, height=None)


Figure_1 = panel.panel(ConstractImageLinkAnchor('https://simtk.org/projects/therefmodel','TheReferenceModelCOVID19_Figure1.png','View the model web site',900), width=Width, height=380)


Section1_1_2 = panel.panel(FixReferences(RefDict,"""

The ensemble model structure is presented above . The transition probabilities between states is controlled by multiple models:

* ***Infectiousness Models***: Indicating the level of infectiousness of each individual from time of infection. 
* ***Transmission Models***: Indicating the probability of contracting the disease considering encounters with infected individuals.
* ***Response models***: The behavior choice of each individual that affects the number of interactions in response to the pandemic. 
* ***Mortality Models***: A variety of models defining mortality of infected individuals 
    * ***Mortality rate models***: Mortality tables indicating the probability of dying from COVID-19 by age.
    * ***Mortality time***: Models attempting to estimate the time of death in days since infection
    * ***Mortality distribution***: A model that indicates the daily probability of mortality by age group since infection. 
* ***Recovery model***: defines condition of recovery as a combination of infectiousness, mortality probability, mortality time, and time since infection. 

The Reference Model combines these models and matches their results to results from The COVID Tracking project [1] every 10 days for 60 days to extract the best ensemble.

### Initialization
Populations for 51 US states and territories were generated from data of multiple sources: 

* The Covid Tracking project [1] at the first day of simulation April 1st 2020. 
* Age and state/territory statistics from US Census [21],[22]. 
* Number of Interaction per individual according to [42],[43].

Evolutionary computation is used to optimize the randomly generated individuals to match the target statistics.


"""), width=Width, height=None)
 

Section1 = panel.Column(Section1_0, Figure_1, Section1_1_2, margin = (0,0,0,0))


Section2_1 = panel.panel(FixReferences(RefDict,"""### Infectiousness
During the pandemic, the DHS released a master question list about the pandemic [24]. The version from 26 May 2020 has the following question: "What is the average infectious period during which individuals can transmit the disease?". Infectiousness models attempt to answer this question.  

There were 4 relative infectiousness curves used in the ensemble extracted from [28],[29],[30] and was made public in [31].

"""), width=Width, height=None)

Figure_2 = ObjectInlineHTML(ResourceDir + '/COVID19_Infectiousness_Multi.html', Width=1150, Height=620)


Section2 = panel.Column(Section2_1, Figure_2, margin = (0,0,0,0))


css = """
div.special_table + table * {
  border: 1px solid blue;
  text-align: left;
}
"""

panel.extension(raw_css=[css])


Section3 = panel.panel(FixReferences(RefDict,"""
#### Transmission models

The transmission model considers 3 elements:

1. ***Individual Encounter*** - What is the probability of transmission in case infected individuals are encountered. It defines the probability in percent of contracting the disease per one encounter with an infected person. 
2. ***Population Density*** - How does this probability change with population density. This is controlled by a coefficient that indicates the relative population density boost to the probability per encounter. 
3. ***Random Constant*** - What is the probability of contracting the disease due to another reason other than direct contact with a modeled infectious person. For example, contracting the virus from a person outside the modeled group, such as a person visiting out of state falls into this group.

We have 4 variations of models using different values for those parameters. 

<div class="special_table"></div>
| Transmission Function  | Individual Encounter | Population Density    | Random Constant |  Comments / Rational                                                                                                                                                        |
|:-----------------------|:---------------------|:----------------------|:----------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1                      | 0.5                  | 0                     | 1e-6            | Low bound - Similar to previous publication with slightly lower a to represent a low bound while ignoring density and adding a small constant.                              |
| 2                      | 10                   | 0                     | 4e-6            | Very high a that is probably unreasonable and adding a higher randomness. This was added on purpose to show how unreasonable assumptions are treated in the ensemble.       |
| 3                      | 1.5                  | 0.1                   | 0               | Reasonable assumption - elevated transmission with original population density.                                                                                             |
| 4                      | 2.5                  | 0.2                   | 0               | Reasonable assumption - more elevated transmission with elevated population density.                                                                                        |

"""), width=Width, height=None)




Section4 = panel.panel(FixReferences(RefDict,"""### Response Models
Response models represent behavior of different individuals in response to the pandemic:

<div class="special_table"></div>
| Response Model | Model Description                                                                                                                                                           |
|:---------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1              | Apple mobility interpolates level of interactions beyond family size. 10% infected people randomly reduce their number of interactions daily until family size is reached.  |
| 2              | Apple mobility interpolates level of interactions beyond family size.  20% infected people randomly reduce their number of interactions daily until family size is reached. |
| 3              | Healthy individuals do not change behavior. Infected persons drop to interaction with family only.                                                                          |

"""), width=Width, height=None)


Section5 = panel.panel(FixReferences(RefDict,"""### Mortality Models
There were several mortality models merged:

1. Mortality rate by age extracted from:

    * US CDC Low Bound [35] 
    * US CDC High Bound [35]  
    * The Novel Coronavirus Pneumonia Emergency Response Epidemiology Team Table 1 Case fatality rate column [36] 

2. Mortality Time:

    * Zhou et. al. [37] - Adapted form table 2 non survivor column - Time from illness onset to death or discharge
    * The COVID Tracking Project [1] - Calculated statistics from finding the first death per state since first diagnosis

3. Mortality of an individual per age per day from infection 

    * Castiglione et. al. [38] reimplemented in [40].

"""), width=Width, height=None)



Section6_1 = panel.panel(FixReferences(RefDict,"""### Results
The results presented here was executed on 32 nodes x 36 cores = 1152 cores total for almost 49 hours - this roughly means roughly 6.6 years or computation on a single CPU core.  

The Interactive plots blow summarize the results: 

* ***Population Plot - Top Left*** - This plot shows difference between model and observed data - fitness. The fitness score is displayed for each state population every 10 days as a circle. A viewer hovering with the mouse over the circle will see information about the population at that time including number of infections and deaths. The numbers are presented as model projection / observed numbers by the COVID tracking project. The numbers are scaled to cohort batch size of 10,000 individuals in this simulation. The fitness score in this paper is very close to the mortality difference with slight influence of 1/1000 from difference of infections. Note that COVID-19 death is much more accurate than infection numbers.
       
* ***Model Mixture Plot - Top Right*** -  This plot shows the influence of each model on the ensemble. Models from the same group that compete with each other are presented in the same color and their combined influence will be 1. Initially all models in a group have the same influence so in iteration 1 - the plot shows many bars in the same height. When dragging the iteration slider and increasing the iteration, it is possible to see that some models gain influence while others lose it. In one case a transmission model is fully rejected. 
       
* ***Convergence Plot - Bottom*** - This plot shows the weighted average fitness for the US states and territories used for each iteration. The blue vertical line shows the current iteration, while the large yellow circle shows the fitness for the unperturbed simulation that is the base of the optimization algorithm. The small circles show the results for the perturbed simulations, those help determine sensitivity and are used in optimization. The red horizontal lines represent the average fitness considering all the simulations in an iteration. This plot clearly shows some models are outliers in some iterations by seeing a spread far away from the unperturbed solution. 

The interesting element in this simulation is the elimination of the second transmission model that had a high transmission rate.
"""), width=Width, height=None)


Figure_4 = ObjectInlineHTML(ResourceDir + '/CombinedPlot.html', Width=1150, Height=620)


Section6 = panel.Column(Section6_1, Figure_4, margin = (0,0,0,0))


Section7_1 = panel.panel(FixReferences(RefDict,"""### Combined Infectiousness Model

***The relative infectiousness per day since infection as assembled by the ensemble***
"""), width=Width, height=None)


Figure_5 = ObjectInlineHTML(ResourceDir + '/EnsembleInfectiousness.html', Width=1150, Height=520)

Section7 = panel.Column(Section7_1, Figure_5, margin = (0,0,0,0))



Section8_1 = panel.panel(FixReferences(RefDict,"""### Combined Mortality Model

***The mortality rate and time assembled by the ensemble. Top: Mortality rate, Bottom: Mortality Time.***
"""), width=Width, height=None)


Figure_6 = ObjectInlineHTML(ResourceDir + '/EnsembleMortality.html', Width=1150, Height=620)

Figure_3 = ObjectInlineHTML(ResourceDir + '/COVID19_Mortality_Castiglione.html', Width=1150, Height=620)

Section8_2 = panel.panel(FixReferences(RefDict,"""

The influence of all mortality models in this simulation remain mostly unchanged. Note that even different models from different types did not change - this may indicate that the main driver of mortality relies on other models more and simulation is has not reach the fine resolution where mortality models have influence. However, mortality numbers are underestimated by the combined model. 

The Castiglione et. all model below that combines are and rate has roughly the same influence as all above models combined. 

***The Castiglione et. al model***

"""), width=Width, height=None)

Section8 = panel.Column( Section8_1, Figure_6, Section8_2, Figure_3, margin = (0,0,0,0))


Section9_1 = panel.panel(FixReferences(RefDict,"""### Conclusions
* Results presented underestimate the disease impact 

* It is still unclear if it is possible to explain the phenomena like COVID-19 impact in a population in a period of two months using only initial conditions and mechanistic models. 

* The phenomena itself is random and has large variability, even between states, and behavior patterns in each state were different.

* More work is needed to improve machine comprehension - even this technology requires additional research.

* Future work will include adding human interpretation to the computational models.

"""), width=700, height=None)



Section9SummaryText = panel.panel(FixReferences(RefDict,"""
### Acknowledgments: 
This work used the High-Performance Computing Environment provided by the MIDAS Coordination Center, supported by NIGMS grant 5U24GM132013 and the NIH STRIDES program. Thanks for the Rescale clouds who provided additional cloud infrastructure. Thanks to Amazon AWS and Microsoft Azure that provided cloud credits for simulation.  Thanks to John Rice and Jered Hodges for hosting and taking care of a server for simulations. Thanks to Filippo Castiglione, Robin Thompson, William Hart, and Alan Perelson for making available mortality and infectiousness models that were integrated in the model. Thanks to the MSM viral pandemic working group that helped make the connections and support model development. Thanks to the COVID tracking project for providing a special license for using the data.  Thanks to all other sources of data that make it available easily online, including Apple for mobility data, US Census, Los Alamos National Lab. Thanks to Harel Dahari who made the connection to the MIDAS network and IMAG wiki for providing information to connect to Rescale. Thanks to Philipp Rudiger, James Bednar, and Jean-Luc Stevens for helping with HoloViz technologies that created this interactive paper. Thanks To Deanna J.M. Isaman who introduced me to disease modeling.

### Conflict of Interest Statement:
Payment/services info: Dr. Barhak reports non-financial support and other from Rescale, and MIDAS Network, other from Amazon AWS, Microsoft Azure, MIDAS network, other from The COVID tracking project at the Atlantic,  other from John Rice and Jered Hodges, 
Financial relationships: Jacob Barhak declare(s) employment from MacroFab, United Solutions, B. Well Connected health. The author had a contract with MacroFab, United Solutions, and B. Well during the work. However, none of these companies had influence on the modeling work reported in the paper. Jacob Barhak declare(s) employment and Technical Support from Anaconda. The author contracted with Anaconda in the past and uses their free open source software tools. Also the Author received free support from Anaconda Holoviz team and Dask teams. Intellectual property info: Dr. Barhak has a patent US Patent 9,858,390 - Reference model for disease progression issued to Jacob Barhak, and a patent US patent Utility application #15466535 - Analysis and Verification of Models Derived from Clinical Trials Data Extracted from a Database. Other relationships: During the conduct of the study; personal fees from United Solutions, personal fees from B. Well Connected health, personal fees and non-financial support from Anaconda, outside the submitted work; In addition, Dr. Barhak has a patent US Patent 9,858,390 - Reference model for disease progression issued to Jacob Barhak, and a US patent Number 10,923,234 - Analysis and Verification of Models Derived from Clinical Trials Data Extracted from a Database pending to Jacob Barhak and The author was engaged with a temporary team formed for a duration of the Pandemic Response Hackathon. The team consisted of Christine Mary, Doreen Darsh, Lisbeth Garassino . They supported work during the Hackathon in initial stages of this work. Many others have expressed their support in this project. This has been publicly reported here: https://devpost.com/software/improved-disease-modeling-tools-for-populations . However, despite all support, Dr. Barhak is solely responsible for modeling decisions made for this paper an is responsible for its contents.

### Reproducibility:
Results presented in this work are archived in the file MIST_Ref_COVID19_Large_2021_01_26_Midas.zip for reproducibility purposes. MIST version 0.99.5.0 and python 2.7.18 with the Anaconda distribution were used for executing the simulation on the MIDAS cloud. 
Visualization processing is archived in: ExplorationCOVID19_2021_01_26_10Kx40x51_Midas_AddedVisual_20201_02_09.zip. 
This presentation is accessible [here](%s). The code that generated the presentation can be accessed [here](%s). This presentation is generated using Python 2.7.16, panel-0.8.0, holoviews 1.12.7, bokeh-1.4.0.
"""%(PublishURL,CodePublishURL)), width=Width, height=None)

Section9 = panel.Column( panel.Row(Section9_1,PresentationURL, margin = (0,0,0,0)), Section9SummaryText, margin = (0,0,0,0))

SectionSelectorTab = panel.layout.Tabs (
                                        ('Abstract',Section0),
                                        ('Introduction', Section1),
                                        ('Infectiousness', Section2),
                                        ('Transmission', Section3),
                                        ('Response Models', Section4),
                                        ('Mortality Models', Section5),
                                        ('Results', Section6),
                                        ('Results Infectiousness', Section7),
                                        ('Results Mortality', Section8),
                                        ('Conclusions', Section9),
                                        margin = (0,0,0,0), 
                                        )
#Section6References = panel.panel(ReferencesText, width=Width, height=None)

                                       
Presentation = panel.Column(PresentationHeader, SectionSelectorTab)
Presentation.save(SavedFileName, resources=INLINE, title=TitleHTML)       

