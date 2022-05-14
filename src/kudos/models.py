from django.db import models


class Kudo(models.Model):
    from_user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='to_user')
    date = models.DateField(auto_now_add=True)
    message = models.TextField(max_length=280)

    def __str__(self):
        return self.from_user.username
