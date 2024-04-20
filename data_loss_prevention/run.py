import asyncio
import os
import sys

from asgiref.sync import sync_to_async
from django.core.management import execute_from_command_line

from data_loss_prevention import LossPreventionManager
from data_loss_prevention.tasks import say


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    sync_to_async(execute_from_command_line(sys.argv))
    loss_prevention_manager = LossPreventionManager("slack-messages", {"say": say})
    asyncio.run(loss_prevention_manager.main())
