from users.models import CustomUser
from users.pagination import CustomPagination
from users_administration.serializers import HintSerializer


class AdminCustomPagination(CustomPagination):
    def get_meta(self):
        hints = HintSerializer(CustomUser.objects.all(), many=True)
        return {"pagination": {
            "total": self.page.paginator.count,
            "page": self.page.number,
            "size": len(self.page)},
            "hint": {"city": hints.data}
        }
