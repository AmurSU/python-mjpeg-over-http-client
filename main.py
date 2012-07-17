#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Name:       Python M-JPEG Over HTTP Client Program
Version:    0.1
Purpose:    This program connects to an MJPEG stream and saves retrived images.
Author:     Sergey Lalov
Date:       2011-03-30
License:    GPL
Target:     Cross Platform
Require:    Python 2.6+. Modules: zope.interface, twisted
"""
from twisted.internet import reactor

from http_mjpeg_client import MJPEGFactory

def processImage(img):
    'This function is invoked by the MJPEG Client protocol'
    # Process image
    # Just save it as a file in this example
    f = open('frame.jpg', 'wb')
    f.write(img)
    f.close()
    
def main():
    print 'Python M-JPEG Over HTTP Client 0.1'
    # Define connection parameters, login and password are optional.
    config = {'request': '/?action=stream',
              'login': 'admin',
              'password': 'admin',
              'ip': '127.0.0.1',
              'port': 8080,
              'callback': processImage}
    # Make a connection
    reactor.connectTCP(config['ip'], config['port'], MJPEGFactory(config))
    reactor.run()    
    print 'Python M-JPEG Client stopped.'

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
