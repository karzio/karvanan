import re

from django.db import models


class Pattern(models.Model):
    name = models.CharField(max_length=120)
    regex = models.CharField(max_length=120)

    def is_matching(self, text):
        compiled_regex = re.compile(self.regex)
        return compiled_regex.search(text)

    def __str__(self):
        return self.name
