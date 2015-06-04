from datetime import datetime
from urllib import urlencode
from urllib2 import urlopen
from StringIO import StringIO
from numpy import genfromtxt
import ast

station_ids = [ 2 ]

base_url = "http://data.hisparc.nl/api/station/%d/"

for id in station_ids:
	url = urlopen(base_url % (id))
	meta_data = url.read()
	print( meta_data )
