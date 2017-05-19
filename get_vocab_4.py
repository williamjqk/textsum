from collections import Counter
import re
import sys
from multiprocessing import Pool, Manager
from functools import reduce
import operator as op

# def main(input_file,output_file):

input_file = '/home/ljc/mywork/corpus/dailymail_20170307/data_dailymail_training'
output_file ='./data/vocab_data_dm_tr'

# input_file = '/home/ljc/mywork/corpus/dailymail_20170307/data_dailymail_validation'
# output_file ='./data/vocab_data_dm_va'




def split_words(text):
    return re.split(' |=|\n|\t',text)

with open(input_file,'r') as fr:
    text_in = fr.readlines()
    with Pool(8) as p:
        words = p.map(split_words, text_in)
        #words = [re.split(' |=|\n|\t',text) for text in text_in]
#print(words)

# v = []
# for x in words:
#     v = v+x


def merge_list(alist):
    len_of_list = len(alist)
    half = int(len_of_list/2)
    if len_of_list > 10:
        list1 = alist[0:half]
        list2 = alist[half:]
        merged_list = merge_list(list1) + merge_list(list2)
    else:
        merged_list = []
        for x in alist:
            merged_list += x
        #merged_list = reduce(op.add, alist)
    return merged_list

# %%
# v = []
# for i,x in enumerate(words):
#     if i % 100 == 0:
#         print('Has added %d documents' % i)
#     v = v+x
n_thread = 8
chunk_size = int(len(words)/8) + 1
words_chunks = [words[i:chunk_size] for i in range(0,len(words),chunk_size)]
with Pool(n_thread) as p:
    temp = p.map(merge_list, words_chunks)
    v = merge_list(temp)
len(v)



# #
# d1 = {}
# for x in v:
#     if x in d1:
#         d1[x] += 1
#     else:
#         d1[x] = 1
#
# len(d1)
# del d1['']
# d1['<UNK>'] = 12
# d1['<PAD>'] = 5

# %%s
v_dict = Counter(v)
#print(v_dict)
del v_dict['']
v_dict['<UNK>'] = 12
v_dict['<PAD>'] = 5

# %%
with open(output_file,'w') as fw:
    for x in v_dict:
        fw.write(x+' '+str(v_dict[x])+'\n')


# if __name__ == '__main__':
#     script, input_file,output_file = sys.argv
#     main(input_file,output_file)


# %%
reduce(op.add, [[1,2,3],['a','b','c'],[4,5,6]])
