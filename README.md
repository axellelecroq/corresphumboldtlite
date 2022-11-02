# Corresp<ins>humboldt</ins>lite

This repository allows to use the jupyter notebook made in [corresp-humboldt-dataviz](https://github.com/edition-humboldt-collection/corresp-humboldt-dataviz) in a browser. The user no longer needs to clone the whole repo and launch the jupyter notebook in his terminal in order to use it. This repository offers better accessibility than the corresp-humboldt-dataviz.

Access to jupyter notebooks and map visualisations: [corresphumboldtlite](https://axellelecroq.github.io/corresphumboldtlite/lab/index.html)

In order for the map visualisations to be presented in the jupyter lab, the code had to be adapted. Furthermore, these are not entirely the same functions as the one in [corresp-humboldt-dataviz](https://github.com/edition-humboldt-collection/corresp-humboldt-dataviz). Also, within this repository only the jupyter notebook presenting the data visualisations is available, not the dynamic search within the data ([search.ipynb](https://github.com/edition-humboldt-collection/corresp-humboldt-dataviz/blob/main/notebooks/search.ipynb) in [corresp-humboldt-dataviz](https://github.com/edition-humboldt-collection/corresp-humboldt-dataviz)). 

## About this project

This experimental project seeks to discover, explore and visualize the correspondence of Alexander von Humboldt. The idea started with the catalog of Alexander von Humboldt's letters held at the  [Berlin-Brandenburg Academy of Sciences (BBAW)](https://www.bbaw.de/). Up to now, the collection is only accessible via an index card system established in the 1950s. Only the research aid has been digitally reproduced.

The original idea was to make at least a part of the collection digitally accessible and to discover it with the help of new research tools. With this goal in mind, the catalog was to be correlated with modern manuscript databases.

## Data
The used dataset come from 3 different sources:
1. **The Kalliope Verbund**: data of the letters sent and received by Alexander von Humboldt (AvH) have been retrieved from the Kalliope's API in Dublin Core format.
2. **Bibliothèque nationale de France** (BnF): data were  retrieved in csv format on the user-friendly API
3. **American Philosophical Society** : data were retrieved in EAD format.

The three dataset were cleaned and homogenised in order to be able to query them. To visualise the letters on a map, geopoint, geoname ID and [humboldt digital edition](https://edition-humboldt.de/?&l=en) identifier (edh id) were also added. 

In the digital collection there are **3465** letters written by Alexander von Humboldt and **1467** letters sended to him. 

## Used tools
Several libraries were used for data visualisations, among them the main ones are: [ipywidgets](https://ipywidgets.readthedocs.io/en/latest/), [ipyleaflet](https://ipyleaflet.readthedocs.io/en/latest/), [matplotlib](https://matplotlib.org/), [pandas](https://pandas.pydata.org/), [numpy](https://numpy.org/).

# Credits
[corresp-humboldt-dataviz](https://github.com/edition-humboldt-collection/corresp-humboldt-dataviz) is developed by Axelle Lecroq, intern in the BBAW's project ["Travelling Humboldt - Science on the Move"](https://edition-humboldt.de/?&l=en). Corresphumboldtlite enhances [corresp-humboldt-dataviz](https://github.com/edition-humboldt-collection/corresp-humboldt-dataviz) in order to give an easier access to the jupyter notebook and to use them in browser. 