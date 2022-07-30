from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

# Creating Model

class TenderHeader(BaseModel):
    Tender: str
    tender_creation_date_and_time: datetime
    stage : str
    contact_no : int
    title_type_of_Project_Procurement_model : str
    tender_called_for : str
    email : str
    multiple_submission : str

    class Config:
        allow_population_by_field_name = True
        

class TenderFeeDetails(BaseModel):
    work : int
    emd : int
    tpf_Inc_of_GST_BSEDC_PAN : int
    cot : str
    description_of_work : str
    estimated_cost : int
    cost_of_boq : int
    region : str
    general_document_upload_required : str
    remarks_if_any : str
        
    class Config:
        allow_population_by_field_name = True

        
class ImportantDates(BaseModel):
    request_of_tender_document_form : datetime
    request_of_tender_document_to : datetime
    bid_clarification_date : datetime
    techno_comercial_open_date_and_time : datetime
    issue_of_tender_document_from : datetime
    issue_of_tender_document_to : datetime
    tender_closing_date_and_time : datetime
    cost_open_date_and_time : datetime
        
    class Config:
        allow_population_by_field_name = True
