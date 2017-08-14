from django.db import models
from django.utils import timezone
from django.utils.text import slugify
import uuid
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from config.settings import AWS_URL
from .managers import ContentManager
import os

STATUS_CHOICES = (
    ('d', 'Draft'),
    ('p', 'Published'),
    ('v', 'Previewed')
)
ACADEMIC_FIELDS_CHOICES = (
    ('S', 'Sciences'),
    ('H', 'Humanities')
)
BY_IN_COLOR_CHOICES = (
    ('w', 'white'),
    ('b', 'black')
)
AUTHOR_NAME_SIZE_CHOICES = (
    ('n', 'normal'),
    ('s', 'smaller')
)


class Classification(models.Model):
    discipline = models.CharField(max_length=100, default="le discipline",help_text="topic discipline (ex: Neuroscience)")
    academic_field = models.CharField(max_length=2, choices=ACADEMIC_FIELDS_CHOICES, help_text="Sciences or Humanities")

    def __str__(self):
        return "{0} ({1})".format(self.discipline, self.get_academic_field_display())

    def save(self, *args, **kwargs):
        self.slug = slugify("_".join((self.academic_field,self.discipline)))
        super(Classification, self).save(*args, **kwargs)


def episode_image_directory_path(instance, filename):
    # Episode images will be uploaded to MEDIA_ROOT/Episode_image-id_<id>/<filename>
    return 'Episodes_images/episode_id-{0}/{1}'.format(instance.unique_id, filename)

def author_image_directory_path(instance, filename):
    # Author images will be uploaded to MEDIA_ROOT/Author_images/<author_name>/<filename>
    return 'Author_images/{0}/{1}'.format(instance.name, filename)

class Author(models.Model):
    name = models.CharField(max_length=200, default="le author name")
    image = models.ImageField(upload_to=author_image_directory_path, null=True, blank=True)
    bio = RichTextField(default="author bio", config_name='default')
    slug = models.SlugField(unique=True, max_length=200)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Author, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Episode(models.Model):
    unique_id = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4, help_text="This determines the Disqus comment section. Need to set this manually for old KiW episodes (that were on Flask)")
    author = models.ForeignKey(Author, null=True)
    title = models.CharField(unique=True,max_length=100, default='le title')
    topic_image = models.ImageField(upload_to=episode_image_directory_path, null=True, blank=True, verbose_name="Cover image")
    topic_image_latest = models.ImageField(upload_to=episode_image_directory_path, null=True, blank=True, verbose_name="'featured episode' cover image", help_text="The cover image for 'featured' on the homepage")
    topic_image_box = models.ImageField(upload_to=episode_image_directory_path, null=True, blank=True, verbose_name="Mobile circular image",help_text="This is for the circular audio player on mobile")
    transcript = RichTextUploadingField(default='le transcript', config_name='transcript')
    abstract = RichTextField(default="le abstract", config_name='default')
    by_in_colour = models.CharField(max_length=1, choices=BY_IN_COLOR_CHOICES, default='b', verbose_name="'by/in' colour")
    author_name_size = models.CharField(max_length=1, choices=AUTHOR_NAME_SIZE_CHOICES, default='n')
    image_credits = RichTextField(default="", config_name='image_credits', blank=True, help_text="Example of the correct format: The Morgan Library & Museum, New York. By <a target='_blank' href='https://commons.wikimedia.org/wiki/File:The_Morgan_Library_%26_Museum.jpg'>Paolatrabanco</a> [<a target='_blank' href='https://creativecommons.org/licenses/by-sa/4.0/deed.en'>CC BY-SA 4.0</a>]")
    narration_credits = models.CharField(default="", max_length=300, blank=True, help_text="Example of correct format: Mary Wellesley and Vidish Athavale")
    music_credits = models.CharField(default='', max_length=300, blank=True, help_text="Example of correct format: Greg Joy and Neil Cross")
    video_embed = models.CharField(default='', max_length=300, blank=True, verbose_name="Youtube URL")
    audio_mp3 = models.FileField(blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d')
    classification = models.ManyToManyField(Classification, blank=True)
    pub_date = models.DateTimeField('date published',default=timezone.now)
    slug = models.SlugField(unique=True, max_length=120)
    old_KiW_slug = models.CharField(max_length=200, blank=True, help_text="For old episodes (that were on Flask): need to fill this in so that the old links on social media and stuff still work")

    objects = ContentManager()

    def create_youtube_embed(self, url):
        """
        Parses URL to youtube video and returns the embeded link.
        """
        if 'www.youtube.com' not in url:
            return ""
        if 'youtube.com/embed' in url:
            if "?" in url:
                url = url.split("?")[0]
            url = url.split('embed/')[-1]
            # return url
        if 'watch' in url:
            url = url.split("=")[1]
        if "&" in url:
            url = url.split("&")[0]
        return os.path.join('https://www.youtube.com','embed',url+'?autoplay=1')

    def save(self, *args, **kwargs):
        # create slug field from title
        self.slug = slugify(self.title)
        self.video_embed = self.create_youtube_embed(url=self.video_embed)
        super(Episode, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class FlashSeminar(models.Model):
    episode = models.ForeignKey(Episode)
    title = models.CharField(max_length=100, unique=True, default='le title')
    event_date = models.DateTimeField(default=timezone.now)
    event_location = models.CharField(max_length=400, default='somewhere')
    description = RichTextField(default='a flash seminar!', config_name='default')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d')
    slug = models.SlugField(unique=True, max_length=120, default='le slug')

    objects = ContentManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(FlashSeminar, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
