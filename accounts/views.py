from django.shortcuts import render
from .forms import RegistrationForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)        
        if form.is_valid():
            
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            type = form.cleaned_data['type']
            user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,type=type,username=username)
            user.phone_number = phone_number
            user.save()
            
            # USER ACTIVATION email sending
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/acount_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            
            return redirect('/accounts/login/?command=verification&email='+email)
        else:
            print('form is invalid',form.errors)
        
    else:
        form = RegistrationForm()
    context = {
        'form':form,
    }
    return render(request, 'accounts/register.html', context)
    
    
   
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account is activated.")
        
        return redirect('login')
        
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')
      