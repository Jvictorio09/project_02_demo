from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from myApp.models import Property, Lead
from myApp.management.commands.seed_props import Command


class PropertyHubTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a superuser for admin access
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='testpass123'
        )

    def test_home_page_loads(self):
        """Test that the home page loads successfully"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Find Your Perfect Property')

    def test_results_page_loads(self):
        """Test that the results page loads successfully"""
        response = self.client.get(reverse('results'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Search Results')

    def test_property_detail_page_loads(self):
        """Test that property detail page loads for existing property"""
        # First create a property
        property_obj = Property.objects.create(
            slug='test-property',
            title='Test Property',
            price_amount=50000,
            city='Test City',
            beds=2,
            baths=1
        )
        
        response = self.client.get(reverse('property_detail', args=[property_obj.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, property_obj.title)

    def test_property_detail_page_404(self):
        """Test that property detail page returns 404 for non-existent property"""
        response = self.client.get(reverse('property_detail', args=['non-existent-slug']))
        self.assertEqual(response.status_code, 404)

    def test_book_page_loads(self):
        """Test that the book page loads successfully"""
        response = self.client.get(reverse('book'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Book a Call')

    def test_thanks_page_loads(self):
        """Test that the thanks page loads successfully"""
        response = self.client.get(reverse('thanks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You\'re All Set!')

    def test_lead_submit_creates_lead(self):
        """Test that lead submission creates a new lead"""
        # Test data
        lead_data = {
            'name': 'John Doe',
            'phone': '+63 912 345 6789',
            'email': 'john@example.com',
            'buy_or_rent': 'rent',
            'budget_max': 100000,
            'beds': 2,
            'areas': 'BGC, Makati',
            'consent_contact': True
        }
        
        # Submit lead form
        response = self.client.post(reverse('lead_submit'), lead_data)
        
        # Check that lead was created
        self.assertEqual(Lead.objects.count(), 1)
        lead = Lead.objects.first()
        self.assertEqual(lead.name, 'John Doe')
        self.assertEqual(lead.phone, '+639123456789')  # Should be cleaned
        self.assertEqual(lead.email, 'john@example.com')
        self.assertEqual(lead.buy_or_rent, 'rent')
        self.assertEqual(lead.budget_max, 100000)
        self.assertEqual(lead.beds, 2)
        self.assertEqual(lead.areas, 'BGC, Makati')
        self.assertTrue(lead.consent_contact)
        
        # Check redirect to thanks page
        self.assertEqual(response.status_code, 302)
        self.assertIn('/thanks', response.url)

    def test_lead_submit_invalid_form(self):
        """Test that invalid lead form doesn't create lead"""
        # Test with missing required fields
        lead_data = {
            'name': '',  # Required field missing
            'phone': '+63 912 345 6789',
            'buy_or_rent': 'rent',
            'consent_contact': True
        }
        
        response = self.client.post(reverse('lead_submit'), lead_data)
        
        # Check that no lead was created
        self.assertEqual(Lead.objects.count(), 0)
        
        # Should redirect to home for invalid form
        self.assertEqual(response.status_code, 302)

    def test_seed_command(self):
        """Test that the seed command creates properties"""
        # Run the seed command
        command = Command()
        command.handle()
        
        # Check that properties were created
        self.assertEqual(Property.objects.count(), 8)
        
        # Check that properties have expected data
        bgc_properties = Property.objects.filter(city='Taguig')
        self.assertEqual(bgc_properties.count(), 2)
        
        # Check price ranges
        expensive_properties = Property.objects.filter(price_amount__gte=200000)
        self.assertEqual(expensive_properties.count(), 1)  # Luxury penthouse
        
        budget_properties = Property.objects.filter(price_amount__lt=50000)
        self.assertEqual(budget_properties.count(), 2)  # Two budget studios

    def test_results_with_filters(self):
        """Test that results page filters work correctly"""
        # First seed some properties
        command = Command()
        command.handle()
        
        # Test city filter
        response = self.client.get(reverse('results'), {'city': 'Taguig'})
        self.assertEqual(response.status_code, 200)
        # Should have 2 Taguig properties
        
        # Test beds filter
        response = self.client.get(reverse('results'), {'beds': '3'})
        self.assertEqual(response.status_code, 200)
        # Should have properties with 3+ beds
        
        # Test price filter
        response = self.client.get(reverse('results'), {'price_max': '100000'})
        self.assertEqual(response.status_code, 200)
        # Should have properties under 100k

    def test_results_after_seed(self):
        """Test that results page shows properties after seeding"""
        # Seed properties
        command = Command()
        command.handle()
        
        # Check results page
        response = self.client.get(reverse('results'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '8 matches found')  # Should show count

    def test_phone_cleaning(self):
        """Test that phone numbers are cleaned properly"""
        lead_data = {
            'name': 'Jane Doe',
            'phone': '+63 912 345 6789',  # Has spaces
            'buy_or_rent': 'buy',
            'consent_contact': True
        }
        
        response = self.client.post(reverse('lead_submit'), lead_data)
        
        lead = Lead.objects.first()
        self.assertEqual(lead.phone, '+639123456789')  # Spaces removed

    def test_utm_tracking(self):
        """Test that UTM parameters are captured"""
        lead_data = {
            'name': 'Test User',
            'phone': '+63 912 345 6789',
            'buy_or_rent': 'rent',
            'consent_contact': True
        }
        
        # Simulate UTM parameters in cookies
        self.client.cookies['utm_source'] = 'google'
        self.client.cookies['utm_campaign'] = 'property_search'
        
        response = self.client.post(reverse('lead_submit'), lead_data)
        
        lead = Lead.objects.first()
        self.assertEqual(lead.utm_source, 'google')
        self.assertEqual(lead.utm_campaign, 'property_search')
