from insurance.settings import AWS_S3_MEDIA_BUCKET_NAME, AWS_S3_STATIC_BUCKET_NAME
from storages.backends.s3boto3 import S3Boto3Storage


class S3MediaStorage(S3Boto3Storage):
    bucket_name = AWS_S3_STATIC_BUCKET_NAME
    location = "media"


class S3StaticStorage(S3Boto3Storage):
    bucket_name = AWS_S3_MEDIA_BUCKET_NAME
    location = "static"
