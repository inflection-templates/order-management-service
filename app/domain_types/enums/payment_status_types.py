from enum import Enum

class PaymentStatusTypes(Enum):
    INITIATED  = "Initiated"
    INPROGRESS = "In-Progress"
    SUCCEEDED  = "Succeeded"
    FAILED     = "Failed"
    CANCELLED  = "Cancelled"
    REFUNDED   = "Refunded"
    EXPIRED    = "Expired"
    UNKNOWN    = "Unknown"


