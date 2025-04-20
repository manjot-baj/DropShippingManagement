import random
import string

ORDER_STATUS_COLORS = {
    "Placed": "#FFA500",  # Orange – indicates a new order, awaiting action
    "Confirmed": "#1E90FF",  # Dodger Blue – represents progress and validation
    "Shipped": "#6A5ACD",  # Slate Blue – implies transition, in motion
    "Delivered": "#28A745",  # Green – universal symbol of success/completion
}

PO_STATUS_COLORS = {
    "Approval_Pending": "#FFA500",  # Orange – action required
    "Approved": "#1E90FF",  # Blue – confirmed
    "In-Progress": "#17A2B8",  # Teal – ongoing activity
    "Fulfilled": "#28A745",  # Green – successful completion
    "Payment_Pending": "#FFC107",  # Amber – financial action required
    "Payment_Completed": "#6F42C1",  # Purple – completed, distinct from fulfillment
}


def generate_order_id(length=12):
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choices(chars, k=length))
