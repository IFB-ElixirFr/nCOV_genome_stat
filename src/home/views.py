from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from home.forms import applicationUserForm, UserForm, contactForm
from home.models import countries

def home(request):
    return render(request, "home/index.html")

def thanks(request, userName):
     return render(request, 'home/thanks.html', context={
         'userName':userName,
     })



def contact(request):
    if request.method == 'POST':
        form = contactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['email']
            cc_myself = form.cleaned_data['cc_myself']

            recipients = ['thomas.denecker@france-bioinformatique.fr']
            if cc_myself:
                recipients.append(sender)

            send_mail(subject, message, sender, recipients)
            return HttpResponseRedirect(reverse('thanks', args=[sender]))
    else:
        form = contactForm()

    return render(request, 'home/contact.html', {'form': form})


def register(request):
    error = False
    country_list = countries.objects.values_list('ADMIN', flat=True)
    if request.method == "POST":
        u_form = UserForm(request.POST)
        p_form = applicationUserForm(request.POST, data_list=country_list)

        updated_request = request.POST.copy()
        updated_request.update({'country': countries.objects.get(ADMIN=p_form.data['country'])})
        p_form = applicationUserForm(updated_request, data_list=country_list)

        if u_form.is_valid():
            user = u_form.save(commit=False)
            if User.objects.filter(username=user.username).count() != 0:
                messages.info(request, 'Username already exists !')

            if p_form.is_valid():
                user = u_form.save()
                p_form = p_form.save(commit=False)
                p_form.user = user
                p_form.save()
                return HttpResponseRedirect(reverse('thanks', args=[user.username]))
            else:
                print("Not valid")
                error = True
        else:
            error = True
    else:
        u_form = UserForm(request.POST)
        p_form = applicationUserForm(request.POST, data_list=country_list)

    return render(request, 'home/signUp.html', {'u_form': u_form, 'p_form': p_form, 'error': error})