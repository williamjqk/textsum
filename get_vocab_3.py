from collections import Counter
import re
import sys

def main(input_file,output_file):
    # input_file ='./data/text_data'
    # output_file ='./data/toy_vocab'
    with open(input_file,'r') as fr:
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


    with open(output_file,'w') as fw:
        for x in v_dict:
            fw.write(x+' '+str(v_dict[x])+'\n')


if __name__ == '__main__':
    script, input_file,output_file = sys.argv
    main(input_file,output_file)
