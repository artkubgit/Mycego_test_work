from django.test import TestCase, Client
from django.urls import reverse

class FileListViewTest(TestCase):
    def test_file_list_view_exists(self):
        """Проверяет, что view file_list доступна по URL."""
        response = self.client.get(reverse('file_list'))
        self.assertEqual(response.status_code, 200)

    def test_file_list_view_uses_correct_template(self):
        """Проверяет, что view file_list использует правильный шаблон."""
        response = self.client.get(reverse('file_list'))
        self.assertTemplateUsed(response, 'file_list.html')