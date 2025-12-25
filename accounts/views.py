from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from orders.models import Order

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def profile_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/profile.html', {'orders': orders})
