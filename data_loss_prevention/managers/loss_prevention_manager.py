from data_loss_prevention.managers.manager import Manager
from queue_client.aws_queue_client import AWSQueueClient


class LossPreventionManager(Manager):

    async def _get_messages(self):
        """Read and pop messages from SQS queue"""
        queue_client = AWSQueueClient(self.queue)
        messages = queue_client.pop_messages()
        return messages
