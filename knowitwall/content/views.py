from django.views import generic
from django.shortcuts import render

from .models import Episode, FlashSeminar
from team.models import TeamMember

# this is so that the old KiW URLs still work
old_KiW_urls = [
    'science_of_attraction', 'spanish_forger', 'neurons_move_with_you', 'stem_cell_hotel', 'blast_injury',
    'modify_genome', 'emotional_expression', 'US_constitution',
    'crazy_or_physics', 'migrant_crisis', 'earth_habitable', 'quantum_computers', 'russia_west',
    'string_theory','quantum_life', 'flying_spying', 'sport_society','dante_750',
     'human_language', 'higgs_boson', 'real_shakespeare',
    'neural_cartography', 'saharan_dust', 'viral_pandemics', 'memory_bike',
    'antartica_discovery', 'stegosaurus', 'ganymede', 'tate'
    ]

class IndexView(generic.ListView):
    template_name = 'content/redesign/index.html'

    def get_queryset(self):
        query_episodes = Episode.objects.order_by('-pub_date')
        if self.request.user.is_staff:
            return query_episodes.preview_and_published()#[:13]
        else:
            return query_episodes.published()#[:13]


class AllEpisodesView(generic.ListView):
    template_name = 'content/all_episodes.html'

    def get_queryset(self):
        query_episodes = Episode.objects.alphabetical()
        if self.request.user.is_staff:
            return query_episodes.preview_and_published()
        else:
            return query_episodes.published()

class EpisodePageView(generic.DetailView):
    template_name = 'content/episode_page.html'
    slug_field = 'slug'

    def get_queryset(self, **kwargs):
        slug = self.kwargs['slug']
        if slug in old_KiW_urls:
            self.slug_field = "old_KiW_slug"

        if self.request.user.is_staff:
            return Episode.objects.preview_and_published()
        else:
            return Episode.objects.published()


class AboutView(generic.ListView):
    template_name = 'content/about_page.html'
    object_name = 'flash_seminar_list'
    model = FlashSeminar
    context_object_name = 'flash_seminar_list'

    def get_queryset(self):
        return FlashSeminar.objects.published().order_by('event_date')

def terms(request):
    return render(request, 'content/terms.html')

def team(request):
    teammembers = TeamMember.objects.all()
    return render(request, 'team/teampage.html', {'teammembers': teammembers})
