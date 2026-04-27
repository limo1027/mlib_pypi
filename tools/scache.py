# scache.py - 缓存工具模块


class LRUCache:
    """最近最少使用缓存 (Least Recently Used Cache)"""

    def __init__(self, max_size=100):
        """初始化 LRU 缓存"""
        self._max_size = max_size
        self._cache = {}
        self._order = []

    def get(self, key, default=None):
        """获取缓存值"""
        if key not in self._cache:
            return default

        self._order.remove(key)
        self._order.append(key)

        return self._cache[key]

    def set(self, key, value):
        """设置缓存"""
        if key in self._cache:
            self._order.remove(key)
        elif len(self._cache) >= self._max_size:
            oldest = self._order.pop(0)
            del self._cache[oldest]

        self._cache[key] = value
        self._order.append(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __getitem__(self, key):
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value

    def __contains__(self, key):
        return key in self._cache

    def pop(self, key, default=None):
        """移除并返回缓存"""
        if key not in self._cache:
            return default

        self._order.remove(key)
        value = self._cache.pop(key)
        return value

    def clear(self):
        """清空缓存"""
        self._cache.clear()
        self._order.clear()

    def keys(self):
        """所有键"""
        return list(self._cache.keys())

    def values(self):
        """所有值"""
        return list(self._cache.values())

    def items(self):
        """所有键值对"""
        return list(self._cache.items())

    @property
    def size(self):
        """当前缓存数量"""
        return len(self._cache)

    @property
    def max_size(self):
        """最大缓存数量"""
        return self._max_size

    def __len__(self):
        return len(self._cache)

    def __repr__(self):
        return f"LRUCache(size={len(self._cache)}, max_size={self._max_size})"


class CacheEntry:
    """缓存条目（带过期时间）"""

    def __init__(self, key, value, ttl=None):
        """初始化缓存条目"""
        self.key = key
        self.value = value
        self.ttl = ttl
        self.access_count = 0
        self.last_access = 0

    def is_expired(self, current_time):
        """检查是否过期"""
        if self.ttl is None:
            return False
        return current_time > self.ttl


class TTLCache:
    """带过期时间的缓存"""

    def __init__(self, max_size=100, default_ttl=None):
        """初始化 TTL 缓存"""
        self._max_size = max_size
        self._default_ttl = default_ttl
        self._cache = {}

    def get(self, key, default=None, current_time=0):
        """获取缓存值"""
        if key not in self._cache:
            return default

        entry = self._cache[key]

        if entry.ttl is not None and current_time > entry.ttl:
            del self._cache[key]
            return default

        entry.access_count += 1
        entry.last_access = current_time

        return entry.value

    def set(self, key, value, ttl=None, current_time=0):
        """设置缓存"""
        if ttl is None:
            ttl = self._default_ttl

        if ttl is not None:
            ttl = current_time + ttl

        if key not in self._cache and len(self._cache) >= self._max_size:
            self._evict_lru()

        self._cache[key] = CacheEntry(key, value, ttl)

    def _evict_lru(self):
        """驱逐最少使用的条目"""
        if not self._cache:
            return

        lru_key = min(self._cache.keys(), key=lambda k: self._cache[k].last_access)
        del self._cache[lru_key]

    def clear(self):
        """清空缓存"""
        self._cache.clear()

    def remove_expired(self, current_time):
        """移除所有过期条目"""
        expired_keys = [
            key for key, entry in self._cache.items()
            if entry.ttl is not None and current_time > entry.ttl
        ]

        for key in expired_keys:
            del self._cache[key]

        return len(expired_keys)

    @property
    def size(self):
        """当前缓存数量"""
        return len(self._cache)

    def __len__(self):
        return len(self._cache)

    def __repr__(self):
        return f"TTLCache(size={len(self._cache)}, max_size={self._max_size})"


class _MemoizeFunc:
    """记忆化装饰器（内部类）"""

    def __init__(self, func, max_size=128):
        self._func = func
        self._cache = LRUCache(max_size)

    def __call__(self, *args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))

        if key in self._cache:
            return self._cache.get(key)

        result = self._func(*args, **kwargs)
        self._cache.set(key, result)
        return result

    def clear(self):
        """清空缓存"""
        self._cache.clear()

    def __repr__(self):
        return f"<memoized function: {self._func.__name__}>"


def memoize(max_size=128):
    """记忆化装饰器"""
    def decorator(func):
        return _MemoizeFunc(func, max_size)
    return decorator


class RingBuffer:
    """环形缓冲区 - 固定大小的 FIFO 缓冲区"""

    def __init__(self, capacity):
        """初始化环形缓冲区"""
        self._capacity = capacity
        self._buffer = [None] * capacity
        self._head = 0
        self._tail = 0
        self._size = 0

    def push(self, item):
        """添加元素"""
        self._buffer[self._tail] = item
        self._tail = (self._tail + 1) % self._capacity

        if self._size < self._capacity:
            self._size += 1
        else:
            self._head = (self._head + 1) % self._capacity

    def pop(self):
        """弹出元素"""
        if self._size == 0:
            raise IndexError("Buffer is empty")

        item = self._buffer[self._head]
        self._buffer[self._head] = None
        self._head = (self._head + 1) % self._capacity
        self._size -= 1

        return item

    def peek(self):
        """查看队首元素"""
        if self._size == 0:
            raise IndexError("Buffer is empty")
        return self._buffer[self._head]

    def clear(self):
        """清空缓冲区"""
        self._buffer = [None] * self._capacity
        self._head = 0
        self._tail = 0
        self._size = 0

    def __len__(self):
        return self._size

    @property
    def capacity(self):
        """容量"""
        return self._capacity

    def is_empty(self):
        """是否为空"""
        return self._size == 0

    def is_full(self):
        """是否已满"""
        return self._size == self._capacity

    def __repr__(self):
        return f"RingBuffer(size={self._size}, capacity={self._capacity})"


class CacheStats:
    """缓存统计"""

    def __init__(self):
        self._hits = 0
        self._misses = 0
        self._evictions = 0

    def record_hit(self):
        """记录命中"""
        self._hits += 1

    def record_miss(self):
        """记录未命中"""
        self._misses += 1

    def record_eviction(self):
        """记录驱逐"""
        self._evictions += 1

    @property
    def hits(self):
        """命中次数"""
        return self._hits

    @property
    def misses(self):
        """未命中次数"""
        return self._misses

    @property
    def evictions(self):
        """驱逐次数"""
        return self._evictions

    @property
    def total_requests(self):
        """总请求数"""
        return self._hits + self._misses

    @property
    def hit_rate(self):
        """命中率"""
        total = self.total_requests
        if total == 0:
            return 0.0
        return self._hits / total

    def reset(self):
        """重置统计"""
        self._hits = 0
        self._misses = 0
        self._evictions = 0

    def __repr__(self):
        return f"CacheStats(hits={self._hits}, misses={self._misses}, hit_rate={self.hit_rate:.2%})"
