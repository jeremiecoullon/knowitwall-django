from django.contrib import admin
from django.utils.html import format_html
from .models import Episode, FlashSeminar, Classification, Author, Season


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    exclude = ['slug']
    search_fields = ['name']

    def count_episodes(self, obj):
        return obj.episode_set.count()
    count_episodes.short_description = "number of episodes written"
    list_display = ['name', 'thumbnail', 'count_episodes']

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="%s" style="height: 50px; width: auto">' % (obj.image.url))
        else:
            "no image"
    thumbnail.short_description = 'Le author'

# ======================================================

publication_info_description = """<h1>Select publication status</h1>
                                <ul>
                                  <li><strong>Draft:</strong> the episode will not visible on the site</li>
                                  <li><strong>Previewed:</strong> the episode will only visible to logged in admin users
                                  (such as yourself!) and not to anyone else.
                                   Save your changes and go to site to see what the episode will look like once it's published.</li>
                                  <li><strong>Published:</strong> the episode will be visible to everyone</li>
                                </ul>"""

episode_images_description = """<h1>Upload the episode images</h1>
                                <ul>
                                  <li><strong>Topic image:</strong> Cover image for the episode page. By default
                                  this is also used for the homepage (the boxes) and the all_episodes page</li>
                                  <li><strong>Topic image latest:</strong> upload an image here for the main 'featured episode'
                                  box on the homepage. This is usually because the default 'topic image' above isn't cropped correctly for the "featured episode" box</li>
                                  <li><strong>Topic image box:</strong> upload an image here for the circular audio player on mobile.</li>
                                </ul>"""
film_description = "To add the video, enter the link to the youtube video. Otherwise just leave this blank"
audio_description = "To add the audio, upload the .mp3 and add the credits info. Otherwise just leave this blank"
random_stuff_description = """Random styling stuff.
                                <ul>
                                  <li><strong>'by/in' colour:</strong> chooses the colour of the author attribution on the cover image
                                   on the epsiode page</li>
                                  <li><strong>author name size:</strong> this is for authors with annoyingly long name so they can
                                  fit in the episode page (next to their picture). Almost all of them use the 'normal' setting</li>
                                </ul>"""
transcript_image_description = """<h1>How to embed images in the transcript:</h1>
                                <p>To add an image</p>
                                <ol>
                                    <li>Create a new line in the transcript where the image should go</li>
                                    <li>Click on the 'image' icon (4th icon from the left)</li>
                                    <li>Choose 'Upload' tab</li>
                                    <li>Choose file, then click 'Send it to the server'. Then 'OK'</li>
                                    <li>Click 'Save and continue editing' (at the bottom of the page) to save the episode. This will style the image correctly. You can then add the caption to the image</li>
                                </ol>
                                <p>By default the position of the image is in the middle. To change the positioning:</p>
                                <ol>
                                    <li>Click on the image, and go to the 'Advanced' tab</li>
                                    <li>Fill in the box called 'Long description URL', and write either 'left' or 'middle'. Then click 'OK'</li>
                                    <li>Save the episode ('Save and continue editing') to apply the new stying</li>
                                </ol>
"""

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Episode overview', {'fields': ['title', 'abstract']}),
        ('Transcript', {'fields': ['transcript'], 'description': transcript_image_description}),
        ('Author', {'fields': ['author']}),
        ('Classification', {'fields': ['classification', 'season']}),
        ('Episode Images', {'fields': [('topic_image', 'thumbnail', 'image_credits'), 'topic_image_latest', 'topic_image_box'],
                            'description': '{}'.format(episode_images_description)}),
        ('Audio', {'fields': ['audio_mp3', 'narration_credits', 'music_credits'],'description': '{}'.format(audio_description)}),
        ('Film', {'fields': ['video_embed'], 'description': '{}'.format(film_description)}),
        ('Random stuff', {'fields': ['by_in_colour', 'author_name_size'], 'description': '{}'.format(random_stuff_description)}),
        ('Publication info', {'fields': ['status', 'pub_date'],
                            'description': '{}'.format(publication_info_description)}),
        # this line is to add fields to keep Disqus comment section and to keep old KiW slugs
        # ('ID stuff', {'fields': ['unique_id', 'old_KiW_slug'], 'description': "DON'T TOUCH THIS. This is because of Jeremie's shitty coding skillz."}),
    ]

    def get_disciplines(self, obj):
        return " and ".join([c.discipline for c in obj.classification.all()])

    def thumbnail(self, obj):
        if obj.topic_image:
            return format_html('<img src="%s" style="height: 50px; width: auto">' % (obj.topic_image.url))
        else:
            "no image"
    thumbnail.short_description = 'Preview'
    readonly_fields = ('thumbnail',)

    get_disciplines.short_description = "Disciplines"

    list_display = ['title', 'thumbnail', 'status', 'get_disciplines']
    search_fields = ['title']
    ordering = ('-pub_date',)
    list_filter = ['pub_date']
    filter_horizontal = ('classification',)

# ======================================================

class EpisodeInline(admin.TabularInline):
    model = Episode.classification.through
    verbose_name = "Episodes in this discipline"
    verbose_name_plural = "Episodes in this discipline"
    max_num = 0
    readonly_fields = ('episode',)
    can_delete = False



@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):

    def discipline_episode_count(self, obj):
        return obj.episode_set.count()
    discipline_episode_count.short_description = 'Number of episodes'

    list_display = ['discipline', 'academic_field', 'discipline_episode_count']
    inlines = [EpisodeInline,]

# ======================================================

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="%s" style="height: 50px; width: auto">' % (obj.image.url))
        else:
            "no image"

    def season_episode_count(self, obj):
        return obj.episode_set.count()

    season_episode_count.short_description = 'Number of episodes'

    def season_list_episodes(self, obj):
        return list(obj.episode_set.all())

    list_display = ['title', 'thumbnail', 'season_episode_count', 'season_list_episodes']
    fieldsets = [
    ('Season info', {'fields': ['title', 'abstract', 'image'], 'description': 'hello!'}),
    ]

# ======================================================

@admin.register(FlashSeminar)
class FlashSeminarAdmin(admin.ModelAdmin):
    fieldsets = [
    ('Related Episode', {'fields': ['episode']}),
    ('Text stuff', {'fields': ['title', 'description']}),
    ('Event info', {'fields': ['event_date', 'event_location']}),
    ('Publication status', {'fields': ['status']}),
    ]
    list_display = ['title', 'status']
    search_fields = ['title']
