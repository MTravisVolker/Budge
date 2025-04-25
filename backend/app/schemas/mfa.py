from pydantic import BaseModel

class MFAEnableRequest(BaseModel):
    code: str

class MFAEnableResponse(BaseModel):
    secret: str
    provisioning_uri: str

class MFAVerifyRequest(BaseModel):
    code: str

class MFAVerifyResponse(BaseModel):
    success: bool

class MFADisableRequest(BaseModel):
    code: str
