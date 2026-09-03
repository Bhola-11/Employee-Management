from django.test import TestCase
from datetime import date
from apps.organizations.models import Organization
from apps.accounts.models import User
from apps.employees.models import Employee
from apps.helpdesk.models import TicketCategory, HelpdeskTicket, TicketComment

class HelpdeskTicketingTests(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name='Helpdesk Corp', code='HDC')
        self.user = User.objects.create_user(email='bjarne@helpdesk.com', username='bjarne@helpdesk.com', password='Password@123', organization=self.org)
        self.emp = Employee.objects.create(
            organization=self.org, employee_id='EMP-HD-01', first_name='Bjarne', last_name='Stroustrup',
            work_email='bjarne@helpdesk.com', phone_number='+1-555-7878', user=self.user,
            joining_date=date(2025, 1, 1), employment_status='ACTIVE'
        )
        self.cat = TicketCategory.objects.create(organization=self.org, name='IT Hardware Support', code='IT-HW', sla_response_hours=12)

    def test_ticket_creation_and_comment(self):
        ticket = HelpdeskTicket.objects.create(
            organization=self.org, category=self.cat, ticket_number='TKT-1001',
            employee=self.emp, subject='Need 4K Monitor for Workstation',
            description='Dual screen setup required for C++ compiler benchmarking.', priority='HIGH', status='OPEN'
        )
        comment = TicketComment.objects.create(
            ticket=ticket, author=self.user, message='Order placed with IT warehouse.'
        )
        self.assertEqual(ticket.comments.count(), 1)
        self.assertEqual(ticket.category.sla_response_hours, 12)
