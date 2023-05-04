import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), nullable=False)

    book = relationship("Book", back_populates='publisher')
    def __str__(self):
        return f'Издатель {self.id}: {self.name}'


class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=40), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)

    publisher = relationship(Publisher, back_populates='book')

    def __str__(self):
        return f'Книга {self.id}: ({self.title}, {self.id_publisher})'


class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), nullable=False)

    stock = relationship("Stock", back_populates='shop')
    def __str__(self):
        return f'Магазин {self.id}: {self.name}'



class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    Book = relationship(Book, backref='id_book')
    shop = relationship(Shop, back_populates='stock')

    def __str__(self):
        return f'Склад {self.id}: {self.id_book}, {self.id_shop}, {self.count}'

class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.String(length=40), nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    Stock = relationship(Stock, backref='sale')

    def __str__(self):
        return f'Продажи {self.id}: {self.price}, {self.date_sale}, {self.id_stock}, {self.count}'


def create_table(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
