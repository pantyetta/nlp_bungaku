import csv
import pickle

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

dataset_file_name = './corpus.csv'
texts, label_ids = [], []

# データの読み込み
with open(dataset_file_name, mode='r', encoding='utf-8') as f:
    data = list(csv.reader(f))

for counter, row in enumerate(data):
    label = row[0]
    word_list = row[1].split(' ')
    label_ids.append(label)
    texts.append(word_list)

# データの分割
X_train_texts, X_test_texts, y_train, y_text = train_test_split(texts, label_ids, test_size=.2, random_state=42)

