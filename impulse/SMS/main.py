# Import modules
import impulse.SMS.sendRequest as request
from impulse.SMS import randomData

__services = request.getServices()


def flood(target):
    # Get services list
    service = randomData.random_service(__services)
    service = request.Service(service)
    service.sendMessage(target)
