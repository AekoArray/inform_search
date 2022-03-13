import string
import re
import pymorphy2

morph = pymorphy2.MorphAnalyzer()
set = set()


def tokenize():
    for i in range(1, 101):
        file = open(f'C:/Домашки/информационный_поиск/1/files2/{i}.txt', 'r', encoding='utf-8')
        text = file.read()

        for p in string.punctuation:
            if p in text:
                text = text.replace(p, '')

        #remove numbers
        text = re.sub(r'[^\w\s]+|[\d]+', r'', text).strip()

        words = text.split()
        tokens = open(f'file/{i}.txt', 'w', encoding='utf-8')
        for word in words:
            try:
                tokens.write(word + "\n")
                set.add(word)
            except UnicodeEncodeError:
                pass
    return set


def lemmatize(words):
    obj = {}
    for word in words:
        word = word.lower()
        p = morph.parse(word)[0].normal_form
        if not p in obj.keys():
            obj[p] = [word]
        else:
            if not word in obj[p]:
                obj[p].append(word)
    lemmas = open(f'lemmas.txt', 'w', encoding='utf-8')
    for elem in obj.keys():
        lemmas.write(elem + " - " + str(obj[elem]) + "\n")


words = tokenize()
lemmatize(words)
