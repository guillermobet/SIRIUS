from django.test import TestCase
from .models import *
from django.db import transaction, IntegrityError

class UserTestCase(TestCase):
    
    def setUp(self):
        self.regUser = User.objects.create(
            user = 'RegularTestCaseUser',
            email = 'regularTestCaseEmail@gmail.com',
            full_name = 'Regular Test Case User',
            telephone = '4122569351',
            is_staff = False
        )
        
        self.staffUser = User.objects.create(
            user = 'StaffTestCaseUser',
            email = 'staffTestCaseEmail@gmail.com',
            full_name = 'Staff Test Case User',
            telephone = '4122569351',
            is_staff = True
        )
        
    def test_integrity_on_create(self):
        try:
            with transaction.atomic():
                asd = User.objects.create(
                    user = self.regUser.user,
                    email = 'staffTestCase@gmail.com',
                    full_name = 'Staff  Case User',
                    telephone = '4122551',
                    is_staff = True
                )
            self.fail('Integrity net boing checked propperly at User name')
        except IntegrityError:
            pass
            
        try:
            with transaction.atomic():
                asd = User.objects.create(
                    user = 'NewUser',
                    email = self.regUser.email,
                    full_name = 'Staff  Case User',
                    telephone = '4122551',
                    is_staff = True
                )
            self.fail('Integrity net boing checked propperly at User email')
        except IntegrityError:
            pass
            
    def test_integrity_on_update(self):
        asd = User.objects.get(user = self.regUser.user)
        asd.user = self.staffUser.user
        try:
            with transaction.atomic():
                asd.save()
            self.fail('Integrity net boing checked propperly at User name update')
        except IntegrityError:
            pass
            
        asd.user = self.regUser.user
        asd.email = self.staffUser.email
        try:
            with transaction.atomic():
                asd.save()
            self.fail('Integrity net boing checked propperly at User email update')
        except IntegrityError:
            pass
            
class WebsiteTestCase(TestCase):
    
    def setUp(self):
        testWebsite = Website.objects.create(
            url = 'https://test.case',
            name = 'Test Case',
            description = ''
        )
            
        
        

# Create your tests here.
