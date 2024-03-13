import sqlalchemy as sq
import json
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=60), unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)

    def __str__(self):
        return f'{self.title}'


class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=50), unique=True)

    books = relationship(Book, backref='publisher')

    def __str__(self):
        return f'{self.name}'

class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=50), unique=True)

    def __str__(self):
        return f'{self.name}'


class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer)

    book = relationship(Book, backref="stock")
    shop = relationship(Shop, backref="stock")

    def __str__(self):
        return f'{self.books_stock} | {self.shops_stock} | {self.count}'


class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float)
    date_sale = sq.Column(sq.DateTime)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)
    count = sq.Column(sq.Integer)

    sale = relationship(Stock, backref="sale")
    def __str__(self):
        return f'{self.price} | {self.date_sale} | {self.count} {self.sale}'



# удаление
def drop_tables(ses, engine):
    Base.metadata.drop_all(engine)
    ses.commit()
    return print('Таблицы удалены')

# создание таблиц
def create_tables(ses, engine):
    Base.metadata.create_all(engine)
    ses.commit()
    return print('Таблицы созданы')

# заполнение таблиц данными
def insert_table(ses, path):
  with open(path) as f:
    json_data = json.load(f)
  models = {
    'publisher': Publisher,
    'book': Book,
    'shop': Shop,
    'stock': Stock,
    'sale': Sale
  }
  for line in json_data:
    model = models.get(line.get('model'))
    ses.add(model(id=line.get('pk'), **line.get('fields')))
  ses.commit()
  return print('Таблицы заполнены')

# Поиск магазина по названию или id издателя
def search_shop(ses):
  pub_name = None
  pub_id = None
  pub = input('Введите название издательства или его ID: ')
  if pub.isdigit():
    pub_id = pub
  else:
    pub_name = pub
  print(f'Издательство продается в магазинах:')
  for i in ses.query(Shop).join(Stock).join(Book).join(Publisher).\
          filter((Publisher.name == pub_name) | (Publisher.id == pub_id)).all():
    print(i)




def get_shops(session):
    res = input('Введите ID или имя издателя: ')
    query = session.query(
        Book.title, Shop.name, Sale.price, Sale.date_sale,
    ).select_from(Shop).join(Stock).join(Book).join(Publisher).join(Sale)
    if res.isdigit():
        query = query.filter(Publisher.id == res).all()
    else:
        query = query.filter(Publisher.name == res).all()
    for title, name, price, date_sale in query:
        print(f"{title: <20} | {name: <15} | {price: <5} | {date_sale.strftime('%d-%m-%Y')}")