#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from datetime import datetime

from flask import g, request
from flask_restful import Resource

import api.error.errors as error
from api.conf.auth import auth, refresh_jwt
from api.database.database import db
from api.models.comment_models import Comments
from api.roles import role_required
from api.schemas.comment_schema import BaseCommentSchema


class CommentsClass(Resource):
    @staticmethod
    @auth.login_required
    def post():

        try:
            # Get username, password and email.
            username, noteid, description = request.json.get('username').strip(), request.json.get('noteid').strip(), \
                                        request.json.get('description').strip()
        except Exception as why:

            # Log input strip or etc. errors.
            logging.info("Couldn't add the comment" + str(why))

            # Return invalid input error.
            return error.INVALID_INPUT_422

        # Check if any field is none.
        if username is None or noteid is None or description is None:
            return error.INVALID_INPUT_422

        # Create a new user.
        comment = Comments(username=username, noteid=noteid, description=description)

        # Add user to session.
        db.session.add(comment)

        # Commit session.
        db.session.commit()

        # Return success if registration is completed.
        return {'status': 'comment added.'}
    
    @auth.login_required
    def get(self):
        try:
            noteid = request.args.get('noteid')
            comments=Comments.query\
                .filter(Comments.noteid==noteid)\
                .all()
            comments_schema = BaseCommentSchema(many=True)

            # Get json data
            data, errors = comments_schema.dump(comments)

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
