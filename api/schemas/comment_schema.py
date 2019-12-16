#!/usr/bin/python
# -*- coding: utf-8 -*-

from marshmallow import Schema, fields


class BaseCommentSchema(Schema):

    """
        Base user schema returns all fields but this was not used in user handlers.
    """

    # Schema parameters.

    id = fields.Int(dump_only=True)
    username = fields.Str()
    noteid = fields.Int()
    description = fields.Str()
    created = fields.Str()
