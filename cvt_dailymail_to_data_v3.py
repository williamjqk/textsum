import json
import spacy
from multiprocessing import Pool, Array, Manager
from functools import partial
import os

news_name = 'dailymail_'
mode = 'test'
# file_name = '../corpus/dailymail_20170307/out_dailymail_wayback_training_urls.json'
# file_name = '../corpus/dailymail_20170307/out_dailymail_wayback_test_urls.json'
file_name = '../corpus/dailymail_20170307/out_dailymail_wayback_'+mode+'_urls.json'
# file_name = '../corpus/dailymail_20170307/json_test.json'

def json2textsumFormat(log_stat, json1):
    id_here = os.getpid()
    idx = id_here % 10
    log_stat[idx] = log_stat[idx] + 1
    if log_stat[idx] % 10 == 0:
        print(str(id_here)+'-------'+str(log_stat[idx]),idx)
    # print(log_stat)
    json1['text']
    len(json1['text'])
    lines = [x for x in json1['text'].split('\n') if x]
    nlp = spacy.load('en')
    l_temp = [' '.join(['<s>'] + [x.text.lower() for x in nlp(line)] + ['</s>']) for line in lines]
    article = ' '.join(l_temp)
    article = 'article=<d> <p> ' + article + ' </p> </d>\t'
    abstract = 'abstract=<d> <p> <s> ' + ' '.join([x.text for x in nlp(json1['title'].split('\n')[0])]) + ' </s> </p> </d>\t'
    publisher = 'publisher=AFP\n'
    out1 = article + abstract + publisher
    return out1



with open(file_name,'r') as f:
    json_list = [json.loads(line) for line in f]
    json_list = [x for x in json_list if x['title']!=None and x['text']!=None]
    json_list = [x for x in json_list if len(x['title'])>4 and len(x['text'])>4]

# log_stat = [0]*100
# log_stat = Array('i', [0]*100)
nlp = spacy.load('en') # spacy.load cost a lot of time
# nlp10 = [nlp]*10
log_stat = Manager().list([0]*100)
func1 = partial(json2textsumFormat, log_stat)
with Pool(8) as p:
    out_list = p.map(func1, json_list)


# %%
out_file = '../corpus/dailymail_20170307/data_'+news_name + mode
with open(out_file, 'w') as f:
    f.writelines(out_list)

# %%
if None != None:
    print(1)

# %%
from spacy.en import English
# nlp = spacy.load('en')
nlp = English()
doc = nlp("Who'S Your daddy")
doc[1].text.lower()
