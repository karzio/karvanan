from django.db import models

from .pattern import Pattern


class CaughtMessage(models.Model):
    text = models.TextField(blank=True)
    caught_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE)

    def __str__(self):
        if len(self.text) > 20:
            return self.text[:20]
        return self.text
