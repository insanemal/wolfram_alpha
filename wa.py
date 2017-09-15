#!/usr/bin/python2


import requests
import os
import getpass
import argparse
from os.path import expanduser

def main():
    home = expanduser("~")
    config = os.path.join(home,'.wa_api_key')
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--short', action="store_true",help="Return just the answer.")
    parser.add_argument('-l','--long', action="store_false",help="Default. Return full text")
    parser.add_argument("query", help="Wolfram Alpha query")
    args = parser.parse_args()
    if os.path.exists(config):
        api_key = open(config,"r")
        key = api_key.readline().strip()
        api_key.close()
    else:
        print "API Key not found. Please enter API key"
        key= getpass.getpass()
        api_key = open(config,"w")
        api_key.write(key)
        api_key.close()
    query = args.query
    r = requests.get("http://api.wolframalpha.com/v2/query?input={}&appid={}&format=plaintext&output=json".format(query,key))
    j = r.json()['queryresult']
    if args.short:
        print_short(j)
    else:
        print_long(j)

def print_long(j):
    for field in j['pods']:
        if 'title' in field:
            print '\x1b[1;34;40m'+field['title']+'\x1b[0m'
            for subpod in field['subpods']:
                if 'plaintext' in subpod:
                        print subpod['plaintext']



def print_short(j):
    for field in j['pods']:
        if 'title' in field:
            if field['title'] == 'Result':
                for subpod in field['subpods']:
                    if 'plaintext' in subpod:
                        print subpod['plaintext']

if __name__ == '__main__':
    main()
