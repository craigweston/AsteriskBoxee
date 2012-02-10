#!/usr/bin/env python

import argparse
import sys

from boxee.rpc import BoxeeRPC

def pair(boxee, args):
    boxee.pair(args.passcode) 
    boxee.pair(sys.stdin.readline().strip())

def connect(boxee, args):   
    boxee.connect()

def notify(boxee, args):
    boxee.connect()
    boxee.notify(" ".join(args.msg))
 
def main():
                   
    parser = argparse.ArgumentParser(description='Boxee RPC client')

    parser.add_argument('host', help='the hostname of the boxee server')
    parser.add_argument('--port', help='the port of the boxee server, default: 9090', type=int)
                        
    subparsers = parser.add_subparsers(help='sub commands help')
             
    pairparser = subparsers.add_parser('pair', help='pair command help')
    pairparser.add_argument('--passcode', help='passcode to response to pair request')
    pairparser.set_defaults(execute=pair)

    connectparser = subparsers.add_parser('connect', help='connect command help')
    connectparser.set_defaults(execute=connect)

    notifyparser = subparsers.add_parser('notify', help='notify command help')
    notifyparser.add_argument('--msg', help='the notification message to display', nargs='*') 
    notifyparser.set_defaults(execute=notify)    

    args = parser.parse_args()

    boxee = BoxeeRPC(args.host, args.port or 9090)
    boxee.open()

    try:
        args.execute(boxee, args)
    except Exception, err:
        sys.stderr.write('ERROR: %s\n' % str(err))
        return 1 
    finally:
        boxee.close()
    
    return 0

if __name__ == '__main__':
    sys.exit(main())


