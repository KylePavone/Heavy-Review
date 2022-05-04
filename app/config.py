class Configuration:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://dima:diman1243@localhost:5432/heavyreview"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "efalksglidghdofihgdlsvdfjishfzdkfjbgi"
    WTF_CSRF_SECRET_KEY = "a csrf secret key"

    SECURITY_PASSWORD_SALT = 'saltjisfdjsfoihfosdfsihfdijsd;knfsl'
    SECURITY_PASSWORD_HASH = 'bcrypt'
