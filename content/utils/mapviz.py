import pandas as pd
import json
import numpy
import random
import IPython
from IPython.display import display, clear_output, Javascript
from ipywidgets import HTML, Output, HBox, Layout
from ipyleaflet import Map, Marker, Popup, CircleMarker
import matplotlib.pyplot as plt
import ipywidgets as widgets
import gender_guesser.detector
from collections import Counter

from .nestedlookup import *
from .search_dynamic import show_webpage,btn_new_search
from .prepare_data import getJSON, avoidTupleInList, getYears, getHumboldtYears
from .widgets import createDropdown, createButton, createCheckBox

data = getJSON('data/records.json')
out = Output()

def writeJSON(file, data):
    """
    Store JSON data in a JSON file 
    :param file: str
    :param data: dict
    """
    with open(file, mode='w') as f:
        json.dump(data, f)

def download_data(data):
    """
    Download searched data
    :return: btn
    :rtype: button
    """
    # Create the button
    btn = createButton('Download data', 'info')
    output = widgets.Output()

    def new_search(b):
        writeJSON('./downloaded/results.json', data)
    
    # When the button is clicked, then the output of the jupyter
    # cell will be clean.
    btn.on_click(new_search)
    return btn

def allonmap(data, by: str):
    cities = {}
    marker = None
    coordinates = []
    m= Map(
            zoom=1.5,
            layout=Layout(width='80%', height='500px'),
            close_popup_on_click=False
            )
    
    for i in data:
            try:
                if i["date"]:
                        date = i["date"]
            except : date = "Unknown date."
            try :
                if i[by]["address"] not in cities:
                    city = i[by]["address"]
                    cities[city] = {}
                    cities[city]["message"] = "<b>"+ date + " </b> " + i["title"] + "<br><i>"+ i["contributor"] +"</i> <br> <a href=\""+ i["identifier"][1] + "\" target=\"_blank\">online</a> <hr>"
                    cities[city]["coordinates"] = [i[by]["coordinates"][1], i[by]["coordinates"][0]]
                    
                elif i[by]["address"] in cities:
                    city = i[by]["address"]
                    cities[city]["message"] = cities[city]["message"] + "<b>"+ date + " </b> " + i["title"] + "<br><i>"+ i["contributor"] +"</i> <br> <a href=\""+ i["identifier"][1] + "\" target=\"_blank\">online</a> <hr>"
            except : pass
            
    # Coordinates to create a dynamic map boundaries
    try:
        for i in cities.keys():
            if type(cities[i]["coordinates"][0]) == float and type(cities[i]["coordinates"][1]) == float:
                coordinates.append([float(cities[i]["coordinates"][0]), float(cities[i]["coordinates"][1])])
            elif type(cities[i]["coordinates"][0]) == str and type(cities[i]["coordinates"][1]) == str:
                coordinates.append([float(cities[i]["coordinates"][0]), float(cities[i]["coordinates"][1])])
    
        coordinates = numpy.array(coordinates)
        data_frame = pd.DataFrame(coordinates, columns=['Lat', 'Long'])
        sw = data_frame[['Lat', 'Long']].min().values.tolist()
        ne = data_frame[['Lat', 'Long']].max().values.tolist()
        m.fit_bounds([sw, ne])
    except: pass


    # Mapmarker and popup message
    for i in cities.keys():
            try :
                # Create the message of the popup
                message = HTML()
                if cities[i]["message"].count("<hr>") <3 :
                    message.value = cities[i]["message"]
                else : 
                    message.value = str(cities[i]["message"].count("<hr>")) + " letters. There are too many results to show them all here."
                message.description = i.upper()

                # Create the marker
                marker = CircleMarker(location=(cities[i]["coordinates"][0], cities[i]["coordinates"][1]))
                radius = cities[i]["message"].count("<hr>")+3
                if radius > 10:
                    radius = 12
                marker.radius = radius
                marker.fill_opacity = 0.8
                marker.fill_color = '#3E81B8'
                marker.stroke = False

                # Add marker on the map
                m.add_layer(marker)
                marker.popup = message
            except: pass
    return display(download_data(data), m)
    

def map_by_date():
    
    def on_value_change(change):
        output_bydate.clear_output(wait=True)
        display(Javascript('IPython.notebook.execute_cell()'))
        results = []
        with output_bydate:
            for i in data:

                try:
                    if i["date"]:
                        if change['new'] in i["date"]:
                            results.append(i)
                except: pass
            allonmap(results, 'coverage_location')

    dropdown = createDropdown('', getHumboldtYears(getYears(avoidTupleInList(nested_lookup('date', data)))))
    output_bydate = widgets.Output()
    display(dropdown, output_bydate)
    dropdown.observe(on_value_change, names='value')
    

def byperson():
    # Get the letters which have a recorded date
    with_date= []
    for i in data:
        try:
            if bool(i['date']) == True:
                with_date.append(i)
        except:pass
        
    # Get all people who received or sent a letter    
    creators = avoidTupleInList(nested_lookup('creator', with_date))
    subjects = avoidTupleInList(nested_lookup('subject', with_date))
    people = []
    
    # Delete Humboldt from creators' and subjects' lists
    for i in creators:
        if '[' in i :
            i = i.split(' [vermutlich]')[0]
        if 'Humboldt' not in i:
            people.append(i)
    for i in subjects:
        if 'Humboldt' not in i and i not in people:
            people.append(i)

    #Create dropdown Menu
    dropdown = createDropdown('', people)
    return dropdown 


def map_by_person():
    
    def on_value_change(change):
        output_bydate.clear_output(wait=True)
        display(Javascript('IPython.notebook.execute_cell()'))
        results = []
        with output_bydate:
            person = change['new']
            for i in data:
                try : 
                    if person in i["creator"] or person in i["subject"]:
                        results.append(i)
                except: pass
            allonmap(results, 'coverage_location')

    dropdown = byperson()
    output_bydate = widgets.Output()
    display(dropdown, output_bydate)
    dropdown.observe(on_value_change, names='value')


def createhistogramm(data, person):
    """
    Create a histogramm of the exchange of letters
    between AvH and a selected person during the time.
    :param data: List of letters
    :param person: Selected person 
    """
    title = 'Correspondence between AvH(1769-1859) und ' + person
    x_coords = [coord[0] for coord in data]
    fig= plt.figure(figsize=(7,2))
    plt.hist(x_coords, bins=30)
    fig.suptitle(title, fontsize=9)
    plt.xlabel('Year', fontsize=9)
    plt.ylabel('Number of letters', fontsize=12)
    
    return plt.show()
    

def byperson():
    # Get the letters which have a recorded date
    with_date= []
    for i in data:
        try:
            if bool(i['date']) == True:
                with_date.append(i)
        except:pass
        
    # Get all people who received or sent a letter    
    creators = avoidTupleInList(nested_lookup('creator', with_date))
    subjects = avoidTupleInList(nested_lookup('subject', with_date))
    people = []
    
    # Delete Humboldt from creators' and subjects' lists
    for i in creators:
        if '[' in i :
            i = i.split(' [vermutlich]')[0]
        if 'Humboldt' not in i:
            people.append(i)
    for i in subjects:
        if 'Humboldt' not in i and i not in people:
            people.append(i)

    #Create dropdown Menu
    dropdown = createDropdown('', people)
    return dropdown 


def histogramm_by_person(all:bool):
    
    if all == True:
        d = byperson()
    else : d = by_women(women_partner())
    
    def on_value_change(change):
        output_bydate.clear_output(wait=True)
        display(Javascript('IPython.notebook.execute_cell()'))
        results = []
        liste = []
        with output_bydate:
            person = change['new']
            for i in data:
                try : 
                    if person in i["creator"] or person in i["subject"]:
                        results.append(i)
                except: pass     
            
            for i in results:
                try :
                    if int(i['date'][:4]) <1859:
                        liste.append((int(i['date'][:4]), int(1)))
                except:pass
            
            
            print('Number of letters: {0}'.format(len(results)))
            print('Letters with date: {0}'.format(len(liste)))
            print('Letters without date: {0}'.format(len(results)-len(liste)))      
            
            if len(liste) > 1:
                HBox([createhistogramm(liste, person), allonmap(results, 'coverage_location')])
            else:
                allonmap(results, 'coverage_location')
    dropdown = d
    output_bydate = widgets.Output()
    display(dropdown, output_bydate)
    dropdown.observe(on_value_change, names='value')


def sorted_by_period(data:list):
    by_period = {'1792-1796: Deutschland' : [], '1797-1804: Amerika': [] , '1805: Berlin': [], '1806-1828: Paris':[] ,'1829: Russland': [] ,'1830-1859: Berlin':[]}
    
    for i in data:
        try :
            date = int(i['date'][:4])
            if date > 1792 and date < 1796:
                by_period['1792-1796: Deutschland'].append(i)
            elif date > 1799 and date < 1804:
                by_period['1797-1804: Amerika'].append(i)
            elif date == 1805:
                by_period['1805: Berlin'].append(i)
            elif date > 1806 and date < 1828:
                by_period['1806-1828: Paris'].append(i)
            elif date == 1829:
                by_period['1829: Russland'].append(i)
            elif date > 1830 and date < 1859:
                by_period['1830-1859: Berlin'].append(i)
        except: pass

    return by_period


def mapByPeriod():
    btn = widgets.ToggleButtons(
                options= sorted_by_period(data),
                description='',
                disabled=False,
                button_style='',
                )

    def onchange(change):
        output.clear_output(wait=True)
        display(Javascript('IPython.notebook.execute_cell()'))
        with output:
             display(allonmap(change['new'], 'coverage_location'))


    output = widgets.Output()
    display(btn, output)
    btn.observe(onchange, 'value')

def mapByLocationType():
    btn = widgets.ToggleButtons(
                options= {"Show all letters": "coverage_location", "Show all contributors": "contributor_location"},
                description='',
                disabled=False,
                button_style='',
                )

    def onchange(change):
        output.clear_output(wait=True)
        display(Javascript('IPython.notebook.execute_cell()'))
        with output:
             display(allonmap(data, change['new']))


    output = widgets.Output()
    display(btn, output)
    btn.observe(onchange, 'value')
    

#### WOMEN ####
def women_partner():
    guess = gender_guesser.detector.Detector()
    data_women = []

    # Letters to AvH
    for i in data:
        try :
            if 'Humboldt' not in i['creator'] and 'Unbekannt' not in i['creator'] and type(i['creator']) != list:
                firstname = i['creator'].split(' ')[0]
                gender =guess.get_gender(firstname)
                if gender == 'unknown':
                    firstname = i['creator'].split(', ')[1].split(' (')[0]
                    gender =guess.get_gender(firstname)
                
                    if ' ' in firstname :
                        firstname = firstname.split(' ')[0]
                    elif '-' in firstname :
                        firstname = firstname.split('-')[0]

                if firstname == 'Henriette':
                    gender = 'female'
                else : 
                    gender = guess.get_gender(firstname)
                    
            if 'female' in gender:
                data_women.append(i)
        except: pass

    # Letters by AvH
    for i in data:
        try :
            if 'Humboldt' not in i['subject'] and 'Unbekannt' not in i['subject'] and type(i['subject']) != list:
                firstname = i['subject'].split(' ')[0]
                gender = guess.get_gender(firstname)
                if gender == 'unknown':
                    firstname = i['subject'].split(', ')[1].split(' (')[0]
                    gender =guess.get_gender(firstname)
                    if ' ' in firstname :
                        firstname = firstname.split(' ')[0]
                    elif '-' in firstname :
                        firstname = firstname.split('-')[0]

                    if firstname == 'Henriette':
                        gender = 'female'
                    else : 
                        gender =guess.get_gender(firstname)
                    
            if 'female' in gender:
                data_women.append(i)
        except: pass

    return data_women
       
def by_women(data:dict):
    """
    Function that creates a dropdown menu of all persons 
    who have received and/or sent at least one letter 
    for which a date is recorded
    :param data: dict
    :return: dropdown menu
    :rtype: widget
    """
 
    # Get all people who received or sent a letter    
    creators = avoidTupleInList(nested_lookup('creator', data))
    subjects = avoidTupleInList(nested_lookup('subject', data))
    people = []
    
    # Delete Humboldt from creators' and subjects' lists
    for i in creators:
        if '[' in i :
            i = i.split(' [vermutlich]')[0]
        if 'Humboldt' not in i:
            people.append(i)
    for i in subjects:
        if 'Humboldt' not in i and i not in people:
            people.append(i)

    #Create dropdown Menu
    dropdown = createDropdown('', people)
    return dropdown
    
#####

def age_distribution() :
    years_an = {}
    years_von = {}
    liste_an=[]
    liste_von=[]
    
    # Letter to Humboldt
    for i in data :
        try :
            if i["date"] and "Humboldt" not in i["creator"] and type(i["creator"]) != list :
                if i["date"][:4] not in years_an:
                    years_an[i["date"][:4]] = []
                years_an[i["date"][:4]].append(int(i["date"][:4]) - int(i["creator"].split("(")[1].split("-")[0][:4]))
        except: pass 

    # Letter by Humboldt     
    for i in data :
        try :
            if i["date"] and "Humboldt" not in i["subject"] and type(i["subject"]) != list :
                if i["date"][:4] not in years_von:
                    years_von[i["date"][:4]] = []
                years_von[i["date"][:4]].append(int(i["date"][:4]) - int(i["subject"].split("(")[1].split("-")[0][:4]))
        except: pass 

    for element in years_an.keys():
        try :
            if (float(element)<1859):
                for element1 in years_an[element]: 
                    if (float(element1)>0):
                        liste_an.append((float(element), float(element1)))
        except : pass
                
    for element in years_von.keys():
        try :
            if (float(element)<1859):
                for element1 in years_von[element]: 
                    if (float(element1)>0):
                        liste_von.append((float(element), float(element1)))
        except : pass

    x_coords = [coord[0] for coord in liste_an]
    y_coords = [coord[1] for coord in liste_an]
    fig= plt.figure(figsize=(10,8))
    plt.hist2d(x_coords, y_coords, bins=(40, 40), cmap=plt.cm.Reds)
    fig.suptitle('Letters to AvH: age distribution of senders', fontsize=14)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Age of the correspondence partner', fontsize=12)
    plt.colorbar()
    an_plt = plt.show()

    von_x_coords = [coord[0] for coord in liste_von]
    von_y_coords = [coord[1] for coord in liste_von]
    fig= plt.figure(figsize=(10,8))
    plt.hist2d(von_x_coords, von_y_coords, bins=(40, 40), cmap=plt.cm.Reds)
    fig.suptitle('Letters by AvH: age distribution of addressees', fontsize=14)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Age of the correspondence partner', fontsize=12)
    plt.colorbar()
    von_plt = plt.show()


# Represented data with recorded coordinates

def represented_data():
    both = 0
    contributor = 0
    for i in data:
        try:
            if i["coverage_location"] and i["contributor_location"]:
                both+=1
            elif i["contributor_location"]:
                contributor +=1
            
        except: pass
    no_represented= len(data) -(both+contributor)
    return [both, contributor, no_represented]

def recordedCoordinatePlot():
    fig, ax = plt.subplots()
    plt.rcParams.update({'font.size': 6})
    explode = (0.1, 0.2, 0.1)
    ax.pie(represented_data(),
       explode=explode,
       labels=["Contributor's and coverage's coord.", "Only contributor's coord.", "No recorded coordinate"] ,
        autopct='%1.1f%%',
       startangle=10)
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
    ax.set_title('Percentage of recorded coordinates in data')
    return plt.show()

# Functions for language plot

def language_data():
    eng = 0
    ger = 0
    fre = 0
    ita = 0
    spa = 0
    other =0
    more_than_one = 0 
    #more_than_one_list = []
    for i in data:
        try:
            if "ger" in i["language"]:
                ger+=1
            elif "fr" in i["language"]:
                fre +=1
            elif "en" in i["language"]:
                eng +=1
            elif "it" in i["language"]:
                ita +=1
            elif "sp" in i["language"]:
                spa +=1
            else:
                other +=1
                
            if type(i["language"])==list:
                more_than_one +=1
                
            
        except: pass
    return [[eng, ger, fre, ita, spa, other], more_than_one]

def languagePlot():
 
    fig, ax = plt.subplots()
    plt.rcParams.update({'font.size': 6})
    explode = (0.2, 0.1, 0.1, 0.4, 0.35, 0.25)
    ax.pie(language_data()[0],
       explode=explode,
       labels=["English", "German", "French", "Italian", "Spanish", "Other"] ,
        autopct='%1.1f%%',
       startangle=10)
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
    ax.set_title('In what languages are the letters written?')
    return plt.show()


# Contributor Plot
def contributorPlot():
    institutions = Counter(nested_lookup('contributor', data))
    filtered= {"others":0}

    for i in institutions:
        if institutions[i] > 100:
            filtered[i] = institutions[i]
        elif "France" in i:
            filtered["Bibliothèque nationale de France"] = institutions[i]
        elif institutions[i] <100:
            filtered["others"] += int(institutions[i])
    
    fig, ax = plt.subplots()
    plt.rcParams.update({'font.size': 6})
    #explode = (0.1, 0.1, 0.1, 0, 0.1, 0.1,0.1, 0.1)
    ax.pie(filtered.values(),
       #explode=explode,
       labels=filtered.keys(),
        autopct='%1.1f%%',
       startangle=40)
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
    ax.set_title('Where are most of the letters kept?')
    return plt.show()