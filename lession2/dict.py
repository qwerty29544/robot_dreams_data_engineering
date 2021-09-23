py_dict = {"a": 1, "b": 2, 'c': 2, 'd': [1, 2]}

print(py_dict['a'])

# По ключам
for x in py_dict:
    print(x)

py_dict['c'] = 3

print(py_dict)