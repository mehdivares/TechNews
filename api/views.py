from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Tag, News
from django.db.models import Q
from .serializers import NewsSerializer


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by("-published_at")
    serializer_class = NewsSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params

        # Filter by tag name exact match
        if tag_name := params.get('tags'):
            qs = qs.filter(tags__name__iexact=tag_name)

        # Include keywords
        if include := params.get('include'):
            keywords = [kw.strip() for kw in include.split(',')]
            include_q = Q()
            for kw in keywords:
                include_q |= Q(body__icontains=kw)
            qs = qs.filter(include_q)

        # Exclude keywords
        if exclude := params.get('exclude'):
            keywords = [kw.strip() for kw in exclude.split(',')]
            for kw in keywords:
                qs = qs.exclude(body__icontains=kw)

        return qs