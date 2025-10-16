# Import modules
import tools.SMS.sendRequest as request
from tools.SMS import randomData

__services = request.getServices()


def flood(target):
    # Get services list
    service = randomData.random_service(__services)
    service = request.Service(service)
    service.sendMessage(target)
