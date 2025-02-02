import json
from datetime import date, datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from notification.models import Notification
from notification.serializers import DynamicNotificationSerializer
from notification.views import NotificationViewSet
from user.models import User


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        kwargs = self.scope["url_route"]["kwargs"]
        if "user" in self.scope:
            user = self.scope["user"]
        else:
            user_id = kwargs["user_id"]
            user = User.objects.get(id=user_id)

        if user.is_anonymous:
            self.close(code=401)
        else:
            self.user = user
            room = f"notification_{user.id}"
            self.room_group_name = room

            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name, self.channel_name
            )
            self.accept(subprotocol="Token")

    def disconnect(self, close_code):
        if close_code == 401 or not hasattr(self, "room_group_name"):
            return
        else:
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name, self.channel_name
            )

    def send_notification(self, event):
        # Send message to webSocket (Frontend)
        notification_type = event["notification_type"]
        notification_id = event["id"]
        context = NotificationViewSet()._get_context()
        notification = Notification.objects.get(id=notification_id)
        serialized_data = DynamicNotificationSerializer(
            notification,
            _include_fields=[
                "action_user",
                "body",
                "created_date",
                "id",
                "notification_type",
                "read",
                "read_date",
                "recipient",
            ],
            context=context,
        ).data
        data = {"notification_type": notification_type, "data": serialized_data}
        self.send(text_data=json.dumps(data, default=json_serial))
