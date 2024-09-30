from common.settings.configured_settings import ConfiguredSettings


class S3Settings(ConfiguredSettings):
    s3_endpoint: str
    s3_bucket: str
    s3_region: str
    s3_key: str
    s3_secret: str
    s3_enabled: bool
