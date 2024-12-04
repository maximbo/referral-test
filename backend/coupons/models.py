from django.db import models
from django.contrib.auth import get_user_model
from django_sqids import SqidsField


User = get_user_model()


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        related_name="received_invitations",
        on_delete=models.CASCADE,
    )
    coupon = models.ForeignKey(
        "Coupon",
        related_name="sent_invitations",
        on_delete=models.CASCADE,
    )

    created_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(db_index=True, null=True)

    class Meta:  # pyright: ignore
        verbose_name = "отправленное приглашение"
        verbose_name_plural = "отправленные приглашения"


class Coupon(models.Model):
    code = SqidsField(real_field_name="id", min_length=6)
    activated_on = models.DateTimeField(null=True)

    owner = models.OneToOneField(
        User,
        related_name="owned_coupon",
        on_delete=models.CASCADE,
    )
    subscribed_users = models.ManyToManyField(
        User,
        related_name="connected_coupons",
        through=Subscription,
    )

    created_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(db_index=True, null=True, default=None)

    class Meta:  # pyright: ignore
        verbose_name = "купон"
        verbose_name_plural = "купоны"

    def __str__(self) -> str:
        return f"{self.created_on}: {self.code}"

    __repr__ = __str__
