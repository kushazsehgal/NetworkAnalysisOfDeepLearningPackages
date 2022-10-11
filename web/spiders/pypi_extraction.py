import scrapy
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
from functools import partial
import datetime
pre = "https://pypi.org/project/"

global total_count 
total_count = 0

def parse_attr(html,pkg_name):

    soup = BeautifulSoup(html, 'lxml')
    # print(soup)
    global total_count
    dictionary = {}
    dictionary['Package Name'] = pkg_name
    dictionary["Package Version"] = ""
    dictionary["Release Date"] = ""
    dictionary['Package URL'] = pre+pkg_name + '/'
    dictionary['Stars'] = 0
    dictionary['Forks'] = 0
    dictionary['Open/Closed Issues'] = 0
    dictionary['License'] = ""
    dictionary["Author"] = ""
    dictionary["pypi_keywords"] = ""
    dictionary["Requires"] = ""
    dictionary["Maintainers"] = []
    dictionary["Development Status"] = []
    dictionary["Environment"] = []
    dictionary["Intended Audience"] = []
    dictionary["Classifier License"] = []
    dictionary["Programming Language"] = []
    dictionary["Topic"] = []
    dictionary["Framework"] = []
    dictionary["Natural Language"] = []
    dictionary["Package Version"] = soup.find('h1',{"class":"package-header__name"}).text.strip()
    dictionary["Release Date"] = (soup.find('p',{"class":"package-header__date"})).find('time').text.strip()
    dictionary["Operating System"] = []
    dictionary['GitHub Link'] = ""

    left_tab = soup.find('div',{"class":"vertical-tabs__tabs"})
    # print(left_tab)
    for sidebar_section in left_tab.find_all('div',{"class":"sidebar-section"}):

        if sidebar_section.find('h3',{"class":"sidebar-section__title"}) == None:
            continue
        title = sidebar_section.find('h3',{"class":"sidebar-section__title"}).text.strip()
        if title == "Statistics":
            # print("*"*50,"In Statistics","*"*50)
            do_Statistics(sidebar_section,dictionary)
        if title == "Meta":
            # print("*"*50,"In Meta","*"*50)
            do_Meta(sidebar_section,dictionary)
        if title == "Maintainers":
            # print("*"*50,"In Maintainers","*"*50)
            do_Maintainers(sidebar_section,dictionary)
        if title == "Classifiers":
            # print("*"*50,"In Classifiers","*"*50)
            do_Classifiers(sidebar_section,dictionary)

    # print("#"*75)
    total_count+=1
    if total_count%100 == 0:
        e = datetime.datetime.now()
        print(total_count,dictionary['Package Name'])
        print ("The time is now: = %s:%s:%s" % (e.hour, e.minute, e.second))
    return dictionary

def do_Statistics(sidebar_section,dictionary):

    if sidebar_section.find('div',{"class":"github-repo-info"}) != None:
        dictionary["GitHub Link"] = sidebar_section.find('div',{"class":"github-repo-info"})["data-url"]
    if sidebar_section.find('span',{"data-key":"stargazers_count"}) != None:
        dictionary['Stars'] = sidebar_section.find('span',{"data-key":"stargazers_count"}).text.strip()
    # print("Stars",sidebar_section.find('span',{"data-key":"stargazers_count"}))
    # print("Stars",sidebar_section.find('span',{"data-key":"stargazers_count"}).parent.text)
    if sidebar_section.find('span',{"data-key":"forks_count"}) != None:
        dictionary['Forks'] = sidebar_section.find('span',{"data-key":"forks_count"}).text.strip()
    # print("Forks",sidebar_section.find('span',{"data-key":"forks_count"}).next_sibling.text.strip())
    if sidebar_section.find('span',{"data-key":"open_issues_count"}) != None:
        dictionary['Open/Closed Issues'] = sidebar_section.find('span',{"data-key":"open_issues_count"}).text.strip()
def do_Meta(sidebar_section,dictionary):
    for strong_tag in sidebar_section.find_all('strong'):
        if strong_tag.text == "License:":
            dictionary['License'] = strong_tag.parent.text.strip()
            # print("license",strong_tag.parent.text)
        if strong_tag.text == "Author:":
            if strong_tag.find_next_sibling('a') != None:
                dictionary['Author'] = strong_tag.find_next_sibling('a').text.strip()
        if strong_tag.text == "Requires:":
            # dictionary['Requires'] = strong_tag.findParent('p').text
            dictionary['Requires'] = strong_tag.parent.text.strip()
    for keyword_span in sidebar_section.find_all('span',{"class":"package-keyword"}):
                dictionary['pypi_keywords'] += keyword_span.text.strip()
def do_Maintainers(sidebar_section,dictionary):

    for maintainer_span in sidebar_section.find_all('span',{"class":"sidebar-section__user-gravatar-text"}):
        dictionary['Maintainers'].append(maintainer_span.text.strip())
#TODO:
def do_Classifiers(sidebar_section,dictionary):
    
    ul_tag = sidebar_section.find('ul',{"class":"sidebar-section__classifiers"})
    for strong_tag in ul_tag.find_all('strong'):
        val = strong_tag.text.strip()
        val_ul_tag = strong_tag.find_next_sibling('ul')
        for li_tag in val_ul_tag.find_all('li'):
            if val == "License":
                dictionary['Classifier License'].append(li_tag.text.strip())
                continue
            dictionary[val].append(li_tag.find('a').text.strip())

    

def write_data(file, dictionary):
    output_file = open(file, 'a', encoding='utf-8')
    # for dic in dictionary_list:
    json.dump(dictionary, output_file) 
    output_file.write("\n")

class web(scrapy.Spider):  

    name = "pypi_data" 

    def start_requests(self): 

        df = pd.read_csv('F:\IIM banglore\python packages\data\pypi_pkg_names.csv')
        pkg_names = df['Package Name'].tolist()
        # pkg_names = ['torch','Actflow','101903755','a99']
        # pkg_names = ['torch']
        for pkg_name in pkg_names[207680:]:
            url = pre + pkg_name + '/'
            yield scrapy.Request(url=url, callback=partial(self.parse,pkg_name)) 
        
    def parse(self,pkg_name,response):
      
        html = response.text
        # print(html.encode('gbk', 'ignore').decode('gbk'))
        data = parse_attr(html,pkg_name)
        write_data('F:\IIM banglore\python packages\output\pypi_data.jsonl', (data))
