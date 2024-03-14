from rest_framework import serializers

from .models import Listing


class ListingSerializer(serializers.ModelSerializer):
    responsible_name = serializers.CharField(source='responsible.user.first_name', read_only=True)

    class Meta:
        model = Listing
        fields = (
        'title', 'price', 'address', 'link', 'phone_number', 'responsible', 'responsible_name', 'call_status', 'created_at', 'agency')
