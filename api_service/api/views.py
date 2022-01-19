# encoding: utf-8

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import UserRequestHistory
from api.serializers import UserRequestHistorySerializer

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
    # TODO: Implement the query needed to get the top-5 stocks as described in the README, and return
    # the results to the user.
    def get(self, request, *args, **kwargs):
        return Response()
