import os
import json
import ssl
import time
import urllib.request
import urllib.parse
from datetime import datetime
from typing import Dict, Any, Optional

CONFIG_FILE = "whatsapp_config.json"

DEFAULT_CONFIG: Dict[str, Any] = {
    "provider": "callmebot",  # "callmebot" | "openwa"
    "phone": "+23058169420",
    "callmebot": {
        "api_key": os.getenv("CALLMEBOT_API_KEY", "").strip()
    },
    "openwa": {
        "base_url": os.getenv("OPENWA_BASE_URL", "http://localhost:3000").strip(),
        "api_key": os.getenv("OPENWA_API_KEY", "").strip(),
        "session": os.getenv("OPENWA_SESSION", "default").strip(),
        "chat_id": os.getenv("OPENWA_CHAT_ID", "23058169420@c.us").strip()
    }
}

def load_whatsapp_config() -> Dict[str, Any]:
    """Loads active WhatsApp gateway configuration from whatsapp_config.json or defaults."""
    if not os.path.exists(CONFIG_FILE):
        return DEFAULT_CONFIG.copy()
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            # Ensure nested keys exist
            merged = DEFAULT_CONFIG.copy()
            merged.update(cfg)
            if "callmebot" not in merged:
                merged["callmebot"] = DEFAULT_CONFIG["callmebot"]
            if "openwa" not in merged:
                merged["openwa"] = DEFAULT_CONFIG["openwa"]
            return merged
    except Exception:
        return DEFAULT_CONFIG.copy()

def save_whatsapp_config(new_config: Dict[str, Any]) -> Dict[str, Any]:
    """Saves updated WhatsApp gateway configuration."""
    current = load_whatsapp_config()
    current["provider"] = new_config.get("provider", current.get("provider", "callmebot")).lower()
    if "phone" in new_config:
        current["phone"] = new_config["phone"].strip()
    
    if "callmebot" in new_config and isinstance(new_config["callmebot"], dict):
        current["callmebot"].update(new_config["callmebot"])
    if "openwa" in new_config and isinstance(new_config["openwa"], dict):
        current["openwa"].update(new_config["openwa"])

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(current, f, indent=2)

    # Sync environment variables in memory
    if current.get("callmebot", {}).get("api_key"):
        os.environ["CALLMEBOT_API_KEY"] = current["callmebot"]["api_key"]
    if current.get("openwa", {}).get("base_url"):
        os.environ["OPENWA_BASE_URL"] = current["openwa"]["base_url"]

    return current

def _send_callmebot(phone: str, text: str, api_key: str) -> Dict[str, Any]:
    """Dispatches message via CallMeBot HTTP API."""
    if not api_key:
        return {
            "channel": "WhatsApp (CallMeBot Simulated)",
            "status": "SIMULATED",
            "mock_mode": True,
            "error": "No CALLMEBOT_API_KEY configured. Please provide your API key in Settings.",
            "response": "Simulation mode active."
        }

    params = urllib.parse.urlencode({
        "phone": phone,
        "text": text,
        "apikey": api_key
    })
    url = f"https://api.callmebot.com/whatsapp.php?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": "NexusWorkforce-Gateway/3.0"})
    
    with urllib.request.urlopen(req, timeout=15, context=ssl.create_default_context()) as resp:
        body = resp.read().decode("utf-8", errors="replace")
        status_code = resp.status
        is_ok = status_code == 200
        return {
            "channel": "WhatsApp (CallMeBot Live)",
            "phone": phone,
            "status": "DELIVERED" if is_ok else f"HTTP_{status_code}",
            "mock_mode": False,
            "response": body[:300],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

def _send_openwa(base_url: str, chat_id: str, text: str, api_key: str = "", session: str = "default") -> Dict[str, Any]:
    """
    Dispatches message via self-hosted OpenWA REST Gateway (https://github.com/rmyndharis/OpenWA).
    Supports OpenWA endpoints: /api/messages/send, /api/send-message, and /api/{session}/send-message.
    """
    clean_base = base_url.rstrip("/")
    # Clean up destination ID
    dest = chat_id.strip()
    if "@" not in dest:
        # e.g. +23058169420 -> 23058169420@c.us
        clean_num = dest.replace("+", "").replace(" ", "").replace("-", "")
        dest = f"{clean_num}@c.us"

    payload_dict = {
        "chatId": dest,
        "phone": dest.split("@")[0],
        "message": text,
        "text": text,
        "session": session
    }
    data_bytes = json.dumps(payload_dict).encode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "NexusWorkforce-OpenWAGateway/3.0"
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
        headers["x-api-key"] = api_key

    # Try common OpenWA REST endpoints
    endpoints_to_try = [
        f"{clean_base}/api/messages/send",
        f"{clean_base}/api/send-message",
        f"{clean_base}/api/{session}/send-message"
    ]

    last_error = None
    for endpoint in endpoints_to_try:
        try:
            req = urllib.request.Request(endpoint, data=data_bytes, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=12, context=ssl.create_default_context()) as resp:
                body = resp.read().decode("utf-8", errors="replace")
                return {
                    "channel": "WhatsApp (OpenWA Self-Hosted Live)",
                    "gateway": "OpenWA (github.com/rmyndharis/OpenWA)",
                    "endpoint": endpoint,
                    "recipient": dest,
                    "status": "DELIVERED",
                    "mock_mode": False,
                    "response": body[:300],
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
        except urllib.error.HTTPError as he:
            # If 404, might be other endpoint variant
            if he.code == 404:
                last_error = f"HTTP 404 on {endpoint}"
                continue
            err_body = he.read().decode("utf-8", errors="replace")[:200]
            return {
                "channel": "WhatsApp (OpenWA)",
                "status": "FAILED",
                "mock_mode": False,
                "error": f"OpenWA HTTP {he.code}: {err_body}",
                "endpoint": endpoint,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as ex:
            last_error = str(ex)

    # If all endpoints failed
    return {
        "channel": "WhatsApp (OpenWA)",
        "status": "UNREACHABLE",
        "mock_mode": True,
        "error": f"Could not connect to OpenWA at {clean_base} ({last_error}). Ensure OpenWA is running: docker run -p 3000:3000 rmyndharis/openwa",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def send_whatsapp_message(text: str, phone: Optional[str] = None, title: Optional[str] = None) -> Dict[str, Any]:
    """
    Universal WhatsApp dispatcher.
    Routes to CallMeBot or OpenWA based on user configuration in whatsapp_config.json.
    """
    cfg = load_whatsapp_config()
    provider = cfg.get("provider", "callmebot").lower()
    target_phone = phone or cfg.get("phone", "+23058169420")

    formatted_msg = text
    if title:
        formatted_msg = f"*{title}*\n\n{text}"

    if provider == "openwa":
        openwa_cfg = cfg.get("openwa", {})
        base_url = openwa_cfg.get("base_url", "http://localhost:3000")
        chat_id = openwa_cfg.get("chat_id") or target_phone
        api_key = openwa_cfg.get("api_key", "")
        session = openwa_cfg.get("session", "default")
        result = _send_openwa(base_url=base_url, chat_id=chat_id, text=formatted_msg, api_key=api_key, session=session)
        result["provider"] = "openwa"
        return result
    else:
        # CallMeBot
        cmb_cfg = cfg.get("callmebot", {})
        api_key = cmb_cfg.get("api_key") or os.getenv("CALLMEBOT_API_KEY", "").strip()
        result = _send_callmebot(phone=target_phone, text=formatted_msg, api_key=api_key)
        result["provider"] = "callmebot"
        return result
