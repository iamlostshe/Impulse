import json
import random
import string

from fake_useragent import UserAgent

ua = UserAgent()


MAILS = (
    "mail.ru",
    "inbox.ru",
    "list.ru",
    "bk.ru",
    "ya.ru",
    "yandex.com",
    "yandex.ua",
    "yandex.ru",
    "gmail.com",
)


def random_name() -> str:
    """Create random name."""
    with open("impulse/SMS/names.json") as names:
        return random.choice(json.load(names)["names"])


def random_suffix(int_range: int | None = 4) -> str:
    """Create random suffix for email.

    %random_name%SUFFIX@%random_email%
    """
    return "".join(
        [str(random.randint(1, 9)) for _ in range(int_range)],
    )


def random_email() -> str:
    """Create random email by name, suffix, mail.

    Example: Jefferson3715@gmail.com
    """
    return random_name() + random_suffix() + "@" + random.choice(MAILS)


def random_password() -> str:
    """Create random password.

    %random_name%%random_suffix%
    """
    return random_name() + random_suffix(10)


def random_token() -> str:
    """Create random token.

    %token%
    """
    letters = string.ascii_letters + string.digits
    return "".join(random.choice(letters) for _ in range(random.randint(20, 50)))


def random_useragent() -> str:
    """Get random user agent."""
    return ua.random
