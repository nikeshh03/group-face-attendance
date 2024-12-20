from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def about(request):
    context = {
        'stats': {
            'days_guaranteed': '100',
            'households': '15+ Crore',
            'women_participation': '55%',
            'states_covered': '28'
        },
        'objectives': [
            {
                'title': 'Livelihood Security',
                'description': 'Guaranteed wage employment for rural households',
                'icon': 'fa-hands-helping'
            },
            {
                'title': 'Rural Development',
                'description': 'Creating sustainable infrastructure',
                'icon': 'fa-road'
            },
            {
                'title': 'Social Inclusion',
                'description': 'Priority to marginalized communities',
                'icon': 'fa-users'
            },
            {
                'title': 'Environmental Protection',
                'description': 'Focus on conservation and sustainability',
                'icon': 'fa-leaf'
            }
        ]
    }
    return render(request, 'about.html', context)

def features(request):
    context = {
        'features': [
            {
                'title': 'Legal Guarantee',
                'description': 'Right to demand work',
                'icon': 'fa-gavel'
            },
            {
                'title': '100 Days Employment',
                'description': 'Annual guaranteed employment',
                'icon': 'fa-calendar'
            },
            {
                'title': 'Direct Benefits',
                'description': 'Transparent wage payments',
                'icon': 'fa-money-bill'
            }
        ]
    }
    return render(request, 'features.html', context)

def contact(request):
    context = {
        'contacts': {
            'email': 'info@mgnrega.gov.in',
            'phone': '1800-112233',
            'hours': '9:00 AM - 5:00 PM'
        },
        'offices': [
            {
                'name': 'Head Office',
                'address': 'New Delhi',
                'phone': '011-23462456'
            }
        ]
    }
    return render(request, 'contact.html', context)
