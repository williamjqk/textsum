import json
import spacy
from multiprocessing import Pool, Array, Manager
from functools import partial
import os

news_name = 'dailymail_'
mode = 'training' #validation
# file_name = '../corpus/dailymail_20170307/out_dailymail_wayback_training_urls.json'
# file_name = '../corpus/dailymail_20170307/out_dailymail_wayback_test_urls.json'
file_name = '../corpus/dailymail_20170307/out_dailymail_wayback_'+mode+'_urls.json'
# file_name = '../corpus/dailymail_20170307/json_test.json'

def json2textsumFormat(nlp, json_list, pid):
    log = 0
    out_list = []
    for json1 in json_list:
        id_here = os.getpid()
        idx = id_here % 10
        log = log + 1
        if log % 100 == 0:
            print('Thread %d completes %d duc' % (pid, log) )
        json1['text']
        len(json1['text'])
        lines = [x for x in json1['text'].split('\n') if x]
        l_temp = [' '.join(['<s>'] + [x.text.lower() for x in nlp(line)] + ['</s>']) for line in lines]
        article = ' '.join(l_temp)
        article = 'article=<d> <p> ' + article + ' </p> </d>\t'
        abstract = 'abstract=<d> <p> <s> ' + ' '.join([x.text for x in nlp(json1['title'].split('\n')[0])]) + ' </s> </p> </d>\t'
        publisher = 'publisher=AFP\n'
        out1 = article + abstract + publisher
        out_list.append(out1)
    return out_list

def for2mpChunk(json_list):
    nlp = spacy.load('en') # spacy.load cost a lot of time
    pid = os.getpid()
    return json2textsumFormat(nlp, json_list, pid)



with open(file_name,'r') as f:
    json_list = [json.loads(line) for line in f]
    json_list = [x for x in json_list if x['title']!=None and x['text']!=None]
    json_list = [x for x in json_list if len(x['title'])>4 and len(x['text'])>4]

n_thread = 8
seg = int(len(json_list) / 8 + 1)
json_chunk = [json_list[i:i+seg] for i in range(0,len(json_list),seg)]

with Pool(n_thread) as p:
    out_chunk = p.map(for2mpChunk, json_chunk)

out_list = []
for x in out_chunk:
    out_list += x

# %%
out_file = '../corpus/dailymail_20170307/data_'+news_name + mode
with open(out_file, 'w') as f:
    f.writelines(out_list)

# %%
if None != None:
    print(1)

a = [1,2,3]
b = [7,8,9]
c = ['a','b','c']
l = [a,b,c]
import operator as op
from functools import reduce
reduce(op.add,l)

# %%
from spacy.en import English
# nlp = spacy.load('en')
nlp = English()
doc = nlp("Who'S Your daddy")
doc[1].text.lower()
