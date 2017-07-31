from django.db import models

class ContentQueryset(models.query.QuerySet):

    def published(self):
        return self.filter(status='p')

    def draft(self):
        return self.filter(status='d')

    def preview_and_published(self):
        return self.filter(models.Q(status='v') | models.Q(status='p'))

    def alphabetical(self):
        return self.order_by('title')

class ContentManager(models.Manager):

    def get_queryset(self):
        return ContentQueryset(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def draft(self):
        return self.get_queryset().draft()

    def preview_and_published(self):
        return self.get_queryset().preview_and_published()

    def alphabetical(self):
        return self.get_queryset().alphabetical()
