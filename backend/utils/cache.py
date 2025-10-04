"""
Cache utilities for ExoScout Backend.

Provides caching functionality using diskcache for NASA API responses
and light curve data to improve performance and reduce API calls.
"""

import os
import logging
from typing import Any, Optional, Callable
from functools import wraps

import diskcache as dc
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Cache configuration
CACHE_DIR = os.getenv("CACHE_DIR", ".cache/exoscout")
CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))  # 1 hour default

# Initialize cache
cache = dc.Cache(CACHE_DIR)


def get_cache_key(prefix: str, *args, **kwargs) -> str:
    """
    Generate a cache key from prefix and arguments.
    
    Args:
        prefix (str): Cache key prefix
        *args: Positional arguments
        **kwargs: Keyword arguments
        
    Returns:
        str: Generated cache key
    """
    key_parts = [prefix]
    key_parts.extend(str(arg) for arg in args)
    key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
    return ":".join(key_parts)


def cached(prefix: str, ttl: Optional[int] = None):
    """
    Decorator for caching function results.
    
    Args:
        prefix (str): Cache key prefix
        ttl (Optional[int]): Time to live in seconds, defaults to CACHE_TTL
        
    Returns:
        Callable: Decorated function
    """
    if ttl is None:
        ttl = CACHE_TTL
        
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            cache_key = get_cache_key(prefix, *args, **kwargs)
            
            # Try to get from cache
            try:
                result = cache.get(cache_key)
                if result is not None:
                    logger.debug(f"Cache hit for key: {cache_key}")
                    return result
            except Exception as e:
                logger.warning(f"Cache get error for key {cache_key}: {e}")
            
            # Execute function and cache result
            try:
                result = await func(*args, **kwargs)
                cache.set(cache_key, result, expire=ttl)
                logger.debug(f"Cached result for key: {cache_key}")
                return result
            except Exception as e:
                logger.error(f"Function execution error: {e}")
                raise
                
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            cache_key = get_cache_key(prefix, *args, **kwargs)
            
            # Try to get from cache
            try:
                result = cache.get(cache_key)
                if result is not None:
                    logger.debug(f"Cache hit for key: {cache_key}")
                    return result
            except Exception as e:
                logger.warning(f"Cache get error for key {cache_key}: {e}")
            
            # Execute function and cache result
            try:
                result = func(*args, **kwargs)
                cache.set(cache_key, result, expire=ttl)
                logger.debug(f"Cached result for key: {cache_key}")
                return result
            except Exception as e:
                logger.error(f"Function execution error: {e}")
                raise
        
        # Return appropriate wrapper based on function type
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
            
    return decorator


def get_cached(key: str) -> Any:
    """
    Get value from cache by key.
    
    Args:
        key (str): Cache key
        
    Returns:
        Any: Cached value or None if not found
    """
    try:
        return cache.get(key)
    except Exception as e:
        logger.warning(f"Cache get error for key {key}: {e}")
        return None


def set_cached(key: str, value: Any, ttl: Optional[int] = None) -> bool:
    """
    Set value in cache with key.
    
    Args:
        key (str): Cache key
        value (Any): Value to cache
        ttl (Optional[int]): Time to live in seconds
        
    Returns:
        bool: True if successful, False otherwise
    """
    if ttl is None:
        ttl = CACHE_TTL
        
    try:
        cache.set(key, value, expire=ttl)
        return True
    except Exception as e:
        logger.warning(f"Cache set error for key {key}: {e}")
        return False


def delete_cached(key: str) -> bool:
    """
    Delete value from cache by key.
    
    Args:
        key (str): Cache key
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        return cache.delete(key)
    except Exception as e:
        logger.warning(f"Cache delete error for key {key}: {e}")
        return False


def clear_cache() -> bool:
    """
    Clear all cached values.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cache.clear()
        logger.info("Cache cleared successfully")
        return True
    except Exception as e:
        logger.error(f"Cache clear error: {e}")
        return False


def get_cache_stats() -> dict:
    """
    Get cache statistics.
    
    Returns:
        dict: Cache statistics
    """
    try:
        return {
            "size": len(cache),
            "volume": cache.volume(),
            "directory": cache.directory
        }
    except Exception as e:
        logger.error(f"Cache stats error: {e}")
        return {"error": str(e)}