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
        self.port = int(self.config['port'])

    def get_default_config_help(self):
        config_help = super(DpdkLogCollector, self).get_default_config_help()
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

    def collect(self):
        recv_str = ""
        try:

            self.server_client = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            self.server_client.connect((self.hostname, self.port))

            self.log.info("connected")

#               self.server_client.settimeout(3)

            while True:
                rec = self.server_client.recv(128)
                if not rec:
                    break

                recv_str += rec

            recv_str = recv_str.decode("ascii")

            self.log.info("receive:{}".format(str(recv_str).split()))
        except socket.info:
            self.log.exception('Failed to get stats from %s:%s',
                               self.hostname, self.port)

        self.log.info("closing")
        self.server_client.close()

        self.log.info("publishing...")
        # publish numbers
        self.publish("dpdk_arg:", str(recv_str).split()[0])

        self.log.info("done")
