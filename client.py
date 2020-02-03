import irc.client
import os
import shlex
import struct
import sys

from jaraco.stream import buffer
irc.client.ServerConnection.buffer_class = buffer.LenientDecodingLineBuffer

debug = False


class IRCClient(irc.client.SimpleIRCClient):
	def __init__(self, config, bot_name, file_number):
		irc.client.SimpleIRCClient.__init__(self)

		self.bot_name = bot_name
		self.file_number = file_number
		self.nickname = config["nickname"]
		self.master_bot = config["master_bot"]
		self.private_channel = config["private_channel"]
		self.secret = config["secret"]
		self.received_bytes = 0

		global debug
		debug = config["debug"]
		dprint(" === Starting client ")


	def on_welcome(self, connection, event):
		dprint(" === Sending invitation request to " + self.master_bot)
		self.connection.privmsg(self.master_bot, "enter " + self.private_channel + " " + self.nickname + " " + self.secret)


	def on_invite(self, connection, event):
		if event.arguments[0] == self.private_channel:
			dprint(" === Joining private channel " + self.private_channel)
			self.connection.join(self.private_channel)


	def on_join(self, connection, event):
		if event.target == self.private_channel:
			dprint(" === Requesting file " + self.file_number + " to " + self.bot_name)
			self.connection.privmsg(self.bot_name, "xdcc get " + self.file_number)


	def on_ctcp(self, connection, event):
		payload = event.arguments[1]
		parts = shlex.split(payload)
		command, filename, peer_address, peer_port, size = parts
		if command != "SEND":
			return
		self.filename = os.path.basename(filename)
		self.file = open(self.filename, "wb")
		peer_address = irc.client.ip_numstr_to_quad(peer_address)
		peer_port = int(peer_port)
		self.dcc = self.dcc_connect(peer_address, peer_port, "raw")


	def on_dccmsg(self, connection, event):
		data = event.arguments[0]
		self.file.write(data)
		self.received_bytes = self.received_bytes + len(data)
		self.dcc.send_bytes(struct.pack("!I", self.received_bytes))


	def on_dcc_disconnect(self, connection, event):
		self.file.close()
		dprint(" === Received " + self.filename)
		self.connection.quit()


	def on_disconnect(self, connection, event):
		sys.exit(0)


def dprint(msg):
	global debug
	if debug:
		print(msg)


