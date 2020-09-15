import configparser
import irc.client
import sys


from client import IRCClient
from clientdirect import IRCDirectClient

CONFIG_FILE = "config.ini"


def main():
	if len(sys.argv) < 4:
		print("Usage: python3 main.py <env> <bot_name> <file_number>")
		sys.exit(1)
	environnement = "IRC_" + sys.argv[1]
	bot_name = sys.argv[2]
	file_number = sys.argv[3]

	config = configparser.ConfigParser()
	config.read(CONFIG_FILE)

	if not environnement in config:
		print("Configuration missing")
		sys.exit(1)
	irc_config = config[environnement]
	server = irc_config["server"]
	port = irc_config["port"]
	nickname = irc_config["nickname"]

	if "master_bot" in config:
		client = IRCClient(irc_config, bot_name, file_number)
	else:
		client = IRCDirectClient(irc_config, bot_name, file_number)

	try:
		client.connect(server, int(port), nickname)
	except irc.client.ServerConnectionError as error:
		print(error)
		sys.exit(1)
	client.start()



if __name__ == "__main__":
	main()


