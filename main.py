import csv
import collections

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import gensim
from gensim import models
import pandas as pd

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
X_train_texts, X_test_texts, y_train, y_test = train_test_split(texts, label_ids, test_size=.2, random_state=42)

# 辞書の作成
dictionary = gensim.corpora.Dictionary(X_train_texts)
# 辞書を用いてBoW形式に文章を行列化します
corpus = [dictionary.doc2bow(text) for text in X_train_texts]

# BoW形式で作成したcorpusをtfidfを用いて重み付けします
tfidf_model = models.TfidfModel(corpus)
tfidf_corpus = tfidf_model[corpus]

num_words = len(dictionary)
X_train_tfidf = gensim.matutils.corpus2dense(tfidf_corpus, num_terms=num_words).T


# testのテキストデータから、tfidfで重み付けされた単語文書行列を作成します

# 辞書を用いてBoW形式に文章を行列化します
corpus = [dictionary.doc2bow(text) for text in X_test_texts]
# BoW形式で作成したcorpusをtfidfを用いて重み付けします
tfidf_corpus = tfidf_model[corpus]

num_words = len(dictionary)
X_test_tfidf = gensim.matutils.corpus2dense(tfidf_corpus, num_terms=num_words).T

# trainデータを用いて分類器を構築します
clf = LogisticRegression(C=1, penalty='l2')
clf.fit(X_train_tfidf, y_train)

y_pred = clf.predict(X_test_tfidf)

print('\n====================== total ========================\n\n', collections.Counter(y_pred), '\n\n=====================================================\n')

print(classification_report(y_test, y_pred, digits=5))
cm = confusion_matrix(y_test, y_pred)
df_cm = pd.DataFrame(cm, index=['Actual A', 'Actual B', 'actual C', 'Actual D', 'actual E'], columns=['pre A', 'pre B', 'pre C', 'pre D', 'pre E'])
print(df_cm)