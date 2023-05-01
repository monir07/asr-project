from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType


class CustomLogEntry():
    def log_change(self, request, object, message):        
        return LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(object).pk,
            object_id=object.id,
            object_repr=str(object),
            action_flag=CHANGE,
            change_message=message,
            )
    def log_addition(self, request, object, message):
        return LogEntry.objects.log_action(
            user_id=request.user.pk,
            content_type_id=ContentType.objects.get_for_model(object).pk,
            object_id=object.pk,
            object_repr=str(object),
            action_flag=ADDITION,
            change_message=message,
        )
    def log_deletion(self, request, object, message):
        return LogEntry.objects.log_action(
            user_id=request.user.pk,
            content_type_id=ContentType.objects.get_for_model(object).pk,
            object_id=object.pk,
            object_repr=str(object),
            action_flag=DELETION,
            change_message=message,
        )