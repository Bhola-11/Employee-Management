from django.test import TestCase, Client
from django.urls import reverse
from apps.accounts.models import User, Role, UserRoleAssignment
from apps.organizations.models import Organization

class AccountsRBACTests(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name='Acme Corp', code='ACM')
        self.role_super = Role.objects.create(name='Super Admin', code='SUPER_ADMIN', is_system_role=True)
        self.role_hr = Role.objects.create(name='HR Manager', code='HR_MANAGER', is_system_role=True)
        self.role_emp = Role.objects.create(name='Employee', code='EMPLOYEE', is_system_role=True)
        
        self.user = User.objects.create_user(
            email='testuser@acme.com', username='testuser@acme.com', password='Password@123',
            organization=self.org, active_role=self.role_emp
        )
        UserRoleAssignment.objects.create(user=self.user, role=self.role_emp, organization=self.org, is_primary=True)
        self.client = Client()

    def test_user_creation_and_auth(self):
        login_success = self.client.login(username='testuser@acme.com', password='Password@123')
        self.assertTrue(login_success)

    def test_role_assignment(self):
        self.assertEqual(self.user.role_assignments.count(), 1)
        self.assertEqual(self.user.role_assignments.first().role.code, 'EMPLOYEE')

    def test_switch_active_role(self):
        UserRoleAssignment.objects.create(user=self.user, role=self.role_hr, organization=self.org, is_primary=False)
        self.client.login(username='testuser@acme.com', password='Password@123')
        res = self.client.post(reverse('accounts:switch_role', args=['HR_MANAGER']))
        self.assertEqual(res.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.active_role.code, 'HR_MANAGER')

    def test_roles_matrix_view(self):
        self.client.login(username='testuser@acme.com', password='Password@123')
        res = self.client.get(reverse('accounts:roles_matrix'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, '13 Roles Matrix')
