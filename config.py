import os

class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY')

    database_url = os.environ.get(
        'DATABASE_URL',
        'sqlite:///SPP.db'
    )

    # Convert older PostgreSQL URL format if supplied
    if database_url.startswith('postgres://'):
        database_url = database_url.replace(
            'postgres://',
            'postgresql://',
            1
        )

    SQLALCHEMY_DATABASE_URI = database_url

    SQLALCHEMY_TRACK_MODIFICATIONS = False
