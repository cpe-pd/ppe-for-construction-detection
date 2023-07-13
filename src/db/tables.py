from sqlalchemy.orm import registry, relationship
from sqlalchemy import (
    Column, Integer, 
    String, DateTime, 
    Boolean, ForeignKey
)
from datetime import datetime

mapper_registry = registry()

# These are PPE detection tables for construction

@mapper_registry.mapped
class PPEClass:
    """
        A mapped class that defines a table that holds classes of PPE for construction.
    """
    __tablename__="ppeclass"
    id = Column(Integer, primary_key=True)
    class_name = Column(String(length=250))
    detectedppeclasses = relationship("DetectedPPEClass", back_populates="ppeclass")
    def __str__(self):
        return f"PPEClass(id={self.id}, name='{self.name}')"
    def __repr__(self):
        return f"'{self.name}'"

# Associative table for PPEClass and violator
@mapper_registry.mapped
class DetectedPPEClass:
    """
        A mapped class that defines a table that asoociates both PPEClass and Violator.
    """
    __tablename__ = "detectedppeclass"
    id = Column(Integer, primary_key=True)
    bbox_id = Column(Integer)
    confidence = Column(Integer)
    violator_id = Column(Integer, ForeignKey("violator.id", ondelete="CASCADE"))
    ppeclass_id = Column(Integer, ForeignKey("ppeclass.id", ondelete="CASCADE"))
    violator = relationship("Violator", back_populates="detectedppeclasses")
    ppeclass = relationship("PPEClass", back_populates="detectedppeclasses")
    def __str__(self):
        return f"DetectedPPEClass(violator='{self.violator}',ppeclass='{self.ppeclass}')"
    def __repr__(self):
        return f"{self.ppeclass}"

@mapper_registry.mapped
class Violator:
    """
        A mapped class that defines a table which contains information about the violator and its detected PPE classes.
    """
    __tablename__="violator"
    id = Column(Integer, primary_key=True)
    bbox_id = Column(Integer)
    x1 = Column(Integer)
    y1 = Column(Integer)
    x2 = Column(Integer)
    y2 = Column(Integer)
    detectedppeclasses = relationship("DetectedPPEClass", back_populates="violator", cascade="all, delete")
    violationdetails_id = Column(Integer, ForeignKey("violationdetails.id", ondelete="CASCADE"))
    violationdetails = relationship("ViolationDetails", back_populates="violators")
    def __str__(self):
        return f"Violator(id={self.id}, detectedppeclasses={self.detectedppeclasses})"
    def __repr__(self):
        return f"Violator(id={self.id}, detectedppeclasses={self.detectedppeclasses})"

@mapper_registry.mapped
class ViolationDetails:
    __tablename__ = "violationdetails"
    id = Column(Integer, primary_key=True)
    image = Column(String(length=250))
    violators = relationship("Violator", back_populates="violationdetails", cascade="all, delete")
    timestamp = Column(DateTime, default=datetime.now())
    devicedetails_id = Column(Integer, ForeignKey("devicedetails.id", ondelete="CASCADE"))
    devicedetails = relationship("DeviceDetails", back_populates="violationdetails")
    def __str__(self):
        return f"ViolationDetails(id={self.id},image='{self.image}',violators='{self.violators}',timestamp={self.timestamp})"
    def __repr__(self):
        return f"ViolationDetails(id={self.id},image='{self.image}',violators='{self.violators}',timestamp={self.timestamp})"
    
@mapper_registry.mapped
class DeviceDetails:
    __tablename__="devicedetails"
    id = Column(Integer, primary_key=True)
    kvs_name = Column(String(length=250))
    uuid = Column(String(length=250))
    password = Column(String(length=250))
    pub_topic = Column(String(length=250))
    set_topic = Column(String(length=250))
    is_active = Column(Boolean, default=False, nullable=False)
    violationdetails = relationship("ViolationDetails", back_populates="devicedetails", cascade="all, delete")
    def __str__(self):
        return f"DeviceDetails(id={self.id}, uuid='{self.uuid}', pub_topic='{self.pub_topic}', set_topic='{self.set_topic}', is_active={self.is_active})"
    def __repr__(self):
        return f"DeviceDetails(id={self.id}, uuid='{self.uuid}', pub_topic='{self.pub_topic}', set_topic='{self.set_topic}', is_active={self.is_active})"
