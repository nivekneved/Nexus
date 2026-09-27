"""
Nexus Security Vault — AES-256-GCM Envelope Encryption
======================================================
Protects autonomous agent private keys and sensitive keystores.
Replaces plaintext key exposure with authenticated AES-GCM encryption.
"""

import os
import hashlib
from typing import Dict, Any
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

_DEFAULT_SEED = "nexus_sovereign_vault_anchor_salt_2026_base"

def _get_master_key(salt: bytes) -> bytes:
    """Derives a 256-bit AES key using Scrypt and environment/system secret."""
    secret = os.getenv("NEXUS_VAULT_KEY", _DEFAULT_SEED).encode("utf-8")
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return kdf.derive(secret)


def encrypt_secret(secret_str: str) -> Dict[str, str]:
    """Encrypts a plaintext secret into an AES-256-GCM envelope."""
    salt = os.urandom(16)
    key = _get_master_key(salt)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, secret_str.encode("utf-8"), None)
    return {
        "version": "v1_aes_gcm",
        "salt": salt.hex(),
        "nonce": nonce.hex(),
        "ciphertext": ciphertext.hex()
    }


def decrypt_secret(envelope: Dict[str, str]) -> str:
    """Decrypts an AES-256-GCM envelope back to plaintext string."""
    if not isinstance(envelope, dict) or "ciphertext" not in envelope:
        raise ValueError("Invalid encryption envelope format.")
    salt = bytes.fromhex(envelope["salt"])
    nonce = bytes.fromhex(envelope["nonce"])
    ciphertext = bytes.fromhex(envelope["ciphertext"])
    key = _get_master_key(salt)
    aesgcm = AESGCM(key)
    plaintext_bytes = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext_bytes.decode("utf-8")


def protect_keystore(keystore: Dict[str, Any]) -> Dict[str, Any]:
    """Encrypts any plaintext private key within a keystore dictionary."""
    if "private_key" in keystore and isinstance(keystore["private_key"], str):
        raw_key = keystore["private_key"]
        keystore["encrypted_key"] = encrypt_secret(raw_key)
        del keystore["private_key"]
        keystore["vault_status"] = "ENCRYPTED_AES256_GCM"
    return keystore


def unlock_keystore(keystore: Dict[str, Any]) -> str:
    """Extracts and decrypts private key in-memory on demand."""
    if "encrypted_key" in keystore:
        return decrypt_secret(keystore["encrypted_key"])
    if "private_key" in keystore and isinstance(keystore["private_key"], str):
        return keystore["private_key"]
    raise KeyError("No valid encrypted or plaintext key found in keystore.")
