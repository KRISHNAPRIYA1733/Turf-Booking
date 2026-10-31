from rest_framework import serializers
from Booking.models import TurfDb,BookingDb
from datetime import date, datetime, time, timedelta
class Turf_serializer(serializers.ModelSerializer):
    class Meta:
        model=TurfDb
        fields="__all__"
        read_only_fields=["id"]

class Booking_serializer(serializers.ModelSerializer):
    class Meta:
        model=BookingDb
        fields="__all__"
        read_only_fields=["id","token_number","total_price"]
    def validate(self,validated_data):
        booking_date=validated_data.get("booking_date")
        time_slot=validated_data.get("time_slot")
        turf=validated_data.get("turf")

        if booking_date<date.today():
            raise serializers.ValidationError("date is invalid")
        
        if not turf.is_available:
            raise serializers.ValidationError("Turf is unavilable")

        if time_slot<time(6,0) or time_slot>time(20,0):
            raise serializers.ValidationError("This Time is not available")
        if BookingDb.objects.filter(
            turf=turf,
            booking_date=booking_date,
            time_slot=time_slot
        ).exists():
            raise serializers.ValidationError("Alreday Booked!!")
        return validated_data