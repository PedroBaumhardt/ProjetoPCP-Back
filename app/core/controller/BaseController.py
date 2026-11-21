from typing import TypeVar, Generic

ServiceType = TypeVar("ServiceType")


# -- controller base: apenas guarda o service, sem CRUD e sem conhecer Models
class BaseController(Generic[ServiceType]):
    def __init__(self, service: ServiceType) -> None:
        self.service = service
