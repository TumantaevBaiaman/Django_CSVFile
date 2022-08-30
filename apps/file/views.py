import csv
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from apps.file.file_data import data, test

import ru_core_news_lg

list_h = ['здравствуйте', 'меня зовут', 'до свидания', 'добрый день']
file_csv = ['dlg_id', 'line_n', 'role', 'text', 'insight']


def download_file(request):
    nlp = ru_core_news_lg.load()
    response = HttpResponse(content_type='text/csv')
    t = []
    name = ''
    context = {}
    if request.method == "POST":
        file = request.FILES['document']
        fs = FileSystemStorage()
        t_d = FileSystemStorage()
        fs.save(file.name, file)
        t_d.save('test.csv', file)
        name = file.name
        data_file = test(data(name))
        # print(data_file)
        for i in range(len(data_file)):
            print("-------------------------------")
            for n in data_file[str(i)]:
                list = []
                list.append(i)
                list.append(n['line_n'])
                list.append(n['role'])
                list.append(n['text'])

                text_data = n['text'].lower()
                doc = nlp(text_data)

                if (text_data.find(list_h[0]) != -1 and n['role'] == "manager") or text_data.find(list_h[2]) != -1 or (
                        n['role'] == "client" and text_data.find(list_h[1]) != -1) or (
                        text_data.find(list_h[3]) != -1 and n['role'] == "manager"):
                    list.append('True')
                else:
                    list.append('False')

                t.append(list)

                if (text_data.find(list_h[0]) != -1 and n['role'] == "manager") or (
                        text_data.find(list_h[3]) != -1 and n['role'] == "manager"):
                    hello = text_data

                if text_data.find(list_h[2]) != -1:
                    b = text_data

                if n['role'] == "client" and text_data.find(list_h[1]) != -1:

                    for p in doc.ents:
                        if p.label_ == "PER":
                            client = p.text

                    cl = text_data
                    f = text_data.split(' ')
                    index = f.index('компания')
                    company = f[index + 1]

                if n['role'] == "manager":
                    for l in doc.ents:

                        if l.label_ == "PER":
                            name = l.text

            info_context = {}
            tl = {0:'zero', 1:'one', 2:'two', 3:'three', 4:'four', 5:'five'}
            print("Менеджер №:", i + 1)
            info_context['id'] = str(i)
            print("Имя: ", name.title())
            if name:
                info_context['name'] = str(name.title())
            else:
                info_context['name'] = str('None')
            if hello:
                print(hello)
                info_context['he'] = str(hello)
            else:
                info_context['he'] = str("None")
            print("Клиент №:", i + 1)
            print("Имя: ", client.title())
            if client:
                info_context['name_c'] = str(client.title())
            else:
                info_context['name_c'] = str('None')
            if cl:
                print(cl)
                info_context['cl'] = str(cl)
            else:
                info_context['cl'] = str('None')
            if company:
                print("Компания: ", company.title())
                info_context['company'] = str(company.title())
            else:
                info_context['company'] = str('None')
            if b:
                print(b)
                info_context['b'] = str(b)
            else:
                info_context['b'] = str('None')
            context[tl[i]] = info_context
            print(context)

        with open('data.json', 'w') as fp:
            json.dump(context, fp)

        # write csv file
        with open('test_data.csv', 'w', encoding='UTF8') as file:
            writer = csv.writer(file)
            writer.writerow(file_csv)
            writer.writerows(t)

        # down csv file
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="file.csv"'},
        )
        writer = csv.writer(response)
        writer.writerow(file_csv)
        writer.writerows(t)
        return response

    return render(request, 'file/home.html')


def read_file(requests):
    nlp = ru_core_news_lg.load()
    t = []
    context = {}
    data_file = test(data('test.csv'))
    for i in range(len(data_file)):
        for n in data_file[str(i)]:
            list = []
            list.append(i)
            list.append(n['line_n'])
            list.append(n['role'])
            list.append(n['text'])

            text_data = n['text'].lower()
            doc = nlp(text_data)

            if (text_data.find(list_h[0]) != -1 and n['role'] == "manager") or text_data.find(list_h[2]) != -1 or (
                    n['role'] == "client" and text_data.find(list_h[1]) != -1) or (
                    text_data.find(list_h[3]) != -1 and n['role'] == "manager"):
                list.append('True')
            else:
                list.append('False')

            t.append(list)

            if (text_data.find(list_h[0]) != -1 and n['role'] == "manager") or (
                    text_data.find(list_h[3]) != -1 and n['role'] == "manager"):
                hello = text_data

            if text_data.find(list_h[2]) != -1:
                b = text_data

            if n['role'] == "client" and text_data.find(list_h[1]) != -1:

                for p in doc.ents:
                    if p.label_ == "PER":
                        client = p.text

                cl = text_data
                f = text_data.split(' ')
                index = f.index('компания')
                company = f[index + 1]

            if n['role'] == "manager":
                for l in doc.ents:

                    if l.label_ == "PER":
                        name = l.text

        info_context = {}
        tl = {0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five'}
        info_context['id'] = str(i)
        if name:
            info_context['name'] = str(name.title())
        else:
            info_context['name'] = str('None')
        if hello:
            info_context['he'] = str(hello)
        else:
            info_context['he'] = str("None")
        if client:
            info_context['name_c'] = str(client.title())
        else:
            info_context['name_c'] = str('None')
        if cl:
            info_context['cl'] = str(cl)
        else:
            info_context['cl'] = str('None')
        if company:
            info_context['company'] = str(company.title())
        else:
            info_context['company'] = str('None')
        if b:
            info_context['b'] = str(b)
        else:
            info_context['b'] = str('None')
        context[tl[i]] = info_context
    print(context)

    return render(requests, 'file/data.html', context=context)
