from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from Booking.models import TurfDb,BookingDb
from Booking.serializers import Turf_serializer,Booking_serializer
from datetime import datetime,timedelta,time
from rest_framework import status


# Create your views here.
class TurfCreateListView(APIView):
    def get(self,request):
        qs=TurfDb.objects.all()
        serializer_instance=Turf_serializer(qs,many=True)
        return Response(data=serializer_instance.data)
    def post(self,request):
        form_data=request.data
        serializer_instance=Turf_serializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)
class TurfUpdateDeleteView(APIView):
    def get(self,request,pk):
        qs=get_object_or_404(TurfDb,id=pk)
        serializer_instance=Turf_serializer(qs)
        return Response(data=serializer_instance.data)
    def put(self,request,pk):
        form_data=request.data
        Turf_object=get_object_or_404(TurfDb,id=pk)
        serializer_instance=Turf_serializer(data=form_data,instance=Turf_object)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)
    def delete(self,request,pk):
        Turf_object=get_object_or_404(TurfDb,id=pk)
        Turf_object.delete()
        return Response(data={"Message":"Deleted..."})

class BookingCreateListView(APIView):
    def get(self,request):
        qs=BookingDb.objects.all()
        serializer_instance=Booking_serializer(qs,many=True)
        return Response(data=serializer_instance.data)
    def post(self,request):
        form_data=request.data
        serializer_instance=Booking_serializer(data=form_data)

        if serializer_instance.is_valid():
            booking_date=serializer_instance.validated_data.get("booking_date")
            turf=serializer_instance.validated_data.get("turf")
            time_slot=serializer_instance.validated_data.get("time_slot")

            starting=datetime.combine(booking_date,time_slot)
            ending=starting+timedelta(hours=2)

            last_booking=BookingDb.objects.filter(
                booking_date=booking_date,
                turf=turf
            ).order_by("-token_number").first()

            if last_booking is None:
                token_number=1
            else:
                token_number=last_booking.token_number+1

            total_price=turf.price_per_hour*2
            form_data=serializer_instance.validated_data
            form_data["token_number"]=token_number
            form_data["total_price"]=total_price

            qs=BookingDb.objects.create(**form_data)
          
            return Response({"Message":"Booking Created",
                             "Token_number":token_number,
                            "starting_Time":starting.time(),
                            "ending_time":ending.time(),
                            "Total_price":total_price})

        else:
            return Response(data=serializer_instance.errors,status=status.HTTP_400_BAD_REQUEST)


