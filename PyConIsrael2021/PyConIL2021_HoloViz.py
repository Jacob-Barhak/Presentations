"""PyCon Israel 2021 HoloViz Tutorial"""
###############################################################################
# This work is available under 
#
# To the extent possible under law, Jacob Barhak has waived all copyright and 
# related or neighboring rights to PyCon Israel 2021 HoloViz Tutorial 
# This work is published from: United States.
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
# Jacob Barhak wrote the presentation that reuses web sites from https://holoviz.org/
# 
# Special thanks to:
# Philipp Rudiger, James Bednar, and Jean-Luc Stevens for assisting with 
# Panel, bokeh, and HoloViews issues.
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
import matplotlib.pyplot as plt
import pandas
import math
from bokeh.resources import INLINE
from matplotlib.cm import  PuBu, PuRd, Greens


default_width = 1100

image_dir = 'Images'
data_dir = 'Data'

def convert_file_to_data(file_name):
    "Convert file to data that can be used in html"
    data_file = open(file_name,'rb')
    data = data_file.read()
    data_file.close()
    return base64.b64encode(data).decode()

def constract_image_link_anchor(link, image_file_name, text, width):
    "Constructs html to describe the png image and link it"
    encoded_image = convert_file_to_data (image_dir+os.sep+image_file_name)
    template = ('<a title="%s" target="_blank" href="%s">'
                '<img src="data:image/png;base64,%s" alt="%s" width="%i"/> </a>')
    return template % (text, link, encoded_image, text,width)

def object_inline_HTML(Extrnalfile_name, width=default_width, height=700):
    "Encodes html from a file into object"
    ret_str = '<object width="'+str(width)+'" height="'+str(height)+'" data="%s">Warning:%s Not Accessible!</object>'%(Extrnalfile_name,Extrnalfile_name)
    return ret_str





title_html = 'Using Python HoloViz Technologies to Create Interactive Presentations by Jacob Barhak & James Bednar'
saved_file_name = 'Presentation_PyConIL2021_HoloViz.html'
publish_url = 'https://jacob-barhak.github.io/'+saved_file_name
code_publish_url = 'https://github.com/Jacob-Barhak/Presentations/tree/master/PyConIsrael2021'
qr_file_name = 'PyConIL_2021.png'


presentation_url = panel.panel(constract_image_link_anchor(publish_url,qr_file_name,'View this presentation on the web',400), width=400, height=400)

presentation_title = panel.panel('# Using Python HoloViz Technologies to Create Interactive Presentations', width=900, height=50, margin = (0,0,0,0))
presentation_venue_text = panel.panel('PyCon Israel 2021 May 2-3', width=200, height=20, margin = (0,0,0,0))
presentation_venue_figure = panel.panel(constract_image_link_anchor('https://pycon.org.il/2021/','PyConIL2021_logo.png','PyCon Israel 2020',170), width=200, height=20, margin = (0,0,0,0))
presentation_authors = panel.panel("[Jacob Barhak](http://sites.google.com/site/jacobbarhak/) & [James Bednar](https://www.linkedin.com/in/james-bednar-7602911b/)", width=200, height=20, margin = (0,0,0,0))
presentation_venue = panel.Column(presentation_authors, presentation_venue_text, presentation_venue_figure, margin = (0,0,0,0) )

presentation_header = panel.Row ( presentation_title,  presentation_venue, margin = (0,0,0,0))






section1_left = panel.panel("""# Introduction
HoloViz is a set of Python visualization libraries.

Those libraries can be combined together to create 
presentations and interactive posters like the one seen on the right.

This interactive presentation will first give an overview of 
HoloViz and HoloViews by following links to online content.

It then shows basic operations in Panel to create an interactive presentation.

Please follow the tab / links in reading order. 

## HoloViz Overview:

### Topic 1. Introduction to HoloViz Technologies and Libraries 
[Click here](https://holoviz.org/) to follow the overview

### Topic 2. Getting started with Holoviews

[Click here](https://holoviews.org/) to reach holoviews.org

[Click here](https://holoviews.org/getting_started/Introduction.html) for getting started

[Click here](https://holoviews.org/user_guide/Dashboards.html) for dashboards

""", width=700, height=500)


section1_right = panel.panel(   constract_image_link_anchor(
                                'https://jacob-barhak.github.io/Poster_MSM_ML_IMAG_2019.html',
                                'PosterNIH_Edit.jpg','Jacob showing poster at the NIH', 400))

section1 = panel.Row(section1_left, section1_right)




section3_title = panel.panel("""# Using Panel for Creating Interactive Presentations
""", width=700, height=50)

section3_1_top = panel.panel("""# Panel using Markdown
Panel supports [Markdown](https://en.wikipedia.org/wiki/Markdown) text. Here is an example with code on the left and result on the right.
""", width=1000, height=70)

section3_1_left = panel.panel("""
````python
panel.panel(\"\"\"
# This is a title

## Heading

### Sub Heading

*Italics*

**Bold**

`code1`

[This is a link to HoloViz](https://holoviz.org/)

plain text
\"\"\")
````

""", width=500, height=500)



section3_1_right = panel.panel("""
# This is a title
## Heading
### Sub Heading

*Italics*

**Bold**

`code1`

[This is a link to HoloViz](https://holoviz.org/)

plain text

""", width=500, height=500)

section3_1 = panel.Column(section3_1_top, panel.Row(section3_1_left, section3_1_right) )




section3_2_top = panel.panel("""# Panel can show matplotlib and bokeh plots
""", width=1000, height=30)

data = {}
data['Year'] =    [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, ]
data['Cohorts'] = [  22,   34,   40,   47,   47,   91,   91,  123,  123, ]

holoviews.extension('matplotlib')
plot1 = holoviews.Scatter(data, kdims=['Year'], vdims=['Cohorts'])

section3_2_1_left = panel.panel("""
````python
data = {}
data['Year'] =    [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, ]
data['Cohorts'] = [  22,   34,   40,   47,   47,   91,   91,  123,  123, ]
plot1 = holoviews.Scatter(data, kdims=['Year'], vdims=['Cohorts'])
panel.pane.HoloViews(plot1, width=400, height=170, backend='matplotlib')
````
""", width=600, height=170)


holoviews.extension('bokeh')
plot2raw = holoviews.Bars(data, kdims=['Year'], vdims=['Cohorts'])
plot2 = plot2raw.opts (toolbar=None, default_tools=[], tools=['hover'], xrotation=90)

section3_2_2_left = panel.panel("""
````python
holoviews.extension('bokeh')
plot2raw = holoviews.Bars(data, kdims=['Year'], vdims=['Cohorts'])
plot2 = plot2raw.opts (toolbar=None, default_tools=[], tools=['hover'], xrotation=90)
panel.panel(plot2, width=400, height=170)
````
""", width=600, height=170)

section3_2_left = panel.Column(section3_2_1_left, section3_2_2_left)

section3_2_1_right = panel.pane.HoloViews(plot1, width=400, height=170, backend='matplotlib')

section3_2_2_right = panel.panel(plot2, width=400, height=170)

section3_2_right = panel.Column(section3_2_1_right, section3_2_2_right)


section3_2 = panel.Column(section3_2_top, panel.Row(section3_2_left, section3_2_right) )









section3_3_top = panel.panel("""# Panel using LaTeX
Panel supports [LaTeX](https://en.wikipedia.org/wiki/Latex). It supports two back-ends [katex](https://katex.org/) by default and [mathjax](https://www.mathjax.org/).
""", width=1000, height=70)



section3_3_left_1 = panel.panel("""
````python
panel.pane.LaTeX("Method 1 to embed $LaTeX$")
````
""", width=600, height=50)

section3_3_left_2 = panel.panel("""
````python
panel.pane.LaTeX("Method 2 to embed \(LaTeX\)")
````
""", width=600, height=50)


section3_3_left_3 = panel.panel("""
````python
panel.pane.LaTeX("Einstein said $E = MC^2$")
````
""", width=600, height=50)


section3_3_left_4 = panel.panel("""
````python
panel.pane.LaTeX("More complex  $\\frac{\\sum_{i}{a_i*b_i}}{\\sum_{i}{a_i}}$")
````
""", width=600, height=50)

section3_3_left_5 = panel.panel("""
````python
panel.pane.LaTeX("Bigger $\\frac{\\sum_{i}{a_i*b_i}}{\\sum_{i}{a_i}}$", 
                 style = {'font-size':'16pt'})
````
""", width=600, height=50)


section3_3_left = panel.Column(
    section3_3_left_1,
    section3_3_left_2,
    section3_3_left_3,
    section3_3_left_4,
    section3_3_left_5,
)


section3_3_right_1 = panel.pane.LaTeX("Method 1 to embed $LaTeX$", width=500, height=50)

section3_3_right_2 = panel.pane.LaTeX("Method 2 to embed \(LaTeX\)", width=500, height=50)


section3_3_right_3 = panel.pane.LaTeX("Einstein said $E = MC^2$", width=500, height=50)


section3_3_right_4 = panel.pane.LaTeX("More complex  $\\frac{\\sum_{i}{a_i*b_i}}{\\sum_{i}{a_i}}$", width=500, height=50)

section3_3_right_5 = panel.pane.LaTeX("Bigger $\\frac{\\sum_{i}{a_i*b_i}}{\\sum_{i}{a_i}}$", style = {'font-size':'16pt'}, width=500, height=50)


section3_3_right = panel.Column(
    section3_3_right_1,
    section3_3_right_2,
    section3_3_right_3,
    section3_3_right_4,
    section3_3_right_5,
)


section3_3 = panel.Column(section3_3_top, panel.Row(section3_3_left, section3_3_right) )





section3_4_top = panel.panel("""# Using HTML with Panel
""", width=800, height=30)


section3_4_left_1 = panel.panel("""
````python
panel.panel('Using <span style="color:red">color</span> in text')

````
""", width=800, height=20)

section3_4_left_2 = panel.panel("""
````python
panel.panel('Add a <a title="hover tool" target="_blank"' 
            'href="https://holoviz.org/">link</a> with hover tool')

````
""", width=800, height=40)


section3_4_left_3 = panel.panel("""
````python
def convert_file_to_data(file_name):
    "Convert file to data that can be used in html"
    data_file = open(file_name,'rb')
    data = data_file.read()
    data_file.close()
    return base64.b64encode(data).decode()

def constract_image_link_anchor(link, image_file_name, text, width):
    "Constructs html to describe the png image and link it"
    encoded_image = convert_file_to_data (image_dir+os.sep+image_file_name)
    template = ('<a title="%s" target="_blank" href="%s">'
                '<img src="data:image/png;base64,%s" alt="%s" width="%i"/> </a>')
    return template % (text, link, encoded_image, text,width)

panel.panel('Show an image using HTML</br>' + constract_image_link_anchor('https://holoviz.org/',
                                 'PosterNIH_Edit.jpg','Jacob showing poster at the NIH', 220)
````
""", width=800, height=300)



section3_4_left = panel.Column(
    section3_4_left_1,
    section3_4_left_2,
    section3_4_left_3,

)



section3_4_right_1 = panel.panel("""
Using <span style="color:red">color</span> in text
""", width=300, height=20)

section3_4_right_2 = panel.panel('Add a <a title="hover tool" target="_blank"' 
                                 'href="https://holoviz.org/">link</a> with hover tool', 
                                 width=300, height=40)


section3_4_right_3 = panel.panel('Show an image using HTML</br>' + constract_image_link_anchor('https://holoviz.org/',
                                 'PosterNIH_Edit.jpg','Jacob showing poster at the NIH', 220)
            , width=300, height=300)




section3_4_right = panel.Column(
    section3_4_right_1,
    section3_4_right_2,
    section3_4_right_3,

)


section3_4 = panel.Column(section3_4_top, panel.Row(section3_4_left, section3_4_right) )






section3_5_top = panel.panel("""# Showing tables with Panel
Tables can be defined using [Markdown extended syntax](https://www.markdownguide.org/extended-syntax/) or [Panel dataframe](https://panel.holoviz.org/reference/panes/DataFrame.html#panes-gallery-dataframe)
""", width=1000, height=80)


section3_5_left_1 = panel.panel("""
````python
TableCSS = "div.special_table + table * {border: 1px solid blue;}"
panel.extension(raw_css=[TableCSS])
panel.panel(\"\"\"<div class="special_table"></div>

| Num | First Name   | Last Name |
|-----|--------------|-----------|
| 1.  | James        | Bednar    |
| 2.  | Jacob        | Barhak    |
\"\"\")
````
""", width=600, height=200)

section3_5_left_2 = panel.panel("""
````python
dataframe=pandas.DataFrame({'Num': [1,2],
'First Name': ['James','Jacob'],
'Last Name': ['Bednar','Barhak'],})

panel.pane.DataFrame(dataframe, index = False)
````
""", width=600, height=150)



section3_5_left = panel.Column(
    section3_5_left_1,
    section3_5_left_2,

)


TableCSS = "div.special_table + table * {border: 1px solid blue;}"

panel.extension(raw_css=[TableCSS])

section3_5_right_1 = panel.panel("""<div class="special_table"></div>

| Num | First Name   | Last Name |
|-----|--------------|-----------|
| 1.  | James        | Bednar    |
| 2.  | Jacob        | Barhak    |
""", width=300, height=200)

dataframe=pandas.DataFrame({'Num': [1,2],
'First Name': ['James','Jacob'],
'Last Name': ['Bednar','Barhak'],})
section3_5_right_2 = panel.pane.DataFrame(dataframe, index = False, width=300, height=150)



section3_5_right = panel.Column(
    section3_5_right_1,
    section3_5_right_2,

)


section3_5 = panel.Column(section3_5_top, panel.Row(section3_5_left, section3_5_right) )








section3_6_top = panel.panel("""# Arranging panels
Elements can be arranged in many layouts including [Row](https://panel.holoviz.org/reference/layouts/Row.html), [Column](https://panel.holoviz.org/reference/layouts/Column.html), [Tabs](https://panel.holoviz.org/reference/layouts/Tabs.html)
""", width=700, height=70)

section3_6_left = panel.panel("""
````python
text1 = panel.panel('scatter', width=50, height=50)
text2 = panel.panel('bars', width=50, height=50)
fig1 = panel.panel(plot1, width=250, height=180)
fig2 = panel.panel(plot2, width=250, height=180)
fig_row = panel.Row(fig1,fig2)
fig_column = panel.Column(fig1,fig2)
mix1 = panel.Row(panel.Column(text1,fig1),
                 panel.Column(text2,fig2))
mix2 = panel.Column(panel.Row(text1,fig1),
                    panel.Row(text2,fig2))
tabs = panel.layout.Tabs (  ('Fig Row',fig_row),
                            ('Fig Column',fig_column),
                            ('Mix 1',mix1),
                            ('Mix 2',mix2),
                          ) 
````
""", width=500, height=500)


text1 = panel.panel('scatter', width=50, height=50)
text2 = panel.panel('bars', width=50, height=50)
fig1 = panel.panel(plot1, width=250, height=180)
fig2 = panel.panel(plot2, width=250, height=180)
fig_row = panel.Row(fig1,fig2)
fig_column = panel.Column(fig1,fig2)
mix1 = panel.Row(panel.Column(text1,fig1),
                 panel.Column(text2,fig2))
mix2 = panel.Column(panel.Row(text1,fig1),
                    panel.Row(text2,fig2))
tabs = panel.layout.Tabs (  ('Fig Row',fig_row),
                            ('Fig Column',fig_column),
                            ('Mix 1',mix1),
                            ('Mix 2',mix2),
                          ) 

section3_6_right = panel.panel(tabs, width=600, height=500)


section3_6 = panel.Column(section3_6_top, panel.Row(section3_6_left, section3_6_right) )

section3_7 = panel.panel("""# Save presentation as static HTML
Most Panel objects can be saved to a file. 
For example we will save the tabs object created in the "Arranging Panels" tab

````python
tabs.save(filename='tabs_small.html' )
````

This will create an interactive html file for you. 

However, this file will not work if you are not connected to the Internet
since it downloads javascript code from another server to conserve size. 

To create a fully reproducible self contained interactive file, use:

````python
from bokeh.resources import INLINE
tabs.save(filename='tabs_full.html',
          resources=INLINE,
          embed=True,
          title='fully reproducible')
````

Note that if `embed=False` it may result in non interactive file 
where sliders can slide, yet there is no effect on screen. 


For additional tips on saving files, visit this [tips page](https://discourse.holoviz.org/t/tips-for-saving-interactive-plots-as-html/175/3)

""", width=1000, height=500)

tabs.save(filename='tabs_small.html' )

tabs.save(filename='tabs_full.html',
          resources=INLINE,
          embed=True,
          title='fully reproducible')



section3_tabs = panel.layout.Tabs (
                                        ('Markdown',section3_1),
                                        ('Plots',section3_2),
                                        ('LaTeX',section3_3),
                                        ('HTML',section3_4),
                                        ('Tables',section3_5),
                                        ('Arranging Panels',section3_6),
                                        ('Save',section3_7),
                                        margin = (0,0,0,0), 
                                  )




section3 = panel.Column(section3_title,section3_tabs) 




section4_summary_text = panel.panel("""# Summary
HoloViz technologies allow non web developers develop interactive web pages using python.
This can be used to create presentations and interactive posters like these:

* J. Barhak, J. Schertz, Clinical Unit Mapping for Standardization of ClinicalTrials.Gov . MSM/IMAG meeting. IMAG MSM Meeting March 6-7, 2019 @ NIH, Bethesda, MD. [Poster](https://jacob-barhak.github.io/InteractivePoster_MSM_IMAG_2019.html)
* J. Barhak, Clinical Data Modeling with Python, AnacondaCon , Austin, Texas,  April 3-5, 2019. [Video](https://youtu.be/fQIYMf5wKGE) , [Presentation](https://jacob-barhak.github.io/AnacondaCon_2019.html) 
* J. Barhak, J. Schertz, Standardizing Clinical Data with Python . PyCon Israel 3-5 June 2019, [Video](https://youtu.be/vDXyCb60L5s)  [Presentation](https://jacob-barhak.github.io/Presentation_PyConIsrael2019.html) 
* J. Barhak, J. Schertz, Clinical Unit Mapping with Multiple Standards . 2019 CDISC U.S. Interchange, [Poster](https://jacob-barhak.github.io/Poster_CDISC2019.html) 
* J. Barhak, J. Schertz, Supervised Learning of Units of Measure. IMAG ML-MSM/IMAG meeting. Oct 24-25, 2019 @ NIH, Bethesda, MD . [Poster](https://jacob-barhak.github.io/Poster_MSM_ML_IMAG_2019.html)
* J. Barhak, J. Schertz, Visualizing Machine Learning of Units of Measure using PyViz . PyData Austin 2019 , 6-7 December 2019, Galvanize Austin. [Presentation](https://jacob-barhak.github.io/Presentation_PyData_Austin_2019.html) , [Video](https://youtu.be/KS-sRpUvnD0)
* J. Barhak, The Reference Model Accumulates Knowledge With Human Interpretation. IMAG wiki - MODELS, TOOLS & DATABASES Uploaded 16 March 2020.  [Poster](https://jacob-barhak.github.io/Poster_MSM_IMAG_2020.html)

Additional support at [Gitter Pyviz Channel](https://gitter.im/pyviz/pyviz) and [Discourse HoloViz Channel](https://discourse.holoviz.org/)

## Acknowledgments: 
* Many thanks to the HoloViz team and particularly to Philipp Rudiger and Jean-Luc Stevens.
""", width=700, height=300)


section4_summary = panel.Row(section4_summary_text,presentation_url, margin = (0,0,0,0))

section4_additional_info = panel.panel("""
## Reproducibility:
This presentation is accessible [here](%s). The code that generated the presentation is available [here](%s). This presentation is generated with Python 3.7.9, Panel-0.9.5, HoloViews 1.13.4, bokeh-2.0.2 .
"""%(publish_url,code_publish_url), width=default_width, height=800)


section4 =  panel.Column(section4_summary, section4_additional_info, margin = (0,0,0,0))




section_selector_tab = panel.layout.Tabs (
                                        ('Introduction to HoloViz',section1),
                                        ('Panel for Presentations', section3),                                       
                                        ('Summary', section4),
                                        margin = (0,0,0,0), 
                                        )
                                        
presentation = panel.Column(presentation_header, section_selector_tab)
presentation.save(saved_file_name, resources=INLINE, title=title_html, embed=True)       

