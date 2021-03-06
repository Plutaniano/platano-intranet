import datetime
import csv

from unidecode import unidecode

from ..models import db


def query_to_csv(queries, tabela: db.Model, user: str) -> str:
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