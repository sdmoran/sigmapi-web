from django.contrib.auth.models import Group, User
from django.test import Client, TestCase
from django.urls import reverse

class AddUserTest(TestCase):
    fixtures = ['dev_data']

    def setUp(self):
        self.p_group = Group.objects.get(name='Pledges')
        self.client = Client()
        self.client.force_login(User.objects.get(username='sage'))

    def test_group_add_on_create_user(self):
        """
        Test if the Pledges group is added to a user
        when they are added through the Add User form
        """
        path = reverse('userinfo-add_users')
        self.client.post(path, {
            'username': 'tu',
            'firstname': 'Test',
            'lastname': 'User',
            'major': 'Computer Science',
            'class': 2000,
            'type': 'SINGLE',
        })

        created_user = User.objects.get(username='tu')

        self.assertEqual(created_user.groups.count(), 1)
        self.assertIn(self.p_group, created_user.groups.all())
