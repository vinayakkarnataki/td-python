__author__ = 'vinayakkarnataki'
import sys, argparse

def createParser(parsestr):
    parsestr.add_argument('-d', required=True, help='d help')
    parsestr.add_argument('-t', required=True, help='t help')
    parsestr.add_argument('-c', default='*', help='c help')
    parsestr.add_argument('-l', default=100, help='l help')
    parsestr.add_argument('-m', default="NULL", help='m help')
    parsestr.add_argument('-M', default="NULL", help='M help')
    parsestr.add_argument('-f', default="tsv", help='f help')
    parsestr.add_argument('-e', default="presto", help='e help')
    return parsestr


def initTabfile():
    tabfile = open("results_query.txt", "w")
    return tabfile

def initCSVfile():
    csvfile = open("results_query.csv", "w")
    return csvfile

def validateString(text):
    if (isinstance(text, basestring)):
        return True
    else:
        print("%s is not a sting parameter" % text)
        sys.exit(1)

def validateInt(num):
    if isinstance(int(num), int):
        return True
    else:
        print("%i is not an int parameter" % num)
        sys.exit(1)

def validateTime(min, max):
    code=''
    if min != "NULL":
        if isinstance(int(min), int):
            code = True
        else:
            print("%i is not an int parameter" % min)
            sys.exit(1)

    if max != "NULL":
        if isinstance(int(max), int):
            code = True
        else:
            print("%i is not an int parameter" % max)
            sys.exit(1)


    if min!="NULL" and max!="NULL":
        if int(min) > int(max):
            print("The minimum time is greater than the maximum time")
            sys.exit(1)
        else:
            code = True

    return code


def validateFile(fformat):
    if fformat not in "csv, tsv":
        print("File format should be csv or tsv")
        sys.exit(1)

def validateEngine(enginename):
    if enginename not in "presto, hive":
        print("Engine should be presto or hive")
        sys.exit(1)

def writeTSV(writer, alist):

    for items in alist:
        writer.write(str(items) + '\t')
    writer.write('\n')

def writeCSV(writer, alist):

    for items in alist:
        writer.write(str(items) + ', ')
    writer.write('\n')
