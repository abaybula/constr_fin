from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


def validate_positive(value):
    """
    Validates that the value is positive.
    :param value: The value to be validated.
    :type value: int
    :raises ValidationError: If the value is not positive.
    """
    if value < 0:
        raise ValidationError('Order number must be positive.')


class Construction(models.Model):
    """
    Model representing a construction.
    """
    construction_name = models.CharField(max_length=255, unique=True, verbose_name='construction name')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns a string representation of the object.
        :return: The string representation of the object, which is the construction name.
        :rtype: str
        """
        return self.construction_name


class Position(models.Model):
    """
    Model representing a position.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(default=1, validators=[validate_positive])
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        """
        Metaclass for Position model.
        """
        unique_together = ('user', 'order', 'name')

    def __str__(self):
        """
        Returns a string representation of the object.
        :return: The string representation of the object, which is the position name.
        :rtype: str
        """
        return f"{self.user.username} - {self.name}"
