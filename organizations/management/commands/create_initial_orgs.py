import uuid

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from core.models import EmailVerification
from library.mail.SendgridEmailClient import SendgridEmailClient
from library.mail.VerifyMail import VerifyMail
from organizations.models import OrganizationTag
from organizations.views import create_organization

initial_orgs = [
['Dahir Insaat', 'http://dahirinsaat.com/en/', ['automation']],
['Equilibrium', 'http://equilibrium.org.br/', ['sustainability']],
['EOS Life', 'http://www.eoslife.eu/', ['systems', 'scientific']],
['Holacracy', 'http://holacracy.org/', ['constitutional', 'governance', 'commercial']],
['Humanitad' , 'http://www.humanitad.org/', ['state', 'governance', 'commercial']],
['New Earth Project', 'http://www.newearthnation.org/', ['monetary', 'commercial']],
['One Community Global', 'http://www.onecommunityglobal.org/', ['local', 'sustainability', 'low-tech', 'RBE']],
['Paradism', 'http://www.paradism.org/', ['no-money', 'RBE']],
['Peter Joseph', 'http://peterjoseph.info/', ['no-money', 'media', 'systems', 'scientific', 'open-source', 'RBE']],
['Potentialist Movement', 'http://potentialistmovement.com', ['potentialist']],
['Ubuntu Liberation Movement', 'http://www.ubuntuplanet.org/', ['constitutional', 'charter', 'rights', 'self-governance', 'contributionism']],
['Ubuntu Party', 'http://www.ubuntuparty.org.za/', ['constitutional', 'charter', 'rights', 'self-governance', 'contributionism']],
['Futurist Playground', 'http://futuristplayground.org/', ['community', 'no-money', 'orientation', 'RBE']],
['The Venus Project (TVP)', 'http://thevenusproject.com', ['automation', 'media', 'closed-source', 'RBE']],
['The Zeitgeist Movement (TZM)', 'http://www.thezeitgeistmovement.com/', ['no-money', 'systems', 'scientific', 'open-source', 'RBE']],
['RBE-Network', 'https://rbe-network.org', ['directory, open-source']],
['Auroville', 'http://www.auroville.org/', ['ecovillage', 'low-tech']],

['Cooperative of Catalonia, Spain', 'http://cooperativa.cat/', ['cooperative']],
['Federation of Egalitarian Communities', 'http://www.thefec.org/', ['egalitarian', 'ecovillages']],
['Fellowship for Intentional Communities', 'http://directory.ic.org', ['directory', 'ecovillage', 'religious', 'spiritual']],
['Global Ecovillage', 'http://gen.ecovillage.org/', ['directory', 'ecovillage']],

['Kadagaya, Peru', 'http://www.kadagaya.org/', ['ecovillage']],
['Lammas ecovillage, UK', 'http://lammas.org.uk/', ['ecovillage']],
['Regen Villages', 'http://www.regenvillages.com/', ['ecovillage']],
['Tamera, Portugal', 'http://www.tamera.org/', ['ecovillage']],
['The Telaithrion Project', 'http://en.telaithrion.freeandreal.org', ['ecovillage']],
['Transition Network', 'http://www.transitionnetwork.org/', ['directory', 'ecovillage']],
['Transition Town', 'http://transitiontown.com', ['directory']],

['Copiosis', 'http://www.copiosis.com', ['net-benefit-algorithm', 'closed-source', 'market']],
['The Money Free Party', 'http://moneyfree.party', ['moneyless', 'politics']],

['Money-Free Initiatives', 'https://medium.com/age-of-awareness/money-free-movements-projects-initiatives-b20192683abf#.nsx8wsrom', ['no-money', 'directory']],
['AdBusters', 'http://www.adbusters.org/', ['media']],
['Arlington Institute', 'www.thearlingtoninstitute.com', ['futurist']],
['Bill Plotkin', 'http://www.natureandthehumansoul.com/newbook/aboutBill.htm', ['researcher']],
['BioEcon', 'http://www.bioecon.net/', ['economy', 'ecology', 'oriented']],
['Blue Zones Book', 'http://bluezones.com/', ['community']],
['Blue Zones Project', 'bluezonesproject.com', ['community']],
['C-Realm Podcast', 'http://c-realm.blogspot.com/', ['sustainability']],
['Club Orlov', 'http://cluborlov.blogspot.com', ['sustainability']],
['Center for a Stateless Society', 'http://c4ss.org', ['stateless']],
['City Plan', 'http://www.dahirinsaatmakine.com/city2015/295-3-NH/3d-gorod-295-3-nh/3d-gorod-295-3-nh.html', ['city']],
['Collage Lab', 'http://www.collagelab.org/results/shop/', ['post-capitalism']],
['Collective Evolution (CE)', 'http://www.collective-evolution.com', ['news', 'books', 'documentary']],
['Commons Transition', 'http://commonstransition.org/', ['directory', 'commons', 'sustainability']],
['Community Planet Foundation', 'http://www.communityplanet.org/', ['book', 'community', 'ecology', 'sustainability']],
['Contributive Energy Blog', 'http://contributiveenergy.rocks/', ['no-money']],
['Earth Sphere Development Corporation', 'http://www.earthspheredevelopment.com/', ['no-money']],
['Earth2Hub', 'http://www.earth2hub.com', ['sustainability']],
['Earthship Biotecture', 'http://earthship.com/', ['sustainablility', 'construction']],
['Earth Vote', 'http://http://earthvote.org/', ['sustainability', 'ecology']],
['Electronic Frontier Foundation', 'https://www.eff.org/',['internet', 'freedom']],
['Envienta', 'http://www.envienta.com/', ['sustainability', 'construction']],
['Evolver', 'http://www.evolver.net/', ['media']],
['Except', 'http://www.except.nl/en', ['sustainability']],
['Federico Pistono', ['http://www.federicopistono.org'], ['books']],
['Foster Gamble; Thrive Movement', 'www.thrivemovement.com', ['documentary']],
['FQXi Community', 'http://www.fqxi.org/', ['science', 'edutation']],
['Free World Charter', 'http://www.freeworldcharter.org/en/charter', ['freedom', 'no-money', 'charter']],
['Futuragora', 'http://www.futuragora.pt/', ['no-money']],
['Gar Alperovitz', 'http://www.garalperovitz.com/', ['post-capitalism']],
['Global Futures 2045', 'http://gf2045.com/', ['futurist']],
['HiFreedom', 'http://www.hifreedom.org/#read', ['no-money']],
['Integrative Design Collaborative', 'http://www.integrativedesign.net', ['sustainability', 'book']],
['Lucis Trust', 'http://www.lucistrust.org/en', ['spiritual']],
['Make Magazine', 'http://makezine.com/', ['media']],
['Michael Tellinger', 'http://www.michaeltellinger.com/ubuntu-cont.php', ['open-source']],
['One World Information System', 'http://www.one-world-is.com/rer/owis/owis.htm', ['systems']],
['On The Commons', 'http://www.onthecommons.org/', ['commons']],
['Open Knowledge Foundation', 'http://blog.okfn.org/', ['open-source']],
['P2P Foundation', 'http://p2pfoundation.net/Advanced_Civilisation', ['open-source']],
['Open Agriculture MIT', 'http://openag.media.mit.edu/', ['agriculture']],
['Open Source Ecology', 'opensourceecology.org', ['open-source', 'architecture']],
['Pangea', 'http://www.thepangea.org/', ['no-money']],
['Paul Hawken', 'http://www.paulhawken.com/paulhawken_frameset.html', ['environmentalist']],
['Project Tetra', 'http://www.projecttetra.com/', ['community', 'no-money', 'systems']],
['Project Reason', 'http://www.project-reason.org/', ['scientific', 'thinking']],
['Radical Unschooling', 'http://sandradodd.com/unschooling', ['learning', 'education']],
['Resilience', 'http://www.resilience.org/', ['media']],
['Robin Hahnel', 'http://robinhahnel.com/', ['economist']],
['Root Strikers', 'http://www.rootstrikers.org/#!/', ['media']],
['School Sucks Project', 'http://schoolsucksproject.com/', ['learning', 'education']],
['Sustainable Human', 'http://sustainablehuman.com/', ['no-money', 'sustainability']],
['System Dynamics Society', 'http://www.systemdynamics.org/', ['systems']],
['Technocracy Inc.', 'http://www.technocracyinc.org/', ['systems', 'sustainability', 'automation', 'access']],
['The Archdruid Report', 'http://thearchdruidreport.blogspot.com/', ['collapse']],
['The Emergence Project', 'http://emergenceproject.org', ['no-money']],
['The Moneyless Manifesto', 'http://www.moneylessmanifesto.org/', ['books']],
['The Freedom Line', 'http://www.thefreedomline.com/', ['stateless', 'freedom', 'liberty']],
['The Resonance Project', 'http://resonance.is/', ['science', 'sustainability']],
['The Resource Based Sharing Economy Blog', 'http://www.theresourcebasedeconomy.com/', ['media']],
['The Seasteading Institute', 'http://www.seasteading.org/', ['seasteading']],
['Thrive Movement Solution Hub', 'http://www.thrivemovement.com/solutions-hub', ['sustainability', 'documentary']],
['TROM', 'https://www.tromsite.com/', ['community', 'moneyless', 'systems', 'automation']],
['TZM Education', 'http://tzmeducation.org/', ['no-money', 'systems', 'learning', 'science', 'automation']],
['TZM Forum', 'http://thezeitgeistmovementforum.org/', ['no-money', 'sustainability', 'systems']],
['Russian TVP FB Group', 'https://www.facebook.com/groups/3dcomputer.graphics/', ['no-money']],
['V-radio', 'http://v-radio.org/', ['no-money']],
['WikiHouse', 'http://www.wikihouse.cc/', ['architecture']],
['World Science U', 'http://www.worldscienceu.com/', ['science', 'educatation']],]


class Command(BaseCommand):
    help = "creates the initial set of organizations"

    def handle(self, *args, **options):
        for element in initial_orgs:
            ozt = [OrganizationTag.objects.get_or_create(value=e)[0] for e in element[2]]

            org = create_organization(name=element[0], website_url=element[1])
            org.enabled = True
            for e in ozt:
                org.tags.add(e)

            org.save()


