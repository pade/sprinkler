# -*- coding: UTF-8 -*-


import logging
import sys
from queue import Queue, Empty
import json

from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.exceptions import PubNubException
from pubnub.pubnub import PubNub, SubscribeListener
from pubnub.enums import PNReconnectionPolicy


class Messages():
    """Manage connexion with external device"""

    def __init__(self, subkey, pubkey, id):
        """Class constructor
        :param subkey: PubNub subscription key
        :param pubkey: PubNub publish key
        :param id: device id (UUID)
        """

        class MySubscribeListener(SubscribeListener):
            def __init__(self):
                self._logger = logging.getLogger('sprinkler')
                super().__init__()

            def message(self, pubnub, message):
                if message.message['sender'] != pubnub.uuid:
                    self._logger.debug(f"RECV from {message.message['sender']}: \
                        {message.message['content']}")
                    super().message(pubnub, message.message['content'])

        self._logger = logging.getLogger('sprinkler')

        self.message_listener = MySubscribeListener()
        self.messages = self.message_listener.message_queue

        pnconfig = PNConfiguration()
        pnconfig.subscribe_key = subkey
        pnconfig.publish_key = pubkey
        pnconfig.uuid = id
        pnconfig.reconnect_policy = PNReconnectionPolicy.LINEAR
        pnconfig.subscribe_timeout = 20
        self.pubnub = PubNub(pnconfig)
        self.pubnub.add_listener(self.message_listener)
        self.pubnub.subscribe().channels('sprinkler').execute()
        self.message_listener.wait_for_connect()

    def send(self, msg):
        try:
            self.pubnub.publish().channel("sprinkler")\
                .message({'sender': self.pubnub.uuid, 'content': msg}).sync()
            self._logger.debug(f"SEND from {self.pubnub.uuid}: {msg}")
        except PubNubException as e:
            self._logger.error("Sending error: " + str(e))

    def stop(self):
        self.pubnub.unsubscribe().channels('sprinkler').execute()
        self.message_listener.wait_for_disconnect()
        self.pubnub.stop()

    def get_message(self, timeout=None):
        try:
            return self.messages.get(timeout=timeout)
        except Empty:
            return None

    def is_message(self):
        return not self.messages.empty()
