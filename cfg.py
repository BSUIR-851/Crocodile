import configparser
import os

def getValues(configFileName, sections, options):
	baseHost, basePort = 'localhost', 49100
	addressSection = sections[0]
	hostOpt, portOpt = options[0], options[1]
	validSections = [addressSection]
	validOptions = [hostOpt, portOpt]

	config = configparser.ConfigParser()

	try:
		if os.path.exists(configFileName):
			config.read(configFileName)
			try:
				host = config.get(addressSection, hostOpt)
				port = config.getint(addressSection, portOpt)

			except configparser.NoSectionError:
				config.add_section(addressSection)
				config.set(addressSection, hostOpt, baseHost)
				host = baseHost
				config.set(addressSection, portOpt, str(basePort))
				port = basePort

			except configparser.NoOptionError:
				if not config.has_option(addressSection, hostOpt):
					config.set(addressSection, hostOpt, baseHost)
					host = baseHost
				else:
					host = config.get(addressSection, hostOpt)

				if not config.has_option(addressSection, portOpt):
					config.set(addressSection, portOpt, str(basePort))
					port = basePort
				else:
					port = config.getint(addressSection, portOpt)

			finally:
				with open(configFileName, 'w') as configFile:
					config.write(configFile)

		else:
			config.add_section(addressSection)
			config.set(addressSection, hostOpt, baseHost)
			config.set(addressSection, portOpt, str(basePort))
			host = baseHost
			port = basePort

	finally:
		sects = config.sections().copy()
		for sect in sects:
			if sect not in validSections:
				config.remove_section(sect)
			else:
				opts = config.options(sect).copy()
				for opt in opts:
					if opt not in validOptions:
						config.remove_option(sect, opt)
						
		with open(configFileName, 'w') as configFile:
			config.write(configFile)

	return host, port



