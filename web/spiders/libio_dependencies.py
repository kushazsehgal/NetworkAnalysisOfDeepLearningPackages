"""
RUN COMMAND - 
scrapy crawl libio_dependencies
"""
import scrapy
import json
import pandas as pd
from functools import partial
import datetime
from bs4 import BeautifulSoup
pre = "https://libraries.io"
post = "/json"
FILENAME = "./output/libio_data.jsonl"
SAVENAME = './output/libio_depen_added.jsonl'
save = './data/num.txt'
global total_count 
total_count = 0
global total_empty_count
total_empty_count = 0
def parse_attr(html,dic):

    # print(soup)
    global total_count
    global total_empty_count
    soup = BeautifulSoup(html, 'lxml')
    dic['package dependencies'] = []
    dic['package dependencies link'] = []
    dic['Dependencies Tree'] = ''
    # print(dic.keys())
    dl = soup.find('dl')
    if dl != None:
        for dt_tag in dl.find_all('dt'):
            a_tag = dt_tag.find('a')
            dic['package dependencies'].append(a_tag.text)
            dic['package dependencies link'].append(a_tag.get('href'))
        dic['Dependencies Tree'] = soup.find_all('a')[-1].get('href')
    else:
        print('here')
        total_empty_count += 1
    total_count+=1
    if total_count%100 == 0:
        e = datetime.datetime.now()
        print(total_count)
        print ("The time is now: = %s:%s:%s" % (e.hour, e.minute, e.second))
    # print(dic)
    with open(save,'w') as f:
        string =str(total_empty_count) + ' out of ' + str(total_count) 
        f.write(string)
    write_data(SAVENAME, dic)

    return

def write_data(file, dictionary):
    output_file = open(file, 'a', encoding='utf-8')
    json.dump(dictionary, output_file) 
    output_file.write("\n")


class web(scrapy.Spider):  

    name = "libio_dependencies" 

    def start_requests(self): 

        with open(FILENAME) as libo_file:
            count = 0
            for line in libo_file.readlines():
                dic = json.loads(line)
                url = pre + dic['Dependencies Link']
                yield scrapy.Request(url = url,callback = partial(self.parse,dic))
                # count += 1
                # if count >= 5:
                #     break
            
    def parse(self,dic,response):
      
        html = response.text
        parse_attr(html,dic)
        
