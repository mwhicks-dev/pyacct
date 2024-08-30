from sqlalchemy.orm import Session as SQLSession

from model import Attribute, AttributeDetails
from schema import AttributeDto

class AttributeService:

    @staticmethod
    def create_attribute(db: SQLSession, key: str, 
            required: bool, sensitive: bool, unique: bool) -> None:
        db_attribute = AttributeDetails(key=key,
                        required=required, sensitive=sensitive, unique=unique)
        db.add(db_attribute)
        db.commit()

        return
    
    @staticmethod
    def read_attribute(db: SQLSession, key: str) -> AttributeDetails | None:
        return db.query(AttributeDetails).filter(
            AttributeDetails.key == key).first()
    
    @staticmethod
    def update_attribute(db: SQLSession, key: str, 
                         required: bool, sensitive: bool, unique: bool) -> None:
        db_attribute = AttributeService.read_attribute(db=db, key=key)
        if db_attribute is None:
            AttributeService.create_attribute(db=db, key=key, required=required, 
                sensitive=sensitive, unique=unique)
            return

        db_attribute.required = required
        db_attribute.sensitive = sensitive
        db_attribute.unique = unique
        db.commit()

        return
    
    @staticmethod
    def delete_attribute(db: SQLSession, key: str) -> None:
        db.query(Attribute).filter(Attribute.key == key).delete()
        db.query(AttributeDetails).filter(
            AttributeDetails.key == key).delete()
        
        db.commit()

        return
    
    @staticmethod
    def create_account_attribute(db: SQLSession, account_id: int, 
                                 attribute: AttributeDto) -> None:
        db_attribute = Attribute(account_id=account_id, 
                                 key=attribute.key, value=attribute.value)
        db.add(db_attribute)
        db.commit()

        return
    
    @staticmethod
    def read_account_attribute(db: SQLSession, account_id: int, key: str) -> Attribute | None:
        return db.query(Attribute).filter(Attribute.account_id 
            == account_id).filter(Attribute.key == key).first()
    
    @staticmethod
    def update_account_attribute(db: SQLSession, 
            account_id: int, attribute: AttributeDto) -> None:
        db_attribute = AttributeService.read_account_attribute(db=db, 
            account_id=account_id, key=attribute.key)
        
        if db_attribute is None:
            AttributeService.create_account_attribute(db=db, account_id=account_id,
                attribute=attribute)
            return
        
        db_attribute.value = attribute.value
        db.commit()

        return

    @staticmethod
    def delete_account_attribute(db: SQLSession, account_id: int, key: str) -> None:
        db.query(Attribute).filter(Attribute.account_id == account_id
            ).filter(Attribute.key == key).delete()
        
        return