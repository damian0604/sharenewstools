'''
Provides main functionality to engagement data
'''
import datetime
from time import sleep
from urllib.parse import quote
from os import environ
import requests


class Crowdtangle():
    '''A wrapper around the Crowdtangle API that automatically respects rate
    limits'''
    def __init__(self, token=None, startdate='2018-01-01'):
        if token is None:
            self.token = environ['CROWDTANGLETOKEN']
        else:
            self.token = token
        # TODO: allow for different endpoints
        self.endpoint = "https://api.crowdtangle.com/links?link={}&startDate={}&token={}"
        self.lastcall = datetime.datetime(2000, 1, 1)
        self.startdate = startdate

    def _respectlimit(self):
        '''This function makes sure that the rate limit of 2 calls per second
        is respected'''
        while (datetime.datetime.now() - self.lastcall) < datetime.timedelta(seconds=35):
            sleep(1.1)
        self.lastcall = datetime.datetime.now()

    def retrieve(self, url):
        '''Retrieves engagement data for a given URL'''
        call = self.endpoint.format(quote(url), self.startdate, self.token)
        self._respectlimit()
        r = requests.get(call)
        data = r.json()
        return data

class GraphAPI():
    '''A wrapper around the Graph API that automatically respects rate
    limits'''
    def __init__(self, token=None):
        if token is None:
            self.token = environ['GRAPHAPITOKEN']
        else:
            self.token = token
        # TODO: allow for different endpoints
        self.endpoint = "https://graph.facebook.com/?id={}&fields=engagement&access_token={}"
        self.batchstart = datetime.datetime.now()
        self.callsthisbatch = 0

    def _respectlimit(self):
        '''This function makes sure that the rate limit of 200 calls per hour
        is respected'''
        #print(self.callsthisbatch)
        #print(datetime.datetime.now() - self.batchstart)
        if self.callsthisbatch == 198:
            while (datetime.datetime.now() - self.batchstart) < datetime.timedelta(hours=1, minutes=5):
                sleep(60)
                print('Sleeping until {}'.format(self.batchstart + datetime.timedelta(hours=1)))
            self.batchstart = datetime.datetime.now()
            self.callsthisbatch = 0

    def retrieve(self, url):
        '''Retrieves engagement data for a given URL'''
        call = self.endpoint.format(quote(url), self.token)
        self._respectlimit()
        r = requests.get(call)
        self.callsthisbatch +=1
        data = r.json()
        return data
