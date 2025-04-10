from .forms import SubscriberForm

def newsletter_form(request):
    return {'form': SubscriberForm()}
