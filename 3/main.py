from ast import literal_eval
import json

def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k


def read_lemmas():
    file = open('../2/lemmas.txt', 'r', encoding='utf-8')
    lines = file.readlines()
    lemmas = dict()
    for line in lines:
        key, value = line.split(" - ")
        parse = literal_eval(value)
        lemmas[key] = parse
    return lemmas


def get_words_from_files():
    words_list = []
    for i in range(1, 101):
        file = open(f'../2/file/{i}.txt', 'r', encoding='utf-8')
        words = set()
        lines = file.readlines()
        for line in lines:
            words.add(line.replace("\n", "").lower())
        words_list.append(list(words))
    return words_list


def find_indexes(lemmas, words_list):
    map = dict()
    for values in lemmas.values():
        key = get_key(lemmas, values)
        map[key] = []
        for value in values:
            for i in range(len(words_list)):
                if value in words_list[i]:
                    if not i + 1 in map[key]:
                        map[key].append(i + 1)
    return map


def write_to_file(map):
    str = json.dumps(map, separators=(',', ':'), sort_keys=False, indent=4, ensure_ascii=False)
    file = open(f'index.txt', 'w', encoding='utf-8')
    file.write(str)



lemmas = read_lemmas()
words_list = get_words_from_files()
map = find_indexes(lemmas, words_list)
write_to_file(map)


