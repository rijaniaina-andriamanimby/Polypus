from django.db import models
from django.utils.timezone import now


class Visitor(models.Model):
    ip_address = models.GenericIPAddressField()
    visit_time = models.DateTimeField(default=now)
