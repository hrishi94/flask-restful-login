#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from datetime import datetime

from flask import g, request
from flask_restful import Resource

import api.error.errors as error
from api.conf.auth import auth, refresh_jwt,get_username
from api.database.database import db
from api.models.note_models import Notes
from api.models.user_models import User
from api.roles import role_required
from api.schemas.note_schema import BaseNoteSchema


class NotesClass(Resource):
    @staticmethod
    @auth.login_required
    def post():

        try:
            # Get username, password and email.
            title, description = request.json.get('title').strip(), \
                                        request.json.get('description').strip()
            
            header_token = request.headers.get('Authorization')
            print(get_username(header_token[7:]))
			username = get_username(header_token[7:]) 



        except Exception as why:
            print why
            # Log input strip or etc. errors.
            logging.info("Couldn't add the note" + str(why))

            # Return invalid input error.
            return error.INVALID_INPUT_422

        # Check if any field is none.
        if username is None or title is None or description is None:
            return error.INVALID_INPUT_422

        # Create a new user.
        note = Notes(username=username, title=title, description=description)

        # Add user to session.
        db.session.add(note)

        # Commit session.
        db.session.commit()

        # Return success if registration is completed.
        return {'status': 'note added.'}
    
    @auth.login_required
    def get(self):
        try:
            username = request.args.get('username')
            notes=Notes.query\
                .filter(Notes.username==username)\
                .all()
            notes_schema = BaseNoteSchema(many=True)

            # Get json data
            data, errors = notes_schema.dump(notes)

            # Return json data from db.
            return data

        except Exception as why:

            # Log the error.
            logging.error(why)

            # Return error.
            return error.INVALID_INPUT_422

class NotesData(Resource):
    @auth.login_required
    @role_required.permission(2)
    def get(self):
        try:

            # Get usernames.
            usernames = [] if request.args.get('usernames') is None else request.args.get('usernames').split(',')

            # Get emails.
            description = [] if request.args.get('emails') is None else request.args.get('emails').split(',')

            # Get start date.
            start_date = datetime.strptime(request.args.get('start_date'), '%d.%m.%Y')

            # Get end date.
            end_date = datetime.strptime(request.args.get('end_date'), '%d.%m.%Y')

            print(usernames, emails, start_date, end_date)

            # Filter users by usernames, emails and range of date.
            users = Notes.query\
                .filter(Notes.username.in_(usernames))\
                .filter(Notes.email.in_(emails))\
                .filter(Notes.created.between(start_date, end_date))\
                .all()

            # Create user schema for serializing.
            user_schema = UserSchema(many=True)

            # Get json data
            data, errors = user_schema.dump(users)

            # Return json data from db.
            return data

        except Exception as why:

            # Log the error.
            logging.error(why)

            # Return error.
            return error.INVALID_INPUT_422


# auth.login_required: Auth is necessary for this handler.
# role_required.permission: Role required user=0, admin=1 and super admin=2.

class DataAdminRequired(Resource):
    @auth.login_required
    @role_required.permission(1)
    def get(self):

        return "Test admin data OK."


class AddUser(Resource):
    @auth.login_required
    @role_required.permission(2)
    def get(self):

        return "OK"


class DataUserRequired(Resource):

    @auth.login_required
    def get(self):

        return "Test user data OK."
