import os
import MeCab
import pandas as pd
import csv

pre_folder_path = "./dataset/pre"
author_word_count = {}

def scan_file(path) -> list[str]:
    try:
        with os.scandir(path) as entries:
            items = [entry.name for entry in entries if entry.is_file()]
        return items
    except Exception as e:
        print(e)

def read_file(path):
    f = open(path, encoding="shift_jis")
    return f.read()

stop_df = pd.read_csv('./output/stopword_n_None.csv')

def skip(word) -> bool:
    if word == '':
        return True
    return stop_df['label'].isin([word]).any()

tagger = MeCab.Tagger()

author_dict = {'pre': []}
line_dict = []

print(stop_df['label'])
word_count = {}
files = scan_file(f'{pre_folder_path}')
for file in files:
    text = read_file(f'{pre_folder_path}/{file}')

    node = tagger.parseToNode(text)

    while node:
        word = node.surface
        if not skip(word):
            line_dict.append(word)
        if word == '。':
            author_dict['pre'].append(line_dict)
            line_dict = []
        
        node = node.next
word_count = sorted(word_count.items(), key=lambda x:x[1], reverse=True)
author_word_count['pre'] = word_count

print(author_dict)

with open('./pre_corpus.csv', mode='w', encoding='utf-8') as f:
    writer = csv.writer(f, lineterminator='\n')

    for author, lines in author_dict.items():
        for line in lines:
            text = ' '.join(line)
            writer.writerow([author, text])