"""
to RUN - 
scrapy crawl github_final
"""

from functools import partial
import json
import pandas as pd
import datetime
import scrapy


FILENAME = './output/pypi_data.pkl'
SAVENAME = './data/pypi_added.jsonl'
STATSNAME = './data/stats.txt'
FROM_TILL = './data/fromtill.txt'
global not_found_count
not_found_count = 0
global total_count
total_count = 0
personal_tokens = ['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','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','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','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','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','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']
length = len(personal_tokens)

df = pd.read_pickle(FILENAME)
columns = df.columns
FROM =  293250
# TILL = 5
TILL = min(FROM + 4800*length,len(df))


def write_data(file, dictionary):
    output_file = open(file, 'a', encoding='utf-8')
    json.dump(dictionary, output_file) 
    output_file.write("\n")


def save_data(data,row):
    global not_found_count
    global total_count
    if 'message' in data.keys() and data['message'] == "Not Found":
        not_found_count += 1
    else:
        dic = {}
        dic['forks_count'] = data['forks_count']
        dic['stargazers_count'] = data['stargazers_count']
        dic['watchers_count'] = data['watchers_count']
        for col in columns:
            dic[col] = row[col]
        write_data(SAVENAME,dic)
    if total_count % 50 == 0:
        with open(STATSNAME,'w') as f:
            f.write(f'{(total_count+1) - not_found_count} out of {total_count+1}')
    if total_count%100 == 0:
        e = datetime.datetime.now()
        print(total_count)
        print ("The time is now: = %s:%s:%s" % (e.hour, e.minute, e.second))
    total_count += 1
    


class web(scrapy.Spider):  

    name = "github_final" 

    def start_requests(self): 

        with open(FROM_TILL,'w') as f:
            f.write(f'FROM : {FROM} TILL : {TILL}\n')
        for i in range(FROM,TILL):
            
            row = df.iloc[i]
            link = row['GitHub Link']
            if link == "" or link == None:
                continue
            yield scrapy.Request(url=link,callback = partial(self.parse,row),headers={"Authorization": f"token {personal_tokens[i%length]}"}) 

            

    def parse(self,row,response):
      
        data = json.loads(response.text)
        save_data(data,row)
