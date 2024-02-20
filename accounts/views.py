from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from accounts.forms import SignupForm, LoginForm, UpdateProfileForm,  UpdateUserForm


@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = UpdateProfileForm(request.POST, request.FILES,
                                         instance=request.user.profile)
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.avatar
            profile_form.save()
            user_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('storage:root')

    else:
        profile_form = UpdateProfileForm(instance=request.user.profile)
        user_form = UpdateUserForm(instance=request.user)
    return render(request, 'registration/profile.html',
                  {'profile_form': profile_form, 'user_form':user_form})


class CustomLoginView(LoginView):

    redirect_authenticated_user = True
    success_url = reverse_lazy("storage:root")
    form_class = LoginForm


class SignupView(generic.CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'registration/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("storage:root")
        return super(SignupView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('accounts:login')
        return render(request, self.template_name, {'form': form})

