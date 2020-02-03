import irc.client

from jaraco.stream import buffer
irc.client.ServerConnection.buffer_class = buffer.LenientDecodingLineBuffer


class IRCClient(irc.client.SimpleIRCClient):
	def __init__(self, config, bot_name, file_number):
		irc.client.SimpleIRCClient.__init__(self)

		self.bot_name = bot_name
		self.file_number = file_number
		self.master_bot = config["master_bot"]
		self.private_channel = config["private_channel"]
		self.debug = config["debug"]


def dprint(msg):
	global debug
	if debug:
		print(msg)


