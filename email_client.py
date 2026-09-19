import imaplib
import email
from email.header import decode_header
import re
import logging

logger = logging.getLogger(__name__)

class EmailClient:
    """
    Handles secure IMAP connection, searching unread emails,
    parsing MIME payloads & headers (including List-Unsubscribe),
    moving emails between folders, and restoring trashed emails.
    """
    def __init__(self, host: str, port: int, username: str, password: str, 
                 trash_folder: str = "[Gmail]/Trash", review_folder: str = "[Gmail]/Spam",
                 smtp_host: str = "smtp.gmail.com", smtp_port: int = 465):
        self.host = host
        self.port = int(port)
        self.username = username.strip() if username else ""
        self.password = password.replace(" ", "").strip() if password else ""
        self.trash_folder = trash_folder
        self.review_folder = review_folder
        self.smtp_host = smtp_host
        self.smtp_port = int(smtp_port)
        self.mail = None

    def connect(self):
        """Connects and logs into the IMAP email server using SSL."""
        try:
            self.mail = imaplib.IMAP4_SSL(self.host, self.port, timeout=8)
            self.mail.login(self.username, self.password)
            logger.info(f"Successfully connected and logged in as {self.username}")
            self._auto_detect_special_folders()
            return True
        except Exception as e:
            logger.error(f"Failed to connect to IMAP server: {e}")
            raise

    def _auto_detect_special_folders(self):
        """Dynamically detects the exact Trash and Spam folders matching server locale/provider."""
        try:
            typ, folder_list = self.mail.list()
            if typ != 'OK' or not folder_list:
                return
            for f in folder_list:
                decoded = f.decode('utf-8', errors='replace')
                # Check for RFC 6154 special-use flags
                if r"\Trash" in decoded:
                    # Extract folder name in quotes or at end
                    parts = decoded.split(' "/" ')
                    if len(parts) == 2:
                        folder_name = parts[1].strip('"')
                        self.trash_folder = folder_name
                        logger.info(f"Auto-detected IMAP Trash folder: '{self.trash_folder}'")
                elif r"\Junk" in decoded:
                    parts = decoded.split(' "/" ')
                    if len(parts) == 2:
                        folder_name = parts[1].strip('"')
                        self.review_folder = folder_name
                        logger.info(f"Auto-detected IMAP Junk folder: '{self.review_folder}'")
        except Exception as e:
            logger.debug(f"Error auto-detecting special folders: {e}")

    def disconnect(self):
        """Gracefully logs out and closes the IMAP connection."""
        if self.mail:
            try:
                self.mail.close()
            except Exception:
                pass
            try:
                self.mail.logout()
            except Exception:
                pass
            logger.info("Disconnected from IMAP server.")

    def fetch_unread_emails(self, folder="INBOX") -> list:
        """
        Searches the given folder for unread ('UNSEEN') emails
        and returns a list of parsed email dictionaries.
        """
        if not self.mail:
            raise RuntimeError("Not connected to email server. Call connect() first.")

        self.mail.select(folder)
        status, messages = self.mail.uid('search', None, 'UNSEEN')
        if status != 'OK':
            logger.warning(f"Could not search folder {folder}")
            return []

        email_uids = messages[0].split()
        logger.info(f"Found {len(email_uids)} unread email(s) in {folder}")

        parsed_emails = []
        for uid in email_uids:
            res, msg_data = self.mail.uid('fetch', uid, '(RFC822)')
            if res != 'OK':
                continue

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    parsed_email = self._parse_email(uid.decode('utf-8'), msg)
                    parsed_emails.append(parsed_email)

        return parsed_emails

    def _parse_email(self, uid: str, msg) -> dict:
        """Helper to extract sender, subject, date, unsubscribe header, and clean text body."""
        subject = self._decode_str(msg.get("Subject", "(No Subject)"))
        sender = self._decode_str(msg.get("From", "Unknown Sender"))
        reply_to = self._decode_str(msg.get("Reply-To", ""))
        date = msg.get("Date", "")
        
        # Feature 4: Extract List-Unsubscribe header
        unsubscribe_header = msg.get("List-Unsubscribe", "")
        unsubscribe_link = self._extract_unsubscribe_url(unsubscribe_header)

        body = self._extract_body(msg)

        return {
            "uid": uid,
            "sender": sender,
            "reply_to": reply_to,
            "subject": subject,
            "date": date,
            "unsubscribe_link": unsubscribe_link,
            "body": body
        }

    def _extract_unsubscribe_url(self, raw_header: str) -> str:
        """Finds HTTP/HTTPS link or mailto link inside List-Unsubscribe header."""
        if not raw_header:
            return ""
        # Match URL inside angle brackets e.g. <https://.../unsubscribe> or <mailto:...>
        match = re.search(r'<(https?://[^>]+)>', raw_header)
        if match:
            return match.group(1)
        match_mailto = re.search(r'<(mailto:[^>]+)>', raw_header)
        if match_mailto:
            return match_mailto.group(1)
        return raw_header.strip()

    def _decode_str(self, header_value: str) -> str:
        """Decodes MIME encoded-word syntax (e.g. =?UTF-8?B?...?=)."""
        decoded_fragments = decode_header(header_value)
        text_parts = []
        for fragment, encoding in decoded_fragments:
            if isinstance(fragment, bytes):
                try:
                    text_parts.append(fragment.decode(encoding or "utf-8", errors="replace"))
                except Exception:
                    text_parts.append(fragment.decode("latin1", errors="replace"))
            else:
                text_parts.append(str(fragment))
        return "".join(text_parts)

    def _extract_body(self, msg) -> str:
        """Recursively extracts plain text from multipart or single-part emails."""
        body_parts = []

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if content_type == "text/plain" and "attachment" not in content_disposition:
                    payload = part.get_payload(decode=True)
                    if payload:
                        charset = part.get_content_charset() or "utf-8"
                        body_parts.append(payload.decode(charset, errors="replace"))
        else:
            payload = msg.get_payload(decode=True)
            if payload:
                charset = msg.get_content_charset() or "utf-8"
                body_parts.append(payload.decode(charset, errors="replace"))

        return "\n".join(body_parts).strip()

    def move_to_folder(self, uid: str, target_folder: str, dry_run: bool = True) -> bool:
        """
        Safely moves an email to a target folder (e.g. Trash or Review) by UID.
        """
        if dry_run:
            logger.info(f"[DRY-RUN] Would move email UID {uid} to '{target_folder}'")
            return True

        candidates = [target_folder]
        if "trash" in target_folder.lower() or "bin" in target_folder.lower():
            candidates = [target_folder, self.trash_folder, "[Gmail]/Bin", "[Gmail]/Trash", "Trash", "Deleted Items", "Deleted Messages"]
        elif "spam" in target_folder.lower() or "junk" in target_folder.lower():
            candidates = [target_folder, self.review_folder, "[Gmail]/Spam", "Junk", "Bulk"]

        # Deduplicate candidates while preserving order
        unique_candidates = []
        for c in candidates:
            if c and c not in unique_candidates:
                unique_candidates.append(c)

        for folder in unique_candidates:
            try:
                res, _ = self.mail.uid('COPY', uid.encode('utf-8'), folder)
                if res == 'OK':
                    self.mail.uid('STORE', uid.encode('utf-8'), '+FLAGS', '(\\Deleted)')
                    self.mail.expunge()
                    logger.info(f"Successfully moved email UID {uid} to '{folder}'")
                    return True
            except Exception:
                continue

        logger.error(f"Failed to move email UID {uid} across candidate folders: {unique_candidates}")
        return False

    def restore_email(self, uid: str, from_folder: str, to_folder: str = "INBOX") -> bool:
        """
        Feature 7 (Undo/Restore): Moves an email back from Trash/Spam to the INBOX.
        """
        try:
            self.mail.select(from_folder)
            res, _ = self.mail.uid('COPY', uid.encode('utf-8'), to_folder)
            if res == 'OK':
                self.mail.uid('STORE', uid.encode('utf-8'), '+FLAGS', '(\\Deleted)')
                self.mail.expunge()
                logger.info(f"Restored email UID {uid} from '{from_folder}' back to '{to_folder}'")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to restore email UID {uid}: {e}")
            return False

    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        from_name: str = "Deven Pawaray",
        reply_to: str = None,
        html_body: str = None
    ) -> dict:
        """
        Transmits an outbound email via secure SMTP SSL (port 465) or STARTTLS (port 587).
        """
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.header import Header
        from email.utils import formataddr, formatdate, make_msgid

        if not self.username or not self.password:
            raise ValueError("Sender credentials missing. Cannot dispatch email.")

        msg = MIMEMultipart("alternative")
        msg["Subject"] = Header(subject, "utf-8")
        msg["From"] = formataddr((str(Header(from_name, "utf-8")), self.username))
        msg["To"] = to_email
        msg["Date"] = formatdate(localtime=True)
        domain = self.username.split("@")[-1] if "@" in self.username else "nexus.ai"
        msg["Message-ID"] = make_msgid(domain=domain)
        if reply_to:
            msg["Reply-To"] = reply_to

        # Attach plain text part
        msg.attach(MIMEText(body, "plain", "utf-8"))

        # Attach HTML part if provided
        if html_body:
            msg.attach(MIMEText(html_body, "html", "utf-8"))

        clean_pwd = self.password.replace(" ", "").strip()
        host = self.smtp_host or "smtp.gmail.com"
        port = self.smtp_port or 465

        try:
            if port == 465:
                with smtplib.SMTP_SSL(host, port, timeout=15) as server:
                    server.login(self.username, clean_pwd)
                    server.sendmail(self.username, [to_email], msg.as_string())
            else:
                with smtplib.SMTP(host, port, timeout=15) as server:
                    server.ehlo()
                    server.starttls()
                    server.ehlo()
                    server.login(self.username, clean_pwd)
                    server.sendmail(self.username, [to_email], msg.as_string())

            logger.info(f"Outbound email successfully sent to {to_email} via {self.username}")
            return {
                "success": True,
                "sender": self.username,
                "recipient": to_email,
                "subject": subject,
                "message_id": msg["Message-ID"],
                "sent_at": formatdate(localtime=True)
            }
        except Exception as e:
            logger.error(f"SMTP dispatch error from {self.username} to {to_email}: {e}")
            raise e

