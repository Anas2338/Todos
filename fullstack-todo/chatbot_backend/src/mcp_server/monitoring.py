"""Monitoring and health checks for the MCP server."""

import asyncio
import time
from typing import Dict, Any, List
from datetime import datetime
from enum import Enum
from ..core.performance_monitor import perf_monitor
from ..services.chat_service import chat_service
from ..core.database import engine
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    """Health status enumeration."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class MCPServerMonitor:
    """Monitoring and health checks for the MCP server."""

    def __init__(self):
        self.health_checks = {}
        self.metrics = {}
        self.last_check_time = None

    async def run_health_checks(self) -> Dict[str, Any]:
        """
        Run all health checks for the MCP server.

        Returns:
            Dictionary with health check results
        """
        self.last_check_time = datetime.now().isoformat()

        # Run all registered health checks
        results = {}
        for check_name, check_func in self.health_checks.items():
            try:
                results[check_name] = await check_func()
            except Exception as e:
                logger.error(f"Health check {check_name} failed: {str(e)}")
                results[check_name] = {
                    "status": HealthStatus.UNHEALTHY.value,
                    "message": str(e),
                    "timestamp": datetime.now().isoformat()
                }

        # Overall status is the worst of all checks
        overall_status = HealthStatus.HEALTHY.value
        for check_result in results.values():
            if check_result["status"] == HealthStatus.UNHEALTHY.value:
                overall_status = HealthStatus.UNHEALTHY.value
                break
            elif check_result["status"] == HealthStatus.DEGRADED.value and overall_status == HealthStatus.HEALTHY.value:
                overall_status = HealthStatus.DEGRADED.value

        return {
            "status": overall_status,
            "timestamp": self.last_check_time,
            "checks": results,
            "metrics": await self.get_current_metrics()
        }

    def register_health_check(self, name: str, check_func):
        """Register a health check function."""
        self.health_checks[name] = check_func

    async def get_current_metrics(self) -> Dict[str, Any]:
        """Get current metrics from the performance monitor."""
        return perf_monitor.get_metrics()

    async def database_health_check(self) -> Dict[str, Any]:
        """
        Check database connectivity and performance.

        Returns:
            Health check result
        """
        start_time = time.time()
        try:
            # Test database connectivity
            async with engine.connect() as conn:
                result = await conn.execute(text("SELECT 1"))
                await result.fetchall()

            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds

            return {
                "status": HealthStatus.HEALTHY.value,
                "message": "Database connection successful",
                "response_time_ms": response_time,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": HealthStatus.UNHEALTHY.value,
                "message": f"Database connection failed: {str(e)}",
                "response_time_ms": (time.time() - start_time) * 1000,
                "timestamp": datetime.now().isoformat()
            }

    async def chat_service_health_check(self) -> Dict[str, Any]:
        """
        Check chat service functionality.

        Returns:
            Health check result
        """
        try:
            # Test basic chat service functionality
            # Just test that we can access the service
            service_available = chat_service is not None

            if service_available:
                return {
                    "status": HealthStatus.HEALTHY.value,
                    "message": "Chat service is available",
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "status": HealthStatus.UNHEALTHY.value,
                    "message": "Chat service is not available",
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            return {
                "status": HealthStatus.UNHEALTHY.value,
                "message": f"Chat service check failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    async def mcp_tools_health_check(self) -> Dict[str, Any]:
        """
        Check MCP tools availability.

        Returns:
            Health check result
        """
        from .server import mcp_server

        try:
            # Check that MCP server is available and has tools
            if mcp_server is None:
                return {
                    "status": HealthStatus.UNHEALTHY.value,
                    "message": "MCP server is not available",
                    "timestamp": datetime.now().isoformat()
                }

            # Check that tools are registered
            tool_count = len(mcp_server.tools)
            if tool_count == 0:
                return {
                    "status": HealthStatus.DEGRADED.value,
                    "message": "MCP server has no tools registered",
                    "tool_count": tool_count,
                    "timestamp": datetime.now().isoformat()
                }

            return {
                "status": HealthStatus.HEALTHY.value,
                "message": f"MCP server is available with {tool_count} tools",
                "tool_count": tool_count,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": HealthStatus.UNHEALTHY.value,
                "message": f"MCP tools check failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    async def performance_health_check(self) -> Dict[str, Any]:
        """
        Check performance metrics against thresholds.

        Returns:
            Health check result
        """
        try:
            # Get current performance metrics
            metrics = await self.get_current_metrics()

            # Define thresholds
            avg_response_threshold = 2000  # 2 seconds
            max_response_threshold = 5000  # 5 seconds

            # Check if we have metrics to evaluate
            if not metrics:
                return {
                    "status": HealthStatus.UNKNOWN.value,
                    "message": "No performance metrics available for evaluation",
                    "timestamp": datetime.now().isoformat()
                }

            # Evaluate performance against thresholds
            issues = []
            for op_name, op_metrics in metrics.items():
                avg_duration = op_metrics.get('avg_duration_ms', 0)
                max_duration = op_metrics.get('max_duration_ms', 0)

                if avg_duration > avg_response_threshold:
                    issues.append(f"Avg response time for {op_name} ({avg_duration:.2f}ms) exceeds threshold ({avg_response_threshold}ms)")

                if max_duration > max_response_threshold:
                    issues.append(f"Max response time for {op_name} ({max_duration:.2f}ms) exceeds threshold ({max_response_threshold}ms)")

            if issues:
                return {
                    "status": HealthStatus.DEGRADED.value,
                    "message": "Performance issues detected",
                    "issues": issues,
                    "timestamp": datetime.now().isoformat()
                }

            return {
                "status": HealthStatus.HEALTHY.value,
                "message": "Performance metrics within acceptable ranges",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": HealthStatus.UNHEALTHY.value,
                "message": f"Performance check failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    def start_periodic_health_checks(self, interval: int = 30):
        """
        Start periodic health checks.

        Args:
            interval: Interval in seconds between health checks
        """
        async def run_periodic_checks():
            while True:
                try:
                    health_result = await self.run_health_checks()
                    logger.info(f"MCP Server Health Check: {health_result['status']}")

                    # Log any issues found
                    for check_name, check_result in health_result.get('checks', {}).items():
                        if check_result['status'] != HealthStatus.HEALTHY.value:
                            logger.warning(f"Health check '{check_name}' reported: {check_result['message']}")

                    await asyncio.sleep(interval)
                except Exception as e:
                    logger.error(f"Error during periodic health check: {str(e)}")
                    await asyncio.sleep(interval)

        # Run the periodic checks in the background
        asyncio.create_task(run_periodic_checks())


# Global instance of the MCP server monitor
mcp_monitor = MCPServerMonitor()


# Register default health checks
async def setup_default_health_checks():
    """Set up default health checks for the MCP server."""
    mcp_monitor.register_health_check("database", mcp_monitor.database_health_check)
    mcp_monitor.register_health_check("chat_service", mcp_monitor.chat_service_health_check)
    mcp_monitor.register_health_check("mcp_tools", mcp_monitor.mcp_tools_health_check)
    mcp_monitor.register_health_check("performance", mcp_monitor.performance_health_check)


# Initialize default health checks
asyncio.create_task(setup_default_health_checks())