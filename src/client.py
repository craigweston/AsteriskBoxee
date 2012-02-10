#!/usr/bin/env python

import argparse
import sys

from boxee.rpc import BoxeeRPC

def pair(boxee, args):
    boxee.pair() 

    print 'Please enter the passcode shown on your TV: ' 
    success = boxee.pair(sys.stdin.readline().strip())
    if success:
        print 'You have successfully paired your device'
    else:
        print 'There was an error pairing your device'

def unpair(boxee, args):   
    boxee.connect()
    success =boxee.unpair()
    if success:
        print 'You have unpaired your device successfully'
    else:
        print 'There was an error unpairing your device'

def notify(boxee, args):
    boxee.connect()
    boxee.notify(" ".join(args.msg))
 
def main():
                   
    parser = argparse.ArgumentParser(description='Boxee RPC client')

    parser.add_argument('host', help='the hostname of the boxee server')
    parser.add_argument('--port', help='the port of the boxee server, default: 9090', type=int)
                        
    subparsers = parser.add_subparsers(help='sub commands help')
             
    pairparser = subparsers.add_parser('pair', help='pair command help')
    pairparser.set_defaults(execute=pair)

    unpairparser = subparsers.add_parser('unpair', help='connect command help')
    unpairparser.set_defaults(execute=unpair)

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


