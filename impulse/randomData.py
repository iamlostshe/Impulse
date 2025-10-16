import random

from fake_useragent import UserAgent

ua = UserAgent()


def random_IP() -> str:
    """Get random IP."""
    ip = [str(random.randint(1, 255)) for _ in range(4)]
    return ".".join(ip)


def random_referer() -> str:
    """Get random referer."""
    with open("impulse/L7/referers.txt") as referers:
        return random.choice(referers)


def random_useragent() -> str:
    """Get random user agent."""
    return ua.random
