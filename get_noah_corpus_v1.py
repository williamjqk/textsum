import json
from multiprocessing import Pool, Array, Manager
from functools import partial
import os
import pandas as pd
import re
import itertools
from collections import Counter

base_dir = './noah_chs_chat/'
post_file = base_dir + 'post.index'
response_file = base_dir + 'response.index'
original_pair_file = base_dir + 'original.pair'
output_data_file = base_dir + 'noah_data'

re_sub = re.compile('[^,，。！!\u4e00-\u9fa5]')

def lines2list(line):
    x = line.split('##')
    return [int(x[0]), re_sub.sub(' ', x[1]).split()]

pool_num = 16
with open(post_file, 'r') as f:
    lines = f.readlines()
    with Pool(pool_num) as p:
        lines = p.map(lines2list, lines)
    post_dict = {x[0]: x[1] for x in lines}
with open(response_file, 'r') as f:
    lines = f.readlines()
    with Pool(pool_num) as p:
        lines = p.map(lines2list, lines)
    response_dict = {x[0]: x[1] for x in lines}
with open(original_pair_file, 'r') as f:
    lines = f.readlines()
    lines = [x.split(':') for x in lines]
    lines = [[[int(x[0]),int(y)] for y in x[1].split(',')] for x in lines]
    pair_l = list(itertools.chain(*lines))
len(pair_l),pair_l[-1]
len(post_dict),post_dict[0]
len(response_dict),response_dict[0]

corpus_pairs = [[post_dict[x[0]],response_dict[x[1]]] for x in pair_l]
len(corpus_pairs),corpus_pairs[1]

# %% generate chat corpus fit textsum model
def pair2textsumFormat(pair):
    article = ' '.join(pair[0])
    abstract = ' '.join(pair[1])
    article = 'article=<d> <p> <s> ' + article + ' </s> </p> </d>\t'
    abstract = 'abstract=<d> <p> <s> ' + abstract + ' </s> </p> </d>\t'
    publisher = 'publisher=AFP\n'
    return article + abstract + publisher
with Pool(pool_num) as p:
    out_l = p.map(pair2textsumFormat, corpus_pairs)

with open(output_data_file, 'w') as f:
    f.write(''.join(out_l))

# %% generate noah chat vocab
in_file = output_data_file
out_file = base_dir + 'noah_vocab'
with open(in_file,'r') as fr:
    text_in = fr.readlines()
    words = [re.split(' |=|\n|\t|article|abstract|publisher|AFP',text) for text in text_in]

v_l = list(itertools.chain(*words))

v_counter = Counter(v_l)
least_times = 20
v_dict = {}
for k,v in v_counter.items():
    if v > least_times:
        v_dict[k] = v
# print(v_dict)
del v_dict['']
v_dict['<UNK>'] = 2000
v_dict['<PAD>'] = 2000
len(v_dict)

with open(out_file,'w') as fw:
    for x in v_dict:
        fw.write(x+' '+str(v_dict[x])+'\n')
