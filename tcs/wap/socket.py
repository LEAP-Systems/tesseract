"""
LEAP™ Socket Handler
====================
Contributors: Christian Sargusingh
Modified: 2020-08
Repository: https://github.com/LEAP-Org/LEAP
README available in repository root
Version: 

Dependencies
------------

Copyright © 2020 LEAP. All Rights Reserved.
"""

import os
import logging.config
import pickle
import socket
from threading import Thread

from tcs.event.registry import EventRegistry

class SocketHandler:
    
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        with EventRegistry as event:
            event.register('SHUTDOWN', self.shutdown)
            event.register('POST_REQUEST', self.post_request)
            event.register('GET_REQUEST', self.get_request)
        self.host = os.environ.get('HOSTNAME')
        self.port = int(os.environ.get('PORT'))
        # Uplink socket bind
        try:
            self.soc.bind((self.host, self.port))
        except ConnectionError as exc:
            # Protect against multiple instances by checking the server port
            self.log.exception(
                "TCU initialization failed. Server socket bind encountered a connection error: %s",
                exc)
            raise ConnectionError from exc
        else:
            self.log.info("Server socket bind successful. Initializing listener thread")
            Thread(target=self.request_listener, daemon=True).start()
        self.log.info("%s successfully instantiated", __name__)

    def request_listener(self):
        """
        """
        while True:
            self.log.info("Waiting for receiver request on port %s", self.port)
            self.soc.listen()
            #TODO: add dictionary of connected self.conn, self.addr tuples for concurrent ap connection
            self.conn, self.addr = self.soc.accept()
            self.log.info("Connected by device at: %s", self.addr)
            # receive a bitarray object
            apr = self.get_request()
            self.log.info("Validating received APR key: %s", apr)
            # APR verification
            with EventRegistry() as event:
                event.execute('VALIDATE_APR', apr)

    def post_request(self, obj:object, msg:str=""):
        """
        This function is bound to event:POST_REQUEST. It pickles an object to the client and sends
        an optional message.

        :param obj: object to pickle to client
        :param msg: optional message to client
        """
        with self.conn as conn:
            conn.send(pickle.dumps(obj))
            if len(msg) > 0:
                conn.send((msg).encode('utf-8'))

    def get_request(self, size:int=2048):
        """
        This function is bound to event:POST_REQUEST. It pickles an object to the client and sends
        an optional message.

        :param size: size for byte load (default fo 2048)
        :return: object pickled from client
        """
        with self.conn as conn:
            return pickle.loads(conn.recv(size))

    def shutdown(self):
        """
        This function is bound to event:SHUTDOWN. It simply closes the active socket
        """
        self.log.info("Closing network sockets...")
        self.soc.close()
        self.log.info("socket shutdown complete")