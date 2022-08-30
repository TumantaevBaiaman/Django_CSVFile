import csv
from django.conf import settings
import os


def data(file):
    base_dir = settings.MEDIA_ROOT
    my_file = os.path.join(base_dir, str(file))
    list_f = []
    with open(my_file, 'r', encoding='UTF8') as file:
        reader = csv.DictReader(file, skipinitialspace=True)

        for l in reader:
            list_f.append(l)
    return list_f


def test(info):
    table = info
    list = {}
    for i in table:
        list[i['dlg_id']] = []
    for i in table:
        list[i['dlg_id']].append({'line_n': i['line_n'], 'role': i['role'], 'text': i['text']})
    return list