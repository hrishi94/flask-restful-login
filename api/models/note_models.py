#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime

from flask import g

from api.conf.auth import auth, jwt
from api.database.database import db


class Notes(db.Model):

    # Generates default class name for table. For changing use
    # __tablename__ = 'users'

    # User id.
    id = db.Column(db.Integer, primary_key=True)

    # User name.
    username = db.Column(db.String(length=80))

    # User password.
    title = db.Column(db.String(length=80))

    # User email address.
    description = db.Column(db.String(length=250))

    # Creation time for user.
    created = db.Column(db.DateTime, default=datetime.utcnow)
	
	filename = db.Column(db.String(length=80),nullable=True)


    def __repr__(self):

        # This is only for representation how you want to see user information after query.
        return "<User(id='%s', name='%s', title='%s', description='%s', created='%s')>" % (
                      self.id, self.username, self.title, self.description, self.created)

