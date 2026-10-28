"""
Nexus Pre-Send Email & MX Verification Engine
=============================================
Verifies email syntax and validates domain Mail Exchange (MX) records
before transmitting outbound SMTP messages to eliminate bounce-backs.
"""

import re
import socket
import logging
from typing import Tuple, Optional

try:
    import dns.resolver
    HAS_DNS = True
except ImportError:
    HAS_DNS = False

logger = logging.getLogger("Nexus.EmailVerifier")

EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
)

# Known disposable/fake domain patterns
DISPOSABLE_DOMAINS = {
    "mailinator.com", "tempmail.com", "10minutemail.com", "guerrillamail.com",
    "sharklasers.com", "throwawaymail.com", "yopmail.com"
}

import time
from typing import Dict, Any

# 24-Hour Persistent + In-Memory DNS MX Cache (eliminates repeated DNS socket lookups per domain)
_MX_DOMAIN_CACHE: Dict[str, Dict[str, Any]] = {}
_MX_CACHE_TTL_SECONDS = 86400  # 24 hours

def _get_cached_domain_mx(domain: str) -> Optional[Tuple[bool, str, Optional[str]]]:
    now = time.time()
    if domain in _MX_DOMAIN_CACHE:
        entry = _MX_DOMAIN_CACHE[domain]
        if now - entry.get("ts", 0) < _MX_CACHE_TTL_SECONDS:
            return entry["deliverable"], entry["reason"], entry["primary_mx"]
    try:
        from core.dal import dal
        persisted = dal.load("mx_domain_cache", default={})
        if isinstance(persisted, dict) and domain in persisted:
            entry = persisted[domain]
            if now - entry.get("ts", 0) < _MX_CACHE_TTL_SECONDS:
                _MX_DOMAIN_CACHE[domain] = entry
                return entry["deliverable"], entry["reason"], entry["primary_mx"]
    except Exception:
        pass
    return None

def _set_cached_domain_mx(domain: str, deliverable: bool, reason: str, primary_mx: Optional[str]) -> None:
    entry = {
        "deliverable": deliverable,
        "reason": reason,
        "primary_mx": primary_mx,
        "ts": time.time()
    }
    _MX_DOMAIN_CACHE[domain] = entry
    try:
        from core.dal import dal
        persisted = dal.load("mx_domain_cache", default={})
        if not isinstance(persisted, dict):
            persisted = {}
        persisted[domain] = entry
        dal.save("mx_domain_cache", persisted)
    except Exception:
        pass

def verify_email_deliverability(email_address: str, timeout: float = 4.0) -> Tuple[bool, str, Optional[str]]:
    """
    Performs pre-flight deliverability checks on a recipient address with 24h DNS MX caching.
    Returns:
        (is_deliverable: bool, reason: str, primary_mx: Optional[str])
    """
    if not email_address or not isinstance(email_address, str):
        return False, "EMPTY_EMAIL", None

    clean_email = email_address.strip().lower()

    # 1. Regex format check
    if not EMAIL_REGEX.match(clean_email):
        return False, "INVALID_SYNTAX", None

    domain = clean_email.split("@")[-1]

    # 2. Disposable check
    if domain in DISPOSABLE_DOMAINS:
        return False, "DISPOSABLE_DOMAIN", None

    # 2.5 Check 24h Domain MX Cache
    cached = _get_cached_domain_mx(domain)
    if cached is not None:
        return cached

    # 3. DNS MX Record Lookup
    if HAS_DNS:
        try:
            resolver = dns.resolver.Resolver()
            resolver.lifetime = timeout
            resolver.timeout = timeout
            mx_answers = resolver.resolve(domain, "MX")
            if mx_answers and len(mx_answers) > 0:
                # Sort by priority (lowest number = highest priority)
                sorted_mx = sorted(mx_answers, key=lambda r: r.preference)
                primary_mx = str(sorted_mx[0].exchange).rstrip(".")
                _set_cached_domain_mx(domain, True, "MX_VERIFIED", primary_mx)
                return True, "MX_VERIFIED", primary_mx
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            pass
        except dns.resolver.Timeout:
            logger.warning(f"DNS MX query timeout for domain {domain}")
        except Exception as e:
            logger.warning(f"DNS MX lookup error for {domain}: {e}")

    # 4. Fallback: Host existence / A record check via socket
    try:
        addr_info = socket.getaddrinfo(domain, 25, proto=socket.IPPROTO_TCP)
        if addr_info:
            _set_cached_domain_mx(domain, True, "HOST_RESOLVED_NO_MX", domain)
            return True, "HOST_RESOLVED_NO_MX", domain
    except socket.gaierror:
        _set_cached_domain_mx(domain, False, "DOMAIN_NOT_FOUND_NO_MX", None)
        return False, "DOMAIN_NOT_FOUND_NO_MX", None
    except Exception as e:
        logger.warning(f"Socket resolution error for {domain}: {e}")

    _set_cached_domain_mx(domain, False, "NO_VALID_MAIL_SERVER", None)
    return False, "NO_VALID_MAIL_SERVER", None
