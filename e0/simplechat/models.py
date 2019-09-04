from django.db import models

class Message(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=50)
    created_at = models.DateTimeField()

    def __str__(self):
        return f"{self.text} by {self.author}"