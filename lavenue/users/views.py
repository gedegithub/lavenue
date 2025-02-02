from django.contrib.auth import login
from django.urls.base import reverse_lazy
from django.views.generic import CreateView

from .forms import UserCreationForm


class CreateAccountView(CreateView):
	form_class = UserCreationForm
	template_name = "create_account.html"
	success_url = reverse_lazy('login')

	def form_valid(self, form):
		user = form.save()
		login(self.request, user)
		return super().form_valid(form)
