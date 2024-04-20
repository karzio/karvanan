import abc


class QueueClient:
    def __init__(self, queue_name: str | None = None):
        self.queue_name = queue_name if queue_name else "slack-messages"

    @abc.abstractmethod
    def push_message(self, message):
        raise NotImplementedError

    @abc.abstractmethod
    def pop_messages(self):
        raise NotImplementedError
