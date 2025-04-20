from django.db import models
from common.models import BaseModel
from order.models import OrderItem
from user_profile.models import UserProfile


class PurchaseOrderInvoice(BaseModel):
    PO_STATUS = [
        ("Approval_Pending", "Approval_Pending"),
        ("Approved", "Approved"),
        ("In-Progress", "In-Progress"),
        ("Fulfilled", "Fulfilled"),
        ("Payment_Pending", "Payment_Pending"),
        ("Payment_Completed", "Payment_Completed"),
    ]
    order_item = models.ForeignKey(
        OrderItem,
        on_delete=models.CASCADE,
        related_name="po_order_item",
        null=True,
        blank=True,
    )
    sender = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="po_sender",
        null=True,
        blank=True,
    )
    reciever = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="po_reciever",
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=100,
        choices=PO_STATUS,
        blank=True,
        null=True,
        default="Approval_Pending",
    )
    is_payment_done = models.BooleanField(default=False)
    is_invoiced = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)
