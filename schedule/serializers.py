from rest_framework import serializers

from schedule.models import Position, Construction


class ConstructionSerializer(serializers.ModelSerializer):
    """
    Serializer class for Construction model.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def __init__(self, *args, **kwargs):
        """
        Initializes the ConstructionSerializer class.
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        This method overrides the __init__ method of the parent class (ModelSerializer) to add a hidden field 'user' to
        the serializer fields. The 'user' field is set to the current user making the request using the 'request' context.
        Returns:
            None
        """
        super(ConstructionSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            self.fields['user'] = serializers.HiddenField(default=self.context['request'].user)

    def create(self, validated_data):
        """
        Creates a new Construction object with the given validated data.
        Args:
            validated_data (dict): The validated data for the Construction object.
        Returns:
            Construction: The created Construction object.
        Raises:
            None
        """
        return Construction.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Updates an existing Construction object with the given validated data.
        Args:
            instance (Construction): The existing Construction object to be updated.
            validated_data (dict): The validated data for the Construction object.
        Returns:
            Construction: The updated Construction object.
        Raises:
            None
        """
        instance.user = validated_data.get('user', instance.user)
        instance.construction_name = validated_data.get('construction_name', instance.construction_name)
        instance.save()
        return instance

    class Meta:
        """
        Metaclass for ConstructionSerializer.
        """
        model = Construction
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    """
    Serializer class for Position model.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def __init__(self, *args, **kwargs):
        """
        Initializes the PositionSerializer class.
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        This method overrides the __init__ method of the parent class (ModelSerializer) to add a hidden field 'user' to
        the serializer fields. The 'user' field is set to the current user making the request using the 'request' context.
        Returns:
            None
        """
        super(PositionSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            self.fields['user'] = serializers.HiddenField(default=self.context['request'].user)

    def create(self, validated_data):
        """
        Creates a new Position object with the given validated data.
        Args:
            validated_data (dict): The validated data for the Position object.
        Returns:
            Position: The created Position object.
        Raises:
            None
        """
        return Position.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Updates an existing Position object with the given validated data.
        Args:
            instance (Position): The existing Position object to be updated.
            validated_data (dict): The validated data for the Position object.
        Returns:
            Position: The updated Position object.
        Raises:
            None
        """
        instance.order = validated_data.get('order', instance.order)
        instance.name = validated_data.get('name', instance.name)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.cost = validated_data.get('cost', instance.cost)
        instance.save()
        return instance

    class Meta:
        """
        Metaclass for PositionSerializer.
        """
        model = Position
        fields = '__all__'
