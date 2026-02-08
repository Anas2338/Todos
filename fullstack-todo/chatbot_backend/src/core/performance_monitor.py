"""Performance monitoring utilities for measuring response times."""

import time
import functools
import asyncio
from typing import Callable, Any
from datetime import datetime
import logging
from .logging_setup import log_performance

logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """Class for monitoring and measuring performance metrics."""

    def __init__(self):
        self.metrics = {}

    def time_function(self, operation_name: str = None):
        """
        Decorator to time function execution.

        Args:
            operation_name: Optional name for the operation being timed
        """
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                start_time = time.perf_counter()
                try:
                    result = await func(*args, **kwargs)
                    return result
                finally:
                    duration = (time.perf_counter() - start_time) * 1000  # Convert to milliseconds
                    op_name = operation_name or f"{func.__module__}.{func.__name__}"

                    # Log performance metric
                    log_performance(logger, op_name, duration)

                    # Store metric for potential aggregation
                    self._record_metric(op_name, duration)

            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                start_time = time.perf_counter()
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    duration = (time.perf_counter() - start_time) * 1000  # Convert to milliseconds
                    op_name = operation_name or f"{func.__module__}.{func.__name__}"

                    # Log performance metric
                    log_performance(logger, op_name, duration)

                    # Store metric for potential aggregation
                    self._record_metric(op_name, duration)

            # Return the appropriate wrapper based on function type
            if asyncio.iscoroutinefunction(func):
                return async_wrapper
            else:
                return sync_wrapper
        return decorator

    def time_block(self, operation_name: str):
        """
        Context manager to time a block of code.

        Args:
            operation_name: Name for the operation being timed
        """
        return TimingContext(self, operation_name)

    def _record_metric(self, operation_name: str, duration_ms: float):
        """Record a performance metric."""
        if operation_name not in self.metrics:
            self.metrics[operation_name] = []

        self.metrics[operation_name].append({
            'timestamp': datetime.utcnow().isoformat(),
            'duration_ms': duration_ms
        })

    def get_metrics(self, operation_name: str = None) -> dict:
        """
        Get performance metrics.

        Args:
            operation_name: Optional operation name to get metrics for (None for all)

        Returns:
            Dictionary with performance metrics
        """
        if operation_name:
            if operation_name in self.metrics:
                durations = [m['duration_ms'] for m in self.metrics[operation_name]]
                return {
                    'operation': operation_name,
                    'count': len(durations),
                    'avg_duration_ms': sum(durations) / len(durations) if durations else 0,
                    'min_duration_ms': min(durations) if durations else 0,
                    'max_duration_ms': max(durations) if durations else 0,
                    'metrics': self.metrics[operation_name]
                }
            else:
                return {'operation': operation_name, 'count': 0, 'avg_duration_ms': 0}
        else:
            all_metrics = {}
            for op_name in self.metrics:
                durations = [m['duration_ms'] for m in self.metrics[op_name]]
                all_metrics[op_name] = {
                    'operation': op_name,
                    'count': len(durations),
                    'avg_duration_ms': sum(durations) / len(durations) if durations else 0,
                    'min_duration_ms': min(durations) if durations else 0,
                    'max_duration_ms': max(durations) if durations else 0
                }
            return all_metrics

    def clear_metrics(self, operation_name: str = None):
        """
        Clear performance metrics.

        Args:
            operation_name: Optional operation name to clear metrics for (None for all)
        """
        if operation_name:
            if operation_name in self.metrics:
                del self.metrics[operation_name]
        else:
            self.metrics.clear()


class TimingContext:
    """Context manager for timing code blocks."""

    def __init__(self, monitor: PerformanceMonitor, operation_name: str):
        self.monitor = monitor
        self.operation_name = operation_name
        self.start_time = None

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time is not None:
            duration = (time.perf_counter() - self.start_time) * 1000  # Convert to milliseconds

            # Log performance metric
            log_performance(logger, self.operation_name, duration)

            # Store metric
            self.monitor._record_metric(self.operation_name, duration)


# Global performance monitor instance
perf_monitor = PerformanceMonitor()


# Convenience functions
def time_function(operation_name: str = None):
    """Decorator to time function execution."""
    return perf_monitor.time_function(operation_name)


def time_block(operation_name: str):
    """Context manager to time a block of code."""
    return perf_monitor.time_block(operation_name)


def get_performance_metrics(operation_name: str = None) -> dict:
    """Get performance metrics."""
    return perf_monitor.get_metrics(operation_name)


def clear_performance_metrics(operation_name: str = None):
    """Clear performance metrics."""
    perf_monitor.clear_metrics(operation_name)


# Example usage:
if __name__ == "__main__":
    import asyncio

    @time_function("example_async_operation")
    async def example_async_operation():
        await asyncio.sleep(0.1)  # Simulate async work
        return "Done"

    @time_function("example_sync_operation")
    def example_sync_operation():
        time.sleep(0.05)  # Simulate work
        return "Done"

    # Example of using context manager
    def example_context_usage():
        with time_block("context_operation"):
            time.sleep(0.02)  # Simulate work

    # Run examples
    async def run_examples():
        await example_async_operation()
        example_sync_operation()
        example_context_usage()

        # Print metrics
        print(get_performance_metrics())

    # asyncio.run(run_examples())