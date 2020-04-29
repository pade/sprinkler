# -*- coding: UTF-8 -*-


import logging
import json
import asyncio
from pubnub.pnconfiguration import PNConfiguration
from pubnub.enums import PNStatusCategory
from pubnub.pubnub_asyncio import PubNubAsyncio, SubscribeListener
from pubnub.enums import PNReconnectionPolicy


class Messages:
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

            def status(self, pubnub, status):
                if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
                    # This event happens when radio / connectivity is lost
                    self._logger.error("Unexpected disconnection")

                elif status.category == PNStatusCategory.PNConnectedCategory:
                    # Connect event. You can do stuff like publish, and know you'll get it.
                    # Or just use the connected event to confirm you are subscribed for
                    # UI / internal notifications, etc
                    self._logger.info("Connection OK")

                elif status.category == PNStatusCategory.PNReconnectedCategory:
                    # Happens as part of our regular operation. This event happens when
                    # radio / connectivity is lost, then regained.
                    self._logger.info("Reconnection OK")
                elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
                    # Handle message decryption error. Probably client configured to
                    # encrypt messages and on live data feed it received plain text.
                    self._logger.error("Decryption error")
                super().status(pubnub, status)

            def message(self, pubnub, message):
                if message.publisher != pubnub.uuid:
                    self._logger.debug(f"RECV from {message.publisher}: \
                        {json.dumps(message.message['content'])}")
                    super().message(pubnub, message.message['content'])

        self._logger = logging.getLogger('sprinkler')
        self.message_listener = MySubscribeListener()
        self.messages = self.message_listener.message_queue

        pnconfig = PNConfiguration()
        pnconfig.subscribe_key = subkey
        pnconfig.publish_key = pubkey
        pnconfig.uuid = id
        pnconfig.ssl = True
        pnconfig.reconnect_policy = PNReconnectionPolicy.LINEAR
        pnconfig.subscribe_timeout = 20
        self.pubnub = PubNubAsyncio(pnconfig)
        self.pubnub.add_listener(self.message_listener)
        self.pubnub.subscribe().channels('sprinkler').execute()

    def publish_callback(self, task):
        exception = task.exception()
        if exception is not None:
            self._logger.error(f"Sending error: {str(exception)}")

    async def send(self, msg):
        t = asyncio.create_task(self.pubnub.publish().channel("sprinkler").message({'content': msg}).future()). \
            add_done_callback(self.publish_callback)
        self._logger.debug(f"SEND from {self.pubnub.uuid}: {json.dumps(msg)}")

    async def stop(self):
        #self.pubnub.unsubscribe().channels('sprinkler').execute()
        #try:
        #    self.message_listener.wait_for_disconnect()
        #except:
            # Already disconnected
        #    pass
        await self.pubnub.stop()
        self._logger.debug("Message manager stopped")

    async def get_message(self):
        return await self.messages.get()

    def is_message(self):
        return not self.messages.empty()
