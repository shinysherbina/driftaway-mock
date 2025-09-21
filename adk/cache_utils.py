import hashlib
import json
import time

# In-memory cache
_mcp_cache = {}

def get_cached_response(mcp_id, input_data):
    """
    Retrieves a cached response if available and not expired.
    """
    input_hash = _generate_input_hash(input_data)
    cache_key = f"{mcp_id}:{input_hash}"
    
    cached_item = _mcp_cache.get(cache_key)
    
    if cached_item and not _is_expired(cached_item):
        return cached_item['response']
    
    return None

def set_cached_response(mcp_id, input_data, response, ttl=3600):
    """
    Caches an MCP response with a TTL.
    """
    input_hash = _generate_input_hash(input_data)
    cache_key = f"{mcp_id}:{input_hash}"
    
    _mcp_cache[cache_key] = {
        'response': response,
        'timestamp': time.time(),
        'ttl': ttl
    }

def _generate_input_hash(input_data):
    """
    Generates a SHA-256 hash of the input data.
    """
    serialized_data = json.dumps(input_data, sort_keys=True).encode('utf-8')
    return hashlib.sha256(serialized_data).hexdigest()

def _is_expired(cached_item):
    """
    Checks if a cached item has expired.
    """
    elapsed_time = time.time() - cached_item['timestamp']
    return elapsed_time > cached_item['ttl']