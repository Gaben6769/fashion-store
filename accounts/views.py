from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render

from .forms import RegistrationForm, UkrainianAuthenticationForm


def register_view(request):
    """Реєстрація нового користувача."""

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                "Реєстрація успішна. Вітаємо у FASHION STORE!",
            )

            return redirect("home")
    else:
        form = RegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form},
    )


class UserLoginView(LoginView):
    """Вхід користувача."""

    template_name = "accounts/login.html"
    authentication_form = UkrainianAuthenticationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(
            self.request,
            "Ви успішно увійшли до свого акаунта.",
        )
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    """Вихід користувача."""

    next_page = "home"

    def dispatch(self, request, *args, **kwargs):
        messages.info(
            request,
            "Ви вийшли зі свого акаунта.",
        )
        return super().dispatch(request, *args, **kwargs)