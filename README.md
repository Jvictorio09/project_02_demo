# PropertyHub - Real Estate Lead Generation Platform

A Django 5.1 MVP real-estate lead generation platform with modern frontend using Tailwind CSS, HTMX, and Alpine.js.

## Features

- **Property Search & Filtering**: Advanced search with filters for location, price, bedrooms, and more
- **Property Details**: Detailed property pages with galleries, specifications, and context-aware chat
- **Context-Aware Chat**: Rule-based property chat that answers questions using property data
- **Listings Dashboard**: Internal dashboard for managing, searching, and sorting properties
- **Lead Capture**: Multi-step lead forms with UTM tracking and consent management
- **Booking System**: Scheduler integration for property consultations
- **Mobile-First Design**: Responsive design with mobile-optimized interactions
- **Admin Interface**: Full Django admin for managing properties and leads

## Tech Stack

- **Backend**: Django 5.1, Python 3.11+
- **Frontend**: Tailwind CSS (CDN), HTMX, Alpine.js
- **Database**: SQLite (development)
- **Static Files**: Custom JavaScript for interactions

## Project Structure

```
myProject/
├── manage.py
├── myProject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── myApp/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── admin.py
│   ├── urls.py
│   ├── tests.py
│   └── management/
│       └── commands/
│           └── seed_props.py
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── results.html
│   ├── property_detail.html
│   ├── book.html
│   ├── thanks.html
│   └── partials/
│       ├── lead_form.html
│       └── lead_success.html
└── static/
    └── app.js
```

## Installation & Setup

### Prerequisites

- Python 3.11 or higher
- pip (Python package installer)

### Step 1: Clone and Setup

```bash
# Navigate to project directory
cd project_02

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install Django
pip install django==5.1.*
```

### Step 2: Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser (optional, for admin access)
python manage.py createsuperuser
```

### Step 3: Seed Demo Data

```bash
# Add demo properties to database
python manage.py seed_props
```

### Step 4: Run Development Server

```bash
# Start the development server
python manage.py runserver
```

### Step 5: Access the Application

Open your browser and visit:
- **Main Site**: http://127.0.0.1:8000
- **Admin Panel**: http://127.0.0.1:8000/admin

## Usage

### Home Page (`/`)
- Hero search with filters
- Top picks property grid
- Neighborhood quick links

### Search Results (`/list`)
- Advanced filtering sidebar
- Property cards with specs
- Mobile-friendly filter drawer

### Property Details (`/property/<slug>/`)
- Property gallery and specifications
- AI chat widget (stub)
- Lead capture form

### Booking (`/book`)
- Scheduler placeholder
- WhatsApp integration
- Lead recap if available

### Thank You (`/thanks`)
- Confirmation page
- WhatsApp deep links
- Next steps information

### Listings Dashboard (`/dashboard`)
- Internal dashboard for property management
- Search and filter properties
- Sort by date, price, bedrooms
- Pagination and bulk actions
- Copy property links

### Property Chat (`/property/<slug>/chat`)
- Context-aware chat widget on property pages
- Rule-based responder using property data
- Answers questions about price, beds, location, parking
- HTMX-powered real-time responses

## Models

### Property
- UUID primary key
- Slug, title, description
- Price, location (city, area)
- Specifications (beds, baths, floor area, parking)
- Hero image URL, badges
- Affiliate source, commission tracking

### Lead
- UUID primary key
- Contact info (name, phone, email)
- Preferences (buy/rent, budget, beds, areas)
- Interest tracking (property IDs)
- UTM tracking (source, campaign, referrer)
- Consent management

## API Endpoints

- `GET /` - Home page
- `GET /list` - Search results with filters
- `GET /property/<slug>/` - Property detail
- `POST /property/<slug>/chat` - Property chat (HTMX endpoint)
- `POST /lead/submit` - Lead submission (HTMX compatible)
- `GET /book` - Booking page
- `GET /thanks` - Thank you page
- `GET /dashboard` - Listings dashboard for internal users

## Testing

Run the test suite:

```bash
python manage.py test
```

Tests cover:
- Page loading and routing
- Lead form submission and validation
- Property seeding
- Search filtering
- UTM parameter tracking
- Dashboard functionality
- Property chat responses
- Pagination and sorting

## Customization

### Adding New Properties

Use the Django admin or create a custom management command:

```python
from myApp.models import Property

Property.objects.create(
    slug='new-property',
    title='New Property Title',
    price_amount=75000,
    city='Your City',
    # ... other fields
)
```

### Styling

The project uses Tailwind CSS via CDN. To customize:

1. Modify templates in `templates/` directory
2. Update Tailwind classes as needed
3. Add custom CSS in `static/` directory if required

### JavaScript Functionality

Core JavaScript is in `static/app.js`:
- UTM parameter capture
- Shortlist functionality (localStorage)
- HTMX integration
- Form handling

## Production Deployment

For production deployment:

1. Set `DEBUG = False` in settings
2. Configure proper database (PostgreSQL recommended)
3. Set up static file serving
4. Configure environment variables for `SECRET_KEY`
5. Set up proper logging and monitoring

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is for educational and demonstration purposes.

## Support

For questions or issues:
- Check the Django documentation: https://docs.djangoproject.com/
- Review the test suite for usage examples
- Check the admin panel for data management

---

**Note**: This is an MVP (Minimum Viable Product) for demonstration purposes. For production use, consider additional security measures, performance optimizations, and comprehensive testing.
"# project_02_demo" 
