from contextlib import contextmanager
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class SubnetPool(Base):

    __tablename__ = "subnetpool"

    #attrs
    id = Column(Integer, primary_key=True, index=True)
    prefixname = Column(String, unique=True)
    description = Column(String)
    prefixlen_subnets = Column(Integer)
    
     # relation
    subnets = relationship("Subnet")

    
class Subnet(Base):

    __tablename__ = "subnet"

    #attrs
    id = Column(Integer, primary_key=True, index=True)
    prefixname = Column(String, unique=True)
    status = Column(String)
    cid = Column(String)
    
    subnetpool_id = Column(String, ForeignKey('subnetpool.id'))
    

engine = create_engine("sqlite:///subnetmanager.db")
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()

Base.metadata.drop_all(engine)
Base.metadata.create_all(bind=engine)


subnetpool = SubnetPool(prefixname="10.5.0.0/24", description="Test", prefixlen_subnets=25)
subnet = Subnet(prefixname="10.5.0.0/25", status="in_use", cid="customer-1", subnetpool_id=1)
subnetpool.subnets.append(subnet)
subnet = Subnet(prefixname="10.5.0.128/25", status="free", cid="", subnetpool_id=1)
subnetpool.subnets.append(subnet)
session.add(subnetpool)
session.commit()


subnetpool = SubnetPool(prefixname="10.6.0.0/24", description="Test", prefixlen_subnets=25)
subnet = Subnet(prefixname="10.6.0.0/25", status="free", cid="", subnetpool_id=2)
subnetpool.subnets.append(subnet)
subnet = Subnet(prefixname="10.6.0.128/25", status="free", cid="", subnetpool_id=2)
subnetpool.subnets.append(subnet)
session.add(subnetpool)
session.commit()
