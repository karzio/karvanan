import boto3

from queue_client.queue_client import QueueClient


class AWSQueueClient(QueueClient):
    def __init__(self, queue_name: str | None = None):
        super().__init__(queue_name)
        self.message_group_id = "slack-fifo-messages"

    def push_message(self, message):
        sqs = boto3.resource("sqs")

        queue = sqs.get_queue_by_name(QueueName=self.queue_name)

        response = queue.send_message(
            MessageBody=message,
        )
        if (status_code := response["ResponseMetadata"]["HTTPStatusCode"]) is not None:
            return status_code

    def pop_messages(self):
        sqs = boto3.resource("sqs")

        queue = sqs.get_queue_by_name(QueueName=self.queue_name)

        messages = queue.receive_messages()
        for message in messages:
            yield message
            message.delete()
