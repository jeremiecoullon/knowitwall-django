from django.test import TestCase
from content.models import Episode, FlashSeminar
from .utils import create_episode, create_flash_seminar

class Managers(TestCase):

    def test_managers_alphabetical(self):
        """
        Calling alphabetical() on a manager should return a queryset that's sorted
        alphabetically based on title
        """
        create_episode(title="A cool title", author_name="Alice")
        create_episode(title="B is a cool letter", author_name="Bob")
        self.assertQuerysetEqual(Episode.objects.order_by("-pub_date"),
            ['<Episode: B is a cool letter>', '<Episode: A cool title>']
        )
        self.assertQuerysetEqual(Episode.objects.alphabetical(),
            ['<Episode: A cool title>', '<Episode: B is a cool letter>']
        )

    def test_managers_draft_episodes(self):
        """
        Using the draft() manager should return a queryset with only draft
        episodes
        """
        create_episode(title="a published episode", author_name="Alice", status='p')
        create_episode(title="a draft episode", author_name="Bob", status='d')
        self.assertQuerysetEqual(Episode.objects.draft(),
            ["<Episode: a draft episode>"]
        )

    def test_managers_preview_and_published_episode(self):
        """
        Using the preview_and_published() manager should return all episodes with
        status's "preview" and "published".
        """
        create_episode(title="a published episode", author_name="Alice", status='p')
        create_episode(title="a draft episode", author_name="Bob", status='d')
        create_episode(title="a previewed episode", author_name="Carol", status='v')
        create_episode(title="another published episode", author_name="Derek", status='p')
        self.assertQuerysetEqual(Episode.objects.preview_and_published(),
            ["<Episode: a published episode>", "<Episode: a previewed episode>",
            "<Episode: another published episode>"], ordered=False
        )

    def test_managers_preview_and_published_AND_preview_episode(self):
        """
        Using BOTH the preview_and_published() and preview() manager should return all episodes with
        status "published".
        """
        create_episode(title="a published episode", author_name="Alice", status='p')
        create_episode(title="a draft episode", author_name="Bob", status='d')
        create_episode(title="a previewed episode", author_name="Carol", status='v')
        create_episode(title="another published episode", author_name="Derek", status='p')
        self.assertQuerysetEqual(Episode.objects.preview_and_published().published(),
            ["<Episode: a published episode>", "<Episode: another published episode>"], ordered=False
        )

    def test_managers_draft_flashseminar(self):
        """
        Using the draft() manager should return a queryset with only draft flash seminars.
        Also, flash seminars can have the same name as the relevant episode, or can have different names.
        """
        create_flash_seminar(flash_sem_title='a draft flash seminar', episode_title="a draft flash seminar", author_name="Carol", status="d")
        create_flash_seminar(flash_sem_title='a published flash seminar', episode_title="relevant published episode", author_name="Derek", status="p")
        self.assertQuerysetEqual(FlashSeminar.objects.draft(),
            ["<FlashSeminar: a draft flash seminar>"]
        )
        self.assertQuerysetEqual(Episode.objects.draft(),
            ["<Episode: a draft flash seminar>"]
        )

    def test_managers_published_flashseminar(self):
        """
        Using the draft() manager should return a queryset with only draft flash seminars.
        Also, flash seminars can have the same name as the relevant episode, or can have different names.
        """
        create_flash_seminar(flash_sem_title='a draft flash seminar', episode_title="a draft flash seminar", author_name="Carol", status="d")
        create_flash_seminar(flash_sem_title='a published flash seminar', episode_title="relevant published episode", author_name="Derek", status="p")
        create_flash_seminar(flash_sem_title='a previewed flash seminar', episode_title="relevant previewed episode", author_name="Alphone", status="v")
        self.assertQuerysetEqual(FlashSeminar.objects.published(),
            ["<FlashSeminar: a published flash seminar>"]
        )
        self.assertQuerysetEqual(Episode.objects.published(),
            ["<Episode: relevant published episode>"]
        )

    def test_managers_preview_and_published_flashseminar(self):
        """
        Using the preview_and_published() manager should return a queryset with only previewed flash seminars.
        """
        create_flash_seminar(flash_sem_title='a draft flash seminar', episode_title="a draft flash seminar", author_name="Carol", status="d")
        create_flash_seminar(flash_sem_title='a published flash seminar', episode_title="relevant published episode", author_name="Derek", status="p")
        create_flash_seminar(flash_sem_title='a previewed flash seminar', episode_title="relevant previewed episode", author_name="Alphone", status="v")
        self.assertQuerysetEqual(FlashSeminar.objects.preview_and_published(),
            ["<FlashSeminar: a previewed flash seminar>", "<FlashSeminar: a published flash seminar>"], ordered=False
        )
        self.assertQuerysetEqual(Episode.objects.preview_and_published(),
            ["<Episode: relevant previewed episode>", "<Episode: relevant published episode>"], ordered=False
        )
