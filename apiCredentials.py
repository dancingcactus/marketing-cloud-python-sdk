#!/usr/bin/python
import sys
import ConfigParser

class ApiCredentials(ConfigParser.ConfigParser):
    def __init__(self, config_file):
        ConfigParser.ConfigParser.__init__(self)
        self.read(config_file)
        self.default_api_end_point = 'https://api.omniture.com/admin/1.3/rest/'

    def getConfigValue(self, config_section, config_key):
        if config_section not in self.sections():
            print '%s not a valid config section'
            sys.exit(1)
        else:
            try:
                return self.get(config_section, config_key)
            except ConfigParser.NoOptionError, e:
                print 'Failed to retrive value for %s in section %s' % (config_key, config_section)
                sys.exit(1)

    @property
    def webServicesUsername(self):
        return self.getConfigValue('Web Services', 'username')

    @property
    def webServicesSharedSecret(self):
        return self.getConfigValue('Web Services', 'shared_secret')

    def getApiEndPoint(self, end_point_label):
        return self.getConfigValue('API End Point', end_point_label)