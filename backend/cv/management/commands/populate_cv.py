"""Populate CV data from Jón Helgi's CV (jhekcv.pdf).

Usage:  python manage.py populate_cv
        python manage.py populate_cv --clear   (wipe and reload)

Idempotent: skips creation if a Person already exists (unless --clear).
"""

from datetime import date

from django.core.management.base import BaseCommand

from cv.models import CVItem, ItemPoint, ItemType, Person, Recommender, Skill


class Command(BaseCommand):
    help = "Populate CV database with structured data from jhekcv.pdf"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete all existing CV data before populating.",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            for model in (ItemPoint, CVItem, Skill, Recommender, Person):
                count = model.objects.count()
                model.objects.all().delete()
                self.stdout.write(f"  Deleted {count} {model.__name__} objects")

        if Person.objects.exists() and not options["clear"]:
            self.stdout.write(self.style.WARNING("CV data already exists. Use --clear to reload."))
            return

        self._create_person()
        self._create_jobs()
        self._create_education()
        self._create_seminars()
        self._create_skills()
        self._create_recommenders()

        self.stdout.write(self.style.SUCCESS("CV data populated successfully."))

    def _create_person(self):
        Person.objects.create(
            name="Jón Helgi Elínar Kjartansson",
            kt="1204903549",
            email="jhek@jhek.is",
            phone="8489903",
            address="Halldóruhagi 10",
            city="Akureyri",
            intro_is=(
                "Ég er tölvunar- og margmiðlunarfræðingur með starfsreynslu bæði úr "
                "störfum tengdum þeirri menntun og annarsstaðar frá. Ég er fljótur að "
                "læra og tileinka mér ný vinnubrögð eða aðferðir, og tel mig vera "
                "samviskusaman starfsmann. Ég á bæði auðvelt og finnst gaman að vinna "
                "í hópi en hef einnig tölverða reynslu af því að þurfa að vinna "
                "sjálfstætt og sýna frumkvæði í starfi. Þá þyki ég þægilegur í "
                "samskiptum og umgengni."
            ),
            intro_en=(
                "I am a computer science and multimedia professional with work experience "
                "in roles both related to my education and beyond. I am a quick learner "
                "who adapts easily to new methods and approaches, and I consider myself "
                "a conscientious worker. I enjoy working in teams but also have "
                "considerable experience working independently and showing initiative. "
                "I am told I am pleasant to work with."
            ),
            hobbies_is=(
                "Hljóðfæraleikur og tónlist almennt. Tölvur og tækni, grafík og "
                "margmiðlun. Björgunarsveitarstörf og önnur útivist og ferðalög. "
                "Ípróttir og þá aðallega handbolti og hestamennska.\n"
                "Virkur útkallsfélagi í Björgunarsveitinni Ársæli og Súlum "
                "Björgunarsveitinni á Akureyri.\n"
                "Seta í stjórn Bjsv. Ársæli 2016-2022, gjaldkeri 2018-2022.\n"
                "Seta í stjórn Súlna, bjsv. 2024-, gjaldkeri 2025-.\n"
                "Önnur lykilhlutverk hjá báðum sveitum ss kerfis- vef- og "
                "samfélagsmiðlaumsjón, kennsla og umsjón nýliðaþjálfunar."
            ),
            hobbies_en=(
                "Music and playing instruments. Computers and technology, graphics "
                "and multimedia. Search and rescue volunteer work, outdoor activities, "
                "and travel. Sports, primarily handball and horseback riding.\n"
                "Active on-call member of Björgunarsveitin Ársæll and Súlur Search "
                "and Rescue in Akureyri.\n"
                "Board member of Bjsv. Ársæll 2016-2022, treasurer 2018-2022.\n"
                "Board member of Súlur SAR 2024-, treasurer 2025-.\n"
                "Other key roles in both teams including system, web, and social media "
                "management, training, and new member onboarding."
            ),
        )
        self.stdout.write("  Created Person")

    def _create_jobs(self):
        jobs = [
            {
                "title_is": "UT þjónusta og forritun",
                "title_en": "IT Services and Development",
                "where_is": "Háskólinn á Akureyri",
                "where_en": "University of Akureyri",
                "start": date(2022, 2, 1),
                "leave": None,
                "points": [
                    (
                        "Forritun, bæði í vefforritun og öðrum tilfallandi verkefnum innanhúss og þá aðallega í Python og Javascript. Í mörgum tilfellum á móti vefþjónustum og gagnagrunum úr ytri kerfum.",
                        "Programming, both web development and other in-house projects, primarily in Python and Javascript. Often integrating with web services and databases from external systems.",
                    ),
                    (
                        "Umsjón og framsetning kerfa og gagna sem þeim tilheyra.",
                        "Management and presentation of systems and their associated data.",
                    ),
                    (
                        "Tækniþjónusta við starfsfólk og nemendur ýmist á þjónustuborði eða í gegnum síma eða Jira beiðnakerfi.",
                        "Technical support for staff and students via service desk, phone, or Jira ticketing system.",
                    ),
                    (
                        "Aðstoð við beinar útsendingar og aðrar tæknilegar útfærslur á viðburðum Háskólans.",
                        "Assistance with live broadcasts and other technical implementations at university events.",
                    ),
                ],
            },
            {
                "title_is": "Innkaup og markaðsmál",
                "title_en": "Procurement and Marketing",
                "where_is": "Háskólinn á Akureyri",
                "where_en": "University of Akureyri",
                "start": date(2019, 8, 1),
                "leave": date(2021, 11, 1),
                "points": [
                    (
                        "Vörustyring, gerð pantana til birgja, yfirferð á birgðahaldi og önnur tilfallandi störf í innkaupadeildinni.",
                        "Product management, purchase orders to suppliers, inventory oversight, and other procurement tasks.",
                    ),
                    (
                        "Umsjón samfélagsmiðla og póstlista, þar með talið samskipti við viðskiptavini, textaskrif og önnur efnisgerð.",
                        "Social media and mailing list management, including customer communication, copywriting, and content creation.",
                    ),
                    (
                        "Val og birting á myndum og myndböndum af vörum á síðu fyrirtækisins og önnur verkefni tengd markaðssetningu.",
                        "Selection and publishing of product photos and videos on the company website and other marketing projects.",
                    ),
                    (
                        "Sala á tölvum og tengdum vörum, tiltekt pantana og önnur störf í verslun.",
                        "Sales of computers and related products, order fulfillment, and other retail tasks.",
                    ),
                ],
            },
            {
                "title_is": "Prentþjónusta",
                "title_en": "Print Services",
                "where_is": "Prenta ehf",
                "where_en": "Prenta ehf",
                "start": date(2018, 5, 1),
                "leave": date(2018, 11, 1),
                "points": [
                    (
                        "Prentun og prenttengd störf þar með talin uppsetning og hönnun á prentverkum.",
                        "Printing and print-related work including layout and design of print materials.",
                    ),
                    (
                        "Afgreiðslustörf og reikningagerð í DK.",
                        "Customer service and invoicing in DK.",
                    ),
                    (
                        "Umsjón með tölvu- og vefmálum þar sem aðal verkefnin voru hugbúnaðar uppfærslur og viðhald með Wordpress vefsíðu auk þess að hefja hönnun og þarfagreiningu á nýrri vefsíðu fyrir fyrirtækið.",
                        "IT and web management, primarily software updates and WordPress site maintenance, plus initiating design and requirements analysis for a new company website.",
                    ),
                ],
            },
            {
                "title_is": "Ferðaundirbúningur",
                "title_en": "Trip Preparation",
                "where_is": "Íslenksir Fjallaleiðsögumenn",
                "where_en": "Icelandic Mountain Guides",
                "start": date(2017, 5, 1),
                "leave": date(2017, 9, 1),
                "points": [
                    (
                        "Pökkun og frágangur á mat og útlegubúnaði fyrir og eftir ferðir hópa. Unnið á 11 klst. vöktum þar sem skipulag þurfti að ganga upp fyrir brottfarir og heimkomu margra ferða á svipuðum eða sama tíma.",
                        "Packing and preparation of food and expedition gear before and after group trips. Worked 11-hour shifts coordinating departures and arrivals of multiple trips simultaneously.",
                    ),
                    (
                        "Utanumhald og innkaup á sjúkrabúnaði fyrir ferðir.",
                        "Management and procurement of medical supplies for trips.",
                    ),
                    (
                        "Umhirða og ósérhæft viðhald á búnaði.",
                        "Care and general maintenance of equipment.",
                    ),
                    (
                        "Önnur tilfallandi verkefni.",
                        "Other ad hoc tasks.",
                    ),
                ],
            },
            {
                "title_is": "Myndbandagerð",
                "title_en": "Video Production",
                "where_is": "Advania",
                "where_en": "Advania",
                "start": date(2015, 11, 1),
                "leave": date(2016, 8, 1),
                "points": [
                    (
                        "Gerð kennslumyndbanda fyrir hugbúnað, ætluð viðskiptavinum, unnin í Articulate Storyline. Vann sem nokkurskonar verktaki innan fyrirtækisins og gerði myndböndum fyrir mismunandi kerfi fyrir mismunandi deildir eftir óskum þeirra.",
                        "Production of instructional software videos for clients, created in Articulate Storyline. Worked as an internal contractor producing videos for different systems and departments on request.",
                    ),
                ],
            },
            {
                "title_is": "Vefforritun",
                "title_en": "Web Development",
                "where_is": "Slökkvilið Höfuðborgarsvæðisins",
                "where_en": "Capital Area Fire Department",
                "start": date(2015, 6, 1),
                "leave": date(2015, 10, 1),
                "points": [
                    (
                        "Forritun á starfsmanna- og gestabókunar vefjum.",
                        "Development of staff and guest booking web applications.",
                    ),
                    (
                        "Unnið í .NET umhverfi þar sem notast var við C# og Javascript.",
                        "Worked in a .NET environment using C# and Javascript.",
                    ),
                    (
                        "Skipulag á þeim SQL töflum sem þurfti í verkefnin sem ekki voru þegar til í grunn.",
                        "Design of SQL tables needed for projects that did not already exist in the database.",
                    ),
                ],
            },
        ]

        for j in jobs:
            points = j.pop("points")
            item = CVItem.objects.create(item_type=ItemType.JOB, **j)
            for text_is, text_en in points:
                ItemPoint.objects.create(item=item, text_is=text_is, text_en=text_en)

        self.stdout.write(f"  Created {len(jobs)} jobs with bullet points")

    def _create_education(self):
        education = [
            {
                "title_is": "Tölvunarfræði BSc",
                "title_en": "Computer Science BSc",
                "where_is": "Háskólinn í Reykjavík",
                "where_en": "Reykjavik University",
                "start": date(2013, 8, 1),
                "leave": date(2020, 2, 1),
                "points": [
                    (
                        "Lokaverkefni unnið í samstarfi við Marel.",
                        "Final project completed in collaboration with Marel.",
                    ),
                ],
            },
            {
                "title_is": "Margmiðlunarfræði Dipl.",
                "title_en": "Multimedia Studies Diploma",
                "where_is": "Margmiðlunarskólinn",
                "where_en": "The Multimedia School",
                "start": date(2011, 8, 1),
                "leave": date(2013, 6, 1),
                "points": [
                    (
                        "Áhersla á vefforritun og grafíska hönnun, en einnig tekin fyrir 3D módeling og kvikun, kvikmyndagerð og eftirvinnska.",
                        "Focus on web development and graphic design, also covering 3D modeling and animation, filmmaking, and post-production.",
                    ),
                    (
                        "Lokaverkefni vefsíða unnin í PHP, Javascript og MySQL.",
                        "Final project website built in PHP, Javascript, and MySQL.",
                    ),
                ],
            },
        ]

        for e in education:
            points = e.pop("points")
            item = CVItem.objects.create(item_type=ItemType.EDUCATION, **e)
            for text_is, text_en in points:
                ItemPoint.objects.create(item=item, text_is=text_is, text_en=text_en)

        self.stdout.write(f"  Created {len(education)} education entries")

    def _create_seminars(self):
        seminars = [
            ("IBM Data Science Professional Certificate", "IBM Data Science Professional Certificate", "IBM/Coursera", "IBM/Coursera", date(2024, 11, 1), None),
            ("Aukin ökuréttindi CD", "Extended Driving License CD", "Ekill ökuskóli", "Ekill Driving School", date(2022, 10, 1), None),
            ("Sigraðu sjálfan þig - Leiðtoganámskeið", "Leadership Course - Conquer Yourself", "Profectus", "Profectus", date(2018, 2, 1), None),
            ("Kennsluréttindi í fyrstu hjálp", "First Aid Instructor Certification", "SL og RKÍ", "SL and ICRC", date(2015, 10, 1), None),
            ("Wilderness First Responder", "Wilderness First Responder", "SL", "SL", date(2015, 3, 1), None),
            ("Smáskiparéttindi", "Small Vessel Certificate", "Tækniskólinn", "Technical College", date(2014, 10, 1), None),
            ("Nýliðaþjálfun björgunarsveitar", "Search and Rescue New Member Training", "Björgunarsveitin Ársæll", "Björgunarsveitin Ársæll", date(2013, 3, 1), None),
            ("Dale Carnegie Næsta kynslóð #07.08", "Dale Carnegie Next Generation #07.08", "Dale Carnegie", "Dale Carnegie", date(2008, 4, 1), None),
            ("Þjálfararéttindi fyrsta stig", "Coaching Certificate Level 1", "ÍSÍ", "National Olympic Committee of Iceland", date(2007, 4, 1), None),
        ]

        for title_is, title_en, where_is, where_en, start, leave in seminars:
            CVItem.objects.create(
                item_type=ItemType.SEMINAR,
                title_is=title_is,
                title_en=title_en,
                where_is=where_is,
                where_en=where_en,
                start=start,
                leave=leave,
            )

        self.stdout.write(f"  Created {len(seminars)} seminars")

    def _create_skills(self):
        skills = [
            # Languages
            ("Íslenska", "Icelandic", 5),
            ("Enska", "English", 4),
            ("Danska", "Danish", 3),
            ("Þýska", "German", 2),
            # Programming
            ("Python", "Python", 4),
            ("Javascript", "Javascript", 4),
            ("HTML", "HTML", 5),
            ("CSS", "CSS", 4),
            ("SQL", "SQL", 3),
            ("C#", "C#", 3),
            ("C++", "C++", 3),
            ("Java", "Java", 3),
            ("PHP", "PHP", 3),
            # Operating systems
            ("Windows", "Windows", 4),
            ("Linux Ubuntu", "Linux Ubuntu", 4),
            ("Mac OS", "Mac OS", 4),
            # Design
            ("Photoshop", "Photoshop", 4),
            ("Illustrator", "Illustrator", 3),
            ("InDesign", "InDesign", 3),
            ("Premiere Pro", "Premiere Pro", 3),
            ("After Effects", "After Effects", 2),
        ]

        for name_is, name_en, level in skills:
            Skill.objects.create(
                skill_name_is=name_is,
                skill_name_en=name_en,
                skill_level=level,
            )

        self.stdout.write(f"  Created {len(skills)} skills")

    def _create_recommenders(self):
        recommenders = [
            {
                "name": "Alex Uni Torfason",
                "title_is": "Innkaupastjóri",
                "title_en": "Procurement Manager",
                "workplace_is": "Tölvutek",
                "workplace_en": "Tölvutek",
                "email": "alex@tolvutek.is",
                "phone": "6160003",
            },
            {
                "name": "Gunnar Ingi Ómarsson",
                "title_is": "Tæknistjóri",
                "title_en": "Technical Director",
                "workplace_is": "Háskólinn á Akureyri",
                "workplace_en": "University of Akureyri",
                "email": "gunnaringi@unak.is",
                "phone": "4608072",
            },
        ]

        for r in recommenders:
            Recommender.objects.create(**r)

        self.stdout.write(f"  Created {len(recommenders)} recommenders")
