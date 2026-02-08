"""MCP Server configuration options."""

from typing import Optional
from pydantic import BaseModel
from ..core.config import config


class MCPConfig(BaseModel):
    """Configuration for the MCP server."""

    # Server configuration
    host: str = config.MCP_SERVER_HOST
    port: int = config.MCP_SERVER_PORT
    debug: bool = config.APP_ENV == "development"

    # Connection settings
    max_connections: int = 100
    keepalive_timeout: int = 120
    request_timeout: int = 30

    # Tool execution settings
    max_concurrent_executions: int = 10
    execution_timeout: int = 60
    retry_attempts: int = 3

    # Security settings
    enable_auth: bool = True
    auth_required_for_all_tools: bool = True
    rate_limit_enabled: bool = True
    max_requests_per_minute: int = 60

    # Monitoring settings
    enable_monitoring: bool = True
    log_level: str = config.LOG_LEVEL
    enable_detailed_logs: bool = False

    # Performance settings
    cache_enabled: bool = True
    cache_ttl_seconds: int = 300
    enable_caching_for_tools: bool = True

    # Error handling settings
    graceful_error_handling: bool = True
    error_notification_enabled: bool = True
    max_error_retries: int = 2


# Global MCP configuration instance
mcp_config = MCPConfig()


def get_mcp_config() -> MCPConfig:
    """Get the global MCP configuration instance."""
    return mcp_config