# encoding: utf-8

from os import sep
from telnetlib import STATUS
from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd
import json



class StockView(APIView):
    """
    Receives stock requests from the API service.
    """
    
    def get(self, request, *args, **kwargs):
         
        stock_code = request.query_params.get('stock_code')
        
        try:
            #with request.Session() as s:
                stock_info=f'https://stooq.com/q/l/?s={stock_code}&f=sd2t2ohlcvn&h&e=csv'
                stock_df=pd.read_csv(stock_info)
                
                stock_json=stock_df.to_json(orient='records',lines=True)
                status=200

                if str(stock_df["Date"][0])=="N/D":
                    stock_json='{"Error": "Error invalid sotck name"}'     
                    status=404
                    
        except Exception as e:
            stock_json='{"Error": "Error to Fech stock information"}'     
            status=500

        finally:
            return Response(json.loads(stock_json),status=status)
