from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# views.py
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            next_param = request.POST.get('next') or request.GET.get('next')
            if next_param:
                return redirect(next_param)
            return render(request, 'register_success.html')
    else:
        form = UserCreationForm()

    next_param = request.GET.get('next', '')
    return render(request, 'register.html', {
        'form': form,
        'errors': form.errors.items(),
        'next': next_param
    })


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.POST.get('next') or request.GET.get('next', 'blog_list')
            return redirect(next_url)
    else:
        form = AuthenticationForm()

    next_param = request.GET.get('next', '')
    return render(request, 'login.html', {
        'form': form,
        'errors': form.errors.items(),
        'next': next_param
    })


def logout_view(request):
    logout(request)
    return redirect('blog_list')
