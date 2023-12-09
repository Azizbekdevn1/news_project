
#User permissions
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

class OnlyloggedSuperUser(LoginRequiredMixin,UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

