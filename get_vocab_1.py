from collections import Counter
import re
with open('./data/text_data','r') as fr:
    text_in = fr.readlines()
    words = [re.split(' |=|\n|\t',text) for text in text_in]
#print(words)

v = []
for x in words:
    v = v+x
v_dict = Counter(v)
print(v_dict)
del v_dict['']
v_dict['<UNK>'] = 12
v_dict['<PAD>'] = 5




with open('./data/toy_vocab','w') as fw:
    for x in v_dict:
        fw.write(x+' '+str(v_dict[x])+'\n')



# %%
a = 'a nn dsf'
print(re.split(' |n',a))
