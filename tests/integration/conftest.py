# tests/conftest.py
import pytest
import uuid
from azure.storage.blob import BlobServiceClient

CONNECTION_STRING = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/"
    "K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)


@pytest.fixture
def blob_service():
    return BlobServiceClient.from_connection_string(CONNECTION_STRING)


@pytest.fixture
def container_name():
    return f"test-{uuid.uuid4().hex[:8]}"


@pytest.fixture
def blob_storage_service(blob_service):
    from blob_storage_service import BlobStorageService

    return BlobStorageService(blob_service)


@pytest.fixture
def test_file(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("Hello, Azure!")
    return str(file_path)
