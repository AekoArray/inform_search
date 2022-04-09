import pymorphy2
import json5
import math

morph = pymorphy2.MorphAnalyzer()

def compute_tf(words):
    dictionary = dict()
    for word in words:
        if not word in dictionary.keys():
            dictionary[word] = 1
        else:
            dictionary[word] += 1
    for lemma in dictionary.keys():
        dictionary[lemma] /= len(words)
    return dictionary


def compute_idf(json):
    dictionary = dict()
    for index in json.keys():
        dictionary[index] = math.log(100/len(json[index]))
    return dictionary


def compute_tfidf(tf, idf):
    dictionary = dict()
    for w in tf.keys():
        dictionary[w] = tf[w] * idf[w]
    return dictionary


file = open(f'../3/index.txt', 'r', encoding='utf-8')
indexes = file.readlines()
json = json5.loads("".join(indexes))
idf = compute_idf(json)
tfidf = []
all_tf = []
for i in range(1, 101):
    file = open(f'../2/file/{i}.txt', 'r', encoding='utf-8')
    lines = file.readlines()
    words = []
    for line in lines:
        word = line.lower().replace('\n', '')
        p = morph.parse(word)[0].normal_form
        words.append(p)
    tf = compute_tf(words)
    all_tf.append(tf)
    tfidf.append(compute_tfidf(tf,idf))
str = json5.dumps(tfidf, separators=(',', ':'), sort_keys=False, indent=4, ensure_ascii=False)
file = open(f'tfidf.txt', 'w', encoding='utf-8')
file.write(str)
str1 = json5.dumps(idf, separators=(',', ':'), sort_keys=False, indent=4, ensure_ascii=False)
file = open(f'idf.txt', 'w', encoding='utf-8')
file.write(str1)
str2 = json5.dumps(all_tf, separators=(',', ':'), sort_keys=False, indent=4, ensure_ascii=False)
file = open(f'tf.txt', 'w', encoding='utf-8')
file.write(str2)
