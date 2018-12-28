#!/usr/bin/python
# -*- coding: utf-8 -*-
DEBUG = True
DEBUG_TB_INTERCEPT_REDIRECTS = False

SOCIAL_AUTH_LOGIN_URL = '/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/done/'
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
SOCIAL_AUTH_USER_MODEL = 'pacifica.auth.orm.User'
SOCIAL_AUTH_STORAGE = 'social_flask_peewee.models.FlaskStorage'
SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
    'social_core.backends.orcid.ORCIDOAuth2',
    'social_core.backends.keycloak.KeycloakOAuth2',
)

SOCIAL_AUTH_TRAILING_SLASH = True

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'pacifica.auth.pipeline.require_email',
    'pacifica.auth.pipeline.debug_social_user',
    'social_core.pipeline.user.create_user',
    'pacifica.auth.pipeline.debug_social_user',
    'social_core.pipeline.social_auth.associate_user',
    'pacifica.auth.pipeline.debug_social_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'pacifica.auth.pipeline.debug_social_user',
    'social_core.pipeline.user.user_details',
    'pacifica.auth.pipeline.send_user'
)
