# 运行方式
CUDA_VISIBLE_DEVICES=2 python local_test.py
### data convert
python data_convert_example.py --command text_to_binary --in_file /home/data/ljc/film_caption/corpus/film_data --out_file /home/data/ljc/film_caption/corpus/film_data_bin
### train
CUDA_VISIBLE_DEVICES=2 python local_test.py --mode=train --article_key=article --abstract_key=abstract --data_path=data/toy_chat_data_bin --vocab_path=data/toy_data_vocab --log_root=log_root --train_dir=log_root/train
### test
CUDA_VISIBLE_DEVICES=2 python local_test.py --mode=decode --article_key=article --abstract_key=abstract --data_path=data/toy_chat_data_bin --vocab_path=data/toy_data_vocab --log_root=log_root --decode_dir=log_root/decode

### train film caption data
CUDA_VISIBLE_DEVICES=2 python main_film_caption_v1.py --mode=train --article_key=article --abstract_key=abstract --data_path=/home/data/ljc/film_caption/corpus/training-aa --vocab_path=/home/data/ljc/film_caption/corpus/film_vocab --log_root=log_root --train_dir=log_root/train

### train noah data
CUDA_VISIBLE_DEVICES=2 python local_test.py --mode=train --article_key=article --abstract_key=abstract --data_path=noah_chs_chat/noah_data_bin --vocab_path=noah_chs_chat/noah_vocab --log_root=log_root --train_dir=log_root/train
### test noah data
CUDA_VISIBLE_DEVICES=2 python local_test.py --mode=decode --article_key=article --abstract_key=abstract --data_path=noah_chs_chat/noah_data_bin --vocab_path=noah_chs_chat/noah_vocab --log_root=log_root --decode_dir=log_root/decode --beam_size=2

### train use bucket
CUDA_VISIBLE_DEVICES=2 python local_test.py --mode=train --article_key=article --abstract_key=abstract --data_path=data/toy_chat_data_bin --vocab_path=data/toy_data_vocab --log_root=log_root --train_dir=log_root/train --use_bucketing=True
### test use bucket
CUDA_VISIBLE_DEVICES=2 python local_test.py --mode=decode --article_key=article --abstract_key=abstract --data_path=data/toy_chat_data_bin --vocab_path=data/toy_data_vocab --log_root=log_root --decode_dir=log_root/decode --use_bucketing=True

download_common_crawl_170222a.py-----用网上的程序下载amazon的common crawl有问题
download_common_crawl_170223a.py-----自己修改过的用urllib和gzip保存common crawl的wet
                                -----这个程序虽然能用，但是aws common crawl中的内容太杂了
------上述的两个文件已经移到aws_common_crawl文件夹下了-------
read_usenet_170222a.py---------------读取这个网站下载下来的数据，但是这组数据全是乱序的语句，
                      ---------------没法做textsum
                      ---------------http://statmt.org/wmt13/translation-task.html#download

********下面是和textsum比较相关的自定义程序**********
get_vocab_1.py--------------对一个语料文件中出现的所有词提取出来，并记录出现次数生成一个类似
              --------------/data/vocab的文件
get_vocab_2.py--------------将data中的vocab和原始自带的vocab合并，生成一个新的vocab
get_vocab_3.py--------------写成一个shell可执行的，可给输入参数的版本
get_vocab_4.py--------------不用Counter的多进程版本(统计的时候就用最简单的for循环)

cvt_dailymail_to_data.py----将使用newspaper爬下来的dailymail处理为textsum能识别的格式
                        ----(当然还需要用的data_convert_example.py转一下)
cvt_dailymail_to_data_v2.py----写成函数封装对整个文件进行转换
cvt_dailymail_to_data_v3.py----转换成Pool多进程
cvt_dailymail_to_data_v4.py----单线程版本(spacy.load太慢)
cvt_dailymail_to_data_v5.py----多线程，每个线程处理list的一大部分
data_convert_example_v2.py-----split '=' on first occurrence

local_test.py-----本地测试程序
test_py2py3.py-----测试py2py3兼容性
compat.py---------统一的兼容性导入文件

get_noah_corpus_v1.py-----把华为的noah语料整理成textsum格式

---------------------------------------------------------
python2到python3迁移的修改点
data_convert_example.py--------------加入了encode和decode
batch_reader---------import Queue改成import queue as Queue, xrange --> range
beam_search---------- xrange --> range
seq2seq_attention_model.py------ xrange --> range
seq2seq_attention_decode.py------ xrange --> range

tf0.x到tf1.x的迁移
tf_upgrade --> seq2seq_attention.py
tf_upgrade --> seq2seq_attention_model.py
tf_upgrade --> seq2seq_attention_decode.py
seq2seq_attention_model.py ----- tf.nn.rnn_cell.LSTMCell-->tf.contrib.rnn.LSTMCell
                          ----- tf.nn.bidirectional_rnn-->tf.contrib.rnn.static_bidirectional_rnn
                          -----tf.nn.seq2seq-->tf.contrib.legacy_seq2seq
                          -----在tf.nn.sampled_softmax_loss中inputs,labels-->labels, inputs,
seq2seq_lib---------line45-----tf.op_scope(values, name, default_name) is deprecated, use tf.name_scope(name, default_name, values)


-----------------在toy数据集上的指令---------------------
# Run the training.
bazel-bin/textsum/seq2seq_attention \
  --mode=train \
  --article_key=article \
  --abstract_key=abstract \
  --data_path=textsum/data/data \
  --vocab_path=textsum/data/vocab \
  --log_root=textsum/log_root \
  --train_dir=textsum/log_root/train
*********************
bazel-bin/textsum/seq2seq_attention \
  --mode=train \
  --article_key=article \
  --abstract_key=abstract \
  --data_path=textsum/data/data \
  --vocab_path=textsum/data/toy_vocab \
  --log_root=textsum/log_root \
  --train_dir=textsum/log_root/train
---------------------------------------------
# Run the eval. Try to avoid running on the same machine as training.
bazel-bin/textsum/seq2seq_attention \
  --mode=eval \
  --article_key=article \
  --abstract_key=abstract \
  --data_path=textsum/data/data \
  --vocab_path=textsum/data/vocab \
  --log_root=textsum/log_root \
  --eval_dir=textsum/log_root/eval
----------------------------------------------
# Run the decode. Run it when the most is mostly converged.
bazel-bin/textsum/seq2seq_attention \
  --mode=decode \
  --article_key=article \
  --abstract_key=abstract \
  --data_path=textsum/data/data \
  --vocab_path=textsum/data/vocab \
  --log_root=textsum/log_root \
  --decode_dir=textsum/log_root/decode \
  --beam_size=8
*******************
bazel-bin/textsum/seq2seq_attention \
  --mode=decode \
  --article_key=article \
  --abstract_key=abstract \
  --data_path=textsum/data/one_article_bin \
  --vocab_path=textsum/data/vocab \
  --log_root=textsum/log_root \
  --decode_dir=textsum/log_root/decode \
  --beam_size=4
