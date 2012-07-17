Python MJPEG over HTTP client
=============================

A program and library, that connects to web server, parses MJPEG video stream and save video frames to a file.

Usage
-----

	./main.py --request /video/mjpg.cgi?profileid=2 --ip 192.168.1.5 --port 80 --login login --password my_secure_password --filename videoframe.jpg

Authors
-------

Original author: Sergey Lalov

Original source code can be found at [Google code][origin].

The original source code was adopted and fixed by Andrey Novikov in 2012 for Amur State University.

As of summer 2012, this software is used in university [swimming pool construction webpage][pool].

License
-------

This software is licensed under [GNU General Public License][GNU GPL] and distributed AS IS, without warranties of any kind.

[origin]: http://code.google.com/p/python-mjpeg-over-http-client/ "Original project page"
[pool]: http://pool.amursu.ru/
[GNU GPL]: http://opensource.org/licenses/gpl-3.0.html "GNU General Public License text"
