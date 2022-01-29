from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'size'

    def get_meta(self):
        return {"pagination": {
            "total": self.page.paginator.count,
            "page": self.page.number,
            "size": len(self.page)},
        }

    def get_paginated_response(self, data):
        return Response({"data": data,
                         "meta": self.get_meta()
                         })
