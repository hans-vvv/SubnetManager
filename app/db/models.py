from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class SubnetPool(Base):
    __tablename__ = "subnetpool"

    # attrs
    id = Column(Integer, primary_key=True, index=True)
    prefixname = Column(String, unique=True)
    description = Column(String)
    prefixlen_subnets = Column(Integer)

    # relation
    subnets = relationship("Subnet")


class Subnet(Base):
    __tablename__ = "subnet"

    # attrs
    id = Column(Integer, primary_key=True, index=True)
    prefixname = Column(String, unique=True)
    status = Column(String)
    cid = Column(String)

    subnetpool_id = Column(String, ForeignKey("subnetpool.id"))
