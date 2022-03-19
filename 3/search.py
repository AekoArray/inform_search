import json
import pymorphy2

morph = pymorphy2.MorphAnalyzer()


def read_indexes():
    file = open("index.txt", 'r', encoding='utf-8')
    lines = file.readlines()
    full_line = ' '.join(lines)
    indexes = json.loads(full_line)
    return indexes


logic_expressions = {
    "|": lambda x, y: list(set(x + y)),
    "&": lambda x, y: list(set(x) & set(y)),
    "!": lambda x, y: set(x) ^ set(y)
}

full_files = list(range(1, 101))


def search(indexes, query):
    query_list = query.split(" ")
    logical_operations = ["&", "|"]
    for i in range(len(query_list)):
        if not query_list[i] in logical_operations:
            if query_list[i][0] == "!":
                word = query_list[i][1:]
                p = morph.parse(word)[0].normal_form
                query_list[i] = list(logic_expressions["!"](full_files, indexes[p]))
            else:
                p = morph.parse(query_list[i])[0].normal_form
                query_list[i] = indexes[p]
    for elem in logical_operations:
        while elem in query_list:
            idx = query_list.index(elem)
            query_list[idx] = logic_expressions[elem](query_list[idx - 1], query_list[idx + 1])
            query_list.pop(idx + 1)
            query_list.pop(idx - 1)
    return query_list[0]


indexes = read_indexes()
arr = search(indexes, "спортивная & !образования | подразделением")

print(arr)
