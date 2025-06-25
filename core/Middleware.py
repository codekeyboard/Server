from abc import ABC, abstractmethod

class Middleware(ABC):
    @abstractmethod
    async def next(self, request, handler):
        """
        Process the request and pass it to the next handler.
        :param request: The incoming request object.
        :param handler: The next handler to call.
        :return: The response from the next handler.
        """
        pass
