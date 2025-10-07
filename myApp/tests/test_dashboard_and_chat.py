from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from myApp.models import Property, Lead
from myApp.management.commands.seed_props import Command


class DashboardAndChatTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a superuser for admin access
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='testpass123'
        )

    def test_dashboard_route_ok(self):
        """Test that dashboard route returns 200"""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Listings Dashboard')

    def test_dashboard_search(self):
        """Test that dashboard search works correctly"""
        # Seed some properties
        command = Command()
        command.handle()
        
        # Search for BGC properties
        response = self.client.get(reverse('dashboard'), {'q': 'BGC'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'BGC')

    def test_dashboard_filters(self):
        """Test dashboard city filter"""
        # Seed properties
        command = Command()
        command.handle()
        
        # Filter by city
        response = self.client.get(reverse('dashboard'), {'city': 'Taguig'})
        self.assertEqual(response.status_code, 200)
        
        # Should have Taguig properties
        self.assertContains(response, 'Taguig')

    def test_dashboard_sorting(self):
        """Test dashboard sorting options"""
        # Seed properties
        command = Command()
        command.handle()
        
        # Test price ascending
        response = self.client.get(reverse('dashboard'), {'sort': 'price_asc'})
        self.assertEqual(response.status_code, 200)
        
        # Test price descending
        response = self.client.get(reverse('dashboard'), {'sort': 'price_desc'})
        self.assertEqual(response.status_code, 200)
        
        # Test beds descending
        response = self.client.get(reverse('dashboard'), {'sort': 'beds_desc'})
        self.assertEqual(response.status_code, 200)

    def test_dashboard_pagination(self):
        """Test dashboard pagination"""
        # Seed properties
        command = Command()
        command.handle()
        
        # Test pagination
        response = self.client.get(reverse('dashboard'), {'page': 1, 'per': 5})
        self.assertEqual(response.status_code, 200)
        
        # Should have pagination controls
        self.assertContains(response, 'Next')

    def test_property_chat_basic(self):
        """Test property chat endpoint with basic questions"""
        # Create a property
        property_obj = Property.objects.create(
            slug='test-property',
            title='Test Property',
            price_amount=50000,
            city='Test City',
            beds=2,
            baths=1
        )
        
        # Test price question
        response = self.client.post(
            reverse('property_chat', args=[property_obj.slug]),
            {'message': 'What is the price?'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '₱50,000')

    def test_property_chat_beds_question(self):
        """Test property chat with beds question"""
        property_obj = Property.objects.create(
            slug='test-property-2',
            title='Test Property 2',
            price_amount=75000,
            city='Test City',
            beds=3,
            baths=2
        )
        
        response = self.client.post(
            reverse('property_chat', args=[property_obj.slug]),
            {'message': 'How many bedrooms?'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '3 bedroom')

    def test_property_chat_baths_question(self):
        """Test property chat with baths question"""
        property_obj = Property.objects.create(
            slug='test-property-3',
            title='Test Property 3',
            price_amount=60000,
            city='Test City',
            beds=2,
            baths=2
        )
        
        response = self.client.post(
            reverse('property_chat', args=[property_obj.slug]),
            {'message': 'How many bathrooms?'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '2 bathroom')

    def test_property_chat_parking_question(self):
        """Test property chat with parking question"""
        property_obj = Property.objects.create(
            slug='test-property-4',
            title='Test Property 4',
            price_amount=80000,
            city='Test City',
            beds=2,
            baths=1,
            parking=True
        )
        
        response = self.client.post(
            reverse('property_chat', args=[property_obj.slug]),
            {'message': 'Is parking available?'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'available')

    def test_property_chat_location_question(self):
        """Test property chat with location question"""
        property_obj = Property.objects.create(
            slug='test-property-5',
            title='Test Property 5',
            price_amount=90000,
            city='Makati',
            area='BGC',
            beds=2,
            baths=1
        )
        
        response = self.client.post(
            reverse('property_chat', args=[property_obj.slug]),
            {'message': 'Where is this located?'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Makati')
        self.assertContains(response, 'BGC')

    def test_property_chat_availability_question(self):
        """Test property chat with availability question"""
        property_obj = Property.objects.create(
            slug='test-property-6',
            title='Test Property 6',
            price_amount=70000,
            city='Test City',
            beds=1,
            baths=1
        )
        
        response = self.client.post(
            reverse('property_chat', args=[property_obj.slug]),
            {'message': 'Is this available?'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Availability changes daily')

    def test_property_chat_fallback(self):
        """Test property chat fallback response"""
        property_obj = Property.objects.create(
            slug='test-property-7',
            title='Test Property 7',
            price_amount=55000,
            city='Test City',
            beds=1,
            baths=1
        )
        
        response = self.client.post(
            reverse('property_chat', args=[property_obj.slug]),
            {'message': 'What is the meaning of life?'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'pass this to the agent')

    def test_property_chat_invalid_property(self):
        """Test property chat with non-existent property"""
        response = self.client.post(
            reverse('property_chat', args=['non-existent-slug']),
            {'message': 'What is the price?'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 404)

    def test_property_chat_missing_message(self):
        """Test property chat with missing message"""
        property_obj = Property.objects.create(
            slug='test-property-8',
            title='Test Property 8',
            price_amount=65000,
            city='Test City',
            beds=2,
            baths=1
        )
        
        response = self.client.post(
            reverse('property_chat', args=[property_obj.slug]),
            {},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 400)

    def test_dashboard_after_seed(self):
        """Test that dashboard shows properties after seeding"""
        # Seed properties
        command = Command()
        command.handle()
        
        # Check dashboard
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '8 properties found')  # Should show count

    def test_dashboard_empty_state(self):
        """Test dashboard empty state with no properties"""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No properties found')
