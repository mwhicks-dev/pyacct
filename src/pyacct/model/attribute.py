from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, PrimaryKeyConstraint

from persistence.database import Base

class AttributeDetails(Base):
    __tablename__ = "attribute_details"

    key = Column(String, primary_key=True)

    required = Column(Boolean, nullable=False)
    sensitive = Column(Boolean, nullable=False)
    unique = Column(Boolean, nullable=False)

class Attribute(Base):
    __tablename__ = "attributes"

    account_id = Column(Integer, ForeignKey("accounts.id"))
    key = Column(String, ForeignKey("attribute_details.key"))
    value = Column(String)

    # ref: https://stackoverflow.com/questions/10059345/sqlalchemy-unique-across-multiple-columns
    __table_args__ = (PrimaryKeyConstraint("key", "account_id"), )