import scrapy
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
from functools import partial
import datetime
pre = "https://libraries.io/pypi/"

global total_count 
total_count = 0

def parse_attr(html,pkg_name):

    soup = BeautifulSoup(html, 'lxml')
    # print(soup)
    global total_count
    dictionary = {}
    dictionary["Package Name"] = pkg_name
    dictionary["libio - Keywords"] = []
    dictionary["SourceRank"] = ""
    dictionary["Dependencies"] = ""
    dictionary["Dependent packages"] = ""
    dictionary["Dependent repositories"] = ""
    dictionary["Total releases"] = ""   
    dictionary["Latest release"] = ""
    dictionary["First release"] = ""
    dictionary["Stars"] = ""
    dictionary["Forks"] = ""
    dictionary["Watchers"] = ""
    dictionary["Contributors"] = ""
    dictionary["Repository size"] = "" 
    dictionary["(Dependency,Version)"] = []
    dictionary["(Dependent,stars)"] = []
    dictionary["Dependencies Link"] = ""
    dictionary["Dependent Repos Link"] = ""
    doKeywords(soup,dictionary)
    div_tags = soup.find_all('div',{"class":"col-md-4 sidebar"})
    doDiv0(div_tags[0],dictionary)
    doDiv1(div_tags[1],dictionary)

    total_count+=1
    if total_count%100 == 0:
        e = datetime.datetime.now()
        print(total_count,dictionary['Package Name'])
        print ("The time is now: = %s:%s:%s" % (e.hour, e.minute, e.second))
    return dictionary

def doKeywords(soup,dictionary):

    div_tag = soup.find('div',{"class":"col-md-8"})
    dd_tag = div_tag.find('dd')
    if dd_tag == None:
        return
    for a_tag in dd_tag.find_all('a'):
        dictionary["libio - Keywords"].append(a_tag.text.strip())

def doDiv0(div_tag,dictionary):

    dt_tags = div_tag.find_all('dt')
    for dt_tag in dt_tags:
        tag_val = dt_tag.text.strip()
        dictionary[tag_val] = dt_tag.find_next_sibling('dd').text.strip()


def doDiv1(div_tag,dictionary):
    
    # print(div_tag)
    dependencies_tag = div_tag.find('div',{"id":"version_dependencies"})
    dictionary["Dependencies Link"] = dependencies_tag['data-url']
    # print('*'*50)
    # print(dependencies_tag)
    if dependencies_tag != None:
        for dt_tag in dependencies_tag.find_all('dt'):
            dependency = dt_tag.text.strip()
            version = dt_tag.find_next_sibling('dd').text.strip()
            dictionary["(Dependency,Version)"].append((dependency,version))
    
    usedby_tag = div_tag.find('div',{"id":"top_dependent_repos"})
    dictionary['Dependent Repos Link'] = usedby_tag['data-url']
    if usedby_tag != None:
        for dt_tag in usedby_tag.find_all('dt'):
            usedby = dt_tag.text.strip()
            stars = dt_tag.find_next_sibling('dd').text.strip()
            dictionary["(Dependent,stars)"].append((usedby,stars))
def write_data(file, dictionary):
    output_file = open(file, 'a', encoding='utf-8')
    # for dic in dictionary_list:
    json.dump(dictionary, output_file) 
    output_file.write("\n")

class web(scrapy.Spider):  

    name = "libio_data" 

    def start_requests(self): 

        df = pd.read_csv('F:\IIM banglore\python packages\data\pypi_pkg_names.csv')
        pkg_names = df['Package Name'].tolist()
        # pkg_names = ['torch','Actflow','101903755','a99','tensorflow']
        # pkg_names = ['torch']
        for pkg_name in pkg_names[207680:]:
            url = pre + pkg_name + '/'
            yield scrapy.Request(url=url, callback=partial(self.parse,pkg_name)) 

    def parse(self,pkg_name,response):
      
        html = response.text
        # print(html.encode('gbk', 'ignore').decode('gbk'))
        data = parse_attr(html,pkg_name)
        write_data('F:\IIM banglore\python packages\output\libio_data.jsonl', (data))
