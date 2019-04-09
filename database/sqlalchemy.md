
# SQLAlchemy

**database_setup.py**

```python
#!/usr/bin/python2
# -*- coding: utf-8 -*-
"""
The classes which are mapped to database entries
"""
import os

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()


class User(Base):
    """
    Registered user information is stored in db
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    picture = Column(String(250))
    email = Column(String(250))

    @property
    def serialize(self):
        return {
           'id': self.id,
           'name': self.name,
           'email': self.email,
           'picture': self.picture
        }


class Catalog(Base):
    """
    Catalog information
    """
    __tablename__ = 'catalog'

    name = Column(String(80), nullable=False, unique=True)
    id = Column(Integer, primary_key=True)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
        }


class CatalogItem(Base):
    """
    Catalog item
    """
    __tablename__ = 'catalog_item'

    name = Column(String(80), nullable=False, unique=True)
    id = Column(Integer, primary_key=True)
    creation_date = Column(DateTime, nullable=False)
    description = Column(String(250))
    catalog_id = Column(Integer, ForeignKey('catalog.id'))
    catalog = relationship(Catalog)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'creation_date': self.creation_date,
            'description': self.description,
            'catalog_id': self.catalog_id,
            'user_id': self.user_id
        }


current_dir = os.path.dirname(os.path.abspath(__file__))
database_path = 'sqlite:///{}/catalog.db?check_same_thread=False'\
    .format(current_dir)
engine = create_engine(database_path)
Base.metadata.create_all(engine)
```

**database.py**

```python
# -*- coding: utf-8 -*-
"""
Helper functions to create, get, edit and delete database entries
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from database_setup import Base, User, Catalog, CatalogItem, database_path

current_dir = os.path.dirname(os.path.abspath(__file__))

engine = create_engine(database_path)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()


def get_catalogs():
    return session.query(Catalog).all()


def get_catalog(catalog_name):
    return session\
        .query(Catalog)\
        .filter_by(name=catalog_name)\
        .one()


def get_items(catalog_id=None):
    if catalog_id is not None:
        return session.query(CatalogItem)\
            .filter_by(catalog_id=catalog_id)\
            .all()
    else:
        return session.query(CatalogItem).all()


def get_item(catalog_id, item_name):
    return session.query(CatalogItem)\
        .filter_by(catalog_id=catalog_id, name=item_name)\
        .one()


def add_catalog_item(creation_date,
                     catalog_id,
                     name,
                     description,
                     user_id):
    catalog_item = CatalogItem(creation_date=creation_date,
                               catalog_id=catalog_id,
                               name=name,
                               description=description,
                               user_id=user_id)
    session.add(catalog_item)
    session.commit()


def edit_catalog_item(catalog_item):
    session.add(catalog_item)
    session.commit()


def delete_catalog_item(catalog_item):
    session.delete(catalog_item)
    session.commit()


def create_user(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User)\
        .filter_by(email=login_session['email'])\
        .one()
    return user.id


def get_user_info(user_id):
    try:
        return session.query(User)\
            .filter_by(id=user_id)\
            .one()
    except NoResultFound:
        return None


def get_user_id(email):
    try:
        return session.query(User)\
            .filter_by(email=email)\
            .one()\
            .id
    except NoResultFound:
        return None
```
