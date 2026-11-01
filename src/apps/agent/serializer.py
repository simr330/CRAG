from rest_framework import serializers


class DeterministicGuardRail(serializers.Serializer):
    print('serializer start')
    message = serializers.CharField(
        required=True,
        allow_blank=False,
        allow_null=False,
        trim_whitespace=True,
        max_length=5000,
    )

    def validate_message(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Message cannot be empty."
            )
        print('validation done')
        return value

