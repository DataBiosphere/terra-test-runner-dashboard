class AppConfig(object):
    SQLALCHEMY_DATABASE_URI = 'bigquery://terra-kernel-k8s/simple_stream_dataset'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
