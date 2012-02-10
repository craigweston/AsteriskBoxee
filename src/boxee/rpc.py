#!/usr/bin/env python

import sys
import socket
import json
import logging
from logging.handlers import SysLogHandler

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
syslog = SysLogHandler(address='/dev/log')
formatter = logging.Formatter('%(name)s: %(levelname)s %(message)s')
syslog.setFormatter(formatter)
logger.addHandler(syslog)

class BoxeeRPCException(Exception):
    def  __init__(self, message):
       self.message = message

    def __str__(self):
        return repr(self.message)
        
class BoxeeRPC:
    
    def __init__(self, host, port, appId = 'Boxee RPC Client'):
        self.socket = None
        self.host = host
        self.port = port
        self.id = 100

    def open(self):
        if self.socket is not None:
            return;
   
        try:
            logger.debug('opening socket')
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
        except:
            logger.exception('failed to open socket')
            raise BoxeeRPCException('open connection failure')

    def close(self):
        if self.socket is not None:    
            logger.debug('closing socket')
            self.socket.close()
            self.socket = None

    def createCall(self, method, params=None):
        data = {
            'method': method,
            'id': self.id,
            'jsonrpc': '2.0' 
        }

        if params:
            data['params'] = params

        self.id += 1
        return json.dumps(data)

    def call(self, data): 
        logger.debug(data);
        self.socket.send(data) 
        return self.parseResponse()

    def parseResponse(self):
        data = '' 
        while True:
            read = self.socket.recv(1024)
            if not read:
                break;
            data += read
            if data.find('\n') >= 0:
                break
        
        jsonData = json.loads(data)
        logger.debug(jsonData);
        
        if jsonData.has_key('error'):
            logger.warning('response returned error')
            raise BoxeeRPCException('Error returned in response')
       
        return jsonData

    def pair(self, passcode = None):
            
        if passcode is not None:        
            return self.pairRespond(passcode)
         
        logger.info('sending pairing request')
      
        params = {
            'deviceid': socket.gethostname(),
            'applicationid': self.appId,
            'label': 'Boxee Box Python Client',
            'icon': '',
            'type': 'other'
        }    
       
        data = self.createCall('Device.PairChallenge', params) 
        try:
            response = self.call(data)
        
            result = response['result']
            if result['success']:
                logger.info('pairing request successful')
                return True  
        except Exception, e:
            logger.exception('error sending pairing request: %s' % e)
            raise BoxeeRPCException('pairing failure') 
        
        return False

    def pairRespond(self, passcode):
        logger.info('sending pair response')
        
        params = {
            'deviceid': socket.gethostname(),
            'code': passcode
        }
        
        data = self.createCall('Device.PairResponse', params)
        try:   
            response = self.call(data) 
            result = response['result']
            if result['success']:
                logger.info('pairing response successful')
                return True 

        except Exception, e:
            logger.exception('error sending pair response: %s' % e) 
            raise BoxeeRPCException('pairing response failure') 

        return False;

    def connect(self):
        params = { 
            'deviceid': socket.gethostname()
        }
       
        data = self.createCall('Device.Connect', params)        

        logger.info('sending connect request')
        try:
            response = self.call(data) 
            result = response ['result']
            if result['success']:
                logger.info('connected successfully')
                return True 
        except Exception, e:
            logger.exception('error sending connect request')
            raise BoxeeRPCException('connect failure') 

        return False

    def unpair(self):
        
        params = {
            'deviceid': socket.gethostname()
        }

        data = self.createCall('Device.Unpair', params)

        logger.info('sending unpair request')
        try:
            response = self.call(data)
            result = response['result']
            if result['success']:
                logger.info('unpaired successfully')
                return True
        except Exception, e:
            logger.exception('error sending unpair request')
            raise BoxeeRPCException('unpair failure') 
            
        return False

    def notify(self, message):
        params = {
            'msg': message
        }

        data = self.createCall('GUI.NotificationShow', params)
        logger.info('sending notification')
        try:
            response = self.call(data)
            result = response['result']
            if result['success']:
               logger.info('sent notification, successfully')
               return True
        except Exception, e:
            logger.exception('error sending notification')
            raise BoxeeRPCException('notification failure') 
