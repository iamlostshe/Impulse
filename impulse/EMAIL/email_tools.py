import json
import os
import sys
from getpass import getpass, getuser
from pathlib import Path
from smtplib import SMTP, SMTPAuthenticationError

from colorama import Fore

# https://github.com/LimerBoy/Twilight-Algoritm
from impulse.addons.twilight.twilight import Decrypt, Encrypt

# File with login data
sender_email_database = "impulse/EMAIL/sender.json"
twilight_encryption_key = getuser() + ":TWILIGHT"
smtp_server = "smtp.gmail.com"
smtp_port = 587


def WriteSenderEmail():
    """Write sender email."""
    username = input(
        f"{Fore.BLUE}[?] {Fore.MAGENTA}Please enter your gmail address from which messages will be sent: {Fore.BLUE}",
    )
    password = getpass(
        f"{Fore.BLUE}[?] {Fore.MAGENTA}Please enter your gmail password: {Fore.BLUE}",
    )
    server = SMTP(smtp_server, smtp_port)
    server.ehlo()
    server.starttls()
    # Try login to gmail account
    try:
        server.login(username, password)
    except SMTPAuthenticationError:
        print(
            f"{Fore.RED}[!] {Fore.MAGENTA}Wrong password from account or try enable this:"
            f"\n    https://myaccount.google.com/lesssecureapps{Fore.RESET}",
        )
        sys.exit(1)
    else:
        print(f"{Fore.GREEN}[+] {Fore.YELLOW}Successfully logged in{Fore.RESET}")

    # Saved data to db?
    confirm = input(
        f"{Fore.BLUE}[?] {Fore.MAGENTA}Should this information be retained for future reference? (y/n) : {Fore.BLUE}",
    )
    confirm = confirm.upper() in ("Y", "YES", "1", "TRUE")
    if confirm:
        # Write database
        with Path(sender_email_database).open("w") as db:
            json.dump(
                {
                    "username": Encrypt(username, twilight_encryption_key),
                    "password": Encrypt(password, twilight_encryption_key),
                },
                db,
            )
        print(
            f"{Fore.GREEN}[+] {Fore.YELLOW}Data saved to: {sender_email_database!r}{Fore.RESET}",
        )

    return [server, username]


def ReadSenderEmail() -> list:
    """Read sender email."""
    p = Path(sender_email_database)

    # Create if not exists
    if not p.exists():
        return WriteSenderEmail()
    # Read database
    with p.open() as db:
        auth = json.load(db)
        auth["username"] = Decrypt(auth["username"], twilight_encryption_key)
        auth["password"] = Decrypt(auth["password"], twilight_encryption_key)
    # Login
    server = SMTP(smtp_server, smtp_port)
    server.ehlo()
    server.starttls()
    try:
        server.login(auth["username"], auth["password"])
    except SMTPAuthenticationError:
        print(f"{Fore.RED}[!] {Fore.MAGENTA}Wrong email password{Fore.RESET}")
        os.remove(sender_email_database)
        sys.exit(1)
    else:
        return [server, auth["username"]]
