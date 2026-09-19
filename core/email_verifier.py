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

def verify_email_deliverability(email_address: str, timeout: float = 4.0) -> Tuple[bool, str, Optional[str]]:
    """
    Performs pre-flight deliverability checks on a recipient address.
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
            return True, "HOST_RESOLVED_NO_MX", domain
    except socket.gaierror:
        return False, "DOMAIN_NOT_FOUND_NO_MX", None
    except Exception as e:
        logger.warning(f"Socket resolution error for {domain}: {e}")

    return False, "NO_VALID_MAIL_SERVER", None
