'''
Created on May 28, 2015

@author: local
'''

import sys
import argparse
import logging

logging.getLogger("spectrumbrowser").disabled = True


def setupConfig(host, configFile):
    configuration = Config.parse_local_config_file(configFile)
    configuration["HOST_NAME"] = host
    if not Config.isConfigured():
        Config.setSystemConfig(configuration)
    else:
        print "System is already configured -- not reconfiguring."


if __name__ == "__main__":
    sys.path.append("/opt/SpectrumBrowser/services/common")
    parser = argparse.ArgumentParser(description='Process command line args')
    parser.add_argument('-host', help='Host')
    parser.add_argument('-f', help='config file')
    args = parser.parse_args()
    configFile = args.f
    host = args.host
    import Config
    setupConfig(host, configFile)
