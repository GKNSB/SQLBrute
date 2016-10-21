Python script to bruteforce data of databases in case of blind sql injections.

Parses an http(s) request and bruteforces in the given points finding one char at a time.
Will look for either a delay (in case of time-based) or some text (string indicating true statement).

Delay between requests and proxy usage hardcoded for now. Still needs much work.

usage example:
Usage: python sqlbrute.py -i <inputfile> -s <sqlitype> [-t <textmatch>|-d <timedelay>]
Arguments:
 -i, --ifile        Input file. Defines the file containing your request.
 -s, --sqlitype     SQL injection type. Can be either "text" or "time".
 -t, --text         Should be defined if sqlitype="text". The text to look for in a true response
 -d, --delay        Should be defined if sqlitype="time". The time delay a response will have if true.