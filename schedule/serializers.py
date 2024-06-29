from rest_framework import serializers

from schedule.models import Construction, Position


class ConstructionSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Construction model.
    """
    class Meta:
        """
        Meta class for ConstructionSerializer.
        Attributes:
            model (Construction): The model associated with the serializer.
            fields (list): The fields to include in the serializer.
        """
        # Set the model and fields for the serializer
        model = Construction
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Position model.
    """
    class Meta:
        """
        Meta class for PositionSerializer.
        Attributes:
            model (Position): The model associated with the serializer.
            fields (list): The fields to include in the serializer.
        """
        # Set the model and fields for the serializer
        model = Position
        fields = '__all__'
       