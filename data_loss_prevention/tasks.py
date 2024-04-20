import asyncio
from datetime import datetime


from data_loss_prevention.utils import clean_timestamp
from slack_manager.tasks import delete_file, sub_original_message, get_text_from_file


async def save_caught_pattern(text: str, pattern: str, **kwargs):
    """
    Saves a message content with a pattern that caught the message.
    :param text:
    :param pattern:
    :param kwargs:
    :return:
    """
    from data_loss_prevention.models import CaughtMessage

    if timestamp := kwargs.get("timestamp"):
        timestamp = clean_timestamp(timestamp)
        sent_at = datetime.fromtimestamp(int(timestamp))
        caught_message = CaughtMessage(text=text, pattern=pattern, sent_at=sent_at)
        await caught_message.asave()


async def say(*args, **kwargs):
    """
    Analyzes messages received from slack.
    If file or message has a pattern inside the message, the message is substituted
    with a predefined text and file is removed.
    Stops on a first found pattern.
    :param args:
    :param kwargs:
    :return:
    """
    from data_loss_prevention.models import Pattern

    patterns = Pattern.objects.all()

    files: dict = kwargs.get("files", {})
    files_texts = {
        file_id: await get_text_from_file(file_url)
        for file_id, file_url in files.items()
    }
    text = kwargs.pop("text", "")

    caught_pattern = False
    async for pattern in patterns:
        if pattern.is_matching(text):
            asyncio.create_task(save_caught_pattern(text, pattern, **kwargs))
            caught_pattern = True
        for file_id, file_text in files_texts.items():
            if pattern.is_matching(file_text):
                asyncio.create_task(save_caught_pattern(file_text, pattern, **kwargs))
                asyncio.create_task(delete_file(file_id))
                caught_pattern = True

        if caught_pattern:
            await sub_original_message(
                channel=kwargs.get("channel"),
                timestamp=kwargs.get("timestamp"),
            )
            break
