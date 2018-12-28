#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Peewee ORM Module."""
from datetime import datetime
from peewee import Model, Proxy, CharField, BooleanField, DateTimeField
from flask_login import UserMixin

database_proxy = Proxy()


class BaseModel(Model):
    """Base Peewee model class."""

    class Meta:
        """Peewe meta class."""

        database = database_proxy


class User(BaseModel, UserMixin):
    """User model class."""

    username = CharField(unique=True)
    first_name = CharField(null=True)
    last_name = CharField(null=True)
    middle_initial = CharField(null=True)
    email = CharField(null=True)
    active = BooleanField(default=True)
    join_date = DateTimeField(default=datetime.now)

    class Meta:
        """Meta class for user."""

        order_by = ('username',)
