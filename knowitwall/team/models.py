from django.db import models
from ckeditor.fields import RichTextField

def teammember_image_directory_path(instance, filename):
    # Author images will be uploaded to MEDIA_ROOT/TeamMember/<author_name>/<filename>
    return 'TeamMember_images/{0}/{1}'.format(instance.name, filename)


class TeamMember(models.Model):
    name = models.CharField(max_length=200, default="le name")
    role = models.CharField(max_length=100, default="role within Knowitwall")
    image = models.ImageField(upload_to=teammember_image_directory_path, null=True, blank=True)
    bio = RichTextField(default="le bio", config_name='default')

    def __str__(self):
        return self.name
