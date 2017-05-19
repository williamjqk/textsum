with open('data/toy_vocab','r') as f:
    v1 = f.readlines()
with open('data/vocab','r') as f:
    v2 = f.readlines()
v = v1+v2

d = {}
for l in v:
    temp = l.strip('\n').split(' ')
    if temp[0] not in d:
        d[temp[0]] = int(temp[1])
    else:
        d[temp[0]] = d[temp[0]] + int(temp[1])


# %%
# with open('data/toy_data_vocab','w') as f:
#     f.writelines(v)
with open('data/toy_data_vocab','w') as f:
    for x in d:
        f.write(x+' '+str(d[x])+'\n')
