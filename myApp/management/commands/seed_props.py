from django.core.management.base import BaseCommand
from myApp.models import Property
import uuid


class Command(BaseCommand):
    help = 'Seed the database with demo properties'

    def handle(self, *args, **options):
        # Clear existing properties
        Property.objects.all().delete()
        
        # Demo properties data
        properties_data = [
            {
                'slug': 'modern-condo-bgc',
                'title': 'Modern 2BR Condo in BGC',
                'description': 'Beautiful modern condo with city views, perfect for young professionals. Features open-plan living, modern kitchen, and access to building amenities.',
                'price_amount': 85000,
                'city': 'Taguig',
                'area': 'BGC',
                'beds': 2,
                'baths': 2,
                'floor_area_sqm': 65,
                'parking': True,
                'hero_image': 'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800',
                'badges': 'Furnished, Pool, Gym',
                'affiliate_source': 'PropertyGuru',
                'commissionable': True
            },
            {
                'slug': 'luxury-penthouse-makati',
                'title': 'Luxury Penthouse in Makati',
                'description': 'Stunning penthouse with panoramic city views. Features high-end finishes, private terrace, and premium location in the heart of Makati.',
                'price_amount': 250000,
                'city': 'Makati',
                'area': 'Ayala Avenue',
                'beds': 3,
                'baths': 3,
                'floor_area_sqm': 120,
                'parking': True,
                'hero_image': 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800',
                'badges': 'Luxury, Penthouse, City View',
                'affiliate_source': 'Lamudi',
                'commissionable': True
            },
            {
                'slug': 'cozy-studio-ortigas',
                'title': 'Cozy Studio in Ortigas',
                'description': 'Affordable studio unit perfect for students or young professionals. Walking distance to offices and shopping centers.',
                'price_amount': 35000,
                'city': 'Pasig',
                'area': 'Ortigas Center',
                'beds': 1,
                'baths': 1,
                'floor_area_sqm': 25,
                'parking': False,
                'hero_image': 'https://images.unsplash.com/photo-1522708323598-d192d84dfb3b?w=800',
                'badges': 'Student-friendly, Near MRT',
                'affiliate_source': 'MyProperty',
                'commissionable': True
            },
            {
                'slug': 'family-house-quezon-city',
                'title': 'Spacious Family House in QC',
                'description': 'Perfect family home with garden space and multiple bedrooms. Quiet neighborhood with good schools nearby.',
                'price_amount': 120000,
                'city': 'Quezon City',
                'area': 'Diliman',
                'beds': 4,
                'baths': 3,
                'floor_area_sqm': 180,
                'parking': True,
                'hero_image': 'https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=800',
                'badges': 'Family-friendly, Garden, Near Schools',
                'affiliate_source': 'Property24',
                'commissionable': True
            },
            {
                'slug': 'executive-condo-bgc',
                'title': 'Executive 1BR in BGC',
                'description': 'Executive condo unit with premium amenities. Perfect for business professionals working in BGC.',
                'price_amount': 95000,
                'city': 'Taguig',
                'area': 'BGC',
                'beds': 1,
                'baths': 1,
                'floor_area_sqm': 45,
                'parking': True,
                'hero_image': 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800',
                'badges': 'Executive, Business District',
                'affiliate_source': 'PropertyGuru',
                'commissionable': True
            },
            {
                'slug': 'modern-townhouse-pasig',
                'title': 'Modern Townhouse in Pasig',
                'description': 'Contemporary townhouse with modern design and smart home features. Great for growing families.',
                'price_amount': 180000,
                'city': 'Pasig',
                'area': 'Capitol Commons',
                'beds': 3,
                'baths': 2,
                'floor_area_sqm': 150,
                'parking': True,
                'hero_image': 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800',
                'badges': 'Modern, Smart Home, Family',
                'affiliate_source': 'Lamudi',
                'commissionable': True
            },
            {
                'slug': 'budget-friendly-makati',
                'title': 'Budget-Friendly Studio in Makati',
                'description': 'Affordable studio unit in the heart of Makati. Perfect for those starting their career in the business district.',
                'price_amount': 45000,
                'city': 'Makati',
                'area': 'Poblacion',
                'beds': 1,
                'baths': 1,
                'floor_area_sqm': 20,
                'parking': False,
                'hero_image': 'https://images.unsplash.com/photo-1522708323598-d192d84dfb3b?w=800',
                'badges': 'Budget-friendly, Central Location',
                'affiliate_source': 'MyProperty',
                'commissionable': True
            },
            {
                'slug': 'premium-condo-quezon-city',
                'title': 'Premium 3BR Condo in QC',
                'description': 'Premium condo with luxury amenities and great views. Perfect for families who want comfort and convenience.',
                'price_amount': 150000,
                'city': 'Quezon City',
                'area': 'Eastwood',
                'beds': 3,
                'baths': 2,
                'floor_area_sqm': 95,
                'parking': True,
                'hero_image': 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800',
                'badges': 'Premium, Family, Amenities',
                'affiliate_source': 'Property24',
                'commissionable': True
            }
        ]
        
        # Create properties
        created_count = 0
        for prop_data in properties_data:
            property_obj = Property.objects.create(**prop_data)
            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(f'Created property: {property_obj.title}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} demo properties!')
        )
