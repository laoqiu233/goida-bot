from logging import getLogger

from aiobotocore.session import get_session
from botocore.exceptions import ClientError

from common.settings import S3Settings
from common.storage import ArticlesStorage

logger = getLogger(__name__)


class S3ArticlesStorage(ArticlesStorage):
    def __init__(self, settings: S3Settings):
        self._settings = settings

    def _append_suffix(self, key: str):
        return f"{key}.pdf"

    def _get_client(self):
        session = get_session()
        return session.create_client(
            "s3",
            endpoint_url=self._settings.s3_endpoint,
            region_name=self._settings.s3_region,
            aws_access_key_id=self._settings.s3_key,
            aws_secret_access_key=self._settings.s3_secret,
        )

    async def store(self, key: str, content: bytes) -> None:
        try:
            async with self._get_client() as s3:
                await s3.put_object(
                    Bucket=self._settings.s3_bucket,
                    Key=self._append_suffix(key),
                    Body=content,
                )
        except ClientError as e:
            logger.error("Failed to store key %s to S3: %s", key, e)

    async def read(self, key: str) -> bytes | None:
        if not await self.exists(key):
            return None

        try:
            async with self._get_client() as s3:
                result = await s3.get_object(
                    Bucket=self._settings.s3_bucket, Key=self._append_suffix(key)
                )
                return await result["Body"].read()
        except ClientError as e:
            logger.error("Failed to read key %s from S3: %s", key, e)

    async def exists(self, key: str) -> bool:
        try:
            async with self._get_client() as s3:
                response = await s3.list_objects(Bucket=self._settings.s3_bucket)
                if "Contents" in response:
                    return self._append_suffix(key) in map(
                        lambda object: object["Key"] if "Key" in object else "",
                        response["Contents"],
                    )
                return False
        except ClientError as e:
            logger.error("Failed to check existence of key from S3 %s: %s", key, e)
            return False
