import django_filters
from django.utils import timezone
from .models import Message, Conversation


class MessageFilter(django_filters.FilterSet):
    """Filter messages by conversation participants and sent_at time range."""

    participant = django_filters.UUIDFilter(field_name='conversation__participants__user_id')
    start = django_filters.IsoDateTimeFilter(field_name='sent_at', lookup_expr='gte')
    end = django_filters.IsoDateTimeFilter(field_name='sent_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['participant', 'start', 'end']
