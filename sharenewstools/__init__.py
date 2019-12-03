#!/usr/bin/env python3

import json
import argparse
import logging
import requests
import datetime
from time import sleep
from os.path import isfile
from urllib.parse import quote
from os import environ

def parse_inputfile(filename,filetype):
    if filetype=='json':
        with open(filename) as fi:
            urls = json.load(fi)
    else:
        raise NotImplementedError

    return urls

def parse_outputfile(filename,filetype):
    if filetype=='json':
        # assume one json object per line
        with open(filename) as fi:
            urls = []
            for line in fi:
                data = json.loads(line)
                urls.append(data.get('url'))
    else:
        raise NotImplementedError

    return urls

def append_to_outputfile (filename,filetype,data):
    if filetype=='json':
        # assume one json object per line
        with open(filename, mode='a') as f:
            json.dump(data,f)
            f.write('\n')
    else:
        raise NotImplementedError


class Crowdtangle():
    def __init__(self, token=None, startdate='2018-01-01'):
        if token==None:
            self.token = environ['CROWDTANGLETOKEN']
        else:
            self.token = token
        # TODO: allow for different endpoints
        self.endpoint = "https://api.crowdtangle.com/links?link={}&startDate={}&token={}"
        self.lastcall = datetime.datetime(2000,1,1)
        self.startdate = startdate

    def _respectlimit(self):
        # we are only allowed to make 2 calls per second
        while (datetime.datetime.now() - self.lastcall) < datetime.timedelta(seconds=35):
            sleep(1)
        self.lastcall = datetime.datetime.now()
    
    def retrieve(self,url):
        call = self.endpoint.format(quote(url), self.startdate, self.token)
        self._respectlimit()
        r = requests.get(call)
        data = r.json()
        return data
        
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Retrieves crowdtangle engagement data for a list of URLs')
    parser.add_argument("inputfile", help="File that provides the URLs to process")
    parser.add_argument("outputfile", help="File to which the output should be written")
    parser.add_argument("--inputfiletype", default="json", choices=["json", "txt", "csv"])
    parser.add_argument("--outputfiletype", default="json", choices=["json", "txt", "csv"])
    parser.add_argument("--overwrite", action="store_true",
                        help='Instead of appending to outputfile, overwrite it')
    parser.add_argument("--verbose", action='store_true')
    parser.add_argument("--token", help='Allows to specify crowdtangle token. Alternatively, it will be read from the environment variable CROWDTANGLETOKEN') 
    args = vars(parser.parse_args())
    if args['verbose']:
        logging.basicConfig(format='%(asctime)s- %(levelname)s - %(message)s', level=logging.DEBUG)
    urls = parse_inputfile(args['inputfile'], args['inputfiletype'])
    logging.info('{} URLs found in {}'.format(len(urls),args['inputfile']))
    
    if args['overwrite']==True or isfile(args['outputfile'])==False:
        already_processed_urls = []
        pass
    else:
        already_processed_urls = parse_outputfile(args['outputfile'], args['outputfiletype'])

    urls_to_be_processed = [u for u in urls if not u in already_processed_urls]
    logging.info('{} URLs still need to be processed'.format(len(urls_to_be_processed)))

    myct = Crowdtangle(args['token'])

    for url in urls_to_be_processed:
        data = {'url':url, 'crowdtangle':myct.retrieve(url)}
        append_to_outputfile(args['outputfile'],args['inputfiletype'],data)
