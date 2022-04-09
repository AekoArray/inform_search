import math

import json5

from scipy import spatial
import pymorphy2

morph = pymorphy2.MorphAnalyzer()


def get_indexes(tf_idf_data):
    all_data = set()
    for data in tf_idf_data:
        all_data.update(list(data.keys()))
    return list(set(all_data))


def read_tf_idf_file():
    with open("../4/tfidf.txt", encoding='utf-8') as file:
        return json5.load(file)


def create_matrix(all_files_words, tf_idf_data):
    page_count = 100
    all_count = len(all_files_words)
    matrix = [[0] * all_count for _ in range(page_count)]
    for idx, page in enumerate(tf_idf_data):
        # print(page)
        page_words = page.keys()
        for word in page_words:
            all_idx = all_files_words.index(word)
            matrix[idx][all_idx] = page[word]
    # print(sum(matrix[0]))
    return matrix


def get_tf_for_word(word, tokens):
    return tokens.count(word) / len(tokens)


def get_idf_for_word(word, tokens):
    file = open(f'../3/index.txt', 'r', encoding='utf-8')
    indexes = file.readlines()
    json = json5.loads("".join(indexes))
    return math.log(100 / len(json[word]))


def get_tf_idf_for_word(word, tokens):
    idf = get_idf_for_word(word, tokens)
    tf = get_tf_for_word(word, tokens)
    return tf * idf


def get_query_vector(query, all_files_words):
    normal_query = query.lower().split(" ")
    for i in range(len(normal_query)):
        normal_query[i] = morph.parse(normal_query[i])[0].normal_form
    vector = list()
    for word in all_files_words:
        if word in normal_query:
            vector.append(get_tf_idf_for_word(word, normal_query))
        else:
            vector.append(0)
    return vector


def get_distances(query_vector, matrix):
    distances = list()
    for i, vector in enumerate(matrix):
        distance = 1 - spatial.distance.cosine(query_vector, vector)
        distance = distance or 0
        distances.append(distance)
    return distances


def read_sites():
    with open("../1/index2.txt", 'r', encoding="utf-8") as outfile:
        return json5.load(outfile)


def get_page_url(idx):
    sites = read_sites()
    for i in sites:
        if i["file_name"] == f"{idx}.txt":
            return i["url"]
    return ""


def convert_distances_to_results(distances):
    results = list()
    for i, distance in enumerate(distances):
        url = get_page_url(i + 1)
        results.append({"url": url, "distance": distance})
    return sorted(results, key=lambda result: result["distance"])


query = "Прием заявок КФУ"
query1 = "спортивный комплекс кфу"
tf_idf_data = read_tf_idf_file()
all_files_words = get_indexes(tf_idf_data)
matrix = create_matrix(all_files_words, tf_idf_data)
query_vector = get_query_vector(query, all_files_words)
distances = get_distances(query_vector, matrix)
ans = convert_distances_to_results(distances)
str = json5.dumps(ans, separators=(',', ':'), sort_keys=False, indent=4, ensure_ascii=False)
file = open(f'index.txt', 'w', encoding='utf-8')
file.write(str)
print(len(ans))
