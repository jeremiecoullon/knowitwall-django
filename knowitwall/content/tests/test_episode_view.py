from django.test import TestCase
from django.urls import reverse
from .utils import create_episode, create_admin

class EpisodeViewTests(TestCase):

    def test_index_returns_correct_template(self):
        """
        Rendering the homepage should use the correct template
        """
        response = self.client.get(reverse('content:index'))
        self.assertTemplateUsed(response, 'content/index.html')

    def test_index_view_with_no_episodes(self):
        """
        If there are no episodes, you should get no episodes...
        """
        response = self.client.get(reverse('content:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['episode_list'], [])

    def test_index_view_with_a_published_episode(self):
        """
        Published episodes should be displayed on the index page
        """
        create_episode(title="a published episode", author_name="Alice", status='p')
        response = self.client.get(reverse('content:index'))
        self.assertQuerysetEqual(response.context['episode_list'],
            ["<Episode: a published episode>"]
        )

    def test_index_view_with_a_draft_episode(self):
        """
        Drafts shouldn't be displayed on the index page
        """
        create_episode(title="a draft", author_name="Alice", status='d')
        response = self.client.get(reverse('content:index'))
        self.assertQuerysetEqual(response.context['episode_list'], [])

    def test_index_view_with_a_draft_and_published_episode(self):
        """
        If a draft and published episode exist, only the published episode
        shoudl be displayed on the index page.
        """
        create_episode(title="a published episode", author_name="Alice", status='p')
        create_episode(title="a draft episode", author_name="Bob", status='d')
        response = self.client.get(reverse('content:index'))
        self.assertQuerysetEqual(response.context['episode_list'],
            ["<Episode: a published episode>"]
        )

    def test_index_with_two_published_episodes(self):
        """
        If there are 2 published episodes, they should be dislpayed on the index page.
        Note the ordering is in reverse order of publication
        """
        create_episode(title="a first published episode", author_name="Alice", status='p')
        create_episode(title="a second published episode", author_name="Bob", status='p')
        response = self.client.get(reverse('content:index'))
        self.assertQuerysetEqual(response.context['episode_list'],
            ["<Episode: a second published episode>", "<Episode: a first published episode>"]
        )

    def test_index_with_published_and_previewed_episodes_as_staff(self):
        """
        If there is a published and a previewed episodes and user is staff, they should
        both be dislpayed on the index page.
        Need to create a superuser to test this.
        Note the ordering is in reverse order of publication
        """
        create_admin(username="le user", password='hip-ass-password')
        self.client.login(username='le user', password='hip-ass-password')
        create_episode(title="a published episode", author_name="Alice", status='p')
        create_episode(title="a previewed episode", author_name="Bob", status='v')
        response = self.client.get(reverse('content:index'))
        self.assertQuerysetEqual(response.context['episode_list'],
            ["<Episode: a previewed episode>", "<Episode: a published episode>"]
        )

    def test_index_with_published_and_previewed_episodes_not_staff(self):
        """
        If there is a published and a previewed episodes and user is anonymous, on
        the published episode should be viewable.
        Note the ordering is in reverse order of publication
        """
        create_episode(title="a published episode", author_name="Alice", status='p')
        create_episode(title="a previewed episode", author_name="Bob", status='v')
        response = self.client.get(reverse('content:index'))
        self.assertQuerysetEqual(response.context['episode_list'],
            ["<Episode: a published episode>"]
        )
