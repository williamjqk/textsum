import json
import spacy
with open('../corpus/dailymail_20170307/out_dailymail_wayback_training_urls.json','r') as f:
    line = f.readline()
line
json1 = json.loads(line)
json1['text']
len(json1['text'])
lines = [x for x in json1['text'].split('\n') if x]
# lines
# lines[0]

# %%
nlp = spacy.load('en')
doc = nlp(lines[0])
#[x for x in doc]


#l_temp = ['<s>'] + [doc[i].text for i in range(doc.__len__())] + ['</s>']
#type(doc)
l_temp = [' '.join(['<s>'] + [x.text for x in nlp(line)] + ['</s>']) for line in lines]
#print(l_temp)

article = ' '.join(l_temp)
#print(article)

article = 'article=<d> <p> ' + article + ' </p> </d>\t'
#print(article)
abstract = 'abstract=<d> <p> <s> ' + ' '.join([x.text for x in nlp(json1['title'].split('\n')[0])]) + ' </s> </p> </d>\t'
#print(abstract)

publisher = 'publisher=AFP\n'
out1 = article + abstract + publisher
#print(out1)

# %%
