Python script to bruteforce data of databases in case of blind sql injections.

Parses an http(s) request and bruteforces in the given points finding one char at a time.
Will look for either a delay (in case of time-based) or some text (string indicating true statement).
In case of time-based simply ignore the -t arguement.

Delay between requests and proxy usage hardcoded for now. Still needs much work.

usage example:
python sqlbrute.py -i request.txt -s text -t "lala"