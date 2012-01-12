#!/usr/bin/env python

import argparse
import sys
import logging

from rpc import RPC

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

log_handler = logging.StreamHandler(sys.stdout)
log_handler.setLevel(logging.DEBUG)
logger.addHandler(log_handler)


def pair(boxee, args):
    boxee.pair(args.passcode) 

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

    boxee = RPC(args.host, args.port or 9090)
    try:
        args.execute(boxee, args)
    except Exception:
        logger.exception('Boxee RPC error')
        return 1 
    finally:
        boxee.close()
    
    return 0

if __name__ == '__main__':
    sys.exit(main())


