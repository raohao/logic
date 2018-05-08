from rest_framework import serializers
from guard.models import AlarmCheck

class AlarmCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlarmCheck
        fields = ('check_id', 'title', 'status')

