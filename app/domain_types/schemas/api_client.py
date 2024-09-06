from datetime import datetime
from typing import List, Optional, Literal
from pydantic import UUID4, BaseModel, Field
from app.domain_types.schemas.base_search_types import BaseSearchFilter, BaseSearchResults

class ApiClientCreateModel(BaseModel):
    ClientName            : Optional[str | None] = Field(default=None, description="Name of the client")
    FirstName             : Optional[str | None] = Field(default=None, description="First name of the client")
    LastName              : Optional[str | None] = Field(default=None, description="Last name of the client")
    ClientCode            : Optional[str | None] = Field(default=None, description="Code of the client")
    ClientInterfaceType   : Optional[Literal['Mobile App', 'Web App', 'Desktop App', 'Other']] = Field(default="Mobile App", description="Type of client interface. Possible values are 'Mobile App', 'Web App', 'Desktop App', 'Other'.")
    IsPrivileged          : Optional[bool] = Field(default=False, description="Indicates whether the client has privileged access. True if the client has elevated permissions, otherwise False.")
    CountryCode           : str = Field( min_length=2, max_length=64, description="Country code of the client")
    Phone                 : str = Field (max_length=10, description="Phone of the client")
    Email                 : str = Field(min_length=5, max_length=512, description="Email of the client")
    Password              : str = Field(min_length=5, max_length=512, description="Password of the client")
    ApiKey                : Optional[str | None] = Field(default=None, description="Api key of the client")
    ValidFrom             : Optional[datetime] = Field(default=None, description="The date and time from which api client is valid.")
    ValidTill             : Optional[datetime] = Field(default=None, description="The date and time until which api client is valid.")
   
ApiClientCreateModel.model_rebuild() 

class ApiClientUpdateModel(BaseModel):
    ClientName            : Optional[str | None] = Field(description="Name of the client")
    FirstName             : Optional[str | None] = Field(description="First name of the client")
    LastName              : Optional[str | None] = Field(description="Last name of the client")
    ClientCode            : Optional[str | None] = Field( description="Code of the client")
    ClientInterfaceType   : Optional[Literal['Mobile App', 'Web App', 'Desktop App', 'Other']] = Field(description="Type of client interface. Possible values are 'Mobile App', 'Web App', 'Desktop App', 'Other'.")
    IsPrivileged          : Optional[bool] = Field(description="Indicates whether the client has privileged access. True if the client has elevated permissions, otherwise False.")
    CountryCode           : Optional[str | None]  = Field( min_length=2, max_length=64, description="Country code of the client")
    Phone                 : Optional[str | None]  = Field (max_length=10, description="Phone of the client")
    Email                 : Optional[str | None]  = Field(min_length=5, max_length=512, description="Email of the client")
    Password              : Optional[str | None]  = Field(min_length=5, max_length=512, description="Password of the client")
    ApiKey                : Optional[str | None] = Field( description="Api key of the client")
    ValidFrom             : Optional[datetime] = Field(description="The date and time from which api client is valid.")
    ValidTill             : Optional[datetime] = Field(description="The date and time until which api client is valid.")

ApiClientUpdateModel.model_rebuild()

class ApiClientsSearchFilter(BaseSearchFilter):
    ClientName     : Optional[str | None] = Field(description="Search by the name of the api client")
    Email          : Optional[str | None] = Field(description="Search by the email of the api client")
    Phone          : Optional[str | None] = Field(description="Search by the phone number of the api client")
    ClientCode     : Optional[str | None] = Field(description="Search by the code of the api client")
    CreatedBefore  : Optional[datetime] = Field(description="Search api clients created before the given date")
    CreatedAfter   : Optional[datetime] = Field(description="Search api clients created after the given date")
    PastMonths     : Optional[int] = Field(ge=0, le=12, description="Search api clients created in the past given number of months")

ApiClientsSearchFilter.model_rebuild()

class ApiClientResponseModel(BaseModel):
    id                    : UUID4 = Field(description="Id of the ApiClient")
    ClientName            : Optional[str | None] = Field(default=None, description="Name of the client")
    FirstName             : Optional[str | None] = Field(default=None, description="First name of the client")
    LastName              : Optional[str | None] = Field(default=None, description="Last name of the client")
    ClientCode            : Optional[str | None] = Field(default=None, description="Code of the client")
    ClientInterfaceType   : Optional[Literal['Mobile App', 'Web App', 'Desktop App', 'Other']] = Field(description="Type of client interface. Possible values are 'Mobile App', 'Web App', 'Desktop App', 'Other'.")
    IsPrivileged          : Optional[bool] = Field(description="Indicates whether the client has privileged access. True if the client has elevated permissions, otherwise False.")
    CountryCode           : str = Field( min_length=2, max_length=64, description="Country code of the client")
    Phone                 : str = Field (max_length=10, description="Phone of the client")
    Email                 : str = Field(min_length=5, max_length=512, description="Email of the client")
    ApiKey                : Optional[str | None] = Field(default=None, description="Api key of the client")
    ValidFrom             : Optional[datetime] = Field(description="The date and time from which api client is valid.")
    ValidTill             : Optional[datetime]= Field(description="The date and time until which api client is valid.")
    CreatedAt             : datetime = Field(description="Created at")
    UpdatedAt             : datetime = Field(description="Updated at")

ApiClientResponseModel.model_rebuild()

class ApiClientSearchResults(BaseSearchResults):
    Items : List[ApiClientResponseModel] = Field(description="List of clients")
