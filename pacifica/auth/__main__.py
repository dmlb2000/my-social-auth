#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Pacifica Auth main methods."""
from flask_script import Server, Manager, Shell
from social_flask_peewee.models import FlaskStorage
from .rest import app
from .orm import User

manager = Manager(app)
manager.add_command('runserver', Server())
manager.add_command('shell', Shell(make_context=lambda: {
    'app': app
}))


@manager.command
def syncdb():
    models = [
        User,
        FlaskStorage.user,
        FlaskStorage.nonce,
        FlaskStorage.association,
        FlaskStorage.code,
        FlaskStorage.partial
    ]
    for model in models:
        model.create_table(True)


def main():
    return manager.run()
