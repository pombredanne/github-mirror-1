import pytest

from ghmirror.data_structures.monostate import RequestsCache
from ghmirror.data_structures.monostate import StatsCache


class TestStatsCache:

    def test_shared_state(self):
        stats_cache_01 = StatsCache()
        with pytest.raises(AttributeError) as e_info:
            stats_cache_01.foo
            assert 'object has no attribute' in e_info.message
        assert stats_cache_01.counter._value._value == 0

        stats_cache_01.count()
        stats_cache_01.count()

        assert stats_cache_01.counter._value._value == 2

        stats_cache_02 = StatsCache()
        assert stats_cache_02.counter._value._value == 2

        stats_cache_02.count()
        stats_cache_02.count()

        assert stats_cache_01.counter._value._value == 4
        assert stats_cache_02.counter._value._value == 4


class MockResponse:
    def __init__(self, content, headers, status_code):
        self.content = content.encode()
        self.headers = headers
        self.status_code = status_code

    def content(self):
        return self.content

    def headers(self):
        return self.headers

    def status_code(self):
        return self.status_code


class TestRequestsCache:

    @classmethod
    def setup_class(cls):
        cls.requests_cache_01 = RequestsCache()
        cls.requests_cache_01['foo'] = MockResponse(content='bar',
                                                    headers={},
                                                    status_code=200)

    def test_interface(self):
        assert list(self.requests_cache_01)
        assert 'foo' in self.requests_cache_01

    def test_shared_state(self):
        requests_cache_02 = RequestsCache()

        assert requests_cache_02['foo'].content == 'bar'.encode()
        assert requests_cache_02['foo'].status_code == 200
