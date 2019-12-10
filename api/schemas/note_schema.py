#!/usr/bin/python
# -*- coding: utf-8 -*-

from marshmallow import Schema, fields


class BaseNoteSchema(Schema):

    """
        Base user schema returns all fields but this was not used in user handlers.
    """

    # Schema parameters.

    id = fields.Int(dump_only=True)
    username = fields.Str()
    title = fields.Str()
    description = fields.Str()
    created = fields.Str()
