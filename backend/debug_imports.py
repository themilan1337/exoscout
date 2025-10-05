#!/usr/bin/env python3
"""
Debug script to check library availability and versions in production environment.
"""

import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_library(name, import_path=None):
    """Check if a library is available and get its version."""
    try:
        if import_path:
            module = __import__(import_path)
        else:
            module = __import__(name)
        
        # Try to get version
        version = "unknown"
        for attr in ['__version__', 'version', 'VERSION']:
            if hasattr(module, attr):
                version = getattr(module, attr)
                break
        
        logger.info(f"✓ {name}: {version}")
        return True, version
    except ImportError as e:
        logger.error(f"✗ {name}: Import failed - {e}")
        return False, str(e)
    except Exception as e:
        logger.error(f"✗ {name}: Error - {e}")
        return False, str(e)

def main():
    """Main function to check all required libraries."""
    logger.info("Checking library availability...")
    
    libraries = [
        ("lightkurve", "lightkurve"),
        ("astroquery", "astroquery"),
        ("astropy", "astropy"),
        ("numpy", "numpy"),
        ("pandas", "pandas"),
        ("fastapi", "fastapi"),
        ("httpx", "httpx"),
        ("requests", "requests"),
    ]
    
    results = {}
    
    for name, import_path in libraries:
        available, info = check_library(name, import_path)
        results[name] = {"available": available, "info": info}
    
    # Test specific functionality
    logger.info("\nTesting specific functionality...")
    
    # Test lightkurve search
    try:
        import lightkurve as lk
        logger.info("Testing lightkurve search...")
        search_result = lk.search_lightcurve("KIC 10666592", mission="Kepler")
        logger.info(f"lightkurve search returned {len(search_result)} results")
        
        if len(search_result) > 0:
            logger.info(f"First result: {search_result[0]}")
        
    except Exception as e:
        logger.error(f"lightkurve search test failed: {e}")
    
    # Test astroquery
    try:
        from astroquery.mast import Observations
        logger.info("Testing astroquery MAST...")
        
        obs_table = Observations.query_criteria(
            target_name="kplr010666592",
            obs_collection="Kepler"
        )
        logger.info(f"astroquery search returned {len(obs_table)} observations")
        
        if len(obs_table) > 0:
            obs_id = obs_table[0]['obsid']
            products = Observations.get_product_list(obs_id)
            lc_products = products[products['productSubGroupDescription'] == 'LC']
            logger.info(f"Found {len(lc_products)} lightcurve products")
        
    except Exception as e:
        logger.error(f"astroquery test failed: {e}")
    
    # Summary
    logger.info("\nSummary:")
    for name, result in results.items():
        status = "✓" if result["available"] else "✗"
        logger.info(f"{status} {name}: {result['info']}")

if __name__ == "__main__":
    main()