from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView, CreateView

from apicbase.forms import UserForm
from apicbase.models import CustomUser


class LoginView(FormView):
    """
    Provides the ability to login as a user with a username and password
    """
    success_url = '/'
    form_class = AuthenticationForm
    redirect_field_name = 'next'
    template_name = 'login.html'

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name, '')
        if not is_safe_url(url=redirect_to, allowed_hosts=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/login/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class SignupView(CreateView):
    """
    Provides users the ability to signup
    """
    model = CustomUser
    template_name = 'register.html'
    form_class = UserForm
    success_url = '/'

    def form_valid(self, form):
        response = super(SignupView, self).form_valid(form)
        # auth_user = authenticate(
        #     username=self.object.username,
        #     password=self.object.password
        # )
        login(self.request, self.object)
        return response


def redirect_view(request):
    if 'GET' == request.method:
        return redirect('recipe-show-all')
