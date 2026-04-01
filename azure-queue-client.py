# queue_example.py - Azure Queue Storage operations against Azurite
from azure.storage.queue import QueueServiceClient
import json

CONN_STR = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/"
    "K1SZFPTOtr/KBHBeksoGMGw==;"
    "QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;"
)

queue_service = QueueServiceClient.from_connection_string(CONN_STR)

# Create a queue if it doesn't exist
queue_name = "task-queue"
queue_client = queue_service.get_queue_client(queue_name)
try:
    queue_client.create_queue()
    print(f"Created queue: {queue_name}")
except Exception:
    print(f"Queue {queue_name} already exists")

# Send messages to the queue
for i in range(5):
    message = json.dumps({"task_id": i, "action": "process_image"})
    queue_client.send_message(message)
    print(f"Sent message {i}")

# Receive and process messages
messages = queue_client.receive_messages(max_messages=5, visibility_timeout=30)
for msg in messages:
    data = json.loads(msg.content)
    print(f"Processing task {data['task_id']}: {data['action']}")
    # Delete the message after processing
    queue_client.delete_message(msg)
