import enum
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Enum, JSON, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from backend.models.base import Base

class OrderStatus(enum.Enum):
    order_received = 'order_received'
    production_chart = 'production_chart'
    ancillary_prep = 'ancillary_prep'
    site_verification = 'site_verification'
    customer_profiled = 'customer_profiled'
    machine_arrived = 'machine_arrived'
    material_verified = 'material_verified'
    installed = 'installed'

class MachineStatus(enum.Enum):
    in_transit = 'in_transit'
    installed = 'installed'
    under_maintenance = 'under_maintenance'
    decommissioned = 'decommissioned'

class SiteVerificationStatus(enum.Enum):
    pending = 'pending'
    passed = 'passed'
    failed = 'failed'

class ServiceDepartment(enum.Enum):
    electrical = 'electrical'
    mechanical = 'mechanical'
    software_plc = 'software_plc'

class ServiceStatus(enum.Enum):
    open = 'open'
    in_progress = 'in_progress'
    resolved = 'resolved'
    closed = 'closed'

class Customer(Base):
    __tablename__ = "customers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    company = Column(String(255))
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    phone = Column(String(50))
    email = Column(String(255))
    gst = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")


class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.order_received)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    customer = relationship("Customer", back_populates="orders")
    machine = relationship("Machine", uselist=False, back_populates="order", cascade="all, delete-orphan")
    production_chart = relationship("ProductionChart", uselist=False, back_populates="order", cascade="all, delete-orphan")
    ancillary_equipment = relationship("AncillaryEquipment", uselist=False, back_populates="order", cascade="all, delete-orphan")
    site_verification = relationship("SiteVerification", uselist=False, back_populates="order", cascade="all, delete-orphan")
    packing_list = relationship("PackingList", uselist=False, back_populates="order", cascade="all, delete-orphan")
    material_verification = relationship("MaterialVerification", uselist=False, back_populates="order", cascade="all, delete-orphan")
    installation_record = relationship("InstallationRecord", uselist=False, back_populates="order", cascade="all, delete-orphan")


class Machine(Base):
    __tablename__ = "machines"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), unique=True, nullable=False)
    serial_number = Column(String(255), unique=True, nullable=False)
    model = Column(String(255), nullable=False)
    vendor = Column(String(255))
    installation_date = Column(DateTime(timezone=True))
    warranty_start = Column(DateTime(timezone=True))
    warranty_end = Column(DateTime(timezone=True))
    status = Column(Enum(MachineStatus), default=MachineStatus.in_transit)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    order = relationship("Order", back_populates="machine")
    service_calls = relationship("ServiceCall", back_populates="machine", cascade="all, delete-orphan")




# Order Sub-Modules

class ProductionChart(Base):
    __tablename__ = "production_charts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), unique=True, nullable=False)
    notes = Column(Text)
    chart_data = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    order = relationship("Order", back_populates="production_chart")

class AncillaryEquipment(Base):
    __tablename__ = "ancillary_equipment"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), unique=True, nullable=False)
    items = Column(JSONB, nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    order = relationship("Order", back_populates="ancillary_equipment")


class SiteVerification(Base):
    __tablename__ = "site_verifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), unique=True, nullable=False)
    layout_notes = Column(Text)
    floor_dimensions = Column(String(255))
    power_specs = Column(String(255))
    status = Column(Enum(SiteVerificationStatus), default=SiteVerificationStatus.pending)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    order = relationship("Order", back_populates="site_verification")


class PackingList(Base):
    __tablename__ = "packing_lists"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), unique=True, nullable=False)
    accessories = Column(JSONB)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    order = relationship("Order", back_populates="packing_list")

class MaterialVerification(Base):
    __tablename__ = "material_verifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), unique=True, nullable=False)
    is_verified = Column(Boolean, default=False)
    notes = Column(Text)
    verified_at = Column(DateTime(timezone=True))

    order = relationship("Order", back_populates="material_verification")

class InstallationRecord(Base):
    __tablename__ = "installation_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), unique=True, nullable=False)
    installed_by = Column(String(255))
    notes = Column(Text)
    installation_date = Column(DateTime(timezone=True), server_default=func.now())

    order = relationship("Order", back_populates="installation_record")


class ServiceCall(Base):
    __tablename__ = "service_calls"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    machine_id = Column(UUID(as_uuid=True), ForeignKey("machines.id", ondelete="CASCADE"), nullable=False)
    is_warranty = Column(Boolean, default=False)
    department = Column(Enum(ServiceDepartment), nullable=False)
    error_description = Column(Text, nullable=False)
    solution = Column(Text)
    parts_used = Column(JSONB)
    status = Column(Enum(ServiceStatus), default=ServiceStatus.open)
    technician_id = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    machine = relationship("Machine", back_populates="service_calls")
