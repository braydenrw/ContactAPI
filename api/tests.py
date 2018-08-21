from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from .views import *


class ContactTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username='admin', email='admin@gmail.com')
        self.user.set_password('badpassword')
        self.user.save()

        Contact.objects.create(name='Archie Carboni', phone_number='13605551234', physical_address='12345 SE 12th Ave',
                               city='Vancouver', state='WA', email='Archie.Carboni@gmail.com', user='admin')
        Contact.objects.create(name='Karmen Braddy', phone_number='13605552345', physical_address='23456 NE 13th Ave',
                               city='Vancouver', state='WA', email='Karmen.Braddyi@gmail.com', user='admin')
        Contact.objects.create(name='Miranda Litwin', phone_number='15035553456', physical_address='34567 NE 14th Ave',
                               city='Portland', state='OR', email='Miranda.Litwin@gmail.com', user='admin')
        Contact.objects.create(name='Jamar Hagerman', phone_number='13605554567', physical_address='45678 SW 15th Ave',
                               city='Vancouver', state='WA', email='Jamar.Hagerman@gmail.com', user='admin')
        Contact.objects.create(name='Eveline Whitman', phone_number='15035555678', physical_address='56789 SW 16th Ave',
                               city='Portland', state='OR', email='Eveline.Whitman@gmail.com', user='admin')

    def test_get_contact_by_id(self):
        # Shows successful return from get_contact
        request = self.factory
        response = get_contact(request, 1)
        self.assertEqual(response.status_code, 200)

        # Shows expected 404 error message on an invalid id
        response = get_contact(request, 0)
        self.assertEqual(response.args[0], 'Contact not found')

    def test_get_full_contact_list(self):
        # Shows expected json in successful return from get_full_contact_list
        test_payload = dict(names='miRanDa litwin,eveLine Whitman,Bob Dylan', emails='jamar.hagerman@gmail.com')
        request = self.factory.get('', data=test_payload)
        response = get_full_contact_list(request)
        expected_response_content = [{"pk": 3, "fields": {"name": "Miranda Litwin", "phone_number": "15035553456", "physical_address": "34567 NE 14th Ave", "city": "Portland", "state": "OR", "email": "Miranda.Litwin@gmail.com", "user": "admin"}}, {"pk": 4, "fields": {"name": "Jamar Hagerman", "phone_number": "13605554567", "physical_address": "45678 SW 15th Ave", "city": "Vancouver", "state": "WA", "email": "Jamar.Hagerman@gmail.com", "user": "admin"}}, {"pk": 5, "fields": {"name": "Eveline Whitman", "phone_number": "15035555678", "physical_address": "56789 SW 16th Ave", "city": "Portland", "state": "OR", "email": "Eveline.Whitman@gmail.com", "user": "admin"}}]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), expected_response_content)

    def test_create_contact(self):
        # Asserts that a new contact was created, successful response only after contact added
        test_payload_with_login = dict(username='admin', password='badpassword', name='new name',
                                       phone_number='12345678910', physical_address='505 SE 40th St', city='Portland',
                                       state='OR', email='new.name@gmail.com')
        request = self.factory.post('', data=test_payload_with_login)
        response = create_contact(request)
        self.assertEqual(response.status_code, 200)

        # Showing authentication is checked
        test_payload_with_bad_login = dict(username='not_admin', password='12345', name='new name',
                                           phone_number='12345678910', physical_address='505 SE 40th St',
                                           city='Portland', state='OR', email='new.name@gmail.com')
        request = self.factory.post('', data=test_payload_with_bad_login)
        response = create_contact(request)
        self.assertEqual(response.status_code, 403)

    def test_edit_contact(self):
        # Shows successful response code on edit
        test_payload = dict(username='admin', password='badpassword', physical_address='505 SE 40th St',
                            city='Portland', state='OR')
        request = self.factory.post('', data=test_payload)
        response = edit_contact(request, 1)
        self.assertEqual(response.status_code, 200)

        # Shows contact was properly updated in the manor expected
        request = self.factory
        response = get_contact(request, 1)
        expected_response_content = [{"pk": 1, "fields": {"name": "Archie Carboni", "phone_number": "13605551234", "physical_address": "505 SE 40th St", "city": "Portland", "state": "OR", "email": "Archie.Carboni@gmail.com", "user": "admin"}}]
        self.assertEqual(json.loads(response.content), expected_response_content)

    def test_delete_contact(self):
        # Shows contact existed before delete is called
        test_payload = dict(username='admin', password='badpassword', contact_id='1')
        request = self.factory
        response = get_contact(request, 1)
        self.assertEqual(response.status_code, 200)

        # Shows successful delete status code
        request_post = self.factory.post('', data=test_payload)
        response = delete_contact(request_post)
        self.assertEqual(response.status_code, 200)

        # Shows successful 404 not found message when contact is no longer there
        response = get_contact(request, 1)
        self.assertEqual(response.args[0], 'Contact not found')
