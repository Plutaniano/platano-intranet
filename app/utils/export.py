import datetime
from flask_sqlalchemy import BaseQuery
from ..models import db
import csv
from unidecode import unidecode


def query_to_csv(queries: BaseQuery, tabela: db.Model, user: str) -> str:
    queries = list(queries)
    filename = f'/tmp/{user}_{datetime.datetime.now().isoformat()}.csv'

    with open(filename, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        col_names = [i[0].name for i in tabela.showable_columns]
        writer.writerow(col_names)

        cols = [i[0] for i in tabela.showable_columns]
        for q in queries:
            writer.writerow(q)

    return unidecode(open(filename, encoding='utf-8').read())