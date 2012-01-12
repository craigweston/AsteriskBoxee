#!/usr/bin/env python

import socket
import json
import logging
import sys

from uuid import getnode as get_mac

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) 
log_handler = logging.StreamHandler(sys.stdout)
log_handler.setLevel(logging.DEBUG)
logger.addHandler(log_handler) 

class BoxeeRPCException(Exception):
    def  __init__(self, message):
       self.message = message

    def __str__(self):
        return repr(self.message)
        

class RPC:
    
    def __init__(self, host, port, appId = 'Boxee RPC Client'):
        self.socket = None  
        self.deviceId = str(get_mac())
        self.appId = appId
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
        self.open()
        try:
            self.socket.send(data) 
            return self.parseResponse()
        finally:
            self.close()

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
            'deviceid': self.deviceId,
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
            logger.exception('error sending pairing request')
            raise BoxeeRPCException('pairing failure') 
        
        return False

    def pairRespond(self, passcode):
        logger.info('sending pair response')
        
        params = {
            'deviceid': self.deviceId,
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
            logger.exception('error sending pair response')
            raise BoxeeRPCException('pairing response failure') 

        return False;

    def connect(self):
        params = { 
            'deviceid': self.deviceId 
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
            'deviceid': self.deviceId
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
