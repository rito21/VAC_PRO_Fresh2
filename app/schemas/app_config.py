from pydantic import BaseModel


# Schema for tbl_config
class ConfigCreate(BaseModel):
    passwd_length: int
    max_tries: int
    passwd_exp: int


class ConfigInfo(BaseModel):
    id: int
    passwd_length: int
    max_tries: int
    passwd_exp: int