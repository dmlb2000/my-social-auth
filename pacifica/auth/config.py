#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Configuration reading and validation module."""
from os import getenv
try:
    from ConfigParser import SafeConfigParser
except ImportError:  # pragma: no cover python 2 vs 3 issue
    from configparser import ConfigParser as SafeConfigParser
from pacifica.auth.globals import CONFIG_FILE


def get_config():
    """Return the ConfigParser object with defaults set."""
    configparser = SafeConfigParser()
    configparser.add_section('auth')
    configparser.set(
        'auth', 'required_provider',
        getenv('AUTH_REQUIRED_PROVIDER', 'orcid')
    )
    configparser.set(
        'auth', 'metadata_url',
        getenv('AUTH_METADATA_URL', 'http://127.0.0.1:8121/users')
    )
    configparser.set(
        'auth', 'default_provider',
        getenv('AUTH_DEFAULT_PROVIDER', '')
    )
    configparser.set(
        'auth', 'cookie_name',
        getenv('AUTH_COOKIE_NAME', 'pacifica_auth')
    )
    configparser.set(
        'auth', 'cookie_domain',
        getenv('AUTH_COOKIE_DOMAIN', 'localhost.localdomain')
    )
    configparser.set(
        'auth', 'redirect_cookie_name',
        getenv('AUTH_REDIRECT_COOKIE_NAME', 'redirect_url')
    )
    configparser.set(
        'auth', 'private_key',
        getenv('AUTH_PRIVATE_KEY', 'private.key.pem')
    )
    configparser.add_section('database')
    configparser.set(
        'database', 'peewee_url',
        getenv('PEEWEE_URL', 'sqliteext:///db.sqlite3')
    )
    configparser.add_section('secret')
    configparser.set(
        'secret', 'key',
        getenv('SECRET_KEY', 'some-random-key')
    )
    configparser.add_section('session')
    configparser.set(
        'session', 'protection',
        getenv('SESSION_PROTECTION', 'strong')
    )
    configparser.set(
        'session', 'cookie_name',
        getenv('SESSION_COOKIE_NAME', 'psa_session')
    )
    configparser.set(
        'session', 'cookie_domain',
        getenv('SESSION_COOKIE_DOMAIN', 'localhost.localdomain')
    )
    configparser.add_section('social_auth')
    configparser.set(
        'social_auth', 'orcid_key',
        getenv('SOCIAL_AUTH_ORCID_KEY', 'example')
    )
    configparser.set(
        'social_auth', 'orcid_secret',
        getenv('SOCIAL_AUTH_ORCID_SECRET', 'example')
    )
    configparser.set(
        'social_auth', 'keycloak_key',
        getenv('SOCIAL_AUTH_KEYCLOAK_KEY', 'example')
    )
    configparser.set(
        'social_auth', 'keycloak_scope',
        getenv('SOCIAL_AUTH_KEYCLOAK_SCOPE', 'example')
    )
    configparser.set(
        'social_auth', 'keycloak_secret',
        getenv('SOCIAL_AUTH_KEYCLOAK_SECRET',
               '1234abcd-1234-abcd-1234-abcd1234adcd')
    )
    configparser.set(
        'social_auth', 'keycloak_public_key',
        getenv('SOCIAL_AUTH_KEYCLOAK_PUBLIC_KEY',
               'pempublickeythatis2048bitsinbase64andhaseg392characters')
    )
    configparser.set(
        'social_auth', 'keycloak_authorization_url',
        getenv('SOCIAL_AUTH_KEYCLOAK_AUTHORIZATION_URL',
               'https://sso.example.com/auth/realms/example/protocol/openid-connect/auth')
    )
    configparser.set(
        'social_auth', 'keycloak_access_token_url',
        getenv('SOCIAL_AUTH_KEYCLOAK_ACCESS_TOKEN_URL',
               'https://sso.example.com/auth/realms/example/protocol/openid-connect/token')
    )
    configparser.read(CONFIG_FILE)
    return configparser
