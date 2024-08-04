from datetime import datetime, timedelta

from model.session import Session
from util.token_validation import ITokenValidation

created_limit: int = 24 * 60 * 60
used_limit: int = 60 * 60

class PyacctTokenValidator(ITokenValidation):

    def is_token_valid(self, session: Session | None) -> bool:
        if session is None:
            return False

        t = datetime.now()

        difference: timedelta = t - session.created_time
        if difference.total_seconds() > created_limit:
            return False
        
        difference: timedelta = t - session.used_time
        if difference. total_seconds() > used_limit:
            return False
        
        return True