from django.http import HttpResponse

def login(request):
    return HttpResponse("This is the login page")
def home(request):
    return HttpResponse("This is the home page")
