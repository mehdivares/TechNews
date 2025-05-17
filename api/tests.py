from rest_framework import status
from rest_framework.test import APITestCase
from .models import Tag, News
from django.urls import reverse


class NewsTestCase(APITestCase):
    def setUp(self):
        t1 = Tag.objects.create(name='Tech')
        t2 = Tag.objects.create(name='Sports')
        n1 = News.objects.create(title='AI breakthrough', body='New AI Model launched', source='https://example.com')
        n1.tags.add(t1)
        n2 = News.objects.create(title='Football Match', body='Exciting game between teams', source='https://example.com')
        n2.tags.add(t2)

    def test_list_news(self):
        url = reverse('news-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_by_tag(self):
        url = reverse('news-list') + '?tags=Tech'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'AI breakthrough')

    def test_include_keyword(self):
        url = reverse('news-list') + '?include=Exciting'
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Football Match')

    def test_exclude_keyword(self):
        url = reverse('news-list') + '?exclude=teams'
        response = self.client.get(url)
        print(response.data)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'AI breakthrough')

    def test_combined_filters(self):
        url = reverse('news-list') + '?include=game, launched&exclude=AI'
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Football Match')