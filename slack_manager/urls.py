from django.urls import path
from slack_manager.views.slack import SlackAPIView


urlpatterns = [
    path(r"", SlackAPIView.as_view(), name="slack"),
]
