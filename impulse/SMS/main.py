import random

import impulse.SMS.send_request as request

__services = request.getServices()


def flood(target):
    """Get services list."""
    service = random.choice(__services)
    service = request.Service(service)
    service.sendMessage(target)
