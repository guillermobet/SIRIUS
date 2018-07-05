from django.test import TestCase
from .models import *
from django.db import transaction, IntegrityError
from django.test import Client


class TestRegister(TestCase):
    
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def run_templateLogin(self):
        response=self.client.get('/login/')
        self.assertTemplateUsed(response, login.html)

    def test_login_details(self):
        # Issue a GET request.
        response = self.client.get('/login/')
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        
    def run_templates(self):
        response=self.client.get('/register/')
        self.assertTemplateUsed(response, register.html)

    def test_details(self):
        # Issue a GET request.
        response = self.client.get('/register/')
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)


    # BASICAS:  Captura de los datos tipo post 

    def test_post_data(self):
        response = self.client.post('/register/', 
            data = { 'user': 'usuario', 'email': 'usuario@gmail.com' , 'full_name': 'Usuario Registro',
                 'password': 'Mipassword123',  'password_confirmation': 'Mipassword123'
                })

        self.assertEquals(User.objects.count(), 1)
        last_user = User.objects.first()
        self.assertEquals(last_user.email, 'usuario@gmail.com')
        self.assertEquals(response.status_code, 302)


    #############################################################################
    #                           PRUEBAS DE FRONTERA                             #        
    #############################################################################

    # FRONTERA : Full name no puede ser un campo vacio, el minimo que puede ser es 1 
    def test_name(self):
        response = self.client.post('/register/', 
        data = { 'user': 'usuario2', 'email': 'name@gmail.com', 'full_name': 'U',
                 'password': 'Mipassword123',  'password_confirmation': 'Mipassword123'
                })

        self.assertEquals(User.objects.count(),1)
        last_user = User.objects.first()
        self.assertEquals(len(last_user.full_name), 1)


    # FRONTERA : Eser no puede ser un campo vacio, al menos un caracter
    def test_last_name(self):
        response = self.client.post('/register/', 
        data = { 'user': 'U',  'email': 'nameu@gmail.com', 'full_name': 'Usuario Registro',
                 'password': 'Mipassword123',  'password_confirmation': 'Mipassword123'
                })
        self.assertEquals(User.objects.count(),1)
        last_user = User.objects.first()
        self.assertEquals(len(last_user.user), 1)



    # FRONTERA : contraseña debe ser mayor a 0 
    def test_password_length(self):
        response = self.client.post('/register/', 
        data = { 'user': 'usuario', 'email': 'usuario@gmail.com' , 'full_name': 'Usuario Registro', 
        'password': '32j',  'password_confirmation': '32j'
                })
        self.assertEquals(User.objects.count(),1)
      


        


    #############################################################################
    #                           PRUEBAS DE ESQUINA                              #        
    #############################################################################

    #ESQUINA:
    #Full name debe tener maximo 100 caracteres
    def test_min_name_max_last(self):
        response = self.client.post('/register/', 
        data = { 'user': 'usuario', 'email': 'usuario@gmail.com' , 'full_name': 'UsuarioRegUsuarioRegUsuarioRegUsuarioRegUsuarioRegUsuarioReg',
                 'password': 'Mipassword123',  'password_confirmation': 'Mipassword123'
                })
        self.assertEquals(User.objects.count(), 1)
        last_user = User.objects.last()
        self.assertEquals(len(last_user.full_name), 60)


    #ESQUINA:
    #contraseña maximo 32 caracteres e email 32
    def test_min_passowd_max_last(self):
        response = self.client.post('/register/', 
        data = { 'user': 'usuariopp', 'email': 'MipasswordMipassword@Mipassw.com' , 'full_name': 'Usuario Registro',
                 'password': 'UsuarioRegUsuarioRegUsuarioReg22',  'password_confirmation': 'UsuarioRegUsuarioRegUsuarioReg22'
                })
        self.assertEquals(User.objects.count(), 1)
        last_user = User.objects.last()
        self.assertEquals(len(last_user.email), 32)


    #############################################################################
    #                           PRUEBAS DE MALICIA                              #        
    #############################################################################

   #MALICIA: password menores al tamaño minimo 

    def test_min_passorwd_max_last(self):
        response = self.client.post('/register/', 
        data = { 'user': 'usuario', 'email': 'usuario@gmail.com' , 'full_name': 'Usuario Registro',
                 'password': '',  'password_confirmation': ''
                })
        self.assertEquals(User.objects.count(), 0)


    #MALICIA: nombre con caracteres especiales
    def test_name_with_special_symbols(self):
        response = self.client.post('/register/', 
        data = { 'user': 'usuario', 'email': 'usuario@gmail.com' , 'full_name': 'Usuarioñ%$&#"Registro',
                 'password': 'Mipassword123',  'password_confirmation': 'Mipassword123'
                })
        self.assertEquals(User.objects.count(), 1)


    #MALICIA: email sin arroba. 
        
    def test_email(self):
        response = self.client.post('/register/', 
        data = { 'user': 'usuario', 'email': 'usuariogmail.com' , 'full_name': 'Usuario Registro',
                 'password': 'Mipassword123',  'password_confirmation': 'Mipassword123'
                })
        self.assertEquals(User.objects.count(),0 )

    #MALICIA: correo incompleto  contiene un solo punto 

    def test_email_imcomplete(self):
        response = self.client.post('/register/', 
        data = { 'user': 'usuario', 'email': 'u.com' , 'full_name': 'Usuario Registro',
                 'password': 'Mipassword123',  'password_confirmation': 'Mipassword123'
                })
        self.assertEquals(User.objects.count(),0 )


    #MALICIA: contraseñas diferentes

    def test_diferents_password(self):
            response = self.client.post('/register/', 
            data = { 'user': 'usuario', 'email': 'usuario@gmail.com' , 'full_name': 'Usuario Registro',
                 'password': 'Mipassword12g3',  'password_confirmation': 'Mipassword123'
                })
            self.assertEquals(User.objects.count(),0 )


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
        self.testWebsite = Website.objects.create(
            url = 'https://test.case',
            name = 'Test',
            description = 'Cualquier cosa'
        )
        self.testWebsite2 = Website.objects.create(
            url = 'https://test.case2',
            name = 'Test2',
            description = 'Cualquier cosa'
        )

            
    def test_creationSameURL(self):   
        try:
            with transaction.atomic():
                asd = Website.objects.create(
                    url = self.testWebsite.url,
                    name = 'Busqueda',
                    description= 'Cualqueir cosa',
                )
            self.fail('Integrity net boing checked propperly at URL link')
        except IntegrityError:
            pass
    
    def test_creationSameName(self):   
        try:
            with transaction.atomic():
                asd = Website.objects.create(
                    url = 'http://Www.google.com.ve',
                    name = self.testWebsite2.name,
                    description= 'Cualqueir cosa',
                )
            self.fail('Integrity net boing checked propperly at URL name')
        except IntegrityError:
            pass


class ReviewTestCase(TestCase):
    def setUp(self):
        #USERS
        user= User.objects.create(
            user = 'RegularUser',
            email = 'regular@gmail.com',
            full_name = 'Regular Test Case User',
            telephone = '4122569351',
            is_staff = False
        )
        user.save()
        #WEBSITES
        testWebsite = Website.objects.create(
            url = 'https://test.case',
            name = 'ttest',
            description = 'Cualquier cosa'
        )
        testWebsite.save()

        testWebsite2 = Website.objects.create(
            url = 'https://test.case2',
            name = 'ttest2',
            description = 'Cualquier cosa'
        )

        testWebsite2.save()

        web = Website.objects.get(name='ttest')
        web2 = Website.objects.get(name='ttest2')
        users= User.objects.get(user='RegularUser')
        
        self.testReview = Review.objects.create(
            website= web,
            username= users,
            browser = 'Chrome',
            browser_version = '66',
            UP = 2.5,
            partial=False
        )
        self.testReview2 = Review.objects.create(
            website= web2,
            username= users,
            browser = 'Chrome',
            browser_version = '66',
            UP = 3.0,
            partial =True,
        )
    def test_ReviewUpdate(self):
        web = Review.objects.get(website = self.testReview.website )
        web.UP = 5.0
        web.save()
        last_user = Review.objects.first()
        self.assertEquals(last_user.UP, 5)


    def test_ReviewUpdate2(self):
        web = Review.objects.get(website = self.testReview2.website )
        web.partial = False
        web.save()
        count = Review.objects.first()
        self.assertEquals(count.partial, False)

    def test_ReviewUpdate3(self):
        web = Review.objects.get(website = self.testReview.website )
        web.UP = 5.0
        web.partial =True
        web.save()
        count = Review.objects.first()
        self.assertEquals(Review.objects.count(), 2)
        self.assertEquals(count.partial, True)
        self.assertEquals(count.UP, 5.0)