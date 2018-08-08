from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

import random
from .models import Episode, FlashSeminar, Classification, Season
from team.models import TeamMember


def index(request):
    all_episodes = Episode.objects.order_by('-pub_date')

    if request.user.is_staff:
        episode_list = all_episodes.preview_and_published()
    else:
        episode_list = all_episodes.published()

    all_audio = [e for e in episode_list if e.has_audio==True]
    all_video = [e for e in episode_list if e.has_video==True]
    all_classifications = Classification.objects.order_by('discipline')
    random_discipline_1, random_discipline_2 = random.sample(population=list(Classification.objects.all()), k=2)

    # get episode for each discipline. Need to do this so that the 'preview_and_published' and 'published' above apply
    episode_discipline_1 = [e for e in episode_list if random_discipline_1.discipline in [cl.discipline for cl in e.classification.all()]]
    episode_discipline_2 = [e for e in episode_list if random_discipline_2.discipline in [cl.discipline for cl in e.classification.all()]]
    season_list = Season.objects.all()

    return render(request, 'content/index.html',
        {'episode_list': episode_list, 'all_audio': all_audio, 'all_video': all_video,
        'random_discipline_1': random_discipline_1, 'random_discipline_2': random_discipline_2,
        'episode_discipline_1': episode_discipline_1, 'episode_discipline_2': episode_discipline_2,
        'all_classifications': all_classifications, 'season_list': season_list})



def episode_page(request, slug):
    episode = get_object_or_404(Episode, slug=slug)
    all_classifications = Classification.objects.order_by('discipline')

    return render(request, 'content/episode_page.html',
        {'episode': episode, 'all_classifications': all_classifications})


def about_page(request):
    flash_seminar_list = FlashSeminar.objects.published().order_by('event_date')
    all_classifications = Classification.objects.order_by('discipline')
    teammembers = TeamMember.objects.order_by('name')

    return render(request, 'content/about_page.html',
        {'flash_seminar_list': flash_seminar_list, 'teammembers': teammembers,
        'all_classifications': all_classifications})

def discipline_page(request, discipline):
    classification = Classification.objects.get(discipline=discipline)
    all_classifications = Classification.objects.order_by('discipline')
    episode_list = classification.episode_set.all()

    # pagination stuff
    page = request.GET.get('page', 1)
    paginator = Paginator(episode_list, 8)
    try:
        episodes = paginator.page(page)
    except PageNotAnInteger:
        episodes = paginator.page(1)
    except EmptyPage:
        episodes = paginator.page(paginator.num_pages)

    return render(request, 'content/discipline_page.html',
        {'classification': classification, 'all_classifications': all_classifications,
        'episodes': episodes})

def contact(request):
    all_classifications = Classification.objects.order_by('discipline')
    return render(request, 'content/contact.html', {'all_classifications': all_classifications})


def terms(request):
    all_classifications = Classification.objects.order_by('discipline')
    return render(request, 'content/terms.html', {'all_classifications': all_classifications})

def search(request):
    all_classifications = Classification.objects.order_by('discipline')
    episodes = Episode.objects.all()

    query = request.GET.get('q')
    if query:
        results = Episode.objects.filter(Q(title__icontains=query) |
         Q(classification__discipline__icontains=query)) # | Q(classification__academic_field__icontains=query))
    else:
        results = Episode.objects.order_by('-pub_date').published()

    page = request.GET.get('page', 1)
    paginator = Paginator(results, 8)
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    return render(request, 'content/search_results.html', {'all_classifications': all_classifications,
                            'results': results, 'query': query})
