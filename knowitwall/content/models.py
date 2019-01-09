from django.db import models
from django.utils import timezone
from django.utils.text import slugify
import uuid
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from .managers import ContentManager
import random
from .images import style_transcript_image
from .util import seasons_image_directory_path, episode_image_directory_path, author_image_directory_path, create_youtube_embed

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

class Season(models.Model):
    title = models.CharField(max_length=100, default="Season title")
    abstract = RichTextField(default="Description of the season", config_name='default')
    image = models.ImageField(upload_to=seasons_image_directory_path, null=True, blank=True, verbose_name="Season image")
    pub_date = models.DateTimeField('date published',default=timezone.now)

    def __str__(self):
        return self.title

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
    author = models.ForeignKey(Author, null=True, on_delete=models.CASCADE, related_name='first_author')
    second_author = models.ForeignKey(Author, null=True, blank=True, on_delete=models.CASCADE, related_name='second_author', help_text="A second author is optional")
    season = models.ForeignKey(Season, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(unique=True,max_length=100, default='le title')
    topic_image = models.ImageField(upload_to=episode_image_directory_path, null=True, blank=True, verbose_name="Cover image")
    topic_image_latest = models.ImageField(upload_to=episode_image_directory_path, null=True, blank=True, verbose_name="'featured episode' cover image", help_text="The cover image for 'featured' on the homepage")
    topic_image_box = models.ImageField(upload_to=episode_image_directory_path, null=True, blank=True, verbose_name="Mobile circular image",help_text="This is for the circular audio player on mobile")
    transcript = RichTextUploadingField(default='le transcript', config_name='transcript', null=True, blank=True)
    abstract = RichTextField(default="le abstract", config_name='default')
    by_in_colour = models.CharField(max_length=1, choices=BY_IN_COLOR_CHOICES, default='w', verbose_name="'by/in' colour")
    author_name_size = models.CharField(max_length=1, choices=AUTHOR_NAME_SIZE_CHOICES, default='n')
    image_credits = RichTextField(default="", config_name='image_credits', blank=True, help_text="Example of the correct format: The Morgan Library & Museum, New York. By <a target='_blank' href='https://commons.wikimedia.org/wiki/File:The_Morgan_Library_%26_Museum.jpg'>Paolatrabanco</a> [<a target='_blank' href='https://creativecommons.org/licenses/by-sa/4.0/deed.en'>CC BY-SA 4.0</a>]")
    narration_credits = models.CharField(default="", max_length=300, blank=True, help_text="Example of correct format: Mary Wellesley and Vidish Athavale")
    music_credits = models.CharField(default='', max_length=300, blank=True, help_text="Example of correct format: Greg Joy and Neil Cross")
    general_credits = models.CharField(default='', max_length=300, blank=True, help_text="Name of podcast interviewer. Example format: 'interviewed by Ellen O'Neill'")
    video_embed = models.CharField(default='', max_length=300, blank=True, verbose_name="Youtube URL")
    audio_mp3 = models.FileField(blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d')
    classification = models.ManyToManyField(Classification, blank=True)
    pub_date = models.DateTimeField('date published',default=timezone.now)
    slug = models.SlugField(unique=True, max_length=120)
    old_KiW_slug = models.CharField(max_length=200, blank=True, help_text="For old episodes (that were on Flask): need to fill this in so that the old links on social media and stuff still work")

    objects = ContentManager()

    def related_episode(self):
        """
        Returns a related episode: an episode that has the same classification as the episode
        If the episode has several classifications, choose one randomly
        """
        related_discipline = random.sample(population=list(self.classification.all()), k=1)[0]
        list_related_episodes = list(related_discipline.episode_set.all())

        if len(list_related_episodes) > 1:
            list_related_episodes = list(filter(lambda x: x!=self, list_related_episodes))
            related_episode = list(random.sample(population=list_related_episodes, k=1))
        else:
            related_episode = None

        return related_episode

    def different_episode(self):
        """
        Returns an unrelated episode: an episode not in the same classification as the current episode
        """
        all_classifications = Classification.objects.order_by('discipline')
        list_different_discipline = list(filter(lambda x: x not in self.classification.all(), all_classifications))
        different_discipline = random.sample(population=list_different_discipline, k=1)[0]
        list_different_episodes = list(different_discipline.episode_set.all())
        a_different_episode = list(random.sample(population=list_different_episodes, k=1))
        return a_different_episode

    def save(self, *args, **kwargs):
        # create slug field from title
        self.slug = slugify(self.title)
        self.video_embed = create_youtube_embed(url=self.video_embed)
        self.transcript = style_transcript_image(input_html=self.transcript)
        super(Episode, self).save(*args, **kwargs)

    @property
    def has_audio(self):
        return bool(self.audio_mp3)

    @property
    def has_video(self):
        return bool(self.video_embed)

    def __str__(self):
        return self.title


class FlashSeminar(models.Model):
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
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
