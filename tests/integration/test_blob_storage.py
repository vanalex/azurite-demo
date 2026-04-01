class TestBlobStorageService:
    def test_ensure_container_creates_new_container(
        self, blob_storage_service, container_name
    ):
        was_created = blob_storage_service.ensure_container_exists(container_name)
        assert was_created is True
        assert len(blob_storage_service.list_blobs(container_name)) == 0

    def test_ensure_container_returns_false_for_existing(
        self, blob_storage_service, container_name
    ):
        blob_storage_service.ensure_container_exists(container_name)
        was_created = blob_storage_service.ensure_container_exists(container_name)
        assert was_created is False

    def test_upload_and_download_file(
        self, blob_storage_service, container_name, test_file
    ):
        blob_storage_service.ensure_container_exists(container_name)
        blob_name = "test-upload.txt"

        blob_storage_service.upload_file(container_name, blob_name, test_file)

        content = blob_storage_service.download_blob(container_name, blob_name)
        assert content.decode("utf-8") == "Hello, Azure!"

    def test_list_blobs(self, blob_storage_service, container_name, test_file):
        blob_storage_service.ensure_container_exists(container_name)
        blob_storage_service.upload_file(container_name, "blob1.txt", test_file)
        blob_storage_service.upload_file(container_name, "blob2.txt", test_file)

        blobs = blob_storage_service.list_blobs(container_name)
        assert len(blobs) == 2

    def test_delete_blob(self, blob_storage_service, container_name, test_file):
        blob_storage_service.ensure_container_exists(container_name)
        blob_name = "to-delete.txt"
        blob_storage_service.upload_file(container_name, blob_name, test_file)

        blob_storage_service.delete_blob(container_name, blob_name)

        blobs = blob_storage_service.list_blobs(container_name)
        assert not any(b.name == blob_name for b in blobs)
