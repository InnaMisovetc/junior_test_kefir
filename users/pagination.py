from django.core.paginator import InvalidPage
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.pagination import PageNumberPagination, _positive_int
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'size'

    def get_paginated_response(self, data):
        return Response({"data": data,
                         "meta": self._get_meta()
                         })

    def paginate_queryset(self, queryset, request, view=None):
        errors = {}
        self._validate_query_parameter(request, self.page_size_query_param, errors)
        self._validate_query_parameter(request, self.page_query_param, errors)

        if len(errors) > 0:
            raise ValidationError(errors)

        page_size = self.get_page_size(request)

        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = self.get_page_number(request, paginator)

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def _get_meta(self):
        return {"pagination": {
            "total": self.page.paginator.count,
            "page": self.page.number,
            "size": len(self.page)},
        }

    def _validate_query_parameter(self, request, parameter, errors):
        try:
            _positive_int(request.query_params[parameter], strict=True, cutoff=self.max_page_size)
        except KeyError:
            errors[parameter] = ["This query parameter is required"]
        except ValueError:
            errors[parameter] = ["This query parameter must be a positive integer"]
