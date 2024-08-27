from abc import ABC, abstractmethod

from model.session import Session

class ITokenValidation(ABC):

    @abstractmethod
    def is_token_valid(self, session: Session) -> bool:
        pass