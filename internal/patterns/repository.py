from abc import ABC, abstractmethod
from typing import  Any, Never

class AbstractRepository(ABC):
    '''Abstract class for CRUID operations with database'''

    @abstractmethod
    async def add_one(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError
    
    @abstractmethod
    async def update_one(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError
    
    @abstractmethod
    async def delete_one(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError
    
    @abstractmethod
    async def get_all(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError
