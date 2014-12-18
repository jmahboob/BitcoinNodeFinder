import socket
import struct
import binascii
import hashlib
import sys, re
if sys.version_info.major < 3:
	sys.stderr.write('Sorry, Python 3.x needed :(\n')
	sys.exit(1)
from bitcoin import SelectParams
from bitcoin.messages import msg_version

# Good node, we think
#HOST = '172.198.176.102'
# Test node
#HOST = '63.116.149.181'
# Known node
#HOST = 'bitcoin.coinprism.com'
PORT = 8333

HOSTS = ['136.227.27.142', \
	'136.227.28.45', \
	'75.104.60.47', \
	'75.104.60.190', \
	'136.227.27.93', \
	'123.138.54.159', \
	'24.17.108.172', \
	'123.58.55.110', \
	'136.227.111.41', \
	'159.19.99.225', \
	'69.207.178.52', \
	'bitcoin.coinprism.com']

for HOST in HOSTS:

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(1)

	data = ""

	try:
		s.connect((HOST, PORT))
		msg = msg_version()
		s.send(msg.to_bytes())
		data = s.recv(1024)
	except socket.timeout:
		print("Timeout")
	except socket.error:
		print("No clue but error")

	if re.search("Satoshi", str(data)):
		print(HOST, " Hurray! :)\n")
	else:
		print(HOST, " Boo! :(\n")

	s.close()
