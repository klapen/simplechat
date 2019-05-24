from __future__ import absolute_import, unicode_literals
from celery import shared_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import requests
import csv

@shared_task
def getStockQuote(room_group_name, stock_code):
    url = 'https://stooq.com/q/l/?s=%s&f=sd2t2ohlcv&h&e=csv​'
    with requests.Session() as s:
        response = s.get(url % stock_code)
        if response.status_code != 200:
            print('getStockQuote - Failed to get data: %s', response.status_code)
            async_to_sync(channel_layer.group_send)(
                room_group_name,
                {
                    'type': 'bot_message',
                    'data': {
                        'command': 'bot_message',
                        'from': 'Bot stock',
                        'message': 'Error getting %s information' % stock_code.upper()
                    }
                }
            )
        else:
            data = csv.DictReader(response.text.strip().split('\n'))
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                room_group_name,
                {
                    'type': 'bot_message',
                    'data': {
                        'command': 'bot_message',
                        'from': 'Bot stock',
                        'message': '%s quote is $%s per share' % (stock_code.upper(), next(data)['Close'])
                    }
                }
            )
        return
