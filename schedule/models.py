from django.contrib.auth.models import User
from django.db import models


class Construction(models.Model):
    """
    Model representing a construction.
    Attributes:
        construction (CharField): The name of the construction.
        user (ForeignKey): The user who owns this construction.
    """
    # The name of the construction
    construction = models.CharField(max_length=255, unique=True)

    # The user who owns this construction
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns a string representation of the object.
        This method is called when the object is converted to a string.
        It returns the value of the 'construction' attribute, which represents the name of the construction.
        Returns:
            str: The string representation of the object, which is the construction name.
        """
        # Return the value of the 'construction' attribute
        return self.construction


class Position(models.Model):
    """
    Model representing a position.
    Attributes:
        construction (ForeignKey): The construction this position belongs to.
        user (ForeignKey): The user who owns this position.
        order (PositiveSmallIntegerField): The order of this position.
        name (CharField): The name of this position.
        start_date (DateField): The start date of this position.
        end_date (DateField): The end date of this position.
        cost (DecimalField): The cost of this position.
    """
    # The construction this position belongs to
    construction = models.ForeignKey('Construction', on_delete=models.CASCADE)

    # The user who owns this position
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # The order of this position
    order = models.PositiveSmallIntegerField(default=1)

    # The name of this position
    name = models.CharField(max_length=100)

    # The start date of this position
    start_date = models.DateField()

    # The end date of this position
    end_date = models.DateField()

    # The cost of this position
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        """
        Meta class for Position model.
        Constraints:
            unique_position_per_construction: Ensures that each position is unique per construction.
        """
        # Add the unique constraint to the model
        constraints = [
            models.UniqueConstraint(fields=['construction', 'order', 'name'], name='unique_position_per_construction')
        ]

    def __str__(self):
        """
        Returns a string representation of the object.

        Returns:
            str: The name of the position.
        """
        # Return the name of the position
        return self.name