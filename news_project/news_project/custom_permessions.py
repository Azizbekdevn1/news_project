
#User permissions
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

class Onlylogged(LoginRequiredMixin,UserPassesTestMixin):
    def test_function(self):
        return self.request.user.is_superuser

