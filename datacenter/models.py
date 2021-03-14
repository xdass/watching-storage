import math

from django.db import models
from django.utils.timezone import localtime, timedelta


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def is_long(self, minutes=60):
        return self.get_duration() > timedelta(minutes=minutes)

    def get_duration(self):
        if self.leaved_at is None:
            time_now = localtime()
            return time_now - localtime(self.entered_at)
        else:
            return localtime(self.leaved_at) - localtime(self.entered_at)

    def __str__(self):
        return "{user} entered at {entered} {leaved}".format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved= "leaved at " + str(self.leaved_at) if self.leaved_at else "not leaved"
        )


def format_duration(duration):
    # 3600 сек в 1 часе
    hours = math.floor(duration.total_seconds() // 3600)
    minutes = math.floor((duration.total_seconds() % 3600) // 60)
    return f"{hours}ч {minutes}мин"