from django.db import models
import uuid

from users.models import Profile
# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    caption = models.TextField()
    # image_url = models.ImageField(null=True, blank=True, default="generated.png")
    image_url = models.TextField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    likes = models.IntegerField(null=True, blank=True, default=0)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title