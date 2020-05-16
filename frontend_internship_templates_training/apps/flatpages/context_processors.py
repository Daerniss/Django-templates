from .models import FlatPage

def flatpages(request):
    return {
        'flatpages': FlatPage.objects.all()
    }
