# config.py - switch between Azurite and real Azure Storage
import os

def get_storage_connection_string():
    """Return the appropriate connection string based on environment."""
    env = os.environ.get("ENVIRONMENT", "development")

    if env == "development":
        return (
            "DefaultEndpointsProtocol=http;"
            "AccountName=devstoreaccount1;"
            "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/"
            "K1SZFPTOtr/KBHBeksoGMGw==;"
            "BlobEndpoint=http://azurite:10000/devstoreaccount1;"
            "QueueEndpoint=http://azurite:10001/devstoreaccount1;"
            "TableEndpoint=http://azurite:10002/devstoreaccount1;"
        )
    else:
        # In production, use the real Azure connection string from env
        return os.environ["AZURE_STORAGE_CONNECTION_STRING"]