import os


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'you-will-never-guess')

    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', None)
