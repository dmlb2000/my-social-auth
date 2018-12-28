#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Flask rest API."""
from os.path import dirname, join, abspath
from playhouse.db_url import connect
from flask import Flask, g, make_response
from flask import render_template, redirect, request
from flask_login import login_required, logout_user
from flask_login import LoginManager, current_user
from social_core.backends.utils import load_backends
from social_flask.utils import load_strategy
from social_flask.routes import social_auth
from social_flask.template_filters import backends
from social_flask_peewee.models import init_social
import pacifica.auth.filters as filters
from .orm import database_proxy, User
from .config import get_config
from .cookie import cookie_data


def config_to_settings():
    """Build a flask settings object from the config."""
    class Settings():
        pass
    ret = Settings()
    for section in ['social_auth', 'session', 'secret']:
        for opt in get_config().options(section):
            setattr(ret, '{}_{}'.format(section.upper(), opt.upper()),
                    get_config().get(section, opt))
    ret.SOCIAL_AUTH_KEYCLOAK_SCOPE = ret.SOCIAL_AUTH_KEYCLOAK_SCOPE.split(',')
    return ret


BASE_DIR = dirname(abspath(__file__))

app = Flask(
    __name__,
    template_folder=join(BASE_DIR, 'templates')
)
app.config.from_object('pacifica.auth.settings')
app.config.from_object(config_to_settings())

database = connect(get_config().get('database', 'peewee_url'))
database_proxy.initialize(database)

app.register_blueprint(social_auth)
init_social(app, database)

login_manager = LoginManager()
login_manager.login_view = 'main'
login_manager.login_message = ''
login_manager.init_app(app)


@app.route('/')
def main():
    force_provider = get_config().get('auth', 'default_provider')
    if force_provider:
        return redirect('/login/{}/'.format(force_provider), code=302)
    return render_template('home.html')


@login_required
@app.route('/done/')
def done():
    redirect_cookie_name = get_config().get('auth', 'redirect_cookie_name')
    redirect_url = request.cookies.get(redirect_cookie_name, False)
    if redirect_url:
        resp = make_response(redirect(redirect_url, code=302))
    else:
        resp = make_response(render_template('home.html'))
    cookie_name = get_config().get('auth', 'cookie_name')
    if not request.cookies.get(cookie_name):
        resp.set_cookie(
            cookie_name, cookie_data(g.user),
            domain=get_config().get('auth', 'cookie_domain')
        )
    return resp


@app.route('/email')
def require_email():
    strategy = load_strategy()
    partial_token = request.args.get('partial_token')
    partial = strategy.partial_load(partial_token)
    return render_template(
        'home.html',
        email_required=True,
        partial_backend_name=partial.backend,
        partial_token=partial_token
    )


@login_required
@app.route('/logout/')
def logout():
    """Logout view"""
    logout_user()
    return redirect('/')


@login_manager.user_loader
def load_user(userid):
    try:
        return User.get(User.id == userid)
    except User.DoesNotExist:
        pass


@app.before_request
def global_user():
    # evaluate proxy value
    g.user = current_user._get_current_object()


@app.context_processor
def inject_user():
    try:
        return {'user': g.user}
    except AttributeError:
        return {'user': None}


def is_authenticated(user):
    if callable(user.is_authenticated):
        return user.is_authenticated()
    else:
        return user.is_authenticated


def associations(user, strategy):
    user_associations = strategy.storage.user.get_social_auth_for_user(user)
    if hasattr(user_associations, 'all'):
        user_associations = user_associations.all()
    return list(user_associations)


def common_context(authentication_backends, strategy, user=None, plus_id=None, **extra):
    """Common view context"""
    context = {
        'user': user,
        'available_backends': load_backends(authentication_backends),
        'associated': {}
    }

    if user and is_authenticated(user):
        context['associated'] = dict((association.provider, association)
                                     for association in associations(user, strategy))
    return dict(context, **extra)


@app.context_processor
def load_common_context():
    return common_context(
        app.config['SOCIAL_AUTH_AUTHENTICATION_BACKENDS'],
        load_strategy(),
        getattr(g, 'user', None)
    )


def url_for(name, **kwargs):
    if name == 'social:begin':
        url = '/login/{backend}/'
    elif name == 'social:complete':
        url = '/complete/{backend}/'
    elif name == 'social:disconnect':
        url = '/disconnect/{backend}/'
    elif name == 'social:disconnect_individual':
        url = '/disconnect/{backend}/{association_id}/'
    else:
        url = name
    return url.format(**kwargs)


app.context_processor(backends)
app.jinja_env.filters['backend_name'] = filters.backend_name
app.jinja_env.filters['backend_class'] = filters.backend_class
app.jinja_env.filters['icon_name'] = filters.icon_name
app.jinja_env.filters['social_backends'] = filters.social_backends
app.jinja_env.filters['legacy_backends'] = filters.legacy_backends
app.jinja_env.filters['oauth_backends'] = filters.oauth_backends
app.jinja_env.filters['filter_backends'] = filters.filter_backends
app.jinja_env.filters['slice_by'] = filters.slice_by
app.jinja_env.globals['url'] = url_for
