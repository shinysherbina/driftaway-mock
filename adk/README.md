# ADK Orchestrator

This service orchestrates the trip planning process by invoking various Micro-Chassis-Processes (MCPs) and enriching their data using the Gemini API.

## Caching

To optimize performance and reduce redundant calls to the Gemini API, the orchestrator implements a caching layer for MCP responses. The cache is stored in-memory.

### Cache Behavior

- **Cache Key**: The cache key is generated using the `mcp_id` and a SHA-256 hash of the input data.
- **Cache Invalidation**: Cached items have a Time-to-Live (TTL) of 1 hour. After this period, the cache is considered stale and will be refreshed.
- **Cache Bypass**: The cache can be bypassed by including the `force_enrich=true` query parameter in the request. This will force the orchestrator to invoke the MCPs and enrich the data, even if a valid cached response is available.

### Fallback Logic

- If a valid cached response is available, it is returned immediately.
- If the cache is stale or no cached response is available, the orchestrator invokes the MCPs and enriches the data using the Gemini API.
- The enriched response is then cached for future requests.

## API

- `POST /planTrip`: Orchestrates the trip planning process.
  - **Query Parameters**:
    - `force_enrich` (boolean, optional): If `true`, bypasses the cache and forces a new request to the MCPs.
- `POST /field-update`: Updates a specific field in the trip plan.
  - **Query Parameters**:
    - `force_enrich` (boolean, optional): If `true`, bypasses the cache and forces a new request to the MCPs.
