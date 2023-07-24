import requests
from cachecontrol import CacheControl, serialize
from cachecontrol.caches.file_cache import FileCache
from cachecontrol.heuristics import LastModified


def get_cached_session() -> requests.Session:
    """
    Create a local requests cache in the hidden
    .cache directory.
    """
    session = CacheControl(
        requests.Session(),
        cache=FileCache(".cache"),
        serializer=serialize.Serializer(),
        heuristic=LastModified(),
    )
    return session
