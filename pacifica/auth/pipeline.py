#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Pipeline functions for social auth."""
from pprint import pprint
from flask import redirect
import requests
from social_core.pipeline.partial import partial
from .config import get_config


def debug_social_user(response, details, *args, **kwargs):
    """Print stuff about social and user."""
    print('=' * 80)
    pprint(response)
    print('-' * 80)
    pprint(details)
    print('-' * 80)
    pprint(args)
    print('-' * 80)
    pprint(kwargs)
    print('=' * 80)


def auth_required(backend, uid, *args, **kwargs):
    """Check required auth provider see if user has that association."""
    req_provider = get_config().get('auth', 'required_provider')
    provider = backend.name
    print('Checking {} and {}'.format(provider, req_provider))
    if provider != req_provider:
        social = backend.strategy.storage.user.get_social_auth(
            req_provider, uid)
        print('Checking {} for {}'.format(social, uid))
        if not social:
            return redirect('/login/{}/'.format(req_provider), code=302)


def auth_metadata_user_map(auth_user_obj):
    """Convert an Auth user object to metadata user object."""
    return {
        '_id': auth_user_obj.id,
        'email_address': auth_user_obj.email,
        'network_id': auth_user_obj.username,
        'last_name': auth_user_obj.last_name,
        'first_name': auth_user_obj.first_name,
        'middle_initial': auth_user_obj.middle_initial
    }


@partial
def send_user(strategy, details, user=None, is_new=False, *args, **kwargs):
    """Send the user details to configured addresses."""
    if is_new:
        method = requests.put
        args = ''
    else:
        method = requests.post
        args = '?_id={}'.format(user.id)
    resp = method(
        '{}{}'.format(get_config().get('auth', 'metadata_url'), args),
        json=auth_metadata_user_map(user)
    )
    assert resp.status_code == 200


@partial
def require_email(strategy, details, user=None, is_new=False, *args, **kwargs):
    if kwargs.get('ajax') or user and user.email:
        return
    elif is_new and not details.get('email'):
        email = strategy.request_data().get('email')
        if email:
            details['email'] = email
        else:
            current_partial = kwargs.get('current_partial')
            return strategy.redirect(
                '/email?partial_token={0}'.format(current_partial.token)
            )
