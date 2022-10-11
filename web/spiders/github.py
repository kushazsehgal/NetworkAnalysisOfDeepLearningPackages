"""
RUN COMMAND - 
scrapy crawl github
"""
from itertools import count
import scrapy
import json
import pandas as pd
from functools import partial
import datetime
from bs4 import BeautifulSoup
pre = "https://github.com"
FILENAME = "./output/pypi_data.jsonl"
SAVENAME = './output/pypi_github_added.jsonl'
save = './data/num_github.txt'
global total_count 
total_count = 0
global total_empty_count
total_empty_count = 0
global counT

def parse_attr(html,dic):

    # print(soup)
    global total_count
    global total_empty_count
    global counT
    soup = BeautifulSoup(html, 'lxml')
    divtag = soup.find('div',{'class':'BorderGrid BorderGrid--spacious'})
    dic['Watchers'] = ''
    # print(dic.keys())
    strongtags = divtag.find_all('strong')
    if len(strongtags) == 0:
        print('here')
        total_empty_count += 1
    for i,strongtag in enumerate(strongtags):
        if i == 0:
            dic['Stars'] = strongtag.text
        if i == 1:
            dic['Watchers'] = strongtag.text
        if i == 2:
            dic['Forks'] = strongtag.text
    total_count+=1
    if total_count%100 == 0:
        e = datetime.datetime.now()
        print(total_count)
        print ("The time is now: = %s:%s:%s" % (e.hour, e.minute, e.second))
    # print(dic)
    if total_count%50 == 0:
        with open(save,'w') as f:
            string =str(total_count) + ' out of ' + str(counT) 
            f.write(string)
    write_data(SAVENAME, dic)
    return

def write_data(file, dictionary):
    output_file = open(file, 'a', encoding='utf-8')
    json.dump(dictionary, output_file) 
    output_file.write("\n")


class web(scrapy.Spider):  

    name = "github" 

    def start_requests(self): 

        with open(FILENAME) as libo_file:
            global counT
            counT = 0
            for line in libo_file.readlines():
                dic = json.loads(line)
                url = pre + '/' + dic['GitHub Link'][29:]
                # print("URL IS : ",url)
                yield scrapy.Request(url = url,callback = partial(self.parse,dic))
                counT += 1
                # if count >= 5:
                #     break
            
    def parse(self,dic,response):
      
        html = response.text
        parse_attr(html,dic)
        
