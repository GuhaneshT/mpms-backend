import enum


class OrderStatus(str, enum.Enum):
    order_received = 'order_received'
    production_chart = 'production_chart'
    ancillary_prep = 'ancillary_prep'
    site_verification = 'site_verification'
    customer_profiled = 'customer_profiled'
    machine_arrived = 'machine_arrived'
    material_verified = 'material_verified'
    installed = 'installed'


class MachineStatus(str, enum.Enum):
    in_transit = 'in_transit'
    installed = 'installed'
    under_maintenance = 'under_maintenance'
    decommissioned = 'decommissioned'


class SiteVerificationStatus(str, enum.Enum):
    pending = 'pending'
    passed = 'passed'
    failed = 'failed'


class ServiceDepartment(str, enum.Enum):
    electrical = 'electrical'
    mechanical = 'mechanical'
    software_plc = 'software_plc'


class ServiceStatus(str, enum.Enum):
    open = 'open'
    in_progress = 'in_progress'
    resolved = 'resolved'
    closed = 'closed'
