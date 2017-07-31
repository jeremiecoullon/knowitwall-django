from django.test import TestCase
from content.models import Episode
from .utils import create_episode

class EpisodeSlugTests(TestCase):

    def test_save_creates_slug(self):
        """
        Creating an episode and an author should automatically create a slug for each
         using 'slugify'.
        """
        create_episode(title="a fun Title with _underscores!", author_name="hip-ass author")
        le_episode = Episode.objects.get(title="a fun Title with _underscores!")
        self.assertEqual(le_episode.author.name, "hip-ass author")
        self.assertEqual(le_episode.slug, "a-fun-title-with-_underscores")
        self.assertEqual(le_episode.author.slug, "hip-ass-author")

    def test_create_youtube_embed(self):
        """
        Test the youtube URL processing function. It should either return an 'embed' style
        youtube or return an empty string.
        Try out a bunch of potential inputs in `url_dict`; keys are inputs and values are the expected outputs
        """
        url_dict = {
        "https://www.youtube.com/embed/JWcaePIBLCU": "https://www.youtube.com/embed/JWcaePIBLCU?autoplay=1",
        "https://www.youtube.com/watch?v=cyZFhJbedA4": "https://www.youtube.com/embed/cyZFhJbedA4?autoplay=1",
        "https://www.youtube.com/embed/JWcaePIBLCU?autoplay=0": "https://www.youtube.com/embed/JWcaePIBLCU?autoplay=1",
        "": "",
        "Not a url!": "",
        "https://www.youtube.com/watch?v=mjnAE5go9dI&t=3337s": "https://www.youtube.com/embed/mjnAE5go9dI?autoplay=1",
        "http://knowitwall.com/": "",

        }
        create_episode(title="a fun Title with _underscores!", author_name="hip-ass author")
        le_episode = Episode.objects.get(title="a fun Title with _underscores!")
        for raw_url, expected_url in url_dict.items():
            self.assertEqual(expected_url,le_episode.create_youtube_embed(url=raw_url))
