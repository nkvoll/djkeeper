import threading

from django.conf import settings

import pykeeper


class NoSuchClientException(Exception):
    pass


class ZooKeeperManager(object):
    _clients = dict()
    _client_create_lock = threading.Lock()

    @classmethod
    def get_or_create_client(cls, name, auto_connect=True, wait_until_connected=True, wait_until_connected_timeout=None):
        client = cls._get_or_create_client(name, auto_connect)
        if wait_until_connected:
            client.wait_until_connected(timeout=wait_until_connected_timeout)
        return client

    @classmethod
    def get_configured_client_names(cls):
        return cls._get_client_configurations().keys()

    @classmethod
    def get_created_client_names(cls):
        return cls._clients.keys()

    @classmethod
    def reset(cls):
        with cls._client_create_lock:
            clients = cls._clients.values()
            cls._clients.clear()

            for client in clients:
                client.close()

    @classmethod
    def _get_or_create_client(cls, name, auto_connect):
        if name not in cls._clients:
            with cls._client_create_lock:
                if name not in cls._clients:

                    kwargs = cls.get_client_kwargs(name)

                    client = pykeeper.ZooKeeper(**kwargs)
                    cls._clients[name] = client
                    if auto_connect:
                        client.connect()

        client = cls._clients[name]
        return client

    @classmethod
    def get_client_kwargs(cls, name):
        client_configurations = cls._get_client_configurations()

        if not name in client_configurations:
            raise NoSuchClientException(name)

        client_settings = client_configurations.get(name, dict())

        # Get a copy of the client settings to avoid potentially changing the original
        client_settings = dict(client_settings)
        client_settings.setdefault('servers', 'localhost:2181')
        client_settings.setdefault('reconnect', True)

        return client_settings

    @classmethod
    def _get_client_configurations(cls):
        return getattr(settings, 'DJKEEPER', dict()).get('clients', dict())