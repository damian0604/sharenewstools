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
