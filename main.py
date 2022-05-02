import collections
import datetime
from pprint import pprint

import pandas
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape


wines_data = pandas.read_excel('wine3.xlsx',
                               na_values='None',
                               keep_default_na=False
                               ).to_dict(orient='record')
wines = collections.defaultdict(list)
for wine in wines_data:
    wines[wine['Категория']].append(wine)
    if wine['Сорт'] == 'None':
        print(wine['Сорт'])


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('index_template.html')

rendered_page = template.render(
    years=str(datetime.datetime.now().year - 1920),
    all_wines=wines
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()

