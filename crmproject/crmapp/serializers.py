from rest_framework import serializers

from .models import Listing


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ('title', 'price', 'address', 'link', 'phone_number', 'responsible', 'call_status', 'created_at', 'agency')
