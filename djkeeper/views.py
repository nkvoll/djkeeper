from django.contrib.admin.views import decorators
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from djkeeper import manager


STATE_TO_COLOR = dict(
    connected = 'green',
    connecting = 'darkorange'
)


def _create_client_context(client_name, has_instance):
    client = dict(name=client_name)

    client['settings'] = manager.ZooKeeperManager.get_client_kwargs(client_name)

    if has_instance:
        instance = manager.ZooKeeperManager.get_or_create_client(client_name, wait_until_connected=False)
        client['instance'] = instance
        client['state_color'] = STATE_TO_COLOR[instance.state_name]
    return client


def unprotected_index(request):
    context = dict(title='djkeeper')

    context['clients'] = clients = dict()

    clients['all'] = manager.ZooKeeperManager.get_configured_client_names()

    active_client_names = manager.ZooKeeperManager.get_created_client_names()
    clients['active'] = [_create_client_context(client_name, True) for client_name in active_client_names]

    inactive_client_names = [client_name for client_name in clients['all'] if client_name not in active_client_names]
    clients['inactive'] = [_create_client_context(client_name, False) for client_name in inactive_client_names]

    return render_to_response('djkeeper/index.html',
                              context, RequestContext(request, dict()))


# create the protected version of index:
index = decorators.staff_member_required(unprotected_index)
