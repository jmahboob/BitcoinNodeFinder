import socket
import struct
import binascii
import hashlib

# Good node, we think
#HOST = '172.198.176.102'
# Test node
#HOST = '63.116.149.181'
# Known node
HOST = 'bitcoin.coinprism.com'
PORT = 8333


def craftBitcoinData():
	return "Test String."

def craftBitcoinHeader(data):
	print "Creating Custom Bitcoin Version Packet"
	to_send = ""

	# This is the known magic number for bitcoin (thanks documentation!)
	magic = 0xd9b4bef9
	magic_struct = struct.pack('I', magic)

	# First append 4-byte magic number
	to_send += magic_struct

	# Append 12 byte field for command, in this case "version"
	# Each character is UTF-8 so "version" is 7 + 5 null bytes is 12
	to_send += "version"
	to_send += "\x00\x00\x00\x00\x00"

	# Append 4 byte payload length field
	# Maybe we should figure out the payload first eh?
	data_len_struct = struct.pack('I', len(data))
	to_send += data_len_struct
	#to_send += "\x00\x00\x00\x00"

	# Append 4 byte checksum
	# checksum is first 4 bytes of sha256(sha256(<payload>))
	# Why? Because fuck you thats why.
	h1 = hashlib.sha256()
	h1.update(data)
	h2 = hashlib.sha256()
	h2.update(h1.hexdigest())
	checksum = h2.hexdigest()[0:8].decode("hex")
	to_send += checksum

	return to_send

def craftBitcoinPacket(header, data):
	return header + data

data = craftBitcoinData()
header = craftBitcoinHeader(data)
to_send = craftBitcoinPacket(header, data)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send(to_send)

data = s.recv(1024)

s.close()

print 'Received', repr(data)

