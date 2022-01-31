from users.models import CustomUser
from users.pagination import CustomPagination
from users_administration.serializers import CitySerializer
from utils.serializers import PrivatePaginatedResponceSerializer


class AdminCustomPagination(CustomPagination):
    def get_meta(self):
        hints = CitySerializer(CustomUser.objects.all(), many=True)
        return PrivatePaginatedResponceSerializer(
            data={
                "pagination": {
                    "total": self.page.paginator.count,
                    "page": self.page.number,
                    "size": len(self.page)},
                "hint": {
                    "city": hints.data}
            }).to_json()
