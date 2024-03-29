replay = __import__('exercise').replay
Cache = __import__('exercise').Cache


cache = Cache()
cache.store("foo")
cache.store("bar")
cache.store(42)
replay(cache.store)
