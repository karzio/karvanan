import asyncio
import os

import requests


SLACK_TOKEN = os.environ.get("SLACK_BOT_TOKEN")


async def sub_original_message(channel: str, timestamp: str):
    """
    Substitutes original message with a statement about an information leak
    :param channel: id of a channel with the message
    :param timestamp: timestamp of the message
    :return:
    """

    # as_user defines if the message update should leave the original author
    data = {
        "channel": channel,
        "ts": timestamp,
        "text": "```This message was removed because it was caught with a pattern```",
        "as_user": True,
    }
    await asyncio.to_thread(
        requests.post,
        "https://slack.com/api/chat.update",
        data=data,
        headers={"Authorization": f"Bearer {SLACK_TOKEN}"},
    )


async def delete_file(file_id: str):
    await asyncio.to_thread(
        requests.post,
        "https://slack.com/api/files.delete",
        data={"file": file_id},
        headers={"Authorization": f"Bearer {SLACK_TOKEN}"},
    )


async def get_text_from_file(file_url: str) -> str:
    """
    Returns a content of a file downloaded from the file_url on Slack server.
    :param file_url:
    :return:
    """
    result = await asyncio.to_thread(
        requests.post, file_url, headers={"Authorization": f"Bearer {SLACK_TOKEN}"}
    )
    return result.content.decode("utf-8")
