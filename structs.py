import dataclasses

@dataclasses
class USSDRequest:
    path: str
    phone: str
    session_id: str | None = None
    service_code: str | None = None
    params: dict = {}
    
    
