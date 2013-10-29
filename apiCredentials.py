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
                return None

    @property
    def webServicesUsername(self):
        return self.getConfigValue('Web Services', 'username')

    @property
    def webServicesSharedSecret(self):
        return self.getConfigValue('Web Services', 'shared_secret')

    def getApiEndPoint(self, end_point_label):
        if self.getConfigValue('API End Point', end_point_label) is not None:
            return self.getConfigValue('API End Point', end_point_label)
        else:
            return self.default_api_end_point