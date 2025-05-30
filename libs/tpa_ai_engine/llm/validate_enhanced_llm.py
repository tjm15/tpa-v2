#!/usr/bin/env python3
"""
Simple validation script for the enhanced LLM abstraction layer.
"""

import os
import sys
import logging

# Set up structured logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("validate_enhanced_llm")

def validate_imports():
    """Validate that all modules can be imported"""
    logger.info("🔍 Validating Enhanced LLM Imports...")
    
    try:
        # Test standard library imports
        import asyncio
        import logging
        from enum import Enum
        from dataclasses import dataclass
        logger.info("✅ Standard library imports successful")

        # Test existing project imports
        from tpa_ai_engine.config import create_llm_client
        logger.info("✅ Existing LLM client import successful")

        # Test enhanced module imports
        from tpa_ai_engine.llm.enhanced_llm_client import LLMResponse, LLMMetrics
        logger.info("✅ Enhanced LLM client base classes imported")

        from tpa_ai_engine.llm.enhanced_providers import EnhancedGeminiClient, EnhancedOpenRouterClient
        logger.info("✅ Enhanced provider classes imported")

        from tpa_ai_engine.llm.enhanced_fallback_client import EnhancedFallbackLLMClient
        logger.info("✅ Enhanced fallback client imported")

        from tpa_ai_engine.llm.enhanced_config import create_enhanced_llm_client, validate_llm_configuration
        logger.info("✅ Enhanced config functions imported")

        return True
        
    except ImportError as e:
        logger.error(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return False

def validate_configuration():
    """Validate LLM configuration"""
    logger.info("🔍 Validating LLM Configuration...")
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    
    logger.info(f"  GEMINI_API_KEY: {'✅ Set' if gemini_key else '❌ Not set'}")
    logger.info(f"  OPENROUTER_API_KEY: {'✅ Set' if openrouter_key else '❌ Not set'}")
    
    if not gemini_key and not openrouter_key:
        logger.warning("⚠️  No API keys configured. Enhanced client will not be fully functional.")
        return False
    
    return True

def main():
    """Main validation function"""
    logger.info("Enhanced LLM Abstraction Layer Validation")
    logger.info("=" * 50)
    
    imports_ok = validate_imports()
    config_ok = validate_configuration()
    
    logger.info("=" * 50)
    if imports_ok and config_ok:
        logger.info("🎉 Validation successful! Enhanced LLM abstraction layer is ready.")
        return 0
    elif imports_ok:
        logger.warning("⚠️  Imports successful but configuration incomplete.")
        logger.warning("   Set GEMINI_API_KEY and/or OPENROUTER_API_KEY to enable full functionality.")
        return 1
    else:
        logger.error("❌ Validation failed. Check imports and dependencies.")
        return 2

if __name__ == "__main__":
    sys.exit(main())
