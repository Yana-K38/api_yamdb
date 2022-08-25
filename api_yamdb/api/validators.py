from rest_framework import serializers


class MeValidate:

    def __init__(self, fields):
        self.fields = fields

    def __call__(self, value):
        if value['username'].lower() == 'me':
            raise serializers.ValidationError(
                'Имя пользователя не может быть me'
            )
        return value
