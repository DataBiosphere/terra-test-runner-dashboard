class AppConfig(object):
    SQLALCHEMY_DATABASE_URI = 'bigquery://terra-kernel-k8s/stream_dataset?credentials_path=/Users/ichang/Downloads' \
                              '/terra-kernel-k8s-bd7b02311de9.json'
    SQLALCHEMY_TRACK_NOTIFICATION = False
