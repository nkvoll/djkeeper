from django.utils import unittest
from django.conf import settings

import pykeeper
from djkeeper import manager


# TODO: clean up settings mangling, require Django 1.4 for tests?

class ManagerTest(unittest.TestCase):

    def setUp(self):
        if not settings.configured:
            settings.configure()

        settings.DJKEEPER = dict()

        pykeeper.install_log_stream()

    def tearDown(self):
        manager.ZooKeeperManager.reset()
        settings.DJKEEPER = dict()

        pykeeper.uninstall_log_stream()

    def test_get_client_with_no_configuration(self):
        self.assertEquals([], manager.ZooKeeperManager.get_configured_client_names())

        self.assertRaises(manager.NoSuchClientException, manager.ZooKeeperManager.get_or_create_client, 'foo')

    def test_get_client(self):
        settings.DJKEEPER = dict(clients=dict(foo=dict(), bar=dict(reconnect=False), baz=dict(servers='localhost:22181')))

        self.assertEquals(set(['foo', 'bar', 'baz']), set(manager.ZooKeeperManager.get_configured_client_names()))

        foo_client = manager.ZooKeeperManager.get_or_create_client('foo', auto_connect=False, wait_until_connected=False)
        self.assertIsInstance(foo_client, pykeeper.ZooKeeper)
        self.assertEquals(foo_client.state_name, None)
        self.assertEquals(foo_client.reconnect, True)

        self.assertEquals(set(['foo']), set(manager.ZooKeeperManager.get_created_client_names()))

        bar_client = manager.ZooKeeperManager.get_or_create_client('bar', auto_connect=False, wait_until_connected=False)
        self.assertEquals(bar_client.reconnect, False)

        self.assertEquals(set(['foo', 'bar']), set(manager.ZooKeeperManager.get_created_client_names()))

        baz_client = manager.ZooKeeperManager.get_or_create_client('baz', wait_until_connected_timeout=5)
        self.assertEquals(baz_client.state_name, 'connected')

        self.assertEquals(set(['foo', 'bar', 'baz']), set(manager.ZooKeeperManager.get_created_client_names()))