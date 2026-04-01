# azurite-storage-client.py - Azure Blob Storage operations against Azurite
from azure.storage.blob import BlobServiceClient
from config import get_storage_connection_string


class BlobStorageService:
    def __init__(self, blob_service: BlobServiceClient):
        self.blob_service = blob_service

    def ensure_container_exists(self, container_name: str) -> bool:
        container_client = self.blob_service.get_container_client(container_name)
        if not container_client.exists():
            container_client.create_container()
            return True
        return False

    def upload_file(self, container_name: str, blob_name: str, file_path: str) -> None:
        blob_client = self.blob_service.get_blob_client(container_name, blob_name)
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

    def list_blobs(self, container_name: str) -> list:
        container_client = self.blob_service.get_container_client(container_name)
        return list(container_client.list_blobs())

    def download_blob(self, container_name: str, blob_name: str) -> bytes:
        blob_client = self.blob_service.get_blob_client(container_name, blob_name)
        return blob_client.download_blob().readall()

    def delete_blob(self, container_name: str, blob_name: str) -> None:
        blob_client = self.blob_service.get_blob_client(container_name, blob_name)
        blob_client.delete_blob()


if __name__ == "__main__":
    blob_service = BlobServiceClient.from_connection_string(
        get_storage_connection_string()
    )
    service = BlobStorageService(blob_service)

    container_name = "my-documents"
    if service.ensure_container_exists(container_name):
        print(f"Created container: {container_name}")
    else:
        print(f"Container {container_name} already exists")

    service.upload_file(container_name, "report.txt", "report.txt")
    print("Uploaded report.txt")

    for blob in service.list_blobs(container_name):
        print(f"  Blob: {blob.name}, Size: {blob.size} bytes")

    content = service.download_blob(container_name, "report.txt")
    print(f"Downloaded {len(content)} bytes")
    print(f"Content: {content.decode('utf-8')}")

    service.delete_blob(container_name, "report.txt")
    print("Deleted report.txt")
