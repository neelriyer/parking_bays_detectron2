import os

class Config:
    SECRET_KEY=             os.environ.get('SECRET_KEY') or "cherry"
    CELERY_BROKER_URL=      "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND=  "redis://localhost:6379/0"
    TRAP_HTTP_EXCEPTIONS=   True
    
    

class DevelopmentConfig(Config):
    MONGO_URI=              "mongodb://localhost:27017/testdb"
    CELERY_BROKER_URL=      "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND=  "redis://localhost:6379/0"
    

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}