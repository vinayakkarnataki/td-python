#!/usr/bin/env python

__author__ = 'vinayakkarnataki'

import tdclient
import sys, os, argparse
import Functions

#requests.packages.urllib3.disable_warnings()
if __name__ == '__main__':
    apikey = os.getenv("TD_API_KEY")
    sys.stdout = open('stdout_query.txt', 'w')

    if (len(sys.argv) < 5):
        print("Usage: %s -d database -t table" % sys.argv[0])
        print("Insufficient arguments provided. Exiting the program")
        sys.exit(1)

    try:
        parser = Functions.createParser(argparse.ArgumentParser())
        args = parser.parse_args()
    except:
        print("Unrecongnized parameter passed. Please check the usage")
        sys.exit(1)

    for arg in vars(args):
        if arg == 'd':
            dbase = getattr(args, arg)
        elif arg == 't':
             table = getattr(args, arg)
        elif arg == 'c':
             columns = getattr(args, arg)
        elif arg == 'm':
             mintime = getattr(args, arg)
        elif arg == 'M':
             maxtime = getattr(args, arg)
        elif arg == 'l':
             limit = getattr(args, arg)
        elif arg == 'f':
             file = getattr(args, arg)
        else:
            print("Undefined argument passed: %s" % getattr(args, arg))
            sys.exit(1)

    Functions.validateString(table)
    Functions.validateString(dbase)
    Functions.validateString(columns)
    Functions.validateTime(mintime,maxtime)
    Functions.validateInt(limit)
    Functions.validateFile(file)


    try:
        if file == 'csv':
            filetype = Functions.initCSVfile()
        else:
            filetype = Functions.initTabfile()
    except IOError:
        print("Error creating file for output. Exiting the program")
        sys.exit(1)

    query = "SELECT " + columns + " FROM " + table + " WHERE " + "TD_TIME_RANGE(time, " + str(mintime) + "," +  str(maxtime) + ")" + " LIMIT " + str(limit)

    with tdclient.Client(apikey) as client:
        try:
            data = client.query(dbase, query)
            data.wait()
            if data.result_size > 20:
                for line in data.result():
                    if file == 'csv':
                        Functions.writeCSV(filetype, list(line))
                    else:
                        Functions.writeTSV(filetype, list(line))
            else:
                print("No matching records found based on the given input")
                sys.exit(1)

        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            sys.exit(1)

    sys.exit(0)

