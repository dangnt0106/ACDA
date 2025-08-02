from abc import ABC, abstractmethod

class BaseTTS(ABC):
    @abstractmethod
    async def synthesize(self, text: str, voice: str, output_path: str) -> str:
        pass
