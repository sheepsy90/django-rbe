import random

from django.contrib.auth.models import User
from django.core.management import BaseCommand

from skills.models import SlugPhrase, UserSkill

sample_skills = [u'computer_science', u'programming', u'microelectronics', u'electronics', u'django', u'python', u'automation', u'biology', u'project', u'swedish', u'svenska', u'v\xe4stervik', u'sm\xe5land', u'c++', u'c', u'software', u'self-engineer', u'business**', u'green-technology', u'robotics', u'computers', u'alternative_health,_agriculture', u'', u'outreach,_transcending_duality,_inclusivism,_ets,_alternative_currencies,_illuminati,_contemporary_shamanism', u'outreach', u'transcending_duality', u'inclusivism', u'ets', u'alternative_currencies', u'contemporary_shamanism', u'spirituality/religion', u'java_machine-learning', u'java', u'machinelearning', u'c+=', u'javascript', u'node.js', u'chemistry', u'mechanical_engineering,_intern,_student,_battery_tech,_electric_vehicles,_automation,_society,_psychology,_rbe,_recycling,_vegetarian,_vegan,_aerospace,_manufacture,_electronics,_travel,_england,_uk,_newcastle,_leeds,', u'engineering', u'mechanical', u'battery_tech', u'electric_vehicles', u'aerospace', u'travel', u'society', u'psychology', u'rbe', u'tvp', u'jaque_fresco', u'industrial_design', u'3d_printing', u'communication', u'intern', u'student', u'england', u'uk', u'newcastle', u'leeds', u'vegetarian', u'vegan', u'agriculture', u'cad', u'transport', u'energy', u'batteries', u'sustainability', u'computer_science_efficient_designs_france_canada_agronomy_self_sustaining_communities_technological_communities', u'efficient_designs', u'france', u'canada', u'agronomy', u'self_sustaining_communities', u'technological_communities', u'food', u'artificial_intelligence', u'solar', u'science', u'philosophy', u'rest', u'openid', u'pedagogy', u'sustainable_building', u'aquaponics', u'urban_farming', u'networks', u'organisation', u'project_organisation', u'economy', u'sketchup', u'construction', u'e-learning', u'organizational_development', u'video_editing', u'audio_editing', u'help_desk_management', u'databases', u'project_management', u'learning_management_systems', u'interest', u'knowledge', u'teaching', u'html', u'css', u'volunteering', u'android', u'linux', u'gaming', u'life', u'enjoying_life', u'coursera', u'it', u'writing', u'government', u'uniting', u'unity', u'patience', u'mutuality', u'truth', u'mathematics', u'vegan,_jacque_fresco,_rbe', u'jacque_fresco', u'web_development', u'dogs', u'behaviorism', u'photography', u'anti-fascism', u'anti-natzi', u'development', u'mindfulness', u'singing', u'music', u'politics', u'freedom', u'japan', u'japanese', u'motorcycle', u'tattoo', u'social_anthropology', u'social_psychology', u'veganisam', u'anti-nuclear', u'veganism', u'v_region', u'chile', u'vi\xf1a_del_mar', u'valparaiso', u'california', u'networking', u'communications', u'quantum_mechanics', u'astrophysics', u'cosmology', u'human_behavioral_studies', u'human_machine_interaction', u'thevenusproject_tvp_rbe_poc_tvpa', u'thevenusproject', u'tvpa', u'poc', u'tvpapoc', u'solidworks', u'manufacturing', u'fabrication', u'welding', u'management', u'socialnetworking', u'resource_based_economy', u'mechanistic_point_of_view', u'positive_change', u'long_term_change', u'scientific_method', u'education', u'transition', u'behavioral_science', u'solutions', u'social_engineer', u'flexitarian', u'the_venus_project', u'tvpa_-_the_venus_project_activism', u'labouring', u'gardening', u'technology', u'rbe_sociology_sustainability_norsk_norge_nord-norge_troms_music_freedom_thevenusproject_labouring_human_behavioral_studies_resource_based_economy_positive_change_solutions', u'sosiologi_samfunnsfag_jacque_fresco_tzm_the_zeitgeist_movement_writing_hip-hop_culture_rap_scientific_method', u'sociology', u'norsk', u'norge', u'norway', u'nord-norge', u'troms', u'sosiologi', u'samfunnsfag', u'tzm', u'the_zeitgeist_movement', u'hip-hop', u'rap', u'hip-hop_culture']


class Command(BaseCommand):
    help = 'Creates some user skills'

    def handle(self, *args, **options):

        for element in sample_skills:
            sp, created = SlugPhrase.objects.get_or_create(value=element)

            for user in User.objects.all():

                if random.random() > 0.5:
                    UserSkill.objects.get_or_create(user=user, slug=sp, level=random.randint(1,6))

