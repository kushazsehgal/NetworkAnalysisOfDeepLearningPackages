"""
RUN COMMAND - 
scrapy crawl description
"""
import scrapy
import json
import pandas as pd
from functools import partial
import datetime
pre = "https://pypi.org/pypi/"
post = "/json"
# FILENAME = "./output/pypi_data.jsonl"
SAVENAME = './output/pypi_desc.jsonl'
global total_count 
total_count = 0
def parse_attr(html,pkg_name):

    # print(soup)
    global total_count
    newdata =  json.loads(html)
    keys = ['html_url','description','stargazers_count','watchers_count','forks_count']
    dic = {} 
    dic['Package Name'] = pkg_name
    dic['Description'] = (newdata['info']['description'])
    total_count+=1
    if total_count%100 == 0:
        e = datetime.datetime.now()
        print(total_count)
        print ("The time is now: = %s:%s:%s" % (e.hour, e.minute, e.second))
    write_data(SAVENAME, dic)
    return

def write_data(file, dictionary):
    output_file = open(file, 'a', encoding='utf-8')
    json.dump(dictionary, output_file) 
    output_file.write("\n")


class web(scrapy.Spider):  

    name = "description" 

    def start_requests(self): 

        df = pd.read_pickle('F:\IIM banglore\python packages\output\pypi_data.pkl');
        # df = df.head(10)
        key = "Package Name"
        for i,row in df.iterrows():
            pkg_name = row[key]
            url = pre + pkg_name + post
            yield scrapy.Request(url=url, callback=partial(self.parse,pkg_name)) 
        print('reached here')
    def parse(self,pkg_name,response):
      
        html = response.text
        # print(html.encode('gbk', 'ignore').decode('gbk'))
        parse_attr(html,pkg_name)
        
