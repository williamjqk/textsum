import json
import spacy


# file_name = '../corpus/dailymail_20170307/out_dailymail_wayback_training_urls.json'
file_name = '../corpus/dailymail_20170307/out_dailymail_wayback_test_urls.json'

def json2textsumFormat(json1):
    # line
    # json1 = json.loads(line)
    json1['text']
    len(json1['text'])
    lines = [x for x in json1['text'].split('\n') if x]
    # lines
    # lines[0]

    nlp = spacy.load('en')
    #doc = nlp(lines[0])
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

    publisher = 'publisher=AFP'
    out1 = article + abstract + publisher
    #print(out1)
    return out1


out_list = []
with open(file_name,'r') as f:
    # line = f.readline()
    for line in f:
        json1 = json.loads(line)
        if json1['title']==None or json1['text']==None:
            continue
        if len(json1['title'])<5 or len(json1['text'])<5:
            out_list.append(json2textsumFormat(json1))

out_file = '../corpus/dailymail_20170307/data_dailymail_test'
with open(out_file, 'w') as f:
    f.writelines(out_list)




# %%
if None != None:
    print(1)
