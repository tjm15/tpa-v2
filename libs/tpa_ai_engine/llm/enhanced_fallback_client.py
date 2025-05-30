"""
Enhanced fallback LLM client with intelligent provider selection,
health monitoring, and comprehensive caching.
"""

import asyncio
import time
import hashlib
import json
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from .enhanced_llm_client import (
    EnhancedLLMClient, LLMResponse, LLMMetrics, ProviderState, logger
)
from shared_utils.llm_task_queue import LLMRedisCache


@dataclass
class ProviderPerformance:
    """Track provider performance metrics"""
    total_calls: int = 0
    successful_calls: int = 0
    total_response_time: float = 0.0
    last_success_time: Optional[datetime] = None
    last_failure_time: Optional[datetime] = None
    consecutive_failures: int = 0
    consecutive_successes: int = 0
    
    @property
    def success_rate(self) -> float:
        if self.total_calls == 0:
            return 0.0
        return self.successful_calls / self.total_calls
    
    @property
    def average_response_time(self) -> float:
        if self.successful_calls == 0:
            return float('inf')
        return self.total_response_time / self.successful_calls
    
    def record_success(self, response_time: float):
        self.total_calls += 1
        self.successful_calls += 1
        self.total_response_time += response_time
        self.last_success_time = datetime.now()
        self.consecutive_successes += 1
        self.consecutive_failures = 0
    
    def record_failure(self):
        self.total_calls += 1
        self.last_failure_time = datetime.now()
        self.consecutive_failures += 1
        self.consecutive_successes = 0


class UniversalLLMCache:
    """Provider-agnostic caching system for LLM responses (now uses shared Redis cache)"""
    
    def __init__(self, prefix: str = "llm:universal:"):
        """
        Initialize with Redis cache
        
        Args:
            prefix: Key prefix for Redis cache
        """
        self.cache = LLMRedisCache(prefix=prefix)
    
    def make_key(self, contents, config, model):
        """Create a unique cache key based on contents, config, and model"""
        key_data = json.dumps({"contents": contents, "config": config, "model": model}, sort_keys=True)
        return hashlib.sha256(key_data.encode()).hexdigest()
    
    def get(self, contents, config, model):
        """Get cached value by contents, config, and model"""
        key = self.make_key(contents, config, model)
        return self.cache.get(key)
    
    def set(self, contents, config, model, value, ex: int = 3600):
        """Set cache value with expiration"""
        key = self.make_key(contents, config, model)
        self.cache.set(key, value, ex=ex)
    
    def delete(self, contents, config, model):
        """Delete key from cache"""
        key = self.make_key(contents, config, model)
        self.cache.delete(key)


class EnhancedFallbackLLMClient:
    """Enhanced LLM client with intelligent fallback and monitoring"""
    
    def __init__(self, providers: List[EnhancedLLMClient]):
        """
        Initialize fallback client
        
        Args:
            providers: List of LLM provider clients (ordered by preference)
        """
        if not providers:
            raise ValueError("At least one provider must be specified")
        
        self.providers = providers
        self.provider_performance: Dict[str, ProviderPerformance] = {
            provider.provider_name: ProviderPerformance() 
            for provider in providers
        }
        
        self.cache = UniversalLLMCache()
        self.global_metrics = LLMMetrics()
        self.cache_hits = 0
        self.cache_misses = 0
        
        # Provider selection strategy
        self.selection_strategy = "health_aware"  # or "round_robin", "fastest"
        self._current_provider_index = 0
        
        logger.info(f"Enhanced fallback client initialized with {len(providers)} providers: "
                   f"{[p.provider_name for p in providers]}")
    
    def _select_best_provider(self) -> EnhancedLLMClient:
        """Select the best available provider based on current strategy"""
        available_providers = [
            p for p in self.providers 
            if p.circuit_breaker.can_attempt_call() and p.is_available()
        ]
        
        if not available_providers:
            # Try to reset circuit breakers and check again
            logger.warning("No providers available, attempting recovery...")
            for provider in self.providers:
                if provider.circuit_breaker.state == ProviderState.FAILED:
                    provider.circuit_breaker.state = ProviderState.RECOVERING
            
            available_providers = [p for p in self.providers if p.is_available()]
            
            if not available_providers:
                raise Exception("No LLM providers are currently available")
        
        if self.selection_strategy == "health_aware":
            # Select provider with highest health score
            return max(available_providers, key=lambda p: p.health_score)
        
        elif self.selection_strategy == "fastest":
            # Select provider with best average response time
            def get_avg_time(provider):
                perf = self.provider_performance[provider.provider_name]
                return perf.average_response_time
            
            return min(available_providers, key=get_avg_time)
        
        elif self.selection_strategy == "round_robin":
            # Round-robin through available providers
            while True:
                provider = self.providers[self._current_provider_index]
                self._current_provider_index = (self._current_provider_index + 1) % len(self.providers)
                
                if provider in available_providers:
                    return provider
        
        else:
            # Default: return first available provider
            return available_providers[0]
    
    async def retry_once(self, provider, contents, config, model):
        """Retry a provider call once with exponential backoff on transient errors"""
        try:
            return await provider.generate_content(contents, config, model)
        except Exception as e:
            error_str = str(e).lower()
            transient_terms = ["timeout", "network", "connection", "temporarily unavailable", "5", "rate limit"]
            if any(term in error_str for term in transient_terms):
                delay = 2.0  # base_delay * (2 ** 0)
                logger.warning(f"Transient error from {provider.provider_name}, retrying once in {delay}s: {e}")
                await asyncio.sleep(delay)
                return await provider.generate_content(contents, config, model)
            raise

    async def generate_content(self, contents: Union[str, List[Any]], 
                             config: Dict[str, Any], model: str) -> LLMResponse:
        """Generate content with intelligent fallback and caching"""
        request_start_time = time.time()
        
        # Check cache first
        cached_response = self.cache.get(contents, config, model)
        if cached_response:
            logger.info("Cache hit for LLM response")
            self.global_metrics.add_call(
                provider="cache",
                success=True,
                response_time=0,
                cache_hit=True
            )
            self.cache_hits += 1
            # Patch: reconstruct LLMResponse if needed
            if isinstance(cached_response, dict):
                cached_response = LLMResponse(**cached_response)
            return cached_response
        self.cache_misses += 1
        
        # Try providers in order of preference
        last_error = None
        attempted_providers = []
        
        while len(attempted_providers) < len(self.providers):
            try:
                # Select best available provider
                provider = self._select_best_provider()
                
                # Skip if already attempted
                if provider.provider_name in attempted_providers:
                    # Remove from available list and try again
                    remaining_providers = [
                        p for p in self.providers 
                        if p.provider_name not in attempted_providers
                    ]
                    if not remaining_providers:
                        break
                    provider = remaining_providers[0]
                
                attempted_providers.append(provider.provider_name)
                
                logger.info(f"Attempting LLM call with {provider.provider_name}")
                
                # Make the request with retry_once
                try:
                    response = await self.retry_once(provider, contents, config, model)
                except Exception as e:
                    last_error = e
                    total_time = (time.time() - request_start_time) * 1000
                    # Record failure
                    if attempted_providers:
                        provider_name = attempted_providers[-1]
                        self.provider_performance[provider_name].record_failure()
                        self.global_metrics.add_call(
                            provider=provider_name,
                            success=False,
                            response_time=total_time
                        )
                    logger.warning(f"Provider {attempted_providers[-1] if attempted_providers else 'unknown'} "
                                  f"failed: {e}")
                    continue
                
                # Record success
                total_time = (time.time() - request_start_time) * 1000
                self.provider_performance[provider.provider_name].record_success(total_time)
                
                self.global_metrics.add_call(
                    provider=provider.provider_name,
                    success=True,
                    response_time=total_time,
                    prompt_tokens=response.prompt_tokens or 0,
                    completion_tokens=response.completion_tokens or 0,
                    cost=response.estimated_cost_usd or 0.0,
                    cache_hit=False
                )
                
                # Cache the successful response (as dict, not object)
                self.cache.set(contents, config, model, response.to_dict())
                
                logger.info(f"Successfully generated content using {provider.provider_name} "
                           f"in {total_time:.0f}ms")
                
                return response
                
            except Exception as e:
                last_error = e
                total_time = (time.time() - request_start_time) * 1000
                
                # Record failure
                if attempted_providers:
                    provider_name = attempted_providers[-1]
                    self.provider_performance[provider_name].record_failure()
                    
                    self.global_metrics.add_call(
                        provider=provider_name,
                        success=False,
                        response_time=total_time
                    )
                
                logger.warning(f"Provider {attempted_providers[-1] if attempted_providers else 'unknown'} "
                              f"failed: {e}")
                
                # Continue to next provider
                continue
        
        # All providers failed
        total_time = (time.time() - request_start_time) * 1000
        logger.error(f"All {len(attempted_providers)} providers failed after {total_time:.0f}ms")
        
        raise Exception(f"All LLM providers failed. Last error: {last_error}")
    
    def get_status_report(self) -> Dict[str, Any]:
        """Get comprehensive status report"""
        provider_stats = {}
        
        for provider in self.providers:
            perf = self.provider_performance[provider.provider_name]
            provider_stats[provider.provider_name] = {
                "state": provider.circuit_breaker.state.value,
                "health_score": provider.health_score,
                "total_calls": perf.total_calls,
                "success_rate": perf.success_rate,
                "avg_response_time": perf.average_response_time,
                "consecutive_failures": perf.consecutive_failures,
                "consecutive_successes": perf.consecutive_successes,
                "last_success": perf.last_success_time.isoformat() if perf.last_success_time else None,
                "last_failure": perf.last_failure_time.isoformat() if perf.last_failure_time else None,
                "is_available": provider.is_available()
            }
        
        return {
            "global_metrics": {
                "total_calls": self.global_metrics.total_calls,
                "success_rate": self.global_metrics.success_rate,
                "avg_response_time": self.global_metrics.average_response_time,
                "total_cost_usd": self.global_metrics.total_cost_usd,
                "total_tokens": self.global_metrics.total_prompt_tokens + self.global_metrics.total_completion_tokens
            },
            "cache_stats": {
                "hit_rate": (self.cache_hits / (self.cache_hits + self.cache_misses)) if (self.cache_hits + self.cache_misses) > 0 else 0.0,
                "hits": self.cache_hits,
                "misses": self.cache_misses
            },
            "providers": provider_stats,
            "current_strategy": self.selection_strategy
        }
    
    def reset_all_providers(self):
        """Reset all provider states and metrics"""
        for provider in self.providers:
            provider.circuit_breaker.failure_count = 0
            provider.circuit_breaker.state = ProviderState.HEALTHY
            provider.circuit_breaker.consecutive_successes = 0
            provider.reset_availability_cache()
        
        self.provider_performance = {
            provider.provider_name: ProviderPerformance() 
            for provider in self.providers
        }
        
        logger.info("All providers reset")
    
    def set_selection_strategy(self, strategy: str):
        """Set provider selection strategy"""
        valid_strategies = ["health_aware", "fastest", "round_robin"]
        if strategy not in valid_strategies:
            raise ValueError(f"Invalid strategy. Must be one of: {valid_strategies}")
        
        self.selection_strategy = strategy
        logger.info(f"Provider selection strategy set to: {strategy}")
    
    @property
    def provider_name(self) -> str:
        """Return description of fallback client"""
        provider_names = [p.provider_name for p in self.providers]
        return f"fallback({', '.join(provider_names)})"
