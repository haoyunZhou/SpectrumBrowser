import unittest
import json
import requests
import argparse
import os
import socket
import ssl


class  ConfigTest(unittest.TestCase):
    def setUp(self):
        global host
        global webPort
        self.sensorId = "E6R16W5XS"
        self.serverUrlPrefix = "https://" + host + ":" + webPort
        print "serverUrlPrefix = " + self.serverUrlPrefix
        f = open("./Config.unittest.txt")
        str = f.read()
        self.config = eval(str)

    def tearDown(self):
        print "Done."

    def test_get_streaming_port(self):
        r = requests.post(self.serverUrlPrefix + "/sensordata/getStreamingPort/" + self.sensorId,verify=False)
        retval = r.json()
        print json.dumps(retval, indent=4)
        streamingPort = int(retval["port"])
        self.assertTrue(streamingPort == self.config["STREAMING_SERVER_PORT"])
        global host
        try :
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock = ssl.wrap_socket(s)
            sock.connect((host, streamingPort))
            sock.close()
        except:
            self.fail("Failed to connect")

    def test_get_monitoring_port(self):
        r = requests.post(self.serverUrlPrefix + "/sensordata/getMonitoringPort/" + self.sensorId,verify=False)
        retval = r.json()
        print json.dumps(retval, indent=4)
        monitoringPort = int(retval["port"])
        self.assertTrue(monitoringPort == self.config["OCCUPANCY_ALERT_PORT"])
        global host
        try :
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock = ssl.wrap_socket(s)
            sock.connect((host, monitoringPort))
            sock.close()
        except:
            self.fail("Failed to connect")

    def test_get_sensor_config(self):
        r = requests.post(self.serverUrlPrefix + "/sensordb/getSensorConfig/" + self.sensorId,verify=False)
        jsonVal = r.json()
        print json.dumps(jsonVal, indent=4)
        self.assertTrue(json != None)
        self.assertTrue(jsonVal["sensorConfig"]["SensorID"] == self.sensorId)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process command line args")
    parser.add_argument("-host",help="Server host.")
    parser.add_argument("-port",help="Server port.")
    args = parser.parse_args()
    global host
    global webPort
    host = args.host
    if host == None:
        host = os.environ.get("MSOD_WEB_HOST")
    webPort = args.port
    if webPort == None:
       webPort = "443"

    if host == None or webPort == None:
        print "Require host and web port"
    webPortInt = int(webPort)
    if webPortInt < 0 :
        print "Invalid params"
        os._exit()
    suite = unittest.TestLoader().loadTestsFromTestCase(ConfigTest)
    unittest.TextTestRunner(verbosity=2).run(suite)



