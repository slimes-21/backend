import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '47UK8GG9ABCYXE5YW3JJGV'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'database.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
