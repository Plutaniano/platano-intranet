def create():
    from .models import db, Usuario
    import csv
    f = open('app/assessores.csv')
    c = csv.DictReader(f, delimiter=';')

    for i in c:
        db.session.add(Usuario(**i))
        db.session.commit()