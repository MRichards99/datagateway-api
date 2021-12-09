import logging

from datagateway_api.src.search_api.session_handler import (
    client_manager,
    SessionHandler,
)


log = logging.getLogger()


# TODO - Make filters mandatory, if no filters are in a request an empty list will be
# given to these functions
@client_manager
def get_search(endpoint_name, entity_name, filters=[]):
    # TODO - `getApiVersion()` used as a placeholder for testing client handling
    # Replace with endpoint functionality when implementing the endpoints
    return SessionHandler.client.getApiVersion()


@client_manager
def get_with_id(endpoint_name, entity_name, id_, filters=None):
    pass


@client_manager
def get_count(endpoint_name, entity_name, filters=None):
    pass


@client_manager
def get_files(endpoint_name, entity_name, filters=None):
    pass


@client_manager
def get_files_count(endpoint_name, entity_name, id_, filters=None):
    pass