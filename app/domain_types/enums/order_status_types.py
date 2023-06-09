from enum import Enum

class OrderStatusTypes(Enum):
    DRAFT              = 'Draft'
    INVENTRY_CHECKED   = 'Inventry Checked'
    PLACED             = 'Placed'
    CONFIRMED          = 'Confirmed'
    PAYMENT_INITIATED  = 'Payment Initiated'
    PAYMENT_COMPLETED  = 'Payment Completed'
    PAYMENT_FAILED     = 'Payment Failed'
    CANCELLED          = 'Cancelled'
    SHIPPED            = 'Shipped'
    DELIVERED          = 'Delivered'
    CLOSED             = 'Closed'
    REOPENED           = 'Reopened'
    RETURN_INITIATED   = 'Return Initiated'
    RETURNED           = 'Returned'
    REFUND_INITIATED   = 'Refund Initiated'
    REFUNDED           = 'Refunded'
    EXCHANGE_INITIATED = 'Exchange Initiated'
    EXCHANGED          = 'Exchanged'

