from unittest.mock import MagicMock

from cachetools import cached
from icat.client import Client

from datagateway_api.common.config import config
from datagateway_api.common.icat.icat_client_pool import create_client_pool
from datagateway_api.common.icat.lru_cache import ExtendedLRUCache


class TestLRUCache:
    def test_valid_cache_creation(self):
        test_cache = ExtendedLRUCache()
        assert test_cache.maxsize == config.get_client_cache_size()

    def test_valid_popitem(self):
        test_cache = ExtendedLRUCache()
        test_pool = create_client_pool()
        test_client = Client(
            config.get_icat_url(), checkCert=config.get_icat_check_cert(),
        )

        test_cache.popitem = MagicMock(side_effect=test_cache.popitem)

        @cached(cache=test_cache)
        def get_cached_client(cache_number, client_pool):
            return test_client

        for cache_number in range(config.get_client_cache_size() + 1):
            get_cached_client(cache_number, test_pool)

        assert test_cache.popitem.called
