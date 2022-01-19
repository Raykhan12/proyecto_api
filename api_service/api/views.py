# encoding: utf-8

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import UserRequestHistory
from api.serializers import UserRequestHistorySerializer
from django.db.models import Count
import requests

API_STOCK_URL="http://127.0.0.1:7000/"

class StockView(APIView):
    """
    Endpoint to allow users to query stocks
    """
    
    def get(self, request, *args, **kwargs):
        
        stock_code = request.query_params.get('stock_code')
       
        try:   
            response = requests.request(
            "GET", API_STOCK_URL+"stock", params ={'stock_code': f'{stock_code}'})

            if response.status_code==200:
                self.save_db(response.json(),request.user)
                
            return Response(response.json(),response.status_code)

        except Exception as e:
            return Response({"Error": "Error to Fech stock information"}, status=500)

    def save_db(self,data,user):

        userRequestHistory = UserRequestHistory()
        userRequestHistory.user = user
        userRequestHistory.date = data["Date"] + " " + data["Time"]
        userRequestHistory.name = data["Name"]
        userRequestHistory.symbol = data["Symbol"]
        userRequestHistory.open = data["Open"]
        userRequestHistory.high = data["High"]
        userRequestHistory.low = data["Low"]
        userRequestHistory.close = data["Close"]
        userRequestHistory.save()


class HistoryView(generics.ListAPIView):
    """
    Returns queries made by current user.
    """

    serializer_class = UserRequestHistorySerializer
   
    def get(self, request, *args, **kwargs):
        
        user_id = request.user.id
        AllStockHistory = UserRequestHistory.objects.all().filter(user_id=user_id)[::-1]
        serializer = self.serializer_class(AllStockHistory, many=True)
        return Response(serializer.data)


class StatsView(APIView):
    """
    Allows super users to see which are the most queried stocks.
    """
    
    def get(self, request, *args, **kwargs):

    
        def Convert_list_to_dict(lst):
            dict_respuestas=[]
            for i in range(0,len(lst)):
                dict_respuestas.append({"stock": lst[i][0], "times_requested" : lst[i][1]})
            return dict_respuestas
           

        if request.user.is_superuser:

            StockStats=Convert_list_to_dict(
                list(
                    UserRequestHistory.objects
                    .values_list('symbol')
                    .annotate(count=Count('symbol'))
                    .order_by('-count')[:5]
                    )
            ) 
                  
            return Response(StockStats, status=200)

        return Response({"Denied": " access denied to this endpoint"}, status=401)    
