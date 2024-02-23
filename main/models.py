from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
import uuid


class Profile(models.Model):
    bio = models.TextField(max_length=500, blank=True)
    user = models.OneToOneField(User, models.CASCADE)


class Poll(models.Model):
    user = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="user_relate")
    slug = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000, blank=True)
    image = models.ImageField(max_length=255, null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)


class Question(models.Model):
    title = models.CharField(max_length=1000, blank=True)
    poll_relate = models.ForeignKey("Poll", on_delete=models.CASCADE, related_name="poll_relate", blank=True)
    type = models.CharField(max_length=8, default='short',
                            choices=[('detailed', 'detailed'), ('plural', 'plural'), ('singular', 'singular')])

    def __str__(self):
        return str(self.title)


class Answer(models.Model):
    title = models.CharField(max_length=1000, default=None, blank=None)
    ans = models.BooleanField(blank=True)
    question_relate = models.ForeignKey("Question", on_delete=models.CASCADE, related_name="question_relate", blank=True)

    def __str__(self):
        return str(self.title)
#
#
class PollResult(models.Model):
    poll_relate = models.ForeignKey("Poll", on_delete=models.CASCADE, related_name="poll_results_relate", blank=True)
    result = models.ManyToManyField("Gift", related_name="gift_relate", blank=True)
    name = models.CharField(max_length=1000, default=None, blank=None)
    surname = models.CharField(max_length=1000, default=None, blank=None)

    def __str__(self):
        return str(self.poll_relate)


class Holiday(models.Model):
    name = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return str(self.name)


class Gift(models.Model):
    holiday_relate = models.ForeignKey("Holiday", on_delete=models.PROTECT, related_name="holiday_relate", blank=True)
    name = models.CharField(max_length=1000, blank=True)
    description = models.CharField(max_length=1000, blank=True)
    link = models.URLField()
    store = models.CharField(max_length=1000, blank=True)
    image = models.ImageField(max_length=255, upload_to="gifts/", null=True, blank=True)

    def __str__(self):
        return str(self.name)
