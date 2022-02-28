from rest_framework import serializers

from profiles_api import models


class HelloSerializer(serializers.Serializer):
    """
    Serializes a name field for testing our APIView
    """
    name = serializers.CharField(
        max_length=10,
    )


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializes a user profile object
    """

    class Meta:
        model = models.UserProfile
        # A list of fields in our model we want to manage through our serializer
        fields = ('id', 'email','name','password')
        # We want to make exception to password: write only
        extra_kwargs = {
            'password': {
                # 'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            }
        }
    
    # Override the create function.
    # So we create new user by create_user function instead of the default create function.
    def create(self, validated_data):
        """
        Create and return new user.
        """
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        return user

    # Override the update function.
    # If the update part include password => we need to hash password
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)


class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """
    Serializes profile feed item
    """
    class Meta:
        model = models.ProfileFeedItem
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        extra_kwargs = {
            'user_profile': {
                'read_only': True,
            },
        }