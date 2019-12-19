#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
from datetime import datetime

from flask import g, request
from flask_restful import Resource

import api.error.errors as error
from api.conf.auth import auth, refresh_jwt
from api.database.database import db
from api.roles import role_required


class FileClass(Resource):

    def CreateNewDir():
        os.makedir("files")
	
    def allowed_file(filename):
		ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])
		return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    #@staticmethod
    #@auth.login_required
    def post(self):

        try:
            # Get username, password and email.
                        if 'file' not in request.files.to_dict():
		        	return error.INVALID_INPUT_422
			file = request.files.to_dict()['file']
        # if user does not select file, browser also
        # submit an empty part without filename
			if file.filename == '':
				return rerror.INVALID_INPUT_422
                        if file :#and allowed_file(file.filename):
				filename = file.filename
				#UPLOAD_FOLDER = './files/'
				#CreateNewDir()
				file.save(filename)
	except Exception as why:

            # Log input strip or etc. errors.
                        logging.info("Couldn't add the file" + str(why))

            # Return invalid input error.
                        return error.INVALID_INPUT_422

        # Check if any field is none.

        # Commit session.

        # Return success if registration is completed.
        return {'status': 'file added.'}
    
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
