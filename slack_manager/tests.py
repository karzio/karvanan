from copy import deepcopy
from unittest.mock import patch

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class SlackApiTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("slack_manager:slack")
        self.data = {
            "event": {
                "user": "U06U9UPCRG9",
                "type": "message",
                "ts": "1713296509.133979",
                "client_msg_id": "df01eead-822f-4056-a6dc-2a62a354f8ef",
                "text": "<mailto:h@h.pl|h@h.pl>",
                "team": "T06TZNW75EG",
                "blocks": [
                    {
                        "type": "rich_text",
                        "block_id": "dFMXA",
                        "elements": [
                            {
                                "type": "rich_text_section",
                                "elements": [
                                    {
                                        "type": "link",
                                        "url": "mailto:h@h.pl",
                                        "text": "h@h.pl",
                                    }
                                ],
                            }
                        ],
                    }
                ],
                "channel": "C06TSRHJA8P",
                "event_ts": "1713296509.133979",
                "channel_type": "channel",
            }
        }

    @patch(
        "queue_client.aws_queue_client.AWSQueueClient.push_message", return_value=200
    )
    def test_push_message(self, mock_push_message):
        response = self.client.post(self.url, data=self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(mock_push_message.call_count, 1)

    @patch(
        "queue_client.aws_queue_client.AWSQueueClient.push_message", return_value=200
    )
    def test_dont_push_other_event(self, mock_push_message):
        data = deepcopy(self.data)
        data["event"]["type"] = "other"
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(mock_push_message.call_count, 0)
