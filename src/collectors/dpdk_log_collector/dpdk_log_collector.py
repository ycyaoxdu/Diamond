# coding=utf-8

"""
The DpdkLogCollector uses the socket to receive dpdk logs.
"""

import diamond.collector
import socket

class DpdkLogCollector(diamond.collector.Collector):

    def process_config(self):
        super(DpdkLogCollector, self).process_config()
        self.hostname = self.config['hostname']
        self.port = self.config['port']
        self.server_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       

    def get_default_config_help(self):
        config_help =  super(DpdkLogCollector, self).get_default_config_help()
        config_help.update({
            'hostname': 'Hostname',
            'port': 'Port',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(DpdkLogCollector, self).get_default_config()
        config['hostname'] = 'localhost'
        config['port'] = 8888

        config.update({
            'path': 'dpdk_log'
        })
        return config

    def collect(self ):
        # TODO: should connect and close in this function? 
        self.server_client.connect((self.hostname, self.port)) 
       
        recv_str = self.server_client.recv(128)
        recv_str = recv_str.decode("ascii")
        print("receive:{}".format(recv_str))

        # publish numbers
        self.publish("numbers:", str(recv_str).split( )[-1])

