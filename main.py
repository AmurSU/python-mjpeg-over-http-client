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
Require:    Python 2.7+. Modules: zope.interface, twisted
"""
from twisted.internet import reactor

from http_mjpeg_client import MJPEGFactory

import argparse

def processImage(img):
    'This function is invoked by the MJPEG Client protocol'
    # Process image
    # Just save it as a file in this example
    f = open(config['filename'], 'wb')
    f.write(img)
    f.close()
    
config = {
    'callback': processImage,
}

def main():
    # Retrieve configuration from command line arguments
    parser = argparse.ArgumentParser(description='Tool for grabbing frames from MJPEG over HTTP video stream to image file.')
    parser.add_argument('--request', metavar='PATH', required=True,
                        help='a path in the server to request for the videostream')
    parser.add_argument('--ip', required=True, help='Remote server IP-address')
    parser.add_argument('--port', type=int, default=80,
                        help='Remote server port (default: 80)')
    parser.add_argument('--login', help='Username for authentication (optional)')
    parser.add_argument('--password', help='Password for authentication (optional)')
    parser.add_argument('--filename', default='frame.jpg', help='A file name to save frames (default: frame.jpg)')
    args = parser.parse_args()
    # Define connection parameters, login and password are optional.
    config.update(vars(args))
    # Make a connection
    print 'Python M-JPEG Over HTTP Client 0.1'
    reactor.connectTCP(config['ip'], config['port'], MJPEGFactory(config))
    reactor.run()    
    print 'Python M-JPEG Client stopped.'

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
