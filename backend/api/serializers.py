from rest_framework import serializers

class RecordSerializer(serializers.Serializer):
    name   = serializers.CharField(max_length=64)
    date   = serializers.IntegerField()
    rating = serializers.IntegerField(min_value=-10, max_value=10)
    sale   = serializers.IntegerField(min_value=0, max_value=1)
