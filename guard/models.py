from django.db import models
from common.models import (HeadUser, Receipt)


class AlarmCheck(Receipt):
    q_id = models.CharField(max_length=32, null=True, blank=True)
    re_id = models.CharField(max_length=255, null=True, blank=True)
    classification = models.IntegerField(null=True, blank=True)
    s_ip = models.GenericIPAddressField(max_length=255, null=True, blank=True)
    d_ip = models.TextField(max_length=255, null=True, blank=True)
    s_address = models.CharField(max_length=255, null=True, blank=True)
    d_address = models.CharField(max_length=255, null=True, blank=True)
    stream = models.IntegerField(null=True, blank=True)
    start_from = models.CharField(max_length=255, null=True, blank=True)
    sustain = models.CharField(max_length=255, null=True, blank=True)
    app = models.CharField(max_length=255, null=True, blank=True)
    plan = models.TextField(max_length=5000, null=True, blank=True)

    class Meta:
        db_table = 'alarmCheck'
        verbose_name = '监控告警单'
        verbose_name_plural = verbose_name


# 事件单表


class EventCheck(Receipt):
    title = models.TextField(max_length=50, null=True, blank=True)
    a_id = models.ForeignKey(AlarmCheck, on_delete=models.SET_NULL, null=True, blank=True)
    s_id = models.ManyToManyField(HeadUser, related_name="s_id")
    transmit = models.ManyToManyField(HeadUser, related_name="transmit")
    history = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'eventCheck'

    def __str__(self):
        return self.id

# 考核评价表


class Evaluation(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    judge = models.ManyToManyField(HeadUser, related_name="judge")
    candidate = models.ManyToManyField(HeadUser, related_name="candidate")
    score = models.IntegerField(null=True, blank=True)
    reason = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'Evaluation'

    def __str__(self):
        return self.id
# Create your models here.
