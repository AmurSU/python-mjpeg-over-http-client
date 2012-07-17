#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Name:       Python M-JPEG Over HTTP Client Module
Version:    0.1
Purpose:    This module parses an MJPEG stream and retrieves actual images.
Author:     Sergey Lalov
Date:       2011-03-30
License:    GPL
Usage:      Connect twisted's reactor with MJPEGFactory(config)
Config
sample:     {'request': '/?action=stream',
              'login': 'admin',
              'password': 'admin',
              'callback': processImage}
            login and password are optional. callback is a function that takes
            one string argument - image data.
Target:     Cross Platform
Require:    Python 2.6+. Modules: zope.interface, twisted
"""
from twisted.internet.protocol import Protocol, ClientFactory
from base64 import b64encode
import re

debug = 1

class MJPEGClient(Protocol):
    def __init__(self):
        # A place for configuration parameters
        self.config = {}
        # I we are connected to a web server
        self.isConnected = False
        # The boundary in multipart stream
        self.boundary = ''
        # Actual image data goes here
        self.img = ''
        # Size of the image frame being downloaded
        self.next_img_size = 0
        # Indicates that currently parsing a header
        self.isHeader = False

    def connectionMade(self):
        # Implement basic authorization
        if self.config['login']:
            authstring = 'Authorization: Basic ' + b64encode(self.config['login']+':'+self.config['password']) + '\r\n'
        else:
            authstring = ''
        # Form proper HTTP request with header
        to_send = 'GET ' + self.config['request'] + ' HTTP/1.1\r\n' + \
            authstring + \
            'User-Agent: Python M-JPEG Client\r\n' + \
            'Keep-Alive: 300\r\n' + \
            'Connection: keep-alive\r\n\r\n'
        # Send it
        self.transport.write(to_send)
        if debug:
            print 'We say:\n', to_send
    
    def dataReceived(self, data):
        if debug:
            print 'Server said:\n', len(data), 'bytes of data.'
        if not self.isConnected:
            # Response header goes before empty line
            data_sp = data.strip().split('\r\n\r\n', 1)
            header = data_sp[0].splitlines()
            # Parse header
            for line in header:
                if line.endswith('200 OK'): # Connection went fine
                    self.isConnected = True
                    if debug: print 'Connected'
                if line.startswith('Content-Type: multipart'): # Got multipart
                    r = re.search(r'boundary="?(.*)"?', line)
                    self.boundary = r.group(1) # Extract boundary
                    if debug: print 'Got boundary:', self.boundary
            # If we got more data, find a JPEG there
            if len(data_sp) == 2:
                self.findJPEG(data_sp[1])
        else:
            # If connection is alredy made find a JPEG right away
            self.findJPEG(data)
    
    def findJPEG(self, data):
        hasMoreThanHeader = False
        # If we know next image size, than image header is already parsed
        if not self.next_img_size:
            # Otherwise it should be a header first
            for line in data.splitlines():
                if line == '--'+self.boundary:
                    self.isHeader = True
                    if debug: print 'Got frame header'
                elif line == '':
                    if self.isHeader:
                        # If we might have more data after a header in a buffer
                        hasMoreThanHeader = True
                    self.isHeader = False
                elif self.isHeader:
                    # Here we can parse all the header information
                    # But we are really interesed only in one
                    if line.startswith('Content-Length:'):
                        self.next_img_size = int(line.split(' ')[1])
                        if debug: print 'Next frame size:', self.next_img_size
                        
        else:
            # How many bytes left to read
            remains = self.next_img_size - len(self.img)
            self.img += data[:remains]
            # We got the whole image
            if len(self.img) == self.next_img_size:
                if debug: print 'Got a frame!'
                # Run a callback function
                self.config['callback'](self.img)
                # Reset variables
                self.img = ''
                self.next_img_size = 0
            # If something left in a buffer
            if data[remains:]:
                self.findJPEG(data[remains:])
        if hasMoreThanHeader:
            data_sp = data.split('\r\n\r\n', 1)
            # If there is something after a header in a buffer
            if len(data_sp) == 2:
                self.findJPEG(data_sp[1])

    def connectionLost(self, reason):
        print 'Connection lost, reconnecting'
        self.isConnected = False
        self.img = ''
        self.next_img_size = 0
        self.isHeader = 0
        self.boundary = ''

class MJPEGFactory(ClientFactory):
    def __init__(self, config):
        self.protocol = MJPEGClient
        self.config = config

    def buildProtocol(self, addr):
        prot = ClientFactory.buildProtocol(self, addr)
        # Weird way to pass the config parametrs to the protocol
        prot.config = self.config
        return prot

    def clientConnectionLost(self, connector, reason):
        # Automatic reconnection
        connector.connect()
