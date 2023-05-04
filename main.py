import sqlalchemy as sq
import json
from sqlalchemy.orm import sessionmaker

from models import create_table, Shop, Publisher, Stock, Sale, Book

DSN = 'postgresql://postgres:************@localhost:5432/netology_db'

engine = sq.create_engine(DSN)

create_table(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json') as td:
    data = json.load(td)
for rec in data:
    model = {'publisher': Publisher,
    'shop': Shop,
    'book': Book,
    'stock': Stock,
    'sale': Sale,} [rec.get('model')]
    session.add(model(id=rec.get('pk'), **rec.get('fields')))



session.commit()


c = input('Введите Id или имя издателя: ')
if c.isnumeric():
    subq = session.query(Stock).join(Book.id_book).join(Book.publisher).filter(Publisher.id == c).subquery()
    for t in session.query(Shop).join(Stock.shop).join (subq, Shop.id == subq.c.id_shop).all():
        print(t)
else:
    subq = session.query(Stock).join(Book.id_book).join(Book.publisher).filter(Publisher.name == c).subquery()
    for t in session.query(Shop).join(Stock.shop).join(subq, Shop.id == subq.c.id_shop).all():
        print(t)

session.close()