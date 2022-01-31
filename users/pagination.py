from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination, _positive_int
from rest_framework.response import Response

from utils.serializers import MetaSerializer, PaginatedResponceSerializer


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'size'

    def get_paginated_response(self, data):
        return Response(PaginatedResponceSerializer(data={"data": data, "meta": self._get_meta()}).to_json())

    def paginate_queryset(self, queryset, request, view=None):
        errors = {}
        self._validate_query_parameter(request, self.page_size_query_param, errors)
        self._validate_query_parameter(request, self.page_query_param, errors)

        if len(errors) > 0:
            raise ValidationError(errors)

        return super(CustomPagination, self).paginate_queryset(queryset, request, view)

    def _get_meta(self):
        return MetaSerializer(data={"pagination": {
            "total": self.page.paginator.count,
            "page": self.page.number,
            "size": len(self.page)},
        }).to_json()

    def _validate_query_parameter(self, request, parameter, errors):
        try:
            _positive_int(request.query_params[parameter], strict=True, cutoff=self.max_page_size)
        except KeyError:
            errors[parameter] = ["This query parameter is required"]
        except ValueError:
            errors[parameter] = ["This query parameter must be a positive integer"]
