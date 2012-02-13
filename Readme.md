# djkeeper: Utilities for using ZooKeeper in a Django project


## Installing

Either install the latest relase from PYPI:

    $ pip install djkeeper

... or get the latest development version from GitHub:

    $ pip install https://github.com/nkvoll/djkeeper/zipball/master#egg=djkeeper

Additionally, djkeeper requires a working installation of the official low level Python ZooKeeper bindings. These can either be built from source (recommended, explanation below), or
you could install the statically compiled version [zc-zookeeper-static](http://pypi.python.org/pypi/zc-zookeeper-static)) from PYPI, which may or may not work on your architecture/OS, and may
or may not be the latest available ZooKeeper version.


### Installing ZooKeeper on OS X (homebrew)

If you don't have homebrew, follow the Linux installation below, skipping "ldconfig", otherwise, use homebrew to install zookeeper with the ``--python`` flag:

    $ brew install --python zookeeper


### Installing ZooKeeper on Linux

Download and unpack the latest release of ZooKeeper from http://zookeeper.apache.org/releases.html:

    $ tar -zxvf zookeeper-3.4.2.tar.gz

Build the C bindings:

    $ cd zookeeper-3.4.2/src/c
    $ ./configure --prefix=/usr/local
    $ make
    $ sudo make install
    $ ldconfig

Build and install the python bindings:

    $ cd ../contrib/zkpython
    $ ant install


## Running the test-suite

The test suite assumes you have a ZooKeeper server running on localhost:22181:

    $ cd example
    $ export ZOOCFGDIR=$(pwd) zkServer start-foreground

zkServer / zkServer.sh is found in the ZooKeeper installation directory.

The tests can then be run via the setup.py script:

    $ python setup.py test


## Example usage with Django

See https://github.com/nkvoll/pykeeper/blob/master/Readme.md for more detailed usage of the client object instance.

### Configuring:

ZooKeeper clients are configured in your ``settings.py`` file under the configuration key ``DJKEEPER``:

    DJKEEPER = dict(
        clients = dict(
            client_name = dict(
                servers = 'localhost:22181', # defaults to localhost:2181
                reconnect = True # defaults to True, which means the client should reconnect if the connection is lost
            )
        )
    )

Multiple named clients can be configured this way.

### Using in a view:

For example, in ``views.py``:

    from django.http import HttpResponse
    from djkeeper import manager


    def index(request):
        client = manager.ZooKeeperManager.get_or_create_client('client_name')
        root_children = client.get_children('/')
        return HttpResponse('Root children: {0}'.format(root_children))


``manager.ZooKeeperManager`` accepts the following keyword parameters:

    * ``auto_connect``: Whether to call .connect() on a newly created client before returning it. Defaults to true.
    * ``wait_until_connected``: Whether to block until the client state becomes ``connected`` before returning the client. Defaults to true.
    * ``wait_until_connected_timeout``: How long the call is allowed to block (in seconds) before a ``pykeeper.TimeoutException`` is raised. Defaults to ``None``, which means no timeout.


### Admin-overview

First, add ``djkeeper`` to your list of ``INSTALLED_APPS`` in settings.py, then
add the following route to your urls.py:

    #...
    url(r'^admin/djkeeper/', 'djkeeper.views.index'),
    #...

Or, if you use [django-adminplus](https://github.com/jsocol/django-adminplus), an overview over the clients is automatically
added to the admin panel when you call ``admin.autodiscover()``. In this case, the custom route should NOT be added to your urls.py.


## License

MIT licensed, see LICENSE for details.