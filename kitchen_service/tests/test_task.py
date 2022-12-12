import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen_service.models import Task


class TaskTest(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            username="chef",
            password="chef12345",
        )
        self.client.force_login(self.admin)

        get_user_model().objects.create_user(
            username="user",
            password="user12345"
        )

        now = datetime.datetime.now()

        Task.objects.create(
            content="Test_task",
            created=now,
            is_done=False,
            cook=get_user_model().objects.get(id=1)
        )
        Task.objects.create(
            content="Test_task",
            created=now,
            is_done=False,
            cook=get_user_model().objects.get(id=2)
        )

    def test_display_only_users_tasks(self):
        user = get_user_model().objects.get(id=2)
        self.client.force_login(user)
        resp = self.client.get(reverse("kitchen_service:task-list"))

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.context["task_list"]) == 1)

    def test_task_displays_for_admin(self):

        resp = self.client.get(reverse("kitchen_service:task-list"))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context["task_list"]), 2)
