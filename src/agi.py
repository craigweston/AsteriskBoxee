#!/usr/bin/env python

import sys
from boxee.rpc import BoxeeRPC 

def parseAGIArgs():
    result ={}
    line = None 
    while(line != '\n'):
        line = sys.stdin.readline()
        args = line.split(":")
        if 2 == len(args):
            result[args[0].strip()] = args[1].strip() 

    return result

def main():
    args = parseAGIArgs()

    boxee = BoxeeRPC(sys.argv[1], int(sys.argv[2]), 'Asterisk Boxee')
    boxee.open()
    try:
        callInfo = (args['agi_calleridname'], args['agi_callerid'])
        boxee.connect()
        boxee.notify("Caller ID: %s \n%s" % callInfo)
    except Exception as e:
        sys.stderr.write("Error: %s" % e)
        return 1
    finally:
        boxee.close()
    
    return 0

if __name__== '__main__':
    main()    

