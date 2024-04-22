import json
import logging

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from queue_client.aws_queue_client import AWSQueueClient


class SlackAPIView(APIView):
    """
    API view for communicating with Slack
    """

    def post(self, request, format=None):
        """
        View for receiving and queueing Slack messages to SQS queue.
        """
        received = request.data
        if received.get("event", {}).get("type") == "message":
            if text := received.get("event", {}).get("text"):
                aws_queue_client = AWSQueueClient()
                response = aws_queue_client.push_message(
                    json.dumps(
                        {
                            "task": "say",
                            "kwargs": {
                                "channel": received["event"]["channel"],
                                "text": text,
                                "timestamp": received["event"]["event_ts"],
                                "files": {
                                    file["id"]: file["url_private"]
                                    for file in received["event"].get("files", [])
                                },
                            },
                        }
                    )
                )
                if response != status.HTTP_200_OK:
                    logging.warning(response)
        elif received.get("type", "") == "url_verification":
            return Response(received.get("challenge"))
        return Response(received.get("token", ""))
