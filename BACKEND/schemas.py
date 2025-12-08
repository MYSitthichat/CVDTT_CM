from pydantic import BaseModel
from typing import List, Optional

class SearchResult(BaseModel):
    id: int
    name: str
    surname: Optional[str] = "" 
    tax_id: Optional[str] = "-"
    display_text: str

class NewCustomer(BaseModel):
    group_id: Optional[str] = ""
    title_name: Optional[str] = ""
    name: Optional[str] = ""
    mid_name: Optional[str] = ""
    surname: Optional[str] = ""
    tax_id: Optional[str] = ""
    phone: Optional[str] = ""
    email: Optional[str] = ""
    line_ID: Optional[str] = ""
    address: Optional[str] = ""
    bill_address: Optional[str] = ""
    updater: Optional[int] = None

class MolecularBiologyData(BaseModel):
    sample_id: str
    tests: List[dict]
    cPCR_req: Optional[int] = 0
    qPCR_req: Optional[int] = 0
    extraction_req: Optional[int] = 0
    status: Optional[int] = 1
    updater: Optional[int] = None

class ParasiteBiologyData(BaseModel):
    sample_id: str
    tests: List[dict]
    status: Optional[int] = 1
    updater: Optional[int] = None

class BacteriaBiologyData(BaseModel):
    sample_id: str
    sample_preparation: List[dict]
    drug_sensitivity: List[dict]
    bacteria_identification: List[dict]
    lab_request: List[dict]
    remark: Optional[str] = ""
    status: Optional[int] = 1
    updater: Optional[int] = None

class SpecimenData(BaseModel):
    case_id: Optional[int] = None
    name: Optional[str] = ""
    opd_number: Optional[str] = ""
    sex: Optional[str] = ""
    age_year: Optional[int] = 0
    age_month: Optional[int] = 0
    age_day: Optional[int] = 0
    demise: Optional[str] = ""
    species: str
    breed: Optional[str] = ""
    sample_type: Optional[str] = ""
    weight: Optional[float] = 0.0
    dead_date: Optional[str] = None
    collect_date: Optional[str] = None
    keep_method: Optional[str] = ""
    speed: Optional[str] = ""
    medical_record: Optional[str] = ""
    dosage_record: Optional[str] = ""
    sample_inspection: Optional[str] = ""
    updater: Optional[int] = None

class LabOrder(BaseModel):
    sample_id: Optional[str] = ""
    room_id: Optional[str] = None
    comments: Optional[str] = ""
    state: Optional[str] = "0"
    status: Optional[str] = "1"
    updater: Optional[int] = None

class UpdateTrackingLabOrder(BaseModel):
    sample_id: Optional[str] = ""
    tracking_info: Optional[str] = "รับงานเข้าระบบ"
    receiver: Optional[str] = None
    updater: Optional[str] = None

class EmployeeData(BaseModel):
    title: Optional[str] = ""
    name: Optional[str] = ""
    surname: Optional[str] = ""
    email: Optional[str] = ""
    username: Optional[str] = ""
    password: Optional[str] = None
    group_id: Optional[int] = None
    signature_base64: Optional[str] = None
    status: Optional[int] = 1
    updater: Optional[int] = None

class AfterDeathData(BaseModel):
    sample_id: str
    service_type: str  # 'Infectious Waste', 'Cremation', or 'Jewelry'
    service_data: Optional[dict] = None  # Contains waste_details, cremation_details, or jewelry_details
    updater: Optional[int] = None