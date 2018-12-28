#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Cookie module for creating user cookie."""
from base64 import urlsafe_b64encode
import json
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from .config import get_config


def generate_json_obj(user_obj):
    """Create the json serializable object from user."""
    return {
        'id': user_obj.id,
        'username': user_obj.username,
        'email': user_obj.email
    }


def cookie_data(user_obj):
    """Create the user cookie."""
    digest = SHA256.new()
    b64_data = urlsafe_b64encode(
        json.dumps(generate_json_obj(user_obj)).encode('utf8')
    )
    digest.update(b64_data)
    private_key = False
    with open(get_config().get('auth', 'private_key'), 'r') as key_fd:
        private_key = RSA.importKey(key_fd.read())
    signer = PKCS1_v1_5.new(private_key)
    sig = signer.sign(digest)
    b64_sig = urlsafe_b64encode(sig)
    return '{}.{}'.format(b64_data.decode('utf8'), b64_sig.decode('utf8'))
