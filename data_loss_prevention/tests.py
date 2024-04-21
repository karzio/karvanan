from django.test import TestCase

from data_loss_prevention.models import Pattern


class PatternTests(TestCase):
    def setUp(self):
        self.email_pattern = Pattern.objects.create(
            name="email", regex="[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}"
        )
        self.visa_pattern = Pattern.objects.create(
            name="visa", regex="^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14})$"
        )

    def test_is_matching_pattern(self):
        assert self.email_pattern.is_matching("email@email.pl")

    def test_is_not_matching_pattern(self):
        assert self.visa_pattern.is_matching("2137") is None

    def test_empty_pattern_is_not_matching(self):
        assert self.email_pattern.is_matching("") is None
        assert self.visa_pattern.is_matching("") is None
