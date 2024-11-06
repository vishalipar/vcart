from django.shortcuts import render

# Create your views here.

def store(request):
    return render(request, 'store/store.html')
    
def prod_detail(request):
    return render(request, 'store/prod_detail.html')