class AppConfig(object):
    # BigQuery related configs
    SQLALCHEMY_DATABASE_URI = 'bigquery://terra-kernel-k8s/simple_stream_dataset'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Flask-Caching related configs
    CACHE_TYPE = 'FileSystemCache'
    CACHE_DEFAULT_TIMEOUT = 3600
    CACHE_IGNORE_ERRORS = True
    CACHE_DIR = '/mnt/trdash_cache'
    CACHE_THRESHOLD = 100
    CACHE_OPTIONS = {'mode': 777}
