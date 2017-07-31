from content.models import Episode, Author, FlashSeminar
from django.contrib.auth.models import User

def create_episode(title, author_name, status='p'):
    le_author = Author.objects.create(name=author_name)
    return Episode.objects.create(title=title, author=le_author, status=status, topic_image='a_url')

def create_flash_seminar(flash_sem_title, episode_title, author_name, status='p'):
    create_episode(title=episode_title, author_name=author_name, status=status)
    le_episode = Episode.objects.get(title=episode_title)
    return FlashSeminar.objects.create(title=flash_sem_title, episode=le_episode,status=status)

def create_admin(username, password):
    return User.objects.create_superuser(username, 'test_user@ilovemails.com', password)
