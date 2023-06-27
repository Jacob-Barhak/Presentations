###############################################################################
# The Reference Model for COVID-19 - The First Multi-Scale Ensemble Disease Model
# Copyright (C) 2021-2022 Jacob Barhak 
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


TitleHTML = 'The Reference Model for COVID-19 attempts to explain USA data'
SavedFileName = 'COVID19_Ensemble_Latest.html'
PublishURL = 'https://jacob-barhak.github.io/'+SavedFileName
CodePublishURL = 'https://github.com/Jacob-Barhak/Presentations/tree/master/COVID19_Ensemble_Latest'
QRCodeFileName = 'COVID19_Ensemble_Latest.png'
 
PresentationURL = panel.panel(ConstractImageLinkAnchor(PublishURL,QRCodeFileName,'View this publication on the web',380), width=380, height=380)

PresentationTitle = panel.panel('# The Reference Model for COVID-19 attempts to explain USA data', width=Width, height=40, margin = (0,0,0,0))
PresentationVenue = panel.panel('[28-29 June 2023, 2023 MSM Consortium Meeting - Past2Future, NIH Campus, Natcher Conference Center, Bethesda MD](https://www.imagwiki.nibib.nih.gov/index.php/imag-events/2023-MSM-Meeting)', width=740, height=40, margin = (0,0,0,0))

PresentationAuthors = panel.panel("By: ***[Jacob Barhak](https://sites.google.com/view/jacob-barhak/home)***", width=280, height=40, margin = (0,0,0,0))

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

45. Lucas Bottcher, Mingtao Xia, Tom Chou. Why case fatality ratios can be misleading: individual- and population-based mortality estimates and factors influencing them. Physical Biology, Volume 17, Number 6. <https://doi.org/10.1088/1478-3975/ab9e59>

46. NOAA - Climate at a glance <https://www.ncdc.noaa.gov/cag/statewide/mapping/110/tavg/202004/1/value>

47. Eric Forgoston, Michael A.S. Thorne. Strategies for Controlling the Spread of COVID-19, medRxiv 2020.06.24.20139014; <https://doi.org/10.1101/2020.06.24.20139014>

48. Jacob Barhak, The Reference Model is a Multi-Scale Ensemble Model of COVID-19. Self Published Interactive Manuscript. Publication Date: 27-May-2021  <http://doi.org/10.34235/b7eaa32b-1a6b-444f-9848-76f83f5a733c>

49. Jacob Barhak, The Reference Model for COVID-19 attempts to explain USA data. Keynote, CHRONIC DISEASES & INFECTIOUS DISEASES 24-NOV-2022, Paris, France. The talk was repeated at PyData Chicago on 15-Dec-2022. Link :  https://www.meetup.com/pydatachi/events/289899473/ Presentation: <https://jacob-barhak.github.io/COVID19_Ensemble_Latest.html>   Video: https://youtu.be/1M645o5gWrc



"""

RefDict = ExtractReferencesDict(ReferencesText)

print "located %i References: " % len(RefDict.keys())




Section0Abstract = panel.panel(FixReferences(RefDict, """## ABSTRACT:
The Reference Model for disease progression was initially a diabetes model. It used the approach of assembling models and validating them against different populations from clinical trials.

The model performs simulation at the individual level while modeling entire populations using the MIcro-Simulation Tool (MIST), employing High Performance Computing (HPC), and using machine learning techniques to combine models.

The Reference Model technology was transformed to model COVID-19 near the start of the epidemic. The model is now composed of multiple models from multiple contributors that represent different phenomena: It includes infectiousness models, transmission models, human response / behavior models, mortality models, and observation models. Some of those models were calculated at different scales including cell scale, organ scale, individual scale, and population scale.

The Reference Model has therefore reached the achievement of being the first known multi-scale ensemble model for COVID-19. This project is ongoing and this presentation is constantly updated for each venue. To access the most recent publication please use this link [https://jacob-barhak.github.io/COVID19_Ensemble_Latest.html](https://jacob-barhak.github.io/COVID19_Ensemble_Latest.html)


*** This is an interactive presentation - please explore the tabs above and interact with the figures - they have sliders and widgets and hover information that will allow interaction. Following the tabs in order from left to right will tell the story ***

Previous published versions of this presentation are archived and can be downloaded below: 

* [MODSIM WORLD, Norfolk, VA 22-23 May 2023](https://modsimworld.org/) - [repository link](https://github.com/Jacob-Barhak/Presentations/blob/25fd75da5c7bd2ea187dfad05a6b210f47172cd9/COVID19_Ensemble_Latest/COVID19_Ensemble_Latest.html) 
* [San Diego Python Users Group Monthly Meetup 27-April-2023](https://www.meetup.com/pythonsd/events/292436501/) - [repository link](https://github.com/Jacob-Barhak/Presentations/blob/fca94ff82a89860b12eb4398ec48920654ced28c/COVID19_Ensemble_Latest/COVID19_Ensemble_Latest.html) - [video](https://www.youtube.com/live/U9jSxbyJU0I?feature=share&t=1773) 
* [PyData Chicago on 15-Dec-2022](https://www.meetup.com/pydatachi/events/289899473/) - [repository link](https://github.com/Jacob-Barhak/Presentations/blob/fca94ff82a89860b12eb4398ec48920654ced28c/COVID19_Ensemble_Latest/COVID19_Ensemble_Latest.html) - [video](https://youtu.be/1M645o5gWrc)
* Keynote at [CHRONIC DISEASES & INFECTIOUS DISEASES 24-NOV-2022, Paris, France](https://www.chronicdiseases.scientexconference.com/) - [repository link](https://github.com/Jacob-Barhak/Presentations/blob/fca94ff82a89860b12eb4398ec48920654ced28c/COVID19_Ensemble_Latest/COVID19_Ensemble_Latest.html)
* [Orlando Machine Learning and Data Science Meetup - 18 June 2022](https://www.meetup.com/orlando-mlds/events/286278255/) - [repository link](https://github.com/Jacob-Barhak/Presentations/blob/9559aa6529400741e2c71fa7b2312ea04f7acfbe/COVID19_Ensemble_Latest/COVID19_Ensemble_Latest.html)

"""), width=Width, height=None)

Section0Video = panel.pane.Video(ResourceDir+os.sep+'COVID_19_Intro_libx264_crf28.mp4', width=1080, height=590, loop=True, name = 'press play to watch the introduction video')

Section0 = panel.Column(Section0Video, Section0Abstract, margin = (0,0,0,0))


Section1_0 = panel.panel(FixReferences(RefDict,"""### Introduction
The Reference Model for disease progression was was extensively published in [12],[13],[14],[15],[19] and patented [16],[17]. With the start of the COVID-19 pandemic the modeling technology was adapted to handle infectious diseases and specifically COVID-19 in [5]. This approach was extended to construct *** the first multi-scale ensemble model for COVID-19 ***!  
"""), width=Width, height=80)


Figure_1 = panel.panel(ConstractImageLinkAnchor('https://simtk.org/projects/therefmodel','TheReferenceModelCOVID19_Figure1.png','View the model web site',1100), width=Width, height=500)


Section1_1_2 = panel.panel(FixReferences(RefDict,"""

The ensemble model structure is presented above. The transition probabilities between states is controlled by multiple models:

* ***Infectiousness Models***: Indicating the level of infectiousness of each individual from time of infection. 
* ***Transmission Models***: Indicating the probability of contracting the disease considering encounters with infected individuals.
* ***Response models***: The behavior choice of each individual that affects the number of interactions in response to the pandemic. 
* ***Mortality Models***: A variety of models defining mortality of infected individuals 
    * ***Mortality rate models***: Mortality tables indicating the probability of dying from COVID-19 by age.
    * ***Mortality time***: Models attempting to estimate the time of death in days since infection
    * ***Mortality distribution***: A model that indicates the daily probability of mortality by age group since infection. 
* ***Recovery model***: defines condition of recovery as a combination of infectiousness, mortality probability, mortality time, and time since infection. 
* ***Observation Models***: defines how an observer sees the numbers - recall that numbers reported are not always accurate. The observer model corrects this.
The Reference Model combines these models and matches their results to results from The COVID Tracking project [1].

### Initialization
Populations for US states and territories were generated from data of multiple sources: 

* The Covid Tracking project [1] at the first day of simulation starting simulations at April 1st 2020.
* Age and state/territory statistics from US Census [21],[22]. 
* Number of Interaction per individual according to [42],[43].
* Temperature in US states extracted from NOAA [46].

Evolutionary computation is used to optimize the randomly generated individuals to match the target statistics.


"""), width=Width, height=None)
 

Section1 = panel.Column(Section1_0, Figure_1, Section1_1_2, margin = (0,0,0,0))


Section2_1 = panel.panel(FixReferences(RefDict,"""### Infectiousness
During the pandemic, the DHS released a master question list about the pandemic [24]. The version from 26 May 2020 has the following question: 

####"What is the average infectious period during which individuals can transmit the disease?".

Infectiousness models attempt to answer this question.  

There were 5 infectiousness curves used in the ensemble extracted from [28],[29],[30],[45]. Those models were made public in [31].

"""), width=Width, height=None)

Figure_2 = ObjectInlineHTML(ResourceDir + '/COVID19_Infectiousness_Multi.html', Width=1150, Height=390)



Section2_2 = panel.panel(FixReferences(RefDict,"""### Combined Infectiousness Model

The relative infectiousness per day since infection will be assembled by the ensemble.

If such information was available in May 2022, the DHS could have had infectiousness information at hand.
"""), width=Width, height=None)

Figure_5 = ObjectInlineHTML(ResourceDir + '/EnsembleInfectiousness.html', Width=1150, Height=320)

Section2 = panel.Column(Section2_1, Figure_2, Section2_2, Figure_5, margin = (0,0,0,0))


css = """
div.special_table + table * {
  border: 1px solid blue;
  text-align: left;
}
"""

panel.extension(raw_css=[css])


Section3 = panel.panel(FixReferences(RefDict,"""
#### Transmission models

The transmission models consider these elements:

1. ***Individual Encounter*** - What is the probability of transmission in case infected individuals are encountered. It defines the probability in percent of contracting the disease per one encounter with an infected person. 
2. ***Population Density*** - How does this probability change with population density. This is controlled by a coefficient that indicates the relative population density boost to the probability per encounter. 
3. ***Random Constant*** - What is the probability of contracting the disease due to another reason other than direct contact with a modeled infectious person. For example, contracting the virus from a person outside the modeled group, such as a person visiting out of state, falls into this category.
4. ***Temperature Effect*** - A multiplier to probability of transmission representing the effect of temperature in each state in 2020 according to NOAA compared to 49.7833333333333 degrees Fahrenheit. The daily temperature was interpolated from average monthly measurements per state, assuming the average occurred on the 15th of the month.

<div class="special_table"></div>
| Model #  | Individual Encounter | Population Density | Random Constant |Temperature Effect         |  Comments / Rational                                                                                                                                   |
|:---------|:---------------------|:-------------------|:----------------|:--------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1        | 0.6                  | 0                  | 1e-6            |                           | Low bound - Similar to previous publication with slightly lower a to represent a low bound while ignoring density and adding a small constant.         |
| 2        | 2                    | 0                  | 0               | 0.9^-(Temp-49.78)         | High Temp increases transmission - Low temperature decreases                                                                                           |
| 3        | 1.5                  | 0.1                | 0               |                           | Reasonable assumption - elevated transmission with original population density.                                                                        |
| 4        | 2.5                  | 0.2                | 0               |                           | Reasonable assumption - more elevated transmission with elevated population density.                                                                   |
| 5        | 2                    | 0                  | 0               | 0.9^(Temp-49.78)          | Low Temp increases transmission - High temperature decreases                                                                                           |

"""), width=Width, height=None)




Section4 = panel.panel(FixReferences(RefDict,"""### Response Models
Response models represent behavior of different individuals in response to the pandemic:

<div class="special_table"></div>
| Response Model | Model Description                                                                                                                                                                |
|:---------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1              | Apple mobility [34] interpolates level of interactions beyond family size. 10% infected people randomly reduce their number of interactions daily until family size is reached.  |
| 2              | Apple mobility [34] interpolates level of interactions beyond family size.  20% infected people randomly reduce their number of interactions daily until family size is reached. |
| 3              | Healthy individuals do not change behavior. Infected persons drop to interaction with family only.                                                                               |
| 4              | 0.5 compliance to state closures considering start of stay-at-home order, schools, bars & restaurants, non-essential shops. Adapted and extended from [47].                      |
| 5              | 0.9 compliance to state closures considering start of stay-at-home order, schools, bars & restaurants, non-essential shops. Adapted and extended from [47].                      |

"""), width=Width, height=None)



Section5_1 = panel.panel(FixReferences(RefDict,"""### Mortality Models
* ***Mortality rate by age***: extracted from US CDC [35] merging 2 models for low bound and high bound.
* ***Mortality Time***: 
    * Zhou et. al. [37] - Adapted form table 2 "non survivor" column - "Time from illness onset to death or discharge".
    * The COVID Tracking Project [1] - Calculated statistics from finding the first death per state since first diagnosis.
"""), width=Width, height=None)

Figure_6 = ObjectInlineHTML(ResourceDir + '/EnsembleMortality.html', Width=1150, Height=450)

Figure_3 = ObjectInlineHTML(ResourceDir + '/COVID19_Mortality_Castiglione.html', Width=1150, Height=300)

Section5_2 = panel.panel(FixReferences(RefDict,"""

* ***Mortality of an individual per age per day from infection*** by Castiglione et. al. [38] reimplemented in [40].
"""), width=Width, height=None)

Section5 = panel.Column( Section5_1, Figure_6, Section5_2, Figure_3, margin = (0,0,0,0))



Section6 = panel.panel(FixReferences(RefDict,"""### Observation Models
Observation models represent how an observer sees the true numbers reported by the model. 
The observation models attempt to imitate the distortion in observed numbers. 
In this work, simple multipliers are used:

* ***Infections Multiplier*** : observed infections = actual infections / Infections Multiplier.
* ***Mortality Multiplier*** : observed deaths = actual deaths / Mortality Multiplier.


<div class="special_table"></div>
| Observation Model | Infections Multiplier | Mortality Multiplier | Comments                                                                                                                                |
|:------------------|:----------------------|:---------------------|:----------------------------------------------------------------------------------------------------------------------------------------|
| 1                 | 1 for all states      | 1 for all states     | This observer believes that observed numbers are true.                                                                                  |
| 2                 | 5 for all states      | 1 for all states     | This observer believes infections are under reported.                                                                                   |
| 3                 | 20 for all states     | 1 for all states     | This observer believes infections are highly under reported.                                                                            |
| 4                 | 7.15 for all states   | Varies per state     | This observer believes infections are under reported and death accuracy varies per state. This model was adapted from analysis in [45]. |
| 5                 | Varies per state      | 1 for all states     | This observer attempts to correct infection numbers to match results from previous simulations.                                         |

"""), width=Width, height=None)


Section7_1 = panel.panel(FixReferences(RefDict,"""### Results
The results presented here was executed on a server with 64 logical CPUs for about 1 week - this means roughly 1 year of computation on a single CPU core. The Interactive plots below summarize the results:


* ***Population Plot - Top Left*** - This plot shows difference between model and observed data - fitness. The fitness score is displayed for each state population starting at different times. ***Each different start time is considered as a different cohort of the population***. A viewer hovering with the mouse over the circle will see information about the population cohort at that time including number of infections and deaths. The numbers are presented as model projection / observed numbers by the COVID tracking project. The numbers are scaled to cohort batch size of ***10,000 individuals*** in this simulation. The fitness score in this work is a norm of the observed mortality difference and observed infections difference.

* ***Model Mixture Plot - Top Right*** -  This plot shows the influence of each model on the ensemble. Models from the same group that compete with each other are presented in the same color and their combined influence will be 1. Initially all models in a group have the same influence so in iteration 1 - the plot shows many bars in the same height. When dragging the iteration slider to increase the iteration, it is possible to see that some models gain influence while others lose it. It is possible for a model to be fully rejected. 

* ***Convergence Plot - Bottom*** - This plot shows the weighted average fitness for the US states and territories used for each iteration. The blue vertical line shows the current iteration, while the large yellow circle shows the fitness for the unperturbed simulation that is the base of the optimization algorithm. The small circles show the results for the perturbed simulations, those help determine sensitivity and are used in optimization. The red horizontal lines represent the average fitness considering all the simulations in an iteration. This plot clearly shows some models are outliers in some iterations by seeing a spread far away from the unperturbed solution. 


## The interesting element in this simulation:

* Near elimination of the high infectiousness profile that was dominant in the past. 
* The transmission model where warm weather reduces transmission becomes dominant.
* Preference of the Castiglione mortality model based on cell and organ failure that deals with mortality time.
* No strong preference of behavioral models.
* Observer models with extreme multipliers of 1 and 20 reduce their influence to other observer models that are considered mainstream.

"""), width=Width, height=600)


Figure_4 = ObjectInlineHTML(ResourceDir + '/CombinedPlot.html', Width=1150, Height=620)


Section7 = panel.Column(Section7_1, Figure_4, margin = (0,0,0,0))








Section10_1 = panel.panel(FixReferences(RefDict,"""### Conclusions

* This model can be used to answer questions the government seeks answers for in a future pandemic.

* It is still unclear if it is possible to explain the phenomena like COVID-19 impact in a population in a period of 3 weeks using only initial conditions and mechanistic models. 

* To reach conclusions, more than a few weeks of data are required to balance for errors.

* Transmission rate seems to be around 2 percent per encounter.

* A near ideal observer model is not dominant - possibly since the phenomenon is not linear.

* Future work includes further exploration of different time periods.



"""), width=700, height=600)



Section10SummaryText = panel.panel(FixReferences(RefDict,"""

### Reproducibility:
Results presented in this work are archived in the file MIST_Ref_COVID19_Prelim_2023_04_30.zip for reproducibility purposes. MIST version 0.99.7.8 and python 2.7.18 with the Anaconda distribution were used for executing the simulation.
Visualization processing is archived in: ExplorationCOVID19_2023_04_30_10K_01Apr_15Dx3_21Dx10x48_present.zip .
This presentation is accessible [here](%s). The code that generated the presentation can be accessed [here](%s). This presentation is generated using Python 2.7.16, panel-0.8.0, holoviews 1.12.7, bokeh-1.4.0.
Published versions of this presentation are archived [here](https://github.com/Jacob-Barhak/Presentations/commits/master/COVID19_Ensemble_Latest)

### Conflict of Interest Statement:
Payment/services info: Dr. Barhak reports non-financial support and other from Rescale, and MIDAS Network, other from Amazon AWS, Microsoft Azure, MIDAS network, other from The COVID tracking project at the Atlantic,  other from John Rice and Jered Hodges, 
Financial relationships: Jacob Barhak declare(s) employment from MacroFab, United Solutions, B. Well Connected health. The author had a contract with U.S. Bank / Apexon, MacroFab, United Solutions, and B. Well during the work. However, none of these companies had influence on the modeling work reported in the paper. Jacob Barhak declare(s) employment and technical support from Anaconda. The author contracted with Anaconda in the past and uses their free open source software tools. Also the author received free support from Anaconda Holoviz team and Dask teams. Intellectual property info: Dr. Barhak has a patent US Patent 9,858,390 - Reference model for disease progression issued to Jacob Barhak, and a patent US patent Utility application #15466535 - Analysis and Verification of Models Derived from Clinical Trials Data Extracted from a Database. Other relationships: During the conduct of the study; personal fees from United Solutions, personal fees from B. Well Connected health, personal fees and non-financial support from Anaconda, outside the submitted work; In addition, Dr. Barhak has a patent US Patent 9,858,390 - Reference model for disease progression issued to Jacob Barhak, and a US patent Number 10,923,234 - Analysis and Verification of Models Derived from Clinical Trials Data Extracted from a Database and The author was engaged with a temporary team formed for a duration of the Pandemic Response Hackathon. The team consisted of Christine Mary, Doreen Darsh, Lisbeth Garassino . They supported work during the Hackathon in initial stages of this work. Many others have expressed their support in this project. This has been publicly reported here: https://devpost.com/software/improved-disease-modeling-tools-for-populations . However, despite all support, Dr. Barhak is solely responsible for modeling decisions made for this publication and is responsible for its contents.

"""%(PublishURL,CodePublishURL)), width=Width, height=None)

Section10 = panel.Column( panel.Row(Section10_1,PresentationURL, margin = (0,0,0,0)), Section10SummaryText, margin = (0,0,0,0))

Section11_1  = panel.panel(FixReferences(RefDict,"""
### Acknowledgments: 
The following researchers provided models. Here is some information on their work:

* [Lucas Boettcher](http://lucas-boettcher.info/) - provided an infectiousness model and an observation model
    - [A statistical model of COVID-19 testing in populations: effects of sampling bias and testing errors](https://doi.org/10.1098/rsta.2021.0121)
    - [Using excess deaths and testing statistics to determine COVID-19 mortalities](https://doi.org/10.1007/s10654-021-00748-2)
    - [On the accuracy of short-term COVID-19 fatality forecasts](https://doi.org/10.1186/s12879-022-07205-9)

* [Robin Thompson](https://robin-thompson.co.uk/) and William Hart - provided an infectiousness model
    - [Generation time of the alpha and delta SARS-CoV-2 variants: an epidemiological analysis](https://doi.org/10.1016/S1473-3099(22)00001-9)
    - [High infectiousness immediately before COVID-19 symptom onset highlights the importance of continued contact tracing](https://doi.org/10.7554/eLife.65534)
    - [Inference of the SARS-CoV-2 generation time using UK household data](https://doi.org/10.7554/eLife.70767)

* [Filippo Castiglione](https://wwwold.iac.cnr.it/~filippo/about-me.html) - provided a mortality model
    - [Emulating complex simulations by machine learning methods](https://doi.org/10.1186/s12859-021-04354-7)
    - [From infection to immunity: understanding the response to SARS-CoV2 through in-silico modeling](https://doi.org/10.3389/fimmu.2021.646972)
    - [Mechanistic Modeling and Multiscale Applications for Precision Medicine](https://doi.org/10.1089/nsm.2020.0002)
    
* [Eric Forgoston](https://eric-forgoston.github.io) - provided data for response models
    - [Knowledge-based learning of nonlinear dynamics and chaos](https://doi.org/10.1063/5.0065617)
    - [Characterizing outbreak vulnerability in a stochastic SIS model with an external disease reservoir](https://doi.org/10.1098/rsif.2022.0253)
    - [Learning Ocean Circulation Models with Reservoir Computing](https://doi.org/10.1063/5.0119061)

Additional thanks to these modelers who provided data for models:

* Alan Perelson - provided infectiousness models.
* Sen Pei - allowed deriving infectiousness model from their computations.

Additional Thanks to:

* Thanks to the COVID tracking project for providing a special license for using the data.
* Thanks to all other sources of data that make it available easily online, including Apple for mobility data, US Census, Los Alamos National Lab. 
* Thanks to Harel Dahari who made the connection to the MIDAS network and IMAG wiki for providing information to connect to Rescale.
* Thanks to Aaron Garrett who helped develop some evolutionary computation algorithms that were incorporated in MIST. 
* Thanks to Deanna J.M. Isaman who introduced me to disease modeling.

"""), width=int(Width * 0.7), height=None)

Section11_2  = panel.panel(FixReferences(RefDict,"""
The above logos acknowledge help provided by these organizations. The logos do not imply any other connection other than a large thank you.

Special Thanks to Anaconda and HoloViz and especially these team members of the HoloViz Team:

* Philipp Rudiger
* James Bednar
* Jean-Luc Stevens 

Thanks to these organizations for providing cloud computing power:

* Rescale 
* Microsoft Azure
* Amazon AWS
* MIDAS Coordination Center, supported by NIGMS grant 5U24GM132013 and the NIH STRIDES program

Thanks to SciPod for good video production services.

Thanks to those who hosted me / my compute server:

* John Rice
* Jered Hodges
* United Solutions
* Jeff Pape
* Boris and Halina Barhak (my parents)
* Ronen Ozer

Additional thanks for those helping locate and interpret Temperature data:

* David Trossman
* Bruce Shapiro
* Scott Stephens (NOAA)

"""), width=int(Width * 0.3), height=None)

AnacondaLogoURL = panel.panel(ConstractImageLinkAnchor('https://www.anaconda.com/','AnacondaLogo.png','Anaconda web site',100), width=100, height=50)
SciPodLogoURL = panel.panel(ConstractImageLinkAnchor('https://www.scipod.global/','SciPod.png','SciPod web site',50), width=50, height=50)
MidasLogoURL = panel.panel(ConstractImageLinkAnchor('https://midasnetwork.us/','MIDAS_Logo.png','MIDAS Network web site',100), width=100, height=50)

HoloVizLogoURL = panel.panel(ConstractImageLinkAnchor('https://holoviz.org/','HolovizLogo.png','Holoviz web site',125), width=125, height=50)
UnitedSolutionsLogoURL = panel.panel(ConstractImageLinkAnchor('https://www.unitedsolutions.io/','UnitedSolutions.png','United Solutions web site',125), width=125, height=50)

Logos = panel.Column(panel.Row( AnacondaLogoURL, SciPodLogoURL, MidasLogoURL), panel.Row(UnitedSolutionsLogoURL, HoloVizLogoURL), margin = (0,0,0,0))

Section11 = panel.Row( Section11_1, panel.Column(Logos, Section11_2, ), margin = (0,0,0,0))


SectionSelectorTab = panel.layout.Tabs (
                                        ('Abstract',Section0),
                                        ('Introduction', Section1),
                                        ('Infectiousness', Section2),
                                        ('Transmission', Section3),
                                        ('Response Models', Section4),
                                        ('Mortality Models', Section5),
                                        ('Observation Models', Section6),
                                        ('Results', Section7),
                                        ('Conclusions', Section10),
                                        ('Acknowledgments', Section11),
                                        margin = (0,0,0,0), 
                                        )

                                       
Presentation = panel.Column(PresentationHeader, SectionSelectorTab)
Presentation.save(SavedFileName, resources=INLINE, title=TitleHTML)       

