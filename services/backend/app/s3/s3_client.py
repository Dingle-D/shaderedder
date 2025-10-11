from aiobotocore.session import get_session
from contextlib import asynccontextmanager

class S3Client:
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        endpoint_url: str, 
        bucket_name: str,
        certificate: str | None = None
    ):
        print(f"\n\n\n\nCertificate: {certificate}\n\n\n\n")
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
            "verify": certificate,
        }
        self.bucket_name = bucket_name
        self.session = get_session()
        print(f"\n\n\nS3 Options:\n{access_key}, {secret_key}, {endpoint_url}, {bucket_name}\n\n\n\n")

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file_from_disk(
        self,
        file_path: str,
        object_name: str,
    ):
        async with self.get_client() as client:
            with open(file_path, "rb") as file:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=file
                )

    async def upload_file(
        self,
        file,
        object_name: str
    ):
        async with self.get_client() as client:
            await client.put_object(
                Bucket=self.bucket_name,
                Key=object_name,
                Body=file
            )


    async def stream_file(
        self,
        object_name: str
    ):
        async with self.get_client() as client:
            response = await client.get_object(
                Bucket=self.bucket_name,
                Key=object_name
            )
            async for chunk in response["Body"].iter_chunks():
                yield chunk
