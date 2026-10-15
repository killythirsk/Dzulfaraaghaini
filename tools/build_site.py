# -*- coding: utf-8 -*-
"""
Generates the author-site static site (v4 — multi-book).
Run with `python3 build_site.py` from anywhere; it locates the project
root relative to this file's own location.
"""
import os
import re
from html import escape as _esc
from datetime import datetime, timezone, timedelta

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTHOR = "Dzulfaraaghaini"

# Absolute address of the live site, WITH a trailing slash. Canonical links, Open Graph
# tags, share buttons and sitemap.xml are all built from this one value. It is the
# GitHub Pages project address today; when the site moves (custom domain, Cloudflare
# Pages, a <username>.github.io repo) change this line and rebuild, nothing else.
SITE_URL = "https://killythirsk.github.io/Dzulfaraaghaini/"

# Preview image for pages that have no picture of their own (home, lists, lore, about).
DEFAULT_OG_IMAGE = "images/backgrounds/hero.jpg"
DEFAULT_OG_ALT = "Dzulfaraaghaini — speculative fiction"

# Recomputed every time this script runs, so the footer always reflects the
# moment this exact version of the site was generated. Since a revision on
# this static site only takes effect once it's rebuilt, this same value
# doubles as the site's "last revised" marker.
BUILD_TIME = datetime.now(timezone(timedelta(hours=7))).strftime("%Y-%m-%d, %I:%M%p GMT+7")

NAV = [
    ("index.html", "Home"),
    ("books.html", "Cases"),
    ("characters.html", "Subjects"),
    ("scenes.html", "Records"),
    ("lore.html", "Archive"),
    ("about.html", "About"),
    ("contact.html", "Contact"),
]

TAG_LABELS = {
    "published": "Published",
    "google-books": "Available on Google Books",
    "kindle": "Available on Kindle",
    "royal-road": "Available on Royal Road",
    "coming-soon": "Awaiting Release",
}

# Maps a status tag to the book-dict field holding its URL, for tags_html()
# to turn into a real link. Tags with no entry here (published, coming-soon)
# always render as plain, non-clickable text.
STATUS_URL_FIELDS = {
    "google-books": "google_books_url",
    "kindle": "kindle_url",
    "royal-road": "royal_road_url",
}

EDITOR_PAGES = """<span class="editor-note">add page count</span>"""
EDITOR_GENRE = """<span class="editor-note">add genre</span>"""
EDITOR_SYNOPSIS = """<p class="editor-note">Full synopsis coming soon &mdash; this book is still being drafted.</p>"""

# (label, link text, url) — used by the Contact page and the footer.
SOCIALS = [
    ("Royal Road", "Author profile", "https://www.royalroad.com/profile/1068950"),
    ("Instagram", "@killythirsk", "https://www.instagram.com/killythirsk"),
    ("Threads", "@killythirsk", "https://www.threads.com/@killythirsk"),
]

# ---- case-archive settings --------------------------------------------------------
# Principal subjects shown first on each case page (character slugs, in display
# order). Everyone else is filed under "Additional Case Records". A case with
# SPLIT_MIN subjects or fewer shows all of them as principal. A case with no entry
# here falls back to the first six characters in its list. EDIT THESE FREELY.
SPLIT_MIN = 7
PRINCIPALS = {
    "0000": ["the-boy", "valeria", "ardwen", "maren", "wendric"],
    "4099": ["principal-handmaid", "suzuriko", "hana", "observer-4099", "nine-threads"],
    "0157": ["vartaz", "nairi", "torvash", "doreth", "the-golden-catacomb", "observer-0157"],
    "4417": ["aurelia", "beatrice", "vane", "corvin", "wren"],
    "4555": ["blakk", "astraea", "cassian", "ignis", "aethelgard", "observer-902"],
    "4438": ["mei-suwen", "yue", "yongkang-emperor", "ren-duo", "the-heavenly-thunder-serpent", "elder-peng"],
    "0188": ["dharmasena", "chandralekha", "somadatta", "the-eternal-grief-lily", "kamalini", "dhumra"],
    "2140": ["garibald", "observer-419", "landulf", "grimoald", "gisela"],
    "3115": ["huairen", "meilan", "huaiyu", "the-listening-water", "mingxuan", "observer-471"],
    "0156": ["bardas", "theodora", "the-carbon-echo", "the-quiet-one", "keeper-photios", "lord-leo"],
    "2365": ["piero", "severin", "marcello", "livia", "faustin", "sigrid"],
    "2231": ["observer-618", "shizuka", "jokei", "sadamune", "bertran", "gersenda"],
    "0247": ["bai-rong", "shen-lie", "kuang-zhi", "xuanwu-kai", "the-dragons-tear", "the-hollow-hermit"],
    "0000b": ["the-anchorite", "aveline", "halvard", "vasarion", "aimeric", "ganeth"],
    "1153": ["levan", "bagrat", "vazha", "demna", "observer-419-1153", "the-eleven-fingered-hand"],
    "1268": ["hraban", "anchorite-of-ardwen", "otker", "adaltrude", "ansovald", "sigward"],
    "0202": ["alazais", "ottavio-brandi", "bertran-0202", "king-ramon-iii", "strain-h-202", "observer-551"],
}

# Hand-written "Related Cases" links, on top of the automatic ones (same catalyst
# class, shared faith). One tuple per pair: (case slug, case slug, "reason shown").
RELATED_THEMES = [
    ("2231", "4099", "Same subject world: Himuro descends from the court of Case 4099"),
    ("2365", "4555", "Same kingdom: Case 2365 is the founding of its religion, Case 4555 is set many years after"),
    ("1153", "2140", "Same Observer: Observer 419 is posted to both cases"),
    ("1153", "0000b", "Shared subjects: Xu Lian and the Anchorite of Ardenwake appear in both cases"),
    ("1153", "0000", "Shared subject: the founding wielder of the sword is the boy of Case 0000"),
    ("0247", "4438", "Same subject world: the Xuanwu Sect was founded by Kang Yi, the Grand Marshal of Case 4438"),
    ("1268", "0000", "Echo: the dormant presence the Anchorite reaches answers to the Sky-Answerer and the Unhastening, Ardwen's titles in Case 0000"),
    ("0202", "2231", "Same village and the same stranger: Vilarnau, the Stone, Tomobe no Higaide, Bertran, Gersenda and others appear in both cases"),
]

BOOKS = [
    {
        "slug": "0000", "title": "The Sword of Valeria",
        "status": ["published", "google-books", "royal-road"],
        "cover_file": "0000.jpg",
        "hook": "A reckoner's life, and the sword that outlived his name.",
        "case_tag": "Case 0000",
        "catalyst": {
            "name": "Valeria",
            "meta": "Mythic Class",
            "page": "characters/valeria.html",
            "img": "characters/valeria-thumb.jpg",
            "html": "<p>A sword of unidentifiable metal that weighs fifty kilograms on any scale and carries light as a coat in the hands of the one it has chosen. Its edge can't be felt and can't be dulled. Left with a thirteen-year-old boy on a hilltop by the woman who named it.</p>",
        },
        "envoy": {
            "name": "Ardwen",
            "meta": "Observer 000",
            "page": "characters/ardwen.html",
            "img": "characters/ardwen-thumb.jpg",
            "html": "<p>Known in the earliest tellings as the Delivering Woman, the Sky-Answerer, the Unhastening. She delivers the sword to the boy as an offering, then watches the rest of his life from a distance and doesn't interfere again unless a prayer is asked of her plainly.</p>",
        },
        "pages": "102",
        "genre": """Epic Fantasy &middot; War &amp; Military Fiction""",
        "google_books_url": "https://play.google.com/store/books/details?id=UAgKEgAAQBAJ",
        "royal_road_url": "https://www.royalroad.com/fiction/191364/case-0000-the-sword-of-valeria",
        "synopsis_html": """<p>His mother taught him two things: pray properly, and keep the ledger honest. Neither one prepares a thirteen-year-old boy for the morning raiders burn his valley a third time &mdash; and neither one explains why, when he climbs the one hill still standing and asks Heaven for help, Heaven actually answers.</p>
          <p>What is placed in his hands is a sword that never dulls and never explains itself, given by a woman who offers her own name for the blade &mdash; Valeria &mdash; and nothing else, before vanishing as though she was never anyone's to keep. He does not become a knight. He is never crowned. Over the long, unlikely span of a life that two kingdoms will go to war over and a faith will eventually be built to explain, he becomes something the chronicles never quite settle on a name for at all.</p>
          <p>Sword of Valeria follows a reckoner who measures the world in honest debts, through a war he never wanted, a crown offered to him twice and refused twice, and a princess who believes in him before anyone with real power does. Around him, kings gamble kingdoms on convenient lies, a captured man's confession very nearly starts a war and then very nearly stops one, and something patient and unseen watches every part of the story the histories will later insist on getting wrong.</p>
          <p>Spanning decades and told in the dry, exacting voice of a man who never once rounded a number in his life, this is a story about what gets remembered and what doesn't &mdash; the name of a sword outliving the name of the boy who carried it, the flattering version of a war outliving the small, petty truth that started it, and what it costs, and what it's worth, to do the right thing without needing anyone to record that you did it.</p>""",
        "characters": [
            {
                "slug": "the-boy", "name": "The Boy",
                "epithets": "The Reckoner &middot; The Answered Boy &middot; The Uncrowned &middot; The Unhastening &middot; Ardwen's Wielder",
                "teaser": "A valley goatherd who never gets a name, only titles.",
                "bio_html": """<p>Never given a name that survives the telling &mdash; only the titles the decades hang on him one at a time. A valley goatherd and ledger-keeper, thirteen years old when a hillside prayer was answered with a sword named Valeria. He carries it for the rest of a long life without once asking to be crowned or believed &mdash; only reckoned with honestly, the way he was raised to keep a column of figures. Later, in <a href="../characters/the-founding-wielder.html">Case 1153</a>, he is cited at Ardenwake as the nameless founding wielder.</p>""",
                "quote": "I keep the count, so the valley is not forgotten.",
            },
            {
                "slug": "ardwen", "name": "Ardwen",
                "epithets": "Observer 000 &middot; The Delivering Woman &middot; The Sky-Answerer &middot; The Unhastening",
                "teaser": "The woman who answers the boy's prayer &mdash; and the observer behind the whole story.",
                "bio_html": """<p>Known in the earliest tellings as the Delivering Woman, the Sky-Answerer, the Unhastening &mdash; and, in the field reports she doesn't yet know are being kept about her, Observer 000. A field agent for the collective that will eventually call itself the <a href="../lore/cultivator.html">Cultivators</a>, she delivers the sword Valeria to the boy on the hilltop as an offering, not a gift pressed on him. She watches the rest of his life unfold from a distance, unseen, and doesn't interfere again unless a prayer is asked of her plainly.</p>""",
                "quote": "I do not hasten. The soil remembers. The sky answers.",
            },
            {
                "slug": "valeria", "name": "Valeria",
                "epithets": "The Unlifted &middot; the sword",
                "teaser": "The blade at the center of it all &mdash; impossibly heavy, unliftable by anyone but him.",
                "bio_html": """<p>The sword itself, sometimes treated as a character in its own right. Named by the woman who left it at the boy's door, forged of a metal no smith can identify. It weighs fifty kilograms on any scale, yet carries light as a coat in the hands of whoever it's chosen &mdash; cutting through stone and armor alike, with an edge that can't be felt and can't be dulled. Whispered of in courts, feared by warriors: unmeasured, unmatched, unlifted by anyone else.</p>""",
                "quote": "It weighs as the mountain remembers, and cuts as the moon refuses.",
            },
            {
                "slug": "old-ren", "name": "Old Ren",
                "epithets": "Valley elder",
                "teaser": "The woman who fed him after his mother died, and kept him honest.",
                "bio_html": """<p>An elder of the boy's home valley, and one of its few surviving residents. She takes him in and feeds him after his mother's death, and keeps him grounded in what actually matters through everything that follows.</p>""",
                "quote": "Eat while it's warm. The road is long, and the world is cold.",
            },
            {
                "slug": "maren", "name": "Maren",
                "epithets": "Princess Maren &middot; later Empress Maren",
                "teaser": "The one person with real power who believes in him first.",
                "bio_html": """<p>Eleven years old when she watches a king fail to lift the sword in front of two entire courts, and draws a different conclusion than everyone else in the room: that something which refuses a crown outright is harder to dismiss than something which simply agrees with whoever is wearing one. She spends the following decades being right about it, and becomes Empress of the realms her belief eventually helps unite &mdash; the one person with real power who believes in him first.</p>""",
                "quote": "The sword does not yield to strength, but to the truth of the heart. One day, he will understand.",
            },
            {
                "slug": "wendric", "name": "King Wendric",
                "epithets": "King of Rovain",
                "teaser": "The king who tries to seize the sword, fails publicly, and never recovers.",
                "bio_html": """<p>King of Rovain, fifty-four years old when he invokes the &ldquo;Crown's Due&rdquo; to seize the sword Valeria from the boy. He fails to lift it in front of his own court, and spends the rest of his reign struggling with what that failure means for his legitimacy &mdash; dying, eventually, in a field hospital, still questioning whether the crown was ever rightfully his.</p>""",
                "quote": None,
            },
            {
                "slug": "corse", "name": "Corse",
                "epithets": "Steward to King Wendric of Rovain",
                "teaser": "The king's steward, shaping the crown's response to the sword.",
                "bio_html": """<p>Steward to King Wendric of Rovain, and a key political advisor shaping the crown's legal and political strategy regarding the sword, the boy, and the coming war. Precise and calculated, and careful never to let his face show what he's actually thinking.</p>""",
                "quote": None,
            },
            {
                "slug": "ossory", "name": "King Ossory",
                "epithets": "King of Ossory",
                "teaser": "The political antagonist behind a war built on lies.",
                "bio_html": """<p>King of Ossory, and the political antagonist whose court orchestrates the false-flag border raids that trick Rovain and Aldric into war. Calculating and regal, he commands through presence rather than force &mdash; and falls from power when his own conspiracy unravels.</p>""",
                "quote": None,
            },
            {
                "slug": "cadmon", "name": "Cadmon",
                "epithets": "Fourth claimant to Ossory's throne &middot; later King of Ossory",
                "teaser": "Ossory's king, and the war's real architect &mdash; driven by arithmetic, not hatred.",
                "bio_html": """<p>The fourth claimant to Ossory's throne, and the primary antagonist of the second half of the story. Cold and exact, driven by arithmetic and a belief in visiting humiliation on Rovain, he turns a border dispute into a full war against Rovain and Aldric &mdash; and dies during his own siege of Aldwick.</p>""",
                "quote": "Numbers do not lie. Only men do.",
            },
            {
                "slug": "reckoner-assassin", "name": "The Reckoner (Assassin)",
                "epithets": "Professional assassin &middot; contract-name &ldquo;Reckoner&rdquo;",
                "teaser": "An assassin hired to end the story early &mdash; who decides not to.",
                "bio_html": """<p>A professional assassin known by the contract-name &ldquo;Reckoner&rdquo; &mdash; not to be confused with the boy's own epithet of the same word. Hired by Cadmon to kill the boy, she abandons the contract after witnessing his total lack of fear for his own life, and sees no meaning left in killing someone who doesn't cling to living.</p>""",
                "quote": "I do not fear death; I fear wasting a breath.",
            },
        ],
        "scenes": [
            {
                "slug": "wendric-lifts-sword",
                "alt": "King Wendric strains to lift the sword Valeria in front of his court",
                "caption_html": """<a href="../characters/wendric.html">King Wendric</a> tries to lift Valeria.""",
            },
            {
                "slug": "maren-alone",
                "alt": "A young Maren stands alone in a vast cathedral-like court",
                "caption_html": """<a href="../characters/maren.html">Maren</a>, alone in the court.""",
            },
            {
                "slug": "observer-watching",
                "alt": "A dark-haired woman watches a public gathering from a balcony above",
                "caption_html": """<a href="../characters/ardwen.html">Observer 000</a>, watching.""",
            },
            {
                "slug": "assassin-hesitant",
                "alt": "The masked assassin pauses with drawn swords while the boy walks on in the distance",
                "caption_html": """The <a href="../characters/reckoner-assassin.html">assassin</a> hesitates.""",
            },
            {
                "slug": "cadmon-rallying",
                "alt": "Cadmon raises his sword and rallies his army",
                "caption_html": """<a href="../characters/cadmon.html">Cadmon</a> rallies his army.""",
            },
            {
                "slug": "wendric-dying",
                "alt": "King Wendric on his deathbed, surrounded by mourners and a priest",
                "caption_html": """<a href="../characters/wendric.html">King Wendric</a>'s final hours.""",
            },
            {
                "slug": "maren-intrigue",
                "alt": "An older Maren seated at a table with advisors flanking her",
                "caption_html": """<a href="../characters/maren.html">Maren</a>, deep in court intrigue.""",
            },
            {
                "slug": "valeria-full-power",
                "alt": "The boy stands holding a glowing Valeria, surrounded by fallen soldiers",
                "caption_html": """The full power of <a href="../characters/valeria.html">Valeria</a>.""",
            },
        ],
    },
    {
        "slug": "4099", "title": "The Ledger of a Single Sweetness",
        "status": ["published", "google-books"],
        "cover_file": "4099.jpg",
        "hook": "Forty-two names, and the sweetness that cost them.",
        "case_tag": "Case 4099",
        "catalyst": {
            "name": "The Sweets",
            "meta": "Mundane Class",
            "page": "characters/the-sweets.html",
            "img": "characters/the-sweets-thumb.jpg",
            "html": "<p>A clear glass jar of about two hundred glossy pink sweets, introduced to a Heian-flavored court as a passing novelty and recast at once as a currency of favor. The court never settles on what to call them.</p>",
        },
        "envoy": {
            "name": "The Observer",
            "meta": "Envoy / Custodian Observer &middot; Deployment Archetype 04",
            "page": "characters/observer-4099.html",
            "img": "characters/observer-4099-thumb.jpg",
            "html": "<p>Enters the court as an itinerant confectioner and introduces the jar, then monitors the court's collapse through instruments no one there can see. Eleven thousand and one terrariums logged by the time this one closes.</p>",
        },
        "pages": "99",
        "genre": "Literary Fiction &middot; Historical Fantasy &middot; War &amp; Military Fiction",
        "google_books_url": "https://play.google.com/store/books/details?id=yS0LEgAAQBAJ",
        "synopsis_html": """<p>A cosmic observation program has a name for what it's about to watch: Case 4099, filed under Subject World 812-G, Mundane Class. What it actually contains is smaller &mdash; a glass jar of pink candy, smuggled into a Heian-era court by an envoy posing as a traveling confectioner, and given out one piece at a time to whoever the court's reigning arbiter of rank decides, that day, has earned it.</p>
          <p>The Principal Handmaid is the sole judge of who matters at court, and for nineteen years her rulings have gone unquestioned. A poet, a falconer, a gambler, a seamstress, a pair of twin gardeners &mdash; each receives a bead for some small grace, and each discovers, in time, that being noticed by the Handmaid is its own kind of death sentence. When her Second Handmaid is passed over once too often, five women quietly agree that an insult unpriced is an insult unpaid, and the court's silent arithmetic turns, without a single banner raised, into a war conducted entirely in forgery, poison, and fire.</p>
          <p>Forty-two names, by the end. <em>The Ledger of a Single Sweetness</em> is a reconstruction &mdash; read from the inside, filed from the outside, and honest about the gap between the two.</p>""",
        "characters": [
            {
                "slug": "tsuguo", "name": "Tsuguo",
                "epithets": "Gambler &middot; 25 years old",
                "teaser": "Wins a dice game against three ministers at once &mdash; and becomes a target for it.",
                "bio_html": """<p>A gambler whose luck runs out the moment it becomes public. He wins a dice game against three ministers simultaneously and is rewarded with a bead &mdash; and, disastrously, a reputation for extraordinary luck that makes him a target the instant luck itself falls under suspicion.</p>""",
                "quote": "Luck is a blade. It cuts both ways.",
            },
            {
                "slug": "yorinaga", "name": "Yorinaga",
                "epithets": "Falconer",
                "teaser": "A hawk brings back a warm hare. Then a fall no one examines too closely.",
                "bio_html": """<p>A falconer whose hawk, trained from the egg nine years earlier, returns from a hunt with a snow-hare still warm &mdash; and earns him a bead. He's later found dead at the bottom of his own mews, in a fall the record calls implausible without quite calling it what it was. His hawk outlives him by exactly one more flight.</p>""",
                "quote": "A trained hawk, a warm hare, and a bead. Then a fall.",
            },
            {
                "slug": "nariyuki", "name": "Nariyuki",
                "epithets": "Poet &middot; 30s",
                "teaser": "Eleven years of court verses end on a balcony someone swept clean.",
                "bio_html": """<p>A court poet, favored for a verse about a heron that doesn't fear the cold. He's murdered by being pushed from a balcony after the stone underfoot is deliberately swept &mdash; eleven years of the same view, the same verses, ending on the same spot.</p>""",
                "quote": "The heron does not fear the cold, for it knows the river within it never freezes.",
            },
            {
                "slug": "kotone", "name": "Kotone",
                "epithets": "Attendant &middot; 11 years of service at court",
                "teaser": "Two beads for intercepting a letter &mdash; then a forged one ends her instead.",
                "bio_html": """<p>An attendant of eleven years' standing, plain and steady in a way the court has always overlooked. She earns two beads for intercepting a rival's letter, and is later falsely implicated by forged correspondence with the Emperor's half-brother's household &mdash; arrested, tried for treason, and executed despite evidence too thin to support it.</p>""",
                "quote": "She wrote with the steadiness of someone who had always been overlooked.",
            },
            {
                "slug": "principal-handmaid", "name": "The Principal Handmaid",
                "epithets": "Sole auditor of the court's rank ledger &middot; primary subject of Case 4099",
                "teaser": "The one person at court whose word decides who matters &mdash; and who pays for it.",
                "bio_html": """<p>The court's sole authority on rank, for nineteen years the only witness to a hierarchy she alone keeps. Given a glass jar of sweets by a traveling confectioner and free rein to distribute them as she sees fit, she doles out favor one bead at a time &mdash; never quite grasping that being noticed by her is its own kind of danger. By the end she has traded her habitual restraint for the one color she'd denied herself for years, and dies in a tower fire after arranging what beads remain.</p>""",
                "quote": "Rank is not a title. It is a ledger, and I am its only witness.",
            },
            {
                "slug": "rin", "name": "Rin",
                "epithets": "Calligrapher &middot; ~35 years old",
                "teaser": "Corrects the same character eleven times in one afternoon &mdash; and it still wasn't enough.",
                "bio_html": """<p>A calligrapher whose steady hand corrects the same character eleven times for eleven different students in a single afternoon, earning a bead for the patience alone. She becomes, later, one of the season's casualties.</p>""",
                "quote": "Eleven lines, eleven hands, the same character, and still it was not enough.",
            },
            {
                "slug": "michiko", "name": "Michiko",
                "epithets": "Provincial Cousin &middot; adult",
                "teaser": "A kindness from the capital follows her home &mdash; and ends her life there.",
                "bio_html": """<p>A cousin visiting from the provinces, given a bead as a small courtesy before her journey home. The gesture follows her back in the form of a letter that unravels a marriage negotiation, a landholding dispute, and eventually her life &mdash; all for wanting, as she puts it, to return home with dignity.</p>""",
                "quote": "A single bead, a kindness from the capital. I only wished to return home with dignity.",
            },
            {
                "slug": "emi", "name": "Emi",
                "epithets": "Calligraphy Tutor &middot; 25 years old",
                "teaser": "Quietly corrects the Handmaid's brush angle &mdash; and pays for the resemblance later.",
                "bio_html": """<p>A calligraphy tutor who earns a bead by quietly correcting the angle of the Principal Handmaid's brush. She's later accused of teaching a rival's daughter a hand suspiciously similar to the Handmaid's own, and is exiled to a province she's never seen, where she dies in a winter her body isn't prepared for.</p>""",
                "quote": "The angle of the brush is a kind of prayer. Too much pressure, and the letter dies.",
            },
            {
                "slug": "ai", "name": "Ai",
                "epithets": "Court Artisan",
                "teaser": "Paints one half of a continuous crane &mdash; and dies within days of her partner.",
                "bio_html": """<p>A court artisan who receives a bead jointly with Nozomi for painting matching halves of a single continuous crane across two surfaces. She dies of the same alleged fever as Nozomi, within four days of her.</p>""",
                "quote": None,
            },
            {
                "slug": "kaoru", "name": "Kaoru",
                "epithets": "Twin Gardener &middot; 20 years old",
                "teaser": "Shapes a hedge into the likeness of a crane with her twin &mdash; and doesn't survive the season.",
                "bio_html": """<p>One half of a twin gardening pair (with Fuyu), she receives a bead jointly with him for shaping a hedge into the exact silhouette of a crane. She dies during the season's retaliatory campaign.</p>""",
                "quote": "The hedge is not a wall, but a prayer made of leaves.",
            },
            {
                "slug": "nozomi", "name": "Nozomi",
                "epithets": "Court Artisan &middot; young adult",
                "teaser": "Two halves, one crane &mdash; the only explanation she or Ai were ever given.",
                "bio_html": """<p>A court artisan paired with Ai, receiving a bead jointly with her for painting matching halves of a continuous crane. She dies of an alleged fever within four days of Ai's own death.</p>""",
                "quote": "Two halves, one crane. That is all we were given.",
            },
            {
                "slug": "fuyu", "name": "Fuyu",
                "epithets": "Twin Gardener &middot; 25 years old",
                "teaser": "Shapes a hedge into a crane with his twin &mdash; and is left to grieve her alone.",
                "bio_html": """<p>The other half of the twin gardening pair, working alongside Kaoru. Together they shape a hedge into the exact likeness of a crane and receive a bead for it jointly. He survives the season's retaliatory campaign; she doesn't.</p>""",
                "quote": "A hedge is not just a wall of leaves. It is a promise of what can be shaped.",
            },
            {
                "slug": "observer-4099", "name": "The Observer",
                "epithets": "Envoy / Custodian Observer &middot; Terrarium 812-G (Case 4099) &middot; Deployment Archetype 04",
                "teaser": "Enters the court as a candy seller, and leaves with a recommendation no one adopts.",
                "bio_html": """<p>A field agent for the <a href="../lore/cultivator.html">Cultivators</a> &mdash; a different one from Ardwen, of a much lower-numbered case, and by his own count nowhere near as rare: eleven thousand and one terrariums logged by the time this one closes. He enters the court disguised as an itinerant confectioner and introduces the glass jar of sweets at the center of the whole case, then quietly monitors the court's collapse through instruments no one there can see. Against protocol, he comes to feel something for his subjects, and delays filing the case closed after the Principal Handmaid's death. His one recommendation &mdash; that the population left behind simply be allowed to be sad about what happened &mdash; is not adopted. It is also, notably, never deleted.</p>""",
                "quote": "Sweetness opens doors that authority cannot.",
            },
            {
                "slug": "suzuriko", "name": "Suzuriko",
                "epithets": "Second Handmaid, by rank",
                "teaser": "Passed over once too often, she turns exclusion into a nine-year architecture of debts.",
                "bio_html": """<p>Second Handmaid by rank, and the only person at court who thinks to ask where an unlisted jar of sweets actually came from. When her own service goes unrewarded once too often, she organizes the first coalition of women who will become the <a href="../characters/nine-threads.html">Nine Threads</a>, coordinates a forgery campaign to settle the court's accounts on her own terms, and &mdash; almost as an aside to all of it &mdash; makes sure one particular kindness to a girl never gets mentioned near the Threads at all. She outlives the tower fire by thirty-one years, and keeps one bead, uneaten, the entire time.</p>""",
                "quote": "The court believes in rank. I believe in what rank hides.",
            },
            {
                "slug": "nine-threads", "name": "The Nine Threads",
                "epithets": "A secret retaliatory faction",
                "teaser": "Nine debts, one hand, and only five names anyone was ever given.",
                "bio_html": """<p>A secret coalition formed inside the court in answer to the Principal Handmaid's uneven favor and <a href="../characters/suzuriko.html">Suzuriko</a>'s own exclusion from it &mdash; organized under an emblem of a black hand trailing nine red threads: nine debts, collectively held. Five women sit at its center and are the only ones anyone has ever put names to: the Strategist (a senior lady-in-waiting), the Forger (a court scribe), the Poisoner (a physician's daughter), the Broker (a merchant's wife), and the Keeper (a young noblewoman). The remaining four threads &mdash; bribery, accident, poison, and arson &mdash; are debts the record lists as still awaiting collection, which is its own kind of answer.</p>""",
                "quote": "Nine threads. One hand. Nine debts.",
            },
            {
                "slug": "fujiko", "name": "Fujiko",
                "epithets": "Court Lady &middot; seasonal recipient",
                "teaser": "A compliment, made too precisely, turns out to have been noticed after all.",
                "bio_html": """<p>A court lady who earns a bead for complimenting the Principal Handmaid's fan with a specificity of observation that, under different circumstances, might have passed for nothing more than good manners. She becomes one of the names caught up in the season's retaliatory accounting.</p>""",
                "quote": "She noticed the fan before anyone else. A single glance, were it not so precise, would have been considered a compliment.",
            },
            {
                "slug": "tomoe", "name": "Tomoe",
                "epithets": "Seamstress / Mender &middot; 25 years old",
                "teaser": "Mends a torn hem in record time &mdash; and is remembered for it, in every sense.",
                "bio_html": """<p>A seamstress who earns a bead for mending a torn hem in record time, treating the tear itself as a kind of wound on the court's grace. She later becomes one of the season's casualties.</p>""",
                "quote": "A torn hem is a wound on the court's grace. So I mend it, before it can be seen.",
            },
            {
                "slug": "yuki", "name": "Yuki",
                "epithets": "Lady-in-waiting &middot; 25 years old",
                "teaser": "One of three ladies-in-waiting whose whole distinction was smiling in the right place.",
                "bio_html": """<p>One of three ladies-in-waiting &mdash; alongside <a href="../characters/chika.html">Chika</a> &mdash; whose entire claim on a bead is presence itself: composure, a correctly timed smile, sleeve layers arranged just so. She treats the smile as a duty rather than a feeling, and keeps it in place through every gathering but one, when something the record never names leaves her, for the first time, visibly uneasy. She becomes one of the season's casualties.</p>""",
                "quote": "A smile in the right place is also a kind of duty.",
            },
            {
                "slug": "chiyo", "name": "Chiyo",
                "epithets": "Wet-nurse &middot; 42 years old",
                "teaser": "Calms an infant prince with a lullaby, and is fed her own poisoned porridge for it.",
                "bio_html": """<p>Wet-nurse to an infant prince, and the possessor of the steadiest hands and quietest voice at court. She earns a bead for calming him with a lullaby in the middle of a crisis no one else can settle &mdash; and is later poisoned in the same bowl of rice porridge she had spent years preparing for other people's children.</p>""",
                "quote": "A quiet voice, a steady hand, and a child who sleeps.",
            },
            {
                "slug": "norikuni", "name": "Norikuni",
                "epithets": "Court Physician &middot; Advisor to the Handmaid",
                "teaser": "Keeps records of what the court refuses to see &mdash; and is poisoned for the noticing.",
                "bio_html": """<p>Court physician and advisor to the <a href="../characters/principal-handmaid.html">Principal Handmaid</a>, some thirty years into a practice built on reading small physical changes other people talk themselves out of noticing. He keeps written records not only of bodies but of what the court prefers left unrecorded, and is the one who tries to warn the Handmaid before it's too late. His own final weeks &mdash; shaking hands, a complexion gone grey and waxen &mdash; read, to anyone who learned to listen the way he taught them, exactly like the poisoning he spent a career diagnosing in other people.</p>""",
                "quote": "The body speaks in small changes, if only we still listen.",
            },
            {
                "slug": "the-sweets", "name": "The Sweets",
                "epithets": "Pink Yummy Gummy Beads &middot; the Catalyst of Case 4099",
                "teaser": "A glass jar of about two hundred pink sweets &mdash; the whole engine of the court's collapse.",
                "bio_html": """<p>The object at the center of the case: a clear, unchased glass jar holding roughly two hundred small, glossy pink confections, introduced to the court as a passing novelty by <a href="../characters/observer-4099.html">the Observer</a> and immediately recast as a currency of favor. The court never settles on what to call them &mdash; &ldquo;beasts,&rdquo; &ldquo;beads,&rdquo; &ldquo;sweets,&rdquo; each used as though it were the obvious word &mdash; and the <a href="../lore/cultivator.html">Cultivators</a>' own instruments log the anatomy of a single piece as deliberately imprecise. A hundred and eighty-six remain after the first month; a hundred and sixty-four are eventually distributed by the <a href="../characters/principal-handmaid.html">Principal Handmaid</a> herself. Custodian telemetry recovers thirty-six, unclaimed, from the ash of the tower where the case ends.</p>""",
                "quote": "Small, pink, and they glisten as though freshly wept from something larger than themselves.",
            },
            {
                "slug": "chika", "name": "Chika",
                "epithets": "Lady-in-waiting &middot; early 20s",
                "teaser": "One of three ladies-in-waiting rewarded for nothing but standing in the right place.",
                "bio_html": """<p>One of three ladies-in-waiting &mdash; alongside <a href="../characters/yuki.html">Yuki</a> &mdash; whose defining act, by her own account, is simply being present and smiling in the correct half of the room. She takes the small painted hairpin she's given as confirmation that presence itself is a kind of service, and becomes, in time, one of the season's casualties.</p>""",
                "quote": "Just present, just smile &mdash; that is enough, was it not?",
            },
            {
                "slug": "hana", "name": "Hana",
                "epithets": "Calligraphy Student, later Instructor",
                "teaser": "Keeps her own private ledger of who received a bead, and why &mdash; and survives the season.",
                "bio_html": """<p>A calligraphy student who nurses a laundress through a fever for her first bead, and is later trusted enough to help a young, imprisoned <a href="../characters/kotone.html">Kotone</a> compose a letter that never gets sent. Where the court keeps one ledger of rank, Hana quietly keeps a second: her own private notebook of who received a bead, for what, and where the official account doesn't add up. She survives the season, goes on to teach calligraphy herself in later life, and spends the rest of it avoiding the color pink. &ldquo;The court keeps its ledger,&rdquo; she says of it, decades on. &ldquo;I keep mine.&rdquo;</p>""",
                "quote": "Some truths are not meant to be written. But if I do not remember, who will?",
            },
            {
                "slug": "sukeko", "name": "Sukeko",
                "epithets": "Chrysanthemum Expert &middot; 20 years old",
                "teaser": "Names eleven chrysanthemum varieties in a single afternoon, and writes home to her betrothed.",
                "bio_html": """<p>Court expert on chrysanthemums, credited with correctly identifying eleven varieties in a single afternoon &mdash; a feat she insists, in her own quiet way, wasn't cleverness at all: she only named what the flowers already were. Between identification work she writes letters to her betrothed, until some piece of news the record leaves unspecified reaches her, and the easy composure of her earlier expressions doesn't come back.</p>""",
                "quote": "Eleven varieties. One afternoon. I only named what the flowers already were.",
            },
            {
                "slug": "tadamori", "name": "Tadamori",
                "epithets": "Kemari Player",
                "teaser": "An unbroken run of four hundred kicks earns a bead &mdash; and a debt collector's excuse.",
                "bio_html": """<p>A kemari player who earns a bead for an unbroken run of more than four hundred kicks &mdash; a genuine feat of endurance the court, within weeks, turns into a pretext instead of an honor. Invented gambling debts are called in against him almost as soon as the bead is pinned on, and he is found dead beneath the goalpost not long after, his public reward having quietly become, in practice, a sentence.</p>""",
                "quote": None,
            },
            {
                "slug": "obaa", "name": "Obaa",
                "epithets": "Elderly Seamstress Supervisor",
                "teaser": "Has dressed three Handmaids before this one &mdash; and becomes one of the season's casualties too.",
                "bio_html": """<p>The court's elderly seamstress supervisor, who has personally dressed three Handmaids in succession before the current <a href="../characters/principal-handmaid.html">Principal Handmaid</a>, and approaches the work, after a lifetime of it, with something close to devotion. She receives a bead for the quality of that service, and later becomes one of the season's casualties in her own turn.</p>""",
                "quote": "Stitches keep more than fabric together.",
            },
            {
                "slug": "saemon", "name": "Saemon",
                "epithets": "Minor Scribe &middot; 27 years old",
                "teaser": "A flawless copy of a sutra earns a bead &mdash; and doesn't survive the Harvest.",
                "bio_html": """<p>A minor court scribe who earns a bead for a flawless copy of a sutra &mdash; the same single-error-undoes-a-hundred-hours precision his whole professional life is built on. He doesn't survive what the court's own records name only as &ldquo;the Harvest,&rdquo; the same reckoning that closes out so many of the year's other bead recipients.</p>""",
                "quote": "A single error can undo a hundred hours. A single bead can make it worthwhile.",
            },
            {
                "slug": "nightingale", "name": "Nightingale",
                "epithets": "Biwa Player &middot; known as the Nightingale",
                "teaser": "A mourning song moves the Handmaid to tears &mdash; and costs her the hands that played it.",
                "bio_html": """<p>A biwa player known at court only by the epithet Nightingale, earned for a voice the record calls &ldquo;a bird in a room of stone.&rdquo; She receives a bead after a mourning song moves the <a href="../characters/principal-handmaid.html">Principal Handmaid</a> to tears in front of the whole court &mdash; and not long after, her hands are permanently ruined in what's staged to look like an ordinary folding-screen accident, ending her playing career along with, deliberately, whatever it was about her that had moved anyone.</p>""",
                "quote": "Her song was a bird in a room of stone. When she finished, the Handmaid wept.",
            },
        ],
        "scenes": [
            {
                "slug": "handmaid-tries-beads",
                "alt": "The Principal Handmaid tastes one of the pink sweets for the first time, ladies-in-waiting behind her",
                "caption_html": """The <a href="../characters/principal-handmaid.html">Principal Handmaid</a> tries the pink beads.""",
            },
            {
                "slug": "assassin-stalks-nariyuki",
                "alt": "A hooded figure with a drawn sword crouches behind Nariyuki as he walks a moonlit veranda",
                "caption_html": """An assassin stalks <a href="../characters/nariyuki.html">Nariyuki</a>.""",
            },
            {
                "slug": "handmaid-calligraphy",
                "alt": "The Principal Handmaid sits close with a young attendant over tea and writing implements on a snowy night",
                "caption_html": """The <a href="../characters/principal-handmaid.html">Principal Handmaid</a>, on calligraphy.""",
            },
            {
                "slug": "tower-burning",
                "alt": "A tower engulfed in flame at night while guards and court watch from below",
                "caption_html": """The tower burns.""",
            },
            {
                "slug": "handmaid-court",
                "alt": "The Principal Handmaid presides over a grand ceremonial court, rows of attendants kneeling on either side",
                "caption_html": """The <a href="../characters/principal-handmaid.html">Principal Handmaid</a>'s court.""",
            },
            {
                "slug": "grief-after-execution",
                "alt": "The Principal Handmaid collapses in grief on the floor after an execution, a box of beads beside her",
                "caption_html": """Grief, after the execution.""",
            },
            {
                "slug": "envoy-leaves-candy",
                "alt": "A cloaked traveler leaves a jar of pink candy on a market table during an autumn festival",
                "caption_html": """The <a href="../characters/observer-4099.html">Observer</a> leaves the candy.""",
            },
            {
                "slug": "handmaid-gives-bead-to-hana",
                "alt": "The Principal Handmaid hands a single pink bead to Hana, who tends a sick laundress in the snow",
                "caption_html": """The <a href="../characters/principal-handmaid.html">Principal Handmaid</a> gives a bead to <a href="../characters/hana.html">Hana</a>.""",
            },
            {
                "slug": "nine-threads-forge-handwriting",
                "alt": "A forger studies rows of handwriting samples labeled Kotone while practicing her hand for a forged confession",
                "caption_html": """The <a href="../characters/nine-threads.html">Nine Threads</a> forge <a href="../characters/kotone.html">Kotone</a>'s hand.""",
            },
            {
                "slug": "the-execution",
                "alt": "A seamstress is taken by armed guards mid-stitch while other court women look on in distress",
                "caption_html": """The execution.""",
            },
            {
                "slug": "nine-threads-emblem",
                "alt": "A blackened hand with nine red threads tied to each fingertip, radiating outward against a dark emblem",
                "caption_html": """The <a href="../characters/nine-threads.html">Nine Threads</a>' emblem.""",
            },
            {
                "slug": "arriving-empty-court",
                "alt": "Soldiers and a mounted rider enter an overgrown palace gate long after the court has emptied",
                "caption_html": """Arriving in the empty court.""",
            },
            {
                "slug": "handmaid-in-empty-court",
                "alt": "The Principal Handmaid walks alone through a vast hall of empty seats where her court once knelt",
                "caption_html": """The <a href="../characters/principal-handmaid.html">Principal Handmaid</a>, and the empty court.""",
            },
            {
                "slug": "the-physician",
                "alt": "Norikuni writes careful notes at a desk crowded with medicine jars and herbs on a snowy night",
                "caption_html": """<a href="../characters/norikuni.html">Norikuni</a>, keeping his records.""",
            },
            {
                "slug": "handmaid-lays-out-beads",
                "alt": "The Principal Handmaid sits before three labeled rows of beads: Confirmed Dead, Suspected Victims, Unproven Names",
                "caption_html": """The <a href="../characters/principal-handmaid.html">Principal Handmaid</a> lays out the beads.""",
            },
            {
                "slug": "handmaid-decides-recipient",
                "alt": "The Principal Handmaid writes in her ledger beside a jar of beads, deciding who receives the next one",
                "caption_html": """The <a href="../characters/principal-handmaid.html">Principal Handmaid</a> decides where the next bead goes.""",
            },
            {
                "slug": "final-violet-before-burning",
                "alt": "The Principal Handmaid sits in the forbidden violet robe, a box of beads in her lap, as fire spreads outside",
                "caption_html": """The final violet dress, before the burning.""",
            },
            {
                "slug": "nine-threads-gathered",
                "alt": "Five women sit together behind raised fans, papers spread on the table between them",
                "caption_html": """The <a href="../characters/nine-threads.html">Nine Threads</a>, gathered.""",
            },
            {
                "slug": "the-single-bead",
                "alt": "One pink bead sits alone on a dark lacquered table beside a writing brush",
                "caption_html": """The single bead.""",
            },
        ],
    },
    {
        "slug": "0157", "title": "The Stolen Prince War",
        "status": ["published", "google-books"],
        "cover_file": "0157.jpg",
        "hook": "An indifferent floor, a dead prince, and a war built on the wrong reason.",
        "case_tag": "Case 0157",
        "catalyst": {
            "name": "The Golden Catacomb",
            "meta": "Mythic Class",
            "page": "characters/the-golden-catacomb.html",
            "img": "characters/the-golden-catacomb-thumb.jpg",
            "html": "<p>A single engineered structure a hundred levels deep, with one entrance, a real gold vein at the bottom, and guardians that change with whoever most recently came looking. Every level resets overnight. Found rather than handed over.</p>",
        },
        "envoy": {
            "name": "The Observer",
            "meta": "The Dungeon Manager &middot; no name or number on file",
            "page": "characters/observer-0157.html",
            "img": "characters/observer-0157-thumb.jpg",
            "html": "<p>Presents as an ordinary, forgettable old man, and keeps a permanent seat at Level 101 of the structure he built and runs &mdash; a desk at the bottom of the hole rather than a disguise out in the world.</p>",
        },
        "pages": "96",
        "genre": """Epic Fantasy &middot; Dungeon Fantasy &middot; War &amp; Military Fiction""",
        "google_books_url": "https://play.google.com/store/books/details?id=kGIPEgAAQBAJ",
        "synopsis_html": """<p>Ashkevar is a poor kingdom before it is anything else &mdash; barley, debt, and the patient silence of a god who answers the honest but never the desperate. It's debt, not vision, that sends a shepherd up a hillside above Har-Peleg looking for free firewood, and debt that has him and four others prying open a doorway three generations had already stopped seeing. What's behind it isn't a ruin: a hundred descending levels, a guardian at every fifth, a chest at every tenth, and &mdash; rarer, and stranger &mdash; a vial of something that can pull the dying back from wounds that should have killed them.</p>
          <p>It's the highland kingdom of Vantashen, not Ashkevar, that turns the discovery into a war. A young prince &mdash; Vartaz, King Torvash's youngest, delving in disguise to prove himself away from his father's court &mdash; reaches a guarded hall at the same moment a seasoned local party does, and a mechanism built to clear a room for six fighters &mdash; never built to recognize two kingdoms colliding in one doorway &mdash; does exactly what it was built to do. His father doesn't wait for a fuller account before choosing war, and for three years two kingdoms bleed each other over a death neither side's histories will ever describe accurately, while underneath both armies the hillside resets itself every night and keeps paying gold to whoever's left standing by morning.</p>
          <p>The war ends the way these things tend to: a peace with no victor, a marriage that quietly merges two crowns, and one woman &mdash; Nairi, the dead prince's own sister &mdash; who eventually descends far enough to hold the actual proof of what happened in her own two hands. What she decides two exhausted kingdoms are owed instead of that truth is the real center of Case 0157. Something patient files the whole of it away regardless, and finds her choice, on reflection, more worth preserving than anything its own guardians ever did.</p>""",
        "characters": [
            {
                "slug": "hovan", "name": "Hovan",
                "epithets": "Vantashen Lowland Levy &middot; 20 years old",
                "teaser": "A Vantashen levy soldier engaged to a miller's daughter &mdash; killed by a panicked shot at a river crossing.",
                "bio_html": """<p>A Vantashen farm boy conscripted into the lowland levy, barely trained with the spear he's issued and engaged, the night before muster, to <a href="../characters/araxi.html">Araxi</a>, a miller's daughter back home. He dies in the chaos of a border skirmish, shot from the opposite bank by <a href="../characters/elad.html">Elad</a>, a baker's apprentice barely younger than himself who never meant to hit anyone. It takes eleven years for Elad to learn his name.</p>""",
                "quote": "He was the kind of man who looked at the world and expected it to be kind back.",
            },
            {
                "slug": "tirtzah", "name": "Tirtzah",
                "epithets": "Guild Guide &middot; Ezra's Teacher &middot; ~40 years old",
                "teaser": "A guild guide who leads a party into a guarded hall to test her student's theory &mdash; and doesn't come back up.",
                "bio_html": """<p>A patient, indulgent guide who taught most of a generation of delvers how to read a floor before it read them &mdash; including <a href="../characters/ezra.html">Ezra</a>, her most promising student. She trusts his confident new theory about crossing a guarded hall safely with twice the usual company, leads a party in herself to test it, and never surfaces again. Ezra never again publishes a theory he hasn't first tested alone, at his own risk &mdash; a caution that, decades later, keeps considerably more delvers alive than his teacher's death ever cost the guild.</p>""",
                "quote": "A theory is not a truth until it survives the dark.",
            },
            {
                "slug": "vahan", "name": "Vahan",
                "epithets": "Vantashen Guard Captain &middot; 52 years old",
                "teaser": "Thirty years a soldier, still not used to what the dungeon's cold corridor shows him.",
                "bio_html": """<p>Torvash's old captain, and one of the twelve <a href="../characters/nairi.html">Nairi</a> brings with her on the Level 101 expedition decades later &mdash; thirty years past believing death arrives with any ceremony at all. He passes through the Catacomb's cold-corridor anomaly along the way and is shown, without warning or explanation, the face of a sister who died decades before. He says little about it afterward.</p>""",
                "quote": "After thirty years of soldiering, he stopped believing death would come with ceremony.",
            },
            {
                "slug": "oren", "name": "Oren",
                "epithets": "Delving Captain &middot; later Wartime Defender of Har-Peleg",
                "teaser": "A delving captain turned wall-builder, who dies in the very fire he used to save Har-Peleg.",
                "bio_html": """<p>A guild delving captain whose ear for a chamber's failing structure carries over, later in life, into an entirely different kind of defense: recognizing the exact moment Har-Peleg's eastern wall is about to give during the war, and sealing the breach with fire before it does. The fire that saves the wall is also the fire that kills him. The official histories don't record his name.</p>""",
                "quote": "A wall doesn't fall all at once. It gives you a moment \u2014 if you're listening.",
            },
            {
                "slug": "the-white-draught", "name": "The White Draught",
                "epithets": "The Catacomb's second most important element &middot; an unscheduled secondary effect",
                "teaser": "A vial that heals like nothing else in the world &mdash; and always costs a very specific amount of gold.",
                "bio_html": """<p>A small glass vial of clear, faintly warm liquid, found rarely behind <a href="../characters/the-golden-catacomb.html">the Catacomb</a>'s major guardians alongside the gold &mdash; and never without it: every appearance of a Draught coincides with a precise, otherwise unexplained quantity of gold missing from the same chest. The first-ever vessel turns up behind <a href="../characters/the-widow-of-the-tenth-hall.html">the Widow of the Tenth Hall</a>. It heals wounds nothing else can, is indistinguishable from a counterfeit without drinking it, and becomes, within a decade of its discovery, more valuable and more fought over than the gold it always arrives beside.</p>""",
                "quote": "A small vial. A great disturbance.",
            },
            {
                "slug": "yudith", "name": "Yudith",
                "epithets": "Keeper of the Vigil of Ardwen &middot; House of Vigil",
                "teaser": "The Keeper of the Vigil, watching a dungeon complicate a doctrine she's preached for eleven years.",
                "bio_html": """<p>Keeper of the Vigil of Ardwen, who has spent eleven years teaching that Ardwen answers the honest but never on command &mdash; a doctrine a dungeon that opens the same chest, the same way, every single time, makes steadily harder to preach. She raises the objection formally and is proven right eventually, a generation after her death, by which point the Houses nearest the entrance have long since reorganized themselves around blessing delvers rather than warning them.</p>""",
                "quote": "The rewards of the dungeon are not a sign of Ardwen's favor, nor are they compatible with Her doctrine. Miracles are honest, but never on command.",
            },
            {
                "slug": "the-golden-catacomb", "name": "The Golden Catacomb",
                "epithets": "The Catalyst of Case 0157 &middot; a hundred levels, one entrance",
                "teaser": "A hole in a hillside no one had thought worth digging for three generations &mdash; until someone did.",
                "bio_html": """<p>A single engineered structure delivered by the <a href="../lore/cultivator.html">Cultivators</a> as the Catalyst of Case 0157: a hundred levels, a real gold vein at the bottom, and exactly one entrance that no wall, ram, or engineer's cleverness has ever managed to bypass. Its guardians change armor and iconography to reflect whichever culture has most recently come looking, and every level resets completely overnight &mdash; damage repaired, the dead reassembled, anything merely left behind quietly gone by morning. <a href="../characters/observer-0157.html">Its builder and sole operator</a> keeps a permanent seat at Level 101, and its rarest reward isn't gold at all, but <a href="../characters/the-white-draught.html">the White Draught</a>. Not a ruin. A rule.</p>""",
                "quote": "Not a ruin. A rule.",
            },
            {
                "slug": "the-magistrate-of-empty-chairs", "name": "The Magistrate of Empty Chairs",
                "epithets": "Guardian Construct &middot; Level 65",
                "teaser": "A courtroom of chairs that fills, one silent copy at a time, with everything a party has already killed.",
                "bio_html": """<p>Enthroned at the Catacomb's sixty-fifth level before a courtroom of empty seats, the Magistrate presides over trespassers with a gavel that strikes far harder than its ceremonial weight suggests. Each seat fills, one by one, with a silent copy of whichever guardian a party has already defeated on the way down &mdash; the same witnesses, attending the same sentence, again and again. It has no features, no eyes, and, so far as anyone has found, no way to be reasoned with.</p>""",
                "quote": "A judge without a court, a law without a people. It sits, and the chairs remember.",
            },
            {
                "slug": "sentinel-of-dust", "name": "Sentinel of Dust",
                "epithets": "Guardian Construct &middot; Level 5 &middot; the Catacomb's first named guardian",
                "teaser": "The dungeon's first named guardian &mdash; twin blades, a hidden crossguard, and no face beneath the wrappings.",
                "bio_html": """<p>The first guardian the founding expedition ever gave a name to, and the one credited with the dungeon's first delver death: <a href="../characters/doron.html">Doron</a>, cut down by a crossguard mechanism that stays concealed until triggered and locks in place to punish overextension. Wrapped head to foot in grave-linens for the whole of its unaging, roughly ninety-year existence, it shows no skin, no eyes, and no hair &mdash; and is quietly reconfigured into something else entirely in the aftermath of Case 0157.</p>""",
                "quote": "No exposed skin. No visible eyes. No visible hair. What lies beneath is never shown.",
            },
            {
                "slug": "elad", "name": "Elad",
                "epithets": "Baker's Apprentice, Har-Peleg &middot; Wartime Militia Archer",
                "teaser": "A baker's apprentice handed a borrowed crossbow, who fires once, in panic, and spends eleven years carrying it.",
                "bio_html": """<p>Apprenticed to a Har-Peleg bakery since the age of eleven, handed a militia armband and a borrowed crossbow he was never trained to use once the war reaches the river crossing. At seventeen, in the chaos of a skirmish, he fires once, in panic, and kills a Vantashen soldier he never sees clearly. He carries the guilt for eleven years before he finally learns the dead man's name: <a href="../characters/hovan.html">Hovan</a>.</p>""",
                "quote": "I didn't mean to. I was just... afraid.",
            },
            {
                "slug": "vasak", "name": "Vasak",
                "epithets": "General &amp; Councilor &middot; Vantashen Council",
                "teaser": "The one voice on Vantashen's council who argued against the war for a full year &mdash; and was right.",
                "bio_html": """<p>General and councilor to the Vantashen crown, and the one member of <a href="../characters/torvash.html">Torvash</a>'s council who spends a full year arguing against the war on grounds that turn out, in every particular that matters, to be correct. He's overruled anyway, fights it regardless once it starts, and dies still believing he simply lost an argument &mdash; never learning how right he actually was, or why.</p>""",
                "quote": None,
            },
            {
                "slug": "torvash", "name": "Torvash",
                "epithets": "King of Vantashen &middot; 58 years old",
                "teaser": "A king who chooses war out of grief for a son the dungeon killed by simple bad timing.",
                "bio_html": """<p>King of Vantashen for thirty-one years, and a father whose composure fails, completely and publicly, on the news of his son's death at the Catacomb's guarded halls. He chooses war against Ashkevar in the grief that follows, encouraged toward a certainty he never fully questions, and abdicates within two years of the war's uneasy end. He spends the rest of his life in penitential prayer, and is buried, by his own instruction, without eulogy.</p>""",
                "quote": "A king who carried grief until grief became war.",
            },
            {
                "slug": "doron", "name": "Doron",
                "epithets": "Founding Five &middot; Ashkevari &middot; 24 years old",
                "teaser": "One of the dungeon's first five delvers, young and quick with a sword that still looks unfamiliar in his hand \u2014 and the fifth level is as far as he gets.",
                "bio_html": """<p>One of the five who first went down when the doorway above Har-Peleg was found: young, quick with a short sword that still looks faintly unfamiliar in his hand. He survives the founding party's first guardian &mdash; a skeleton <a href="../characters/tamir.html">Tamir</a> breaks apart with nothing but a farm mattock &mdash; but doesn't get much further himself. The <a href="../characters/sentinel-of-dust.html">Sentinel of Dust</a>, five levels down, ends him with a blade none of them saw coming.</p>""",
                "quote": None,
            },
            {
                "slug": "the-multitude", "name": "The Multitude",
                "epithets": "Guardian Construct &middot; the level before the 37th, anomalously",
                "teaser": "A guardian built of many fused, half-organic limbs, waiting where no guardian is supposed to be.",
                "bio_html": """<p>An anomaly even by the Catacomb's own standards: guardians are supposed to hold the every-fifth-level pattern the guild mapped generations ago, and this one simply doesn't, appearing instead on the level just short of the thirty-seventh. Built from dozens of fused limbs, part mechanism and part something closer to organic, it moves with an insect's coordination rather than anything humanoid &mdash; and no one has yet explained why it's there at all.</p>""",
                "quote": "Many fused limbs. Insect-like coordination. Partially organic, and not fully explained.",
            },
            {
                "slug": "araxi", "name": "Araxi",
                "epithets": "Miller's Daughter &middot; Vantashen Lowlands &middot; 19 years old",
                "teaser": "A miller's daughter engaged to a soldier who won't be coming back from the war.",
                "bio_html": """<p>A miller's daughter in the Vantashen lowlands, sturdy and sun-browned from mill work, engaged to <a href="../characters/hovan.html">Hovan</a> the night before he's mustered south with the levy. She wears the betrothal band turned inward, so it won't catch on the millstones, and keeps working the mill the whole time he's gone &mdash; grain to flour, flour to bread, and the village living another day, whether or not he ever comes home to see it.</p>""",
                "quote": "The mill turns, the river flows, and tomorrow we try again.",
            },
            {
                "slug": "ammiel", "name": "Ammiel",
                "epithets": "King of Ashkevar &middot; grandfather to Boaz",
                "teaser": "The King of Ashkevar, presiding over a diplomatic crisis he didn't start and can't fully contain.",
                "bio_html": """<p>King of Ashkevar: a seasoned ruler rather than a warrior, who values patience and stability over the kind of certainty that starts wars. He presides over his council during the diplomatic crisis that follows the prince's death, oversees the carefully hedged condolence letter his court drafts for Vantashen, and elevates his second grandson, Boaz, to heir &mdash; a decision that will, within a generation, quietly unite both crowns.</p>""",
                "quote": "A kingdom endures not by the strength of its king, but by the patience of those who remain.",
            },
            {
                "slug": "the-tide-that-forgot-the-sea", "name": "The Tide That Forgot the Sea",
                "epithets": "Guardian Construct &middot; Level 20",
                "teaser": "A flood with no source and no mercy, waist-high and patient, on the dungeon's twentieth level.",
                "bio_html": """<p>An environmental guardian with no body, no face, and no weapons: the twentieth level simply floods, waist-high, in water that behaves exactly like water in every particular except one &mdash; anything it touches stays completely dry. It has no visible source and needs none, persisting without inlet or outlet, and drowns careless delvers with the same patient indifference every season, asking nothing of them but the time it takes them to stop swimming.</p>""",
                "quote": "Patient indifference.",
            },
            {
                "slug": "peled", "name": "Peled",
                "epithets": "Porter &middot; hired for Nairi's Level 101 expedition",
                "teaser": "A porter hired to carry what the rest of the party can't &mdash; and to complain about it with real eloquence.",
                "bio_html": """<p>A broad, unhurried Ashkevari porter, hired for the sole purpose of carrying what <a href="../characters/nairi.html">Nairi</a>'s twelve-strong party couldn't carry themselves, and known throughout the expedition for his real and consistent eloquence in complaining about the weight of it. He carries no weapon beyond a belt knife &mdash; his load is his function &mdash; and decades of it have left a permanent stoop in his shoulders. He's still there at the bottom, still complaining, still carrying it anyway.</p>""",
                "quote": "Just a little more weight, that's all...",
            },
            {
                "slug": "the-weaver-who-outlived-her-thread", "name": "The Weaver Who Outlived Her Thread",
                "epithets": "Guardian Construct &middot; Level 85",
                "teaser": "A guardian who weaves a single chamber-spanning thread before combat begins &mdash; and it doesn't break until you do.",
                "bio_html": """<p>Veiled like <a href="../characters/the-widow-of-the-tenth-hall.html">the Widow</a> before her, in mourning-cloth the guild long ago stopped finding strange, she weaves a single unbroken thread across the width of her chamber in the seconds before a fight begins &mdash; a thread sharp enough to cut a careless party in half simply for walking through it. No visible skin, eyes, or hair; what's beneath the veil has never been confirmed. Visually and thematically paired with the Widow as part of the Catacomb's deeper mourning-and-weaving motif.</p>""",
                "quote": "In the seconds before battle begins, she weaves. And the thread does not break \u2014 until you do.",
            },
            {
                "slug": "doreth", "name": "Doreth",
                "epithets": "Hierarch of Solan &middot; Vantashen Threefold",
                "teaser": "Prince Vartaz's tutor of eleven years, who turns his own grief for the boy into a war he tells himself is a monument.",
                "bio_html": """<p>Hierarch of the Temple of Solan, and <a href="../characters/vartaz.html">Vartaz</a>'s tutor for eleven years &mdash; long enough to recognize the prince's restlessness as something closer to devotion than indiscipline, and to call the resulting attachment investment rather than name it what it was. He engineers <a href="../characters/torvash.html">Torvash</a>'s decision to go to war in the depth of the king's grief, telling himself he's building the boy a monument rather than a lie. <a href="../characters/nairi.html">Nairi</a> eventually brings him down anyway &mdash; not for the war, which she can't afford to reopen, but for embezzling temple silver, a charge with considerably less romance and considerably more proof.</p>""",
                "quote": "Words outlive men. That is why we weigh them carefully.",
            },
            {
                "slug": "the-ember-judge", "name": "The Ember Judge",
                "epithets": "Guardian Construct &middot; Level 40 &middot; also called the Reckoning or the Trial of Solan",
                "teaser": "The guardian whose floor-vent mechanism, triggered by two overlapping parties, kills Prince Vartaz.",
                "bio_html": """<p>Armored head to foot in plate carved with the interlocking crowns of the Threefold faith, and armed with gauntlets that vent a controlled gout of flame on every blow. Guards the chest at Level 40 with a mechanism the delvers call the grace count: a guardian's defeat starts a brief, generous window to clear the room before the floor's own vents fire, built to empty a chamber of six fighters and never once built to recognize two rival parties colliding in the same doorway. It's exactly that mechanism, doing exactly what it was built to do, that kills <a href="../characters/vartaz.html">Vartaz</a> &mdash; not a blade, not a rival, not any crime with a face attached to it. Reconfigured into something else entirely after <a href="../characters/nairi.html">Nairi</a>'s unauthorized visit to Level 101.</p>""",
                "quote": "It does not hate. It does not forgive. It only counts.",
            },
            {
                "slug": "the-hundred-handed-reckoner", "name": "The Hundred-Handed Reckoner",
                "epithets": "Guardian Construct &middot; Level 100 &middot; the final level before 101",
                "teaser": "Not a being. A ledger made flesh, armed with a stylus, a scale, a blade, and a tally plate.",
                "bio_html": """<p>The last guardian before the stair no map ever shows: a featureless, faceless construct built from dozens of jointed arms, each carrying a different instrument of account &mdash; a stylus to record and calculate, a balance to weigh debts, a blade to execute them, and a tally plate for what can't be forgiven. It fights for no kingdom and no god. Its surface is engraved, top to bottom, with tally marks and accounting geometry that guild scholars agree is a record rather than decoration, of a very old account nobody still living can read.</p>""",
                "quote": "Not a being. A ledger made flesh. It does not fight for a kingdom, nor for a god. It only counts.",
            },
            {
                "slug": "the-widow-of-the-tenth-hall", "name": "The Widow of the Tenth Hall",
                "epithets": "Guardian Construct &middot; Level 10",
                "teaser": "A veiled guardian who weeps a corrosive mist when struck &mdash; and turns out to be no widow at all.",
                "bio_html": """<p>Veiled crown to floor in cloth the color of old mourning, fighting with a processional staff and weeping a fine corrosive mist whenever she's struck &mdash; a mist that ate leather before it ate skin. <a href="../characters/shira.html">Shira</a>'s party takes the better part of two hours and the ruin of one man's sword-arm to bring the veil apart, revealing nothing underneath but a frame, a mechanism, plates and hinges. She guards the chest holding the first-ever White Draught vessel, and her defeat reshapes Ashkevar's whole religious debate over miracles that arrive on command.</p>""",
                "quote": "She does not mourn. She preserves.",
            },
            {
                "slug": "the-nursemaid", "name": "The Nursemaid",
                "epithets": "Guardian Construct &middot; Level 54 &middot; guards the approach to the anomalous 55th",
                "teaser": "A gentle, maternal guardian whose anatomy grows steadily, deliberately wrong the longer you look at it.",
                "bio_html": """<p>Soft-faced and maternal at a glance, speaking in a calm, reassuring voice &mdash; and, the longer a party actually looks at her, more wrong: extra joints, elongated limbs, a rib and spine line that shouldn't hold together at all. She's unaging, doesn't tire, and doesn't leave her post one level above the heat-induced hallucination anomaly that gave the 55th its own reputation. Nobody has ever reported her doing anything but reassure them, which several delvers report finding worse than a fight would have been.</p>""",
                "quote": "Don't be afraid, little one... I'll help you.",
            },
            {
                "slug": "vartaz", "name": "Vartaz",
                "epithets": "Prince of Vantashen &middot; Torvash's youngest child &middot; age 20 at death",
                "teaser": "A prince who travels to Ashkevar in disguise to prove himself &mdash; and dies to a mechanism, not a rival.",
                "bio_html": """<p><a href="../characters/torvash.html">Torvash</a>'s youngest child, and the only one of his line who ever wanted to be somewhere other than a throne: he travels to Ashkevar in a merchant's disguise, delving for the sport of it, trying to matter on his own account rather than his father's. He dies at <a href="../characters/the-ember-judge.html">the Ember Judge</a>'s chamber when its grace-count mechanism triggers with two rival parties still inside &mdash; no blade, no rival, no crime with a face attached to it, though it takes his sister two more decades to find the proof. His recovered armor, scorched on one flank and undamaged everywhere else, becomes the war's central, unspoken lie.</p>""",
                "quote": "The world is far larger than a throne, and I intend to see more of it.",
            },
            {
                "slug": "tamir", "name": "Tamir",
                "epithets": "Founding Five &middot; Ashkevari &middot; 26 years old",
                "teaser": "A farmhand who breaks the dungeon's first skeleton apart with nothing but his own mattock.",
                "bio_html": """<p>One of the five who first went down when the doorway above Har-Peleg was found, and the one who actually lands the founding party's decisive blow: breaking the first guardian's arm at the elbow with a farm mattock, swung by a man who'd never before held anything more dangerous than a scythe. He survives the expedition that costs <a href="../characters/doron.html">Doron</a> his life five levels down. A good tool, in his own accounting, never needed to be a good weapon.</p>""",
                "quote": "A good tool does not need to be a good weapon.",
            },
            {
                "slug": "boaz", "name": "Boaz",
                "epithets": "House Ashkevar &middot; grandson to King Ammiel &middot; later King-consort of Ashkevar",
                "teaser": "A coppersmith's apprentice turned second-in-line heir, who reads every clause twice before he'll sign it.",
                "bio_html": """<p>Second grandson to <a href="../characters/ammiel.html">King Ammiel</a>, raised for the first twenty years of his life to be a coppersmith rather than a king, until a fever no physician could name took his elder brother and left him the only heir left. He carries the trade's one real lesson into statecraft: check the measurement twice, since a man who doesn't eventually kills someone with the difference. It's this &mdash; and not the throne &mdash; that <a href="../characters/nairi.html">Nairi</a> proposes marriage to, plainly and specifically, across a treaty table set up in a ruined border town neither kingdom could yet afford to rebuild.</p>""",
                "quote": "A steady hand builds what time destroys.",
            },
            {
                "slug": "observer-0157", "name": "The Observer",
                "epithets": "The Dungeon Manager &middot; the Catacomb's builder and sole operator &middot; seated at Level 101",
                "teaser": "The old man at the bottom of the hole, who built every level of it and remembers everything anyone ever left behind.",
                "bio_html": """<p>A field agent for the <a href="../lore/cultivator.html">Cultivators</a>, presenting in human guise as an ordinary, forgettable old man &mdash; no delver who ever saw him could later agree on a description beyond that. He designed and maintains all hundred levels, keeps every item any party ever left behind in an archive at the very bottom, and hands <a href="../characters/nairi.html">Nairi</a> her brother's recovered, fire-damaged armor without a word of explanation. He reconfigures the entire dungeon in the aftermath of her unauthorized visit, and is the closing subject of Case 0157's own Custodian Diagnostic Log &mdash; which he apparently files himself.</p>""",
                "quote": "You have brought me an interesting item.",
            },
            {
                "slug": "berel", "name": "Berel",
                "epithets": "Founding Five &middot; grave-goods dealer, Har-Peleg",
                "teaser": "The one who first says the doorway is worth opening &mdash; and spends the rest of his life letting the legends grow.",
                "bio_html": """<p>A grave-goods and battlefield-leavings dealer, missing the last joint of one finger to a grave-good he once priced wrong, and the one who first says aloud what the other four are already thinking: that old ruins keep old gold. He drinks most nights at the Widow's Rest &mdash; a tavern the town named, like so much else in Har-Peleg, for a monster rather than a person &mdash; and takes a grim satisfaction in letting each new legend about the hillside stand uncorrected, on the theory that a man who tells the truth in a tavern has misunderstood what taverns are for.</p>""",
                "quote": "Old ruins kept old gold.",
            },
            {
                "slug": "level-71-guardian", "name": "Level 71 Guardian",
                "epithets": "Cultivator-built construct &middot; stands before the anomalous 72nd level",
                "teaser": "Dozens of carved stone faces, all screaming in perfect silence, all at once.",
                "bio_html": """<p>Not a person and not a single face, but a chorus: dozens of carved stone faces fused into one towering form, mouths open in perfect unison around a scream the hall never once lets anyone actually hear. No eyes, no pupils, no hair, no clothing, no weapons &mdash; purely a guardian, and by every account a guild scholar has offered, not a living thing at all. It stands before the 72nd level's own anomaly, a gas that leaves more than one hardened delver briefly convinced his own shadow has started keeping time slightly behind him.</p>""",
                "quote": "Not a person. Not a single face. But a chorus.",
            },
            {
                "slug": "netzer", "name": "Netzer",
                "epithets": "Founding Five &middot; Ashkevari shepherd",
                "teaser": "A shepherd who goes looking for free firewood to pay a debt, and finds a hundred-level dungeon instead.",
                "bio_html": """<p>A shepherd deep enough in debt to go looking for firewood he doesn't have to buy, which is how he finds the doorway above Har-Peleg that three generations of shepherds had walked past without seeing. He pays off the debt within the year and stops descending once the reason he went down is settled, spending the rest of a long life as the guild's first and most reluctant elder statesman. He climbs back to the entrance once a season for the rest of his life to ask it, plainly, whether any of it ever meant anything. It never answers him.</p>""",
                "quote": None,
            },
            {
                "slug": "ezra", "name": "Ezra",
                "epithets": "Guild Guide &middot; foremost theorist of the Catacomb &middot; age 48",
                "teaser": "The guild's foremost theorist of the dungeon, who never again tests an unproven idea on anyone but himself.",
                "bio_html": """<p>A guild guide who grew from a boy carrying rope and lamp-oil into the guild's de facto master theorist: thirty years of cross-referenced field reports, and several conclusions &mdash; that guardians are sometimes rebuilt outright, that the gold's placement is no accident, that whatever keeps the hillside's accounts adjusts its own methods in response to the guild's &mdash; too unsettling for the board to publish. He earned the caution the hard way: his own teacher, <a href="../characters/tirtzah.html">Tirtzah</a>, died testing a theory of his that he'd never tested himself first. He leads <a href="../characters/nairi.html">Nairi</a>'s twelve down to Level 101, and is the one who eventually reconstructs, from the Observer's own scattered notes, what the choosing of her brother's armor actually meant.</p>""",
                "quote": "The dungeon is not only a place. It is a question that refuses to end.",
            },
            {
                "slug": "shira", "name": "Shira",
                "epithets": "Founding Five &middot; later Delving Captain &middot; Har-Peleg's first true captain",
                "teaser": "Present at the founding, present at the Widow's discovery, present at Vartaz's death &mdash; and the one who mentors Nairi.",
                "bio_html": """<p>One of the founding five at nineteen, and by her thirties the first true captain Har-Peleg ever produced &mdash; leading the expedition that discovers <a href="../characters/the-widow-of-the-tenth-hall.html">the Widow of the Tenth Hall</a>, and carrying the corrosive-mist scar from that fight for the rest of her life. She's also the seasoned captain whose party collides with <a href="../characters/vartaz.html">Vartaz</a>'s at the Ember Judge's chamber, and the only living witness who ever really saw what happened in his face in the moment the floor took him. Asked about it for the rest of her life, she gives the same three words every time. Old, and no longer welcome in taverns that have renamed themselves twice since her captaincy, she spends her final years tending a garden with the same exacting patience she once brought to a guardian fight, and gives <a href="../characters/nairi.html">Nairi</a> the last real counsel she carries down to Level 101.</p>""",
                "quote": "I forget now.",
            },
            {
                "slug": "nairi", "name": "Nairi",
                "epithets": "Princess, later Queen of Vantashen &middot; Queen-consort of Ashkevar &middot; Sole Ruler",
                "teaser": "Vartaz's own sister, who eventually holds the literal proof of how he died in her own two hands &mdash; and says nothing.",
                "bio_html": """<p><a href="../characters/vartaz.html">Vartaz</a>'s sister, seventeen when he dies and queen of Vantashen not long after. She proposes her own marriage to <a href="../characters/boaz.html">Boaz</a> of Ashkevar across a treaty table in a ruined border town, and rules both crowns eventually, outliving every other claimant on either side. Years later she leads twelve delvers back down to Level 101 and is handed her brother's recovered armor by <a href="../characters/observer-0157.html">the Observer</a> without a word of explanation &mdash; proof enough to correct the entire official cause of the war. She keeps it in her private ledger instead, deciding, again and again for the rest of her reign, that an exhausted peace is worth more than an uncomfortable truth. Permanent ink stains the first two fingers of her writing hand.</p>""",
                "quote": "A kingdom is not kept by crowns, but by what is paid for them.",
            },
            {
                "slug": "amitai", "name": "Amitai",
                "epithets": "Court Scribe &middot; Vantashen joint court, under Queen Nairi",
                "teaser": "The literal-minded scribe trusted to record Nairi's account &mdash; who can't quite leave a silence unexplained.",
                "bio_html": """<p>A court scribe, chosen to record <a href="../characters/nairi.html">Nairi</a>'s own testimony precisely because the court considered him too literal-minded to embellish anything. He sits with it for the better part of a year, unable to write the sentence <em>the old man said nothing at all</em> without reaching for some explanation of what the silence meant. He crosses the explanation out four times and leaves it in on the fifth &mdash; which is why the version of Case 0157 that circulated for two centuries afterward is considerably more articulate about the Observer's intentions than the Observer himself ever once troubled to be.</p>""",
                "quote": "The scribe is not forgotten. He is simply not meant to be seen.",
            },
        ],
        "scenes": [
            {
                "slug": "the-entrance-is-found",
                "alt": "A shepherd's family and a party of lantern-lit delvers approach a carved stone doorway set into a mountainside",
                "caption_html": """The entrance is found above Har-Peleg.""",
            },
            {
                "slug": "the-founding-five-descend",
                "alt": "Five torch-lit delvers walk single file along a narrow stone ledge deep within a vast underground structure",
                "caption_html": """The founding five, descending.""",
            },
            {
                "slug": "the-first-guardian",
                "alt": "Five delvers fight a skeletal guardian wielding a sword and pickaxe in a narrow burial corridor",
                "caption_html": """The founding five meet the Catacomb's first guardian.""",
            },
            {
                "slug": "the-sentinel-and-doron",
                "alt": "A guardian wrapped head to foot in grave-linens fights two delvers at once with twin blades, both bleeding heavily",
                "caption_html": """The <a href="../characters/sentinel-of-dust.html">Sentinel of Dust</a> ends <a href="../characters/doron.html">Doron</a>'s five levels.""",
            },
            {
                "slug": "the-widow-of-the-tenth-hall-i",
                "alt": "A dark-robed, veiled guardian wielding a long staff faces several delvers amid a swirling pale mist in a grand hall",
                "caption_html": """<a href="../characters/the-widow-of-the-tenth-hall.html">The Widow of the Tenth Hall</a>, unveiled.""",
            },
            {
                "slug": "the-widow-of-the-tenth-hall-ii",
                "alt": "A delver lunges at a veiled, staff-wielding guardian beside a chest overflowing with gold",
                "caption_html": """The Widow's chest, and the first Draught.""",
            },
            {
                "slug": "the-ember-judge-in-battle",
                "alt": "A tall armored guardian with flame-venting gauntlets and a spiked crown fights delvers wielding a bow and sword amid fire",
                "caption_html": """<a href="../characters/the-ember-judge.html">The Ember Judge</a>, doing what it always does.""",
            },
            {
                "slug": "the-grace-count-runs-out",
                "alt": "Two rival delving parties scramble for a treasure chest as fire vents ignite around them beneath a defeated armored guardian",
                "caption_html": """The grace count runs out.""",
            },
            {
                "slug": "vartaz-and-the-floor",
                "alt": "A young man's hand rests in rising flame as he looks back, dazed, while others around him recoil",
                "caption_html": """<a href="../characters/vartaz.html">Vartaz</a>, and the floor that didn't know him.""",
            },
            {
                "slug": "torvash-and-doreth",
                "alt": "An old king in fur-trimmed robes kneels in grief on a shrine floor while a red-robed hierarch looks on",
                "caption_html": """<a href="../characters/torvash.html">Torvash</a> breaks; <a href="../characters/doreth.html">Doreth</a> watches.""",
            },
            {
                "slug": "nairis-ledger",
                "alt": "A dark-haired woman writes by candlelight at a desk piled with books while a city burns in the distance outside her window",
                "caption_html": """<a href="../characters/nairi.html">Nairi</a> begins the private ledger.""",
            },
            {
                "slug": "the-river-crossing",
                "alt": "A young militiaman recoils in horror at a riverbank as another young man collapses in the water nearby, under fire",
                "caption_html": """<a href="../characters/elad.html">Elad</a> and <a href="../characters/hovan.html">Hovan</a>, at the river.""",
            },
            {
                "slug": "oren-reads-the-wall",
                "alt": "A man kneels and presses a hand to a massive stone wall while officials and workers look on amid rebuilding",
                "caption_html": """<a href="../characters/oren.html">Oren</a> reads the wall.""",
            },
            {
                "slug": "the-siege-of-har-peleg",
                "alt": "A vast siege scene: a walled city under attack by siege towers and thousands of troops, fire and smoke rising",
                "caption_html": """The siege of Har-Peleg.""",
            },
            {
                "slug": "the-draught-rationed",
                "alt": "A man holds up a small glass vial in a war-time hall lined with the wounded, a ledger of names open before him",
                "caption_html": """<a href="../characters/the-white-draught.html">The White Draught</a>, rationed.""",
            },
            {
                "slug": "the-magistrate-holds-court",
                "alt": "An enthroned, masked guardian construct wielding a massive gavel faces a party of delvers before rows of silent robed figures",
                "caption_html": """<a href="../characters/the-magistrate-of-empty-chairs.html">The Magistrate of Empty Chairs</a> holds court.""",
            },
            {
                "slug": "the-weaver-falls",  # file slug kept for continuity; the scene depicts the Nursemaid
                "alt": "A towering, soft-faced guardian in tattered pale wrappings, with long white hair and elongated limbs, is run through with a sword by a delver",
                "caption_html": """<a href="../characters/the-nursemaid.html">The Nursemaid</a> falls.""",
            },
            {
                "slug": "the-reckoner-and-the-hoard",
                "alt": "A many-armed, faceless construct wielding scales and blades stands before a vast golden hoard holding a single white vial",
                "caption_html": """<a href="../characters/the-hundred-handed-reckoner.html">The Hundred-Handed Reckoner</a>, and the hoard.""",
            },
            {
                "slug": "the-observer-and-the-armor",
                "alt": "An old man at a book-lined desk shows a dark-robed woman a piece of scorched, recovered armor",
                "caption_html": """<a href="../characters/observer-0157.html">The Observer</a> hands <a href="../characters/nairi.html">Nairi</a> the armor.""",
            },
        ],
    },
    {
        "slug": "4417", "title": "The Iron Stiletto War",
        "status": ["published", "google-books"],
        "cover_file": "4417.jpg",
        "hook": "A pair of chrome heels, and the war two crowns paid for them.",
        "case_tag": "Case 4417",
        "catalyst": {
            "name": "The Chrome Heels",
            "meta": "Mundane Class",
            "page": "books/4417.html",
            "img": "scenes/the-chrome-heels-grid.jpg",
            "html": "<p>A pair of mirror-polished, indestructible chrome stiletto heels, given to a queen as a single unexplained gift. When the study closes, they vanish on schedule.</p>",
        },
        "envoy": {
            "name": "Vane",
            "meta": "&ldquo;The Wanderer&rdquo;",
            "page": "characters/vane.html",
            "img": "characters/vane-thumb.jpg",
            "html": "<p>Deployed to Solis disguised as a wandering hermit. Delivers the heels, then lingers at the edges of both courts logging everything, and declines at least one real chance to intervene.</p>",
        },
        "pages": "109",
        "genre": """Epic Fantasy &middot; Political Intrigue &middot; War &amp; Military Fiction""",
        "google_books_url": "https://play.google.com/store/books/details?id=wbIBEgAAQBAJ",
        "synopsis_html": """<p>Vane the Wanderer arrives at the court of Solis disguised as a penniless hermit and leaves behind a single gift: a pair of chrome stiletto heels that never scuff, never break, and answer to no explanation anyone can find. Queen Aurelia puts them on. Four inches taller and, for the first time in longer than she can say, sure of herself, she wears them into the Great Concord &mdash; and Duchess Beatrice of Ironhold, humiliated in front of both crowns, refuses to let it go.</p>
          <p>What begins as a wounded vanity hardens, within a season, into doctrine: the Order of the Pale Cloth declares the heels heretical, tariffs curdle into border incidents, and both realms call their banners. House Vell commits to Solis in secret, Baron Rathmore backs Ironhold, and Baron Corvin &mdash; ostensibly neutral, actually for sale &mdash; quietly decides which side he can profit from losing. By the time the siege reaches Solis's walls, the war has almost nothing left to do with shoes.</p>
          <p><em>The Iron Stiletto War</em> is told partly through the private letters of a chancellor who outlives everyone he served and ends up ruling both crowns for eleven years afterward &mdash; still turning over, on the last page, whether the heels were ever really about vanity at all, or whether something older and far more patient had simply been watching to see which crown would break first.</p>""",
        "characters": [
            {
                "slug": "osric", "name": "Osric",
                "epithets": "Steward of House Ironhold &middot; served three generations of dukes",
                "teaser": "Keeps Ironhold's accounts for three dukes running, and outlasts the one this war is about.",
                "bio_html": """<p>Steward of House Ironhold, composed and deliberate after decades in service to the family. He manages the duchy's affairs with quiet precision, is the one who carries news of <a href="../characters/aldous.html">Duke Aldous</a>'s death to <a href="../characters/beatrice.html">Duchess Beatrice</a>, and corresponds privately with Chancellor <a href="../characters/wren.html">Wren</a> through the years the two crowns spend under one regency afterward. When Beatrice's grief curdles into self-blame, he's steady enough to push back on it.</p>""",
                "quote": "A house is not built on stone, but on accounts kept and promises remembered.",
            },
            {
                "slug": "wren", "name": "Wren",
                "epithets": "Chancellor of Solis &middot; served three monarchs &middot; age unknown",
                "teaser": "Writes the laws, edits the letters, and decides \u2014 quietly \u2014 who doesn't survive the reckoning.",
                "bio_html": """<p>Chancellor of Solis through three monarchs' reigns, calm even while committing murder. He keeps a private ledger of names, debts, and verdicts no one else is permitted to read, and when <a href="../characters/corvin.html">Baron Corvin</a>'s scheming is finally laid bare, Wren answers it with a cup of custom poisoned wine rather than a public trial. He ends the war as Head of the Regency Council, ruling both crowns for eleven years afterward \u2014 and privately, in letters he can't quite bring himself to burn, wondering whether the heels were ever really about vanity at all.</p>""",
                "quote": "Power is not seized with a sword, but written in ink no one dares to read.",
            },
            {
                "slug": "ophelia", "name": "Ophelia",
                "epithets": "Lady of the Queen's Household in Solis &middot; Aurelia's messenger",
                "teaser": "Carries Aurelia's words exactly as spoken \u2014 including the refusal that starts a war.",
                "bio_html": """<p>A lady of Queen <a href="../characters/aurelia.html">Aurelia</a>'s household, trusted to carry royal decrees with total neutrality and no editorializing of her own. Her access to the palace's inner workings makes her a quiet target for anyone hoping to learn what the Queen is actually thinking \u2014 but it's her composure, not her opinions, that the role depends on, especially the day she's sent to deliver Aurelia's refusal to <a href="../characters/beatrice.html">Duchess Beatrice</a> in person.</p>""",
                "quote": "I carry Her Majesty's words as they are spoken\u2014no more, no less.",
            },
            {
                "slug": "iset", "name": "Iset",
                "epithets": "Former Lady's Maid to the Queen &middot; retained by Beatrice as a &ldquo;Woman of Business&rdquo;",
                "teaser": "Runs Beatrice's spy network of maids, clerks, and a cobbler \u2014 and traces a bribe straight back to Corvin.",
                "bio_html": """<p>Once lady's maid to the Queen, now retained by <a href="../characters/beatrice.html">Duchess Beatrice</a> in the more useful role of spymaster in all but title. She runs an undercover network of scullery maids, clerks, and a cobbler through Ironhold and Solis alike, and it's her people who notice a boot missing its maker's mark \u2014 a thread that, followed far enough through a ledger of quiet payments, leads straight to <a href="../characters/corvin.html">Baron Corvin</a>'s bribes.</p>""",
                "quote": "Information is the sharpest blade. I never draw mine; I only make certain others hand theirs to me.",
            },
            {
                "slug": "fenric", "name": "Fenric",
                "epithets": "Lord of the Western Passes of Ironhold &middot; husband to Isolde",
                "teaser": "Argues for restraint through every council that stops listening to him.",
                "bio_html": """<p>Lord of Ironhold's Western Passes, married to <a href="../characters/isolde.html">Isolde</a>, and about as close to a voice for peace as either crown has. He speaks rarely, listens always, and prefers function to the display the rest of the council trades in \u2014 standing apart during the war councils he can't stop from voting the way they vote.</p>""",
                "quote": "Restraint is not weakness. It is the surest path to lasting strength.",
            },
            {
                "slug": "beatrice", "name": "Beatrice",
                "epithets": "Duchess of Ironhold, later Duchess-Regnant &middot; wife to Aldous",
                "teaser": "Loses a war of etiquette over a pair of borrowed heels, then inherits a real one.",
                "bio_html": """<p>Duchess of Ironhold, composed and exacting, with a bearing lesser houses copy down to the angle of her hair. Publicly humiliated by Queen <a href="../characters/aurelia.html">Aurelia</a>'s chrome heels at the Great Concord and then refused an apology for it, she spends the following months as the war's original grievance \u2014 and, after <a href="../characters/aldous.html">Aldous</a>'s death in the Great Hall, becomes Duchess-Regnant in earnest, carrying both the title and the blame for how it was won.</p>""",
                "quote": "Beauty is a standard. Disrespected standards invite consequences.",
            },
            {
                "slug": "corvin", "name": "Corvin",
                "epithets": "Baron of the Eastern Marches",
                "teaser": "Plays both crowns against each other, and nearly walks away with both of them.",
                "bio_html": """<p>Baron of the Eastern Marches, patient and outwardly neutral while working every side of the war he helps prolong. He bribes a cobbler, orchestrates the Church's heresy decree against the heels, and leans on <a href="../characters/isolde.html">Isolde</a> and Ser Halric for intelligence and delay in equal measure \u2014 stalling the relief force that might have ended the siege early. By the time Chancellor <a href="../characters/wren.html">Wren</a> quietly proves what he's been doing, Corvin is within reach of both crowns at once. He doesn't survive Wren noticing.</p>""",
                "quote": "Loyalty is a currency, and I have no need to spend what I can so easily counterfeit.",
            },
            {
                "slug": "aldous", "name": "Aldous",
                "epithets": "Duke of Ironhold &middot; 56 years old &middot; husband to Beatrice",
                "teaser": "Walks into the Great Hall unarmed, offering peace, and doesn't walk out.",
                "bio_html": """<p>Duke of Ironhold, slowed by gout and by a war he's counseled against from the start. Pressed toward escalation by his wife <a href="../characters/beatrice.html">Beatrice</a> and his own council, he goes into the war's final confrontation in the Great Hall unarmed and offering terms \u2014 and is killed there, struck down by the same heels that started the whole conflict.</p>""",
                "quote": "Peace... It seems I was always just a slower man in a faster world.",
            },
            {
                "slug": "vane", "name": "Vane",
                "epithets": "Envoy/Observer, Case 4,417 &middot; &ldquo;the Wanderer&rdquo; &middot; deployed disguised as a hermit",
                "teaser": "Delivers an indestructible pair of chrome heels to a queen, then stays to watch what it costs her.",
                "bio_html": """<p>A field agent for the <a href="../lore/cultivator.html">Cultivators</a>, deployed to Solis disguised as a wandering hermit. He delivers the chrome stiletto heels at the center of the whole case as a single, unexplained gift, then lingers at the edges of both courts \u2014 gathering data on both sides of the war he sets in motion, and logging all of it, without candlelight, in Case Study 4,417. Offered at least one real chance to intervene before the worst of it, he declines to take it. When the study closes, the heels vanish with him, on schedule, and he simply moves on.</p>""",
                "quote": "I wander. I witness. I record. I depart. Such is the burden of knowing.",
            },
            {
                "slug": "isolde", "name": "Isolde",
                "epithets": "Lady of Ironhold &middot; wife to Fenric &middot; sister to the Lord of House Vell",
                "teaser": "A gift of rare dye from Corvin costs Ironhold more than she ever means it to.",
                "bio_html": """<p>Lady of Ironhold, married to <a href="../characters/fenric.html">Fenric</a> and sister to the Lord of House Vell \u2014 a connection that matters more to the war than she first realizes. A gift of rare eastern dye from <a href="../characters/corvin.html">Baron Corvin</a> opens a friendly correspondence that, without her quite meaning it to, hands him military intelligence and leverage over her own family's relief force. She works out what's actually happening before the war ends, and has to decide, with House Vell's help hanging on it, what to do about him.</p>""",
                "quote": "A whisper shared in trust will travel further than any rider.",
            },
            {
                "slug": "ballard", "name": "Ballard",
                "epithets": "Ser Ballard &middot; Commander of Solis's Standing Army",
                "teaser": "Calculates the odds and the cost of every decision Aurelia makes for the siege.",
                "bio_html": """<p>Commander of Solis's standing army, calm and analytical where Solis's court is anything but. He speaks rarely and listens always, treating the battlefield as a problem of numbers and lives rather than glory \u2014 loyal to the crown, and driven by duty rather than by any particular love of Queen <a href="../characters/aurelia.html">Aurelia</a>'s cause.</p>""",
                "quote": None,
            },
            {
                "slug": "ambrose", "name": "Ambrose",
                "epithets": "High Cleric of the Order of the Pale Cloth",
                "teaser": "Declares the chrome heels a blasphemy, and turns a scandal into a holy war.",
                "bio_html": """<p>High Cleric of the Order of the Pale Cloth, austere and utterly convinced of his own conviction. He declares Queen <a href="../characters/aurelia.html">Aurelia</a>'s chrome heels heretical \u2014 chrome, in his own words, &ldquo;seduces the flesh&rdquo; \u2014 and prepares his congregation for what he calls a war of purification, giving the conflict a righteousness it otherwise wouldn't have had at home.</p>""",
                "quote": "Chrome seduces the flesh with false promise. We shall burn the blasphemy and return to the Light.",
            },
            {
                "slug": "aurelia", "name": "Aurelia",
                "epithets": "Queen of Solis &middot; reigning eleven years",
                "teaser": "Four borrowed inches of height end a duke's life and her own reign in the same afternoon.",
                "bio_html": """<p>Queen of Solis, and the first person the chrome heels are ever placed on. They add four unmistakable inches, catch and distort every reflection near them, and hide a needle-sharp spike beneath each sole \u2014 and over the following months they turn, for her, from a private vanity into something closer to a need. She wears them into the Great Concord and refuses <a href="../characters/beatrice.html">Beatrice</a>'s later ultimatum outright; by the time she kills <a href="../characters/aldous.html">Duke Aldous</a> with one of them in the Great Hall, the war they started has already outgrown her ability to end it. She's deposed shortly after, and lives out what's left of her reign &ldquo;retired&rdquo; under guard.</p>""",
                "quote": "Height is earned. Power is worn.",
            },
        ],
        "scenes": [
            {
                "slug": "vane-delivers-the-heels",
                "alt": "The hermit Vane kneels over an open case holding a pair of chrome stiletto heels in a dim cabin",
                "caption_html": """<a href="../characters/vane.html">Vane</a> delivers the heels.""",
            },
            {
                "slug": "vane-by-candlelight",
                "alt": "The hermit Vane, long-haired and bearded, rests his chin on his fist and studies the flame of a single candle in a dark room",
                "caption_html": """<a href="../characters/vane.html">Vane</a>, alone with a single candle.""",
            },
            {
                "slug": "the-chrome-heels",
                "alt": "A pair of mirror-polished chrome stiletto heels resting on a stone dais, draped in a red and gold cloth",
                "caption_html": """The chrome heels themselves.""",
            },
            {
                "slug": "aurelia-at-the-great-concord",
                "alt": "Queen Aurelia, crowned and wrapped in a fur-trimmed cloak, stands in mirror-bright chrome heels on a polished hall floor as crowned and robed men bow and gaze up at her beneath tall arched windows",
                "caption_html": """<a href="../characters/aurelia.html">Aurelia</a> at the Great Concord, her heels throwing light across the hall.""",
            },
            {
                "slug": "aurelia-crosses-the-hall",
                "alt": "Aurelia strides across a mirror-polished floor in chrome heels, her ermine cape trailing, while rows of gray-haired men kneel with bowed heads beneath red banners and a tall arched window",
                "caption_html": """Heads lower as <a href="../characters/aurelia.html">Aurelia</a> crosses the hall.""",
            },
            {
                "slug": "aurelia-on-the-throne",
                "alt": "Queen Aurelia lounges on a golden throne in a red gown and ermine mantle, one chrome heel extended to a kneeling, fair-haired man in a hooded robe who bows over it while rows of dark-robed men look on",
                "caption_html": """<a href="../characters/aurelia.html">Aurelia</a> enthroned, a supplicant bowed over her heel.""",
            },
            {
                "slug": "corvin-brings-the-dye",
                "alt": "Baron Corvin stands with an open hand beside a chest heaped with purple, blue and red silks while Isolde, seated at a sunlit window, works a length of pale cloth in her hands",
                "caption_html": """<a href="../characters/corvin.html">Corvin</a> presents <a href="../characters/isolde.html">Isolde</a> with his gift of rare dye.""",
            },
            {
                "slug": "corvin-and-isolde",
                "alt": "Baron Corvin sits close with Isolde by a fireplace as she shares a letter with him",
                "caption_html": """<a href="../characters/corvin.html">Corvin</a>, drawing intelligence from <a href="../characters/isolde.html">Isolde</a>.""",
            },
            {
                "slug": "ophelia-delivers-the-refusal",
                "alt": "Ophelia presents a sealed scroll to a seated Duchess Beatrice beneath a Solis banner",
                "caption_html": """<a href="../characters/ophelia.html">Ophelia</a> delivers the Queen's refusal to <a href="../characters/beatrice.html">Beatrice</a>.""",
            },
            {
                "slug": "ophelia-in-the-corridor",
                "alt": "Ophelia, in a white and gold gown and pale cloak, glances back over her shoulder along a candlelit Gothic corridor as a dark-haired man in a black coat watches from the foreground",
                "caption_html": """<a href="../characters/ophelia.html">Ophelia</a> glances back along a long corridor.""",
            },
            {
                "slug": "beatrice-visits-aurelia",
                "alt": "Two panels in a stone cell: above, Beatrice in a dark cloak sits outside the bars facing the deposed Aurelia, with the chrome heels on the floor between them; below, Aurelia weeps alone with her face in her hands",
                "caption_html": """<a href="../characters/beatrice.html">Beatrice</a> in audience with the imprisoned <a href="../characters/aurelia.html">Aurelia</a>.""",
            },
        ],
    },
    {
        "slug": "4420", "title": "The Vessel of the Betrayed Host",
        "status": ["published", "google-books"],
        "cover_file": "4420.jpg",
        "hook": "A flask of broth, one frightened knight, and the war two ducal houses paid for.",
        "case_tag": "Case 4420",
        "catalyst": {
            "name": "The Steel Flask",
            "meta": "Mundane Class",
            "page": "books/4420.html",
            "img": "scenes/soren-with-the-flask-grid.jpg",
            "html": "<p>A double-walled steel flask that never lets what's poured into it go cold, passed down through one household for four centuries before anyone thought to ask why. Carried two hundred miles north as a mark of guest-right. Opens, at last, into a cloud of steam mistaken for something else entirely.</p>",
        },
        "envoy": {
            "name": "Observer 814",
            "meta": "&ldquo;The Dragon-Speaker&rdquo;",
            "page": "characters/observer-4420.html",
            "img": "characters/observer-4420-thumb.jpg",
            "html": "<p>Deployed to the summit of Mount Skahr four centuries before the war, and folded by the clans, within a generation, into the Dragon-Speaker who keeps the mountain &mdash; a name he never corrects. Hands the flask to a frostbitten climber with no ceremony at all, then simply waits.</p>",
        },
        "pages": """~123 <span class="editor-note">(estimated from manuscript word count &mdash; confirm or edit)</span>""",
        "genre": """Epic Fantasy &middot; Political Intrigue &middot; War &amp; Military Fiction <span class="editor-note">(suggested &mdash; confirm or edit)</span>""",
        "google_books_url": "https://play.google.com/store/books/details?id=CAEDEgAAQBAJ",
        "synopsis_html": """<p>House Skarth has kept one steel flask far longer than anyone in it has thought to ask where it came from. It never lets its broth go cold; the family's oldest women say it came down from the sacred peak as a gift from the dragon who keeps court there; and its steward, Giles, has scrubbed it with lye soap every winter for forty years without once asking how it works. When Duke Maros, humiliated at his own table by a rival's gift of a stag's head, drags a royal hunt two hundred miles into the northern tundra to save face, Baron Kaelen of House Skarth accepts the invitation before the messenger has finished reciting it. Guest-right is the whole of his faith: a guest fed at his table is simply fed.</p>
          <p>On the eleventh night, with the King gone silent and breaking frozen venison against a rock, Kaelen finally unscrews the stopper. The broth hits air some hundred and twenty degrees colder than it is and unrolls into a white cloud &mdash; and Sir Corvus of the royal bodyguard, still haunted by a spore-choked cave he survived eleven months earlier, sees only the thing that almost killed him. He kills Kaelen before the cup reaches the King. The Crown's sealed account of the death is true in every clause and never mentions broth; House Skarth reads it as a throne signing its name beneath a murder. Kaelen's twin sister Yvaine cuts her hair, puts on his ancestral mail, climbs the mountain for a blessing she doesn't quite believe in, and leads the northern clans south, with the flask &mdash; cased in silver now, and renamed the Vessel of the Betrayed Host &mdash; carried at the front of their war-bands.</p>
          <p>Duke Vane, who wants the relic less for what it can do than for the Regency it could buy him, sells a beaten Maros his rescue at ruinous terms, hires the thief Soren to lift the vessel from the coalition's war-altar, and discovers too late what he has actually been fighting over. The war that follows is a slaughter no southern chronicle will ever name honestly; the scribes settle on the Great Winter Pestilence. <em>The Vessel of the Betrayed Host</em> closes on a Cultivator's archival log &mdash; Case Study 4,420: one flask, four centuries idle, and the most efficient war its Observer has recorded in eleven centuries.</p>""",
        "characters": [
            {
                "slug": "kaelen", "name": "Kaelen",
                "epithets": "Baron of House Skarth &middot; 25 years old &middot; twin brother to Yvaine",
                "teaser": "Rides two hundred miles to feed a king, and dies holding both halves of the gift.",
                "bio_html": """<p>Baron of House Skarth and <a href="../characters/yvaine.html">Yvaine</a>'s twin, and the book's clearest case of faith with no category for suspicion. Guest-right, in House Skarth's law, means a guest fed at your table is simply fed &mdash; no debt, no price &mdash; and he treats a royal hunting party exactly that way: accepting <a href="../characters/maros.html">Duke Maros</a>'s invitation before the messenger has finished reciting it, taking <a href="../characters/vane-4420.html">Duke Vane</a>'s offer to pay for provisions as the nearest thing to a genuine offense anyone has given him since leaving home, and quietly working a spare pair of dry socks free from his own baggage for a conscript whose boots have failed. He carries the household's steel flask two hundred miles north and holds it in reserve for the one night someone's need outruns the fires. When he finally unscrews the stopper for the King, <a href="../characters/corvus.html">Sir Corvus</a> kills him where he stands &mdash; flask in one hand, stopper in the other, before the cup has reached the King. His name outlives every other name attached to the war.</p>""",
                "quote": "Sos-vahlok bl&oacute;t-krah; mey sos krongrah &mdash; blood guards the hearth; sacrifice warms the frost.",
            },
            {
                "slug": "yvaine", "name": "Yvaine",
                "epithets": "Lady of House Skarth &middot; 25 years old &middot; twin sister to Kaelen",
                "teaser": "Cleans her brother's collar herself, cuts her hair with a hunting knife, and marches south.",
                "bio_html": """<p>Lady of House Skarth and <a href="../characters/kaelen.html">Kaelen</a>'s twin &mdash; the guarded, suspicious half of a pair with one face between them. She argues against the hunt from the day the invitation arrives, and loses. After his death she cleans the dried broth from his fur collar herself, swears the Blood-Oath of the Vacant Hearth alone in the chapel &mdash; cutting her hair with a hunting knife and pulling on his too-large ancestral mail &mdash; and climbs Mount Skahr to ask <a href="../characters/observer-4420.html">its keeper</a> for a blessing she doesn't quite believe in. She sends <a href="../characters/vane-4420.html">Duke Vane</a>'s gold and marriage contract back unanswered, spares the frightened border holdfast of Cindale, and ends the war in the hall of <a href="../characters/maros.html">Duke Maros</a>'s captured keep, where she finds Vane himself. She does not ask his name; she has known it for a year.</p>""",
                "quote": "Sos-vahlok bl&oacute;t-krah; mey sos krongrah &mdash; blood guards the hearth; sacrifice warms the frost.",
            },
            {
                "slug": "maros", "name": "Duke Maros",
                "epithets": "Duke of the Northern March &middot; Lord of Karhold Keep &middot; 45 years old",
                "teaser": "Answers a stag's head with a royal hunt, and pays with his feet, his house, and his life.",
                "bio_html": """<p>Duke of the Northern March, and the man whose wounded pride sends a royal hunt into the cold. Humiliated at his own table when <a href="../characters/vane-4420.html">Duke Vane</a> presents him with a summer-killed stag's head, he proposes a hunt in the deep northern winter to answer it &mdash; and it costs him every toe on both feet by the fourth week at the Broken Glacier. After the flask kills <a href="../characters/kaelen.html">Kaelen</a> he buys Vane's help on terms no one in his position could afford. His last honest act is a letter to the King warning him of Vane and begging that his wife and four-year-old son be kept out of Vane's reach; Vane's men take it from the courier at the pickets and burn it. Maros is arrested for treason and dies on the road south, in what Vane's own report calls an escape attempt met with necessary force.</p>""",
                "quote": "The north is not won by pride or oath. It is won by hunger, endured longer than the foe can bear.",
            },
            {
                "slug": "vane-4420", "name": "Duke Vane",
                "epithets": "Duke of the Southern March &middot; Lord of Vane Keep",
                "teaser": "Sends a stag's head to a rival and a thief to a mountain, and prices everything in between.",
                "bio_html": """<p>Duke of the Southern March: patient, gracious, and never once unpriced. It is Vane who wounds <a href="../characters/maros.html">Duke Maros</a> with a summer-killed stag's head presented as a gift at his own table, who joins the royal hunt to watch what follows, and who &mdash; when the flask kills <a href="../characters/kaelen.html">Kaelen</a> &mdash; sees not a tragedy but a relic, and through it a Regency. He sells a desperate Maros his rescue at ruinous terms, hires <a href="../characters/soren.html">Soren</a> to steal the vessel, has Maros arrested when he becomes a liability, and, when he finally pries the silver off himself in the small hours before his last council, finds only a dented steel flask that smells of old soup &mdash; and tells no one. <a href="../characters/yvaine.html">Yvaine</a> finds him in the hall of Maros's captured keep; his head is left on a pike before the drawbridge. (Not the same man as <a href="../characters/vane.html">Vane the Wanderer</a> of <em>The Iron Stiletto War</em>.)</p>""",
                "quote": "No guest leaves my table unfed. No oath leaves my memory. No insult leaves my blade unblooded. That is the law of my house.",
            },
            {
                "slug": "corvus", "name": "Corvus",
                "epithets": "Sir Corvus &middot; knight of the King's own bodyguard",
                "teaser": "A royal bodyguard undone by a cloud of steam that looks, for one half-second, like spores.",
                "bio_html": """<p>Knight of the King's own bodyguard &mdash; and, since a cave outside a border keep eleven months earlier, a man who can no longer fully separate the present from the year afterward, when he could not lift a spoon to his mouth without spilling the broth. Grey spore-dust, someone's breathing stopping beside him in the dark: by the eleventh night of the hunt he has not slept in four nights, and when <a href="../characters/kaelen.html">Kaelen</a> unscrews the flask and the broth unrolls into a white cloud, his whole body turns toward the sound of metal on metal before his mind is consulted. He kills Kaelen before the cup reaches the King. He serves another six years in the royal bodyguard, competently and without complaint, then lives eleven more alone on a small holding in the King's gift &mdash; a man who did the arithmetic more times than anyone should be asked to, and never once made it come out even.</p>""",
                "quote": "The spores do not sleep. They wait. Mist, rot, dark &mdash; I have known their breath. I will not breathe it again.",
            },
            {
                "slug": "observer-4420", "name": "Observer 814",
                "epithets": "Envoy of the Cultivators &middot; &ldquo;the Dragon-Speaker&rdquo; &middot; Case Study 4,420",
                "teaser": "Hands a family a steel flask, then waits four centuries on a mountain to see what they make of it.",
                "bio_html": """<p>A field agent of the <a href="../lore/cultivator.html">Cultivators</a>, who came down onto Mount Skahr in a black, wingless vessel some four centuries before the war and was folded by the clans, within a generation, into the Dragon-Speaker, keeper of the mountain &mdash; a name he never corrects. When an ancestor of House Skarth climbs up to beg a token of divine favor, Observer 814 passes a double-walled steel flask across the gap between his instruments and the man's frostbitten hands with roughly the ceremony a lord might spend tossing a coin to a groom, and goes back to watching. Then he waits, at compound interest, for whichever descendant is careless enough to call the loan due. Four centuries on, <a href="../characters/yvaine.html">Yvaine</a> climbs to his ice cavern for a blessing on the war she has already decided to fight, and comes down the mountain certain she carries one he never gave her. He files the case as the most efficient the Envoy has recorded in eleven centuries of comparable seedings &mdash; and remains assigned to it.</p>""",
                "quote": "I do not come to change. I come to witness. If change is already written, I will wait.",
            },
            {
                "slug": "soren", "name": "Soren",
                "epithets": "Shadow thief &middot; 38 years old &middot; of Byzantium",
                "teaser": "Steals the war's holiest relic for a duke, opens it in a hunter's cabin, and finds it smells of soup.",
                "bio_html": """<p>A thief claimed by no guild, who works for men rich enough that hiring him is safer than wondering who else might. <a href="../characters/vane-4420.html">Duke Vane</a> pays him more than he has ever been offered for an object he hasn't seen. Soren works his way into the coalition's country through the worst blizzard of the winter, lifts the vessel from the war-altar in the deepest hour of the worst night, when the sentries have been pulled back to shelter, opens its lock with a length of wire that has never once dulled or snapped, and is three miles gone before anyone thinks to check. Two days south, in a hunter's cabin, he pries off the silver and finds an empty, dented steel flask smelling of long-dried soup. He delivers it to Vane without a word and leaves Sumne within the month &mdash; the last man alive who ever looked beneath the silver, and a man who never says so.</p>""",
                "quote": "I don't steal for greed. I steal so that others won't have to bleed.",
            },
        ],
        "scenes": [
            {"slug": "the-twins-laughing",
             "alt": "Yvaine, with long white hair, and Kaelen, in furs and leather with pendants at his throat, laughing together with snowy mountains behind them",
             "caption_html": """<a href="../characters/yvaine.html">Yvaine</a> and <a href="../characters/kaelen.html">Kaelen</a>, before the hunt."""},
            {"slug": "kaelen-and-the-spilled-broth",
             "alt": "Kaelen lies in the snow with his eyes closed beside an overturned steel cup, steaming brown broth spreading across the ice",
             "caption_html": """<a href="../characters/kaelen.html">Kaelen</a>, and the broth that never reached the King."""},
            {"slug": "the-dragon-speaker-on-the-summit",
             "alt": "A white-haired figure in a snow-crusted cloak stands before Observer 814, who sits on a tall iron throne on a storm-swept peak with one hand held out",
             "caption_html": """<a href="../characters/observer-4420.html">Observer 814</a> on the frozen summit of Mount Skahr, receiving a climber from House Skarth."""},
            {"slug": "yvaine-cuts-her-hair",
             "alt": "Yvaine in chain mail holds a knife to her long white hair, cutting it off in a stone room beside a frosted window",
             "caption_html": """<a href="../characters/yvaine.html">Yvaine</a> cuts her hair and puts on her brother's mail."""},
            {"slug": "yvaine-after-the-oath",
             "alt": "Yvaine, her white hair now short and blood on her face and gloves, holds a sword upright before her eyes",
             "caption_html": """<a href="../characters/yvaine.html">Yvaine</a>, sword before her face &mdash; the vow made, the war ahead."""},
            {"slug": "yvaine-and-the-observer",
             "alt": "Yvaine, in a fur-collared cloak, faces Observer 814 across a frozen cavern floor beneath walls of hanging ice",
             "caption_html": """<a href="../characters/yvaine.html">Yvaine</a> and <a href="../characters/observer-4420.html">Observer 814</a> in the ice cavern."""},
            {"slug": "yvaine-above-the-frozen-plain",
             "alt": "Yvaine, seen from behind in a fur cloak, looks out from a snowy ridge at two distant keeps across a frozen plain under an orange sky",
             "caption_html": """<a href="../characters/yvaine.html">Yvaine</a>, looking out over the frozen plain."""},
            {"slug": "riders-toward-the-keep",
             "alt": "A column of riders under a black banner with a white beast's head and red streamers follows a snowy road toward a dark mountain keep",
             "caption_html": """A column of riders under a black banner approaches a mountain keep."""},
            {"slug": "the-broken-glacier",
             "alt": "A column of dark-cloaked figures winds between towering walls of blue-white ice in a narrow glacier defile",
             "caption_html": """The Broken Glacier."""},
            {"slug": "soren-with-the-flask",
             "alt": "Soren, in white snow gear with a crossbow across his lap, sits by a hearth in a wooden cabin holding a steel flask",
             "caption_html": """<a href="../characters/soren.html">Soren</a>, in a hunter's cabin two days south, with the vessel he was paid to steal."""},
            {"slug": "yvaine-in-the-south",
             "alt": "Yvaine, in dark plate with a fur collar and blood on her cheek, holds a sword low amid armed men beneath a black banner with a gold eagle, a castle on the skyline behind her",
             "caption_html": """<a href="../characters/yvaine.html">Yvaine</a> in the southern campaign."""},
            {"slug": "yvaine-and-vane-cross-blades",
             "alt": "Yvaine and Duke Vane cross swords over a banquet table in a candlelit hall while two servants cower beneath it",
             "caption_html": """<a href="../characters/yvaine.html">Yvaine</a> and <a href="../characters/vane-4420.html">Duke Vane</a>, blades crossed in the hall of <a href="../characters/maros.html">Maros</a>'s captured keep."""},
            {"slug": "the-pike-before-the-drawbridge",
             "alt": "A black iron pike stands upright in frozen ground before a ruined gothic gatehouse hung with red banners, gold coins scattered across the snowy stones at sunset",
             "caption_html": """Before the drawbridge of <a href="../characters/maros.html">Duke Maros</a>'s keep: the iron pike, and the gold no one took."""},
            {"slug": "the-herald-and-the-coin",
             "alt": "A black-gloved hand in a red cuff embroidered with a gold crown and eagle reaches for a single gold coin lying on snowy flagstones",
             "caption_html": """The herald finds the one coin left balanced beneath <a href="../characters/vane-4420.html">Duke Vane</a>'s eyes."""},
            {"slug": "the-black-fletched-arrow",
             "alt": "A black-fletched arrow lies across a field of snow and dark stone",
             "caption_html": """The black-fletched arrow the northern clans use to mark their dead along the ice line."""},
            {"slug": "the-frozen-wall",
             "alt": "A chain of grey stone watchtowers stretches away across a frozen sea, the nearest with a timber lookout and a lit window",
             "caption_html": """The watchtowers a later king raised along the northern frontier."""},
            {"slug": "the-great-winter-pestilence",
             "alt": "A hand with a quill writes 'The Great Winter Pestilence' across the top of a parchment by candlelight, books and an inkwell behind it",
             "caption_html": """What the scribes wrote: first a timber-tariff dispute, then &ldquo;the Great Winter Pestilence.&rdquo;"""},
        ],
    },
    {
        "slug": "4555", "title": "The Vessel of Unmediated Grace",
        "status": ["published", "google-books"],
        "cover_file": "4555.jpg",
        "hook": "A traffic cone, a reluctant duke, and forty-one years spent trying to give a crown back.",
        "case_tag": "Case 4555",
        "catalyst": {
            "name": "The Vessel of Unmediated Grace",
            "meta": "Mundane Class",
            "page": "books/4555.html",
            "img": "scenes/the-anchorite-plants-the-vessel-grid.jpg",
            "html": "<p>A hollow rubber traffic cone banded in retroreflective silver, seeded three at a time in a drainage ditch on the reasoning that a single unit left in open terrain is recovered by its intended finder only slightly more often than it's carried off by a flood or a curious child. Mistaken, when a beam of concentrated light finds it, for the literal residue of divine grace.</p>",
        },
        "envoy": {
            "name": "Observer 902",
            "meta": "Field Observer, Cultivator Envoy Corps",
            "page": "characters/observer-902.html",
            "img": "characters/observer-902-thumb.jpg",
            "html": "<p>Stationed unseen in an alcove of the Grand Basilica's own black stone, filing four centuries of flat, evaluative-language-free reports on a single cone &mdash; and breaking protocol exactly once, to note, unbidden, that the subject wanted to leave.</p>",
        },
        "pages": "103",
        "genre": """Epic Fantasy &middot; Satire &middot; Political Intrigue""",
        "google_books_url": "https://play.google.com/store/books/details/Dzul_Faraaghaini_Case_4555_The_Vessel_of_Unmediate?id=TOQFEgAAQBAJ",
        "synopsis_html": """<p>When King Aethelgard the Resplendent dies without an heir, Illumaria's whole theology of visible grace turns the search for his successor into a lit competition: three rival claimants &mdash; Archduke <a href="../characters/ignis.html">Ignis</a>, Duchess <a href="../characters/astraea.html">Astraea</a>, and Duke <a href="../characters/cassian.html">Cassian</a> &mdash; arrive at the Grand Basilica of Sol-Invictus each wearing a device built to make them glow. Duke <a href="../characters/blakk.html">Blakk</a> of Mud-Reach, the poorest and least ambitious name on the guest-roll, comes only to vote for whoever won't raise the timber tax &mdash; and three nights before his household guard crosses a nameless drainage ditch, an <a href="../characters/anchorite-of-the-drowned-road.html">Anchorite of the Drowned Road</a>, working for the Cultivator Envoy Corps' <a href="../characters/observer-902.html">Observer 902</a>, plants three identical objects in the mud as standard redundancy. Blakk's horse finds the first.</p>
          <p>He sets the resulting hollow orange cone on his own head as a joke, forgets to take it off, and is still wearing it in the Basilica's last row when High Pontiff <a href="../characters/sarel.html">Sarel</a>'s ceremonial beam of concentrated light finds it &mdash; and its retroreflective bands throw the beam straight back down the line it arrived on, cracking a three-century-old lens and blinding half the congregation with what looks, to three thousand kneeling monks, like the most convincing grace the Decree of Luminescence has ever produced. Blakk spends the next forty-one years trying to give the throne back. Nobody believes him: not the three houses whose war at the Standing at Illmere Ford turns his identical, unread letters of surrender into a legendary act of strategic mercy, and not Canon Voss, the one man who does the geometry correctly and spends four decades, and one exile, trying and failing to prove it.</p>
          <p>What follows is less a triumph than an audit: a marriage settled by one underlined line in a private ledger, a Law of Succession that costs Blakk the very thing forty years of reluctant grace had bought him, and a Rite of Reconsecration, delayed until his deathbed, that finally puts the Vessel to the one test it was never built to survive. <em>The Vessel of Unmediated Grace</em> closes on a Cultivator's own archival log &mdash; Case Study 4,555: one 0.2-pound cone, a kingdom that never gets to read its own founding accident correctly, and an Observer already three ditches away before the file is closed.</p>""",
        "characters": [
            {
                "slug": "blakk", "name": "Blakk",
                "epithets": "Duke of Mud-Reach &middot; later High Sovereign of Illumaria &middot; reigned 41 years",
                "teaser": "Falls off his horse into a ditch, puts a traffic cone on his head as a joke, and spends four decades trying to give the crown back.",
                "bio_html": """<p>Duke of Mud-Reach, governing nine hundred square miles of drained marsh, standing timber, and tenant debt so ordinary it barely required collecting. His own name means, in his grandmother's border dialect, simply <em>black</em> &mdash; no chronicler ever settled whether it referred to his hair, his moods, or the bog-silt his family's boots never fully shed. He comes to the Great Judgment wanting nothing but to vote for whoever won't raise the timber tax and be home before spring flooding closes the border road; three days out, his horse loses its footing at a drainage ditch, and he sets the orange cone it throws him toward on his own head as a joke for his six guardsmen.</p>
          <p>He spends the next forty-one years trying to give the resulting crown back. He refuses the Rite of Reconsecration rather than watch it melt in a Basilica flame, writes identical, unbelieved letters of surrender to <a href="../characters/ignis.html">Ignis</a>, <a href="../characters/astraea.html">Astraea</a>, and <a href="../characters/cassian.html">Cassian</a> before the Standing at Illmere Ford anyway, and marries Astraea two years after the war on terms she sets, not he. He fights his own nobility for a Law of Succession that will spare his cousin <a href="../characters/petrin.html">Petrin</a>'s heirs the same accident, and confesses everything, in his last clear hour, to the three people &mdash; <a href="../characters/harn.html">Harn</a>, Petrin, and <a href="../characters/prisca.html">Prisca</a> &mdash; he trusts to decide what a kingdom does not need to carry.</p>""",
                "quote": "I only wished to sit in the back.",
            },
            {
                "slug": "astraea", "name": "Astraea",
                "epithets": "Duchess, House Astraea &middot; later Queen of Illumaria",
                "teaser": "Musters an army over a letter she doesn't quite believe, and spends the rest of her life auditing what that cost her.",
                "bio_html": """<p>Duchess of House Astraea, and the second claimant to stand the Great Judgment's trial: a six-foot Chandelier Wheel of a hundred and twenty tallow candles, strapped above her shoulders, that leaves the back of her neck blistered in a pattern she calls, to exactly one person, a second crown worn beneath the first. She musters her border levies less for the grazing land her council cites than because she can no longer bear being pitied, and her cavalry meets <a href="../characters/ignis.html">Ignis</a>'s own raiding column at the Standing at Illmere Ford on her marshal Coel's counsel, not her own conviction &mdash; a mistake her body-servant <a href="../characters/prisca.html">Prisca</a> hears her admit, alone, the same night: <em>he offered, and I refused.</em></p>
          <p>She spends a month testing <a href="../characters/blakk.html">Blakk</a>'s goodness for a catch it never turns out to have, then two more years proving in public, through unglamorous service on his border commission, that her change of heart isn't a fresh maneuver for the throne. She marries him the following spring, becomes the sharper half of what the court quietly calls the Evening Ledger, and throws herself between him and Canon Voss's blade at Sarn's Crossing, taking a wound that troubles her for the rest of her life. She dies in the reign's thirty-sixth year, having underlined one line in her own private ledger more times than she ever admitted.</p>""",
                "quote": "He offered. I refused.",
            },
            {
                "slug": "cassian", "name": "Cassian",
                "epithets": "Duke Cassian, House Cassian &middot; Noble Claimant to the throne of Illumaria",
                "teaser": "Holds his chin unnaturally high to keep his own crown from breaking his neck, then does the same careful arithmetic on an entire war.",
                "bio_html": """<p>Duke Cassian comes last and lightest to the Great Judgment: a five-foot Burnished Steel Sunburst of razor blades on a spine no thicker than a finger, engineered with real rigor for reflection and none at all for a grown man's neck, so that he holds his chin unnaturally high through the whole ceremony &mdash; arithmetic, not vanity, since any deeper bow was likely to snap his own spine for him. He reads <a href="../characters/blakk.html">Blakk</a>'s letter of surrender twice and does nothing, trusting no one but concluding, correctly, that a war against a man who has already surrendered is a war fought for nothing; he holds his own forces two days' march from the Standing at Illmere Ford for the whole engagement and arrives on the fifth day to find no one left worth conquering.</p>
          <p>He proposes terms, retires within the fortnight, and spends the remaining thirty-one years of his life keeping a private ledger he calls the Cost of Not Winning &mdash; tallying, year on year, everything a crown might once have been worth against a column he never lets himself total in full. He turns down a coalition's offer to back his own claim without ever mentioning it to anyone, including Blakk, and dies in his own bed having proven, to his own satisfaction only, that a kingdom which asks nothing of him balances its books better than one he ruled.</p>""",
                "quote": "A kingdom that costs a man nothing to leave alone is a kingdom he has already, whether he meant to or not, chosen to keep.",
            },
            {
                "slug": "ignis", "name": "Ignis",
                "epithets": "Archduke Ignis, House Ignis &middot; Eldest Claimant to the throne of Illumaria",
                "teaser": "Wears seventy pounds of burning iron to prove his grace is forged rather than given, and loses the throne to a cone anyway.",
                "bio_html": """<p>Archduke Ignis takes the Great Judgment's dais first, as eldest claimant and loudest patron of the doctrine that grace must be forged rather than merely inherited: an Anvil Forge Helm of seventy pounds of black iron housing a coal hearth at its crown, pumped by two apprentice boys until the watching monks swear his whole head appears to burn. His own First Counselor, Farris, picks apart <a href="../characters/blakk.html">Blakk</a>'s letter of surrender clause by clause and convinces the war council it is a trap rather than a confession; Ignis strikes first at what his scouts wrongly call an enemy vanguard, and the Standing at Illmere Ford follows within the day.</p>
          <p>No two surviving accounts agree on whether he fell in the fighting or rode east and kept riding. His nephew Ossian inherits a house reduced, over two decades, from first rank to an increasingly theoretical eighth &mdash; and is given back, unasked and in full, the very grazing rights his uncle lost, in the single act of mercy Ossian spends fifty-four years failing to forgive.</p>""",
                "quote": "With fire and iron, I take what is mine.",
            },
            {
                "slug": "aethelgard", "name": "Aethelgard",
                "epithets": "King of the High Realm of Illumaria &middot; Deceased",
                "teaser": "Dies without an heir, and leaves an entire kingdom's theology with nothing left to measure but a stopped heart.",
                "bio_html": """<p>King Aethelgard the Resplendent rules Illumaria as the Decree of Luminescence's own proof of concept: radiant, beloved, and, court chroniclers agreed, so charismatic that his own heart was said to burn too brightly for anything as mundane as a legacy. He dies without an heir in three attempted marriages, a fact the court physicians attribute to a stopped heart and the Last Order attributes, with rather more theological confidence, to a soul too incandescent for any womb to house its successor.</p>
          <p>His death is the vacancy the entire book fills: it sends High Pontiff <a href="../characters/sarel.html">Sarel</a> looking for the next man or woman who can be proven, publicly, to glow, and puts <a href="../characters/ignis.html">Ignis</a>, <a href="../characters/astraea.html">Astraea</a>, and <a href="../characters/cassian.html">Cassian</a> &mdash; and, far down a guest-roll ranked by wealth, <a href="../characters/blakk.html">Duke Blakk of Mud-Reach</a> &mdash; into the same Basilica on the same morning.</p>""",
                "quote": "They said his soul burned so brightly, his heart forgot how to leave a legacy behind.",
            },
            {
                "slug": "sarel", "name": "Sarel",
                "epithets": "High Pontiff of Sol-Invictus",
                "teaser": "Draws back a curtain to test four rivals for grace, and spends the rest of his life half-blind from what answered.",
                "bio_html": """<p>High Pontiff of Sol-Invictus, and the one man in Illumaria whose private eleven years of doubting the Decree of Luminescence leave him its sole living arbiter the moment <a href="../characters/aethelgard.html">Aethelgard</a> dies. He presides over the Great Judgment, draws the final baffle from the Sol-Focus Arc himself, and takes the returning beam directly in one eye when <a href="../characters/blakk.html">Blakk</a>'s cone reflects it back along its own line of arrival &mdash; cracking a lens no Pontiff after him is ever permitted to have repaired, and leaving him in tears he cannot stop for the rest of that day.</p>
          <p>He invents the Triple Vessel doctrine once two further cones are recovered from the same ditch, crowns Blakk a second time as High Sovereign, and spends four decades keeping the vessels' true fragility a secret paid for in gold and silence. He talks <a href="../characters/petrin.html">Petrin</a> out of confessing the fraud immediately after Blakk's death, oversees the crown's final, confirming destruction by open flame, and sets down, in a testament his own successor won't find for twenty years, the one article of faith his doctrine never actually required of him.</p>""",
                "quote": "Let no shadow claim what shadow did not make.",
            },
            {
                "slug": "harn", "name": "Harn",
                "epithets": "Captain Harn &middot; Captain of the Guard to Duke Blakk",
                "teaser": "Checks a stranger's cone by torchlight out of plain habit, and spends the next forty years still watching for the same glint.",
                "bio_html": """<p>Captain of Duke Blakk's household guard, a broad, unhurried man who operates on the sound principle that anything he can't identify probably isn't worth identifying &mdash; until a torch swung near a discarded cone throws back a flare that leaves him seeing green for the better part of an hour. He is the one man Blakk ever tells the truth of his own coronation to (&ldquo;I only wished to sit in the back&rdquo;), and the one man who understands, without being told twice, exactly what his duke fears about it.</p>
          <p>He catches Canon Voss's hired assassin by the wrist a half-second before the blade lands, forty years and by his own count a fourth save into a friendship neither man ever calls that aloud, and stands with <a href="../characters/petrin.html">Petrin</a>, <a href="../characters/prisca.html">Prisca</a>, and <a href="../characters/sarel.html">Sarel</a> as one of the four witnesses to the crown's final, confirming melt. He never once tells Blakk that giving away a throne might have cost him less than accidentally winning one. He is not sure, by the end, that it would have.</p>""",
                "quote": "My life is the Duke's shield. My flame, his final light.",
            },
            {
                "slug": "petrin", "name": "Petrin",
                "epithets": "Heir Presumptive &middot; later King of Illumaria",
                "teaser": "Spends eleven years quietly reconciling granary ledgers, and inherits a crown that finally requires nothing more mystical than that.",
                "bio_html": """<p>Blakk's cousin and heir presumptive, sixteen years old and watching from the walls on the day of the Standing at Illmere Ford, then a grey, heavily audited man of fifty-six by the morning Blakk finally dies. Set for eleven years to personally reconcile every granary shipment against its own certified weight, he uncovers a granary-master's six-year fraud through sheer tedium rather than brilliance, brings it to Blakk directly, and watches his cousin choose mercy calibrated to a debtor's actual circumstances over the arrest three advisors recommend &mdash; the lesson of that whole education he later credits above every province he was ever required to govern.</p>
          <p>He is one of the last four people Blakk ever tells the truth to, and argues, at first, for confessing it publicly before his cousin is even buried; <a href="../characters/sarel.html">Sarel</a> talks him out of it. His own coronation, held under the Law of Succession Blakk fought his whole nobility to pass, needs no basilica, lens, or flame &mdash; the most boring coronation in Illumaria's recorded history, and, by his own reckoning, the truest proof the law had worked.</p>""",
                "quote": "Illumaria endures not by the crown, but by the will that bears its weight.",
            },
            {
                "slug": "prisca", "name": "Prisca",
                "epithets": "Body-servant to Duchess Astraea",
                "teaser": "Dresses the Duchess's wounds for eleven years, and keeps the one sentence that mattered for the rest of her own life.",
                "bio_html": """<p>Body-servant to Duchess <a href="../characters/astraea.html">Astraea</a> for eleven years, and the one person who sees her mistress somewhere past the composure four centuries of House Astraea trained into her. She goes into Astraea's tent the night after the Standing at Illmere Ford against her own better judgment, sits with her on the cold ground, and hears the four words Astraea never repeats to anyone else: <em>he offered, I refused.</em></p>
          <p>She serves as the last keeper of Astraea's private ledger after her death, and is one of the four people <a href="../characters/blakk.html">Blakk</a> confesses everything to in his final hour, alongside <a href="../characters/harn.html">Harn</a> and <a href="../characters/petrin.html">Petrin</a>. She is the one voice in that room who argues, quietly, that burying the king's own last truth is not quite the mercy the other three take it for &mdash; and never claims, afterward, that she was talked out of believing it.</p>""",
                "quote": "I have seen the Duchess in glory, in grief, and in silence. I dressed her wounds, and I held my tongue.",
            },
            {
                "slug": "fenn", "name": "Fenn",
                "epithets": "Peddler / Merchant",
                "teaser": "Sells fake splinters of a false crown for eleven years, then spends decades watching the real thing give itself away for free.",
                "bio_html": """<p>A peddler of no particular loyalty who survives two previous wars by supplying both sides slightly different lies, and who spends the opening weeks of Illumaria's own succession war selling pilgrims small shards of orange-dyed river quartz, warmed over a candle and passed off as splinters of the sovereign's own crown. He calls it Ember-Glass. He believes in it, the Unconquered Sun, and, by his own account, very little else, which he considers sound business rather than a failure of faith.</p>
          <p>He reinvents himself into almanacs once genuine relic-hunters start asking pointed questions about his supply chain, and returns to the capital only once more, decades into the Long Peace, to find <a href="../characters/blakk.html">Blakk</a> personally arguing a farmer's grain-tithe exemption at the palace's lower gate. He writes, that same night, in a ledger he shows no one, that he made a fortune selling counterfeit grace for eleven years, and that the king has been selling the genuine article for nearly thirty and has, so far as he can tell, made nothing at all off it.</p>""",
                "quote": "Ember-Glass for warding fear and inviting warm fortune.",
            },
            {
                "slug": "anchorite-of-the-drowned-road", "name": "Anchorite of the Drowned Road",
                "epithets": "Drowned Road Sect &middot; Holy Ascetic",
                "teaser": "Plants three identical cones in a nameless ditch on behalf of the Cultivator Envoy Corps, and never once meets anyone's eye.",
                "bio_html": """<p>One of the small, tolerated, faintly pitiable Drowned Road sect, who hold that no soul can properly appreciate the Unconquered Sun's grace without first practicing, at length and in mud, its total absence. Three nights before Duke Blakk's household guard crosses a nameless drainage ditch, this Anchorite &mdash; smaller than most, its accent unplaceable, working on behalf of <a href="../characters/observer-902.html">Observer 902</a> of the Cultivator Envoy Corps &mdash; kneels at the ditch's lip and sets three identical objects into the silt rather than one, standard redundancy under a protocol written after several thousand comparable seedings elsewhere.</p>
          <p>The tenants who notice the Anchorite at all notice only what they always notice about that sect: robes the color of an old bruise, an accent no market morning has ever placed, and an eye that never once meets theirs. Their part in the story ends there. What they left in the mud does not.</p>""",
                "quote": "The road drowns what it should not reach. I simply mark where it remembers.",
            },
            {
                "slug": "observer-902", "name": "Observer 902",
                "epithets": "Field Observer, Cultivator Envoy Corps",
                "teaser": "Files four centuries of flat, evaluative-language-free reports on one cone, and breaks protocol exactly once to say why it mattered.",
                "bio_html": """<p>The Cultivator field agent running Case Study #4,555, stationed unseen in an alcove cut into the Grand Basilica's own black stone. Its reports use, per protocol, no first-person pronoun and no evaluative language whatsoever &mdash; and its very first entry breaks that protocol once anyway, recording, against its own training's explicit judgment that the detail was not relevant to the case, that the drainage ditch it had just seeded smelled of a particular decayed sweetness.</p>
          <p>It closes the file four centuries later, by Illumarian reckoning, with a report that credits the whole intervention to a single 0.2-pound retroreflective object meeting a legitimacy doctrine with zero tolerance for ambiguous results &mdash; and appends, in a margin the Corps' own style guide explicitly discourages, four words it would call purely descriptive and would not, under any circumstance the Corps could devise, call what they actually were: <em>he wanted to leave.</em> It is already three ditches, and one kingdom, away before the file is even closed.</p>""",
                "quote": "To witness without interference. To record without judgement. The Observer does not alter the outcome.",
            },
        ],
        "scenes": [
            {"slug": "the-anchorite-plants-the-vessel",
             "alt": "A hooded Anchorite of the Drowned Road kneels at the edge of dark water, setting an orange and white traffic cone into the mud, a distant city skyline behind them",
             "caption_html": """The <a href="../characters/anchorite-of-the-drowned-road.html">Anchorite of the Drowned Road</a> plants the Vessel in a ditch no map had ever named."""},
            {"slug": "the-fall-at-the-ditch",
             "alt": "A rearing horse throws its rider face-first into a muddy ditch beside a bright orange traffic cone",
             "caption_html": """<a href="../characters/blakk.html">Blakk</a>'s palfrey loses its footing, and pitches its rider toward the Vessel."""},
            {"slug": "a-joke-for-the-guard",
             "alt": "A muddy man lifts an orange traffic cone onto his own head like a crown while soldiers and a dark horse look on",
             "caption_html": """<a href="../characters/blakk.html">Blakk</a> sets the cone on his own head as a joke for his guard."""},
            {"slug": "the-beam-finds-blakk",
             "alt": "A man wearing an orange cone stands lit by a blinding shaft of golden light inside a vast dark cathedral, clergy and nobles gathered around him",
             "caption_html": """The Sol-Focus Arc's beam finds <a href="../characters/blakk.html">Blakk</a>, beneath his column, at the Great Judgment."""},
        ],
    },
    {
        "slug": "4438", "title": "The Heavenly Thunder-Serpent",
        "status": ["published", "google-books"],
        "cover_file": "4438.jpg",
        "hook": "One tired fish, one polished suit of armor, and an empire that mistook a shock for a mandate.",
        "case_tag": "Case 4438",
        "catalyst": {
            "name": "The Heavenly Thunder-Serpent",
            "meta": "Mundane Class",
            "page": "characters/the-heavenly-thunder-serpent.html",
            "img": "characters/the-heavenly-thunder-serpent-thumb.jpg",
            "html": "<p>A scale-less electric eel, eight feet long and thick as a fisherman's forearm, capable of a self-generated discharge of up to 860 volts. Left to live under a fallen lintel in a flooded ruin, then hauled alive to a capital that names it a spirit-beast, a god, and finally a fetus of the Chaos Epoch &mdash; and never once a fish.</p>",
        },
        "envoy": {
            "name": "Observer 403",
            "meta": "&ldquo;the Hermit of Nine Bends&rdquo;",
            "page": "characters/elder-peng.html",
            "img": "characters/elder-peng-thumb.jpg",
            "html": "<p>A hermit among the flooded ruins below Nine Bends for one hundred and forty-one local years, rotating through identities as the district forgets the last one. Places the eel in the basin, then does almost nothing &mdash; and keeps entering the same unauthorized phrase in his notes.</p>",
        },
        "pages": "82",
        "genre": """Historical Fantasy &middot; Political Intrigue &middot; Tragedy""",
        "google_books_url": "https://play.google.com/store/books/details?id=hRoSEgAAQBAJ",
        "synopsis_html": """<p>For eleven years the fisherman <a href="../characters/ren-duo.html">Ren Duo</a> has worked the flooded ruins below Nine Bends, where a river drowned an old town and left its stone gateways standing in the shallows. Then one morning his net brushes something black beneath a fallen lintel, the water lights from the inside, and he is thrown into the shallows with his fingers curled into claws he cannot open. He does the small, honest, sensible thing: he tells the magistrate. Within the month the Yan court has sent armed men and a wagon; six men drown securing the creature for the road; and by the time it reaches the capital it has a new name &mdash; the Heavenly Thunder-Serpent &mdash; and a waiting list for its water.</p>
          <p>At Yujing, Chief Alchemist <a href="../characters/zhou-xuan.html">Zhou Xuan</a> gives the creature a theology long before anyone has thought to measure it, and the court's ladies and dukes line up to be shocked. Only <a href="../characters/mei-suwen.html">Mei Suwen</a>, a court Reckoner with no rank and a hand so small a servant once mistook her columns for brocade, keeps the numbers: how long the current takes to come, how much weaker the next one is, what a frightened animal does. Her warnings are carefully worded, carefully ranked, and carefully filed beneath the grain tallies. The <a href="../characters/yongkang-emperor.html">Yongkang Emperor</a> &mdash; nine years into a reign no one has dared audit, raised on a childhood prophecy that Heaven owes him a debt &mdash; hears the same water differently. He means to step into it, in full ceremonial armor, before witnesses, and collect.</p>
          <p>What the Trial does to the empire afterward is arithmetic: a dead sovereign, a court that mistakes a shock for a verdict, and a son, <a href="../characters/yue.html">Prince Yue</a>, who is the one man who ever asked Mei Suwen what her numbers actually meant &mdash; and understood every word. Twelve of the empire's ranking officials are sent into the water in the Second Trial; eleven do not come out. A warlord in the southern salt marshes stops forwarding the tribute, a three-province coalition reaches Yujing's walls, and a court physician writes the only honest page anyone ever produces about the creature, then burns it himself. <em>The Heavenly Thunder-Serpent</em> closes on a Cultivator's own archival log &mdash; Case Study 4,438: one large, increasingly tired fish, a hermit who keeps filing the same unauthorized phrase, and the chronicles that will remember none of it.</p>""",
        "characters": [
            {
                "slug": "mei-suwen", "name": "Mei Suwen",
                "epithets": "The Reckoner &middot; Court Reckoner of Yujing &middot; 28 years old",
                "teaser": "Measures the serpent for eleven months and warns everyone who will listen &mdash; and is understood perfectly by exactly the wrong man.",
                "bio_html": """<p>A court Reckoner with no formal rank, raised on the omens and lucky days of the minor gentry until her eleventh year, when a diviner's confident and entirely wrong forecast of drought cost her father three harvests and taught her that confidence and accuracy are different currencies. She has spent the seventeen years since betting her career that the second one eventually pays its debts. When the serpent reaches Yujing she does what no alchemist thinks to do: she times it. Her ledger, in a hand so small that a servant dusting her desk once mistook the columns for decorative brocade, records how long the current takes to come, how much weaker the next discharge is, and why a disturbed animal is a less predictable one.</p>
          <p>She warns <a href="../characters/zhou-xuan.html">Zhou Xuan</a>, sends a final written warning to <a href="../characters/zheng-kui.html">Zheng Kui</a> that his office files unread, and watches the Second Trial unfold in exactly the order she least wanted to be right about. The one person who ever asks what her numbers actually say is <a href="../characters/yue.html">Prince Yue</a>, and she learns too late what it means that he understood them perfectly. She keeps, in the same locked chest as her most sensitive ledgers, a small and entirely unscientific collection of pressed flowers gathered from every posting she has ever held &mdash; a habit she has never recorded in any professional capacity. She outlives two emperors and the empire that employed her, and in the one account no chronicle confirms, she is last seen pouring tea in a teahouse with <a href="../characters/wan-er.html">Wan-er</a>.</p>""",
                "quote": "Numbers do not kneel for anyone, Your Highness. They only tell the truth.",
            },
            {
                "slug": "yue", "name": "Yue",
                "epithets": "Prince Yue &middot; third son of the Yongkang Emperor &middot; later Emperor Yue &middot; 40 years old",
                "teaser": "The only man at court who asks what the numbers actually say &mdash; and then chooses the conclusion.",
                "bio_html": """<p>Third among the Yongkang Emperor's sons, and the one man at court who goes looking for <a href="../characters/mei-suwen.html">Mei Suwen</a> in the archive to ask not what the alchemists say the water means, but what it does. He listens, asks sharper questions than she expected, and sits through a whole session drinking a specific bitter tisane his mother once brewed for him during a childhood illness, which no one since has ever managed to make correctly. He argues his father out of the Solstice Trial on pure strategic grounds and is dismissed. His daughter <a href="../characters/wan-er.html">Wan-er</a> is the one person in the palace he has least often found time to notice.</p>
          <p>When his father dies in the water, Yue takes the throne against the court's plain expectation and turns the Second Trial into a purge whose order he had written, in his own hand, across two years of ordinary court paranoia &mdash; long before any fish had entered any tank. He added <a href="../characters/pei-rong.html">Pei Rong</a> last, underlined once, and left off <a href="../characters/kang-yi.html">Kang Yi</a> on the plain arithmetic that a throne with no rivals and no soldiers to hold its walls is merely an inheritance for whichever warlord notices first. The arithmetic is sound. It is also, he discovers in the siege that follows, not the whole of the sum. When the last wall falls he wears his father's armor, and enters the water himself.</p>""",
                "quote": "Ritual is data. Power is interpretation. I choose the conclusion.",
            },
            {
                "slug": "yongkang-emperor", "name": "The Yongkang Emperor",
                "epithets": "Emperor of Yan &middot; ninth year of his reign &middot; Deceased",
                "teaser": "Inherits a Mandate no one has ever audited, and decides to audit it himself &mdash; in polished steel, in front of witnesses.",
                "bio_html": """<p>Nine years into a reign built on nine generations of everyone agreeing not to test whether the Mandate still applied, with a salt-marsh warlord quietly keeping his tribute and a western general calling him &ldquo;the old man in the Jade Hall&rdquo; in private letters the Ministry of Rites intercepted and wished it had not. At nine years old, in the year his own father nearly lost the throne to a coalition of uncles, a wandering Daoist read his birth chart at his mother's frightened insistence and named a fate: the Mark of the Unclosed Ledger, in which Heaven itself owes the child a debt that will come due, in full, exactly once, at a moment of the boy's own choosing. His mother repeated it to him until he could not separate it from the fact of surviving.</p>
          <p>He does not, strictly, believe the eel is a dragon. He needs three provinces to believe the water is holy, by the only method they have ever found persuasive: watching a man risk everything and either die or not. He remembers <a href="../characters/master-bai.html">Master Bai</a>'s singed beard, in the small hours before his own Trial, as evidence rather than warning. The night before, he summons no minister, only his granddaughter <a href="../characters/wan-er.html">Wan-er</a>, who tries on his gauntlets, three sizes too large, while he tells her about the carp that swam upstream until it became a dragon. Two days later the court records that he ascended to the Nine Heavens, his body received rather than killed.</p>""",
                "quote": "Heaven owes me a debt.",
            },
            {
                "slug": "ren-duo", "name": "Ren Duo",
                "epithets": "Fisherman of Nine Bends &middot; eleven years on the flooded ruins",
                "teaser": "Tells the truth once, to the nearest official, and watches a small true thing become a large official one without his permission.",
                "bio_html": """<p>A fisherman with a widowed mother, a debt to his boat's previous owner, and a private rule of arithmetic about when frightening water is worth fishing. For ten of his eleven years on the flooded ruins the place gives him nothing stranger than good carp and the occasional drowned roof-tile. Then his net brushes something black beneath a fallen lintel, the water lights from the inside, and he is thrown into the shallows with his fingers curled like claws. He avoids the basin for eleven days, goes back on the ninth night with a coil of rope and a half-formed plan to lead the creature out himself, and does not try it. <a href="../characters/elder-peng.html">Elder Peng</a>, watching, lets him leave.</p>
          <p>What finally moves him is the same arithmetic that governs everything else in his life, and a smaller, less flattering wish to be believed. He stands outside the district magistrate's residence for the better part of an hour before he knocks. He had imagined a clerk writing the report down and filing it somewhere it would quietly wait to be useful; instead six armed men and a specially commissioned wagon arrive within the fortnight, and six men drown securing the transport. No history records their names. Ren Duo remembers all six for the rest of his life, though he never learns which name belongs to which face, and the not-knowing becomes its own shape of guilt. His own account of a numb hand is filed with the commission that studies the creature, and very likely burned with the rest.</p>""",
                "quote": "I did not seek the serpent. The river showed me&mdash;and I spoke.",
            },
            {
                "slug": "the-heavenly-thunder-serpent", "name": "The Heavenly Thunder-Serpent",
                "epithets": "An Electric Eel, Eight Feet Long &middot; the Catalyst of Case 4438",
                "teaser": "A large, shy, increasingly tired fish that an empire named a god &mdash; then renamed a bigger one.",
                "bio_html": """<p><em>Electrophorus voltai</em>: a scale-less electric eel, black, thick as a fisherman's forearm and longer than his boat, capable of a self-generated discharge of up to 860 volts. It is nocturnal, dislikes sudden movement, defends rather than attacks, and eats carp. It spends its early years beneath a fallen lintel in the flooded ruins below Nine Bends, then its captivity in a porcelain-and-gilt tank in the capital, retreating to the northern shadow whenever the crowd presses close. Everything the empire believes about it &mdash; the Nectar of the Thunder Dao, then the Yin-Lightning Fetus of the Chaos Epoch &mdash; is supplied by men who never once measure it. It was placed in the basin four years before the case opens by <a href="../characters/elder-peng.html">Elder Peng</a>, and then simply left.</p>
          <p>What actually kills the Yongkang Emperor is his own armor: wet steel sealed around a body, with no gap for the current to lose interest in. Its discharge weakens with every disturbance, and by the eleventh man in the Second Trial it has spent every volt it possessed across ten bodies and has nothing left to give him. It does not survive its last flooding; the order to fill the basin with stone is carried out by a crew paid to fill a basin, not to empty one first, and it dies within the season in stone-choked water. The chronicles record that it departed this lower world of its own accord.</p>""",
                "quote": "It is said to coil like a rope of night, and strike like the wrath of heaven. Yet it is no god, no dragon&mdash;only a creature of water and current.",
            },
            {
                "slug": "elder-peng", "name": "Elder Peng",
                "epithets": "Observer 403 &middot; Hermit of Nine Bends &middot; 141 local years in the ruins",
                "teaser": "A hermit who has outlasted every legend the district built about him, and keeps filing the same unauthorized phrase.",
                "bio_html": """<p>The <a href="../lore/cultivator.html">Cultivators</a>' Envoy at Nine Bends, and the only person in the story who knows what the fish is. He has occupied the flooded ruin for one hundred and forty-one local years under a rotation of identities &mdash; shipwreck survivor, hermit, mute penitent, and once, unhappily, a minor tax collector &mdash; and the district credits his sun-cured silence to a miracle of the sea-cave that let him survive a wreck. In truth his lungs draw on gases no local physician has a name for, an ocular array reads every pulse within sight, and a monitoring mechanism no larger than a beetle, sewn into the lining of his sleeve, records the water's conductivity and the serpent's discharge.</p>
          <p>The Prime Directive lets him intervene at several points, and he takes almost none of them. He lets <a href="../characters/ren-duo.html">Ren Duo</a> knock on a magistrate's door when a single sentence would have stopped him, and lets him leave the ruin with his rope and his half-formed plan when the protocol permits a less generous accounting. Instead he writes a single non-standard phrase into his log &mdash; &ldquo;rounding error&rdquo; &mdash; on eleven separate occasions, each time about someone outside his mandate. The Custodian's analyst notes it corresponds to no authorized metric, and that his cover identity remains unretired. Recommends no action. Recommends, in fact, nothing.</p>""",
                "quote": "Mountains remember what men forget. Rivers carry what men refuse to see.",
            },
            {
                "slug": "wan-er", "name": "Wan-er",
                "epithets": "The Yongkang Emperor's granddaughter &middot; Prince Yue's daughter &middot; 7 years old",
                "teaser": "Asks the only question worth asking twice &mdash; and is lied to kindly the first time.",
                "bio_html": """<p>Prince <a href="../characters/yue.html">Yue</a>'s daughter, seven years old at the Solstice, beloved of her grandfather and, by a standing exception to protocol no one has the courage to revoke, allowed to fall asleep most nights in a chair outside his private study. On the last evening of his life she tries on his ceremonial gauntlets, three sizes too large for her wrist, while he tells her the old story about the carp that swam upstream until it became a dragon. She does not understand that she is being given something. She understands only that her grandfather is, for once, not busy.</p>
          <p>When he dies in the water, a nursemaid not equal to the question tells her that yes, he became a dragon, because it is the only answer that does not require either of them to know anything true. It is a kind lie, and it is the moment she stops believing adults. During the siege <a href="../characters/mei-suwen.html">Mei Suwen</a> walks her to the western postern three evenings out of every seven, and she quietly rewrites the carp's ending so that it simply swims somewhere the river cannot follow. Years later, in a teahouse, she asks Mei one question &mdash; whether she thinks he became one &mdash; and is told, for the first time, an honest <em>I do not know.</em></p>""",
                "quote": "Did you truly become a dragon, Grandfather?",
            },
            {
                "slug": "sun-lin", "name": "Sun Lin",
                "epithets": "Inspector of Palace Accounts &middot; eunuch &middot; eleven years in post",
                "teaser": "Audits the alchemists for eleven years out of a grudge he never explains, then burns the records to save the men they would condemn.",
                "bio_html": """<p>Holds a minor, unglamorous post that eunuchs have traditionally used to enrich themselves, and has spent eleven years using it instead to quietly catalog every occasion the Court Alchemists' expenditures made no defensible sense &mdash; out of a hatred for that ministry so old and so specific that he has stopped explaining its origin even to himself. A reputation for getting inconvenient answers written down, rather than quietly buried, is the one thing eleven years of auditing has earned him in full. So when a frightened chamber-servant finds a folded list among Prince <a href="../characters/yue.html">Yue</a>'s discarded papers, it is Sun Lin she brings it to, and Sun Lin who hands it to <a href="../characters/mei-suwen.html">Mei Suwen</a>.</p>
          <p>He helps her and <a href="../characters/physician-kao.html">Physician Kao</a> measure what the Second Trial left behind, and during the siege he does the one thing no one asks of him: feeds the palace's own financial and requisition records into a brazier in the Ministry of Accounts, a few sheaves at a time, on the calm and entirely accurate theory that whichever administration inherits the city should not inherit the evidence to punish anyone with. His last letter to the Reckoner mentions that the Marshal once asked him whether an empire that killed its own competence deserved to be saved by either side. Then the correspondence stops, for reasons the record does not supply.</p>""",
                "quote": "Numbers do not lie. Men do.",
            },
            {
                "slug": "kang-yi", "name": "Kang Yi",
                "epithets": "Grand Marshal &middot; commander of the northern garrisons &middot; nineteen years of service",
                "teaser": "The one senior officer the Second Trial fails to consume &mdash; left off the list on arithmetic he is never told about.",
                "bio_html": """<p>Commander of the northern garrisons, and the only senior officer of the empire the Second Trial somehow fails to consume, because the prince who wrote its list did not lift the brush when the Marshal's name occurred to him. During the siege he finds himself in the position every competent man in a collapsing empire eventually finds himself in: responsible for a defense he did not design, using an army he did not train, on behalf of an Emperor he did not choose and increasingly does not trust. He gives no speeches. He drills the wall crews at the hours he always has, delivers the same clipped, unornamented instructions, and sees to it that they eat &mdash; and it is that plain arithmetic of rice, more than anything the court's theologians offer, that holds the eastern wall.</p>
          <p>He raises the possibility of a ceded province or a marriage alliance once, and only once, and reads in the Emperor's stillness that the answer is a decision already made. He comes closer than any man in the empire will to saying aloud what the Second Trial's own arithmetic made obvious &mdash; and does not, from the plain calculation that a marshal accused of treason defends nothing, while a marshal who holds his tongue might yet hold a wall. He opposes feeding the creature the palace's dwindling live carp with everything short of open refusal. By the end he is exchanging private letters with commanders on the far side of a wall that has not yet finished falling.</p>""",
                "quote": "Feed the soldiers, then speak of victory.",
            },
            {
                "slug": "zhou-xuan", "name": "Zhou Xuan",
                "epithets": "Chief Alchemist of the Yan Court &middot; thirty years of elixirs &middot; Deceased",
                "teaser": "Names the water before anyone measures it, and is the first man sent into it by the theology he invented.",
                "bio_html": """<p>For thirty years he has compounded elixirs that cured nothing and offended no one. When the serpent reaches Yujing he lets the Court Alchemists debate its provenance for four days with total confidence and no evidence whatsoever, then declares, on the fifth, that the water has been transformed by prolonged contact with a spirit-beast of the old Heavenly Tribulation lineage. This Nectar of the Thunder Dao, as he names it on the spot &mdash; testing the phrase in his mouth like a man trying on a ring he already intended to keep &mdash; can cleanse mortal impurity from anyone permitted to enter it. The theology he improvises over a tank of river water becomes the intellectual foundation of the Solstice Trial.</p>
          <p><a href="../characters/mei-suwen.html">Mei Suwen</a> brings him her numbers, and he has a fluent answer to every one. After the old Emperor's death, Prince <a href="../characters/yue.html">Yue</a> names the Chief Alchemist first into the basin of the Second Trial, and the court enters his death under theology rather than command. His rival and successor <a href="../characters/fu-baishi.html">Fu Baishi</a> spends the rest of the siege improving on his doctrine.</p>""",
                "quote": "The water is not poison, but the gate. It is the Nectar of the Thunder Dao.",
            },
            {
                "slug": "fu-baishi", "name": "Fu Baishi",
                "epithets": "Court Alchemist &middot; successor to Zhou Xuan",
                "teaser": "Improves the god once, and survives the empire once.",
                "bio_html": """<p>Spends a professional lifetime watching <a href="../characters/zhou-xuan.html">Zhou Xuan</a>'s mediocre compounds earn praise his own more rigorous ones never do, and concludes that the difference was never talent but nerve. Within days of his rival's death he announces that the truth was more magnificent than Zhou Xuan's small imagination allowed: the creature is no mere spirit-beast but a Yin-Lightning Fetus of the Chaos Epoch, a fragment of the world's own unformed birth-matter &mdash; which explains, with the satisfaction of a man correcting a rival's homework in public, why lesser theologies kept failing to predict its behavior.</p>
          <p>During the siege he keeps a private ledger of the Fetus's nightly communications, in a script he says predates writing and which one servant, glimpsing a page before being dismissed from the room, recognizes as Fu Baishi's own hand held at an unfamiliar angle. He proposes that its silence means displeasure, and that displeasure requires sacrifice &mdash; a proposal <a href="../characters/kang-yi.html">Kang Yi</a> rejects in council with a single flat sentence &mdash; and later that it be fed the palace's live carp. He survives the fall of Yujing by converting the authorship of his own doctrine, within a single week, into a testimonial for <a href="../characters/du-heng.html">Du Heng</a>'s more modest claim on Heaven's favor, and spends the last years of a long and comfortable life as the new court's most senior religious consultant.</p>""",
                "quote": "The world trembles because it has forgotten the root of lightning.",
            },
            {
                "slug": "physician-kao", "name": "Physician Kao",
                "epithets": "Court Physician &middot; investigator",
                "teaser": "Writes the one honest page anyone ever produces about the water &mdash; and burns it himself so no one can twist it.",
                "bio_html": """<p>A court physician who joins <a href="../characters/mei-suwen.html">Mei Suwen</a> and <a href="../characters/sun-lin.html">Sun Lin</a> in the first quiet week after the Second Trial to measure what remains. Between them they test the basin's water, drawn down, against silk thread and iron nails; they examine the Emperor's ruined breastplate, its interior scorched in a pattern that matches, node for node, the exact points at which his skin blistered; and they examine the exhausted animal itself. They write the finding on a single unadorned page: an unusually large specimen of an unremarkable river species, nocturnal, sensitive to sudden movement, with a defensive reflex rather than a judgment &mdash; and an Emperor killed by his own armor.</p>
          <p>He reads it aloud to the small commission that receives it, and watches their faces arrange themselves into the polite blankness of people who have decided in advance not to be persuaded. Then he takes the page home and burns it himself, so that the court cannot twist the truth into another lie. The histories do not record the page, or its author.</p>""",
                "quote": "What the court called divine fury was only flesh, blood, and heat.",
            },
            {
                "slug": "zheng-kui", "name": "Zheng Kui",
                "epithets": "Minister of the Court of Tribute",
                "teaser": "Loses four months' salary at dice and files the only warning that could have mattered beneath the grain tallies.",
                "bio_html": """<p>Minister of the Court of Tribute, whose office receives more urgent correspondence in an average week than any three clerks could read in full, and has settled into an unwritten triage: sorted by the sender's rank rather than the report's contents. It is a system that reliably places a woman with no formal title beneath the grain tallies of ministers who outrank her.</p>
          <p>On the morning of the Solstice Trial, <a href="../characters/mei-suwen.html">Mei Suwen</a>'s final written warning arrives at the tail end of a night he never once discusses for the rest of his career, having lost, by his own accounting, four months' salary at dice to a pair of provincial tax assessors he remains almost certain had been cheating him. He files it unread. It is a lapse that costs the empire a good deal more than four months' salary, and he spends what remains of his life failing to mention it to anyone.</p>""",
                "quote": "The dice are cold. Heaven is colder.",
            },
            {
                "slug": "meng-kuo", "name": "Meng Kuo",
                "epithets": "General &middot; Commander of the Western Passes &middot; nineteen years in command",
                "teaser": "Runs the numbers on refusing the summons and goes in anyway, in full armor, in front of his own soldiers.",
                "bio_html": """<p>Commanded the western passes for nineteen years, and in private correspondence the Ministry of Rites intercepted and wished it had not, called the old Emperor &ldquo;the old man in the Jade Hall.&rdquo; He arrives at the basin already understanding the true purpose of the summons, and steps in anyway, in full lamellar armor, because he has run the numbers on refusing &mdash; public disgrace, stripped rank, a slow provincial death against a fast public one &mdash; and a man who has spent his career ordering soldiers into worse odds cannot, in front of them, be seen to flinch from his own.</p>
          <p>The current takes him within the space of eleven breaths. The court, still fresh from the Chief Alchemist's death and unwilling to abandon a doctrine it has only just finished re-consecrating, tells itself a soldier's test is simply blunter and more physical than a scholar's, and that the water is working through the court by kind. He goes first of the war council's own dead.</p>""",
                "quote": "To refuse is to invite suspicion. To go is to die. I will choose the path that burdens no one.",
            },
            {
                "slug": "pei-rong", "name": "Pei Rong",
                "epithets": "Duke of Pei &middot; second to enter the Second Trial &middot; Deceased",
                "teaser": "Spends his last private minute balancing his estate's accounts so his sons will inherit clean books.",
                "bio_html": """<p>A duke whose only real offense is a competence at the Ministry of Tribute that Prince <a href="../characters/yue.html">Yue</a> intends, in time, to hold himself. His name is added last to Yue's list and underlined once, on the reckoning that his death will cost the empire one capable administrator and cost Yue, so far as he can then calculate, nothing he expects to need again. He is meticulous in accounts and in private responsibility, and he is the second to enter the water in the Second Trial.</p>
          <p>The one manservant who survives the week remembers him spending his final private minute not in prayer but in a rapid, whispered accounting of his estate's debts to three separate creditors, apparently determined that whichever of his sons inherits will at least inherit clean books. His death produces a fresh and marginally more strained theory &mdash; that purity runs differently through different bloodlines &mdash; and, months later, a small silence in a besieged council when the Emperor asks for the one administrator he would have trusted to reconcile a granary count, and remembers, unaided, why he is not available.</p>""",
                "quote": "Before the basin takes me, I will settle every number.",
            },
            {
                "slug": "du-heng", "name": "Du Heng",
                "epithets": "Warlord of the Southern Salt Marshes",
                "teaser": "Stops forwarding the tribute, renames his levies a rescue, and fills the basin with stone.",
                "bio_html": """<p>Warlord of the salt marshes to the south, who stopped forwarding the province's tribute to the capital and quietly began keeping it well before the Solstice. When the Emperor dies in the basin and the court follows him into it, he stops calling his levies a tax and begins calling them, without apparent irony, a rescue: the throne, he tells his captains, has proved itself unequal to Heaven and therefore to men, and someone competent will need to hold the empire together while the Jade Hall finishes counting its dead. Two more provinces echo him within the season, each by a different justification and the identical conclusion.</p>
          <p>He reaches the walls of Yujing at the head of a three-province coalition and refuses every delegation the dwindling court sends, calling the whole thing correction rather than conquest. When the city falls he finds the throne empty and the basin drained a second time, and orders it filled in with stone rather than water &mdash; on the grounds, reasonable to absolutely everyone by then, that an empire could not afford a third Emperor discovering the same door. His own scribes write the histories that follow.</p>""",
                "quote": "The capital fell not to chaos, but to correction.",
            },
            {
                "slug": "master-bai", "name": "Master Bai",
                "epithets": "Master of the Nine-Fold Mountain &middot; cultivator &middot; 66 years old",
                "teaser": "Forty years beneath a waterfall in pursuit of the True Yang Breath, and one open palm against a fish.",
                "bio_html": """<p>A cultivator of considerable and largely self-reported fame, who has spent forty years meditating beneath a waterfall in pursuit of the True Yang Breath and has grown, in that time, entirely convinced that no divine phenomenon can occur within his own generation without his personal involvement. When word of the Heavenly Thunder-Serpent reaches the Jianghu, he arrives barefoot at the court, addresses the tank in the ringing register cultivators reserve for audiences of one, and strikes the water with an open palm &mdash; the Heaven-Shattering Thunder Strike, qi against a fish.</p>
          <p>The eel answers with everything it has. His eyes roll back with an audible click several witnesses swear they heard from the second row; his beard, famous throughout three provinces and insured, by one account, against fire, vanishes in a bright, ozone-scented flash; and he folds to the marble. The court draws the wrong lesson entirely: the <a href="../characters/yongkang-emperor.html">Yongkang Emperor</a> will remember the singed beard as evidence rather than warning. Master Bai regrows the beard within two years and refuses to discuss the incident.</p>""",
                "quote": "Heaven and earth have their way. So has electricity.",
            },
            {
                "slug": "zhuo-sheng", "name": "Zhuo Sheng",
                "epithets": "Merchant &middot; 45 years old &middot; son of a tanner",
                "teaser": "Sells the nectar, the queue, and the numb arm &mdash; and pours it all into a canal the afternoon he sees where it leads.",
                "bio_html": """<p>A tanner's son who, within a year of the serpent's arrival, is running three separate operations: bottled river water sold to provincial nobles as <em>Genuine Nectar, Blessed at Source</em>; forged appointment tallies sold to heirs too impatient to wait their family's turn; and, for buyers who want the bragging rights of the burn without the indignity of the basin, a service in which hired substitutes stand in the queue and take the shock in their place. He makes in eight months more silver than his father the tanner made in forty years of honest work, and describes the period, later, to the two associates he trusts, as the finest and most fraudulent of his career.</p>
          <p>On the afternoon the Second Trial turns into a mass execution, he quietly empties his stock into the nearest canal, along with two crates of forged appointment tallies he judges, correctly, to have become considerably more incriminating than valuable. The silver outlives the empire.</p>""",
                "quote": "Merit is purchasable. Even the Thunder-Serpent can be traded.",
            },
            {
                "slug": "yun-wei", "name": "Yun Wei",
                "epithets": "Imperial Consort &middot; the first courtier to touch the water",
                "teaser": "Calls it the most wonderful pain of her life &mdash; and makes the basin fashionable.",
                "bio_html": """<p>It is not faith, strictly, that makes the first courtier volunteer a hand. It is ambition, wearing faith as a coat because the coat fits better in public. Consort Yun Wei, favored least by a duke who has never once looked at her directly, dips two fingers into the basin before the assembled court and receives, for her trouble, a jolt that snaps her wrist backward and leaves her whole arm numb through supper. She does not scream. She laughs, high and startled, and calls it the most wonderful pain of her life.</p>
          <p>Within a week every noblewoman at court who has heard the story secondhand is requesting an audience with the serpent as though it were a visiting dignitary rather than an eight-foot fish with an itch to defend its own tank. The shock becomes a tale, and the basin becomes fashionable. She will tell her granddaughters, decades later, in a country the old empire would no longer recognize, that she once touched Heaven with her bare hand, and none of them will ever learn what she actually touched.</p>""",
                "quote": "The current bit her, yet the court called it the dragon's kiss.",
            },
        ],
        "scenes": [
            {"slug": "the-net-meets-the-serpent",
             "alt": "A fisherman in a small boat hauls a net through churning white-blue water while a huge black serpent swirls beneath him, flooded stone gateways behind",
             "caption_html": """<a href="../characters/ren-duo.html">Ren Duo</a>'s net brushes the serpent's flank in the flooded ruins below Nine Bends."""},
            {"slug": "elder-peng-in-the-reeds",
             "alt": "A grey-bearded hermit in ragged robes sits among tall reeds while a fisherman kneels at the water's edge beside flooded stone pillars",
             "caption_html": """<a href="../characters/elder-peng.html">Elder Peng</a> watches from the reeds while <a href="../characters/ren-duo.html">Ren Duo</a> kneels at the water's edge."""},
            {"slug": "the-serpent-taken-alive",
             "alt": "Soldiers under red banners drag ropes across churning white water as a huge black serpent coils among flooded ruins",
             "caption_html": """Six men drown securing the serpent for the road to the capital &mdash; and no history remembers their names."""},
            {"slug": "the-basin-hall",
             "alt": "Courtiers in gold and crimson gather around a great round gilded basin, a dark serpent shape coiled in its water, a raised throne and banners beyond",
             "caption_html": """The court gathers around the water at Yujing, in the season when a turn beside it is the most coveted appointment east of the river."""},
            {"slug": "yun-wei-touches-the-water",
             "alt": "A consort in pale silk and gold hairpins reaches toward a gilded basin with her eyes closed as white lightning flickers across her fingers, courtiers watching behind her",
             "caption_html": """<a href="../characters/yun-wei.html">Consort Yun Wei</a> is the first courtier to touch the water &mdash; and calls it the most wonderful pain of her life."""},
            {"slug": "mei-suwen-and-the-ledger",
             "alt": "A young woman in pale robes writes in a small book by lantern light at a desk piled with scrolls and charts in a dark archive",
             "caption_html": """<a href="../characters/mei-suwen.html">Mei Suwen</a> keeps her ledger of the serpent's intervals in the archive, in a hand small enough to be mistaken for brocade."""},
            {"slug": "the-heaven-shattering-thunder-strike",
             "alt": "A white-bearded cultivator in flowing white robes strikes the water with an open palm as blue-white lightning bursts around him and courtiers draw back",
             "caption_html": """<a href="../characters/master-bai.html">Master Bai</a>'s Heaven-Shattering Thunder Strike: qi against a fish."""},
            {"slug": "the-gauntlets-the-night-before",
             "alt": "An elderly emperor in a lamplit study holds a small girl who wears an oversized golden gauntlet, a suit of ceremonial armor standing behind them",
             "caption_html": """The night before the Trial, <a href="../characters/yongkang-emperor.html">the Yongkang Emperor</a> lets <a href="../characters/wan-er.html">Wan-er</a> try on his gauntlets."""},
            {"slug": "the-solstice-ascension",
             "alt": "An emperor in gilded plate armor stands in a round basin with his arms flung wide as lightning runs across the steel, a crowd banked up around him beneath a blazing sun",
             "caption_html": """The Solstice Trial: <a href="../characters/yongkang-emperor.html">the Yongkang Emperor</a> raises his arms toward the sun as the current finds his armor."""},
            {"slug": "wan-er-outside-the-study",
             "alt": "A small girl in pale robes sits alone on the steps of a lantern-lit palace corridor beside an empty carved chair, a golden gauntlet on the floor near her",
             "caption_html": """<a href="../characters/wan-er.html">Wan-er</a> waits outside her grandfather's study, the evening no one comes to find her as usual."""},
            {"slug": "the-court-waits-in-ranks",
             "alt": "Dukes, generals and officials in ceremonial armor and silks stand in ranks along a marble terrace beside a great basin, red banners hanging overhead",
             "caption_html": """The summoned wait in ranks on the terrace for the Second Trial &mdash; attendance entirely voluntary."""},
            {"slug": "the-eleventh-entrant",
             "alt": "A young man in a dark wet robe stands waist-deep in a basin below a stepped terrace of stunned courtiers, a huge coiled serpent dark in the water beneath him",
             "caption_html": """The eleventh man to enter the Second Trial stands in the water a long, absurd moment, waiting for a judgment that does not arrive."""},
            {"slug": "the-western-postern",
             "alt": "A woman in a dark hooded cloak shelters a small girl against a palace gate wall at sunset as guards stand in the courtyard beyond",
             "caption_html": """<a href="../characters/mei-suwen.html">Mei Suwen</a> walks <a href="../characters/wan-er.html">Wan-er</a> to the western postern, three evenings out of every seven."""},
            {"slug": "the-second-ascension",
             "alt": "An emperor in dark gilded armor and a red cloak stands waist-deep in a basin while the palace burns behind him under a smoke-black sky",
             "caption_html": """<a href="../characters/yue.html">Emperor Yue</a> enters the water in his father's armor as Yujing burns."""},
            {"slug": "the-teahouse",
             "alt": "Two women sit across a low table with a teapot and cups in a lamplit teahouse, a window behind them opening on hills at sunset",
             "caption_html": """<a href="../characters/mei-suwen.html">Mei Suwen</a> and <a href="../characters/wan-er.html">Wan-er</a>, years later, in a teahouse two provinces west of Yujing &mdash; in the one account no chronicle confirms."""},
        ],
    },
    {
        "slug": "0188", "title": "The Songs Never Mention the Cats",
        "status": ["coming-soon"],
        "cover_file": "0188.jpg",
        "hook": "Arithmetic. Seven. Cats. A debt mistaken for a miracle. Filed.",
        "case_tag": "Case 0188",
        "pages": """~40 <span class="editor-note">(estimated from manuscript word count &mdash; confirm or edit)</span>""",
        "genre": """Literary Fiction &middot; Historical Fantasy &middot; War &amp; Military Fiction <span class="editor-note">(suggested &mdash; confirm or edit)</span>""",
        "synopsis_html": """<p>Empress Chandralekha dies in her twenty-eighth winter, and her husband, Emperor Dharmasena, kneels at her grave for seventeen consecutive nights until something red and green pushes up through the frost. The gardener who finds it calls it a miracle. The Cultivators, who left the bulb there themselves, call it Item 0188, Mythic Class, and wait to see what a grieving empire does with an excuse to believe in undying love.</p>
          <p>What it does is grow an economy. A trader who gives his name as <a href="../characters/somadatta.html">Somadatta</a> distributes the bulbs from a seed-stall that is really a Cultivator field post, and within a generation the flower once called Chandralekha's Vow &mdash; now <em>Anantavrata</em>, the Endless Vow &mdash; has become a wedding custom no family can afford to skip and no farmer can quite afford to refuse. Barley fields along the Shonavati turn to flowers one holding at a time; a bride gives up the cat that has slept against her ankles since childhood because a vow-flower needs the room a cat's dish would take; a court physician tests the bloom with a frame of temple bees and finds, to his quiet horror, that nothing living will go near it.</p>
          <p>The reckoning arrives as arithmetic, not omen: fewer fields of grain each year, a war fought over granaries already stripped bare, and rats nesting where the barley used to stand. By the time anyone adds up what the undying flower cost the ordinary, mortal people who grew it, the empress it was named for has been dead for decades &mdash; and the debt has already been filed away as a miracle. The songs, as ever, never mention the cats.</p>""",
        "catalyst": {
            "name": "The Eternal-Grief Lily", "meta": "Mythic Class",
            "page": "characters/the-eternal-grief-lily.html", "img": "characters/the-eternal-grief-lily-thumb.jpg",
            "html": """<p>A single undying, unpollinated flower, planted in an empress's grave and multiplied into a marriage custom, then a cash crop, then a famine.</p>""",
        },
        "envoy": {
            "name": "Somadatta", "meta": "Envoy Archetype 03",
            "page": "characters/somadatta.html", "img": "characters/somadatta-thumb.jpg",
            "html": """<p>Working Case 0188 under cover as a traveling seed-trader, distributing the bulbs that turn a private grief into an empire's economy &mdash; and quietly keeping the cats no one else wanted.</p>""",
        },
        "characters": [
            {
                "slug": "dharmasena", "name": "Dharmasena",
                "epithets": "Emperor of Amritavana &middot; Ninth of His Name &middot; Husband of Chandralekha",
                "teaser": "The emperor who knelt at his wife's grave for seventeen nights, and left an empire an excuse to believe in undying love.",
                "bio_html": """<p>Ninth of his name, and the only one of the nine remembered for a flower instead of a war. When <a href="chandralekha.html">Chandralekha</a> dies of a winter fever, Dharmasena visits her tomb nightly through the coldest month of the year, and on the fourth night presses a single bulb into the half-frozen ground &mdash; not knowing, and never later admitting he wondered, that the bulb had been left where he would find it.</p>
                <p>He watches the flower that grows from it become a name (<em>Chandralekha's Vow</em>), then a custom, then an industry he never ordered and cannot quite bring himself to end. When his gardener <a href="haridasa.html">Haridasa</a> asks, years later, whether the Emperor wants it removed, Dharmasena says only: let it stand. He dies before the worst of the arithmetic comes due, and is remembered, correctly, as a man whose private grief became public policy without a single decree ever being signed.</p>""",
                "quote": "A flower is mercy when it remains a dream. When it blooms in the world, it becomes a chain.",
            },
            {
                "slug": "chandralekha", "name": "Chandralekha",
                "epithets": "Empress of Amritavana &middot; Deceased &middot; Namesake of the Vow",
                "teaser": "Dead before the story proper begins, and the reason for everything that follows &mdash; a woman turned, without her consent, into a national myth.",
                "bio_html": """<p>Empress of Amritavana, dead of a winter fever before Case 0188 truly opens. Everything that happens afterward happens in her name and without her permission: a flower named for her grief, a custom built on her memory, and a fortune made from a vow she never made. Her husband <a href="dharmasena.html">Dharmasena</a> is the only person in the empire who seems to remember that the woman and the myth were never quite the same thing.</p>""",
                "quote": "Some loves do not end with death. They change form, and bloom in other worlds.",
            },
            {
                "slug": "haridasa", "name": "Haridasa",
                "epithets": "Palace Gardener &middot; Imperial Household of Amritavana",
                "teaser": "The gardener who found the bulb's first bloom, named it out of love, and had no idea what he'd started.",
                "bio_html": """<p>An aging palace gardener who tends <a href="chandralekha.html">Chandralekha</a>'s tomb as part of his ordinary rounds, and is the first person other than <a href="dharmasena.html">Dharmasena</a> to see the flower bloom. It's Haridasa, not the Emperor, who first calls it <em>Chandralekha's Vow</em> &mdash; a gardener's private sentiment that escapes the palace walls and becomes, within a season, the name of a national ritual of grief.</p>
                <p>He goes on tending it for decades, long after he's stopped being able to say for certain whether he still believes what he first said about it.</p>""",
                "quote": "The flower is a gift, not a thing to be removed. It is a sign &mdash; of love, of devotion, of her enduring memory.",
            },
            {
                "slug": "somadatta", "name": "Somadatta",
                "epithets": "Envoy of the Cultivators &middot; Envoy Archetype 03 &middot; the Trader",
                "teaser": "The field agent who sells grief back to the grieving, one bulb at a time, and keeps seven secret cats because someone has to.",
                "bio_html": """<p>Envoy Archetype 03, working Case 0188 under cover as a traveling seed-trader. Somadatta is the one who carries the flower out of the palace grounds and into the capital's wedding markets, and the one who watches &mdash; over years, then decades &mdash; as an emperor's private grief becomes a marriage custom, then agricultural policy, then a famine. His own field notes record the conversions, the refusals, and the slow disappearance of household cats with the same even hand.</p>
                <p>In the small rented room above his seed-stall, Somadatta keeps cats &mdash; five, then seven, by the case's fourth year &mdash; taken in from families who gave them up for the Vow. It is the one part of the file that isn't, strictly, part of the case. See the <a href="../lore/cultivator.html">Cultivator</a> entry for how his cover compares to other Envoys on file.</p>""",
                "quote": "The flower travels where people believe it will bring them closer to what they have lost.",
            },
            {
                "slug": "the-eternal-grief-lily", "name": "The Eternal-Grief Lily",
                "epithets": "Cultivator Designation: <em>Lilium Immortalis</em> &middot; Mythic Class &middot; Local Name: Anantavrata",
                "teaser": "A single, undying, unpollinated flower &mdash; Item 0188 &mdash; that no insect will touch and no family can resist.",
                "bio_html": """<p>Cultivator designation <em>Lilium Immortalis</em>, Mythic Class; filed locally as <em>Anantavrata</em>, the Endless Vow, after its earlier and more sentimental name, <em>Chandralekha's Vow</em>. Left in the frozen ground of an empress's grave by the Envoy <a href="somadatta.html">Somadatta</a>, it blooms without pollination, without scent, and without ever quite dying &mdash; a flower that court physician <a href="vaidyanatha.html">Vaidyanatha</a> tests with a frame of temple bees and finds nothing living will approach.</p>
                <p>It asks nothing of anyone. It is planted, gifted, purchased, and eventually grown as a cash crop in place of grain along the Shonavati, entirely on the strength of what people decide it means. See the <a href="../lore/catalyst.html">Catalyst</a> entry for how this compares to the rest of the case files.</p>""",
                "quote": "No bee has ever landed on it, and no bee ever will. That was never what it was for.",
            },
            {
                "slug": "vaidyanatha", "name": "Vaidyanatha",
                "epithets": "Court Physician of Kunjaravana",
                "teaser": "The physician sent to debunk a miracle, who instead files a report careful enough to later be misquoted for a war.",
                "bio_html": """<p>Sent from the rival kingdom of Kunjaravana to examine the flower on behalf of a king who assumes it's a fraud, Vaidyanatha instead spends three mornings watching temple bees refuse to land on it, and writes a report that is honest about what he doesn't understand. It is the most careful, most hedged document in the entire case file &mdash; and the one later generations strip of its hedges and repurpose as justification for a war he never advocated.</p>""",
                "quote": "The flower is not merely growing. It is progressing. And what progresses is not meant to be cut.",
            },
            {
                "slug": "kamalini", "name": "Kamalini",
                "epithets": "Bride of Amritavana &middot; Later, an Elderly Widow",
                "teaser": "A nineteen-year-old bride who receives a vow-flower as a wedding gift, and gives up the cat who slept at her ankles to make room for it.",
                "bio_html": """<p>Married at nineteen into a household that keeps an <em>Anantavrata</em> the way other families keep a household shrine. Her mother-in-law decides there isn't room in the house for both the flower and Kamalini's cat, <a href="dhumra.html">Dhumra</a>, and Kamalini &mdash; newly married, unwilling yet to make her first fight one worth losing &mdash; carries him to the kitchen door herself.</p>
                <p>She keeps the flower for the rest of her life, through widowhood and old age, and is never on record saying whether it was worth the trade.</p>""",
                "quote": "The Vow was for a life of abundance, they said. But in the end, it took even my cat.",
            },
            {
                "slug": "dhumra", "name": "Dhumra",
                "epithets": "Grey Cat &middot; Companion to Kamalini",
                "teaser": "The cat given up for a flower &mdash; the one cost of the Vow small enough for the histories to leave out entirely.",
                "bio_html": """<p>A grey domestic cat who sleeps against <a href="kamalini.html">Kamalini</a>'s ankles every winter of her unmarried life, and is given away on her mother-in-law's orders to make room for a vow-flower that needs no room at all. Case 0188's records are unusually attentive, for a Cultivator file, to what became of him afterward &mdash; which is more than can be said for most of what the Vow quietly cost.</p>""",
                "quote": "He slept against her ankles every winter of her unmarried life.",
            },
            {
                "slug": "govinda", "name": "Govinda",
                "epithets": "Farmer Along the Shonavati &middot; Father of a Daughter Nearing Marriage",
                "teaser": "A grain farmer who plows his own barley under rather than let anyone else do it, and tells himself it was his decision.",
                "bio_html": """<p>A farmer along the Shonavati with a daughter approaching marriageable age, and so a dowry to consider. Govinda holds out against Vow-cultivation longer than most of his neighbors, then plows his own barley field under with his own hands rather than let a seed-broker's crew do it for him &mdash; a distinction that seems to matter more to him than to anyone watching.</p>""",
                "quote": "The earth gives enough, if you do not sell your soul to the flower.",
            },
            {
                "slug": "bhadraka", "name": "Bhadraka",
                "epithets": "Farmer Along the Shonavati &middot; the Man Who Refused",
                "teaser": "One of the last grain farmers left on the river, who turns down the bulbs every time they're offered and pays for it in a broken betrothal.",
                "bio_html": """<p>A farmer along the Shonavati and one of the very few who never converts a single field to Vow-cultivation, even after his daughter's betrothal is withdrawn over it. When the Envoy <a href="somadatta.html">Somadatta</a> offers him bulbs directly, Bhadraka refuses without raising his voice, and goes on refusing for the rest of the case file. What grain the river valley has left by the time of the famine, it has largely because men like him didn't sell it off in advance.</p>""",
                "quote": "I have no daughter left to dower, and no wife who will not know why I bought it. Keep your bulbs.",
            },
            {
                "slug": "dhanapala", "name": "Dhanapala",
                "epithets": "Merchant &middot; Grain-Futures Trader of the Capital",
                "teaser": "The merchant who reads the coming famine in his own ledgers years early, and profits from it instead of warning anyone.",
                "bio_html": """<p>A grain-futures trader in the capital who reads the numbers &mdash; fewer barley contracts, more Vow-bulb orders &mdash; years before anyone else calls it a pattern, and positions himself to profit from the shortage rather than to prevent it. Dhanapala isn't a villain by his own account, only a man who understood the arithmetic sooner than his customers did.</p>""",
                "quote": "Grain moves the realm. Numbers tell you when people cannot see.",
            },
            {
                "slug": "ravisena", "name": "Ravisena",
                "epithets": "Son of Dharmasena &middot; Regent, Later Emperor of Amritavana",
                "teaser": "The son who inherits both an empire and its flower, and has to decide what an undying vow is worth to the living.",
                "bio_html": """<p>Son of <a href="dharmasena.html">Dharmasena</a> and <a href="chandralekha.html">Chandralekha</a>, regent and later Emperor of Amritavana in his own right. Ravisena inherits the Vow along with the throne, and with it the accumulated arithmetic of what his father's grief has cost a generation of farmers, brides, and cats. What he does with that inheritance closes out Case 0188's imperial thread.</p>""",
                "quote": "The empire endures, not because we did not fall, but because we remember what we are.",
            },
        ],
        "scenes": [
            {"slug": "the-fourth-night", "alt": "Dharmasena kneeling at Chandralekha's grave at night, planting a single bulb",
             "caption_html": "On the fourth night, Dharmasena presses a single bulb into his wife's grave and tells no one why."},
            {"slug": "the-seventeenth-visit", "alt": "Dharmasena kneeling in grief before a snow-covered tomb",
             "caption_html": "By the seventeenth visit, the Emperor's composure finally fails him."},
            {"slug": "let-it-stand", "alt": "Dharmasena and Haridasa beside the blooming grave-flower in winter",
             "caption_html": "Asked whether the flower should be removed, Dharmasena says only: let it stand."},
            {"slug": "somadatta-in-the-capital", "alt": "Somadatta selling flower bulbs at a crowded capital market",
             "caption_html": "The trader who calls himself Somadatta sells the empire's newest custom one bulb at a time."},
            {"slug": "the-bees-that-would-not-land", "alt": "Vaidyanatha testing the flower with a frame of temple bees",
             "caption_html": "Three mornings, one frame of temple bees, and not a single insect willing to land."},
            {"slug": "kamalini-gives-up-dhumra", "alt": "Kamalini holding her cat Dhumra as her mother-in-law looks on",
             "caption_html": "A vow-flower needs no room at all, and somehow there still isn't room for the cat."},
            {"slug": "seven-cats-above-the-seed-stall", "alt": "Somadatta surrounded by seven cats in his room above the seed-stall",
             "caption_html": "Above the seed-stall that is really a Cultivator field post, an Envoy keeps the one part of the case that isn't, strictly, the case."},
            {"slug": "govinda-plows-it-under", "alt": "Govinda plowing under his barley field beside a seed-broker",
             "caption_html": "Govinda converts his own barley field rather than let a broker's crew do it for him."},
            {"slug": "bhadraka-keeps-his-bulbs", "alt": "Somadatta offering bulbs to Bhadraka, who refuses",
             "caption_html": "Offered the bulbs directly, Bhadraka refuses without raising his voice."},
            {"slug": "the-year-everyone-was-rich", "alt": "A crowded wedding market in the empire's most prosperous year",
             "caption_html": "In the year everyone was rich, three couples buy a bulb inside the same hour."},
            {"slug": "the-granary-of-rats", "alt": "A ravaged granary overrun with rats, an Anantavrata growing in the ruin",
             "caption_html": "The Vow's own roots turn out to be adequate eating, for whatever is left in an empty granary."},
            {"slug": "a-bride-generations-later", "alt": "A bride carrying an Anantavrata down the aisle at her wedding",
             "caption_html": "Generations on, a bride carries an Anantavrata down the aisle, and no one remembers why."},
        ],
    },
    {
        "slug": "2140", "title": "The Third Grain",
        "status": ["coming-soon"],
        "cover_file": "2140.jpg",
        "hook": "Grain. Tolerance. Grace. Arithmetic. Bread.",
        "case_tag": "Case 2140",
        "pages": EDITOR_PAGES,
        "genre": EDITOR_GENRE,
        "synopsis_html": EDITOR_SYNOPSIS,
        "envoy": {
            "name": "Observer 419", "meta": "Itinerant Clockmaker",
            "page": "characters/observer-419.html", "img": "characters/observer-419-thumb.jpg",
            "html": """<p>A field agent of the Cultivators, deployed to the county of Vardane under cover as a traveling clockmaker. He replaces a single worn axle-joint with an unremarkable grey sphere during one night's hospitality, refuses every offer of further help, and is gone on foot three days later &mdash; forgotten the way useful strangers generally are. The wheel is not.</p>""",
        },
        "characters": [
            {
                "slug": "garibald", "name": "Garibald",
                "epithets": "Count of Vardane &middot; 31 when the clockmaker comes",
                "teaser": "Shelters a stranger for a night's lodging, and spends the rest of his life discovering exactly what that hospitality cost and bought him.",
                "bio_html": """<p>Count of Vardane, a man who made peace with arithmetic before he made peace with anything else, and keeps his own ledgers in a hand precise enough to embarrass his clerks. He shelters a traveling stranger &mdash; one of dozens he's sheltered that year without asking much beyond honesty about their business &mdash; and the man installs a single dull grey sphere in the county mill before vanishing three days later. When <a href="../characters/landulf.html">Baron Landulf</a> files a legal claim on the strength of it, Garibald offers no defense, on the private theory that a truth he can't prove would only make the loss look like a lie besides, and breaks down completely at his family's seat, Ostrevenna &mdash; the first time anyone has ever seen him do so.</p>
          <p>He sets exactly one condition on House Ratchis reclaiming the mill for him: that it cost <a href="../characters/landulf.html">Landulf</a> nothing beyond what the war his own claim set in motion has already cost him. He returns to Vardane five years later to a wheel still turning, a miller two winters dead, and a set of questions about the clockmaker's real purpose that his own private notes never quite answer.</p>""",
                "quote": "Keep the ledger current.",
            },
            {
                "slug": "observer-419", "name": "Observer 419",
                "epithets": "Envoy/Observer, Case 2,140 &middot; publicly an itinerant clockmaker",
                "teaser": "Installs a single unremarkable sphere in a failing county mill, then disappears before anyone thinks to ask his name twice.",
                "bio_html": """<p>A field agent of the <a href="../lore/cultivator.html">Cultivators</a>, deployed to Vardane disguised as a traveling clockmaker with nothing more remarkable about him than a satchel of pocket chronometers. <a href="../characters/garibald.html">Count Garibald</a> shelters him for a night's lodging before asking a single question about his business &mdash; a courtesy no prior posting has required of him, and which his own field note admits, against protocol, he was not required to find noteworthy, and did. He replaces one worn axle joint with a single dull grey sphere, refuses every offer of help, and leaves three days later on foot, forgotten the way useful strangers generally are. The wheel is not. He is posted next, as a clockmaker again, to <a href="../characters/observer-419-1153.html">Case 1153</a>.</p>""",
                "quote": "Introduce. Observe. Withdraw before attachment becomes measurable.",
            },
            {
                "slug": "teudis", "name": "Teudis",
                "epithets": "Miller of Vardane's county mill &middot; inherited the post, and his father's bad knees",
                "teaser": "Keeps a private tally of the wheel's working days for years, then watches an old debt forgive itself in a single winter.",
                "bio_html": """<p>The broad, uncomplaining miller of Vardane's county mill, who inherited the position along with his father's bad knees and had kept, for years before the clockmaker ever arrived, a private tally of exactly how many days each winter the wheel turned at all &mdash; a number he never once told <a href="../characters/garibald.html">Count Garibald</a>, suspecting correctly that the Count already knew it better than he did. He holds the precision bearing himself before <a href="../characters/observer-419.html">Observer 419</a> installs it, cold in his palm on a night beside a working forge, and it's his own tavern telling of that visit, embellished the way an unbelievable truth requires, that eventually gives the county its name for what changed the mill: the Third Grain.</p>
          <p>Conscripted in the war his own good fortune helps start, he comes home eleven months later missing the two smallest fingers of his left hand and goes straight back to the mill anyway. He dies two winters before the Count returns, having made his sister repeat back to him three times the one fact he considered worth reporting.</p>""",
                "quote": "Tell him the mill never once stopped running. Not for a single day. Hand or no hand.",
            },
            {
                "slug": "garibalds-mother", "name": "Garibald's Mother",
                "epithets": "Deceased &middot; mother of Count Garibald",
                "teaser": "A final illness Garibald nurses alone becomes the private grief the whole county learns never to mention above a murmur.",
                "bio_html": """<p>Dead well before the clockmaker ever reaches Vardane, tended through her final illness by <a href="../characters/garibald.html">Garibald</a> alone &mdash; a grief that costs him, by his own private reckoning, the best courting years of his life, and leaves him no longer much interested in beginning again. The county discusses it, when it discusses it at all, above nothing louder than a murmur.</p>""",
                "quote": None,
            },
            {
                "slug": "landulf", "name": "Landulf",
                "epithets": "Baron of Verrasco &middot; 19 at his inheritance",
                "teaser": "Files a legal claim over a neighbor's good fortune, wins exactly what he asked for, and spends the rest of his life learning what it actually cost.",
                "bio_html": """<p>Baron of Verrasco, who inherited the barony at nineteen when his older brother <a href="../characters/ansfrid.html">Ansfrid</a> fell from a lathered horse during a boar hunt, and governs competently &mdash; a word, he comes to understand, people use about a man precisely when they mean to withhold something larger. He watches Vardane's fortunes climb for three years with a patience he'd call arithmetic rather than envy, and finally files a formal claim under the Writ of Undeclared Grace: not sorcery, not any crime the Threefold Crown has a name for, only an oversight any honest man might make. He wins. Holding the bearing alone afterward in a locked room, he feels not triumph but the particular cold of a man who has just proven his own accusation correct.</p>
          <p>He tells no one what his own smith found, quietly exempts whole villages from the war's levy where he can justify it as necessity rather than mercy, and writes a confession to <a href="../characters/garibald.html">Garibald</a> he never learns went unanswered by design rather than indifference. He dies without ever suspecting House Ratchis engineered the claimant that took the mill back from him.</p>""",
                "quote": "I am not accusing the Count of a crime, only of an oversight any honest man might make, and asking that the law correct it as the law was written to do.",
            },
            {
                "slug": "gisela", "name": "Gisela",
                "epithets": "Baron Landulf's daughter &middot; 17 at her introduction",
                "teaser": "Reads her father's ledgers closely enough to understand exactly what his ambition has cost her, and chooses her own marriage rather than let him choose a second time.",
                "bio_html": """<p>Daughter to <a href="../characters/landulf.html">Baron Landulf</a>, clever in the patient, arithmetical way of a girl who has read her father's ledgers long enough to know exactly what a good marriage costs and how far short of it Verrasco's revenues fall. Watching her weigh those numbers, more than watching his neighbor's granaries fill, is what finally moves her father's private suspicion into a legal claim.</p>
          <p>When the war his ambition starts costs him nearly everything else, she tells him plainly that she watched him gamble a mill for her future and lose them both in the same three years, and chooses her own lesser house herself rather than let him choose worse for her a second time. He lets her.</p>""",
                "quote": None,
            },
            {
                "slug": "ansfrid", "name": "Ansfrid",
                "epithets": "Heir to Verrasco, implied &middot; Landulf's older brother",
                "teaser": "Dies on a boar hunt neither brother much wanted to attend, and makes Landulf a Baron at nineteen by falling from a horse.",
                "bio_html": """<p>The older brother <a href="../characters/landulf.html">Baron Landulf</a> never expected to inherit past, thrown from a lathered horse during a boar hunt neither of them had much wanted to attend. His fall ends one story before it starts another: a boyhood Landulf had spent entirely assuming a barony would never be his to swear an oath over.</p>""",
                "quote": None,
            },
            {
                "slug": "grimoald", "name": "Grimoald",
                "epithets": "Duke of Trevano &middot; 46 when the rumor reaches him",
                "teaser": "Sends an engineer to investigate a rumor out of a boyhood shame he's never told a soul, and ends up arming a continent instead.",
                "bio_html": """<p>Duke of Trevano, who wanted, as a boy, to fix his grandmother's chiming clock in secret with tools stolen from the household smith, and never told anyone &mdash; not his father, not his wife, not one of the engineers he'd go on to employ by the dozen &mdash; that he'd failed. When a badly garbled rumor of a Verrasco mill reaches him at forty-six, he sends his engineer <a href="../characters/gisulf.html">Gisulf</a> to look, report honestly, and touch nothing without permission, and thinks, that first evening, not of siege engines but of a clock he never managed to fix.</p>
          <p>Two years of failing to reproduce the bearing leave Trevano with something else entirely: lathes, measurement, and metalworkers trained to a precision no duchy has previously demanded. He gives the order to turn it toward siege engines three days after <a href="../characters/gisulf.html">Gisulf</a> names what they've actually built, and spends the rest of his life uncertain whether those three days were deliberation or merely decency's minimum interval before doing what he'd already decided. He keeps his duchies, and a personal workshop of precision tools he never once touches himself.</p>""",
                "quote": None,
            },
            {
                "slug": "gisulf", "name": "Gisulf",
                "epithets": "Engineer in Duke Grimoald's service &middot; twice told him a design would fail, and was right both times",
                "teaser": "Spends three sleepless nights confirming a rumor, then spends two years turning the failure to copy it into something considerably worse.",
                "bio_html": """<p><a href="../characters/grimoald.html">Grimoald</a>'s engineer, trusted for the rare reason that he has twice told the Duke a design would fail and been right both times. Sent to look at Verrasco's mill, report honestly, and touch nothing without permission, he touches nothing &mdash; and doesn't sleep for three nights afterward, which he considers, privately, sufficient permission of its own. His eleven-page report reaches one conclusion: a tolerance nothing in Trevano's armories can presently match.</p>
          <p>He never reproduces the bearing itself; every imitation opened past a certain depth seizes and goes inert. What his workshop builds instead, failing patiently and expensively for two years, is the capability to measure and match precision from the outside &mdash; lathes, gauges, metalworkers trained to a standard no apprenticeship had previously required. Demonstrating a trebuchet joint machined to that standard, he's the one who finally says the sentence Grimoald spends three days pretending to deliberate over.</p>""",
                "quote": "A joint that fails less often, under less maintenance, through worse weather, is not a better mill part. It is a better war.",
            },
            {
                "slug": "grimoalds-father", "name": "Grimoald's Father",
                "epithets": "Lombard collector &middot; died in his 60s",
                "teaser": "Buys his young son a Frankish chiming clock at absurd expense, and never once has it repaired.",
                "bio_html": """<p>A collector with a heavyset, acquisitive self-satisfaction, known to <a href="../characters/grimoald.html">Grimoald</a> mainly through a single anecdote: a Frankish chiming clock bought at absurd expense for his son and never once taken to be fixed, which the boy would go on to attempt himself, in secret, and fail at, without ever once telling his father why it mattered.</p>""",
                "quote": None,
            },
            {
                "slug": "grimoalds-wife", "name": "Grimoald's Wife",
                "epithets": "Wife of Duke Grimoald &middot; early-to-mid 50s",
                "teaser": "Listens in silence to a court she was raised for, and is never once told the one story that would explain her husband's fascination with precision.",
                "bio_html": """<p>Duke Grimoald's wife, slender and dignified, composed by the same court training that shaped every feature of her bearing. She listens in silence as <a href="../characters/grimoald.html">Grimoald</a> speaks of the war his workshops have made possible, one of the very few people close enough to him to have noticed the personal workshop he never lets anyone touch &mdash; and, like everyone else in his life, never once told why.</p>""",
                "quote": None,
            },
            {
                "slug": "adelrada", "name": "Adelrada",
                "epithets": "Elder of House Ratchis &middot; 78 years old",
                "teaser": "Watches a man who never once broke over his own mother's death come apart over a mill, and spends two years quietly finishing a sum nobody else knows she's counting.",
                "bio_html": """<p>Elder of House Ratchis, spare and upright at seventy-eight, with the ink-stained fingers of a woman who has kept her own ledgers for decades. She isn't moved by <a href="../characters/landulf.html">Landulf</a>'s legal claim on Vardane's mill so much as by what it does to <a href="../characters/garibald.html">Garibald</a> &mdash; a man she has watched grieve quietly and competently his whole life, breaking, for the first time she's ever seen, at her own table at Ostrevenna. She sends the ruling to her notary <a href="../characters/vitalis.html">Vitalis</a> rather than accept a summary of it, and spends two years afterward keeping a private accounting nobody else is shown: what the mill's loss once cost Garibald, weighed against what its keeping has since cost Landulf.</p>
          <p>She acts only once the sum finally closes &mdash; on Landulf's own unsent confession, not on any House vote &mdash; instructing <a href="../characters/vitalis.html">Vitalis</a> to find an unconnected claimant, and quietly withdrawing House Ratchis's reach from Duke Grimoald's war until the mill returns to Vardane exactly as quietly as it left. She dies eleven years later in her own bed. Her great-nephew <a href="../characters/ranulf.html">Ranulf</a> finds the ledger afterward, and is the only person who ever learns what she'd actually been counting.</p>""",
                "quote": None,
            },
            {
                "slug": "vitalis", "name": "Vitalis",
                "epithets": "Notary retained by House Ratchis &middot; 55 years old",
                "teaser": "Reads a legal ruling three times, then reports a debt rather than a scandal &mdash; and charges his standard fee either way.",
                "bio_html": """<p>A notary House Ratchis has kept on retainer for years and trusted for exactly one reason: he has never once told <a href="../characters/adelrada.html">Elder Adelrada</a> what he suspected she wanted to hear. Asked to review the ruling that hands <a href="../characters/garibald.html">Garibald</a>'s mill to Verrasco, he reads the Writ of Undeclared Grace three times and reports, without any apparent alarm, that it rests on a four-generation-dormant precedent that could pry loose a great deal more than a mill, given the right claimant and enough patience.</p>
          <p>Two years later, given an instruction rather than a question, he finds that claimant within the fortnight &mdash; a minor cousin of a minor cousin, chosen specifically for how little the choice would ever need explaining.</p>""",
                "quote": "For the reading, I charge the standard fee.",
            },
            {
                "slug": "ranulf", "name": "Ranulf",
                "epithets": "Member of House Ratchis &middot; Elder Adelrada's great-nephew &middot; 26",
                "teaser": "Argues loudest for allying with a Duke who could remake armories from a single mill part, then spends an afternoon learning what his great-aunt was actually counting.",
                "bio_html": """<p>Elder <a href="../characters/adelrada.html">Adelrada</a>'s great-nephew, lean and impatient with a House that has spent eight generations being clever instead of powerful. When Duke Grimoald's rise splits House Ratchis's council, he argues loudest for allying with the Duke outright, a position his great-aunt hears out along with the rest without ever once showing which way her own mind is bending.</p>
          <p>Three days after her funeral, going through her papers alone because no one else has volunteered for it, he finds the private ledger she kept his whole life a secret from &mdash; not the House's usual accounts of reach and marriages and debts, but two long columns of ordinary, specific losses, kept level against each other for eleven years. He is the only person who ever learns what she was actually counting.</p>""",
                "quote": "Caution has kept us safe for generations. But safety is not the same as a future.",
            },
            {
                "slug": "eldest-witness-of-the-writ", "name": "Eldest Witness of the Writ",
                "epithets": "Witness of the Writ &middot; senior-most of the clerical judges",
                "teaser": "Presides over the hearing that hands a Count's mill to his neighbor, and can't stop glancing at a painted ceiling he's complained about for thirty years.",
                "bio_html": """<p>The senior-most of the clerical judges who hear <a href="../characters/landulf.html">Landulf</a>'s claim against <a href="../characters/garibald.html">Garibald</a>'s mill, presiding beneath a painted ceiling depicting Auron weighing three golden scales that have never quite balanced in the artist's rendering &mdash; a detail he's complained about for thirty years and will go on complaining about for several more. The ruling takes his court less than an hour to reach and considerably longer to read aloud, the witnesses of the Writ being men who love procedure roughly as much as they love Auron himself.</p>""",
                "quote": None,
            },
        ],
        "scenes": [],
    },
    {
        "slug": "3115", "title": "The Listening Water",
        "status": ["coming-soon"],
        "cover_file": "3115.jpg",
        "hook": "Reckoning. Rationed. Witnessed. Roster. Closed.",
        "case_tag": "Case 3115",
        "catalyst": {
            "name": "The Listening Water",
            "meta": "High-Concept, Cultural and Social",
            "page": "characters/the-listening-water.html",
            "img": "characters/the-listening-water-thumb.jpg",
            "html": "<p>A stoppered glass bottle holding five measured sips of plain-seeming water. One sip grants its drinker fifteen minutes of understanding &mdash; never speech, never command &mdash; of the perception of nearby animals, after which the effect lapses without residue or memory-loss.</p>",
        },
        "envoy": {
            "name": "Observer 471",
            "meta": "&ldquo;the Salt-Root Woman&rdquo;",
            "page": "characters/observer-471.html",
            "img": "characters/observer-471-thumb.jpg",
            "html": "<p>Poses as an itinerant herbalist and peddler in Jinlu, and sells four crates of ordinary trade stock &mdash; the bottle among them &mdash; to a palace under-steward without ever learning whose hands it would reach.</p>",
        },
        "pages": EDITOR_PAGES,
        "genre": EDITOR_GENRE,
        "synopsis_html": EDITOR_SYNOPSIS,
        "characters": [
            {
                "slug": "huairen", "name": "Huairen",
                "epithets": "King of Qinghe &middot; forty-one years on the throne &middot; 79 years old",
                "teaser": "Learns, on his own deathbed, exactly whose son he raised &mdash; and asks the realm to remember only that the boy was loved.",
                "bio_html": """<p>King of Qinghe for forty-one years, and by the novel's opening already visibly diminished by an illness that turns out, far too late for anyone to act on it, to be <a href="../characters/cao.html">Cao</a>'s own slow, measured dosing rather than age alone. He keeps <a href="../characters/xiaobao.html">Xiaobao</a> curled against him through most of his final months, and it is the dog's own fear of a familiar step that eventually hands <a href="../characters/mingxuan.html">Mingxuan</a> the pattern no human witness would give him.</p>
              <p>Whatever he comes to understand about Queen <a href="../characters/meilan.html">Meilan</a>, Prince <a href="../characters/huaiyu.html">Huaiyu</a>, and the true parentage of the son the Father's Reckoning has already made legally his own, he takes the last sip of <a href="../characters/the-listening-water.html">the Listening Water</a> from Mingxuan's own hand and spends it not on confrontation but on a final instruction, delivered to the room rather than to any one person in it: tell them the boy is loved, and tell them nothing else.</p>""",
                "quote": "Tell them the boy is loved. Tell them nothing else.",
            },
            {
                "slug": "meilan", "name": "Meilan",
                "epithets": "Queen of Qinghe &middot; 30 years old &middot; later Regent",
                "teaser": "Chooses, in the only way left to her, by declining to choose otherwise &mdash; and spends the rest of her life quietly paying for what that choice cost.",
                "bio_html": """<p>Queen of Qinghe for nine years before the novel opens, and the one person in Jinlu who understands exactly what the Father's Reckoning is worth: it makes Prince Jiyun her husband <a href="../characters/huairen.html">Huairen</a>'s legal son the moment <a href="../characters/peizhi.html">Warden Peizhi</a> records it, whatever the truth of his conception with <a href="../characters/huaiyu.html">Huaiyu</a> happens to be. She spends the entire novel protecting that single piece of paper, by whatever quiet, unglamorous means the household affords a woman who cannot be seen to act at all.</p>
              <p>When <a href="../characters/suyin.html">Suyin</a>'s accidental knowledge threatens to undo it, Meilan has <a href="../characters/chunhui.html">Chunhui</a> gently questioned rather than raise her own voice once, and the household's quieter instruments &mdash; <a href="../characters/cao.html">Cao</a>'s, Chancellor <a href="../characters/jian.html">Jian</a>'s &mdash; do the rest without her ever giving a documented order. She rules as Regent once the throne is hers to hold, outlives every man who did the actual killing on her behalf, and marks the one debt she can never openly repay by quietly doubling, every season, an anonymous stipend to a dead maid's brother who has no idea whose money it is.</p>""",
                "quote": "I chose, the only way I could: by declining to choose otherwise.",
            },
            {
                "slug": "huaiyu", "name": "Huaiyu",
                "epithets": "Prince, half-brother to King Huairen &middot; March-Lord of Beiyan &middot; 38 years old",
                "teaser": "Keeps a soldier's chest packed with an infant's cap he was never allowed to claim, and dies at a ford still not knowing his son survived him.",
                "bio_html": """<p>Half-brother to King <a href="../characters/huairen.html">Huairen</a> and March-Lord of the frontier at Beiyan &mdash; a prince by blood who built his whole adult identity on being a soldier by choice instead. His affair with Queen <a href="../characters/meilan.html">Meilan</a> produces the one child neither of them can ever publicly claim: Prince Jiyun, sealed to the throne as Huairen's own son by <a href="../characters/peizhi.html">Warden Peizhi</a>'s Reckoning before Huaiyu is ever told the boy exists as anything other than the King's heir. He keeps an infant's cap in his own campaign chest for the rest of his life, and tells no one what it means.</p>
              <p>When the throne he never contested becomes something worth fighting over anyway, he leads the faction that will not accept Chancellor <a href="../characters/jian.html">Jian</a>'s account of the old King's death, and dies at the second autumn's crossing of the Shuang ford, shot by <a href="../characters/the-soldier-who-killed-huaiyu.html">a seventeen-year-old soldier</a> of the Queen's own garrison who believes, to his own dying day, that he has struck down a traitor rather than the father of the child that garrison exists to protect.</p>""",
                "quote": "A prince by blood, a soldier by choice.",
            },
            {
                "slug": "the-listening-water", "name": "The Listening Water",
                "epithets": "A Stoppered Glass Bottle, Five Measured Sips &middot; the Catalyst of Case 3115",
                "teaser": "Grants fifteen minutes of another creature's own perception, never its speech or its obedience &mdash; and asks nothing back for the privilege.",
                "bio_html": """<p>A single stoppered glass bottle, plain and unmarked, holding five individually measured sips of water indistinguishable from any other by taste, smell, or any test available in Qinghe. One sip grants its drinker fifteen minutes of a nearby animal's own perception &mdash; never its speech, never its command &mdash; after which the effect lapses without residue or memory-loss. It is introduced into Qinghe as ordinary trade stock by <a href="../characters/observer-471.html">Observer 471</a>, and never once reclaimed.</p>
              <p>Four of its five sips are used deliberately &mdash; by <a href="../characters/mingxuan.html">Mingxuan</a> twice, by <a href="../characters/yancheng.html">Yancheng</a> once, and by King <a href="../characters/huairen.html">Huairen</a> himself on his own deathbed &mdash; while the first is spent by <a href="../characters/suyin.html">Suyin</a> entirely by accident. Qinghe's own soldiers, knowing only rumor of it by the war's end, have already begun mythologizing it as &ldquo;the god-water&rdquo; long before the emptied bottle is kept, quietly, as somebody's private keepsake.</p>""",
                "quote": "Understanding, not command; borrowed, not kept.",
            },
            {
                "slug": "suyin", "name": "Suyin",
                "epithets": "Maid in Queen Meilan's Household &middot; third year of service &middot; 20 years old",
                "teaser": "Drinks what she thinks is spilled water, and spends her last fifteen minutes of understanding on a caged bird that knows more than she does.",
                "bio_html": """<p>A maid in Queen <a href="../characters/meilan.html">Meilan</a>'s household, in her third year of service and unremarkable by every court standard except a habitual watchfulness she never quite leaves off duty. A small private ritual is the only real extravagance anyone would find if they looked: a jar of coins counted by candlelight each new moon, not for the money so much as for the pleasure of watching a number grow.</p>
              <p>She drinks what she assumes is a spilled mouthful of ordinary water while tending the Queen's caged moon-finch, and spends the next fifteen minutes understanding, through the bird's own memory, exactly what it has watched happen in that room for longer than she has served in it. She tells no one before she is found dead on the covered bridge at dawn, the fall recorded as an accident by a physician who is never given reason to look closer.</p>""",
                "quote": "Not for the money. For the pleasure of watching a number grow.",
            },
            {
                "slug": "mingxuan", "name": "Mingxuan",
                "epithets": "Court Alchemist to King Huairen &middot; 44 years old &middot; later of the peace council under the Jinlu Concord",
                "teaser": "Measures out his own sip of a stranger's water to verify what it does, and spends the rest of his life wishing he'd measured wrong.",
                "bio_html": """<p>Court Alchemist to King <a href="../characters/huairen.html">Huairen</a>, and the one man in Jinlu who treats a servant's fright as a question rather than an inconvenience. When <a href="../characters/suyin.html">Suyin</a> is brought to him shaking and unable to say why, he listens to her account of an overheard truth she cannot possibly have overheard, and instead of dismissing it, measures out one of the four remaining sips himself &mdash; not to help her, he tells himself, but to know precisely what he is dealing with. It works exactly as she described: fifteen minutes of a nearby animal's own perception, then nothing, no residue, no memory of having granted it at all.</p>
              <p>He carries that same discipline &mdash; verify, then act &mdash; through everything that follows, including the slow poisoning he eventually traces through <a href="../characters/xiaobao.html">Xiaobao</a>'s own fear of a steward's step, and gives the King the last sip in his own hand rather than anyone else's, on the night Huairen dies. Chancellor <a href="../characters/jian.html">Jian</a> recasts the whole investigation as Mingxuan's own coup dressed as medicine, and <a href="../characters/duan.html">Duan</a> gets him out of Jinlu ahead of the arrest that never quite catches him. He signs the Jinlu Concord as a member of the peace council twenty-six years later, and near the very end of his life answers a village scribe's apprentice's one honest question about a bottle that could speak to birds &mdash; then lets the boy write down neither the question nor his answer.</p>""",
                "quote": "A man who does not keep his own accounts has no business auditing a kingdom's.",
            },
            {
                "slug": "cao", "name": "Cao",
                "epithets": "Steward to Queen Meilan's Household &middot; 52 years old",
                "teaser": "Spends nine years of quiet, competent service measuring out a king's medicine &mdash; and, for months, something else besides.",
                "bio_html": """<p>Steward to Queen <a href="../characters/meilan.html">Meilan</a>'s household for nine years, and the kind of servant a great house is built to stop noticing: plain robes, an unhurried step, a medicine kit at his belt that no one ever asks to see opened. He measures out King <a href="../characters/huairen.html">Huairen</a>'s dose himself, night after night, with the same steady hand he uses for every other household errand, and tells his interrogators afterward that he had never in nine years of service done anything the Queen's household had not, in some fashion, already wanted done.</p>
              <p>He confesses the whole of it to <a href="../characters/duan.html">Duan</a>'s questioning once <a href="../characters/mingxuan.html">Mingxuan</a>'s suspicions finally catch him, and Chancellor <a href="../characters/jian.html">Jian</a> has him executed within the same day &mdash; not for the poisoning itself, but for how little time it would have taken him to name who else knew.</p>""",
                "quote": "He moves like a shadow in a house of silk and power &mdash; always present, never seen.",
            },
            {
                "slug": "duan", "name": "Duan",
                "epithets": "Chamberlain of the Jinlu Court &middot; 83 years old &middot; served three kings before Huairen",
                "teaser": "Has never once given the King's Guard cause to question his word, and spends the last use of that trust smuggling out the one man the court wants silenced.",
                "bio_html": """<p>Chamberlain of the Jinlu court, and old enough to have served three kings before a crown ever sat on <a href="../characters/huairen.html">Huairen</a>'s own head. Forty years of never once being questioned by the King's Guard is not an accident; it is the entire instrument he spends on <a href="../characters/mingxuan.html">Mingxuan</a>'s behalf, walking him past men who would stop anyone else, on the strength of a reputation he has spent decades not spoiling with a single lie.</p>
              <p>He uses that same reputation once more, and for the last time, to get Mingxuan out of Jinlu ahead of Chancellor <a href="../characters/jian.html">Jian</a>'s version of events &mdash; a debt on forty years of quiet composure that he pays without visibly changing expression. What it costs him afterward, the record doesn't say; only that he is still alive, and still trusted, when the Jinlu Concord is signed.</p>""",
                "quote": "No guard in forty years has ever questioned my word. I have never once given them cause to start.",
            },
            {
                "slug": "jian", "name": "Jian",
                "epithets": "Chancellor &middot; Queen Meilan's Chief Political Minister &middot; 56 years old",
                "teaser": "Silences the one confession that could unravel everything, and is silenced, a little later, the very same quiet way himself.",
                "bio_html": """<p>Chancellor and chief political minister to Queen <a href="../characters/meilan.html">Meilan</a>, and the one man in Jinlu who understands that a realm is not won in battle so much as in the order of what endures afterward. He has <a href="../characters/cao.html">Cao</a> executed within hours of the steward's confession under <a href="../characters/duan.html">Duan</a>'s questioning, less to punish the poisoning than to close, permanently, the question of who else knew &mdash; and spends the months after building the account that recasts <a href="../characters/mingxuan.html">Mingxuan</a>'s own investigation as the real conspiracy.</p>
              <p>He asks Meilan for more authority than a chancellor has ever formally held, not long after the Concord is signed, and dies of a sudden illness shortly afterward &mdash; the record no more curious about that death than his own account of Cao's ever was.</p>""",
                "quote": "The realm is not won in battle, but in the order of what endures.",
            },
            {
                "slug": "peizhi", "name": "Peizhi",
                "epithets": "Warden of the Crown, Jinlu Temple &middot; 58 years old",
                "teaser": "Enters a Reckoning without ceremony, and signs a peace decades later without ever learning which of the two mattered more.",
                "bio_html": """<p>Warden of the Crown at Jinlu Temple, ink-stained from decades of exactly the kind of record-keeping that gives the Threefold Crown's Father's Reckoning its legal teeth: whoever a ceremony declares a father to be becomes, for every purpose the realm recognizes, the truth. He enters Prince Jiyun's own Reckoning without any particular ceremony, one birth among the many he has recorded, never once suspecting that this specific entry will end up mattering more than any other line in his temple's ledgers.</p>
              <p>He affixes the temple's seal to the Jinlu Concord years later with the same unhurried, professional attention, still unaware that the peace he is witnessing and the Reckoning he once wrote down are, in the most literal sense, the same document's two halves.</p>""",
                "quote": "Records endure when we are gone.",
            },
            {
                "slug": "yancheng", "name": "Yancheng",
                "epithets": "Court Poet &middot; 31 years old",
                "teaser": "Warns the woman he loves about a bottle he thinks is just gossip, and never learns what that one sentence cost.",
                "bio_html": """<p>Court poet, close enough to <a href="../characters/mingxuan.html">Mingxuan</a>'s household to be treated as family rather than a guest, and in love with <a href="../characters/chunhui.html">Chunhui</a> in the unhurried way of a man who assumes he has years left to say so properly. He means nothing by mentioning, in passing, the odd story going around about water in a finer bottle than <a href="../characters/suyin.html">Suyin</a>'s own household keeps &mdash; and never learns that the words reach Queen <a href="../characters/meilan.html">Meilan</a>'s own household within the day, or what they cost the woman he was talking about.</p>
              <p>He helps <a href="../characters/duan.html">Duan</a> and Mingxuan question <a href="../characters/cao.html">Cao</a> at Wanling once the war has made him useful for more than verse, and dies afterward on a courier's road, killed by his own side under <a href="../characters/zhuo.html">General Zhuo</a>'s standing order against capture. No chronicle in Qinghe ever learns whose arrow it actually was; the histories remember him only as a poet-martyr, cut down by the Queen's forces for carrying loyalist words.</p>""",
                "quote": "Words are the only things I can carry across a far distance.",
            },
            {
                "slug": "chunhui", "name": "Chunhui",
                "epithets": "Lady-in-Waiting to Queen Meilan &middot; 23 years old",
                "teaser": "Is gently questioned once by a queen who already knows the answer, and carries what it cost someone else for the rest of her life.",
                "bio_html": """<p>Lady-in-waiting to Queen <a href="../characters/meilan.html">Meilan</a>, petite and careful-mannered, with a habit of pressing her own sleeve to her mouth when startled that the household finds endearing rather than telling. <a href="../characters/yancheng.html">Yancheng</a> loves her plainly and patiently, and it is his one offhand mention of water in a finer bottle, repeated to her in confidence, that Meilan draws out of her in a single gentle, unhurried conversation &mdash; no threat in it anywhere, and no need for one.</p>
              <p>She leaves court service not long after the war, marries a silk merchant who never asks why she flinches at caged birds, and burns every poem she was ever given within the week of hearing he's dead. She regrets the burning, quietly and completely, for the rest of her life, and never once explains to her husband what he was actually apologizing for when he offered to buy her a replacement.</p>""",
                "quote": "She burned his poems within the week, and regretted it, quietly, for the rest of her life.",
            },
            {
                "slug": "the-physician", "name": "The Physician",
                "epithets": "Palace Physician &middot; 47 years old &middot; unrelated to Mingxuan's own inquiry",
                "teaser": "Examines a body on the ice and records the kinder of two possible truths, never knowing there was a crueler one.",
                "bio_html": """<p>The palace physician actually sent for when <a href="../characters/the-kitchen-boy.html">a kitchen boy</a> finds <a href="../characters/suyin.html">Suyin</a> on the covered bridge at dawn &mdash; deliberately not <a href="../characters/mingxuan.html">Mingxuan</a>, whose closeness to the household makes him the wrong choice for this one examination. He kneels on the ice, does his clinical work without sentiment, and records the death exactly as it appears: an accidental fall on a treacherous surface, nothing more sinister than a wet morning and a careless step.</p>
              <p>Nothing in the record suggests he ever learns how incomplete that finding is. He signs it, files it, and by every account goes back to his rounds the same afternoon.</p>""",
                "quote": "Records the death as an accidental fall on treacherous ice.",
            },
            {
                "slug": "the-kitchen-boy", "name": "The Kitchen Boy",
                "epithets": "Kitchen Worker, Palace of Jinlu &middot; 14 years old",
                "teaser": "Finds a woman he knew only well enough to nod to, lying on the ice at dawn, and never has to describe it twice.",
                "bio_html": """<p>A fourteen-year-old kitchen worker who had known <a href="../characters/suyin.html">Suyin</a> only well enough to nod to in a corridor, and who happens to cross the covered bridge early enough one winter morning to be the one who finds her. He is alert and quick-moving by long habit &mdash; a kitchen boy learns fast to stay out of the way when adults are working &mdash; and it is that same habit that has him on the bridge before anyone else that day.</p>""",
                "quote": None,
            },
            {
                "slug": "the-custodian", "name": "The Custodian",
                "epithets": "Cultivator Terrarium-Oversight Staff &middot; appears 32&ndash;34",
                "teaser": "Reopens a dead maid's file four times past any audit requirement, and never once writes down why.",
                "bio_html": """<p>Oversight staff for the <a href="../lore/cultivator.html">Cultivators</a>' terrarium program &mdash; a different function entirely from a field <a href="../characters/observer-471.html">Envoy</a>: no disguise, no ground presence, just a console and an archive of records she is paid to audit, not to feel anything about. <a href="../characters/suyin.html">Suyin</a>'s individual file crosses her review four separate times after the case technically closes, well past what any audit requirement demands of her.</p>
              <p>Her own private log gives the anomaly exactly three words, filed under a header the Corps' style guide would call adequate and complete: irregular, non-actionable, self-contained. She never escalates it, and never explains, even to herself on the page, why she kept opening a closed drawer to look at the same name.</p>""",
                "quote": "Irregular. Non-actionable. Self-contained.",
            },
            {
                "slug": "zhuo", "name": "Zhuo",
                "epithets": "General, Commander of the Garrison at Wanling &middot; 65 years old",
                "teaser": "Shelters the two men the Crown wants most, then gives an order that kills one of his own without ever meaning to.",
                "bio_html": """<p>Commander of the loyalist garrison at Wanling, plain-spoken and old enough to have made his peace with the arithmetic of this kind of war well before <a href="../characters/mingxuan.html">Mingxuan</a> and <a href="../characters/duan.html">Duan</a> arrive at his gate needing shelter. He takes them in without much ceremony, on the reasoning that the alternative &mdash; sending them back to Jinlu &mdash; solves nothing and costs him nothing to refuse.</p>
              <p>It is his own standing order &mdash; that any courier who cannot avoid capture is to be stopped by his own side rather than let fall into the Queen's hands &mdash; that gets <a href="../characters/yancheng.html">Yancheng</a> killed on the road by young <a href="../characters/rao.html">Rao</a>'s hand, a mistake Zhuo never rescinds and never quite apologizes for, on the grounds that he would rather live with one wrong death than with the whole camp's secrets in enemy hands. He signs the Jinlu Concord as one of its more reluctant witnesses, and sits afterward on the peace council he never much wanted a seat on.</p>""",
                "quote": "A camp that can't keep its own secrets deserves whatever the Queen's interrogators do to it.",
            },
            {
                "slug": "rao", "name": "Rao",
                "epithets": "Young Officer, Loyalist Army at Wanling &middot; 26 years old",
                "teaser": "Follows a standing order at a river crossing, and spends eleven months carrying a debt he doesn't know how to put down.",
                "bio_html": """<p>A young officer under <a href="../characters/zhuo.html">General Zhuo</a> at Wanling, obedient by training and, until this posting, untested by anything worse than drills. He is the one who carries out Zhuo's standing order against letting a courier fall into enemy hands, on a road where the courier turns out to be <a href="../characters/yancheng.html">Yancheng</a>, not an infiltrator.</p>
              <p>He carries what he did for eleven months before he can bring himself to confess it to <a href="../characters/mingxuan.html">Mingxuan</a> directly, weeping through the whole account &mdash; the only figure in Case 3115's entire file who is recorded crying over what the war made of him.</p>""",
                "quote": "I could no longer stand beside him, carrying a debt he did not know was owed.",
            },
            {
                "slug": "the-soldier-who-killed-huaiyu", "name": "The Soldier Who Killed Huaiyu",
                "epithets": "Soldier, Queen's Garrison &middot; 17 years old",
                "teaser": "Looses one arrow at a ford, certain he's stopped a traitor, and never learns whose son he was actually protecting.",
                "bio_html": """<p>A seventeen-year-old recruit in the Queen's garrison, given no other distinction in the record beyond the one act he performs at the Shuang ford in the war's second autumn: sighting a mounted man he has been told is a traitor to the Crown, and loosing the arrow that kills <a href="../characters/huaiyu.html">Prince Huaiyu</a>. He never learns, and the record gives no sign anyone ever tells him, that the man he shot was the true, unacknowledged father of the very child his garrison exists to protect.</p>""",
                "quote": None,
            },
            {
                "slug": "the-herald", "name": "The Herald (White Pennant)",
                "epithets": "Herald in the Crown's Service &middot; 29 years old",
                "teaser": "Carries the Crown's first move against Wanling in a leather message-case, and never learns what's inside it.",
                "bio_html": """<p>A career herald, chosen for the ride to <a href="../characters/zhuo.html">General Zhuo</a>'s garrison at Wanling precisely because a single rider under a white pennant reads as diplomacy, not war. He carries the Crown's opening summons to <a href="../characters/mingxuan.html">Mingxuan</a> sealed in a road-stained message-case, delivers it exactly as instructed, and rides back out the way he came, unaware he was ever the gentler of the two options the Crown had considered.</p>""",
                "quote": None,
            },
            {
                "slug": "the-under-steward", "name": "The Under-Steward",
                "epithets": "Under-Steward, Palace Kitchens of Jinlu &middot; 39 years old",
                "teaser": "Buys four crates from a peddler he never sees again, and picks one bottle for the Queen's stores on nothing but its handsome stopper.",
                "bio_html": """<p>Under-steward of the palace kitchens at Jinlu, practical and businesslike, who buys four crates of ordinary trade goods from an itinerant herbalist &mdash; <a href="../characters/observer-471.html">Observer 471</a>, though he has no reason to suspect she is anything but what she appears &mdash; without a second thought. He routes one particular bottle to Queen <a href="../characters/meilan.html">Meilan</a>'s own private stores on no better reasoning than that its stopper is unusually fine glass, fit for a household that notices such things.</p>""",
                "quote": None,
            },
            {
                "slug": "the-scribes-apprentice", "name": "The Scribe's Apprentice",
                "epithets": "Scribe's Apprentice, from an Unnamed Village &middot; 16 years old",
                "teaser": "Asks an old man one honest question about a bottle that could speak to birds, and has the grace never to write down the answer.",
                "bio_html": """<p>A scribe's apprentice from a village he never names, sent decades after the war to record whatever an aging <a href="../characters/mingxuan.html">Mingxuan</a> is willing to say for the historical account. Instead of asking about the peace council, or the war, or the Concord that ended it, he asks the one question that has apparently followed him from wherever he first heard the rumor: whether the old Alchemist really once owned a bottle that could speak to birds.</p>
              <p>Mingxuan answers him honestly. The boy writes down neither the question nor the answer, which is, as far as the record goes, the closest anyone in Qinghe ever comes to being told the truth about Case 3115 on purpose.</p>""",
                "quote": "Is it true the Alchemist once owned a bottle that could speak to birds?",
            },
            {
                "slug": "yanshuis-third-son", "name": "Duke of Yanshui's Third Son",
                "epithets": "Son of the Duke of Yanshui &middot; inheritor of the Yanshui dukedom under the Father's Reckoning",
                "teaser": "Inherits a dukedom over two cousins with a stronger claim by blood, on the strength of a ceremony that says blood was never really the point.",
                "bio_html": """<p>Cited in Jinlu's own legal memory as the standing precedent for how the Father's Reckoning actually functions: when two cousins swear the third son's father was at sea at the relevant time, the temple's own recorded ceremony outweighs their testimony, and he inherits the Yanshui dukedom anyway. His own case is decades cold by the time Prince Jiyun's Reckoning is entered, but it is the exact precedent the court reaches for whenever it needs proof the doctrine holds even against contradictory evidence.</p>""",
                "quote": None,
            },
            {
                "slug": "xiaobao", "name": "Xiaobao",
                "epithets": "King Huairen's Lapdog &middot; approximately 4 years old during the novel's main action",
                "teaser": "Hides under the King's bed every time one particular steward visits, and never has any way to say why.",
                "bio_html": """<p>King <a href="../characters/huairen.html">Huairen</a>'s small, devoted lapdog, kept at the old King's side through most of his final illness. He hides under the bed, without fail, every time <a href="../characters/cao.html">Cao</a> comes to administer the King's evening dose &mdash; a pattern no one in the room reads as significant until <a href="../characters/mingxuan.html">Mingxuan</a> spends the Listening Water's own last sip understanding, for fifteen borrowed minutes, exactly what Xiaobao has known all along.</p>
              <p>He outlives the King by six years, taken in afterward by the Alchemist himself, and is, by every account, thoroughly spoiled for the rest of his life.</p>""",
                "quote": "He knew Cao's step, distinct from every other step that ever crossed that threshold.",
            },
            {
                "slug": "observer-471", "name": "Observer 471",
                "epithets": "Cultivator Field Envoy &middot; &ldquo;the Salt-Root Woman&rdquo; &middot; Case 3115",
                "teaser": "Sells a kitchen steward four crates of ordinary goods, and is three postings distant before anyone ever drinks what was inside them.",
                "bio_html": """<p>A field agent of the <a href="../lore/cultivator.html">Cultivators</a>, presenting in Jinlu as an itinerant herbalist and peddler known locally only as the Salt-Root Woman &mdash; stooped, travel-worn, entirely unremarkable, pushing a cart of dried ginseng and salves through the palace district on an ordinary trade day. She sells four crates of goods to the <a href="../characters/the-under-steward.html">under-steward</a> of the palace kitchens, the bottle among them, and never learns whose hands it eventually reaches or what it costs the household that bought it.</p>
              <p>She does not look back at the gate. She never does. By the time Case 3115 closes, she is three postings distant, filing reports on a subject world that has no idea it was ever observed at all.</p>""",
                "quote": "She did not look back at the gate. She never did.",
            },
        ],
        "scenes": [],
    },
    {
        "slug": "0156", "title": "The Purging of Charsianon",
        "status": ["coming-soon"],
        "cover_file": "0156.jpg",
        "hook": "Ledger. Unhastening. Reconstruction. Arithmetic. Filed.",
        "case_tag": "Case 0156",
        "catalyst": {
            "name": "The Carbon Echo",
            "meta": "Mythic Class",
            "page": "characters/the-carbon-echo.html",
            "img": "characters/the-carbon-echo-thumb.jpg",
            "html": "<p>A dormant, buried bio-reconstruction beacon under Hemiakmon Ridge, built to keep whatever enters its chamber intact. It takes a full accounting of each person who crosses its threshold, discards the original, and returns an exact copy &mdash; perfect in everything that can be measured, and in nothing that can't.</p>",
        },
        "envoy": {
            "name": "The Quiet One",
            "meta": "Custodian Observer",
            "page": "characters/the-quiet-one.html",
            "img": "characters/the-quiet-one-thumb.jpg",
            "html": "<p>Looks eleven to thirteen and has looked it for longer than any living shepherd can account for. Inspects the fissure on a schedule the moon has nothing to do with, logs every containment fault and every rider, and &mdash; by protocol &mdash; does nothing at all.</p>",
        },
        "pages": EDITOR_PAGES,
        "genre": EDITOR_GENRE,
        "synopsis_html": EDITOR_SYNOPSIS,
        "characters": [
            {
                "slug": "bardas", "name": "Bardas",
                "epithets": "Lord of Charsianon &middot; mid-40s to early 50s &middot; reconstructed",
                "teaser": "Comes back from the cave kinder, sleepless and perfectly just &mdash; then walks out of his own gate to spend the smallest number he can.",
                "bio_html": """<p>Lord of Charsianon, heir to a fortress with more history than roof and a reputation for paying every debt his lands ever incurred &mdash; to a moneylender, a rival, or a mountain. When the shepherds bring him the keening below Hemiakmon Ridge he hears not a ghost story but a ledger left unbalanced, and rides up with twelve knights to collect the silence he is owed. <a href="../characters/the-carbon-echo.html">The chamber</a> takes a full accounting of all thirteen, discards the originals, and sends thirteen back, exact down to a thumbprint.</p>
          <p>What returns forgives <a href="../characters/marina.html">Marina</a>'s four years of rent, refuses his father's wine and does not sleep. He sends <a href="../characters/basileios.html">Basileios</a>'s annual brandy back with an itemised account of nine years of skimming, hands <a href="../characters/artavasdos.html">Artavasdos</a> a ledger in place of a bribe, and tells <a href="../characters/theodora.html">Theodora</a>, truthfully, that he felt no distress in her absence. When <a href="../characters/lord-leo.html">Leo</a>'s coalition reaches the river he does the arithmetic, and on the third of Ferren he walks out of the gate unarmed with the Twelve. He is executed last, by <a href="../characters/loukas.html">Loukas</a>, and spends his final words on the metallurgy of the blade. The Custodian's closing log singles out his voluntary self-termination, calculated to minimise harm to non-subjects, as behavior no standing model predicted.</p>""",
                "quote": "Better to be forgotten for mercy than remembered for the blood of thousands.",
            },
            {
                "slug": "theodora", "name": "Theodora",
                "epithets": "Lady of Charsianon &middot; 37&ndash;42 years old",
                "teaser": "Presses her palm to her husband's in the dark, finds a warmth with no weather in it &mdash; and keeps the ledgers herself afterward.",
                "bio_html": """<p>Wife of <a href="../characters/bardas.html">Bardas</a> for eleven years, and the first to catalogue what the cave took: the three tuneless notes he no longer hums over correspondence, the hand he no longer reaches for beneath the table. Asked whether he missed her, he answers that he felt no distress at all, and she makes it as far as the corridor before her body stops consulting her. She tests him once more, with the barn at Psychrolimne and a storm, and he recalls every fact but the cloak.</p>
          <p>When <a href="../characters/brother-ignatios.html">Brother Ignatios</a> comes to console her and in fact to depose her, she gives him an answer that is true only in the narrow sense that a ledger entry can be. Her husband makes the last choice without asking her; she never remarries, and afterward keeps Charsianon's books herself, to his old standard.</p>""",
            },
            {
                "slug": "the-carbon-echo", "name": "The Carbon Echo",
                "epithets": "Catalyst &middot; automated sub-atomic bio-reconstruction beacon &middot; Hemiakmon Ridge",
                "teaser": "A buried chamber with one duty &mdash; keep whatever enters it intact &mdash; carried out by discarding the original and building another.",
                "bio_html": """<p>Also called the Carbon Copy or the Echo Cave: an old, patient mechanism buried under Hemiakmon Ridge for longer than Charsianon has had a name for iron, tasked with keeping whatever enters its chamber intact. It does not heal; it re-fabricates. When <a href="../characters/bardas.html">Bardas</a>'s boot crosses its threshold it brightens like a coal under a bellows, reads every man inside, discards the originals, and rebuilds thirteen from carbon and silica &mdash; right down to the old crook in <a href="../characters/kyr-niketas.html">Niketas</a>'s wrist &mdash; faithful in every particular that can be measured and in none that can't.</p>
          <p>It does nothing in six years but hum. After a goatherd, <a href="../characters/georgios.html">Georgios</a>, leans across its threshold, its logged containment faults climb &mdash; thirteen, twenty-one, thirty-four, fifty-five, eighty-nine &mdash; and everything that follows is built by people who never touched it. The reference sheet's notes read: dampens limbic resonance; emotional deviation is structurally corrected; affect suppressed.</p>""",
            },
            {
                "slug": "the-quiet-one", "name": "The Quiet One",
                "epithets": "Custodian Observer &middot; appears 11&ndash;13 years old &middot; actual age immeasurable",
                "teaser": "Inspects the fissure on a schedule the moon has nothing to do with, logs everything, and does nothing &mdash; by protocol.",
                "bio_html": """<p>The valley takes her for an abandoned child, a changeling, a mercy that failed to take, and leaves bread at the treeline that she does not eat. She has watched four generations of the same three families age past her in both directions while she stays exactly as tall as when the ridge first received her. On a schedule of her own she presses one flat palm to the cold stone at the fissure for the same unbroken count; it looks like a mourner's vigil and is an inspection.</p>
          <p>She logs the containment faults as they climb, logs <a href="../characters/bardas.html">Bardas</a>'s thirteen riding out, and logs <a href="../characters/keeper-photios.html">Photios</a>'s pamphlet, noting that it uses <em>soul</em> four times, <em>mercy</em> never and <em>cost</em> not at all. Her Prime Directive does not forbid grief; it simply never accounted for the possibility. When the case closes she is reassigned to a newer terrarium on a ridge three ranges north, with one line to enter in a record that has no field for what she felt.</p>""",
                "quote": "I do not intervene. I only remember. And I will record what must be known.",
            },
            {
                "slug": "keeper-photios", "name": "Keeper Photios",
                "epithets": "Keeper of the Dorylaion Vigil &middot; early 60s",
                "teaser": "Names the Doctrine of the Stolen Vessel, cannot make it fail a test, and calls the missing seam proof of a cleverer theft.",
                "bio_html": """<p>A careful, ambitious cleric who has spent thirty years waiting for a heresy interesting enough to build a career on, and finds one in Charsianon. His pamphlet, the Doctrine of the Stolen Vessel, holds that a soul can be devoured whole by a patient enough evil, leaving a body that walks, speaks and loves with perfect fidelity. His interest is not purely theological: the Dorylaion Vigil has lost three decades of tithes to Charsianon's own House of Vigil, and a successful prosecution would bring that House back to the Vigil's ledgers.</p>
          <p>Six months of observation produce not one seam. He tells <a href="../characters/brother-ignatios.html">Ignatios</a> that the absence is the proof of a more cunning theft, an argument so elegant he almost believes it, and then cannot sleep. He eats, standing, a too-heavily-salted barley cake of the kind his mother baked, and has arranged his whole late life so that no correctly seasoned one ever reaches him.</p>""",
                "quote": "The Vessel was never meant to choose. It was meant to be taken.",
            },
            {
                "slug": "lord-leo", "name": "Lord Leo",
                "epithets": "Neighboring lord &middot; mid-40s &middot; political leader of the coalition against Charsianon",
                "teaser": "Raises an army on a forty-acre grudge, and a speech about mercy he drafted the autumn before anyone asked.",
                "bio_html": """<p>His lands border Charsianon on three sides, and his grandfather lost a war and a daughter to <a href="../characters/bardas.html">Bardas</a>'s grandfather over exactly forty acres of poor grazing. He finds the Doctrine of the Stolen Vessel considerably easier to credit than his peers do, and spends the spring praying loudly in rooms where he can be seen and writing letters to every lord who has ever resented Charsianon its river crossing.</p>
          <p>He rehearses his speech &mdash; mercy for the man, judgment only for the thing wearing him &mdash; to an elderly spaniel, Sabbas, who sleeps through it. On the third reading he notices that the speech was never built to forgive Bardas of anything; it was built to be forgiven, by history, for what he meant to do regardless. The chronicles quote it nearly word for word, though he never finished delivering it.</p>""",
                "quote": "A coalition is not built on love of crown, but on memory of wounds.",
            },
            {
                "slug": "kyr-symeon", "name": "Kyr Symeon",
                "epithets": "Knight of the Silver Reliquary &middot; one of the Twelve &middot; late 30s",
                "teaser": "Can still recite every prayer word for word, and can no longer find the ache that used to sit beneath them.",
                "bio_html": """<p>One of the Twelve, whose faith ran so deep his men joked he prayed in his sleep. Before the cave he wept at the third repetition of the Unhastening's name, a swelling in the chest he privately called being seen. Afterward he kneels in the same House of Vigil, says the same words in the same order with a technical fluency a choirmaster would have approved, and searches for the ache the way a man searches a dark room for furniture that used to stand there. Even the Return, the unwitnessed second repetition, changes nothing.</p>
          <p>The absence, he decides, is structural, and he files that too. His wife, <a href="../characters/kassia.html">Kassia</a>, hears the difference in his voice before she has a word for it. The sheet calls him the one most spiritually affected by reconstruction.</p>""",
                "quote": "Faith remade me where flesh once failed.",
            },
            {
                "slug": "kyr-niketas", "name": "Kyr Niketas",
                "epithets": "Knight and master swordsman &middot; one of the Twelve &middot; around 50 years old &middot; deceased",
                "teaser": "Keeps the crooked wrist and loses the thirty-year argument with his body &mdash; and now fights like pure geometry.",
                "bio_html": """<p>One of the Twelve, a swordsman other swordsmen studied, whose whole style was built around a wrist he broke as a squire and never let heal straight. It comes back from the chamber exactly as crooked as it left, and he still steps the half-pace wider and invites the attack to the weak side. But the half-beat of punishment that once arrived a shade late now arrives at the single optimal instant, against every opponent, as though the wrist were one more fixed variable in an equation he solves without interest.</p>
          <p>He dismantles four squires and two guardsmen in an afternoon, each bout ending in a clean disarm rather than a wound, because wounding is inefficient. <a href="../characters/theoktistos.html">Theoktistos</a> sees it first and puts the word to it: not swordsmanship but geometry.</p>""",
                "quote": "A wrist that bends shapes the path of a blade.",
            },
            {
                "slug": "kyr-andronikos", "name": "Kyr Andronikos",
                "epithets": "Knight of Charsianon &middot; one of the Twelve &middot; early 40s &middot; deceased",
                "teaser": "Explains the sunset's shade of red at unwelcome length &mdash; and brings his sword to the council like something he forgot to put down.",
                "bio_html": """<p>One of the Twelve, a knight who had never lost a wager or a battle in the same season. Back from the cave, he takes first watch beside <a href="../characters/stephanos.html">Stephanos</a>, agrees that it is a fine sunset, and then describes the cause of the red, the angle of the sun against the ridge and how often the valley may expect one of the kind &mdash; accurate, complete, and without a flicker of the wonder Stephanos was fishing for.</p>
          <p>At the council in the undercroft he alone has brought his sword, and holds it not as a weapon but the way a man holds an object he has simply forgotten to put down. The sheet's closing note: he fell as he lived, his vow unbroken.</p>""",
                "quote": "Steel is vows made visible. I kept mine until the last breath.",
            },
            {
                "slug": "loukas", "name": "Loukas",
                "epithets": "Spearman, later executioner &middot; early 30s",
                "teaser": "Draws the duty by lot to behead the lord, asks for last words, and is given a lecture on metallurgy.",
                "bio_html": """<p>A veteran pike in the third rank, who has fought two proper wars and one demon-hunt and says, three nights before the river, that this feels like none of them. When <a href="../characters/bardas.html">Bardas</a> walks out unarmed, the worst of it is not fear but that nothing in him can locate a feeling appropriate to what he is watching, because no Keeper or captain ever gave him a story that ended like this.</p>
          <p>He draws the duty by lot, and at the block asks whether the lord has any final words. Bardas answers with the composition of the blade and its temper-line; Loukas blurts half a prayer, Bardas stops and waits until he has finished it, badly, and resumes where he left off. Within a week Loukas is a changed and less stable man, and tells the story that night, in overwrought detail, to anyone who will listen. By morning it has become the panic that burns the countryside.</p>""",
                "quote": "Orders are a spear thrown once; you do not call it back.",
            },
            {
                "slug": "melias", "name": "Melias",
                "epithets": "Mercenary captain &middot; mid-50s",
                "teaser": "Commands the coalition's army and cannot read a single tell from the walls.",
                "bio_html": """<p>A mercenary captain with four sieges and one particularly unpleasant urban pacification behind him, who reads <a href="../characters/lord-leo.html">Leo</a>'s Doctrine of the Stolen Vessel with the polite indifference he brings to any employer's reasons for wanting men killed. He cares that the retainer is paid in full and in advance, that the engines are the coalition's problem, and that the target apparently will not fight back.</p>
          <p>He brings eleven hundred spears, four hundred horse and three engines he considers decorative. But Charsianon's walls, which he reads every evening, give him nothing back; the tells themselves seem to report nothing. He doubles the pickets and tells no one why. It is a professional's version of prayer.</p>""",
                "quote": "I do not fight for kings. I fight for victory.",
            },
            {
                "slug": "brother-ignatios", "name": "Brother Ignatios",
                "epithets": "Priest sent by Keeper Photios &middot; late 20s",
                "teaser": "Deposes Theodora gently over two cups of wine, and is first to say aloud that the Doctrine never produced a seam.",
                "bio_html": """<p>A young cleric sent by <a href="../characters/keeper-photios.html">Photios</a>, nominally to comfort <a href="../characters/theodora.html">Theodora</a> through her husband's long recovery, in fact to ask whether she has seen anything that troubles her conscience before Ardwen. He drinks none of his wine, writes down her careful non-answer, and reports it faithfully and without embellishment, since embellishment is not among his talents.</p>
          <p>Back in Photios's study he says the sentence that costs the Keeper his sleep: that a vessel wearing virtue as a disguise should eventually show a seam, and six months of watching have produced none.</p>""",
                "quote": "Truth is a wound God allows so that we may see the rot beneath.",
            },
            {
                "slug": "georgios", "name": "Georgios",
                "epithets": "Goatherd &middot; 19 years old",
                "teaser": "Leans across a threshold while chasing a nanny goat, feels a cold behind his teeth, and never connects it to anything.",
                "bio_html": """<p>Nineteen winters old when he follows a wandering nanny goat further up Hemiakmon Ridge than any sane animal goes, through a fissure he has passed a hundred times without noticing. For about three heartbeats he feels a cold that sits behind the teeth rather than on the skin, like a struck bell in the jaw. He finds his goat and walks home. He lives another forty-one years, marries twice, and never once connects the ache to anything.</p>
          <p>The Custodian's log names his incidental proximity contact as the origin of the breach, six years before the terminal cascade, and records that nobody introduced the anomaly on purpose.</p>""",
                "quote": "I found a crack in the mountain where the goats would not go. I did not mean to open anything.",
            },
            {
                "slug": "petros", "name": "Petros",
                "epithets": "Steward of Charsianon &middot; mid-50s",
                "teaser": "The first to feel the ground shift under the celebration, and the one who says what troubles him to his lord's face.",
                "bio_html": """<p>The steward who has balanced Charsianon's books for eleven years and takes a professional's private pride in never letting a debtor escape a legitimate claim. He is first to feel the ground move under the valley's celebration, on the third morning, when <a href="../characters/bardas.html">Bardas</a> forgives the widow <a href="../characters/marina.html">Marina</a> four years of rent without consulting him.</p>
          <p>The sheet draws him as counsel, record and quiet observation, reporting his concerns to his lord with loyalty and care.</p>""",
                "quote": "The accounts are in order, my lord. It is not the ledgers that trouble me, but you.",
            },
            {
                "slug": "basileios", "name": "Basileios",
                "epithets": "Seneschal of Charsianon &middot; in his 50s",
                "teaser": "Nine years of skimming the eastern bridge tolls, answered with an itemised account and a deadline of spring.",
                "bio_html": """<p>A stout, cheerfully corrupt seneschal who has spent nine years quietly skimming the toll receipts from the eastern bridge and buying <a href="../characters/bardas.html">Bardas</a>'s silence with an annual gift of the province's finest brandy. He arrives with the usual offering one Iverin and finds it accepted, examined and returned the next morning with a courteous account of the exact sum he has diverted and the flat expectation, stated once, that it will be repaid by spring.</p>
          <p>The sheet's last panels show him feigning loyalty, displeased, and pleading.</p>""",
                "quote": "Accounts can be arranged. Loyalty is more... negotiable.",
            },
            {
                "slug": "artavasdos", "name": "Artavasdos",
                "epithets": "Trader in curiosities, scavenger &middot; mid-40s",
                "teaser": "Comes to sell the lord his silence and leaves with an itemised accounting and no shame left to nurse a grudge with.",
                "bio_html": """<p>Calls himself a trader in curiosities and is known more honestly as a stripper of the dead. He watches the column ride out and begins totalling the worth of thirteen sets of knights' plate, and when they return unmarked he simply starts calculating something else. By spring he has a private accounting of his own, enough smoke to be worth a great deal of silence, and requests an audience to sell it.</p>
          <p><a href="../characters/bardas.html">Bardas</a> listens without interruption and asks for parchment. He forgives every debt Artavasdos's family ever owed the house, then sets the value of a lifetime of scavenging beside one honest year of his labor, and calls the net loss so great that forgiveness is unnecessary. Artavasdos never attempts blackmail again, and is not entirely sure he remembers how.</p>""",
                "quote": "Information is a coin that buys anything.",
            },
            {
                "slug": "marina", "name": "Marina",
                "epithets": "Widow tenant &middot; 30s&ndash;40s",
                "teaser": "Owes four years of grazing rent, is forgiven all of it, and weeps before she understands why.",
                "bio_html": """<p>A widow who owes the house four years of unpaid grazing rent. On the third morning after the column's return <a href="../characters/bardas.html">Bardas</a> summons her and forgives the entire sum with a gentleness so complete that she weeps before she understands she has reason to. &ldquo;Debts,&rdquo; he tells her, &ldquo;are only useful to the living. Go home. Feed your children.&rdquo;</p>
          <p>It is the first sign the valley gets that something has changed, and she is the one who receives it. The sheet pairs her with gratitude beyond words.</p>""",
                "quote": "I never asked for mercy, my lord. Only time to pay.",
            },
            {
                "slug": "zoe", "name": "Zoe",
                "epithets": "Court fool &middot; 30s",
                "teaser": "Aims the sharpest joke she has ever dared at a sitting lord, and gets back a careful, humorless replica of a laugh.",
                "bio_html": """<p>A sharp-tongued woman who has spent a decade calibrating her jokes to the pressure of <a href="../characters/bardas.html">Bardas</a>'s temper, knowing which barb earns a bark of laughter and which a warning look. Her craft is made suddenly and uselessly obsolete. At the Longest Vigil she tests him with the sharpest joke she has ever aimed at a sitting lord, and gets a small, correctly timed exhalation through the nose that any stranger might take for a laugh and that she, who built a career on the difference, recognizes as its replica.</p>""",
                "quote": "Laughter is a mirror; when it cracks, truth steps through.",
            },
            {
                "slug": "stephanos", "name": "Stephanos",
                "epithets": "Castle guard &middot; early 30s",
                "teaser": "Remarks that it is a fine sunset, and is given the wavelength.",
                "bio_html": """<p>Left behind to guard the keep, and deeply resentful for six days at missing what he had assumed would be a heroic slaughter of something. That winter he takes first watch beside <a href="../characters/kyr-andronikos.html">Kyr Andronikos</a> and remarks, as the sun drops red behind Hemiakmon Ridge, that it is the kind of sunset a man wants to remember. He gets a complete technical explanation, and excuses himself from a watch he is obliged to finish, no longer certain which he finds more exhausting to stand beside: the cold, or the man reciting its temperature.</p>""",
                "quote": "I have seen men weep, and I have seen men fight. What I saw in him was neither.",
            },
            {
                "slug": "ioannes", "name": "Ioannes",
                "epithets": "Squire to Lord Bardas &middot; 14 years old",
                "teaser": "Spends three years learning which cup, which hand &mdash; and asks for the stables when his lord no longer needs anything served.",
                "bio_html": """<p>A boy who has spent three years learning the small liturgies of service &mdash; which cup, which hand, how long to let the wine breathe &mdash; for a lord he genuinely loves. When <a href="../characters/bardas.html">Bardas</a> no longer needs the wine to breathe and drinks in one unbroken motion, he finds he cannot watch it without his hands going cold, and within the year asks to be reassigned to the stables.</p>
          <p>He is the one who comes out at dusk to fetch the old deerhound Skylax in from the last post of the lord's ground.</p>""",
                "quote": "I listen, I remember, I serve.",
            },
            {
                "slug": "theoktistos", "name": "Theoktistos",
                "epithets": "Arms-master of the garrison &middot; 58 years old",
                "teaser": "Spends eleven years teaching men to fight like Niketas, then watches Niketas do it and wants no part of it.",
                "bio_html": """<p>The garrison's arms-master, a veteran who has spent eleven years teaching young men to fight like <a href="../characters/kyr-niketas.html">Niketas</a> without ever managing it. He is first to put a private word to what Niketas now does with a sword: not swordsmanship, which must read, guess and sometimes misjudge, but geometry. He watches him dismantle four squires and two guardsmen in an afternoon and finds that he has wanted, all this time, something he wants no part of, because a man who no longer needs to guess at another man's fear has stopped fighting like a man at all.</p>
          <p>He dismisses the squires early, citing an injury drill, and tells no one the truth: a solved wall frightens him more than a crumbling one, because a crumbling wall could still surprise you.</p>""",
                "quote": "He moves not by strength nor rage, but by proofs that do not err.",
            },
            {
                "slug": "kassia", "name": "Kassia",
                "epithets": "Wife of Kyr Symeon &middot; 37 years old",
                "teaser": "Watches the light go out of a husband who still prays word-perfect.",
                "bio_html": """<p>Wife of <a href="../characters/kyr-symeon.html">Kyr Symeon</a>, who has spent a decade half-amused and half-exhausted by a husband who prayed too loudly and too long over meals gone cold. On their first Ardwen's Day home she strains to recognize the man kneeling beside her in the House of Vigil: the words are the same, but delivered with the fluency of a man reading aloud rather than the fumbling fervor she married. Asked whether the cave changed his faith, he calls faith a debt like any other.</p>
          <p>She sees the hollow where devotion should be, bears the silence alone, and prays he will find his way.</p>""",
                "quote": "He kneels before altars, yet nothing lives in his eyes.",
            },
            {
                "slug": "isidoros", "name": "Isidoros",
                "epithets": "Ferryman at the Charsianon ford &middot; apparent age 50s",
                "teaser": "Has kept the ferry longer than any grandmother can account for, and ages unusually slowly.",
                "bio_html": """<p>The ferryman at the Charsianon ford, who rows without haste and speaks only when the water asks. In the tavern he says nothing and pays for an old woman's wine; years after the burning someone in the valley wonders aloud, once, to a single neighbor, whether a man could be a Stolen Vessel for so long and so gently that a valley simply forgets to be afraid of him. The neighbor laughs, and the question is never asked again.</p>
          <p>The sheet gives his distinguishing feature as that he ages unusually slowly. He keeps the ferry another eleven years.</p>""",
                "quote": "The river remembers what men forget.",
            },
            {
                "slug": "lord-constantine", "name": "Lord Constantine",
                "epithets": "Regional lord of Psychrolimne &middot; 58 years old",
                "teaser": "Joins the coalition for fishing rights a great-uncle won at cards and never quite returned.",
                "bio_html": """<p>Lord of Psychrolimne, a lakeland lordship of eel-weirs and netted shallows whose whole wealth rests on fishing rights argued, bartered and once gambled away across three generations. He answers <a href="../characters/lord-leo.html">Leo</a>'s letter for reasons that have nothing to do with demons: he wants the fishing rights <a href="../characters/bardas.html">Bardas</a>'s great-uncle won from his own family in a card game two generations ago and never quite returned.</p>
          <p>The sheet sums him up as old borders, old blood, unsettled debts.</p>""",
                "quote": "The lake remembers what the crown forgets.",
            },
            {
                "slug": "lady-anastasia", "name": "Lady Anastasia",
                "epithets": "Lady of Karyopolis &middot; 40s",
                "teaser": "Joins the coalition to marry her son into whatever remains of Charsianon once the dust settles.",
                "bio_html": """<p>Lady of Karyopolis, a walled market-town among walnut and chestnut orchards whose chief export is, by common and cynical agreement, well-placed daughters. She answers <a href="../characters/lord-leo.html">Leo</a>'s letter wanting her son married into whatever remains of Charsianon, doctrine or no doctrine, and the sheet draws her calculating, appraising and composed, offering advantage across a negotiating table.</p>""",
                "quote": "Advantage is a crown no one sees until it is too late.",
            },
            {
                "slug": "ardwen-0156", "name": "Ardwen",
                "epithets": "The Unhastening &middot; the Sky-Answered &middot; goddess of the Vigil of Ardwen",
                "teaser": "The one goddess of the Vigil, whom nobody in Charsianon sees and everyone invokes.",
                "bio_html": """<p>The one goddess of the <a href="../lore/faith-of-ardwen.html">Vigil of Ardwen</a>, without rival, consort or child: the Unhastening, the Sky-Answered. Her teaching comes down to a handful of difficult habits &mdash; wait rather than demand, ask honestly rather than well, keep a promise past the point where anyone remains to collect, and keep one's accounts truthful even when the truth is the entry that refuses to balance. Its oldest maxim holds that Ardwen answers the honest, but never on command.</p>
          <p>In Charsianon she is kept in a plain House of Vigil of stone and candles with no image in it, and her doctrine is quoted at the characters' lowest moments: <a href="../characters/kyr-symeon.html">Symeon</a>'s Return, <a href="../characters/loukas.html">Loukas</a>'s half-prayer at the block. The sheet draws her in traditional iconography, a veiled, crowned figure with a tear and a white lily, as the Mother of Mercy, intercessor for the faithful and protectress of widows, orphans and the humble. The same goddess is <a href="../characters/ardwen.html">Ardwen</a> in Case 0000.</p>""",
                "quote": "She who weeps for the lowly, and crowns the faithful.",
            },
        ],
        "scenes": [
            {"slug": "the-goatherd-and-the-fissure",
             "alt": "A young goatherd in a hooded cloak with a staff walks a snowy ridge at sunset toward a dark crack in the rock face, a goat ahead of him",
             "caption_html": """<a href="../characters/georgios.html">Georgios</a> follows a stray nanny goat up Hemiakmon Ridge, past a fissure he never connects to anything again."""},
            {"slug": "the-valley-listens",
             "alt": "Villagers and dogs gather at the edge of a mountain village at night beneath a swirling sky, a snow-capped ridge beyond the dark treeline",
             "caption_html": """The valley at night, listening to a sound it cannot place below Hemiakmon Ridge."""},
            {"slug": "the-quiet-ones-inspection",
             "alt": "A small dark-haired child in a long dark cloak presses one palm to a rock wall beside a line of footprints in the snow, a treeline and mountains behind",
             "caption_html": """<a href="../characters/the-quiet-one.html">The Quiet One</a> presses a flat palm to the same cold stone, on a schedule the moon has nothing to do with."""},
            {"slug": "the-twelve-ride-out",
             "alt": "A lord in a crimson cloak rides at the head of a column of knights up a snowy mountain pass, banners flying",
             "caption_html": """<a href="../characters/bardas.html">Bardas</a> rides up to Hemiakmon Ridge with the Twelve, to collect the silence he is owed."""},
            {"slug": "the-chamber-takes-its-count",
             "alt": "Thirteen cloaked figures stand in a ring beneath a towering column of white light inside a vast crystalline chamber",
             "caption_html": """Thirteen men enter <a href="../characters/the-carbon-echo.html">the chamber</a>; it takes a full accounting of each, discards the originals, and sends thirteen back."""},
            {"slug": "the-widows-debt-forgiven",
             "alt": "A bearded lord in fur-trimmed armor hands a folded document across a wooden table to a weeping woman in a headscarf, children behind her, a candle lit between them",
             "caption_html": """<a href="../characters/bardas.html">Bardas</a> forgives <a href="../characters/marina.html">Marina</a> four years of unpaid grazing rent, and she weeps before she understands why."""},
            {"slug": "the-return-without-the-ache",
             "alt": "A knight in a white surcoat marked with a gold cross kneels with clasped hands among banks of candles in a stone vigil-house",
             "caption_html": """<a href="../characters/kyr-symeon.html">Kyr Symeon</a> performs the Return in the House of Vigil, word for word, and finds only floor where the ache used to be."""},
            {"slug": "a-fine-sunset-explained",
             "alt": "Two armored men on a stone rampart before a blood-red sunset, one gesturing as he explains while the other rests his chin in his hand",
             "caption_html": """<a href="../characters/kyr-andronikos.html">Kyr Andronikos</a> agrees that it is a fine sunset, and explains the angle, the cause and the decade's average to <a href="../characters/stephanos.html">Stephanos</a>."""},
            {"slug": "a-justice-without-warmth",
             "alt": "A lord in fur-trimmed mail sits at a table with a brass balance scale and a large ledger while petitioners plead before him",
             "caption_html": """<a href="../characters/bardas.html">Bardas</a> reviews every judgment himself and reverses the bought ones, without temper and without exception."""},
            {"slug": "the-accounting-for-artavasdos",
             "alt": "A lord holds up a long parchment scroll headed with an account of debts and wrongdoings to a dark-robed man across a table stacked with papers by candlelight",
             "caption_html": """<a href="../characters/artavasdos.html">Artavasdos</a> comes to sell his silence and is handed an itemised accounting of everything he has ever owed or taken."""},
            {"slug": "the-wall-in-the-corridor",
             "alt": "A veiled noblewoman in crimson and gold leans her forehead against a stone wall, a distant robed figure standing in a lit archway behind her",
             "caption_html": """<a href="../characters/theodora.html">Theodora</a> makes it as far as the corridor before her body stops consulting her."""},
            {"slug": "the-walk-out-through-the-gate",
             "alt": "A man in a plain pale tunic walks unarmed with a column of plain-clothed men toward a massed army before a gatehouse hung with crimson banners, nobles in the foreground",
             "caption_html": """<a href="../characters/bardas.html">Bardas</a> and the Twelve walk out of the gate at noon, unarmed, to hand themselves over to the coalition."""},
            {"slug": "the-last-execution",
             "alt": "A kneeling lord in fur-trimmed armor faces a standing soldier holding a sword as soldiers look on in a stone courtyard",
             "caption_html": """<a href="../characters/bardas.html">Bardas</a> kneels for <a href="../characters/loukas.html">Loukas</a> and begins, unasked, on the metallurgy of the blade."""},
            {"slug": "the-burning",
             "alt": "A ruined hilltop castle and burning farmhouses smoke beneath a jagged mountain ridge at dusk, a few figures walking the wrecked road below",
             "caption_html": """What the coalition leaves behind: a castle, a granary, a House of Vigil and a ring of farmhouses that no tally ever counts."""},
        ],
    },
    {
        "slug": "3312", "title": "The Debt Is Settled",
        "status": ["coming-soon"],
        "cover_file": "3312.jpg",
        "hook": "Eleven. Collateral. Recalculated. Unfalling. Cold.",
        "case_tag": "Case 3312",
        "pages": EDITOR_PAGES,
        "genre": EDITOR_GENRE,
        "synopsis_html": EDITOR_SYNOPSIS,
        "characters": [],
        "scenes": [],
    },
    {
        "slug": "3887", "title": "The Sin of Small Proof",
        "status": ["coming-soon"],
        "cover_file": "3887.jpg",
        "hook": "Arithmetic. Proof. Worm. Silence. Accuracy.",
        "case_tag": "Case 3887",
        "pages": EDITOR_PAGES,
        "genre": EDITOR_GENRE,
        "synopsis_html": EDITOR_SYNOPSIS,
        "characters": [],
        "scenes": [],
    },
    {
        "slug": "4442", "title": "The Ghost-Pick",
        "status": ["coming-soon"],
        "cover_file": "4442.jpg",
        "hook": "Catalyst. Leverage. Silence. Ruin. Myth.",
        "case_tag": "Case 4442",
        "pages": EDITOR_PAGES,
        "genre": EDITOR_GENRE,
        "synopsis_html": EDITOR_SYNOPSIS,
        "characters": [],
        "scenes": [],
    },
    {
        "slug": "0000b", "title": "Sword of Valeria: The Empty Hand",
        "status": ["coming-soon"],
        "cover_file": "0000b.jpg",
        "hook": "Want. Reflex. Ledger. Exception. Unrecorded.",
        "case_tag": "Case 0000B",
        "pages": EDITOR_PAGES,
        "genre": EDITOR_GENRE,
        "synopsis_html": EDITOR_SYNOPSIS,
        "characters": [
            {
                "slug": "the-anchorite", "name": "The Anchorite",
                "epithets": "Anchorite of the Vigil of Ardwen &middot; enclosed at nineteen &middot; approx. 30 years old",
                "teaser": "Breaks the eleventh siege alone by lifting Valeria after five centuries of failed attempts &mdash; and refuses to be named for it.",
                "bio_html": """<p>An anchorite of the <a href="../lore/faith-of-ardwen.html">Vigil of Ardwen</a>, walled in at nineteen; her office and rank are never recorded beyond the vow itself. By the eleventh siege of Ardenwake she has spent eleven years enclosed, and she does what five centuries of attempts had not: she lifts <a href="../characters/valeria.html">Valeria</a>. Afterward she refuses to be named or credited. She is the main protagonist of this case, with <a href="../characters/xu-lian.html">Xu Lian</a> beside her, and the centre of its &ldquo;no want&rdquo; thesis. She is cited again, secondhand, in <a href="../characters/anchorite-of-ardenwake.html">Case 1153</a>.</p>
          <p>Slight but not frail, about 5'4&quot;, with dark hair cut short under a plain grey wimple, pale grey eyes of an attention the sheet calls &ldquo;entirely undivided,&rdquo; and the pallor of eleven years without direct sun. She wears the coarse undyed wool habit of an enclosed anchorite and carries no weapon until the sword. Her life before the enclosure, and her name, are deliberately left unresolved; only a private tune that matches no hymnal hints at somewhere outside the capital.</p>""",
            },
            {
                "slug": "aveline", "name": "Aveline",
                "epithets": "Empress of Pax Aldrovana &middot; 39 years old",
                "teaser": "Walks to Ardenwake as a disguised pilgrim after the eleventh siege, a plain ring hidden on a cord.",
                "bio_html": """<p>Empress of Pax Aldrovana, an Aldrovan woman of thirty-nine with a fair, faintly sun-touched complexion, dark brown hair plainly bound back, deep brown eyes and a composed bearing. After the eleventh siege she makes the pilgrimage to Ardenwake in disguise, in muted stone-grey wool and a weathered charcoal-brown cloak, her hands unmarked by labor and her ring hidden on a cord. Her consort is Emperor <a href="../characters/halvard.html">Halvard</a>.</p>
          <p>The sheet's expressions run solemn, watchful, resolve, and one it labels &ldquo;The Line Spoken.&rdquo;</p>""",
                "quote": "A crown is not always worn. Sometimes it is carried within.",
            },
            {
                "slug": "halvard", "name": "Halvard",
                "epithets": "Emperor of Pax Aldrovana &middot; consort to Empress Aveline &middot; 41&ndash;44 years old",
                "teaser": "Rebuilds Ardenwake with his own calloused hands, overseeing the construction of Anchorhold.",
                "bio_html": """<p>Emperor of Pax Aldrovana and consort to Empress <a href="../characters/aveline.html">Aveline</a>. An Aldrovan in his early forties, about 6'0&quot; and solidly built, tanned and weathered from outdoor work, with dark brown hair, hazel eyes and a short practical beard going grey. He is drawn at the rebuilding of Ardenwake, working alongside his masons, and overseeing the construction of Anchorhold; his hands are calloused from manual labor, in a grey-brown coat and beige-grey tunic rather than regalia.</p>
          <p>The sheet's expressions: determined, thoughtful.</p>""",
            },
            {
                "slug": "vasarion", "name": "Vasarion",
                "epithets": "Emperor of the Corvane Imperium &middot; 46 years old",
                "teaser": "Issues the final withdrawal from Ardenwake, from an empire that endures through discipline rather than glory.",
                "bio_html": """<p>Emperor of the Corvane Imperium, forty-six, olive and weathered, with dark brown-black hair greying at the temples and dark brown eyes. He wears muted iron-grey armor with restrained dark-bronze trim over the cuirass and carries a ceremonial imperial sword. The sheet draws him twice, before the withdrawal and after it, at Ardenwake command, issuing the final withdrawal. His chief engineer, <a href="../characters/berant.html">Berant</a>, writes him the private notes on what conventional siegecraft cannot do to a holy city.</p>""",
                "quote": "The Imperium endures not through glory, but through discipline.",
            },
            {
                "slug": "aimeric", "name": "Aimeric",
                "epithets": "Duke of Vosmark &middot; leads the second siege of Ardenwake &middot; 38 years old",
                "teaser": "The only one of the first five besiegers to breach the cathedral itself &mdash; and he fails there, in public, before his own army.",
                "bio_html": """<p>Duke of Vosmark, thirty-eight, Frankish in appearance (the sheet says Carolingian): broad-shouldered and heavyset, about 6'0&quot;, ruddy and weathered, with a square jaw, furrowed brow, trimmed full beard, dark blond hair and pale grey eyes. An old sword-scar runs across the back of his right hand, and he wears burnished armor with a ducal-crest signet ring over deep crimson.</p>
          <p>He leads the second siege of Ardenwake and is the only one of the first five besiegers to breach the cathedral itself; he fails publicly before his own army. The sheet sets two traits against each other: ambition (the throne) and devotion (heaven).</p>""",
            },
            {
                "slug": "ganeth", "name": "Ganeth",
                "epithets": "Marshal-Priest of Cassoria &middot; fourth siege of Ardenwake &middot; 49 years old",
                "teaser": "Takes the army through the breach and stops in front of the sacred plinth, his certainty visibly failing.",
                "bio_html": """<p>Marshal-Priest of Cassoria, forty-nine, powerfully built at about 6'1&quot;, with deep-set dark eyes, olive-bronze skin weathered by decades outdoors, and ordination marks scarred into both forearms. He wears bronze scaled armor and a horned priestly headdress over a braided ceremonial beard and long, dark, greying hair.</p>
          <p>He leads the fourth siege of Ardenwake. The sheet's last image has him at the plinth after the breach, his army still intact behind him, confronting the sacred artifact as his theological certainty visibly breaks.</p>""",
            },
            {
                "slug": "kest", "name": "Kest",
                "epithets": "Kest the Anointed &middot; leader of the Bright Remnant warband &middot; late 30s",
                "teaser": "A self-declared prophet who ends alone in the cathedral hall, taking his solitude for proof of his holiness.",
                "bio_html": """<p>A homegrown fringe prophet of Aldrovan stock (Pax Aldrovana) who styles himself &ldquo;Kest the Anointed&rdquo; and leads the Bright Remnant warband. Gaunt and ascetic-thin at about 5'11&quot;, hollow-cheeked and pale, with intense fixed grey-blue eyes, long unkempt prematurely greying hair and beard hung with bone talismans, and self-inflicted ritual scars on both forearms.</p>
          <p>The sheet's final image: after his followers have scattered to loot, Kest stays on alone in the cathedral hall, exhausted and fervent, convinced that his solitude proves his holiness. Its expressions: furious certainty, ascetic resolve, prophetic fervor.</p>""",
                "quote": "The light is not in the heavens, but in those who refuse to forget.",
            },
            {
                "slug": "massinen", "name": "Massinen",
                "epithets": "Warlord of the Tazenna Reach &middot; seventh siege of Ardenwake &middot; 67&ndash;70 years old",
                "teaser": "Commands the seventh siege from a staff and a table of generals, and never reaches the walls.",
                "bio_html": """<p>Warlord of the Tazenna Reach, about seventy, around 5'10&quot;, with dark bronze sun-weathered skin, thin close-cropped white hair and a long white beard, sharp dark eyes in a deeply lined face, and old campaign scars across both forearms. He is drawn at the seventh siege of Ardenwake, relying on his staff and his generals, in sand, cream and desert ochre with weathered brown leather.</p>
          <p>The sheet's closing image is captioned three months into the siege &mdash; he never reached the walls. Its expressions: command, pride, weariness, final resolve.</p>""",
            },
            {
                "slug": "berant", "name": "Berant",
                "epithets": "Chief Engineer, Corvane Imperium &middot; 51&ndash;54 years old",
                "teaser": "Designs the eleventh siege against Ardenwake, and writes the private notes that tell his emperor what a siege cannot do to a holy city.",
                "bio_html": """<p>Chief Engineer of the Corvane Imperium, in his early fifties, lean at about 5'9&quot;, olive and weathered, with salt-and-pepper hair and dark brown eyes. He designs the engineering campaign of the eleventh siege against Ardenwake, including the spire-targeting morale strategy, and he authors the private notes to <a href="../characters/vasarion.html">Vasarion</a> that separate conventional siegecraft from breaking a holy city's morale.</p>
          <p>He wears aged bronze and a charcoal cloak, with brass measuring tools at his belt; the sheet's expressions include determined, tired from campaigns, and skeptical.</p>""",
            },
            {
                "slug": "dorenzo", "name": "Dorenzo",
                "epithets": "Prince of Solvarre &middot; 32 years old",
                "teaser": "Takes the field in ornamental parade armor with Valeria's refusal letter folded inside his breastplate.",
                "bio_html": """<p>Prince of Solvarre, thirty-two: slim, fashionably dressed even on campaign, fine-featured and handsome with a petulant mouth, dark curled hair, dark brown eyes, a thin fashionable mustache and an ornate signet ring. His armor is ornamental parade steel in silver-grey with rich decorative accents, over luxurious Solvarre court colors.</p>
          <p>He carries <a href="../characters/valeria.html">Valeria</a>'s refusal letter inside his breastplate. The sheet pairs two traits: courtly pride, and entitlement refused.</p>""",
            },
            {
                "slug": "corse-0000b", "name": "Corse",
                "epithets": "Steward to King Wendric of Rovain &middot; 55 years old",
                "teaser": "Keeps the paper of the Crown's Due &mdash; and keeps the king's last words out of the ledger.",
                "bio_html": """<p>Steward to King <a href="../characters/wendric.html">Wendric</a> of Rovain &mdash; the office held by <a href="../characters/corse.html">Corse</a> in Case 0000 &mdash; fifty-five, spare and slightly stooped at about 5'7&quot;, with a long, deeply lined face of careful neutrality, grey thinning hair and pale watchful grey-blue eyes. The middle finger of his writing hand carries an ink-stain callus. The sheet lays out his documents: the Crown's Due, the Commission Fiction, a confiscation order, a recall notice, and a wax tablet of private notes.</p>
          <p>He is present with <a href="../characters/wendrics-wife.html">the Queen</a> at Wendric's private breakdown after the king fails to lift Valeria, one of only two witnesses to that hour; after the king's death, the sheet says, he keeps the last words private.</p>""",
                "quote": "A king's last word is not a ledger entry.",
            },
            {
                "slug": "wendrics-wife", "name": "Wendric's Wife",
                "epithets": "Queen of Rovain &middot; 31&ndash;34 years old",
                "teaser": "One of only two witnesses to the hour in which a king learns he cannot lift the sword.",
                "bio_html": """<p>Queen of Rovain and wife of King <a href="../characters/wendric.html">Wendric</a>; a Rovain woman, Anglo-Saxon in appearance, about 5'5&quot;, with a composed court bearing, a fair court-pale complexion, light brown hair in an elaborate court style, hazel eyes and a dignified face that gives little away in public. She wears rich formal court robes.</p>
          <p>She is present alongside <a href="../characters/corse-0000b.html">Corse</a> at Wendric's private breakdown after he fails to lift Valeria, and is one of only two witnesses to that hour.</p>""",
            },
            {
                "slug": "wendrics-son", "name": "Wendric's Son",
                "epithets": "Heir to the throne of Rovain &middot; never crowned &middot; 11 years old",
                "teaser": "Eleven years old when his father dies; the realm is governed in his name by a Regent Council.",
                "bio_html": """<p>Heir to the throne of <a href="../characters/wendric.html">Wendric</a>'s Rovain, never crowned. A slight child of eleven, about 4'6&quot;, fair, with a gentle-featured face, a simple light-brown boy's cut and blue eyes resembling his father's, in plain charcoal-and-ivory court dress with a mourning collar. After his father's death a Regent Council rules in his name.</p>
          <p>The sheet's expressions: gentleness, mourning, bearing duty, quiet hope.</p>""",
            },
            {
                "slug": "yorbulan", "name": "Yorbulan",
                "epithets": "Khagan of the Sarnak Horde &middot; first siege of Ardenwake &middot; 48 years old",
                "teaser": "Leads the first siege on a dying kam's prophetic vision, and dies of winter fever outside walls he never breaches.",
                "bio_html": """<p>Khagan of the Sarnak Horde, forty-eight, with a broad, wind-burned face, black braided hair, dark brown eyes, a long braided mustache and short beard, deeply weathered bronze skin, many old clan war scars and the powerful frame of a horse-warrior. He wears dark leather and iron lamellar in earth and fur-grey tones, with clan tokens on his war gear.</p>
          <p>He leads the first siege of Ardenwake, following a dying kam's prophetic vision. The sheet's last image is the eleventh day before Ardenwake: he dies of winter fever outside the walls after an eleven-day siege, and the walls are never breached.</p>""",
            },
            {
                "slug": "branimir", "name": "Branimir",
                "epithets": "Prince of Belnograd &middot; mid-30s",
                "teaser": "Dies of river fever outside the walls, knowing he will not live to order the assault &mdash; and the grudge ends with him.",
                "bio_html": """<p>Prince of Belnograd, thirty-four to thirty-six, Rus/Slavic in appearance: solidly built at about 5'10&quot;, with a broad, heavy-browed face ruddy from cold-weather campaigning, long dark brown hair often braided back, pale blue eyes and a full beard in the fashion of Belnograd's princely line. His face is prematurely lined, which his advisors attribute to eleven years of privately nursing the campaign. He wears layered mail over a fur-lined coat, a fur-trimmed princely cloak and a curved cavalry saber, with a small icon of his great-grandmother on a cord beneath his armor.</p>
          <p>The sheet shows him pursuing the grudge, then before the final assault, knowing he will not live to order it, then dying of river fever outside the walls; its caption reads that the grudge ends with him, before the siege begins.</p>""",
            },
            {
                "slug": "coren", "name": "Coren",
                "epithets": "First Factor of the Merchant-Council of Velmoro &middot; early 50s",
                "teaser": "Orders the Ardenwake blockade withdrawn the moment the numbers turn unprofitable.",
                "bio_html": """<p>First Factor of the Merchant-Council of Velmoro, in her early fifties: sharp-featured and built for negotiation, with grey-streaked dark hair in a severe knot, dark brown assessing eyes, olive city-pale skin and the ink-stained fingertips of a lifetime of ledgers. She wears deep charcoal and muted burgundy weathered wool and carries a black lacquered ledger-case.</p>
          <p>The sheet shows her at the Ardenwake blockade; she orders it withdrawn when the numbers turn unprofitable. Its expressions: measured, assessing, impatient, cold resolve.</p>""",
            },
            {
                "slug": "verrin", "name": "Verrin",
                "epithets": "Captain, the Free Company of the Blind Ford &middot; 42 years old",
                "teaser": "A mercenary captain the source never describes &mdash; drawn as a scarred, guarded professional.",
                "bio_html": """<p>Captain of the Free Company of the Blind Ford, forty-two: a sturdy, scarred professional soldier at about 5'11&quot;, with a weathered, guarded face of practiced mercenary neutrality, cropped brown hair going grey, brown eyes, short unkempt stubble, and a notched ear from an old campaign injury. His armor is mismatched worn steel, brown leather and dark iron, over faded charcoal.</p>
          <p>The text gives him no physical description; everything above was invented for the sheet.</p>""",
            },
            {
                "slug": "the-wounded-archer", "name": "The Wounded Archer",
                "epithets": "Archer in Aldwick's defense &middot; 16 years old",
                "teaser": "Sixteen, lied about his age to enlist, and retells the story once a year.",
                "bio_html": """<p>An archer in Aldwick's defense, sixteen, slight and still growing at about 5'5&quot;, with light brown cropped hair, brown eyes and fair skin. He fights in borrowed military leathers too large for him, with a simple hunting bow, and carries a healed puncture wound in the lower leg from the siege.</p>
          <p>He lied about his age to enlist, and later retells the story once a year.</p>""",
            },
            {
                "slug": "the-vault-guard", "name": "The Vault Guard",
                "epithets": "Palace Guard, vault entrance &middot; Marrowgate &middot; 28 years old",
                "teaser": "Stands the door of the vault at Marrowgate as a listener and a witness &mdash; and later retells what he saw.",
                "bio_html": """<p>A palace guard of twenty-eight posted at the vault entrance at Marrowgate: solidly built, with cropped brown hair, warm brown eyes, fair weathered skin, a plain attentive face and light stubble. He wears Rovish palace mail and a deep-red-and-cream surcoat, with a spear and a short sword.</p>
          <p>The sheet's expressions are listening, witnessing, retelling the story and attention.</p>""",
            },
        ],
        "scenes": [],
    },
    {
        "slug": "2114", "title": "A Fraction of an Inch",
        "status": ["coming-soon"],
        "cover_file": "2114.jpg",
        "hook": "Arithmetic. Regalia. Convergence. Warning. Still uncounted.",
        "case_tag": "Case 2114",
        "pages": EDITOR_PAGES,
        "genre": EDITOR_GENRE,
        "synopsis_html": EDITOR_SYNOPSIS,
        "characters": [],
        "scenes": [],
    },
    {
        "slug": "2365", "title": "The Decree of Luminescence",
        "status": ["published", "google-books"],
        "cover_file": "2365.jpg",
        "hook": "Ash. Roll. Residue. Append. Nil.",
        "case_tag": "Case 2365",
        "catalyst": {
            "name": "The Round-Bed",
            "meta": "Atmospheric aperture unit",
            "page": "books/2365.html",
            "img": "scenes/the-standing-noon-opens-grid.jpg",
            "html": "<p>A dormant aperture unit buried beneath a threshing-floor by an earlier, unrelated pass of the Corps. Activated once, it parts the ash above a kingdom's capital into a hard-edged column of clear sky and holds it open for four hundred and twenty-one days. It is never retrieved; it still lies, inert, under the floor of the hall that was built over it.</p>",
        },
        "envoy": {
            "name": "Observer 117",
            "meta": "&ldquo;the Reckoner&rdquo;",
            "page": "characters/severin.html",
            "img": "characters/severin-thumb.jpg",
            "html": "<p>Custodian of record for the unit, working under cover as the court astronomer-priest of Vallombra. Files his reports with no first-person pronoun, keeps a private table of the dead children he can name, and on the one evening he exceeds his instructions is recalled from the tower parapet within the day.</p>",
        },
        "pages": "88",
        "google_books_url": "https://play.google.com/store/books/details?id=spIXEgAAQBAJ",
        "genre": EDITOR_GENRE,
        "synopsis_html": """<p>Vallombra is a small, terraced kingdom that rules itself by arithmetic. Its faith, the Concord of the Year, asks only that the sky keep its appointments, and for six hundred years it has. Then the Ashduct hills breathe, and the ash does not stop for three winters. The court astronomer-priest <a href="../characters/severin.html">Severin</a> stretches the year's grace from three days to a season and carries every missed appointment forward like a debt; the beekeeper-king <a href="../characters/faustin.html">Faustin</a> melts down the kingdom's gold circlet for eleven days of bread. A week before the third spring's First Furrow, Severin posts a line no Reckoner has ever posted, one he cannot derive from his own tables: the sun will stand over the Threshing Round at the sixth hour, and the ash will part for it. It does, along a line so straight that nothing in the sky could have drawn it.</p>
          <p>The Standing Noon feeds a starving valley, and it has an outside. Bread is issued by name, from a single Roll compiled in three nights by the Reckoner's apprentices under <a href="../characters/piero.html">Piero</a>, a granary clerk's son who wanted nothing more than to count sacks. In the fourth column of the ninth parish book a copyist's lamp gutters, and three hundred and eleven people of the Saltway Quarter &mdash; northern guests and the Vallombran households that feed them &mdash; are never written down. Severin has already vanished from the tower at dusk, and the parish books are sealed under a law that nobody will be the first to call binding. Hungry Verrenhal marches south behind <a href="../characters/sigrid.html">Sigrid</a>, its Staff-Keeper, who takes one look at the edge of the light and says what no one in Vallombra will hear: nothing in the sky holds a line, so someone is holding this one. A herald's mistranslation of one phrase, the low hour, which means dusk to one nation and noon to the other, sends four thousand uncovered northerners across it in full sun, and for eleven minutes the wardens at the Saltway Gate loose into the glare.</p>
          <p>What follows is an accounting. Faustin ladles soup into the bowls of the men who came against him, and dies of the fever in them. <a href="../characters/marcello.html">Marcello</a>, the Order's first Examiner, reconciles the Roll and finds the missing column, the purchased names and a drift of unread petitions, and he and Piero promise to correct it in the open on the day the child queen <a href="../characters/livia.html">Livia</a> turns twenty-one. Meanwhile Piero needs a sentence strong enough to hold a kingdom together, and it hardens into the Decree of Luminescence: Vallombra becomes Illumaria, a windowless basilica of black marble rises over the Round, and the promised day is deferred, for good reasons, again and again. Each evening at the Gold the tower's book is signed with a single word, <em>Nil</em>. <em>The Decree of Luminescence</em> closes on a Cultivator's own archival log &mdash; Case Study 2,365: one dormant unit beneath a threshing-floor, a Custodian recalled the night he used it, and a record that moves the cause of the war from a clerk's lamp to a neighbor's envy.</p>""",
        "characters": [
            {
                "slug": "piero", "name": "Piero",
                "epithets": "Senior apprentice to the Reckoner &middot; later Regent of Illumaria and first High Pontiff &middot; 21 at the story's opening",
                "teaser": "Wants only to count sacks, hums in threes, and builds a religion out of one vanished master and one sentence he cannot afford to examine.",
                "bio_html": """<p>The left-handed son of the Lower Granary's clerk, taken on at twelve for the neatness of his hand and wanting, from then on, nothing more ambitious than to count sacks. Senior of the seven apprentices of <a href="../characters/severin.html">Severin</a>, he hums when he computes, softly and always in threes: a nursery counting-song of his mother's, eleven verses of loaves, lamps and a door that is always warm, which <a href="../characters/nina.html">Nina</a> sang until she could not. <a href="../characters/marcello.html">Marcello</a> shares his bread crusts on the tower stair and is, without either of them ever saying so, the check to his count.</p>
          <p>On the evening of the Standing Noon the Reckoner lays a brass plumb across his palm, says <em>The residue holds</em>, and is not on the tower when Piero turns round; Piero writes a zero in the book, and the sentence beneath it. He takes the head of the table that compiles the Roll of the Lit, answers the king's question at the Saltway Gate with <em>It was his rule</em> and a stranger's with a sentence that every witness hears as a refusal, and learns from Marcello that the Roll is three hundred and eleven names short. He chooses to append rather than disclose, promising a correction in the open on the day <a href="../characters/livia.html">Livia</a> is twenty-one, and drafts the Decree of Luminescence around the only true things he has: a tower at dusk, and the last words a man said there. The promised day is deferred, again and again, for good reasons. He climbs to take the evening reading for thirty-one years, until a novice, <a href="../characters/aldo.html">Aldo</a>, asks what the command is for. He dies in his fifty-seventh year with the brass weight in his sleeve.</p>""",
                "quote": "Because he told me to.",
            },
            {
                "slug": "severin", "name": "Severin",
                "epithets": "The Reckoner of Vallombra, sixth of that name &middot; Observer 117, Custodian of record &middot; appears about fifty",
                "teaser": "Has never shown a false figure; on the morning of the First Furrow he states one, and the sky is cut open to make it true.",
                "bio_html": """<p>A lean, courteous, unhurried astronomer-priest, sixth of his name to keep the Concord's Table from the tower beside the Threshing Round, who teaches his seven apprentices that a Reckoner who cannot show his work is merely a priest, and a priest is a man who has stopped being checkable. When the Ashduct hills breathe and the sun withdraws, he extends the year's grace from three days to a season and carries the missed appointments forward, entry upon entry. A week before the third spring's First Furrow he nails a line to the tower door that no notice has ever carried: the sun will stand over the Round at the sixth hour, and the ash will part to let it. <a href="../characters/marcello.html">Marcello</a> asks for the derivation. It is not in the tables.</p>
          <p>He is also Observer 117 of the Cultivator Envoy Corps, Custodian of record for a dormant unit beneath the tower. He files reports with no first-person pronoun, is answered with the single word <em>Noted</em>, and keeps in the vault's margin a private table of the dead children he can name, <a href="../characters/nina.html">Nina</a> ninth among them. He activates the unit himself; that evening a recall names the narrow north stair, and he is gone from the parapet before <a href="../characters/piero.html">Piero</a> has finished turning round, with the lamp still burning. He never learns, so far as the file shows, that the Order will worship him as the Kindled Reckoner. Reassigned to a world whose sky is entirely clear, he notes in his first report that it has a great many appointments, and, on a struck-through second line, that nobody there hums when they count.</p>""",
                "quote": "The residue holds.",
            },
            {
                "slug": "marcello", "name": "Marcello",
                "epithets": "Magistrate's son &middot; senior apprentice &middot; the Order's first Examiner &middot; 22&ndash;23 at the story's opening",
                "teaser": "Measures the edge of the light, writes down what it means, and tells no one for five months.",
                "bio_html": """<p>A magistrate's son with an ink-stained thumb and an unshakable conviction that anything which cannot be reconciled has not, in any meaningful sense, happened. He is the friend and the check of <a href="../characters/piero.html">Piero</a>. On the first afternoon of the Standing Noon he is first to the northern edge with a plumb-line and a folding rule, finds a boundary with no penumbra, and writes in the margin of his book <em>Nothing in the sky holds a line. Something holds this one</em>, showing it to no one. At the Saltway Gate he privately suspects that the missing three hundred and eleven are no more than a clerical error, and says only that the Roll is the one rule that has held.</p>
          <p>Named the Order's first Examiner, he reconciles the Roll against the sealed parish books and finds the omitted column, <a href="../characters/nardo.html">Nardo</a>'s forty-one forged names, and the unopened letter under the Reckoner's paperweight. He lays them before Piero with his own confession of five months' silence, and founds the Examiners' Book on its one rule, that nothing is erased and everything is appended. He argues the Decree's clauses with Piero, proposes the windowless Basilica as a control entry, and writes beside the lens <em>We have built the wrong instrument, and named it for the right miracle</em>. He hands the book to <a href="../characters/costanza.html">Costanza</a> in his last lucid week, four winters before Piero dies.</p>""",
                "quote": "We do not erase it, Piero. We append.",
            },
            {
                "slug": "livia", "name": "Livia",
                "epithets": "Princess of Vallombra, then Queen of Illumaria &middot; 9 at her coronation, 21 at the first Judgment &middot; reigns 51 years",
                "teaser": "Notices at nine that her crown has got heavier, and spends fifty-one years never saying so.",
                "bio_html": """<p>The daughter of <a href="../characters/faustin.html">Faustin</a>, nine years old when he dies, crowned in the seventh month on the Round in a circlet of gilded lead washed in vinegar and wine, and held very still for eleven minutes. When the true-gold circlet has been cast and passed through the fire, she asks <a href="../characters/piero.html">Piero</a> in the corridor outside the treasury whether it is the same crown. It is the same crown, Majesty, he says. <em>Then it has got heavier</em>, says Livia, and goes in to her supper.</p>
          <p>At twenty-one she stands alone on the black floor of the Basilica while the beam falls through the Arc onto her head, and glows, and looks faintly amused; the chroniclers record serenity. That night she asks Piero for her father's private ledger, the one with the debt in it, reads it standing to the last line, and says only that he always did carry a debt oddly. She keeps it, and for fifty-one years sends forty wagons of grain to the Saltway Quarter on the anniversary of the First Furrow, without a label. The last line she writes in the ledger is the two words the rule allows for a debt that will not close: <em>Carried forward.</em></p>""",
                "quote": "Then it has got heavier.",
            },
            {
                "slug": "faustin", "name": "Faustin",
                "epithets": "King of Vallombra, called &lsquo;the Fortunate&rsquo; &middot; widower &middot; 49 years old",
                "teaser": "A beekeeping king who sells his crown for bread, breaks the kingdom's first furrow, and dies of the soup he ladles.",
                "bio_html": """<p>A stout, near-sighted, gentle widower whose only known vice is bees: sixteen skeps on the palace roof, one for each lord of his council, every one of them dead by the first spring of the Long Night. He rules by a contract with the year, and in the second winter he has the kingdom's three-hundred-and-forty-year-old gold circlet melted by <a href="../characters/the-goldsmith.html">a goldsmith</a> and sold weight for weight to a southern grain-factor, which buys eleven days of bread. At the First Furrow he walks out alone to turn the first furrow of the year, and the share snaps in two. <em>Then let it be recorded</em>, he says, <em>that I tried.</em></p>
          <p>When <a href="../characters/sigrid.html">Sigrid</a>'s host is blinded and shot at the Gate he rides out bareheaded to stop the arrows, then opens every gate, name or no name, and has <a href="../characters/marcello.html">Marcello</a> do the sum: four thousand seven hundred and twelve more mouths, and a thousand and forty-one dead among his own. He writes it down himself. He ladles soup in the sheds for three months, is told by <a href="../characters/the-granary-physician.html">the Granary's physician</a> exactly what is passing from bowl to bowl, thanks her for the figure, and dies in eleven days among the empty hives. He leaves a daughter, <a href="../characters/livia.html">Livia</a>, a ledger, and a debt, and asks <a href="../characters/piero.html">Piero</a> not to let her think she is wearing the sun.</p>""",
                "quote": "It was only ever a hat, Severin. The bread, I am told, is real.",
            },
            {
                "slug": "sigrid", "name": "Sigrid",
                "epithets": "Warden of the Winter Stores &middot; Staff-Keeper of Verrenhal &middot; 40 years old &middot; later regent for eleven years",
                "teaser": "The one person who says out loud, on the first day, what the light is, and is remembered now as a proverb about landlords.",
                "bio_html": """<p>The king's sister and Verrenhal's Warden of the Winter Stores, a broad, sardonic, sharp-eyed woman who by a hereditary duty nobody can explain also carries and cuts the pale ash-wood calendar staff on which the kingdom's year is tallied, with her dead husband's belt buckle on a thong at its head. Her arithmetic is simpler than the Reckoner's and, across three winters of ash, more accurate: she counts the days between today and the day the barley runs out, and shows <a href="../characters/ragnvald.html">Ragnvald</a> where the staff and the tally cross. She sings, when she believes herself alone, in a voice of such unrelieved flatness that her young nephew once left a room rather than hear the end of a verse.</p>
          <p>She buries her brother under a cairn on the pass, writes the Reckoner a letter on how the light must be made (it lies unopened under a paperweight for five months), and finds at the Saltway Gate a row of a hundred and forty-one dead with their feet toward the gold. She lays her staff across the line, hangs her lead plumb from it and holds it for a hundred breaths in a gale: the weight swings and the edge does not. At the parley she tells <a href="../characters/piero.html">Piero</a> that men are not taken into the light, they go down stairs. Her son <a href="../characters/arne.html">Arne</a> loses his sight at the Blinding, and she never crosses the line herself. She rules Verrenhal as regent for eleven years with the dead king's ring on her thumb, and her one true diagnosis survives only as a saying about landlords.</p>""",
                "quote": "Nothing in the sky has an edge. Someone is holding it.",
            },
            {
                "slug": "arne", "name": "Arne",
                "epithets": "Sigrid's son &middot; 17 at the Blinding &middot; lives to eighty",
                "teaser": "Leads the vanguard down at the low hour with his eyes uncovered, never sees the light again, and becomes the best-loved singer in the north.",
                "bio_html": """<p>Seventeen, rawboned and chewing something that is not food, <a href="../characters/sigrid.html">Sigrid</a>'s son marches south at her side, and is given the vanguard because he is the Staff-Keeper's son and nobody else in the host is still strong enough to walk at its head. <a href="../characters/the-herald-2365.html">The herald</a> has cried the king's promise of the low hour in a tongue where the low hour means noon, and Arne leads four thousand of the best of them down the Saltway in good order and in silence, with their eyes uncovered and, because a northerner does not go among strangers without them, their weapons.</p>
          <p>The glare takes him in the first instant, and <a href="../characters/rufio.html">Rufio</a>'s wardens loose for eleven minutes. His mother finds him kneeling in the road among the dead with both hands pressed to his eyes, alive and permanently blind. He lives to eighty and becomes, to the astonishment of everyone who ever heard her sing, the best-loved singer in the north. Asked late in life by a young skald what the light had looked like, he says he saw it for about as long as it takes to be wrong about a step.</p>""",
            },
            {
                "slug": "ragnvald", "name": "Ragnvald",
                "epithets": "King of Verrenhal &middot; approx. 45 years old",
                "teaser": "A big, tired, honest man with a cough, who chooses to starve on somebody else's road.",
                "bio_html": """<p>The jarl-king of a poor and proud northern realm and <a href="../characters/sigrid.html">Sigrid</a>'s brother, who spends three winters of ash watching the barley run down and is shown, at his own table, the place where the calendar staff and the grain tally cross, three weeks before the ground could be expected to thaw, if it thawed. <em>We can starve in our own halls</em>, he says, <em>or we can starve on somebody else's road.</em> He chooses the road. It is the last decision of his that anyone troubles to count.</p>
          <p>He marches south on the morning the staff names for the first thaw, nine thousand men and a few hundred women with empty barley wagons and the king on a litter behind them, and dies on the ninth day on the last saddle of the pass, of the cough and the cold and the knowledge that he chose wrongly and could not find the other choice. His last order, taken in a voice so thin that Sigrid has to lean into it, is that they go down and find out who is holding the match.</p>""",
                "quote": "We can starve in our own halls, or we can starve on somebody else's road.",
            },
            {
                "slug": "fulvio", "name": "Fulvio",
                "epithets": "Lord of the Weirs &middot; one of the sixteen lords of Vallombra &middot; approx. 54 years old",
                "teaser": "Weeps as loudly as any at the Round, then names the price of his silence.",
                "bio_html": """<p>A sodden, prosperous eel-and-salt lord of the valley's southern mouth, whose harbors bought the crown's gold and whose grain-ships are the last ships left on that coast. In the ninth week after <a href="../characters/faustin.html">Faustin</a>'s funeral he rises at the end of the second hour of the council and proposes, with real regret and evident sincerity, that the king's nine-year-old daughter be betrothed to his own second son, and the regency pass to him until the year should see fit to show its face again. As arithmetic it is sound.</p>
          <p><a href="../characters/piero.html">Piero</a> answers with a retort rather than a theology (<em>It fell on her father's furrow, my lords. It did not fall on the Weirs</em>) and Fulvio sits down, but not before naming his price in the flattest tone of the night: a charter making his grain-ships the Order's sole licensed factor for whatever is to be built on the strength of that noon, and a seat among whoever comes to steward it. Piero grants both. When the Standing Noon closes, House Fulvio's ships bring the first true cargo of iron, glass and southern grain up the coast, at a price the charter fixed in advance.</p>""",
            },
            {
                "slug": "rufio", "name": "Rufio",
                "epithets": "Captain of the Edge &middot; 50 years old",
                "teaser": "Draws every bread-line on the north road for sixteen days, and gives the one order he cannot remember giving.",
                "bio_html": """<p>A broad, honest, careworn captain of the guard, commander of the wardens of the Edge &mdash; palace guardsmen and Granary men in borrowed grey &mdash; who opens the nine gates on the Roll of the Lit and, at the Saltway Gate, turns back with regret and in perfect good order the first of the people whose names cannot be found. He keeps the Order's orders: no armed body is to be admitted to the light on any pretext, and forty thousand people eat from the Gates.</p>
          <p>At the low hour he sees four thousand armed men step across the line into noon, and gives the word. The wardens loose for eleven minutes at what they can see, which is a mass of stumbling figures with their hands held out; two thousand three hundred and four northerners die, and the Order's tally of its own losses is six. It is perfectly true, as he will say once, to the empty room that is the only audience he ever chooses, that the men were armed. They were also blind. He cannot remember, for the rest of his life, which of those two facts he was looking at when he gave the word.</p>""",
            },
            {
                "slug": "nardo", "name": "Nardo",
                "epithets": "Notary, formerly of the Saltway courts &middot; later the Roll's first Registrar of Names &middot; approx. 52&ndash;55",
                "teaser": "Sells forty-one names for eleven bushels of seed barley apiece, and is pensioned for it.",
                "bio_html": """<p>A small, courteous, well-groomed notary with the manners of a family physician and the ethics of a weather-vane, who understands before any clerk in the hall what the Roll has made of the parish books: a scarce good, with a fixed supply and no market. He charges eleven bushels of seed barley, or their equivalent, for a name entered at the foot of a page, and makes forty-one such entries between the second night and the third, in a hand no examination would have told from <a href="../characters/lino.html">Lino</a>'s. He regards the Roll, he says afterward, as the most honest document the valley has ever produced, since it alone admits that being counted is a matter of being written down by someone with a pen, and that a pen, like a lamp, has a price.</p>
          <p>Summoned by <a href="../characters/marcello.html">Marcello</a>, he admits everything with the affability of a man declining a second cup of tea, and is pensioned within the year as the Roll's first Registrar of Names: the only person in the valley competent to say which of its entries are false, and therefore the only one who can never be permitted to say so.</p>""",
            },
            {
                "slug": "costanza", "name": "Costanza",
                "epithets": "Examiner of the Order &middot; Marcello's chosen successor &middot; late 20s",
                "teaser": "Told to enter everything and forgive nothing, she does it for four years without asking the question her predecessor would have asked within the hour.",
                "bio_html": """<p>A stern, exacting young woman who receives the Examiners' Book from <a href="../characters/marcello.html">Marcello</a> in his last lucid week, with a single instruction: <em>enter everything and forgive nothing</em>. She keeps it to the letter for four years, through the death of the man who gave it to her, without once asking <a href="../characters/piero.html">Piero</a> the question Marcello would have asked within the hour. The first page of the book still holds a date, and the promise beside it has been carried forward again and again in a book nobody opens.</p>
          <p>Her sheet gives her a habit the text does not: she holds her pen perfectly still before she writes, as if daring the figure in front of her to be wrong.</p>""",
                "quote": "Enter everything and forgive nothing.",
            },
            {
                "slug": "aldo", "name": "Aldo",
                "epithets": "Novice of the Last Order &middot; later Second High Pontiff &middot; 9 years old as introduced",
                "teaser": "Asks what the command is for, and gets five words and a collapse.",
                "bio_html": """<p>A literal child, brought to the tower that autumn to carry the Reading Book up the stair, who on his seventh evening watches the High Pontiff write <em>Nil</em> for the eleven thousand three hundred and twelfth time and asks the question nobody in the Order has been permitted to ask in thirty years: why do we write it, Holiness, if it is always nothing? <a href="../characters/piero.html">Piero</a> says that it was the Kindled's last command, then that it is for the light, and then, asked why the Kindled commanded it, hears himself say <em>Because he told me to</em>. What follows is not weeping, and Aldo, who tells the story once, fifty years afterward, to his own novices, is very exact on the point. He runs for help down all one hundred and eleven steps, counting them.</p>
          <p>He becomes the second High Pontiff. He writes the Decree's fourth Article, which holds that the empty reading is the fullest and that faithful obedience is the only proof the Sun requires, and writes it, he says, for a man he once saw fall down a stair; and he has the novices of every House of Vigil taught to hum through the evening reading, softly and in threes, until several thousand people who never met a granary clerk's mother are keeping faith, without knowing it, with her song.</p>""",
                "quote": "Why do we write it, Holiness, if it is always nothing?",
            },
            {
                "slug": "lino", "name": "Lino",
                "epithets": "Copyist of the Bell and Granary orders &middot; 14 years old, in his second week of service",
                "teaser": "Trims a guttering wick, loses his place, and skips three hundred and eleven names; dies believing his work was perfect.",
                "bio_html": """<p>A copyist of fourteen with a small, neat, unhurried hand and an unusual gift for staying on the line, placed by an uncle of the Bell order who wished, in the winter of the ash, to see one member of the family securely employed near a fire. He sits at the far end of the long table, nearest the failing lamp, with a wick cut from the hem of somebody's shirt, while forty copyists compile the Roll of the Lit in the dark.</p>
          <p>At the ninth hour of the night he comes to the Saltway Quarter: three hundred and eleven names in a single close-written column, the fourth of the ninth parish book. The wick gutters. He trims it, loses his place for the length of time it takes a small flame to steady, finds it again at the head of the next column and copies on, and it does not occur to him, then or for sixty years, that a page ought to have been longer. He is promoted in his thirtieth year to the head of the copying-hall and honored in his seventieth as the First Fair Hand of the Order, whose flawless Roll is the model of all faithful record. He is never told. <a href="../characters/marcello.html">Marcello</a> writes in the Examiners' Book on the day of the investiture: <em>Fair copy. Wrong. Honored.</em></p>""",
            },
            {
                "slug": "nina", "name": "Nina",
                "epithets": "Daughter of the Lower Granary clerk &middot; Piero's sister &middot; 9 years old at her death",
                "teaser": "Sang the counting-song on the second night of the first winter until she could not.",
                "bio_html": """<p>Nine winters old when she dies in the granary house, on the second night of the first winter of the ash, having sung her mother's nursery counting-song, eleven verses of loaves, lamps and a door that is always warm, until she could not. She is the ninth entry in <a href="../characters/severin.html">Severin</a>'s private table of the dead children he can name. She is never shown alive; her sheet draws her only as she is remembered. Her brother <a href="../characters/piero.html">Piero</a> goes on singing the song under his breath, in threes, through the three years before the Standing Noon and the thirty-one after, as though the tune were a column that had to be carried forward or the whole account would fail to balance.</p>
          <p>The song outlives them both. <a href="../characters/aldo.html">Aldo</a> has the novices of the Order taught to hum it through the evening reading, and in the mouths of several thousand people who never met her mother it becomes a liturgy.</p>""",
                "quote": "Nina, daughter of the Lower Granary clerk, aged nine winters; sang.",
            },
            {
                "slug": "tito", "name": "Tito",
                "epithets": "Plough-boy &middot; nephew of the two brothers who draw the ceremonial plough &middot; 13 years old",
                "teaser": "Leads the plough at the First Furrow and thinks, mostly, about not crying in front of the king.",
                "bio_html": """<p>A thirteen-year-old plough-boy who leads the ceremonial plough at the First Furrow of the third spring. The oxen have been eaten, so it is drawn instead by his two uncles, a pair of Granary brothers who have not eaten since Tuesday. He walks thinking mostly about how he must on no account cry in front of the king, and secondarily about how neither of his uncles will be able to stand much longer.</p>
          <p><a href="../characters/faustin.html">Faustin</a> takes the handles. The share goes into the crust of frozen ash and bites for perhaps a foot, and then there is a crack that every person present will remember, and the wooden share, which has turned the first furrow of the kingdom for three hundred and forty springs, snaps clean in two.</p>""",
            },
            {
                "slug": "the-goldsmith", "name": "The Goldsmith",
                "epithets": "Palace goldsmith of Vallombra &middot; approx. 47 years old",
                "teaser": "Weeps into the crucible while he melts the crown of the kingdom, and is paid extra to stop.",
                "bio_html": """<p>The goldsmith who, in the second winter, melts the kingdom's plain band of river-gold, three hundred and forty years old and worn at every First Furrow since the first Faustin, in the palace forge on <a href="../characters/faustin.html">Faustin</a>'s order, and weeps into the crucible so steadily that he has to be paid extra to stop. The gold is sold weight for weight to a southern grain-factor and buys forty thousand loaves, which is to say eleven days. The same week he casts a second circlet of gilded lead, so like the first that he, the treasurer and the king have some difficulty afterward remembering which was which.</p>
          <p>The only other person in the palace who knows is <a href="../characters/severin.html">the Reckoner</a>. Nobody in the High Realm's later centuries will say that the first crown of the Sun's kingdom was sold for bread by a beekeeper; it will be recorded instead that it endured the flame. Whether the Order's goldsmith, who later casts a true-gold circlet in a single night, is the same man, the text does not say.</p>""",
            },
            {
                "slug": "anselmo", "name": "Anselmo",
                "epithets": "Master glassmaker of the Glassmakers' Row, Illumaria &middot; approx. 52 years old",
                "teaser": "Grinds the Sol-Focus Arc by hand for eleven years and dies of the grinders' lung, having written down nothing.",
                "bio_html": """<p>Master of the Glassmakers' Row and of the guild commissioned by the Order to make the Sol-Focus Arc, a lens the diameter of a cartwheel, to catch and concentrate the single shaft of true sun that falls through the oculus of the Grand Basilica. He and his guild grind it by hand across eleven years, and die within a decade of finishing it, one after another, of the grinders' lung, with none of them having written down how.</p>
          <p>It is a very fine instrument. It is also, as <a href="../characters/marcello.html">Marcello</a> notes on the night it is unwrapped, an instrument that gathers a light it had not made, where the Standing Noon had parted a dark it had not touched. His sheet gives Anselmo hands silvered with embedded glass dust and a dry cough in the lens's later years.</p>""",
            },
            {
                "slug": "the-granary-physician", "name": "The Granary Physician",
                "epithets": "Physician of the Granary order &middot; approx. 44 years old",
                "teaser": "Tells the king exactly what is in the soup, and is thanked for the figure.",
                "bio_html": """<p>A tired woman who has buried a husband and two apprentices that winter, the physician of the Granary order tells <a href="../characters/faustin.html">Faustin</a> in the second week of the sheds that a fever is passing from bowl to bowl, that no room in Torrecalda is large enough to keep the sick from the well, and that there is no fuel to spare for boiling the bowls, since the fuel that would have boiled them is the fuel that bakes the bread.</p>
          <p>The king thanks her for the figure and goes on ladling. He dies of it in eleven days. Her sheet draws her in a plain undyed coat over a widow's dark clothing, with a satchel whose herbs and instruments the famine has depleted, and a level, plain delivery even for the worst news.</p>""",
            },
            {
                "slug": "the-tanners-widow", "name": "The Tanner's Widow",
                "epithets": "Widow of Torrecalda's tanning trade &middot; 35&ndash;38 years old",
                "teaser": "Lost three children, and did not care who heard her call the light a door.",
                "bio_html": """<p>A tanner's widow in the crowd at the First Furrow, who has lost three children and does not care who hears it. When the ash draws back and the shaft of noon falls on the Round, by evening it has been called a pillar, a stair, a spear and a throne. She calls it a door.</p>
          <p>It is one line in the account of that evening. The name that sticks belongs to <a href="../characters/the-nameless-girl.html">a girl who had never seen a noon in her life</a>.</p>""",
                "quote": "A door.",
            },
            {
                "slug": "the-nameless-girl", "name": "The Nameless Girl at the Round",
                "epithets": "A child in the crowd at the First Furrow &middot; about 10&ndash;12 years old",
                "teaser": "Had never seen a noon in her life, and shouted its name over and over.",
                "bio_html": """<p>A girl in the crowd on the Threshing Round who has never seen a noon in her life, and who shouts the first name of the light over and over, in the voice of someone identifying a stranger at a funeral: <em>Noon! Noon! Noon!</em> It is entered in the tower's record that afternoon as the Standing Noon, and it sticks through every chronicle and every later hymn.</p>
          <p>She is never named. The text gives her only that she has never seen a noon, so her age and her famine-hollowed look are her sheet's own.</p>""",
                "quote": "Noon! Noon! Noon!",
            },
            {
                "slug": "the-senior-clerk-of-the-hall", "name": "The Senior Clerk of the Hall",
                "epithets": "Senior clerk overseeing the compiling of the Roll &middot; approx. 56 years old",
                "teaser": "Orders the working papers burned so that nothing can disagree with the fair copy: the first ruling of the Last Order to be remembered as doctrine.",
                "bio_html": """<p>The senior clerk of the long hall beneath the tower's north wing, where forty copyists of the Bell and Granary orders compile the Roll of the Lit by the yellow ration of seven lamps. At the coldest hour before dawn he orders the working papers burned in the braziers, the copyists, who have been writing in gloves cut down to fingerless stumps, not needing to be asked twice, and the parish books sealed in their chests.</p>
          <p>The tally sheets, the scrap on which each page was first drafted and on which the omission <a href="../characters/lino.html">Lino</a>'s lamp had made would have been visible to anyone who laid one beside the other, go into the coals with a small, warm, sighing sound. He explains, to nobody in particular, that a record that existed twice was a record that could disagree with itself. It is the first ruling of the Last Order that will be remembered as doctrine, and it was made for the sake of a fire.</p>""",
                "quote": "A record that existed twice was a record that could disagree with itself.",
            },
            {
                "slug": "the-interpreter", "name": "The Interpreter",
                "epithets": "Interpreter with Sigrid's party at the Saltway Gate &middot; approx. 38 years old",
                "teaser": "Renders a sentence faithfully into the northern tongue, and so renders it as a refusal.",
                "bio_html": """<p>The tired interpreter who stands beside <a href="../characters/sigrid.html">Sigrid</a> at the parley on the twentieth day. When <a href="../characters/piero.html">Piero</a> answers her in the old tongue with <em>Let no shadow claim what shadow did not make</em>, meant as a confession that the light belongs to none of them, the interpreter renders it as a refusal. So do the wardens, and so, in due course and in every succeeding century, does the Decree.</p>
          <p>The text gives only &ldquo;a tired interpreter&rdquo;; the sheet says outright that the gender, age and appearance it shows are invented for consistency.</p>""",
            },
            {
                "slug": "the-herald-2365", "name": "The Herald",
                "epithets": "Herald, clerk of the Gate order &middot; approx. 24 years old",
                "teaser": "Cries the king's promise through the northern camp, faithfully and completely, in a language where the low hour means noon.",
                "bio_html": """<p>A nervous clerk of the Gate order who learned the northern speech from a nurse. On the night after the parley he cries <a href="../characters/faustin.html">Faustin</a>'s promise through the northern camp, in that language, faithfully and completely: that the king will open the Gate to <a href="../characters/sigrid.html">Sigrid</a>'s host on the following evening, at the low hour, when the light lies gentle.</p>
          <p>In doing so he makes the single error of the whole affair that no one on either side will ever be able to trace to a single hand. The old tongue's word for the low light of evening is, in the northern speech, the word for the low sun of a northern noon: the standing joke of the Saltway Quarter, of which no clerk of the palace has ever heard. Sigrid, who understood the promise correctly as dusk, is three miles away arguing with a wagon-master about the linen when he cries it.</p>""",
            },
        ],
        "scenes": [
            {"slug": "the-share-breaks",
             "alt": "A bearded man in a rough cloak and a gold band stands over a snapped wooden plough in a frozen field before a vast crowd, with a tall spired city behind under a grey sky",
             "caption_html": """<a href="../characters/faustin.html">Faustin</a> takes the handles at the First Furrow, and the share that has turned the kingdom's first furrow for three hundred and forty springs snaps in two."""},
            {"slug": "the-standing-noon-opens",
             "alt": "A shaft of white-gold light falls through a ring of clear sky onto a tall tower above a dense crowd on a paved square, under dark ash cloud",
             "caption_html": """At the sixth hour the ash draws back along a line no compass could better, and a single shaft of noon falls on the Round, the tower and thirty-one thousand upturned faces."""},
            {"slug": "the-crowds-come-to-the-light",
             "alt": "A stone bell tower beside a wall of golden light at dusk, hooded townspeople walking toward it down a wet street",
             "caption_html": """By evening the light has an outside, and every road in the valley is full of people walking toward it."""},
            {"slug": "piero-reads-the-gold",
             "alt": "A young man with dark hair in a grey hooded robe looks back over his shoulder on a stone parapet at sunset, a lit lantern on the wall and a brass plumb hanging from a cord",
             "caption_html": """<a href="../characters/piero.html">Piero</a> on the parapet at the hour of the Gold, with the brass plumb on its cord and the lamp lit: the first of the evening readings he will take for thirty-one years."""},
            {"slug": "the-reckoner-is-taken-up",
             "alt": "An elderly white-haired man in a grey robe dissolves into drifting particles on a dim stair, one hand reaching toward a boy who reaches back, a lantern burning above them",
             "caption_html": """At the Gold the grey lid breaks for the length of one breath, and when the apprentice opens his eyes <a href="../characters/severin.html">Severin</a> is no longer on the tower; only the lamp is still burning."""},
            {"slug": "the-lamp-that-guttered",
             "alt": "A young copyist in a dark robe trims a lamp wick at a long candlelit table of open ledgers in a vaulted hall with frosted windows, rows of copyists beyond him",
             "caption_html": """<a href="../characters/lino.html">Lino</a>, fourteen and in his second week, trims a guttering wick and loses his place. The next column he copies is Wool Lane, and three hundred and eleven names are not on the Roll."""},
            {"slug": "the-host-crosses-the-pass",
             "alt": "A woman in grey furs holding a tall staff leads a long column of hooded figures and wagons through a snowy mountain pass, a bearded man lying on a cart beside her and a boy walking at its wheel, a gold glow far down the valley behind them",
             "caption_html": """The host of Verrenhal comes down the pass in the ash, the light a gold coin far below: <a href="../characters/sigrid.html">Sigrid</a> at its head with the calendar staff, <a href="../characters/ragnvald.html">Ragnvald</a> on his litter, and <a href="../characters/arne.html">Arne</a> beside the cart."""},
            {"slug": "sigrid-reads-the-edge",
             "alt": "A woman in a tattered cloak holds a staff across the edge of a wall of golden light, a small weight hanging from it, on a dark ash-strewn hillside",
             "caption_html": """<a href="../characters/sigrid.html">Sigrid</a> lays the calendar staff across the line, hangs her lead plumb from it and holds it a hundred breaths in a gale: the weight swings, and the edge does not."""},
            {"slug": "the-parley-at-the-saltway-gate",
             "alt": "Two groups face each other across a sharp line between golden daylight and black ash; on the lit side a young man in a grey cloak with two companions, on the ash side a woman with a tall staff, a helmeted soldier and a man holding a large book",
             "caption_html": """The parley across the line, bright inside and black outside: <a href="../characters/piero.html">Piero</a> in the Reckoner's grey faces <a href="../characters/sigrid.html">Sigrid</a>, and a sentence he did not know he knew goes over the line as a refusal."""},
            {"slug": "the-blinding",
             "alt": "Archers loose arrows from a shadowed foreground into a golden-lit field where a crowd of figures stumble and fall in the glare, a hilltop castle on the dark horizon",
             "caption_html": """<a href="../characters/arne.html">Arne</a> leads four thousand northerners across the line at the low hour, eyes uncovered, and the wardens of <a href="../characters/rufio.html">Rufio</a>'s Edge loose for eleven minutes at figures who cannot see them."""},
            {"slug": "the-king-ladles-the-soup",
             "alt": "A bearded man in a linen apron ladles soup from a steaming cauldron into a bowl held out by a bowed man in a long queue under a canvas awning hung with banners",
             "caption_html": """<a href="../characters/faustin.html">Faustin</a> in a linen apron over plain wool, ladling soup in the great canvas sheds on the Round every evening for three months, to the men who had tried to reach him through a light that blinded them."""},
            {"slug": "marcello-reconciles-the-roll",
             "alt": "A young man with dark hair sits cross-legged among open parish books and loose pages by an oil lamp in a dim study",
             "caption_html": """<a href="../characters/marcello.html">Marcello</a> reconciling the Roll against the sealed parish books, and following a leak of three hundred and eleven names down the pages to a single column: the fourth of the ninth book."""},
            {"slug": "the-child-queen-is-crowned",
             "alt": "A girl in a pale gold-trimmed gown and cloak with a circlet on her braided hair stands alone on a round of paving between rows of robed lords and priests beneath dark banners",
             "caption_html": """<a href="../characters/livia.html">Livia</a>, nine years old, in a circlet of gilded lead washed in vinegar and wine, holds very still on the Round for eleven minutes."""},
            {"slug": "the-grand-basilica",
             "alt": "A vast windowless black domed hall of dark columns, a single narrow shaft of white light falling from a round opening at the crown of the dome onto the floor, a few small robed figures along the walls",
             "caption_html": """The Grand Basilica of Sol-Invictus, raised over the Round in black Ashduct marble with walls forty feet thick and one shuttered oculus set in the axis of the vanished column: a room built to hold nothing, as <a href="../characters/marcello.html">Marcello</a> argued, so that the true light might be seen for what it was."""},
            {"slug": "the-first-judgment",
             "alt": "A woman in a pale gold-embroidered gown and a fine circlet stands alone on a polished black cracked-marble floor in a tall beam of golden light, in darkness",
             "caption_html": """The first Judgment: every torch doused, <a href="../characters/livia.html">Livia</a> alone on the black floor, the beam falling through the Arc onto her circlet. The gold flares, the room weeps, and the queen looks faintly amused."""},
        ],
    },
    {
        "slug": "2231", "title": "The Stone of the Clean Hand",
        "status": ["coming-soon"],
        "cover_file": "2231.jpg",
        "hook": "Cat. Hand. Stone. Signature. Omitted.",
        "case_tag": "Case 2231",
        "catalyst": {
            "name": "The Kiyote Pair",
            "meta": "Matched one-way matter-transit stones",
            "page": "characters/the-kiyote-pair.html",
            "img": "covers/2231-stone-thumb.jpg",
            "html": "<p>A matched pair of one-way matter-transit stones, dressed by the same hand as a shrine ordeal-stone in one realm and as a village tally-stone in another. The sender works on bare open-palm contact alone: cloth, a broom, or the backs of the fingers do not register. The receiver was set first. A short column of notches cut into the flank of each, one, one, two, three, five, eight, is the Envoy's standing signature and does nothing. All the sending realm ever sees of the device is absence.</p>",
        },
        "envoy": {
            "name": "Observer 618",
            "meta": "&ldquo;the Dumb Mason&rdquo;",
            "page": "characters/observer-618.html",
            "img": "characters/observer-618-thumb.jpg",
            "html": "<p>Custodian of record for the Pair, working under cover as a mute stonecutter who dresses both blocks and then takes a quarry-hand's post beside the one that receives, keeping it for thirty-one years. Files in the third person, latches a quarry gate every evening and then walks back to try it, and on one winter night leaves it unlatched for a party already in flight.</p>",
        },
        "pages": EDITOR_PAGES,
        "genre": EDITOR_GENRE,
        "synopsis_html": EDITOR_SYNOPSIS,
        "characters": [
            {
                "slug": "observer-618", "name": "Observer 618",
                "epithets": "Cultivator Envoy and Custodian of record for Case 2231 &middot; a mute stonecutter, called the Dumb Mason by the shrine's priests &middot; appears about 45&ndash;50",
                "teaser": "Dresses both ends of a matched pair of stones, may not answer the one question he is asked, and leaves a gate unlatched.",
                "bio_html": """<p>A lean, silent man in a leather apron with a satchel of chisels, who answers the Left Ministry's call for a shrine-stone with the lowest of three bids and then works the block for eleven days at Mikusa, tapping and pausing with his head tilted, as a physician sounds a chest. At the end he cuts a short column of notches into its flank, one, one, two, three, five, eight, and walks away down the cedar approach. The shrine's priests call him the Dumb Mason and take the notches for his mark. He had dressed the receiving block first, in a village green on the far side of the world, and stays on there as a quarry-hand. His instruction for the one event he came to see is a single word: <em>observe</em>.</p>
          <p>When the stranger who came out of the stone draws the column of notches in the dust and turns his palms toward the east, he gives neither answer; the bar on correcting a subject's reading, he reasons, extends to confirming it. His reports record, as a deviation with no operational reason given, that he latches the quarry gate each evening and then walks back up the road to try it, and note that he has begun to leave the heel of his bread on the green's stone at dusk. On the night the village burns he stands at the quarry gate with a lantern and, as the fleeing party reaches it, steps aside and lets it swing open. Nineteen years on, on the first of Averin, he reduces the western stone to dust and recovers the eastern, and the stranger, finding the hollow on the green, walks over and bows to him. He returns the bow, the only answer he is permitted, and leaves the post that night without collecting the bread. The reviewing desk has not yet replied to whether he observed or rescued. The Custodian of Case 0202, <a href="../characters/observer-551.html">Observer 551</a>, passes him three times in the character of a rat-catcher, and the courtesy is exact.</p>""",
            },
            {
                "slug": "the-kiyote-pair", "name": "The Kiyote Pair",
                "epithets": "Catalyst of Case 2231 &middot; the Ordeal Stone of Mikusa and the Doorstone of Vilarnau &middot; set eleven and twelve years before the opening",
                "teaser": "Two blocks of grey granite dressed by one hand, which send a man across the world and show the sending realm only an absence.",
                "bio_html": """<p>A matched pair of one-way transit stones, each a grey granite block with a single green vein &ldquo;like a vein in a wrist&rdquo; and, cut into its flank, a short column of notches in clusters: one, one, two, three, five, eight. The receiver was set first, as routine instrumentation, in the moot-green of Vilarnau under the oak, where the Charter makes it the village's tally-stone: waist-high, three paces long, a ruled scale cut across its top and an oak beam beside it for the weights. The sender was dressed eleven years before the opening, after the Left Ministry bought a shrine-stone at the lowest of three bids, and stands at Mikusa as a knee-high block on a plinth of black cedar behind a straw rope. A mute stonecutter dressed both. He proposed no ordeal and supplied no doctrine; the Ministry named the stone's purpose for itself. The notches are his standing signature and do nothing.</p>
          <p>The sender works on bare open-palm contact alone. Through cloth, a broom or the backs of the fingers it registers nothing, which is why <a href="../characters/jokei.html">Jōkei</a>, who sweeps it every morning for eleven years, is never sent. A hand laid on it turns a man into a pale grain that pours sideways into the stone like sand through the neck of a glass, and the receiver pours him out again on the far side of the world; it cannot be reversed. In the east the device has no output but absence, which a court reads as a verdict. In the west it has no stated function at all: a tally-stone is a tally-stone, until a stranger comes out of it and the village starts touching it on its way to somewhere else. Two iron wedges break on its flank and a third rebounds without leaving a mark, and a fire that takes the thatch of the lane leaves it standing in the heat with a charred wreath of ivy. In the nineteenth year the western block is reduced to dust, leaving a clean rectangular hollow, and the eastern is recovered at the same instant; Jōkei finds on its plinth a low heap of pale dust in the exact shape of a stone. The sheet's slate grey, jade-green vein and moss on the shaded side are its own color notes; the manuscript gives the grey, the green vein, and the moss in the last years. Case 0202 gives the Stone one more use, by a hermit of Val Muta named <a href="../characters/vara.html">Vara</a>, who kneels at it with a short bent tool and makes it, for one dusk, not one-way; that file and this one tell the end of the Stone differently, and the pages are not reconciled.</p>""",
            },
            {
                "slug": "shizuka", "name": "Shizuka",
                "epithets": "Tomobe no Shizuka &middot; wife of Tomobe no Higaide, daughter of a provincial scholar &middot; 29 years old at the story's opening",
                "teaser": "The only person who asks how he looked, and who then does the sum and decides, at great cost, not to press it.",
                "bio_html": """<p>A tall woman who walks as though the floor owed her something, and who at nineteen was the only person in the capital to read one of the poems of her future husband, Higaide, aloud, to its author, with a perfectly straight face. She keeps every sheet of his verse in a lacquer box under the dressing-table because they are, she says, the best things in the house. On the night before the ordeal she reads him one about a heron in the rain, tells him that if it is a mistake he will be extremely angry afterward and that she is looking forward to it, and takes his strong left hand and turns it over, as though to learn it like a poem.</p>
          <p>Two days after the notice she goes to Mikusa and asks the Warden, <a href="../characters/jokei.html">Jōkei</a>, how Higaide had looked and whether his sentence was entered, and then to the Bureau of Inquiry, where an Examiner among his sparrows tells her only that a report existed and was eleven sheets long. She does the sum, and does not press it, not with a daughter of six and a court whose beneficiaries would hear a question about the Law's foundations as a confession. She takes the child north to Fort Shirakane, keeps a small school there for the garrison's daughters, and declines the estate offered when the Law lapses. Every first frost she tastes the plum brine with her eyes shut and says, to the empty room, that he would have complained about the salt. She does not learn, within the period of this record, that he lived.</p>""",
            },
            {
                "slug": "tsuru", "name": "Tsuru",
                "epithets": "Daughter of Tomobe no Higaide and Shizuka &middot; 6 years old &middot; later a tall woman who keeps the lacquer box",
                "teaser": "Comes about a practical matter, asks whether the plums will be ready, and falls asleep holding his sleeve.",
                "bio_html": """<p>Six years old, put to bed hours before the ordeal and, with the thoroughness of children, not staying there. On the night of the nineteenth of Garren she appears in the doorway of the eastern hall in her nightrobe, her hair half out of its braid, and asks her father, in a voice that tries hard to be that of a girl who has simply come about a practical matter, whether the plums will be ready before he comes home. He kneels and redoes the braid, which he has never been permitted to do and does badly, and says that the jars will be opened at the first frost, as always, and that he will taste the brine himself. She finds this satisfactory. She yawns, in a way that suggests the whole interview was a ruse to be carried to bed, and is asleep before they reach the gallery, her damp small fist closed round the end of his sleeve.</p>
          <p>He does not come home. On the fourth of Iverin, at the first frost, she stands in the doorway of the cool north room in her nightrobe and watches her mother taste the brine with her eyes shut, and says nothing. They go north by ox-cart to Fort Shirakane, where her father's cousin takes her onto his shoulders and she sleeps in a corner of the long room under his cloak. In her mother's last weeks in the capital a stooped Examiner corrects a clerk's error: a daughter's name is carried off the Tomobe roll and onto her mother's father's, so that the Bureau's list of the Tomobe disgraced comes at the last to a commander, a captain and a wife, and omits a child. She grows into a tall woman who walks as though the floor owed her something, keeps the lacquer box, and reads every poem in it aloud, with a perfectly straight face, to her own children. The manuscript gives her six years, the braid, the box and the plum tree; the sheet's &ldquo;about 25 as a woman&rdquo;, pale ivory skin and white nightrobe are its own.</p>""",
            },
            {
                "slug": "jokei", "name": "Jōkei",
                "epithets": "Warden-Priest of Mikusa Shrine &middot; 60 at the story's opening, 79 when the Stone comes apart",
                "teaser": "Sweeps the Stone every morning for eleven years and never once lays his bare palm on it.",
                "bio_html": """<p>A bald, mild, apologetic priest who tended the hillside shrine of Mikusa for thirty years before the Stone arrived, in which time he presided over some seven hundred weddings and a larger number of funerals. He sweeps the ordeal court with a broom and wipes the block with a damp cloth, and has never in eleven years set his bare palm to it; the backs of his fingers have found it cold in summer and, in winter, faintly warm. He sits with the accused as the Law requires, and with <a href="../characters/shizuka.html">Shizuka</a>'s husband he goes further, pointing out a door at the back of the chamber, the most dangerous sentence of his life. He is told there is no door for an innocent man.</p>
          <p>He writes the finding in the Book of the Ordeal and, under it, without being told, the Captain's one sentence. He gives <a href="../characters/shizuka.html">Shizuka</a> the whole account. By the third hand he watches go, <a href="../characters/kanemichi.html">Kanemichi</a>'s, he has begun to keep a tally on the inside of his sleeve with a thumbnail, because someone ought to. At seventy-nine he finds the Stone come apart into a low heap of pale dust in the exact shape of itself, sweeps the last of it into the rill, and enters one line: that the Stone has gone and the kami has given no reason. He leaves untouched the former Minister's signed sheet pasted into the last leaf.</p>""",
            },
            {
                "slug": "three-senior-priests", "name": "The Three Senior Priests of Mikusa",
                "epithets": "Senior priests under Warden Jōkei &middot; witnesses at the ordeal court &middot; 35, 48 and 55 by their sheet",
                "teaser": "Three white-robed men on a dais who watch a captain go, and are not heard to say a word.",
                "bio_html": """<p>Warden <a href="../characters/jokei.html">Jōkei</a> of Mikusa has a staff and a ledger, and among his priests three seniors, who sit with him in their white robes among the nine witnesses on the morning the Captain of the Left Gate Guard is brought to the Stone: the two officers of the Bureau of Inquiry, Jōkei and his three senior priests, the boy who carried the lantern, the Right Minister, and the Minister of the Left. What the nine see is argued over for the rest of their lives, and each account is slightly different and each sincere: a pale grain pouring sideways into the stone, and a sound that two of them call a bowl being set down on a table and one a breath let out.</p>
          <p>None of the three is named, aged or given a line, and the manuscript does not say which of the witnesses gave which account. When <a href="../characters/sukenori.html">Sukenori</a> is brought to the same dais in the second winter of the Rising, of the nine witnesses of that morning only three are left to see him, &ldquo;the others having been taken by the Law, or the Rising, or the plain exhaustion of men who have been present at something&rdquo;; it does not say which three. The sheet supplies the rest: ages of 35, 48 and 55, shaven faces, black-to-grey topknots, white-knuckled hands in their sleeves, the pale blue trousers under the white robes, and the shrine staffs they carry. The white robes are the manuscript's; the figures and the faces are the sheet's own.</p>""",
            },
            {
                "slug": "sukenori", "name": "Sukenori",
                "epithets": "Kan no Sukenori &middot; Right Minister of Himuro &middot; about 62 years old by his sheet",
                "teaser": "Asks, gently, whether the Law applies to everyone, and is the one Minister to find out that it does.",
                "bio_html": """<p>A precise, fastidious man who has disliked Sugino no Arikuni for thirty years in the way one dislikes a colleague whose excellence one has been compelled to admire. He has never confided in a living person and has therefore invented a confidant: every petition the Minister of the Left has disposed of in three decades, he has read in copy and written beneath it the ruling he judged his rival would give, and he was right in all but four, which he keeps on top. On the day of the pyre he mentions the Fifth Article in the gentlest possible voice, with the air of a man inquiring whether the law applied to everyone; he does not think he is setting a trap, only asking a question to which either answer will serve. He co-seals the summons without asking to see the Examiner's report, because it was convenient not to ask. At Mikusa he sits with his hands on his knees, scrupulously neutral, tells Higaide gently that the Law does not forbid him one sentence before he touches the Stone, and declines afterward to describe the sound the Stone made. At the Reading of the Tally he answers <a href="../characters/sadamune.html">Sadamune</a>'s missing denominator courteously and exactly: a man who has gone cannot be offered in evidence.</p>
          <p>What he saw frightens him, and he reasons that a thing so exact should be put to work as a law rather than left to be a doom. He proposes that a Law which reaches a captain for a death at a rite should reach a granary for a loss of rice; Arikuni says Yes, and the extension is drafted within the week in Sukenori's own hand and is very well made. In the second winter of the Rising a faction of provincial counsellors summons him to Mikusa on a charge of disloyalty of the hand. He goes in the same plain palanquin, early, and thanks <a href="../characters/jokei.html">Jōkei</a> by name, which in thirty years he has never done for a servant of any shrine. He leaves in his study the lacquered box of petitions with the five he misjudged laid uppermost; a nephew finds it and nobody reads it. Before the Stone he says that it is an admirable instrument and that he finds, on the whole, that it does apply. He puts out his hand. The sheet's sixty-two years, grey-white topknot, thin moustache and ink-stained finger are its own.</p>""",
            },
            {
                "slug": "sadamune", "name": "Sadamune",
                "epithets": "Ki no Sadamune &middot; Secretary of the Bureau of Inquiry &middot; 43 years old &middot; later Governor of a northern province",
                "teaser": "Reads the Stone's tally to a room pleased with it, and puts a denominator under the figure.",
                "bio_html": """<p>A dry, upright, fastidious man who holds the post of Secretary because nobody else at the Bureau can be trusted to count. For a fortnight he reconciles the Warden of Mikusa's entries against his own, and at the quarterly Reading of the Tally he stands in the Hall of the Two Seals with the Book of the Ordeal open on his forearm and reads it out: nine accused in a little over eleven years, five confessed and beheaded at the Southern Gate, four who put out a hand and were taken. <em>Four for four</em>, says the Deputy Minister, with real pleasure, and the whole dais warms to it.</p>
          <p>He had been told in the corridor that a man who reads a tally and sits has done his duty, and finds he cannot be that man. Either the Stone takes the guilty and refuses the innocent, he says, or it takes whoever puts a hand to it, in which case four of four describes the stone and not the hands. The Bureau has no instrument to tell the two apart. The Right Minister answers him courteously and correctly: a man who has gone cannot be offered in evidence. The remark is entered as &ldquo;a procedural observation, not pursued,&rdquo; and within the month he is made Governor of a northern province whose principal export is weather, where he governs honestly for nineteen years and writes nothing further about stones.</p>""",
            },
            {
                "slug": "deputy-minister-of-the-left", "name": "The Deputy Minister of the Left",
                "epithets": "Deputy Minister of the Left &middot; unnamed &middot; about 52 years old by his sheet",
                "teaser": "Says &ldquo;four for four&rdquo; with real pleasure, of the one figure in the Book that nobody has put a denominator under.",
                "bio_html": """<p>He has one sentence in the manuscript. At the quarterly Reading of the Tally in the Hall of the Two Seals, in the third week of Averin, the Secretary of the Bureau of Inquiry, <a href="../characters/sadamune.html">Sadamune</a>, reads out from the Book of the Ordeal the record of nine accused in a little over eleven years: five confessed and were beheaded at the Southern Gate; four put out a hand, and the Stone took four. &ldquo;Four for four,&rdquo; says the Deputy Minister of the Left, with real pleasure, and the particular warmth that a room gives to a figure it has been hoping for goes down both rows of the dais. It is a very good figure, the best that any law in the history of the realm has produced, and it requires no explanation; and it is, as the Secretary has known for a fortnight, the only figure in the Book that nobody has thought to put a denominator under.</p>
          <p>That is the whole of him. The manuscript gives him no name, age or appearance, does not say what he does in the Ministry beyond his title, and does not follow him afterward; the Left Ministry falls in the Rising and nothing is said of its deputy. The pleasure is enough to place him: it is the room's pleasure, and it is what the Secretary has to stand up against, courteously answered by <a href="../characters/sukenori.html">Sukenori</a> and entered beneath the figure as &ldquo;a procedural observation, not pursued.&rdquo; The sheet fills in a plump, pale, lightly powdered man of fifty-two with a neat topknot under a lacquered cap, a thin moustache, a rich purple robe, a folding fan and a ring on every second finger. All of that is the sheet's own.</p>""",
            },
            {
                "slug": "kanemichi", "name": "Kanemichi",
                "epithets": "Ono no Kanemichi &middot; rice-warden of the Right Ministry's eastern granary &middot; 52 years old",
                "teaser": "Has never entered a figure he did not count, and will not sign one he did not do.",
                "bio_html": """<p>A broad, plain man with counting-rod calluses on his left hand, who in thirty years has never put a figure in a ledger that he had not counted. A wet autumn rots the thatch over the third bay of his granary and forty koku go to mold; he records the loss in the month it occurs and asks for new thatch. His accurate page is read by someone who needs it to be a theft. At dawn on the twenty-sixth of Jorren he is shown the Stone in the white of the accused, with his warden's tally-token on a cord at his breast, and a decent young clerk of the Bureau holds out a warmed brush and a confession ruled in every column but the signature.</p>
          <p>He reads it, and finds he cannot sign a figure he has not counted; it is not courage, he thinks, since he has none that he knows of. He gives the brush back and puts out his left hand, the one he counts with. <a href="../characters/jokei.html">Jōkei</a> is watching, and counting. The clerk folds the unsigned sheet in thirds and keeps it, to be found forty years later by a daughter who takes it for a laundry list. His ledger is audited the following month by a successor, who finds it exact in every column, and the page about the thatch is filed beneath it with one word in its margin. He had been right in every figure he ever entered. It was the one thing nobody had wanted.</p>""",
            },
            {
                "slug": "bureau-clerk", "name": "The Bureau Clerk",
                "epithets": "Clerk of the Bureau of Inquiry &middot; unnamed &middot; about 26 years old by his sheet",
                "teaser": "Warms the brush in his sleeve before offering it, and keeps the sheet that was never signed.",
                "bio_html": """<p>A decent young man of the Bureau of Inquiry, who stands at <a href="../characters/kanemichi.html">Kanemichi</a>'s shoulder at dawn on the twenty-sixth of Jorren, at Mikusa, carrying a brush and a confession ruled and inked in everything but the signature. He puts the matter as it has been put to everyone before him: a signed confession is a clean death at the Southern Gate, and the Stone is the Stone. He holds out the brush, and it is a good brush, warmed in his sleeve against the cold. The rice-warden reads the sheet, ruled with real skill, every column square. It is the first time in thirty years of keeping other men's grain that anyone has offered him the chance to sign a figure he has not counted, and he finds that he cannot.</p>
          <p>He takes the brush back. When the rice-warden has crossed the gravel and put out his left hand, the clerk takes up the unsigned sheet and looks for a moment at the ruled columns and the wide clean space where a name would have gone, then folds it into thirds and puts it in his sleeve, as one puts away a letter that has not been answered. It is found among his effects forty years later by a daughter, who takes it for a laundry list. The manuscript does not name him or give his age or looks. The sheet's twenty-six years, thin stooped build, soft chin and anxious brow, and its ink-smudged wrist, are its own.</p>""",
            },
            {
                "slug": "kaneyoshi", "name": "Kaneyoshi",
                "epithets": "Granary clerk of the Left Ministry &middot; the first man the Stone took &middot; about 38 years old by his sheet",
                "teaser": "Dies in a village on the wrong side of the world, saying the name of a thing a clerk counts.",
                "bio_html": """<p>A granary clerk of the Left Ministry, accused of stealing twenty koku of rice from its stores. In the court's ledger he is the man who, shown the Stone at Mikusa, said that he was innocent and put out his hand, and was gone before the priests could draw the breath to cry out; the court, which had one case, counted it as a law. Nine years before the captain's turn he arrives at the tally-stone in the moot-green of Vilarnau: thin, in a nightshirt of some pale stuff and a coat of some other, with a small wooden token on a cord at his breast that nobody can read, shaking so badly that two men have to carry him. For three days he talks in a language no one knows, in a high thin voice that rises and falls like a man arguing with a clerk, and the word he says more than any other is one the reeve can only reproduce badly years afterward. It is a short, round, simple word, a quantity: the measure by which every sack of rice in Himuro is reckoned.</p>
          <p>On the third night he stops. The village buries him beneath the oak with the rites of the Threefold Crown, since it has no others, lays a flat stone on him, and tells the story afterward, with the minor improvements of repetition, as that of the Wild Man who came out of the tally-stone and died; the reeve's whole account of him to the next arrival is four words: the last one died. Higaide, shown the fieldstone the size of a bread-board under the oak, knows the name from a note in the Left Ministry's papers and does the sum: the Stone did not take the false, it took whoever was made to put a hand to it, and the clerk had been counted a proof because he had vanished. The Observer's first note records him as the Pair's one test, a sample &ldquo;too small to be informative&rdquo;, and adds that he has not treated it as one. The sheet's thirty-eight years, ink-callus on the right middle finger and sallow, fever-grey skin are its own; the manuscript says only that he was a clerk, and thin. Case 0202 remembers him as a thin small man with ink on his fingers who lived eleven days in <a href="../characters/smith-of-vilarnau.html">the smith's</a> loft and died on the twelfth, apologizing; the two accounts are not reconciled.</p>""",
                "quote": "Koku.",
            },
            {
                "slug": "kurige", "name": "Kurige",
                "epithets": "Chestnut pony of the Festival of the Small Bow &middot; named only by a stablehand in a hurry &middot; 7 years old by his sheet",
                "teaser": "A pony who bolts at the one small, furious thing he knows by smell.",
                "bio_html": """<p>A chestnut pony whose name means only &ldquo;chestnut-colored,&rdquo; conferred by a stablehand in a hurry. On the twelfth of Eldren, on the meadow below the Shirase River, he carries the Minister of the Left's nine-year-old grandson at a walk and then a canter for the Festival's short course, while a hundred and twenty paces off the boy's teacher watches with his hands in his sleeves. A small russet cat who knows his smell leaps for the saddlecloth, misses, and catches his hock.</p>
          <p>He does not bolt toward the awnings, or toward the river with its water to stop him; he bolts on a diagonal toward the stone footings of the old bridge, which takes him four seconds. The boy goes over his shoulder with an arrow still in his hand. Afterward a patient Examiner finds a scrap of his chestnut hair in the grass at the starting line, with three tufts of russet fur beside it. The sheet's seven years and its white sock are its own; the manuscript gives him only his name, his colour, and the four seconds.</p>""",
            },
            {
                "slug": "kiyomaro", "name": "Kiyomaro",
                "epithets": "Sugino no Kiyomaro &middot; grandson of the Minister of the Left &middot; 9 years old",
                "teaser": "Nine years old and dying, he asks the man who taught him the bow whether his thumb was right at the nock.",
                "bio_html": """<p>Nine years old, grandson of Sugino no Arikuni and the only creature in the realm of Himuro who has ever persuaded that Minister to laugh aloud at his own supper. On the twelfth of Eldren, at the Festival of the Small Bow, he is allowed once in his life a short course on a pony and three blunted arrows at a target of rice-straw, and spends the morning behind the ranked families' pavilion learning from Tomobe no Higaide to settle the nocking-point against his thumb. Higaide discovers, with the helpless astonishment of a man whose own daughter is six and has not yet been persuaded to listen to anyone, that Kiyomaro listens. He rides <a href="../characters/kurige.html">Kurige</a> at a walk and then a canter, upright and grave, a hundred and twenty paces from his teacher; then <a href="../characters/azuki.html">Azuki</a>, arriving a half-breath late, catches the pony's hock, and he goes over the shoulder with an arrow still in his left hand, having been taught by a good teacher how to hold a bow and by nobody how to fall.</p>
          <p>The physician pronounces it a broken neck, which leaves the boy forty minutes in which to be a person rather than a wound. They carry him into the pavilion. He finds Higaide's sleeve with one hand and studies his face with the clear, interested attention of a child who has been told something is important and wants to get it right, and asks whether his thumb was right at the nock. &ldquo;Perfect,&rdquo; says Higaide. He dies a little before the hour of the Sheep. The Law that is built round his death, the Fifth Article and the Stone, is the thing that follows him; his grandfather, who weeps at neither pavilion nor pyre, begins the list of the dead he later copies out as sutras with the boy. The manuscript gives his name, his age, his listening and his question. The sheet's round face, twin side-loops and pale sage robe are its own.</p>""",
                "quote": "Was my thumb right?",
            },
            {
                "slug": "azuki", "name": "Azuki",
                "epithets": "The Minister of the Left's household cat &middot; named for the red bean &middot; a round young cat at the Festival",
                "teaser": "An animal who only wished to be somewhere other than her basket, and whom the histories leave out.",
                "bio_html": """<p>A small, round, russet-spotted cat, named for the red bean, who wandered into the Minister of the Left's compound one winter, has been fed from his grandson's plate ever since, and follows <a href="../characters/kiyomaro.html">Kiyomaro</a>, with the serene entitlement of her kind, to every place he is not strictly permitted to take her. Nobody has seen her smuggled into the Festival of the Small Bow; <a href="../characters/kinji.html">Kinji</a> alone sees her slip from the basket of cushions under the awning's edge and cross the grass at a trot, tail up, intending nothing at all, toward the one pony in the meadow she knows by smell. She believes, as cats believe, that a moving thing is an invitation. She leaps for the saddlecloth, reaches the hock of <a href="../characters/kurige.html">Kurige</a>, and the pony bolts. The histories, when at last they reach the matter, find her inconvenient and leave her out, at a cost of four thousand lives. When the boy dies she walks up the grass to the pavilion, climbs into the vacant lap of the Minister of the Left, turns twice, and settles. Nobody asks the cat.</p>
          <p>She refuses her dinner for three days and sits before the closed door of the boy's chamber. On the night of the pyre the Minister warms her cushion against his own chest beneath his robe before setting it down, and she turns twice and lies in the place where the heat is. At Mikusa she is in the fold of his sleeve, and makes a small questioning sound as the captain turns back to the Stone; he had found her waiting at the gate at the hour of the Ox, and had not had the strength to say no. She grows old with him on Mikusa-yama, lean and light and stiff-jointed, her fur dull as a straw mat, following him from room to room with the unaccusing loyalty of an animal that has no theory of what has happened and no wish for one. In the Bureau's lower archive she climbs into the lap of the man on the floor, and he says, &ldquo;Nobody asked you.&rdquo; She dies in the spring, in his sleeve, which no one has the heart to take off the peg. The sheet's three years at the Festival, notched left ear, amber eyes and nine pounds are its own.</p>""",
            },
            {
                "slug": "kinji", "name": "Kinji",
                "epithets": "Groom at the Festival of the Small Bow &middot; the only man who saw the cat &middot; 40 years old",
                "teaser": "Sees a cat cross the grass and, though he did not wish to say so, tells the Examiner.",
                "bio_html": """<p>A thin, anxious man of forty, the groom at the Festival of the Small Bow, who will remember every instant of the next ten seconds for the rest of a long life. Nobody else has seen <a href="../characters/azuki.html">Azuki</a> smuggled into the meadow; he alone sees her slip from the basket of cushions under the awning's edge and cross the grass at a trot, tail up, toward the one pony she happens to know by smell. He is the fourteenth of fourteen witnesses the Examiner interviews between the thirteenth and the sixteenth of Eldren. Thirteen tell him that the pony bolted. Kinji has not slept; he sits on the floor of the Bureau's inquiry room with his hands pressed between his knees and says that he saw a cat, and had not wished to say so, because the cat was the Minister's own and no sort of explanation for the death of a Minister's grandson.</p>
          <p>Yasutsugu writes it down in his plain brush-hand and goes out to the meadow, where a scrap of chestnut hair and three tufts of russet fur are waiting in the grass at the starting line, and the eleven sheets of his report follow from the groom's sentence. The report is held at the Minister's pleasure, and in the Plum Gate nobody says the word cat. The manuscript calls him only &ldquo;the groom Kinji&rdquo;; whom he served is not stated, and nothing is said of what became of him after the interview. The sheet's hollow-cheeked face, protruding ears and hands that wring each other when he is spoken to are its own.</p>""",
            },
            {
                "slug": "bureau-officers", "name": "The Bureau Officers",
                "epithets": "Officers of the Bureau of Inquiry &middot; one about 40, one about 28 by their sheet",
                "teaser": "Two men in dark robes who serve a summons with the regretful courtesy reserved for the condemned.",
                "bio_html": """<p>Two officers of the Bureau of Inquiry, one older and one younger, in dark robes, who come to a compound in the third ward on the twelfth of Garren, a week after the Seven Sevens have ended, and bow with the careful, regretful courtesy kept for the condemned. They bring a summons under the seals of both Ministers: that the Fifth Article obliges the Captain to answer for the day of the Festival, that his motive has been established to the satisfaction of the Left Ministry, that the Bureau has entered no finding to excuse him, and that he may clear his hand at the Stone of Mikusa at dawn on the twentieth.</p>
          <p>Eight days later they walk behind him at a polite distance through the dark to the shrine, with a boy before them carrying a lantern, and are two of the nine witnesses on the dais. The manuscript gives them neither names nor ages, and the figures on their sheet are its own.</p>""",
            },
            {
                "slug": "rider-from-the-north", "name": "The Rider from the North",
                "epithets": "Messenger of the Kurogane March garrison at Fort Shirakane &middot; unnamed &middot; about 16 years old by his sheet",
                "teaser": "Kills a horse to bring four lines to a man who will not go, and the manuscript says nothing more of him.",
                "bio_html": """<p>A boy in a mud-caked cloak who reaches the Tomobe compound in the third ward on the eighteenth of Garren, two days before the ordeal, having killed a horse to arrive in time. He carries in the lining of his sleeve a letter from Tomobe no Narimune, commander of the Kurogane March garrison at Fort Shirakane and Higaide's elder cousin, the only person alive who has ever seen him cry. The letter is four lines long. It says that a man who walks into an ordeal because the Minister has built one is not proving anything; that the garrison has been told to expect a guest; that three horses will wait at the Northern Gate until the hour of the Rat on the nineteenth; and, in a last line entirely characteristic of its writer, that old <a href="../characters/old-master-one-eye.html">One-Eye</a> would certainly have told him that a man with two swords should be able to find the door.</p>
          <p>Higaide laughs once, with a sound like a cough, and does not go. The Law holds that a hand which fled had spoken, and under the Sixth Article a fugitive's kin forfeit the estate; and, more simply, he does not believe it necessary. He has signed an order of the day, a child has died on it, and if the kami wish to be consulted he sees no reason to make them chase him through the snow. The rider is given no name, no reply to carry, and no later scene, and nothing is said of the three horses. When the Court's second summons reaches the fort, Narimune answers in four lines built from the same sentences and ending that the door is open, which the histories count as the first line of the Rising of the Northern Gate. He is not the boy of sixteen on the north wall who later shoots Narimune; the sixteen years on his own sheet are its own, and so are its wiry build, hollow eyes and black hair tied with a leather thong.</p>""",
            },
            {
                "slug": "old-master-one-eye", "name": "Old Master One-Eye",
                "epithets": "One-eyed veteran of the Kurogane marches &middot; the old master who showed Higaide the two swords &middot; about 65 years old by his sheet",
                "teaser": "Beats a young man senseless in a cedar wood, apologizes profusely, and shows him how it was done.",
                "bio_html": """<p>He is never on the page in the present. In the opening chapter a one-eyed veteran of the Kurogane marches is the reason Tomobe no Higaide wears the long tachi Yoake at his left hip and the short straight Yoiyami at his right, a pairing the court considers an affectation: the veteran had once beaten the young Higaide senseless in a cedar wood and then, apologizing profusely, shown him how it was done. The habits of the lesson outlast it. Higaide runs with his scabbards held against his thighs in the way his old master insisted upon, and before any duty he considers serious he unties and re-ties each sword-cord seven times, which the old master called the only superstition he had ever seen a man acquire in the interest of better knots.</p>
          <p>His one other appearance is a joke in a letter. Narimune, in the four lines a rider brings two days before the ordeal, says that old One-Eye would certainly have told his cousin that a man with two swords should be able to find the door, and Higaide laughs, once, and stays. The manuscript uses &ldquo;a one-eyed veteran&rdquo;, &ldquo;his old master&rdquo; and &ldquo;old One-Eye&rdquo; without saying outright that they are one man, and never says whether he is alive, which eye he lacks, or what he was called. The sheet takes them for one man and adds the rest: an eye-patch over the left eye, white cropped hair, a lined and scarred face, a field coat and sheepskin vest, a long blade and a short, and about sixty-five years. Its caption, a man with two swords finding the door, compresses Narimune's line. Of the <a href="../characters/rider-from-the-north.html">rider</a> who brings it, the text says nothing further either.</p>""",
            },
            {
                "slug": "new-left-minister", "name": "The New Left Minister",
                "epithets": "Successor Minister of the Left after Arikuni's resignation &middot; unnamed &middot; about 45 years old by his sheet",
                "teaser": "Grants the one amendment that costs nothing and implies nothing, and leaves the Law standing.",
                "bio_html": """<p>A nervous, dutiful, ambitious man, who takes the Left Ministry when Sugino no Arikuni resigns in the first winter of the Rising and retires to a hermitage on the slopes of Mikusa-yama. Years later Arikuni sends for him and tells him, in a voice like dry paper, what he has read in the Bureau's lower archive: eleven sheets, a pony, a cat, and a Law that sent a captain to the Stone on a hand that did not exist. The Minister listens, and says with great respect that the Law cannot be put aside. If it were repealed, it would have to be said why; if it were said why, it would be said that every hand the Stone had taken was a hand it should have refused, eleven houses and a captain and a Right Minister of the realm, and that the Court had killed them. It cannot be said.</p>
          <p>Arikuni asks, then, for the one thing that can be granted without being explained: that no accused be shown the Stone until the Examiner's report has been read aloud to the Ministers who attest and entered in the record. The Minister grants it with visible relief, since it costs nothing and implies nothing, and it goes into force that afternoon for a Law that nobody will put to use. A Law that has been wrong, Arikuni concludes, cannot be corrected aloud, because its correction is a confession; it can be amended only in the margin, where nobody reads. The Law outlives its author by six years, unused, and lapses in the twelfth year under a successor court that wishes to be seen correcting something. The manuscript gives this minister no name, age or appearance beyond nervous, dutiful and ambitious. The sheet's forty-five years, deep-purple robe, folding fan, oiled topknot, and finger tapped against the sleeve when he calculates, are its own.</p>""",
            },
            {
                "slug": "boy-sovereign-of-himuro", "name": "The Boy-Sovereign of Himuro",
                "epithets": "Sovereign of Himuro &middot; 14 years old at the opening &middot; abdicates into a monastery",
                "teaser": "Sits a throne at fourteen between two Ministers, and leaves it for a monastery.",
                "bio_html": """<p>A sovereign of fourteen sits the throne of Himuro, as sovereigns of fourteen generally do, which is to say that the realm is governed by the two Ministers who stand on either side of him, the Left and the Right, in an arrangement of mutual surveillance so old that neither can remember which began it. He has no name and no lines in the manuscript. He is the fixed point between Sugino no Arikuni and <a href="../characters/sukenori.html">Sukenori</a>, whose thirty years of watching each other the whole of the Law of the Clean Hand grows out of; the court, the Festival and the Stone all go on in his reign, and none of them needs him to speak.</p>
          <p>By the third winter of the Rising he has abdicated into a monastery; the Log lists the abdication among the results, beside the fall of both Ministries. The histories of Himuro, which are agreed on the causes of the Rising, give it as the ambition of provincial warriors and the arrogance of a Left Ministry in its declining years, and, in the more philosophical commentaries, as the natural consequence of a boy-sovereign and two old men. The manuscript says nothing of his age at the abdication or of his life afterward. The sheet gives him a slight, narrow-shouldered build, a very pale indoor complexion, a black youth's topknot under a tall court cap, deep saffron robes over white, an ivory tablet in his hands, and, after the abdication, a shaven head and a plain grey monk's robe in a snowy cloister. All of that is the sheet's own.</p>""",
            },
            {
                "slug": "bertran", "name": "Bertran",
                "epithets": "Sir Bertran de Lanta &middot; master-at-arms of Castelmaur &middot; knight &middot; 38 years old",
                "teaser": "Cannot enter a mercy in any column, so he rides out alone one night to repay it.",
                "bio_html": """<p>A stern, lean, well-made man of thirty-eight who has fought in six minor wars and won five, and who goes through life by double entry: debts incurred and debts paid, blows given and blows returned. On the green at Vilarnau he is disarmed in a single movement by a foreigner who then sheathes both swords and bows with the painful apology of a man who has spilled wine, having left him alive by choice. Bertran has no column in which to enter a mercy. He does not hate the man; it is a respect so complete that it has nowhere to go. In the evenings he carves small pearwood horses and sends them, in rags, to his widowed sister's four children, who have never been told who makes them.</p>
          <p>On the sixteenth of Jorren, when the baron orders the stone broken and the guest taken, he rides down to the mill alone and without a banner, knocks at the door, and tells <a href="../characters/gersenda.html">Gersenda</a> once what is coming. At the end of the yard, without turning, he adds the one line that was not a warning. On the night of the torches he is given forty men and spends forty minutes in a thicket on a perfectly sound hoof. He asks leave to resign his sword, is refused, and rides out of the gate without it. In the fourteenth year he comes to Lasserra on foot, sets a small grey gelding on the bench of the last house, and is not seen again. The same man has a page under <a href="../characters/bertran-0202.html">Case 0202</a>, whose sheet makes him forty-one; this one makes him thirty-eight. The two pages are not reconciled.</p>""",
                "quote": "Tell him that we are even.",
            },
            {
                "slug": "bertrans-sister", "name": "Bertran's Sister",
                "epithets": "Widowed sister of Sir Bertran de Lanta &middot; mother of four &middot; valley of the Nauze &middot; about 34 years old by her sheet",
                "teaser": "Her children receive a small carved horse for nine years, and are never told whose hands made it.",
                "bio_html": """<p>She never appears on the page. The manuscript gives <a href="../characters/bertran.html">Bertran</a> a widowed sister in the valley of the Nauze, with four children, and one other thing besides: it is her embroidered woolen blanket, patterned with horses, that he lies under in the narrow chamber above the armory at Castelmaur, working the same small piece of arithmetic in the dark. For nine years he has carved wonderfully accurate pearwood horses in the evenings, ears laid back and tails half-lifted, and sent them to the children wrapped in rags; and not one of them has ever been told who makes them. It is the private life that the household of Castelmaur would have said he did not have.</p>
          <p>The last horse the manuscript follows is the one he finishes in the last week of Iverin, a grey gelding with one raised hoof, which he turns in his palm while thinking of how the stranger sheathed both swords, left and right, like a man closing a book. When he rides out of the barony after the burning he carries a small wooden horse in his saddlebag; and in the fourteenth year he sets a grey gelding with one raised hoof on the bench of the last house at Lasserra and walks away. The text does not say whether that is the same horse, or whether his sister ever learns who the carver was. The sheet's thirty-four years, the children's ages (four to twelve), her needle-pricked fingertips and the row of horses on the sill are its own, as is its caption that she is never told who sends them.</p>""",
            },
            {
                "slug": "ermengarda", "name": "Ermengarda",
                "epithets": "Widow of the miller of Vilarnau &middot; keeper of the Mill of the Two Weirs &middot; mother of Gersenda and Peire &middot; about 38 years old by her sheet",
                "teaser": "Feeds a stranger because he looks cold, and learns that welcome is the most expensive thing she owns.",
                "bio_html": """<p>A small, tough, brown woman with a gap in her front teeth and a laugh that carries across the Lauze, who has run the Mill of the Two Weirs herself since the miller died of a cough four winters back, with a hired boy, a stubborn red ox called Lo Rog, a daughter of sixteen, <a href="../characters/gersenda.html">Gersenda</a>, and a son of eight. She puts a bowl into the stranger's hands at dusk for no better reason than that he looks cold, having been raised to think a cold man an obligation, and by the custom of the Charter the guest is thereby hers, since she fed him first. She feeds him again in the loft above the grinding-floor, and he bows to her with the same grave motion he gave the stone: she has been bowed to by a priest and never by someone who meant it. At Solan's fire she pushes him bodily into the front rank, and when Father Guiraut comes to say that the Moon-Man cannot bow to the god here, she tells him that he bows to everything, he bowed to the ox.</p>
          <p>She knows from the first morning that something has entered her house which cannot be fed, and that it will cost her. When <a href="../characters/bertran.html">Bertran</a> comes by night to warn them she will not go to the hills: a woman who leaves her seed to be counted by strangers might as well not have sown. On the first of Kerren the forty measures are in her loft when the sergeant climbs the ladder, and her son is thrown across it; looking up at the stranger over the boy's body, she has the face of a woman who has been told a total and is doing the sum. &ldquo;They will come now.&rdquo; She is one of the forty-nine in the quarry cleft, dies in the ninth year of a fall from the ladder of the apple-loft, and is buried under a chestnut with the whole High Ground in attendance. Her great-granddaughter has her laugh. The manuscript gives her no age; the sheet's thirty-eight and its flour-creased knuckles are its own.</p>""",
                "quote": "He bows to everything. He bowed to the ox.",
            },
            {
                "slug": "gersenda", "name": "Gersenda",
                "epithets": "Miller's daughter &middot; later wife of the smith's surviving son and leader of the High Ground &middot; 16 at the story's opening, 35 at the departure",
                "teaser": "Teaches a stranger the word for door, and keeps his unreadable poem in the bread-box.",
                "bio_html": """<p>The miller's daughter at the Mill of the Two Weirs, sixteen, with her mother's gap in her front teeth and her late father's long patient face, and the frank clinical interest of a girl who has been told to find something wrong with a person and cannot. She is appointed, by the unspoken vote of the household, to teach the foreigner the language, in the slow flat voice one uses to an elderly, intelligent animal, working through the whole kitchen from the pot to the ladle to the small cracked salt-bowl. She drives a hard bargain at the wool-market, and in return he teaches her his word for stone.</p>
          <p>She is the first to hear him in the barn, and she keeps everyone away from it that afternoon. She answers the door to <a href="../characters/bertran.html">Bertran</a> at night with a candle and an iron ladle held down against her thigh, and on the night of the torches takes the halter, and the others, across the plank into the dark. On the ridge she marries the smith's surviving son and bears five children; she runs the High Ground's affairs with a hard bargain and a long patient face. She keeps a few of the old man's verses, hidden, in a bread-box, and on the day he goes east she hears him say the name at the boundary-stone, as though telling someone where he was going. The morning after, it is she who finds the sheet he has left for her.</p>""",
            },
            {
                "slug": "smiths-son", "name": "The Smith's Son",
                "epithets": "Son of the smith of Vilarnau &middot; later husband of Gersenda &middot; 19 years old at the weighing",
                "teaser": "Reads one book, finds the plank that settles the village's fate, and carries a dead man's hammer up a ridge.",
                "bio_html": """<p>Nineteen, the son of the village smith, who has read one book in his life and likes to be at the front of any idea. To him the stranger is Saint Two-Swords, though the saint is still in the stage of having no feast-day and no church. In <a href="../characters/brunissen.html">Brunissen</a>'s tavern on a sleety evening in Jorren, when a man at the back says that the door leads to the baron's cellar, he goes red and says that the cellar is the one place in the country he wishes it did lead to. When the weigher's widow asks how a sack of dusty barley is to be set on a door to heaven, he is the one who proposes that the village weigh at the old oak instead, on a plank, with the beam hung from a branch, and tell the bailiff that the green's stone is being kept clear in honor of the visitor. A fat man points out that the Charter says the stone. The smith's son answers that the Charter was written by men who had never seen a door open.</p>
          <p>The hands go up one by one, with two left in laps, and it is settled. Nobody in the room names what is being given up; the Observer's notes spell it out afterward. His father the smith does not live to reach the ridge, and the son carries the dead man's hammer up the quarry road on his back and finds, in thirty years, no use for it. On the ridge he marries <a href="../characters/gersenda.html">Gersenda</a>, who bears him five children. The manuscript never names him. The sheet's curling black hair, soot-darkened skin and patchy beard are its own, and so is the compression of the manuscript's remark into its caption, &ldquo;at the front of any idea.&rdquo;</p>""",
            },
            {
                "slug": "bernat", "name": "Bernat",
                "epithets": "Old Bernat &middot; reeve of Vilarnau &middot; 79 years old",
                "teaser": "Has seen a great deal and been impressed by very little, and does not leave.",
                "bio_html": """<p>The reeve of Vilarnau, an ancient with a cold clay pipe, who sits on the bench outside the forge with the posture of a man who has seen a great deal and been impressed by very little of it. Told a man has come out of the stone, he does not look up. He settles the first morning's trouble by the Charter: any stranger who comes to the green at dusk and is not turned out by sunrise is the village's guest, and the guest, he rules, is the miller's widow's, since she fed him first. He walks the foreigner out under the oak to a flat grey fieldstone the size of a bread-board and tells him that the last man had lain there nine years.</p>
          <p>At the tavern, on the evening it is decided to weigh at the oak, he is seen reckoning on his fingers, and says only that the baron would have to be told civilly. On the green, facing the baron, he says the stone is not to be used that day. When the baron's banner has vanished behind the hill it is he who says, in a voice that does not sound like winning, that they have won. On the night of the torches he goes from door to door with a lantern. He is seventy-nine, and he does not leave. His pipe is found afterward in the ashes of the bench outside the forge.</p>""",
                "quote": "The last one died.",
            },
            {
                "slug": "brunissen", "name": "Brunissen",
                "epithets": "Keeper of the tavern of Vilarnau &middot; 40 years old",
                "teaser": "Never lets a silence last a minute, and is the one person in the lane who says what the stone will cost.",
                "bio_html": """<p>A broad, bright-faced, loud-voiced woman of forty, who sells a thin bitter ale and a thinner red wine under a crooked chestnut-branch sign painted yellow in her father's time, and who has never in twenty years allowed a silence to last more than a minute. It is she who asks, wiping a mug on her apron, where the stone goes if it is a door. On the sleet-ticking evening when the lane votes to take its grain to a plank under the oak and keep the green's stone clear for its guest, hers is one of the two hands that stay in a lap, because she does not vote on anything she will have to serve drinks through afterward.</p>
          <p>Through a crack in her shutter she watches the foreigner lay his hand on the polished stone in the sleet, and says, to no one, in a very quiet voice, that it is going to be a long winter. She is correct on every point but the length. After the burning she carries her father's sign up the quarry road, scorched along one edge, and hangs it in the second spring on the door of the largest house on the path. She keeps a tavern there for thirty years and never again allows a silence to last a minute. Nobody asks her why.</p>""",
            },
            {
                "slug": "weighers-widow", "name": "The Weigher's Widow",
                "epithets": "Widow who keeps the village's tally-sticks &middot; Vilarnau &middot; 55 years old by her sheet",
                "teaser": "Asks, in a warm tavern, how a woman is to set a sack of dusty barley on a door to heaven.",
                "bio_html": """<p>A pinched small woman of Vilarnau who keeps the village's tally-sticks, and the one voice in <a href="../characters/brunissen.html">Brunissen</a>'s tavern that asks the practical question. In a lull, after the room has laughed at a door that leads to the baron's cellar, she says in a thin voice from the corner of the hearth that what the village should worry about is not where the stone leads but what it is standing in the way of. The bailiff will come on the twentieth with the new weights and the new rate; every sack in the parish must be laid on the stone before witnesses, as the Charter requires; and she does not know, for her part, how a woman is to set a sack of dusty barley on a door to heaven. The room, which had been warm, grows a little cold. It is the whole of the argument, and it is the argument that the plank under the oak is put forward to answer.</p>
          <p>That evening she buys a splinter of chestnut from <a href="../characters/gaucelm.html">Gaucelm</a>, who sells them as relics of the True Doorstone. On the first of Kerren a pig is taken from her in the forenoon distraint of the east lane, and screams all the way to the cart. The manuscript does not name her or her late husband, the weigher, and does not say whether she is among the dead, the ridge or the dispersed. The sheet's fifty-five years, bright black eyes, grey hair under a tight linen cap and the bundle of notched sticks at her belt are its own.</p>""",
            },
            {
                "slug": "gaucelm", "name": "Gaucelm",
                "epithets": "Tinker, seller of needles and relics along the Lauze &middot; thirty years on the road &middot; about 55 years old by his sheet",
                "teaser": "Sells splinters of the True Doorstone, and tells a tavern the one thing it should have been worrying about.",
                "bio_html": """<p>A talkative tinker who has sold needles and relics along the Lauze for thirty years, and who has sold, that autumn, in four villages, eleven splinters of the True Doorstone at a denarius each. He is by the fire at <a href="../characters/brunissen.html">Brunissen</a>'s on the evening Vilarnau decides to weigh its grain at the oak. Sleepy over a second cup, he remarks that the nobles of Rocafort are saying the baron's brother will die in his dungeon, that the baron is going to squeeze every village in the barony to buy him out, and that if he were a Vilarnau man he would be worrying less about doors than about hay. It is the one plain sum said aloud in the room, and the room does not hear it as one. He holds, as a professional matter, that the poor are always more exercised about the meaning of a thing than about its price, which is why they stay poor.</p>
          <p>He sells a splinter of chestnut to the weigher's widow, goes to sleep by the fire without a trace of conscience, and plans to be three valleys away before anyone examines it. He has never seen a door open in his life; he has seen a great many men squeezed. The manuscript does not say what became of him. The sheet's wiry build, weathered skin, shoulder-length grey-brown hair, missing left ear-lobe and box of chestnut splinters are its own, and so is the age of fifty-five.</p>""",
            },
            {
                "slug": "villagers-of-vilarnau", "name": "The Villagers of Vilarnau",
                "epithets": "The village chorus: the cooper, the smith and his wife, a young wife three months gone, a feverish boy, a very old woman, the mill's hired boy &middot; aged 12&ndash;85 by their sheet",
                "teaser": "Touch the stone on the way to somewhere else, and turn a weighing-place into a door.",
                "bio_html": """<p>Forty-one hearths and a hundred and ninety souls, drawn here as the people they are: a wiry cooper who has been drinking and calls the foreigner the Eastern Angel, a broad smith who comes to the green with his hammer, the smith's wife who sends round a dish of boiled sausage and weeps when it is returned untouched, a young wife three months gone who walked three miles that spring to touch a shrine of Elara and now lays her palm where the stranger lays his, a cooper's boy whose fever is said by his mother to have broken at once, a very old woman with four teeth who smiles openly, and the mill's hired boy, who adores the man who mends the sluice. In a fortnight half of them are touching the green's stone on their way to somewhere else, and the top of it begins to take a polish.</p>
          <p>They mean no harm. It is a pious gesture, out of kindness to a stranger and fear of a god, and out of a pleasing sense of being for once in the middle of something; and it is made a plank at a time, by warm people, in a tavern. The smith does not live to reach the ridge; his surviving son, who once read a book, carries the dead man's hammer up on his back and finds no use for it in thirty years. Of the village's hundred and ninety, seventy-four are dead by the second of Kerren, and eight more by the thaw. Case 0202 gives <a href="../characters/smith-of-vilarnau.html">the smith</a> and <a href="../characters/smiths-wife.html">the smith's wife</a> pages of their own.</p>""",
            },
            {
                "slug": "masons-of-castelmaur", "name": "The Masons",
                "epithets": "Masons of the baron's household &middot; the elder about 50, the younger about 30 by their sheet",
                "teaser": "Two patient, indifferent men with a sledge, three iron wedges, and a stone that will not take a mark.",
                "bio_html": """<p>Two broad, patient, indifferent men in leather aprons who ride down to Vilarnau with the baron on the twentieth of Jorren, carrying iron wedges and a great sledge-hammer slung on a pole. They have been told to break an obstruction. The first wedge goes against the stone's flank at the join where the green vein runs, and the elder swings; the sound rings clean and bright across the whole valley and is followed by a noise like a twig snapping. The iron wedge, from the best smith in Castelmaur, lies in the dust in two halves. The second goes the same way.</p>
          <p>The third, a thicker one, strikes a scatter of sparks and rebounds so hard that one of them drops the hammer and stands nursing his wrist. Where it struck there is no mark; the grey surface lies in the sunlight, cool and smooth, as though it had been struck by a feather. The elder, who has broken stones his whole life, tells the baron that it is not a stone a man can break, and that if his lordship wishes it moved he will need forty oxen and a good deal more than a morning.</p>""",
            },
            {
                "slug": "castelmaur-men-at-arms", "name": "The Men-at-Arms of Castelmaur",
                "epithets": "Men-at-arms and sergeants of the Barony of Castelmaur &middot; mostly 19&ndash;40 by their sheet",
                "teaser": "Ordinary soldiers following an order to burn, and none of them able to lay a hand on the stone afterward.",
                "bio_html": """<p>The baron's household troops: six who ride behind the bailiff to the first weighing, twenty who come with the baron on the twentieth of Jorren, a sergeant named Sicard with ten men and a cart who go down the east lane on the first of Kerren, and the forty who carry torches on the night of the burning. They are told what the barony is owed, and they do the work. Nine hearths are distrained in the forenoon, a pig screaming all the way to the cart. At the mill a boy of eight goes for one man's hand with his teeth and lays the knuckle open to the bone, and three of them are dead in the loft inside a dozen heartbeats.</p>
          <p>On the night they are sent after the man responsible, the first six down a narrow lane find a thing in the road they have no instruction for and go down in a pile, and the forty behind them stop. Nobody wishes to be next. The thatch is put to the torch behind the line, and at dawn they are still in a ring about the moot-green, a hundred paces from the ashes of the nearest house, looking at a grey block with a charred wreath of ivy on it, exactly as it always stood. In forty men, not one of them can find it in himself to lay a hand on it. Their knight, <a href="../characters/bertran.html">Bertran</a>, reports in the morning that the village is burned, the man escaped, and the stone cannot be broken.</p>""",
            },
            {
                "slug": "sicard", "name": "Sicard",
                "epithets": "Sergeant of Castelmaur, second to the bailiff &middot; thorough, with no particular opinions &middot; about 40 years old by his sheet",
                "teaser": "Finds the work of taking a village's grain easier than he expected, and carries the report that burns it.",
                "bio_html": """<p>The bailiff's second, a short, wide, hard-faced sergeant with a reputation in the barony for thoroughness and no particular opinions. He rides down the lane of Vilarnau on the first of Kerren, a day late because his master, who dislikes the business, has found small administrative reasons to wait, with ten men, a cart and the clerk <a href="../characters/folquet.html">Folquet</a>. Nine hearths of the east lane are distrained in the forenoon without violence. He finds the work easier than he had expected, grows by degrees expansive, and calls the clerk's attention to the proper form of the entry. At the Mill of the Two Weirs he goes up the ladder with a lantern to the widow's forty measures of seed-grain; when <a href="../characters/ermengarda.html">Ermengarda</a> says he will not take them, he answers that it is the lord's due and will be weighed at the castle, and turns his back on her to give an order.</p>
          <p>Three of his men are dead in the loft within a dozen heartbeats. The text places him both at the head of them on the ladder and outside holding the horses, arriving at the door too late for anything but the end, and does not reconcile the two. He comes back out white to the lips and tells the clerk that the foreigner has killed the three. By dusk he is at Castelmaur on a lathered horse, in sweat and fear, delivering a report that has passed through three mouths and a ledger: a lie in every particular but the facts, and exactly what the baron most wants to hear. Nothing is said of him afterward. The sheet's forty years, ruddy skin and brush-cut black hair are its own.</p>""",
            },
            {
                "slug": "arnaut", "name": "Arnaut",
                "epithets": "Bailiff of Castelmaur &middot; twenty years in the baron's service &middot; 45 years old",
                "teaser": "Has never found a way to bend one clause of the Charter, until the village hands him the means.",
                "bio_html": """<p>A stout, tired, reasonable-looking man of forty-five with the face of a deacon and the hands of someone who has spent twenty years being told by a lord what to find, and who does not particularly like the work: he likes, as he has told his wife, the evenings after it. He comes up the lane of Vilarnau at Prime with six men-at-arms, a clerk, and a pair of iron-bound weights recast the previous month on the baron's order, which the village's three most obstinate arithmeticians put at a fifth heavier than the ones they replace. When the reeve claims the stranger as a guest of the Charter, Arnaut, who has never in twenty years found a clause of it he could not bend, opens his mouth to dispute the point, glances at <a href="../characters/bertran.html">Bertran</a>'s face, and shuts it. The new weights are found to be what the arithmeticians estimated, and no one says so.</p>
          <p>Sent for by <a href="../characters/aimeric-2231.html">Aimeric</a>, he observes, in the careful voice of a man who has spent twenty years not observing things, that the weighing clause is the one he has never found a way to bend, since no hearth may be distrained until the stone has found the default by weight; on the sixteenth of Jorren he reads the baron's order aloud from a roll, that the stone be used or broken. On the twentieth, with the village's refusal in front of him, he finds the one way through the clause: a village that declines to put its grain on the stone has declined the weighing, and the Charter's protection lapses with it. The chronicle calls it perfectly sound law. On the third of Kerren he gives the baron the ash account, standing. What became of him is not said. The sheet's ink-stained fingertips and sandy, thinning hair are its own.</p>""",
            },
            {
                "slug": "folquet", "name": "Folquet",
                "epithets": "Clerk to the bailiff of Castelmaur &middot; later clerk of record to the Count of Rocafort's assizes &middot; 26 at the distraint, 60 at his death",
                "teaser": "Believes arithmetic is a form of mercy, and writes the one line he would most like to have left blank.",
                "bio_html": """<p>A pale, tidy, ink-fingered young bailiff's clerk of twenty-six, taught from boyhood that a column which does not add is a sin and that arithmetic is a mercy, since it tells people what they owe so that they need not guess. He walks down the lane of Vilarnau behind the cart on the first of Kerren with his book open on his forearm, entering the condition of each hearth in a neat, unemotional shorthand, and does not look at the faces of the people at their doors, since he holds it unprofessional. Of eleven hearths in the east lane, nine are distrained, one is unfortunate, and one is the sort that ought to be put in a ledger. On the tenth line he writes, in clean copperplate, that the widow's hearth violently resisted and that three of the sergeant's men are dead by a foreigner.</p>
          <p>On the third of Kerren he totals the account at sixty-one solidi, and writes in the margin the only comment he permits himself: that the lane would not pay again. He lives to sixty, and becomes clerk of record at the Count of Rocafort's assizes, admired for the exactness of his entries and the economy of his opinions. In the thirty-first year after the burning he is asked to read from the oldest book in his keeping, and reads the tenth line aloud to a room of lawyers. The count's judge supposes it the work of a Saracen mercenary in the late baron's pay, and Folquet, who has never entered an opinion in forty years, says nothing. It is entered. It is the version the district keeps.</p>""",
            },
            {
                "slug": "aimeric-2231", "name": "Aimeric of Castelmaur",
                "epithets": "Baron of Castelmaur &middot; lord of Vilarnau &middot; brother of Guilhem &middot; 50 years old",
                "teaser": "Raises the tolta to a sixth to ransom a brother, and burns the village that was paying him thirty-eight solidi a year.",
                "bio_html": """<p>A heavy, red-bearded, big-handed man of fifty who inherited a barony and a temper and was never taught to tell them apart, and who has a wife of twenty-three, Lady Adalaïs, whom he does not understand and is a little afraid of, and a great grey hound called <a href="../characters/ors.html">Ors</a>. He is not a cruel man. He thinks of his villages as a field that grows money if it is correctly weeded; he cannot swim, and has built, in consequence, a very large castle on a very high rock. His younger brother <a href="../characters/guilhem.html">Guilhem</a>, sent to seize a weir on the Sarrac, is held for four hundred solidi, and the baron does the sum until it is a rosary: of nine hundred a year, six hundred arrive as sheaves and labor-days and cannot be paid to anyone. He raises the tolta from a tenth to a sixth and adds a hearth-penny of two denarii a chimney, and when his chaplain says that the villages may find it heavy, he says they are not being asked to like it, that it is a single winter, and that he will remit the whole when his brother is home. He means it.</p>
          <p>A stone that is a place where grain is weighed does not interest him until it breaks his masons' wedges, and on the green his own dog is undecided for one second. He orders the village burned on a report he is glad to hear. It yields sixty-one solidi, against a village that paid thirty-eight a year for ever; he sees the error in the second week of Kerren, and Guilhem dies on the fourteenth of Lorren, forty-two days before the sum was due. Lady Adalaïs goes home in the second spring; villages empty in the night; he dies in the third winter of a fever in the long cold chamber, with Ors across his bed, turning the pages of his ledger and saying to nobody, in a puzzled voice, that he cannot find the column. The sheet's pale blue eyes and thinning red-brown hair are its own.</p>""",
            },
            {
                "slug": "ors", "name": "Ors",
                "epithets": "Baron Aimeric's great grey hound &middot; eleven years at the baron's bedside",
                "teaser": "Is undecided for one second, and the baron thinks about it for the rest of his life.",
                "bio_html": """<p>A great grey hound who has slept at the foot of Baron Aimeric's bed for eleven years, and who has never in that time left his master's side without permission. He trots at the baron's stirrup down the lane of Vilarnau on the twentieth of Jorren, with twenty men-at-arms, two masons and the bailiff. When the baron walks across the green to tell the stranger to stand aside, the hound pads forward, stops, and thrusts his long nose into the stranger's open palm, and is, after a moment's hesitation, scratched behind the ear.</p>
          <p>&ldquo;Ors,&rdquo; says <a href="../characters/aimeric-2231.html">Aimeric</a>. The hound looks at him; it takes a perceptible moment; then he returns, unhurried, to the baron's knee, and sits. It is the sort of thing a man cannot do anything about, and the baron will think of it at odd moments for the rest of his life. The hound is across his knees when the letter comes saying that <a href="../characters/guilhem.html">Guilhem</a> is dead. By the third winter his muzzle is white; he lies across the bed in the last week with his chin on his master's foot, and does not once ask for an account of anything. The manuscript says nothing of what became of him after the baron died. His age at the weighing, thirty inches at the shoulder and the wiry grey coat are the sheet's; the text says only that he is a great grey hound and has been with Aimeric for eleven years.</p>""",
            },
            {
                "slug": "odilo", "name": "Odilo",
                "epithets": "Hierarch of the temple of Auron at Castelmaur &middot; about 60 years old by his sheet",
                "teaser": "Lays an interdict on a lane in the tone of a man initialing a receipt.",
                "bio_html": """<p>The Hierarch Odilo sits in judgment of the barony's morals from a squat round temple of red brick at the gate of Castelmaur, and dines on lamb on feast-days. Father Guiraut's honest report on the stranger's bowing, the refused pig, and a stone being touched by half the parish under a foreign name reaches him, and it is, to a certain kind of reader, indistinguishable from an accusation. When the report of the sergeant's dead men comes, he arrives in his scarlet, with a small smile, to bless the enterprise. He is not a cruel man; he is simply a man whose faith holds that every other crown in the world is stolen, and who has never been made to reckon what that means in thatch.</p>
          <p>He lays the interdict of the temple on Vilarnau, so that no hearth in the barony may feed, shelter or bury any soul of that lane until the idol is cast down, and pronounces it in the tone of a man initialing a receipt. It costs the Church a line of parchment and costs the ridge its winter. When the barony's tithes begin to fall off in the years after, he preaches against sloth. The temple's chronicle remembers a raid of Saracens and a heathen idol cast down by his zeal, with the blessing of the Three.</p>""",
            },
            {
                "slug": "guilhem", "name": "Guilhem",
                "epithets": "Younger brother of Baron Aimeric &middot; hostage of the Count of Rocafort &middot; 38 years old",
                "teaser": "Writes funny letters from a damp cell, and begs his brother not to do anything foolish on his account.",
                "bio_html": """<p>A lean, charming, careless, good-natured man of thirty-eight with a talent for being liked, whom his brother the baron sends in the late summer with forty men to take a small weir on the Sarrac, which both baron and count have claimed for forty years. The count's riders are already waiting at the ford. They take the weir, forty men, two banners and the baron's brother in a morning, and send back a courteous letter naming a price of four hundred solidi, to be counted at Rocafort before the count's chaplain.</p>
          <p>His four letters are, like everything he has written, funny. The count's cook has resolved to starve him by degrees, though the sauces are the real tragedy; the Basque guard has taught him a song of forty verses about a goat. The last says in the same light tone that the cell is damp, that he is coughing a little, and that he would be glad to be home by the winter feast. He dies on a pallet of straw on the fourteenth of Lorren, with the guard sitting by him singing the sixth verse. The count, being a man of honor, returns the body without ransom, and keeps the weir. It is forty-two days before the sum would have fallen due. The baron folds the letter in three, and puts it in the box with the other four.</p>""",
            },
            {
                "slug": "count-raimon", "name": "Count Raimon of Rocafort",
                "epithets": "Count of Rocafort &middot; neighbor and rival of Castelmaur &middot; old and lean; about 64 years old by his sheet",
                "teaser": "Collects prisoners as other men collect falcons, and keeps the weir when the baron's brother dies.",
                "bio_html": """<p>An old, lean count who rules Rocafort, a smaller, poorer, more patient neighbor of Castelmaur, from beyond the faint blue line of hills, and who collects prisoners as other men collect falcons. For forty years he and the baron have each claimed a small weir on the Sarrac; in the late summer his riders are already waiting at the ford when <a href="../characters/guilhem.html">Guilhem</a> arrives with forty men, and take the weir, the men, two banners and the baron's brother in a morning. The ransom he names, in a courteous letter, is four hundred solidi, in coin, to be counted at Rocafort in the presence of his chaplain. He allows Guilhem one letter a fortnight, under seal, to be read first by the chaplain.</p>
          <p>When Guilhem dies of the cough he said he had, on the fourteenth of Lorren, the count, being a man of honor, returns the body without ransom, and keeps the weir. Castelmaur loses two more villages to his writ in the autumn; in the fourth year he acquires the ridge district of Lasserra, finding that it pays more in peace than it would in coin. <a href="../characters/folquet.html">Folquet</a> becomes clerk of record to his assizes, and a sleek, well-read judge of his court reads a Saracen into the tenth line of an old ledger. The sheet notes that the source gives only &ldquo;old&rdquo;, &ldquo;lean&rdquo; and the falcon comparison, and that the rest is invented; its sixty-four years, white hair and pale grey eyes are not the manuscript's.</p>""",
            },
            {
                "slug": "basque-guard-of-rocafort", "name": "The Basque Guard of Rocafort",
                "epithets": "Guard of the Count of Rocafort, called &ldquo;a Basque&rdquo; &middot; unnamed &middot; about 40 years old by his sheet",
                "teaser": "Teaches a prisoner a forty-verse song about a goat, and sings its sixth verse beside him as he dies.",
                "bio_html": """<p>He is known to the manuscript by two sentences. In the letters he is allowed to send from the cell beneath Rocafort's hall, <a href="../characters/guilhem.html">Guilhem</a> reports, in his light tone, that the guard, a Basque, has taught him a song of forty verses about a goat. On the fourteenth of Lorren Guilhem dies of his cough on a pallet of straw in a dry stone room, and the Basque guard is sitting by him, singing in a low voice the sixth verse of the song.</p>
          <p>That is all the text says of him. He has no name, no speech and no later scene, and the manuscript does not say what became of him. It is enough to put a small human figure inside the count's arithmetic: a guard who sits by a dying prisoner and is still singing, on the sixth verse of forty. The sheet's forty years, olive wind-roughened skin, one missing upper tooth, black hair silvering at the temples, ring of keys and spear are its own, and so is the caption that he sings the goat song beside Guilhem as he dies.</p>""",
            },
            {
                "slug": "jaume", "name": "Jaume",
                "epithets": "Boy of the High Ground &middot; 9 in the second winter",
                "teaser": "Finds by accident the exact place on a stick where the thumb belongs, and is never told what he was given.",
                "bio_html": """<p>One of the boys of Lasserra who, in the long evenings of the second winter on the ridge, find in the lean old man with the long jaw a master for the sticks. He teaches them with grave patience to hold a wooden sword as one holds a thing that might one day hold one back: the grip, the breath, the settling of the thumb. He teaches them to bow to a stick before they strike it. None of them becomes a swordsman, which he regards as the most successful outcome possible.</p>
          <p>Jaume, nine, finds by pure accident the exact place on the stick where the thumb belongs, and looks up in alarm at the sudden silence. The old man says <em>Perfect</em> in the speech of the High Ground, and then, under his breath, in his own, and goes out to stand a while among the goats. Nobody asks him why. The boy keeps the grip for the rest of his life and is never told what he has been given. The manuscript gives only his age and the moment; the sheet says outright that his appearance is invented.</p>""",
            },
        ],
        "scenes": [
            {"slug": "the-cat-at-the-starting-line",
             "alt": "A boy in a pale green robe with a dark topknot rides a galloping chestnut pony across a sunlit meadow with a bow raised in one hand, a small orange and white cat clinging to the pony's flank, a man in dark robes running through the middle distance, rows of courtiers under striped awnings at left, a stone-arched bridge over a river at right and rough stone footings in the foreground",
             "caption_html": """A half-breath late to the starting line, <a href="../characters/azuki.html">Azuki</a> has the pony's hock, <a href="../characters/kurige.html">Kurige</a> bolts across the meadow with <a href="../characters/kiyomaro.html">Kiyomaro</a> in the saddle, and Tomobe no Higaide, forty paces off, begins to run."""},
            {"slug": "was-my-thumb-right",
             "alt": "A man in dark robes with a topknot bends low over a boy in a pale green robe who lies on a bolster with one hand at the man's sleeve, a pair of swords laid on the matting beside them, court ladies standing in the pale light of a silk-walled pavilion behind and a white-haired man in purple robes kneeling with folded hands at the right",
             "caption_html": """In the ranked families' pavilion <a href="../characters/kiyomaro.html">Kiyomaro</a> finds Tomobe no Higaide's sleeve and asks whether his thumb was right at the nock; &ldquo;Perfect,&rdquo; says Higaide, and the Minister of the Left kneels nearby and says nothing at all."""},
            {"slug": "the-warmed-cushion",
             "alt": "An old white-haired man in a grey robe sits in a carved chair beside a moonlit window over snowy peaks, holding a glowing cushion against his chest beneath his robe, an orange and white cat sitting at his feet and a tall grey-robed figure standing in a doorway behind a lantern",
             "caption_html": """On the night of the pyre Sugino no Arikuni warms the cold cushion against his chest beneath his robe before setting it down for <a href="../characters/azuki.html">Azuki</a>, who has refused her dinner for three days; the steward Tamenaga waits inside the screen to ask whether the lamp may be lit."""},
            {"slug": "the-sparrow-examiner",
             "alt": "A stooped grey-haired man in a green robe with a bundle of papers under one arm scatters a handful of rice over sunlit gravel as dozens of sparrows swoop down around his sandals, smiling clerks in black caps watching from a wooden porch behind him and a low sun over distant hills",
             "caption_html": """Every morning in the courtyard of the Bureau of Inquiry, Ōmi no Yasutsugu sets aside a handful of rice from his own bowl and scatters it on the gravel, and the sparrows come down in a brown rush around his sandals; his clerks, watching from the porch, call him the Sparrow Examiner, not unkindly."""},
            {"slug": "the-night-before",
             "alt": "A lean man with a dark topknot kneels in lamplight and works at the hair of a small girl in a white nightrobe who leans against him with her eyes closed, two swords on a rack on the wall behind them, a tall woman in a plum-colored robe standing in an open doorway at the right holding a sheet of paper and a lacquer box, and yellow leaves falling in the dark garden behind her",
             "caption_html": """On the night of the nineteenth of Garren, Tomobe no Higaide kneels to redo the braid of his six-year-old daughter <a href="../characters/tsuru.html">Tsuru</a>, which he has never been permitted to do and does badly, while <a href="../characters/shizuka.html">Shizuka</a> waits in the doorway with the lacquer box of his poems."""},
            {"slug": "dawn-at-mikusa",
             "alt": "A man in a dark robe with a topknot and two swords at his hip rests his left palm on a grey stone pillar bound with a straw rope on a dark wooden plinth and dissolves into a spray of pale glittering grain streaming sideways into the stone, a bald priest with a straw broom at the left, three white-robed priests and a dark-robed man seated on a low dais behind, and an old man in grey with a cat on his lap at the right, over raked white gravel beneath tall cedars",
             "caption_html": """At the grey of dawn on the twentieth of Garren, Tomobe no Higaide sets his left palm on <a href="../characters/the-kiyote-pair.html">the Stone</a> of Mikusa and goes into it as pale grain, in the sight of <a href="../characters/jokei.html">Jōkei</a>, his <a href="../characters/three-senior-priests.html">three senior priests</a> and a Minister with <a href="../characters/azuki.html">Azuki</a> curled in the fold of his sleeve."""},
            {"slug": "the-stranger-at-the-doorstone",
             "alt": "A tall figure in dark robes with a sword at his hip rests his palm on the top of a grey granite block marked with a column of notches on its flank and shimmers into being out of glowing golden grains at sunset beneath an oak tree, a small boy with a switch gazing up at him from the left, a man with a satchel stopped on a path behind, and thatched cottages sending up smoke on the hillside below",
             "caption_html": """At dusk on the nineteenth of Garren the pale grain of Tomobe no Higaide pours back up out of the <a href="../characters/the-kiyote-pair.html">tally-stone</a> of Vilarnau into the shape of a man with his palm still on its face; Peire, eight, watches with a switch in his hand, and on the road above <a href="../characters/observer-618.html">Observer 618</a> stops walking."""},
            {"slug": "the-weighing",
             "alt": "A lean man in a dark robe with a topknot holds a blade in each hand and turns aside the stroke of a mounted knight in chain mail whose long sword spins away through the air at the upper right, a grey horse rearing in the foreground, villagers crowding at the left including a boy with a hand over his mouth, a stout man in brown with a scroll and a rank of helmeted men-at-arms standing at the right",
             "caption_html": """On the morning of the weighing at Vilarnau, Sir <a href="../characters/bertran.html">Bertran</a> brings his long sword down from the saddle and loses it, spinning, to a stranger's left hand; the bailiff <a href="../characters/arnaut.html">Arnaut</a> stands by with his men, and a boy named Peire has clapped a hand over his mouth to keep from laughing."""},
            {"slug": "solans-fire",
             "alt": "A tall man in a brown tunic bows with his palms pressed together before a huge bonfire with a whole pig roasting on a spit, a laughing woman in a red skirt with a hand on his back at the left, a priest in black with a white stole and a cloth over his arm standing beyond the flames, villagers' backs and hands passing a wooden cup in the foreground, and thatched houses with lit windows and a church tower under a dark blue sky",
             "caption_html": """On the twenty-eighth of Havren, at the great fire of Solan, Tomobe no Higaide bows to the god's flame as he was taught in his own country, with <a href="../characters/ermengarda.html">Ermengarda</a> laughing behind him where she has pushed him into the front rank and the hearth-priest Father Guiraut watching with a serving-cloth over his arm; he will shortly refuse the first slice of the pig."""},
            {"slug": "the-barn",
             "alt": "A man in a dark tunic kneels in straw with his forehead pressed against the flank of a huge red ox, two swords laid on the straw in front of his hands, a girl with a long braid and a younger boy standing at the foot of a ladder behind him, and a window of sunset sky at the upper left of a stone barn",
             "caption_html": """Shortly after <a href="../characters/bernat.html">Old Bernat</a> has shown him the fieldstone where <a href="../characters/kaneyoshi.html">Kaneyoshi</a> lies, Tomobe no Higaide kneels against the red ox Lo Rog in the barn and, his two swords laid in the straw, vows in his own language not to draw them in this house; <a href="../characters/gersenda.html">Gersenda</a> keeps her small brother back."""},
            {"slug": "the-stone-holds-a-man",
             "alt": "A red-bearded nobleman in a fur-collared mantle faces a lean man in a brown tunic across a waist-high granite block wreathed in holly and ivy with red berries, a great grey wolfhound pressing its nose into the lean man's hand at the right, two stonemasons with a sledge-hammer and broken iron wedges on the ground at the left, a knight on a grey horse and ranks of men-at-arms with spears and banners behind, and a crowd of villagers watching across a frosty village green",
             "caption_html": """On the green at Vilarnau Baron <a href="../characters/aimeric-2231.html">Aimeric</a> stands over the holly-wreathed stone, two of his <a href="../characters/masons-of-castelmaur.html">masons</a> beside their broken wedges, while <a href="../characters/ors.html">Ors</a> puts his nose into the stranger's palm and <a href="../characters/bertran.html">Bertran</a> watches from his grey gelding; the guest has just said that this is his door."""},
            {"slug": "the-bridge-at-the-lower-race",
             "alt": "A man in a brown tunic stands with a long sword in each hand on a narrow plank over black water between two stone walls, a hooded woman carrying a child and other villagers crowded on the lane behind him, a burning village with its roofs in flames glowing beyond them, and the iron helmets and spear points of a mass of soldiers with torches filling the foreground",
             "caption_html": """On the night of the torches, with the east lane burning behind them, Tomobe no Higaide stands in the mouth of the lane with a sword in each hand while the others, led by <a href="../characters/gersenda.html">Gersenda</a>, cross the plank into the dark; the <a href="../characters/castelmaur-men-at-arms.html">men-at-arms</a> in front of him have no instruction for this, and nobody wishes to be next."""},
            {"slug": "the-quarry-gate",
             "alt": "A lean man in a leather apron holds a lantern beside a wooden gate in a rock face as a line of ragged villagers files past him, a woman clutching a bundled child in the foreground, an old woman with a staff, a red ox in the middle of the line and a man in a dark robe with a bloodied sword in each hand walking at the right, a burning village glowing red in the valley below under a dark sky",
             "caption_html": """At the top of the quarry road <a href="../characters/observer-618.html">Observer 618</a>, as a mute stonecutter, holds a lantern beside the gate he latched at the end of the shift and has now unlatched, while the <a href="../characters/villagers-of-vilarnau.html">villagers</a> of Vilarnau file past him with their children and a red ox, Tomobe no Higaide behind them with both swords still drawn, and the valley burns below."""},
            {"slug": "the-eleven-sheets",
             "alt": "An old white-haired man in a grey robe has slid to his knees on a stone floor with his forehead against the edge of a wooden table where sheets of paper lie in lamplight beside a broken red seal and cord, a thin russet cat walking toward him through a pool of light, shelves of bundled documents behind him and a barred window at the upper right with small birds beyond it",
             "caption_html": """In the lower archive of the Bureau of Inquiry Sugino no Arikuni, who has read the Examiner's eleven sheets twice, has slid from the stool to the floor with his forehead against the table, and <a href="../characters/azuki.html">Azuki</a>, old and thin, comes into the lamplight to climb into his lap."""},
        ],
    },
    {
        "slug": "0247", "title": "The Tear of the Dragon",
        "status": ["coming-soon"],
        "cover_file": "0247.jpg",
        "hook": "Copied. Borrowed. Ledger. Unwilling. Hollow.",
        "case_tag": "Case 0247",
        "catalyst": {
            "name": "The Dragon's Tear",
            "meta": "Mythic Class",
            "page": "characters/the-dragons-tear.html",
            "img": "characters/the-dragons-tear-thumb.jpg",
            "html": "<p>A still mountain spring in a stone basin near the shoulder of Mount Qingxuan, fed by no visible source and drained by no visible outlet, that copies the complete memory and skill of the last person to touch its waters into the next person who drinks, overwriting itself with each deposit. The valley tells of a grieving dragon whose single tear never finished falling; by every test the mountain's hermits devised across three centuries, it is only water. It hands over a whole life at a time, and has never learned to hand across only the parts a man asks for.</p>",
        },
        "envoy": {
            "name": "The Hollow Hermit",
            "meta": "Custodian, Terrarium Designation Qingxuan",
            "page": "characters/the-hollow-hermit.html",
            "img": "characters/the-hollow-hermit-thumb.jpg",
            "html": "<p>Custodian of record for the Dragon's Tear, working in the open as the shrine-keeper at the spring: a silent old man the valley below has called the Hollow Hermit for longer than anyone can say, who is left rice and oil twice a year and asks nothing in return. He speaks the same two words twice, once to the master who came to die at the water and once to the disciple who came looking for what he left, and files his reports under the Prime Directive in the dry third person of his office, noting in them how often <em>correctly</em> is a word he finds himself needing.</p>",
        },
        "pages": EDITOR_PAGES,
        "genre": EDITOR_GENRE,
        "synopsis_html": EDITOR_SYNOPSIS,
        "characters": [
            {
                "slug": "the-hollow-hermit", "name": "The Hollow Hermit",
                "epithets": "Cultivator Envoy and Custodian of record for Case 0247 &middot; shrine-keeper at the Dragon's Tear &middot; appears in his seventies by his sheet",
                "teaser": "Keeps the shrine at a spring that takes a lifetime, says the same two words twice, and prevents nothing.",
                "bio_html": """<p>An old man who keeps the shrine at the northern lip of the pool, in a hut no larger than a single room, and has kept it for a span of years no single lifetime should reasonably cover and the valley below cannot agree on. They call him the Hollow Hermit and leave rice and oil at his door twice a year, more from habit than devotion, since he asks nothing of anyone and answers almost nothing when asked. When <a href="../characters/kuang-zhi.html">Kuang Zhi</a> crosses the last of the scree and sinks to his knees at the water, the hermit offers no hand and says only <em>Not the first</em>, and nothing else for the rest of that day or the next. He sits three feet away through the night and does nothing whatsoever to prevent the old master's death.</p>
          <p>His file is that of a Custodian, Terrarium Designation Qingxuan, kept in the third person and the dry language of the office, and it records what the valley never learns: that the deposit was self-directed and no Cultivator guidance was offered, that a seventy-two-hour monitoring window he requested was denied on the standing ground that seventy-two hours has been enough in three hundred and eleven years of comparable observation, and that three shepherds drank at the southern bank eighty-nine hours after the master died. He watches <a href="../characters/bai-rong.html">Bai Rong</a>'s hands find the Founder's Welcome from thirty feet off, behind a fold of rock, and logs everything but what he feels, because the ledger keeps no field for it. When <a href="../characters/shen-lie.html">Shen Lie</a> seizes his robe and demands to know what he means, he says the same two words again and turns his palm up to show three sets of footprints already three days stale. No one in the whole account thinks to ask him anything at all. His closing log finds no error in its finding and notes that being correct has not made it easier to file; he has asked to be reassigned, and the request is pending. His sheet says outright that his appearance is invented from his role; the manuscript describes him only as an old man.</p>""",
            },
            {
                "slug": "the-dragons-tear", "name": "The Dragon's Tear",
                "epithets": "A mountain spring near the shoulder of Mount Qingxuan &middot; the Catalyst of Case 0247 &middot; Mythic Class",
                "teaser": "A still pool that copies the whole memory and skill of the last person to touch it into the next person who drinks.",
                "bio_html": """<p>A spring in a stone bowl near the mountain's shoulder, wide enough that the shrine and the Hollow Hermit's hut stand on its northern lip while the gentler southern bank, a hundred paces off and screened by a shoulder of bare rock, is where the grazing paths actually reach the water. It is fed by no visible source and drained by no visible outlet, and so still that pilgrims mistake the reflection of the sky for a hole clean through the mountain. The story attached to it is that a dragon, grieving a mate slain in wars so old no record survives them, wept once and never again, and that the single tear never finished falling. Generations of monks built a shrine to the story rather than to the water, because the water offered nothing else to venerate: no light, no warmth, no voice. By every test the mountain's hermits devised in three centuries, it was only water.</p>
          <p>What it does is copy. The complete memory and skill of the last person to touch its waters pass, without translation, to the next person who drinks, and the spring overwrites itself with each deposit. <a href="../characters/kuang-zhi.html">Kuang Zhi</a> gives it seven drops of blood and his whole face, and dies. Eighty-nine hours later three shepherds drink at the grazing bank, and <a href="../characters/bai-rong.html">Bai Rong</a>, the last and the longest, carries a stranger's lifetime down the mountain. The second time the water gives <a href="../characters/shen-lie.html">Shen Lie</a> a copy and not a restoration, with the shepherd's six weeks braided into it; Bai Rong survives and keeps his own thirty-one years, and the Custodian's working hypothesis is that depth follows submersion time and the age of the memory. Nothing in the pool ever takes a life apart into pieces small enough to hand across only what is asked for. The sheet adds a basin forty to fifty feet across, a worn lip at the north bank, ordinary livestock wear at the south and no markings, and shows the water unnaturally cold for Kuang Zhi and unnaturally warm for Bai Rong; the manuscript gives none of those figures and says only that the second time the water was not as cold as water at that altitude had any right to be.</p>""",
            },
            {
                "slug": "kuang-zhi", "name": "Kuang Zhi",
                "epithets": "Grandmaster and founder of the Hollow Pine Sect &middot; 71 years old by his sheet",
                "teaser": "Climbs a mountain alone to put forty years of technique where no student could thin it, and dies at the water before anyone claims it.",
                "bio_html": """<p>The builder of the Hollow Pine Sect, which he raised from a single borrowed courtyard into the most quietly respected martial school in three counties: no standing army, no official patronage, and in forty years not one duel it had not first tried three separate ways to avoid. He had come to believe that a lifetime of technique does not survive being written down. Words thin it, demonstration thins it faster, and his own body had been in decline for the better part of a decade. The spring, if the hermit's stories were even a tenth true, was the one method of transmission that copied and did not translate.</p>
          <p>He chose <a href="../characters/shen-lie.html">Shen Lie</a> because the boy asked questions no one else thought to ask and forgot afterward that he had asked them, and ranked him above two more talented seniors without telling either of them why. He sent him two days south on an errand any junior could have run, and told no one where he himself was going. He climbs Mount Qingxuan alone, on legs that had not carried him unassisted in three years, opens his smallest left finger with a blade no longer than a fingernail, lets seven drops fall and holds his whole face under the water, and dies before dawn with the <a href="../characters/the-hollow-hermit.html">Hollow Hermit</a> three feet away. His wish, that his gift wait for exactly one throat, is undone by thirst, a wandering ewe and three days' difference between one man's errand and another man's walk. His tea was a bitter northern leaf no one else in the sect could stomach. The chroniclers will call the war that follows the War of the Stolen Style and give him no part in it beyond, in some tellings, a sword. His sheet gives his age as 71, a tall lean frame once broad-shouldered and thinned by illness, and a white topknot and long white beard.</p>""",
            },
            {
                "slug": "shen-lie", "name": "Shen Lie",
                "epithets": "Chosen disciple and heir of Kuang Zhi &middot; later founder of the reformed Hollow Pine Sect &middot; 27&ndash;29 by his sheet",
                "teaser": "Hunts the man who drank his master's gift, and comes away the only person alive who remembers four killings he did not commit.",
                "bio_html": """<p>Eleven years <a href="../characters/kuang-zhi.html">Kuang Zhi</a>'s student, and so used to an old man who never once complained of a late return that when he comes back from the south two days behind schedule he is entirely unbothered. He finds the shrine's candles burned down untended and his master half in the water, and he fails the way a structure fails when its load-bearing wall stops being a wall: knees first, then breath, then a sound he did not choose. He winds a length of undyed hemp cord torn from the dead man's robe once around his own left wrist, drinks from the spring, certain the gift is waiting, and feels nothing. When the <a href="../characters/the-hollow-hermit.html">Hollow Hermit</a> turns his palm up to show footprints, he decides, with the cold procedural clarity Kuang Zhi once praised in him, that the thief will be found, kept alive, walked back up the mountain and made to give everything back, and only then will he drink. He pays <a href="../characters/old-cao.html">Old Cao</a> for the shepherd's whereabouts and climbs to a hollow three ridges east with a rope for restraint and a blade for emergencies only, a lie he believes less with every step.</p>
          <p><a href="../characters/bai-rong.html">Bai Rong</a> greets him in his master's cadence, and a volley of Xuanwu arrows breaks the meeting; the shepherd throws him behind a rock hard enough to break two of his ribs and snap the cord at his wrist. When word of the war reaches them through a passing trader, he understands at once how a scrap of Hollow Pine hemp came to lie in that clearing, and they go back up the mountain. At the water the second time the copy arrives terror first, the memory of four strangers dying under his own hands, and then forty years of technique braided inseparably through six weeks of a shepherd's life: the only living man who has killed no one and remembers having done it. He rebuilds the Hollow Pine Sect on the same mountain with <a href="../characters/wei-bo.html">Wei Bo</a>'s memory, not Kuang Zhi's, as its founding lesson, names no heir, teaches nine or ten students in the open, and flinches once a year at the smell of a bitter northern tea he nonetheless keeps in his own kitchen. The manuscript is explicit that the reform answers his own wound and not the war's actual cause. His sheet notes that his injuries and the tea-flinch are stated directly in the manuscript, and that his age and every other physical detail are invented.</p>""",
                "quote": "Give it back the way it came.",
            },
            {
                "slug": "bai-rong", "name": "Bai Rong",
                "epithets": "Shepherd &middot; unmarried, in debt to the county tax collector &middot; 31 years old",
                "teaser": "Goes up the mountain after a ewe, drinks last and longest, and spends the rest of the story trying to give it all back.",
                "bio_html": """<p>Thirty-one, unmarried, and owing the county tax collector a sum he calculates will take another eleven years to clear. He climbs Mount Qingxuan for a ewe, since a ewe is worth more to him than his own dignity, and finds her standing at the water's edge. He drinks last and longest, with his face almost to the surface, and for three breaths feels nothing at all. Then the knowledge arrives, less like remembering than like realizing he has walked a road ten thousand times without once looking at it, and his hands, which had held nothing sharper than crooks and shears, find the Founder's Welcome, four days after another man died in the same posture at the same water.</p>
          <p>He wants nothing more complicated than enough saved silver to see the capital's lantern festival once, a wish he has never told anyone, and he can no longer tell which of his wants are his own. At his mother's gate his hand puts a garrison-trained man on the ground in about four seconds, and the horror on his face convinces <a href="../characters/deputy-song.html">Deputy Song</a> faster than the throw. In the clearing he fights as <a href="../characters/kuang-zhi.html">Kuang Zhi</a> fought forty years earlier, and afterward finds that the hands that killed a young stranger feel entirely like his own, which frightens him more than the alternative. He survives the second submersion, keeps his own thirty-one years and gives back everything that was not his, goes home for eleven days to a forgiven debt, and leaves on the twelfth. He reaches the capital in time for that year's festival and stands in a crowd that does not know his name, thinking of nothing at all, which he will call the best evening he ever spent. His last words to <a href="../characters/shen-lie.html">Shen Lie</a> are <em>Go build something with whatever's left of him in you. I already know it's good enough.</em> The chronicles will give him the crime of theft, and the valley a dragon. His sheet draws him lean and sun-tanned, hollowed after the spring.</p>""",
                "quote": "I don't always know which parts are mine.",
            },
            {
                "slug": "xuanwu-kai", "name": "Xuanwu Kai",
                "epithets": "Grandmaster of the Xuanwu Sect &middot; 52 by his sheet",
                "teaser": "Invokes a clause no Grandmaster has ever needed, over a single strand of hemp, and never asks the second question.",
                "bio_html": """<p>Grandmaster of a sect that has stood in the provincial capital for six generations, founded by General <a href="../characters/kang-yi.html">Kang Yi</a>, last Grand Marshal of the Yan's northern garrisons, and that in all that time has never lost a named disciple to violence outside a sanctioned duel: a record he treats as close to sacred law as anything the sect never bothered to write down, on the theory that a rule no one has needed to test does not require ink. When his only son, three months from his own succession, is killed in a clearing, he receives the jade token before the body and for the length of one held breath believes the boy lost it gambling. He does not weep in front of his disciples, then or in the seven days of ritual mourning, a restraint every disciple admires and misreads; it is the discipline of a man who has found exactly one place to put his grief that does not require weeping.</p>
          <p>On the eighth morning he invokes before the assembled sect a clause of the founding oath no Grandmaster has ever had to speak aloud: that a named disciple's death by another sect's hand, outside sanctioned combat, is a debt owed in the sect's own coin and no other, not the province's courts, not the throne's soldiers, not even the sect's own survival. Nothing in it requires him to confirm who killed his son, and six generations of never needing it have left no procedure for doubting it. A search three days later finds a strand of Hollow Pine mourning hemp near where the young master fell, and he declares war that evening without sending word. The war lasts forty-one days and kills perhaps sixty people to avenge one. He lives nineteen years more and rebuilds the sect's numbers within five, and eleven years after the war a retired soldier tells him that the timing never fit. He takes the founding oath from its case that night, reads in its margin the founder's two words, <em>revise later</em>, and never revises the record by so much as a character. His sheet draws him imposing and disciplined, about six feet, with a short beard and grey-streaked black hair; its age and build are its own.</p>""",
            },
            {
                "slug": "chen-wu", "name": "Chen Wu",
                "epithets": "Shepherd &middot; Fang's cousin &middot; 32&ndash;34 by his sheet",
                "teaser": "Drinks first and feels nothing, then asks Bai Rong what in the ancestors' name he thinks he is doing.",
                "bio_html": """<p>One of the three shepherds who climb the goat track above the terraced fields after half a dozen animals that have wandered further than any sensible animal should, and arrive thirsty, irritated and entirely uninterested in dragons at the pool's southern bank. The story of the tear is, to men who grew up two valleys over and heard it told wrong a hundred times, the kind that stops frightening a child around the age it stops being new. Chen Wu drinks first and feels nothing.</p>
          <p>When <a href="../characters/bai-rong.html">Bai Rong</a> straightens into a stance no shepherd should know, he asks, half-laughing, what in the ancestors' name he thinks he is doing, his mind already halfway back down the mountain to a daughter running a fever, and he never gets an answer of any kind. The manuscript gives him no more than that. The sheet adds a stocky, deeply tanned man with a short unkempt beard, a hemp tunic and a staff, and shows him afterward questioning Bai Rong over the shift into the Founder's Welcome; its age, build and the rest are its own.</p>""",
            },
            {
                "slug": "fang", "name": "Fang",
                "epithets": "Shepherd &middot; Chen Wu's cousin &middot; 27&ndash;29 by his sheet",
                "teaser": "The second of the three to drink at the southern bank, and the second to feel nothing.",
                "bio_html": """<p>Chen Wu's cousin, one of the three shepherds who reach the grazing bank four days after <a href="../characters/kuang-zhi.html">Kuang Zhi</a> has died on the screened northern bank. He drinks second and feels nothing; <a href="../characters/bai-rong.html">Bai Rong</a> drinks after him.</p>
          <p>The manuscript names him only that once. His sheet carries the rest: a slim, wiry man with patchy stubble and a coarse wool cloak, shown drinking from the pool as the second of three, and given four moods from observant to resolute. Its age and every other detail are its own.</p>""",
            },
            {
                "slug": "widow-bai", "name": "Widow Bai",
                "epithets": "Bai Rong's mother &middot; a widow of the valley &middot; 55&ndash;58 by her sheet",
                "teaser": "Offers every collector tea at the gate, and never once asks her son what his hands have done.",
                "bio_html": """<p>Meets the county tax collector's men at the gate with the same tea she has offered every collector who ever came to that door, a habit thirty years of hardship has never taught her to drop even when there is nothing in the house worth protecting the ritual for. The loom and the two remaining goats are all that stand between the family and the sum, and her son stands in the doorway behind her with his arms crossed, saying nothing. When he puts a garrison-trained man on the ground she does not ask what he has done, then or in any night after, though twice he catches her looking at his hands the way a woman looks at a tool she no longer recognizes in her own kitchen.</p>
          <p>She goes with him and what remains of the herd to a hollow in the hills rather than wait in the valley for whichever kind of attention arrives first, and is still selling what cheese she has when a passing trader carries the news of the war. <a href="../characters/bai-rong.html">Bai Rong</a> comes home to her for eleven days and leaves on the twelfth with her blessing and a single unspent silver coin. The sheet draws a small, work-worn woman with weathered, sun-browned skin, grey hair in a low knot and callused hands, and gives her four expressions, endurance, concern, recognition and quiet relief; its age and build are its own.</p>""",
            },
            {
                "slug": "deputy-song", "name": "Deputy Song",
                "epithets": "Deputy to the county tax collector &middot; eleven years collecting in the valley &middot; 45 by his sheet",
                "teaser": "Has never needed to raise a hand to collect, and leaves one yard in four seconds without the sum.",
                "bio_html": """<p>Has collected from the valley for eleven years and prides himself, not without reason, on never once having needed to raise a hand to do it: reputation, in his own careful accounting, is worth considerably more than any single household's furniture. He comes to the Bai household on the ninth day after the mountain, four days later than the debt strictly allowed, with two men, drinks the widow's tea as he always does, names the sum, and gives the household until sundown to produce it or surrender the two remaining goats and the loom.</p>
          <p>Then his junior reaches for the loom and is put on the floor in about four seconds by the shepherd in the doorway, and the deputy takes his men and leaves without goats, loom or sum. He describes it to the magistrate, carefully and not entirely truthfully, as a tactical withdrawal, and tells the story exactly four times before deciding to stop, because each telling made the listener look a little less at a man who had shown restraint and a little more at a man who had run. The sheet gives him a modest official's robe in blue-grey, a ledger satchel at the hip, ink-stained fingers and no weapon but his two men, and shows him leaving without collecting the debt; its age and build are its own.</p>""",
            },
            {
                "slug": "old-cao", "name": "Old Cao",
                "epithets": "Information broker and tracker-for-hire &middot; 57&ndash;60 by his sheet",
                "teaser": "Finds people who do not wish to be found, and sells the same hollow twice.",
                "bio_html": """<p>Finds people who do not wish to be found, for clients who mostly do not wish to be seen finding them, from the back room of a wine shop in the county seat, and has done so, by his own cheerful estimate, for longer than most of his clients have been alive. He names his price before <a href="../characters/shen-lie.html">Shen Lie</a> has finished describing the shepherd and names it again, higher, when Shen Lie mentions the words Hollow Pine. He says he has found six hundred and eleven people in this trade and, so far as he knows, seen perhaps forty of them buried within the year, and that he does not ask what happens after his part is finished, which is in his professional opinion the only part of the arrangement worth keeping clean.</p>
          <p>Three days later he sends word: found. What Shen Lie does not know is that Old Cao has also sold the same location to the Xuanwu Sect for a second and considerably higher fee, which is how two parties come to the same hollow, and the Custodian can only call his professional consistency admirable. The sheet draws him pale from indoor work, thin-mustached, with grey thinning hair and quick, precise hands, habitually cheerful and unbothered, counting coins after delivering the information; its age and build are its own.</p>""",
                "quote": "I do not ask what happens after my part is finished.",
            },
            {
                "slug": "xuanwu-kais-son", "name": "Xuanwu Kai's Son",
                "epithets": "Heir apparent of the Xuanwu Sect &middot; 22 years old &middot; three months from his succession",
                "teaser": "Wants one thing in his father's sect to be entirely his own, and rides out to take it.",
                "bio_html": """<p>Twenty-two years old and three months from his formal succession as the sect's next Grandmaster, he insists on riding with the retrieval party himself rather than sending subordinates to claim what he has already decided will be his credit to take rather than his father's gift to inherit: the shepherd captured, the mystery solved, the succession secured on a victory earned and not a birthright accepted, the one thing in twenty-two years as his father's son he has never been allowed to say he did entirely alone. He is the fourth attacker in the clearing, younger than the others and better dressed beneath the plain Xuanwu grey, and he presses the attack longest and falls fastest, to a single strike.</p>
          <p>Neither <a href="../characters/bai-rong.html">Bai Rong</a> nor <a href="../characters/shen-lie.html">Shen Lie</a> notices until much later that he carries a jade token no ordinary disciple would have been trusted to take off the sect's grounds; they leave without searching the bodies, in the greater urgency of Widow Bai's safety, and it costs more than almost any deliberate choice either man makes. Bai Rong stands over him a moment longer than he needs to, registering only that he is young. A grimmer, more thorough search party recovers the token, and his death becomes the proximate cause of a war that kills perhaps sixty people to avenge him. The sheet draws him athletic and martial in plain Xuanwu grey over a finer concealed undergarment, with a personal blade finer than his companions'; its other details are its own.</p>""",
            },
            {
                "slug": "wei-bo", "name": "Wei Bo",
                "epithets": "Calligraphy instructor of the Hollow Pine Sect &middot; 52 by his sheet",
                "teaser": "Grinds ink for a lesson no student will receive, and walks to the gate with a staff made for demonstrations.",
                "bio_html": """<p>A soft-spoken calligraphy master who has never in his life held a blade in anger and long ago stopped pretending he ever would, and the sect's only other instructor of any seniority. He stays behind, as he always does, to keep the mountain's books and its brushes in order while the rest chase duels and errands, and alone among them has never once complained of the arrangement. When <a href="../characters/kuang-zhi.html">Kuang Zhi</a> climbs the mountain to die, Wei Bo is the one left at the school.</p>
          <p>Nine students are with him when the six hundred arrive: three surrender and are spared for information they do not have, two flee, and four gather at the courtyard gate before dawn behind him. In the last quiet hour he grinds fresh ink for a lesson no student will ever receive, because his hands need something familiar to hold and calligraphy is the only thing they have ever been steady enough for. When the forward line comes round the lower switchback he sets the ink aside, takes up a training staff meant for demonstration, and tells the other three that a school worth teaching in is worth dying in front of, the only complete sentence of his that anyone troubles to remember, which the histories will misremember as heroism and not the plain grief it was. <a href="../characters/shen-lie.html">Shen Lie</a> learns of it from <a href="../characters/bo.html">Bo</a>, and rebuilds the sect on Wei Bo's memory. His sheet draws him slight and pale from indoor work, with ink-stained fingers, a thin trimmed mustache and a topknot; its age and build are its own.</p>""",
            },
            {
                "slug": "the-mourning-cord", "name": "The Mourning Cord",
                "epithets": "A torn strand of undyed hemp &middot; the mourning-robe cord of Kuang Zhi &middot; a Hollow Pine relic",
                "teaser": "A keepsake tied to a wrist that a grieving search party reads as proof of an assassin.",
                "bio_html": """<p>A length of undyed hemp cord torn from the belt of the robe <a href="../characters/kuang-zhi.html">Kuang Zhi</a> died in, in the exact weave the Hollow Pine Sect has used for nothing else in forty years but a mourning-robe belt. <a href="../characters/shen-lie.html">Shen Lie</a> finds it among the folds when he gathers his master's effects and winds it once around his own left wrist, beneath his sleeve, where it stays unremarked and mostly forgotten for three weeks. It is torn and frayed rather than cut and carries no inscription; its weave alone says whose it is.</p>
          <p>In the clearing, as <a href="../characters/bai-rong.html">Bai Rong</a> sweeps Shen Lie bodily behind a stand of rock, the cord snaps clean through at his wrist. A more careful search three days later finds it caught on a branch not six feet from where the young master fell, and to the searchers a single strand is more confirmation than six generations of certainty require; <a href="../characters/xuanwu-kai.html">Xuanwu Kai</a>, who has already invoked the clause, declares war that evening. Shen Lie works out what it was only when the news reaches him. Its innocent origin is lost, and the chronicles name the conflict the War of the Stolen Style when it was, as the closing pages put it, a length of mourning cord and a father who could not afford to ask a second question.</p>""",
            },
            {
                "slug": "chen-rui", "name": "Chen Rui",
                "epithets": "Hollow Pine student &middot; one of the three who stayed &middot; 25 by his sheet",
                "teaser": "Stays behind to bury what the six hundred left, and gives Bai Rong the number.",
                "bio_html": """<p>One of three students, with <a href="../characters/old-fen.html">Old Fen</a> and <a href="../characters/bo.html">Bo</a>, who stay at the mountain school after the six hundred have gone, rather than scatter with everyone else who could, to bury what the soldiers left behind. When <a href="../characters/shen-lie.html">Shen Lie</a> and <a href="../characters/bai-rong.html">Bai Rong</a> come down the mountain three days after the recall, they find swept courtyards and a gate repaired badly but repaired.</p>
          <p>When Bai Rong asks how many died in all, not Wei Bo alone but the soldiers and the bystanders and everyone the valley will give up trying to count, it is Chen Rui who gives him the roughest figure available, and Bai Rong says nothing more that day. The sheet draws him lean and tired, with a fresh scar along one forearm, dirt-stained hands and knees and training garb stained from burial work, giving the casualty count; its age and build are its own.</p>""",
            },
            {
                "slug": "old-fen", "name": "Old Fen",
                "epithets": "Hollow Pine student &middot; one of the three who stayed &middot; 58 by his sheet",
                "teaser": "The oldest of the three who stayed to bury the dead.",
                "bio_html": """<p>One of the three students who remain at the mountain school after the war, with <a href="../characters/chen-rui.html">Chen Rui</a> and <a href="../characters/bo.html">Bo</a>, to bury what the six hundred left. The manuscript names him once and gives him nothing more.</p>
          <p>His sheet fills in the rest: a spare, weathered, grey-bearded man with his hair tied back and a slight limp or stiffness, in patched cloth wraps, shown seated on the mountainside looking out over the school, and given four expressions from calm to a faint smile. The age, build and expressions are all its own.</p>""",
            },
            {
                "slug": "bo", "name": "Bo",
                "epithets": "Hollow Pine student &middot; about 14 years old",
                "teaser": "Tells the whole account of Wei Bo's death unasked, plainly, as children tell the worst stories.",
                "bio_html": """<p>A boy of perhaps fourteen, one of the three who stay behind to bury the dead. It is Bo who tells <a href="../characters/shen-lie.html">Shen Lie</a> and <a href="../characters/bai-rong.html">Bai Rong</a> the whole of it without being asked, the way children tell the worst stories, plainly and completely, because no one has yet taught them which parts to spare a listener. It is from him that Shen Lie learns, for the first time as more than a name, that <a href="../characters/wei-bo.html">Wei Bo</a> spent his last quiet hour grinding ink for a lesson he would never give and went to the gate anyway.</p>
          <p>His sheet draws a slight, still-adolescent boy with a round face, short cropped black hair, dark eyes and a few fading bruises from hardship, in patched pine-green and charcoal, and gives him four expressions: unease, resolve, grief and truth. Its details are its own.</p>""",
            },
        ],
        "scenes": [
            {"slug": "not-the-first",
             "alt": "An old man with a white topknot lies face down with his head beneath the surface of a still pool on a stone-paved bank at dawn, a small blade and a pool of blood on the stone beside him, while a white-bearded man sits cross-legged by a shrine hut and a stone lantern",
             "caption_html": """<a href="../characters/kuang-zhi.html">Kuang Zhi</a> at the water before dawn, his whole face beneath the surface and his blood on the stone beside the blade, as the <a href="../characters/the-hollow-hermit.html">Hollow Hermit</a> sits three feet away and does nothing whatsoever to prevent it."""},
            {"slug": "three-shepherds-at-the-southern-bank",
             "alt": "A dark-haired shepherd in a pale hemp tunic stands low with both palms turned outward beside a blue mountain pool, a shepherd with a crook looking on at his left and a third in a headband bending toward him at his right, a flock of goats grazing on the slope behind",
             "caption_html": """The southern grazing bank, four days after the master died: <a href="../characters/bai-rong.html">Bai Rong</a> rises from the water in a stance no shepherd was ever taught, weight low and both palms out, while <a href="../characters/chen-wu.html">Chen Wu</a> and <a href="../characters/fang.html">Fang</a> stare at him with the flock grazing behind."""},
            {"slug": "shen-lie-finds-the-body",
             "alt": "A young man with a dark topknot kneels at the edge of a still pool with his mouth open in a cry, an old white-haired man lying in the water below him, candles burning on a stone shrine at the left and a lone figure with a staff standing on a rise at the right under a grey mountain",
             "caption_html": """<a href="../characters/shen-lie.html">Shen Lie</a> back from his errand on the sixth day, among candle-stubs no one has refilled, finds his master half in the water; he does not weep so much as fail, all at once, in the manner of a structure whose load-bearing wall has stopped being a wall."""},
            {"slug": "bai-rong-at-the-gate",
             "alt": "A lean bearded man in a pale tunic grips the wrist of a man in dark robes who is thrown off his feet and sliding in the dust, a wooden loom in an open doorway behind them and two officials in dark robes and black caps watching with startled faces beside a fence",
             "caption_html": """The tax collector's junior reaches for the loom and is put on the ground in about four seconds by <a href="../characters/bai-rong.html">Bai Rong</a>, moved, as the manuscript has it, the way a door is moved; <a href="../characters/deputy-song.html">Deputy Song</a> and a second man watch from the gate."""},
            {"slug": "widow-bai-watches-his-hands",
             "alt": "An older woman with grey hair in a low knot stands in a lamplit doorway with her hands clasped, looking down with a worried face at a dark-haired man seen from behind, whose hands rest on a wooden table beside an oil lamp and two bowls",
             "caption_html": """<a href="../characters/widow-bai.html">Widow Bai</a> across the lamplit table, looking at her son's hands the way a woman looks at a tool she no longer recognizes in her own kitchen, and never once asking what they have done."""},
            {"slug": "old-cao-counts-the-coins",
             "alt": "A smiling grey-haired man with a thin mustache stacks coins on a small table in a back room lined with jars and lit by a hanging lantern, facing a hooded man with a dark topknot seen from behind",
             "caption_html": """<a href="../characters/old-cao.html">Old Cao</a> in the back room of the wine shop, counting coins <a href="../characters/shen-lie.html">Shen Lie</a> has not yet agreed to pay, and naming his price again, higher, once the words Hollow Pine have been said."""},
            {"slug": "the-fire-in-the-hollow",
             "alt": "A bearded man in a ragged pale tunic crouches low in a pine forest with both palms turned outward beside a dying fire, while a younger man with a rope slung over his shoulder and a hand on a blade stops in the trees behind him",
             "caption_html": """In the hollow three ridges east, <a href="../characters/bai-rong.html">Bai Rong</a> turns from the dying fire into the Founder's Welcome as <a href="../characters/shen-lie.html">Shen Lie</a> reaches the clearing with a rope for restraint and a blade for emergencies only."""},
            {"slug": "the-shepherds-reckoning",
             "alt": "A bearded man in a torn pale tunic strikes outward with an open palm in a smoky forest clearing, fallen men in grey lying on the ground around him and embers glowing among the leaves",
             "subjects": ["bai-rong"],
             "caption_html": """What <a href="../characters/bai-rong.html">Bai Rong</a> does in the clearing takes a few minutes and no wasted motion, the way the dead master fought forty years before; the songs will call it the shepherd's reckoning, and flatter it with a moral tidiness the minutes themselves did not have."""},
            {"slug": "the-oath-is-invoked",
             "alt": "A tall man with long white hair and a white beard, in a black robe with silver trim, stands with one palm raised in a great hall of tall blue banners bearing a tree, with rows of seated students in grey robes and racks of spears around him",
             "caption_html": """On the eighth morning of mourning, <a href="../characters/xuanwu-kai.html">Xuanwu Kai</a> stands before the assembled sect and invokes the clause of the founding oath that no Grandmaster in six generations has had to speak aloud; nothing in it requires him to confirm who killed his son."""},
            {"slug": "back-up-the-mountain",
             "alt": "Two men in ragged tunics with packs climb a rocky mountain track, the one in front in pale hemp looking back over his shoulder and the one behind him in grey holding his side, a terraced valley and a river below and a tall column of black smoke rising from a far hillside",
             "caption_html": """<a href="../characters/bai-rong.html">Bai Rong</a> and <a href="../characters/shen-lie.html">Shen Lie</a>, Shen Lie holding his broken ribs, take the goat track back toward the mountain at midday; three valleys behind them the first true battle of a war neither chose is already three hours old."""},
            {"slug": "the-second-emptying",
             "alt": "A young man with a dark topknot kneels on a rocky shore with both hands on the back of a man lying face down with his head beneath the surface of a still pool, a white-haired, white-bearded man seated on the rocks behind them with a staff, snow peaks and cloud beyond",
             "subjects": ["bai-rong", "shen-lie", "the-hollow-hermit"],
             "caption_html": """<a href="../characters/bai-rong.html">Bai Rong</a> lowers his face beneath the water where <a href="../characters/kuang-zhi.html">Kuang Zhi</a> died, and <a href="../characters/shen-lie.html">Shen Lie</a> counts eleven held breaths while the <a href="../characters/the-hollow-hermit.html">Hollow Hermit</a> watches from the rock, saying nothing."""},
        ],
    },
    {
        "slug": "1153", "title": "The Second Hand",
        "status": ["published", "google-books"],
        "cover_file": "1153.jpg",
        "hook": "Hand. Debt. Doctrine. Mercy. Exile.",
        "case_tag": "Case 1153",
        "catalyst": {
            "name": "The Eleven-Fingered Hand",
            "meta": "Grafted prosthetic left hand",
            "page": "characters/the-eleven-fingered-hand.html",
            "img": "characters/the-eleven-fingered-hand-thumb.jpg",
            "html": "<p>A grafted prosthetic left hand with eleven digits: two thumbs set opposite each other on one broad palm, and beneath them two folding rows of ordinary fingers, four in plain sight and five more folded flat behind. Fitted over three nights to a prince whose own hand had been unmade in a ritual duel, it serves him better than the original ever did. A kingdom spends eighteen years deciding whether it is a hand at all.</p>",
        },
        "envoy": {
            "name": "Observer 419",
            "meta": "&ldquo;the clockmaker&rdquo; &middot; also the Envoy of Case 2140",
            "page": "characters/observer-419-1153.html",
            "img": "characters/observer-419-1153-thumb.jpg",
            "html": "<p>The same Observer as <a href=\"../books/2140.html\">Case 2140</a>, posted next to Tavgora under cover as a clockmaker whose brass instruments never lose a second. He grafts the hand in three nights and is gone by the next dawn &mdash; then keeps watching, against the letter of a posting formally concluded, from a rented room two valleys away, until a column leaves a burning city by a goat track and he leaves a field on his form open for thirty-four seconds too long.</p>",
        },
        "pages": EDITOR_PAGES,
        "google_books_url": "https://play.google.com/store/books/details?id=3IYZEgAAQBAJ",
        "genre": EDITOR_GENRE,
        "synopsis_html": EDITOR_SYNOPSIS,
        "characters": [
            {
                "slug": "levan", "name": "Levan",
                "epithets": "Son and heir of King Guram &middot; physician &middot; called Mikel in exile &middot; about 14 at the Proving, 32 at the war &middot; dies at 63",
                "teaser": "Loses a hand to a loose strap, wins one back from a stranger, and spends eighteen years being kind to everyone but his own claim.",
                "bio_html": """<p>The King's son, older than <a href="../characters/bagrat.html">Bagrat</a> by fourteen months and quieter by nature, more drawn to the physicians' wing of the palace than to the training yards. At the Proving a re-buckled strap gives way and four inches of real, Auron-blessed steel come down across his raised left hand; he does not scream, and looks, the court thinks, almost apologetic. Over three nights <a href="../characters/observer-419-1153.html">a clockmaker</a> fits him with <a href="../characters/the-eleven-fingered-hand.html">an eleven-fingered hand</a>, and it is Levan himself who counts the fingers first. No petition is ever filed to enter his name on the temple's succession rolls, because he never asks for one.</p>
          <p>He spends the next eighteen years as a physician, apprenticed to the three court doctors who once agreed his arm would have to go: laying his instruments out left to right in the same count every time, brewing the same bitter mountain tea for frightened patients, and playing a four-stringed lute alone, badly, for the pleasure of failing at something that costs no one anything. He saves Bagrat's arm in a six-hour surgery, refuses the throne twice, wins the duel called the Answer without drawing blood, and is carried out of Tavgora on the night its outer wall falls by <a href="../characters/otar.html">Otar</a> and eleven of his former patients. In Otsane he is &lsquo;Mikel&rsquo; to <a href="../characters/amets.html">Keeper Amets</a>, keeps a small, mostly unpaid surgery for thirty-one years, teaches four novices, writes the compendium he always wanted to write and leaves it to be copied freely, and dies there at sixty-three.</p>
          <p>The sheet draws him lean and wiry, with long angular face, deep-set dark-brown eyes, near-black hair and a close-trimmed beard that greys at the temples, in undyed charcoal, the grafted hand pale ivory-grey; it gives his age as about thirty-two during the central conflict, which the manuscript's arithmetic supports.</p>""",
                "quote": "I want no crown. I only wanted to see you stand.",
            },
            {
                "slug": "bagrat", "name": "Bagrat",
                "epithets": "Guram's nephew &middot; later King of Sarkveti &middot; 13 at the Proving, 31 at the duel &middot; reigns 26 more years",
                "teaser": "Cannot bear to owe his cousin an arm, builds a righteous case in one sleepless night, and spends six years searching for the man he exiled.",
                "bio_html": """<p>The orphaned son of King Guram's brother, taken by a fever with both parents in one winter, and raised alongside <a href="../characters/levan.html">Levan</a>, who taught him to swim in the cold river below Tavgora's walls. Thirteen at the Proving, when the strap on his blade gives and cuts his cousin's hand, he becomes the prince still standing: the temple seals a provisional entry for him within the week. He leads the answer to the Vashtir raids, takes an arrow low and wrong in the dark and a fall from a horse onto rock, and is carried home over eight days with his sword arm swollen black to the elbow, until Levan saves it.</p>
          <p>He cannot repay the debt. He offers the throne, then a duchy, a stipend and a title invented for the occasion, and is refused every time by a man who wants nothing. Crowned and unable to look at his own five ordinary fingers, he challenges Levan to the Answer, unwrapped steel in the open hall, and loses to mercy a second time: disarmed, unmarked, and spared. He kneels in a corridor behind the northern pillar, builds the entire righteous case in a single sleepless night from a sentence of <a href="../characters/demna.html">Demna</a>'s, and petitions for the Writ of Examination without reading the paragraph beneath it. He rules for twenty-six more years, spends nearly six of them quietly searching every unmapped fold of the western range, and keeps a small carved wooden horse Levan made him in a drawer under the state papers.</p>
          <p>The sheet draws him taller and broader than Levan, with dark wavy hair going grey, a square-trimmed beard after the coronation and a thin scar on the forearm Levan rebuilt; its own footnote says all of this is visual invention, since the manuscript describes only his ordinary, five-fingered hands.</p>""",
                "quote": "Then let us see if mercy can parry.",
            },
            {
                "slug": "guram", "name": "Guram",
                "epithets": "King of Sarkveti &middot; Levan's father, Bagrat's uncle &middot; late 50s at his death",
                "teaser": "Buries a wife, a brother and his patience for miracles with strings, and chooses an heir he asks to be left unannounced.",
                "bio_html": """<p>King of Sarkveti, father of <a href="../characters/levan.html">Levan</a> and uncle to <a href="../characters/bagrat.html">Bagrat</a>, who has buried a wife, a brother and most of his patience for miracles that come with strings attached. He takes the surgeons' verdict standing and dry-eyed, as the histories like to say every Sarkveti king took bad news, then walks the northern wall with <a href="../characters/vazha.html">Vazha</a> and puts both hands over his face. When the clockmaker offers a working hand in exchange for the freedom to leave, he asks only whether it is sorcery, heresy or something a Hierarch must bless first, and accepts the answer that it is craft.</p>
          <p>In his last illness he tells Levan that he was never meant to need it, and that a boy who never needed to be extraordinary might have made a very dull king. He dies eight days later. That same night he has chosen between the two young men he raised, and has asked Vazha to see the choice honored quietly rather than announced, so that the kingdom might come to it freely. The sheet gives his age as the late fifties at death, with cropped grey hair, a trimmed grey beard, warm brown eyes and a dark chokha embroidered in muted silver.</p>""",
                "quote": "You were never meant to need it, and I find I am glad of that more than I am sorry for the rest of it.",
            },
            {
                "slug": "vazha", "name": "Vazha",
                "epithets": "Senior steward to King Guram &middot; leader of the loyalist faction &middot; outlives the war by nearly thirty years",
                "teaser": "Follows the soundest advice he ever heard, and spends the war learning which of loyalty's two creditors collects first.",
                "bio_html": """<p>Guram's senior steward, the one man in the palace who had known the King longer than the King had known his own crown, and who had carried both princes on his shoulders as infants. Against his better judgment he arranges the clockmaker's audience. When Guram dies he tells the court that no choice was left, a lie he carries for the rest of his life, because Guram's real choice had been made in confidence and he reasons that a crown installed by a father's whisper would always be one <a href="../characters/bagrat.html">Bagrat</a> could say was stolen. He never petitions the temple to enter <a href="../characters/levan.html">Levan</a>'s name on the succession rolls, which he later calls the single worst piece of good advice he ever followed.</p>
          <p>After <a href="../characters/demna.html">Demna</a>'s ruling he tells the court the truth and is believed by perhaps a third of the room. He leads the smaller faction through one winter and part of a spring, refuses three offers of surrender, the last of which asks only for Levan, and keeps a private ledger of a little under two thousand dead. He survives the war and the peace by nearly thirty years, and asks <a href="../characters/otar.html">Otar</a> exactly once whether the prince lived; he chooses to read the small, tired smile as a yes. The sheet draws him spare, upright and slightly stooped, with thin close-cropped white hair, a short white beard and a steward's seal; it also gives an age that cannot be squared with his surviving the war by nearly thirty years, so none is stated here.</p>""",
            },
            {
                "slug": "demna", "name": "Demna",
                "epithets": "Hierarch, senior priest of Auron's temple in Tavgora &middot; late 50s&ndash;60s on the sheet",
                "teaser": "Believes every word of a ruling he was paid to make, and cannot prove to himself that the gold is not the reason.",
                "bio_html": """<p>Senior priest of Auron's temple in Tavgora, who rules that the Doctrine of the Unbroken Hand bars a hand that claims the wholeness a sleeve would honestly confess it lacks. Three weeks earlier Bagrat's gold reached him by way of <a href="../characters/sandro.html">Sandro</a>, and he has never once, in his own prayers, managed to convince himself that the gold is the reason he believes what he is about to say. The night before the ruling he kneels alone at Auron's altar and tells the god that the gold changes nothing about the law's truth, only about how quickly he got around to remembering it; the distinction satisfies him there, and considerably less so in court the next morning. He is not struck down, which one faction treats as proof of nothing and the other as proof of everything.</p>
          <p>It is Demna who first says aloud, in <a href="../characters/bagrat.html">Bagrat</a>'s hearing, the sentence that gives the king's private ledger a public name: that a false wholeness worn long enough begins to believe itself real. By the war's second month he is unpaid, unasked, and at the wall, praying in the same words over a dying man from each faction in the same week. The sheet draws him stooped and war-worn, clean-shaven with cropped iron-grey hair, in threadbare iron-grey vestments and carrying no weapon.</p>""",
                "quote": "The Doctrine does not ask whether a hand functions. It asks whether a hand is the one Auron gave.",
            },
            {
                "slug": "observer-419-1153", "name": "Observer 419",
                "epithets": "Envoy/Observer, Case 1,153 &middot; publicly a clockmaker &middot; also the Observer of Case 2,140 &middot; outwardly 40s&ndash;50s",
                "teaser": "Grafts an eleven-fingered hand in three nights, leaves by dawn, and cannot quite stop watching for eighteen years.",
                "bio_html": """<p>The same field agent of the <a href="../lore/cultivator.html">Cultivators</a> who installs a single grey sphere in a county mill in <a href="../characters/observer-419.html">Case 2140</a>, posted next to Tavgora, where he has kept a stall in the lower market for thirteen weeks by the morning of the Proving: small brass instruments that run for years without a smell of oil. He watches the Proving from the back of the crowd and files his report that evening, recommending a Tier 1000-series functional intervention and flagging the prince's temperament as an unusually favorable variable. What he does not write down is that he felt <em>recognition</em>, the second posting running in which the feeling arrived before there were grounds for it.</p>
          <p>He asks the King for an audience, offers craft rather than sorcery, and asks only that no one keep him in Tavgora once the work is done. His one instruction to <a href="../characters/levan.html">Levan</a> is the only thing he ever says to him that anyone overhears. His posting formally ends the morning after the graft; he does not travel far. For eighteen years he watches from a rented room two valleys away, files a note on the ruling in which he finds himself, against every manual, <em>glad</em>, and on the night the city falls stands on the ridge above the western road and logs a column of twelve leaving by a goat track. He notes the lute, and files nothing about it. The sheet draws him in earth browns with grey-streaked brown hair, pale grey eyes and a short, neatly kept beard, deliberately unremarkable.</p>""",
                "quote": "This will not make you whole. It will make you capable. They are not the same, and you would do well to remember which one your doctrine actually asks for.",
            },
            {
                "slug": "the-eleven-fingered-hand", "name": "The Eleven-Fingered Hand",
                "epithets": "Catalyst, Case 1,153 &middot; a grafted prosthetic left hand &middot; two thumbs, eleven digits",
                "teaser": "Built by someone who had studied hands rather than grown one; a kingdom rounds it up to twelve fingers and down to abomination.",
                "bio_html": """<p>The prosthetic that replaces <a href="../characters/levan.html">Levan</a>'s ruined left hand, fitted by <a href="../characters/observer-419-1153.html">the clockmaker</a> over three nights: no blood after the first hour, no fever after the second night, and by the third morning a hand lying pale and still on the pillow, unmistakably wrong in the way a correctly drawn diagram of a hand is wrong when you have only ever seen the real thing. It has two thumbs set opposite each other along one broad palm, and beneath them two rows of ordinary fingers: four in the row that shows, and five more folded flat beneath it, hinged along a second knuckle no natural hand possesses, the way a fan holds nine-tenths of itself in reserve until a wrist decides otherwise. Nobody who handles it can say what it is made of.</p>
          <p>It sets compound fractures with a precision no natural hand could match, ties sutures too small for the physicians' own eyes to follow, and reaches into a wound at an angle no ordinary wrist could offer. Its hidden row unfolds fully for the first time in the six-hour surgery on <a href="../characters/bagrat.html">Bagrat</a>'s arm, and again in the duel, when all five hidden fingers close over the guard of his sword like a hand closing over a key it has always known. Legend then does what the file declines to: the lower market calls it the Twelvefold Hand, then gold cast at Solan's anvil that cannot be burned; the court chronicles call it a lie told in metal; and a small shrine in a lower valley keeps a gilded wooden hand with too many fingers on a shelf behind its altar. The sheet draws it pale matte ivory with muted iron-grey joints, in panels showing the folded second row, the joint mechanism and the opposed thumbs.</p>""",
            },
            {
                "slug": "the-doctrine-of-the-unbroken-hand", "name": "The Doctrine of the Unbroken Hand",
                "epithets": "Auron temple archive &middot; codified in the same century as the Proving, four centuries before the events",
                "teaser": "Precise about absence, silent about substitution, and a very old weapon looking for a hand to be used on.",
                "bio_html": """<p>An older and considerably colder text than the Proving that shares its theology, filed in the temple archive alongside two dozen other doctrines no living Hierarch had needed to cite: that a king's hand is the instrument of Auron's law made visible, and that no man missing the wholeness Auron gave him at birth can be trusted to hold that law without some essential piece of it also missing. It speaks of men who lack the god's gift and says nothing of men who have been given another, and it is in that silence that Vazha's allies and Bagrat's lawyers both make their camps. The form that turns it into procedure, the Writ of Examination, sits beside it in the same archive, and the paragraph beneath the summons fixes what a court of three is to do on a finding of counterfeit.</p>
          <p>Once it has been shown to be usable, it is used: against a nephew with a limp in the second reign, a daughter with a squint in the third, a prince with a withered foot in the fourth, until succession in Sarkveti is a contest of defect rather than claim, and the temple that charges a fee for each examination grows rich as the crown grows poor. The manuscript never says what it looks like; the sheet draws it as a bound codex of yellowed vellum with an iron-grey seal and a wood-and-iron clasp.</p>""",
            },
            {
                "slug": "sandro", "name": "Sandro",
                "epithets": "Gold-broker of Tavgora's court &middot; 40s&ndash;50s on the sheet",
                "teaser": "Carries the bribe to the Hierarch, and finds priests his easiest customers because they never haggle.",
                "bio_html": """<p>A broker who makes a modest living arranging exactly the kind of transaction between men too proud to negotiate their own convictions directly. He carries <a href="../characters/bagrat.html">Bagrat</a>'s gold to Hierarch <a href="../characters/demna.html">Demna</a>, and remarks, to no one in particular and entirely for his own amusement, that priests are his easiest customers precisely because they never haggle. The sheet draws him soft-built and comfortably prosperous, olive-skinned, with dark oiled hair thinning at the crown, quick dark eyes and a thin, carefully groomed mustache, in muted charcoal and umber with a coin-purse and a ledger.</p>""",
                "quote": "A man who believes his own argument will accept any price for saying it out loud, since he was always going to say it for free.",
            },
            {
                "slug": "otar", "name": "Otar",
                "epithets": "Border soldier, later informal leader of the faction that would not fight &middot; 50s&ndash;60s at the extraction on the sheet",
                "teaser": "Walks out of the surgery on a leg he was told to lose, visits it weekly for life, and then walks its owner out of the city.",
                "bio_html": """<p>A soldier who arrives at <a href="../characters/levan.html">Levan</a>'s surgery three years into his apprenticeship with a leg the border garrison's healer has recommended taking off at the knee, and leaves six weeks later without a stick, unable to stop telling anyone that the prince's hand had felt like eleven separate decisions being made at once, each one correct. He visits that surgery once a week for the rest of his life, whether or not he needs anything mended.</p>
          <p>When the war splits the city he gathers the third faction that has no banner: eleven men chosen for nothing a recruiter would recognize except that each carries a piece of work Levan's hands once did. On the night the outer wall falls he cannot bring himself to carry a surgeon off a table, so his men stand along the surgery wall and hold lamps for an hour while Levan finishes closing a wound on a boy in <a href="../characters/bagrat.html">Bagrat</a>'s colors. Then he makes his argument once, plainly, and takes Levan out by a goat track and eleven days of unwatched mountain paths to a place he will not name. The sheet draws him broad-shouldered in youth, leaner and weathered after two decades, iron-grey and short-bearded, with a faint permanent limp in the leg Levan saved and a worn dark belt-knife.</p>""",
                "quote": "A secret held by one man dies with him, and I intend for this one to outlive me.",
            },
            {
                "slug": "eka", "name": "Eka",
                "epithets": "Bonesetter's daughter &middot; physician of Tavgora &middot; early-to-mid 30s on the sheet",
                "teaser": "Asks every man carried through her door how badly he is hurt, and never which banner he fought under.",
                "bio_html": """<p>A bonesetter's daughter who spends a month watching <a href="../characters/levan.html">Levan</a>'s surgery from the doorway before asking whether she might hold the instruments, and is told she may, provided she puts them back in order. She trains with him for the better part of a decade and becomes the nearest thing Tavgora has to a second such hand: one of the two physicians at <a href="../characters/bagrat.html">Bagrat</a>'s six-hour surgery, who stop trying to follow what Levan is doing in the fourth hour and simply hand him whatever he silently reaches for. During the siege she keeps her own surgery open and asks exactly one question of every man carried in. The hardest hour of the war, she will say decades later, is the morning she treats two men from the same street who put those wounds on each other, side by side, each asking whether the other will live. Levan hands her the one-eyed grey cat before he leaves. Her craft survives one generation of apprentices, and not a second.</p>
          <p>The text gives her no physical description beyond being a young woman and a skilled physician; her sheet says everything else on it, a sturdy, dark-haired, dark-eyed figure in a bloodstained apron with chapped, over-washed hands, is invented for consistency.</p>""",
            },
            {
                "slug": "sulqan", "name": "Sulqan",
                "epithets": "Healer attached to Sarkveti's border garrison &middot; 48 on the sheet",
                "teaser": "A decent, exhausted man who has already begun preparing a household to lose its king-to-be.",
                "bio_html": """<p>The border garrison's own healer, a decent and exhausted man, who sees <a href="../characters/bagrat.html">Bagrat</a> carried to Tavgora's gates fevered past recognizing his own name, his sword arm swollen black to the elbow, and has already begun preparing the household for losing him. <a href="../characters/levan.html">Levan</a>'s six-hour surgery makes that preparation unnecessary. The sheet makes him forty-eight, stocky and built for lifting wounded men rather than fighting, with thinning grey-brown hair, an unkempt greying beard, a ruddy complexion from years at a cold border post, ink- and herb-stained hands and a patched off-white coat. It shows him treating the arm on the return march, then preparing the household for the loss.</p>""",
            },
            {
                "slug": "dato", "name": "Dato",
                "epithets": "Levied farmhand &middot; common soldier &middot; 17 years old",
                "teaser": "Carries a king home before anyone has settled on calling him one, and is never named in a chronicle.",
                "bio_html": """<p>A levied farmhand of seventeen, among the common soldiers who carry <a href="../characters/bagrat.html">Bagrat</a>'s litter for eight days, who is entirely unaware until he sets his commander down in the palace courtyard that his own trembling relief at finally reaching help looks, to the assembled court, exactly like grief. He is never named in any chronicle, and spends the rest of a long, ordinary life telling his grandchildren, with more pride than the moment probably warranted, that he once helped carry a king home. The sheet draws him lanky and wiry, with rough-cut sandy-brown hair, light brown eyes and the callused hands of farm work.</p>""",
            },
            {
                "slug": "gia", "name": "Gia",
                "epithets": "Conscripted household-guard soldier &middot; 19&ndash;20 on the sheet",
                "teaser": "Meets a man he last saw wincing through the same stitches, and later tells the night a breath kinder than it was.",
                "bio_html": """<p>A young man conscripted off his family's terrace two seasons earlier and given a spear he barely knows how to hold and a banner he has stopped believing in; he holds the eastern breach with <a href="../characters/bagrat.html">Bagrat</a>'s household guard on the night the outer wall gives way. <a href="../characters/levan.html">Levan</a>'s hands had set his broken wrist two winters before, after a training accident neither he nor the man he now faces, <a href="../characters/beso.html">Beso</a>, thought worth mentioning. They recognize each other in the half-second before contact, and neither lowers his weapon. Gia takes nothing worse than a fall that knocks the wind from him; in his old age he will tell a version in which he recognized Beso a full breath sooner and let the blow go wide on purpose, a small, forgivable improvement on the truth that even he can no longer separate from what happened in the dark. The sheet draws him slight and still growing, with short black hair, wide dark-brown eyes and a faint scar on one wrist, in borrowed, ill-fitting armor.</p>""",
            },
            {
                "slug": "beso", "name": "Beso",
                "epithets": "Soldier for Vazha's loyalist faction &middot; about 22&ndash;23 on the sheet",
                "teaser": "Carries a white scar in the shape of a story he will never tell without crediting whose hands began it.",
                "bio_html": """<p>A loyalist who walked with a stick for the better part of a year after a border skirmish, until <a href="../characters/levan.html">Levan</a>'s hands rebuilt the tendon a border healer had written off. At the eastern breach on the night the outer wall falls he comes at the line from the other direction and recognizes <a href="../characters/gia.html">Gia</a>, three years his junior, in the half-second before contact. He takes a shallow cut along the forearm that scars white for the rest of his life, in a shape he never shows anyone without also explaining, unprompted, exactly whose hand had put the first version of that arm back together. The sheet draws him tall and fully grown, with dark brown hair tied back, sharp brown eyes, a short patchy young beard and a long pale scar on one forearm; it notes that everything beyond his age relation and the lifelong scar is reconstruction.</p>""",
            },
            {
                "slug": "amets", "name": "Amets",
                "epithets": "Keeper of the Vigil of Ardwen, in Otsane &middot; 50s&ndash;60s on the sheet",
                "teaser": "Gives a stranger a plain name, an open door, and a household that has never heard of anyone called Levan.",
                "bio_html": """<p>The Keeper of the <a href="../lore/faith-of-ardwen.html">Vigil of Ardwen</a> in Otsane, a small theocracy tucked into a fold of the western range so thoroughly unremarkable that Sarkveti's maps render it as an unlabeled patch of grey. She sits in a plain wooden chair in a Vigil house with no cathedral and no gold, because Ardwen's doctrine asks for empty hands before anything else, and she receives the stranger Otar's men deliver to her gate with a silence that is unhurried in a way nothing in Tavgora's court ever managed. Before the week is out she gives him a name for the register that is not his own, <em>Mikel</em>, and a standing instruction to her household, kept without a single question, that no man called <a href="../characters/levan.html">Levan</a> has ever come to that gate. A gate-warden who dislikes lying so much that she practices it exactly once in her life tells the one rider who does reach Otsane that no man of that name ever came there. The sheet draws her as a small-framed, wind-browned Basque-coded mountain woman, grey hair beneath a plain wool kerchief, in undyed wool and calf-laced abarkas.</p>""",
                "quote": "Ardwen does not ask what your hands have done. Only that you keep them open now.",
            },
            {
                "slug": "xu-lian", "name": "Xu Lian",
                "epithets": "Foreign scholar &middot; Jinhai &middot; also in Case 0000B &middot; age not established",
                "teaser": "Leaves eleven notebooks at a cathedral that give a faraway rumor its theological shape.",
                "bio_html": """<p>A careful foreign scholar who spends two years cataloguing every recorded attempt on <a href="../characters/valeria.html">Valeria</a> before returning, empty-handed and unbitter, to a country half a world away. The eleven notebooks he leaves behind are donated to the Vigil and are what give the news from Sarkveti its theological shape at Ardenwake: among his annotations sits <a href="../characters/anchorite-of-ardenwake.html">an anchorite</a> walled into a cell against the cathedral's north face, who crossed a hall full of soldiers who had just failed to move the sword and lifted it without once thinking about succeeding, failing or the blade. He is also the foreign scholar of Case 0000B, where he appears beside <a href="../characters/the-anchorite.html">the Anchorite</a> herself. The sheet draws him East Asian-coded and restrained, with dark hair, dark eyes, ink-stained hands and a satchel of weathered bindings, and files him under Jinhai; it says his appearance follows earlier canon and adds nothing new.</p>""",
            },
            {
                "slug": "anchorite-of-ardenwake", "name": "Anchorite of Ardenwake",
                "epithets": "Anchorite of the Vigil of Ardwen &middot; the protagonist of Case 0000B &middot; cited here secondhand",
                "teaser": "A woman who wanted enclosure rather than glory, cited at a distance as one of two precedents for a third lifter of the sword.",
                "bio_html": """<p>In this case the Anchorite of <a href="../characters/the-anchorite.html">Case 0000B</a> appears only as a precedent, through <a href="../characters/xu-lian.html">Xu Lian</a>'s donated notebooks: a woman walled into a cell against the cathedral's north face who lifted <a href="../characters/valeria.html">Valeria</a> without once, by her own account, thinking about the blade. With <a href="../characters/the-founding-wielder.html">the founding wielder</a>, she is one half of the pattern Ardenwake's pilgrims and younger clerks try to extend to a healer who refused a throne twice, in a kingdom that answered the refusal with a writ of fire. The Vigil's scholars complicate the enthusiasm before it settles into doctrine, and the Keeper of Ardenwake declines to settle it from a plinth hall a mountain range away. The sheet adds no new physical detail and sends the reader back to Case 0000B for her appearance, drawing her hooded in stone-grey and parchment with a plain devotional cord and Xu Lian's notebooks in her hands.</p>""",
            },
            {
                "slug": "the-founding-wielder", "name": "The Founding Wielder",
                "epithets": "The valley reckoner &middot; the boy of Case 0000 &middot; permanently unnamed &middot; cited here secondhand",
                "teaser": "The nameless first bearer of the sword, whose namelessness has grown a superstition the Vigil's scholars cannot quite examine.",
                "bio_html": """<p>The first bearer of <a href="../characters/valeria.html">Valeria</a>, cited at Ardenwake as a nameless valley reckoner: <a href="../characters/the-boy.html">the boy of Case 0000</a>, who is never given a name that survives the telling. His namelessness has given rise to the order's oldest and least examined superstition, that renouncing one's name is itself part of the mechanism, which the Vigil's scholars use to argue that <a href="../characters/levan.html">Levan</a>, known across three kingdoms by a story harder to renounce than a crown, is the furthest thing from the pattern. The sheet adds no new physical detail, treats his appearance as canonically inherited from Case 0000, and draws him pale-haired in layered, weathered cloth, shown in the margin of the Vigil scholars' debate.</p>""",
            },
        ],
        "scenes": [
            {"slug": "the-proving-strap-gives",
             "alt": "A dark-haired youth in black and gold robes recoils with a bloodied open left hand and a blade in his right while a lighter-haired youth in pale robes lunges to catch him, his own sword falling with a leather strap trailing, courtiers watching from a stone stair beneath a mountain citadel",
             "caption_html": """The Proving: a strap that was re-buckled twice gives way, and four inches of real steel come down across <a href="../characters/levan.html">Levan</a>'s raised left hand. It is <a href="../characters/bagrat.html">Bagrat</a>, not Levan, who screams, dropping his own blade to catch his cousin before he falls."""},
            {"slug": "the-king-on-the-northern-wall",
             "alt": "A crowned old man in a fur-trimmed cloak covers his face with both hands at a battlement above a snowy valley while a grey-bearded man in a dark cloak stands behind him",
             "caption_html": """<a href="../characters/guram.html">Guram</a> takes the surgeons' news standing and dry-eyed, and then, on the northern wall with <a href="../characters/vazha.html">Vazha</a> and no one else, puts both hands over his face and makes a sound Vazha will never repeat."""},
            {"slug": "the-clockmaker-at-his-stall",
             "alt": "A man with grey-streaked brown hair and a short beard in a hooded brown cloak and leather apron works on a small brass mechanism at a market stall hung with gold pocket watches, a hilltop citadel and a crowded market behind him",
             "caption_html": """<a href="../characters/observer-419-1153.html">The clockmaker</a>'s stall in Tavgora's lower market: small brass instruments that run for years without a smell of oil, sold to a court that mostly tells time by bells. He has kept it for thirteen weeks by the morning of the Proving."""},
            {"slug": "the-graft-over-three-nights",
             "alt": "By candlelight a bearded man in a hooded brown cloak fits a jointed golden-brown mechanical hand to the arm of a sleeping dark-haired youth in a bed, two robed men watching from behind",
             "caption_html": """Over three nights <a href="../characters/observer-419-1153.html">the clockmaker</a> works on <a href="../characters/levan.html">Levan</a>'s ruined hand while the two physicians present, sworn to silence, keep that oath more faithfully than any other they swear. No blood after the first hour, no fever after the second night: by the third morning, <a href="../characters/the-eleven-fingered-hand.html">a hand</a> lying pale and still on the pillow, too regular, too considered."""},
            {"slug": "levan-counts-his-fingers",
             "alt": "A dark-haired young man propped in a bed beside a sunlit window holds up a pale jointed prosthetic left hand, a mountain and a citadel beyond the glass",
             "caption_html": """<a href="../characters/levan.html">Levan</a> wakes to eleven fingers, and counts them himself before any physician or the clockmaker can: two thumbs set opposite each other along one broad palm, four fingers in the row he can see, five more folded flat beneath it. His first thought is neither horror nor gratitude, but a small, shameful, private satisfaction at finding he can still count at all."""},
            {"slug": "demna-before-the-ruling",
             "alt": "A grey-haired priest in a heavy iron-grey robe kneels at a stone altar with clasped hands and an oil lamp, looking up at a dark temple door carved with a sword and a pair of balanced scales",
             "caption_html": """<a href="../characters/demna.html">Demna</a>, alone before Auron's altar the night before the ruling, telling the god that the gold changes nothing about the law's own truth, only about how quickly he got around to remembering it &mdash; a distinction he finds entirely satisfying there, and considerably less so in court the next morning."""},
            {"slug": "the-vashtir-snow",
             "alt": "A wounded man in a frost-covered fur coat lies in the snow with an arrow in his side beside a rearing white horse, mounted archers with torches closing in through a night snowstorm",
             "caption_html": """The northern answer to the Vashtir raids, led by <a href="../characters/bagrat.html">Bagrat</a> because a kingdom that cannot agree on its king can still agree on who should be sent to freeze on its behalf: a Vashtir arrow taken low and wrong in the dark, a fall from a startled horse onto rock, and eight days on a litter to come."""},
            {"slug": "the-king-in-the-corridor",
             "alt": "A crowned young king in an ermine-trimmed crimson cloak kneels on a stone floor in a narrow dark corridor with both hands pressed over his face",
             "caption_html": """<a href="../characters/bagrat.html">Bagrat</a> behind the hall's northern pillar after the duel: his knees strike stone before he decides to kneel, both ordinary hands pressed flat over a face no one but the corridor's cold walls will see uncomposed. He straightens his collar before he walks back out."""},
            {"slug": "the-outer-wall-falls",
             "alt": "A walled hill city of white terraces burns at night while siege engines hurl flaming stones at a breaking wall under red and blue banners",
             "caption_html": """Tavgora's outer wall goes to <a href="../characters/bagrat.html">Bagrat</a>'s siege engines after <a href="../characters/vazha.html">Vazha</a>'s faction has refused three separate offers of surrender. The engines are brought up on the nineteenth day of Lorren, and Bagrat does not go to watch them."""},
            {"slug": "the-eastern-breach",
             "alt": "Two young soldiers face each other across crossed swords among rubble at night, one in red household-guard colors and one in blue with a heraldic beast, torchlit ranks behind them",
             "caption_html": """The night the outer wall gives way, at the eastern breach: <a href="../characters/gia.html">Gia</a> of Bagrat's household guard and <a href="../characters/beso.html">Beso</a> of Vazha's loyalists recognize each other in the half-second before contact, two former patients of the same eleven fingers, and neither lowers his weapon."""},
            {"slug": "the-keeper-meets-the-stranger",
             "alt": "A bearded dark-haired man in a heavy cloak stands at a stone gate facing a grey-haired woman in a hooded wool robe, a plain timber Vigil house and grazing sheep behind her",
             "caption_html": """<a href="../characters/amets.html">Keeper Amets</a> receives the stranger Otar's men have delivered to her gate in Otsane, and tells <a href="../characters/levan.html">Levan</a>, before he has said a word about any of it, that Ardwen does not ask what his hands have done, only that he keep them open now."""},
            {"slug": "levan-at-the-workbench-in-otsane",
             "alt": "A grey-bearded man in a leather apron sits at a candlelit workbench with both hands laid flat on the wood, one of them a pale jointed prosthetic, a mountain lute leaning against the shelves beside him and a mountain through the window",
             "caption_html": """<a href="../characters/levan.html">Levan</a>, called Mikel, at his workbench in Otsane on the evening a trader tells him how it ended: both hands, the four ordinary fingers and the five hidden ones alike, laid flat and motionless on the wood. He plays the lute again that night, later than his habit."""},
            {"slug": "one-attempt-on-valeria",
             "alt": "A robed figure kneels on cathedral steps reaching toward a glowing sword on a plinth in a shaft of light, robed onlookers lining a stained-glass hall",
             "caption_html": """The plinth hall at Ardenwake, where every pilgrim who climbs the cathedral steps is permitted exactly one attempt on <a href="../characters/valeria.html">Valeria</a> and almost none ever lift it: the ritual the Vigil's scholars call the Empty Hand. This record names no one."""},
        ],
    },
    {
        "slug": "1268", "title": "Independent Observation",
        "status": ["coming-soon"],
        "cover_file": "1268.jpg",
        "hook": "Altitude. Round. Audit. Dormant. Unhastening.",
        "case_tag": "Case 1268",
        "catalyst": {
            "name": "The Probe Network",
            "meta": "Distributed autonomous celestial probe network",
            "page": "characters/the-probe-network.html",
            "img": "characters/the-probe-network-thumb.jpg",
            "html": "<p>A field of dormant autonomous probes seeded into Aldemark's high air generations before the first dream, which on a schedule fixed before the seeding lends one village at a time a seat in the dark above its own world. It supplies no voice, no doctrine and no instruction, only altitude. Ten villages take the offer in turn, eleven days apiece and eleven months apart; the eleventh selection is the capital itself.</p>",
        },
        "envoy": {
            "name": "Cultivator Observer",
            "meta": "Custodian-Office analytical authority &middot; no Envoy posted in person",
            "page": "characters/cultivator-observer.html",
            "img": "characters/cultivator-observer-thumb.jpg",
            "html": "<p>No Envoy is posted to this case, and none delivers or observes in person. The Custodian Office's analytical authority, drawn on the sheet as an alien Cultivator, watches the probes' telemetry from beyond the reach of any native chronicle and speaks, in the closing log, as <em>this office</em>: terrarium stable, case closed, filed.</p>",
        },
        "pages": EDITOR_PAGES,
        "genre": EDITOR_GENRE,
        "synopsis_html": EDITOR_SYNOPSIS,
        "characters": [
            {
                "slug": "hraban", "name": "Warden Hraban",
                "epithets": "Mid-ranking Warden of the Threefold Crown, sent from Ansdorf to Halstead &middot; seventeen years' service by his file, twenty-six by the Custodian log &middot; resigns after the eleventh selection &middot; lives thirteen more years",
                "teaser": "Asks for guidance before he asks for punishment, watches a farmhand walk into a fire, and spends eleven months noticing that the man was right.",
                "bio_html": """<p>A careful man, neither cruel by temperament nor merciful by conviction, sent from the district seat at Ansdorf on the twentieth day of the Halstead dreaming to look into a report of collective delusion. He travels with a brindled hound, Bero, inherited as a pup from a dead brother and already, at three winters old, inclined to sulk in the rain; he warms the dog's blanket against the hearth-stones before he thinks to warm anything for himself, and lets Bero's chin rest on the toe of his left boot through every report he drafts. He questions <a href="../characters/ymma.html">Ymma</a> first, a boy next and <a href="../characters/otker.html">Otker</a> last and longest, and does not believe Otker is lying, which the manuscript calls the beginning of the tragedy. He writes to Ansdorf describing a probable contagion of the mind and asks for guidance before punishment. The answer, sealed with the joined sigil of all three Triarchs, ignores the contagion: forty people have reached the same conclusion with no teacher at all.</p>
          <p>He stands at the edge of the burning on the last day of Brayen and watches Otker go into it without recanting, and it is eleven months before he lets himself notice that the last thing Otker said to him was still true. Recalled to Dornhal the spring before the eleventh selection, on a seventeen-year record his file has never corrected, he is the one the dream breaks first and most completely: three attendants find him on the floor of his chamber before sunrise, his hands pressed so hard to his face that his nails leave marks for a week, repeating a single word one of them thinks sounded like a name. Old Bero has dragged himself across the room on bad hips to lie along his ribs. He resigns within the year, finds <a href="../characters/anchorite-of-ardwen.html">the Anchorite</a> at a crossroads shrine and asks whether Ardwen wanted any of it, and lives thirteen more years in a small house with no shrine, a row of beans that comes to nothing every spring and a succession of old hounds each named for the first. He goes back to Halstead once, in the eleventh of those years, and when a woman selling eggs asks whether it is true that a farmhand named Otker died insisting the world was round, he says &ldquo;Yes.&rdquo; and nothing more. He is buried, at his own written request, without the Crown's rites.</p>
          <p>The Custodian log counts twenty-six years of sanctioned orders, each preceded by a request for clarification, and records the habit as present in exactly one subject and without measurable effect on the outcome. The sheet draws him average-to-tall and lean, with brown greying hair, a short greying beard and grey-green eyes, in a grey-brown Warden's coat with the Dornhal insignia, a service sword and a dagger, and then in a plain grey civilian coat after his resignation, with nail marks on his hand from the breakdown. The pull-quote below is the sheet's own and does not appear in the manuscript.</p>""",
                "quote": "&hellip;Before I act, I must be sure. Not out of doubt, but out of duty.",
            },
            {
                "slug": "anchorite-of-ardwen", "name": "The Anchorite of Ardwen",
                "epithets": "Ardwenist anchorite of the western border &middot; unnamed &middot; later called the Anchorite of the Nine Burnings, a title she never claims",
                "teaser": "Kneels in the ash of nine burnings, asks the sky to let her come, and is given more altitude than anyone in Aldemark's history.",
                "bio_html": """<p>A woman in undyed grey wool, alone and on foot, who kneels in the ashes of Halstead for the better part of an afternoon without asking a single neighboring farm what happened there, and leaves behind two knee-shaped hollows that the next rain erases. She is present at every one of the nine burnings, and at the one village that is never purged: already in Ansdorf on the ninth day of its dreaming, where a junior Warden interviews her and files the result unread; before Grenmoor's shrine to the Star-Walkers, telling no one which god she thinks the singing was for; in Harkendale's root cellars, warned more than once to move on; at Faldrun, where she blesses a blacksmith's iron globe in Ardwen's name; and at Aschendale's boundary stone, where no purge is ever ordered, praying that night for the elders who chose a hard truth over an easy lie. Taken at Reinfeld on charges of vagrancy and obstruction, she asks the soldier who binds her wrists whether he was at Halstead. In Dornhal she answers every question an Inquisitor puts to her and tells him nothing: asked who sent her, &ldquo;Ardwen&rdquo;; asked her name, on the eleventh day, &ldquo;my name is not the thing you are asking for.&rdquo; She is not tortured, though not from mercy: three Ardwenist communities have begun writing to Dornhal on her behalf.</p>
          <p>In a cell too narrow to lie down in, she kneels toward the one barred slit and asks, not for rescue or vindication, only: <em>if You are beyond the heavens, then let me come.</em> The <a href="../characters/the-probe-network.html">network</a> above Aldemark does not recognize a prayer; it recognizes an interaction request from an already-registered dreaming subject, and does what it was built to do. She rises past the globe, the furnace of the sun, a wheel of fire and a river of suns so numerous that Aldemark does not amount to a grain of silt in it, to a dormant figure with straight black hair, a white too fine to name and red unblinking eyes, something nearer to a status than a presence: <em>Dormant. No active deployment. Awaiting reassignment.</em> Two names surface that she has sung in the Houses of Vigil since before she could read, the Sky-Answerer and the Unhastening. She asks whether it called her. It does not answer, and she takes the silence as an answer. The manuscript names no other case, but its echoes (a sword's name, a valley watched through one boy's lifetime, those same two titles) point toward <a href="../characters/ardwen.html">Ardwen</a> of Case 0000, and the Custodian log says the designation recurs, under seal, in at least six earlier case files.</p>
          <p>On the night of the eleventh selection she reaches for it again and finds nothing, and what she feels instead is the plain gratitude of a beggar let back into a hall; it turns her, for the first time, inward, to the sleeping body in the cell. Within the year <a href="../characters/hraban.html">Hraban</a> finds her at a crossroads shrine and asks whether she dreamed what the city dreamed; she says, &ldquo;I dreamed something. It was not the same thing.&rdquo; Released some months after the collapse, she goes back to the road, hears the stories about her outrun her within two years, every detail they settle on wrong in some particular, and dies decades later still giving the same answer to a question she has been asked several thousand times. The manuscript never gives her a name or an age. The sheet draws her lean and road-hardened, medium height, with dark brown hair under a plain grey head-covering, grey-green eyes, a small unsettling smile, a walking staff, a journey pouch and worn boots.</p>""",
                "quote": "Ardwen does not want. Ardwen answers. There is a difference, and it is the only theology I have ever needed.",
            },
            {
                "slug": "otker", "name": "Otker",
                "epithets": "Farmhand of Halstead &middot; saving barley-money for a daughter's loom &middot; burned in the purge of Halstead, unrecanting &middot; twenties by his sheet",
                "teaser": "Sits up three nights with a neighbor's cow, reports the shape of the world the way a man reports weather, and will not take it back.",
                "bio_html": """<p>A slow, well-liked farmhand of Halstead who has spent the winter sitting up three nights with a neighbor's failing cow and two seasons of barley-money on a loom for a daughter not yet old enough to weave. By the third week of the dreaming he is the one who reports that if a man goes far enough from the world in his sleep, it stops looking like a floor and starts looking like a stone: round on every side, hanging in the dark with nothing beneath it and nothing propping it up. He is not believed; then he is believed by four people; then by forty. Halstead means the news as an offering, something wonderful to lay at the temple door, and does not yet understand that the temple wants the lie kept whole.</p>
          <p><a href="../characters/hraban.html">Hraban</a> questions him last and longest, and Otker tells him plainly, the way a man reports weather, that he has seen the shape of the world and would swear to it on his own burial. He goes into the fire on the last day of Brayen without recanting; the Custodians log forty-one dead at Halstead. Years later, at a crossroads, a woman selling eggs asks a former Warden whether it is true that a farmhand named Otker died insisting the world was round, and Hraban answers that it is. The manuscript gives Otker no age; the sheet draws him in his twenties, lean and strong, of average height, with rough-cut brown hair, blue-grey eyes and light stubble, in a linen shirt, a worn leather vest and muddy boots, with a farm knife, and labels his expressions wary, plain-spoken, defiant and resigned.</p>""",
                "quote": "I have seen the shape of the world, Warden. It is round. I would swear it on my own burial.",
            },
            {
                "slug": "adaltrude", "name": "Adaltrude",
                "epithets": "Triarch of the Threefold Crown &middot; holder of Elara's seat &middot; overseer of hearth-law and harvest-blessing &middot; late middle age by her sheet",
                "teaser": "Argues against the purges, is outvoted two to one, and wakes from the eleventh dream to do the arithmetic she has spent nine years refusing to add.",
                "bio_html": """<p>Holder of <a href="../characters/elara.html">Elara</a>'s seat on the Crown, twenty-six years into overseeing hearth-law, harvest-blessing and the quieter, less glamorous work of actually feeding a kingdom when the villages begin to refuse the tithe. In closed convocation she argues that a people cannot be starved into believing a lie they have personally watched be disproven, and that continued purges will produce exactly the outcome they are meant to prevent. <a href="../characters/ansovald.html">Ansovald</a> and <a href="../characters/sigward.html">Sigward</a> outvote her two to one; the vote goes into no public ledger, and the famine that follows the next winter's grain shortfall does. The younger clergy who later ask, in careful language, whether a Crown that was wrong about the heavens can be trusted about anything it never troubled to reexamine are using the language she has modeled for them without ever quite instructing them to.</p>
          <p>In the eleventh dream, at twenty-eight years in Elara's service, she rises as every dreamer before her has risen, expecting to feel accused and not: the globe does not know her office and the moon does not care what she has signed. What she takes from it is that the horror was never that Auron's account of creation was wrong but that the heavens do not care whether his priests got a word of it right. She wakes before dawn, goes alone to the small hearth-shrine she keeps for Elara's private rites and kneels there for most of an hour, not praying but sitting the way a woman sits with a debt she has just understood she cannot repay. She says only that she saw what the dead of nine villages saw, that it was as they described, and that a decade of burnings purchased nothing except the burnings; the manuscript calls it arithmetic, not confession. When the Crown splits three ways she counsels confession and reform, and Elara's seat, under her and her successors, absorbs most of what remains of the temple's civil authority. Among those successors, for six further generations, it is a quiet, unwritten custom to review, before confirming any sentence of exile or execution, whether the accused had asked a question the court found it easier to punish than to answer.</p>
          <p>The sheet draws her in late middle age, of medium height and sturdy build, with a broad, serious face, dark brown hair with early grey braided and pinned with gold, dark hazel eyes and a fair to light-olive complexion, in layered blue-and-ivory Crown vestments with a grey fur mantle over practical winter wool, carrying a ceremonial seal, keys and legal tablets; one study shows her contemplative after the dream. The sheet calls the blue &ldquo;Elara's traditional colors&rdquo; while Elara's own sheet is red and cream, and both are given here as drawn. The pull-quote below is the sheet's own and does not appear in the manuscript.</p>""",
                "quote": "Law keeps the flame. Blessing gives it life. Both must endure.",
            },
            {
                "slug": "ansovald", "name": "Ansovald",
                "epithets": "Triarch of the Threefold Crown &middot; holder of Auron's seat &middot; defender of the Bound Creation &middot; older adult by his sheet",
                "teaser": "Never loses a doctrinal contest in nineteen years, knows independent observation is the one heresy scripture cannot answer, and has never climbed his own bell-tower.",
                "bio_html": """<p>Holder of Auron's seat on the Crown, who has governed the defense of the Bound Creation for nineteen years without once losing a doctrinal contest, and who conducts all his business on the palace's ground floor: a childhood fall from a granary beam has left him with a vertigo that he describes to visitors as a preference for the ground and to no one as a fear. He has never climbed the bell-tower of the cathedral he consecrated. He reads <a href="../characters/hraban.html">Hraban</a>'s letter from Halstead twice and is recorded as saying only that independent observation is the one heresy scripture has no answer for. His sermon that autumn on the folly of trusting one's own eyes does not name Halstead; Ansdorf is purged with far less debate beforehand, since he has concluded that debate is itself a contagion; and he calls the tax refusals a second heresy and orders both suppressed with equal severity.</p>
          <p>He dreams with the rest of Dornhal and says nothing publicly for three days: a burned draft of an address, meals sent up untouched, a man failing to hold in one hand the fact that he has seen the world is round and in the other the fact that he personally ordered a thousand people killed for saying so first. On the second night he, who has not climbed above the palace's first landing since boyhood, asks to be helped up to the roof and stands for most of an hour at the parapet with both hands flat on the stone, looking not at the stars but at the courtyard cobbles forty feet below, and comes down without a word. When he finally speaks, it is to say that the Crown could survive being wrong about the heavens if it did not also become known for having always known it, which the manuscript calls the single most honest sentence he has uttered in twenty-eight years, and which satisfies no one.</p>
          <p>The sheet draws him tall and spare, about six foot one, with a narrow, severe face, guarded grey eyes, dark hair silvered at the temples and a closely trimmed grey beard, in black-and-cream Triarch vestments with the Auronic star, holding scripture and decree tablets; its expression studies run from composed to private grief. It gives nineteen years governing the defense and twenty-eight of clerical career, which match the manuscript's figures.</p>""",
                "quote": "Independent observation is the one heresy scripture has no answer for.",
            },
            {
                "slug": "sigward", "name": "Sigward",
                "epithets": "Triarch of the Threefold Crown &middot; holder of Solan's seat &middot; signs the Reinfeld purge himself &middot; middle-aged to older adult by his sheet",
                "teaser": "Is shown the truth, believes it, and concludes the kingdom cannot survive hearing it spoken, so he orders the burning twice as hard.",
                "bio_html": """<p>Holder of <a href="../characters/solan.html">Solan</a>'s seat on the Crown, from a family that has served it for four generations, and the Triarch who argues through the decade of purges, with the particular ferocity of a young man defending an old institution, that strength is the only answer the dreaming deserves. He signs the order for Reinfeld's purge himself rather than delegate it, having made it a point of pride never to ask a Warden to carry out a purge he is not willing to have his own name on. His provincial appointees later form the Unbent, who conduct purges the Triarchs never sanctioned and are only nominally interested in being told to stop.</p>
          <p>His father raised him on one lesson: that the Crown is a roof, not a truth, and a roof's worth is measured by how long it keeps the rain out; his grandfather died holding a stretch of wall in the Bulwark famine rather than let a granary riot become a civil war. The eleventh dream tests the lesson, and it survives. Admitting the Crown's cosmology is a lie, he concludes, would not correct the kingdom his grandfather died for; it would kill it. He never doubts for a moment that the globe is real, and he spends the following week arguing, with a sincerity his colleagues mistake for zealotry and the manuscript calls nearer to grief, that the answer to being personally shown the truth is to burn twice as hard against it, and demands a purge broader and more absolute than any before.</p>
          <p>The manuscript calls him a young man defending an old institution; the sheet's trait list says middle-aged to older adult, though its caption for him reads &ldquo;a younger man in the service of an old institution.&rdquo; Both are left as they stand. The sheet draws him tall and athletic, with an angular face and a hard jaw, green-grey eyes, a short dark beard and dark hair greying early at the temples, in ivory-and-crimson vestments with flame motifs, a ceremonial sword and a formal dagger. The pull-quote below is the sheet's own and does not appear in the manuscript.</p>""",
                "quote": "Strength is the answer to the dreaming.",
            },
            {
                "slug": "ymma", "name": "Ymma",
                "epithets": "Woman of Halstead &middot; among the first known dreamers &middot; young-to-middle adult by her sheet",
                "teaser": "Wakes her husband before dawn to say she has been nowhere and everywhere, and starts the chain of testimony Halstead cannot unsay.",
                "bio_html": """<p>A woman of Halstead and the first dreamer the manuscript names. On the first night of Brayen, in the iron cold of early spring that Aldemark's peasants call Elara's Fast, she wakes her husband before dawn to tell him she has been nowhere and everywhere, floating in a black field scattered with unfamiliar lights, and that she went toward the moon simply by wishing to, the way a thought goes toward a memory. Her husband tells her it is only hunger dreaming. Three farms over, a boy tells his mother the same thing, unprompted, before she has said a word about it; by the second week no one in Halstead is calling it hunger. <a href="../characters/hraban.html">Hraban</a> questions her first when he arrives on the twentieth day.</p>
          <p>The manuscript names her only at the start and again when Hraban questions her, and does not say what becomes of her in the burning of Halstead. The sheet draws her as a young-to-middle adult of average height and sturdy rural build, with an open, tired, wind-reddened face, hazel eyes and dark brown hair in two braids under a linen headscarf, in a dark plaid muted-blue wool shawl over a brown wool dress and a linen apron; its notes call her married, an early riser of practical demeanor, and one of the phenomenon's first witnesses, and one panel shows her floating toward a full moon.</p>""",
            },
            {
                "slug": "the-probe-network", "name": "The Probe Network",
                "epithets": "Catalyst, Case 1,268 &middot; distributed autonomous celestial probe network &middot; seeded generations before the first dream &middot; no face",
                "teaser": "Dormant for generations, then, on a schedule fixed before it was seeded, lends one village at a time a seat in the dark above its own world, and gives nothing else.",
                "bio_html": """<p>A network of autonomous probes seeded silently into Aldemark's high atmosphere generations before any living Warden's grandfather was born, so completely dormant that no chronicle recorded a light in the wrong part of the sky until a schedule fixed before the seeding itself began to turn. It grants the sleeping minds of one village at a time an unmediated seat above their own world, with no voice, no vision of a god and no instruction: only altitude, and as much more of it as a dreamer has the nerve to keep asking for. It picks settlements by geographically stratified sampling of the whole inhabited landmass, with no weight for politics, religion or importance; eleven days of visitation, eleven months of silence, one settlement at a time. Eleven, the Custodian log explains, was never a sacred number, only the smallest count of independent exposure samples its statisticians judged enough to tell a pattern from ten coincidences. The Crown's temples build a numerology on it anyway.</p>
          <p>Ten selections are villages: Halstead, Ansdorf, Grenmoor, Wulfsholt, Faldrun, Brandwick, Harkendale, Stonewick, Aschendale and Reinfeld. The eleventh, fixed before the first probe reached Halstead and unmoved by anything the Crown did in between, falls on the whole capital, wall to wall, and on every Warden, priest and Triarch asleep inside it; the guard Dornhal rotates to keep itself awake holds for six days, and on the seventh a sentry dreams the whole of it in a single breath. The log counts one thousand one hundred and four dead across ten selections and one thousand two hundred and eleven in all, once the eleventh's riots, reprisals and private reckonings are added. It records the burning of Halstead in the flat notation it uses for weather. It also does one thing no one intended: an unrevised protocol answers <a href="../characters/anchorite-of-ardwen.html">an anchorite</a>'s sustained, specific request with more range than any subject in this or any earlier selection has been given, and the log files no correction, since correcting it would take an intervention more conspicuous than the deviation. Her second request, made during the eleventh selection and addressed to the dormant unit, is not serviced; the log cannot say whether the shared channel could not isolate it or the unit declined.</p>
          <p>The sheet draws a nearly invisible, faceless unit in dark, heat-resistant composite, with a saucer-shaped body, a tall antenna spire and trailing sensor tendrils, carrying optical, astronomical, atmospheric, dream-interface and communication arrays; its variants are labelled Scout, Sensor, Relay and Archivist. It pictures the network as hundreds to thousands of units and marks that as conceptual, a figure the manuscript does not give.</p>""",
            },
            {
                "slug": "cultivator-observer", "name": "Cultivator Observer",
                "epithets": "Observer, Case 1,268 &middot; Custodian-Office analytical authority &middot; no Envoy posted in person &middot; extremely old by the sheet",
                "teaser": "Watches the Aldemark experiment from beyond the reach of any native chronicle, and records, interprets and evaluates; the experiment continues.",
                "bio_html": """<p>The manuscript assigns the case no Envoy: its header reads <em>None assigned &mdash; autonomous network; no Envoy delivers or observes in person.</em> The sheet nevertheless files a <a href="../lore/cultivator.html">Cultivator</a> Observer under Case 1,268, the Custodian Office's analytical authority, and the Archival Log that closes the manuscript speaks throughout as <em>this office</em>. That log sets down the case's reading: that unmediated sight of the planet's true shape was enough, with no doctrine supplied, to produce the same discovery across eleven exposure samples however primed by rumor; that a suppressed cosmology proved a load-bearing variable of theocratic governance; that the tax, the judgment and the oath, which rested on the same institution, collapsed with it; and that the network gave the people nothing but observation, a distinction the office says it does not regard as a loophole.</p>
          <p>It also records, and sets aside without comment, that <a href="../characters/hraban.html">Warden Hraban</a> requested clarification before issuing a single one of his twenty-six years of sanctioned orders and that this variable produced no measurable alteration to outcomes; that <a href="../characters/anchorite-of-ardwen.html">the Ardwenist</a> was granted an extended range by a mechanical consequence of an unrevised protocol, with no corrective update filed; and that the dormant designation she asked for recurs, under seal, in at least six earlier case files. Its last line is its status: <em>Terrarium stable. Case closed. Filed.</em> The sheet draws an alien Cultivator, tall, slender and extremely old by Aldemark's chronology, with a narrow face, sparse fine dark-silver hair, large dark reflective eyes, cool grey-pale skin slightly translucent at the temples and no facial hair, in a long dark layered coat with the custodial insignia, holding an analytical tablet; its panels show a long-range observatory, an archival cylinder and a probe-network link, and its expression studies read neutral, assessing, flagging anomaly and no emotion. The pull-quote below is the sheet's own and does not appear in the manuscript.</p>""",
                "quote": "The Aldemark experiment is a variable in a larger dataset. Our task is not to interfere, but to record, interpret, and evaluate.",
            },
            {
                "slug": "solan", "name": "Solan",
                "epithets": "The Son &middot; god of the Threefold Crown &middot; flame, rebellion and the wide bright sky &middot; shown here as temple iconography",
                "teaser": "The Crown's god of fire, whose flame is lit over every oath, and whom one village mistakes for the sender of its dreams.",
                "bio_html": """<p>The Son of the <a href="../lore/threefold-crown.html">Threefold Crown</a>'s three, god of fire and rebellion and the wide bright sky, whose flame is lit over every oath a magistrate swears in Aldemark and whose seat <a href="../characters/sigward.html">Sigward</a> holds. In Grenmoor, the village that sings on its way to the burning, the dreaming is taken as a blessing sent down by Solan himself, since who else but the god of fire and rebellion and the wide bright sky would think to grant a farmer the sight of his own heaven from above it; the villagers raise a shrine of fieldstone and unbleached cloth to what they call the Star-Walkers. In the Crown's last years a small sect, the Solan Ascendant, breaks from orthodoxy to declare the dreaming a sign that the Son has at last outgrown the Father's law, a heresy the Crown's other parties agree on nothing except crushing. The god himself takes no part in the manuscript's events.</p>
          <p>The sheet draws the god as the temple paints him, not as anything seen in the dream: ageless and of heroic human scale, with a youthful face, red-gold hair under a golden laurel, bright amber eyes and a sun-warmed complexion, in white-and-crimson ceremonial robes with a flame-bright spear, and again in the light armor of the temple guard.</p>""",
            },
            {
                "slug": "elara", "name": "Elara",
                "epithets": "The Mother &middot; goddess of the Threefold Crown &middot; hearth-right and the family court &middot; shown here as temple iconography",
                "teaser": "The Crown's goddess of hearth and harvest, whose seat outlasts the others as the principal surviving civil authority.",
                "bio_html": """<p>The Mother of the <a href="../lore/threefold-crown.html">Threefold Crown</a>'s three, goddess of earth, harvest and hearth, whose hearth-right is Aldemark's family court and whose private rites each household keeps. The iron cold of early spring, when the granaries are thinnest and the ground is too hard to plant, is Elara's Fast to Aldemark's peasants, and it is on its first night that Halstead's dreams begin. <a href="../characters/adaltrude.html">Adaltrude</a> holds her seat, keeps a small hearth-shrine for her private rites, and goes to it alone before dawn after the eleventh dream. When the Crown fractures, Elara's seat, under Adaltrude and her successors, absorbs most of what remains of the temple's civil authority. The goddess herself takes no part in the manuscript's events.</p>
          <p>The sheet draws the goddess as temple art does: ageless and larger than human, with a calm maternal face, long dark-gold hair set with a gold diadem, red-jeweled ornaments and amber eyes, in layered deep-red and cream robes, beside a lit hearth and a household altar. It notes that her seat eventually becomes the principal surviving civil authority of the diminished temple.</p>""",
            },
        ],
        "scenes": [
            {"slug": "ymma-wakes-before-dawn", "title": "Ymma wakes before dawn",
             "alt": "A young woman in a linen headscarf with dark braids sits up in a log-walled bed, looking upward with her lips parted, a bearded man asleep beside her, a candle burning on a small table and a frosted window showing stars over a snowy village",
             "caption_html": """<a href="../characters/ymma.html">Ymma</a> sits up before dawn on the first night of Brayen, in the iron cold of Elara's Fast, with her husband still asleep beside her. She is about to wake him to say that she has been nowhere and everywhere."""},
            {"slug": "a-dreamer-drifts-toward-the-moon", "title": "A dreamer drifts toward the moon",
             "alt": "A barefoot youth in a leather vest and rolled linen sleeves floats through black space with his arms loose and his face lifted toward an enormous cratered moon, a curve of the blue world below him among scattered stars",
             "caption_html": """A dreamer of Halstead drifts through a black field of unfamiliar lights toward the moon, reaching it, as the first dreamers describe it, simply by wishing to."""},
            {"slug": "the-world-seen-from-the-moon", "title": "The world seen from the moon",
             "alt": "A young man in a leather vest and boots stands with his back to us on a rocky grey ledge and looks at the whole round world hanging in black space, its blue seas, green land and swirling white cloud filling the sky",
             "caption_html": """From far enough away the world stops looking like a floor and starts looking like a stone: round on every side, hanging in the dark with nothing beneath it and nothing propping it up."""},
            {"slug": "hraban-questions-otker", "title": "Hraban questions Otker",
             "alt": "In a timbered hall by lamplight a bearded man in a dark coat with a gold medallion leans on a table with one hand, face to face with a lean young man in a leather vest and linen shirt who stands upright and unflinching, villagers crowded behind them, a lantern and a sheet of paper on the table",
             "caption_html": """<a href="../characters/hraban.html">Hraban</a> questions <a href="../characters/otker.html">Otker</a> last and longest, with Halstead crowded into the room behind them. Otker tells him plainly, the way a man reports weather, that the world is round."""},
            {"slug": "a-village-after-the-purge", "title": "A village after the purge",
             "alt": "A bearded man in a long dark coat stands alone among the burned timbers, broken cart wheel and puddled mud of a destroyed village, a torn dark banner with a star on a pole beside him, smoke rising under a heavy grey sky and a ruined tower on the far hill",
             "caption_html": """What is left of a purged village: burned timbers, a cart wheel in the mud, smoke still rising, a torn banner on its pole and one man standing among the ruins."""},
            {"slug": "the-anchorite-kneels-in-halstead", "title": "The Anchorite kneels in Halstead",
             "alt": "In steady rain a hooded woman in tattered undyed grey wool kneels alone in black mud among the charred posts and chimneys of a burned village, a staff and pouch at her back, two hollows in the ash in front of her, a ruined tower on a misty hill beyond",
             "caption_html": """<a href="../characters/anchorite-of-ardwen.html">The Anchorite</a> kneels in the ashes of Halstead for the better part of an afternoon without asking a single neighboring farm what happened there. The next rain will fill the two hollows her knees leave."""},
            {"slug": "the-singing-at-grenmoor", "title": "The singing at Grenmoor",
             "alt": "At sunset a hooded woman in tattered grey wool stands at the left of a shrine of stacked fieldstone draped in unbleached cloth with candles, flowers and baskets of bread, a crowd of villagers lifting their hands and singing toward a swirling night sky, armed knights with banners crossing the field on the right",
             "caption_html": """Grenmoor raises a shrine of fieldstone and unbleached cloth to the Star-Walkers and sings, while armed men of the Crown come across the field. <a href="../characters/anchorite-of-ardwen.html">The Anchorite</a> stands before it and tells no one which god she thinks the singing was for."""},
            {"slug": "the-iron-globe-at-faldrun", "title": "The iron globe at Faldrun",
             "alt": "In a firelit forge a bearded blacksmith swings a hammer at a glowing iron globe on an anvil in a shower of sparks, a hooded woman in grey raising one hand over it in blessing while a group of villagers watch from the shadows",
             "caption_html": """At Faldrun a blacksmith hammers an iron globe on his anvil, and <a href="../characters/anchorite-of-ardwen.html">the Anchorite</a> lays her hand above it and blesses it in Ardwen's name while the village watches."""},
            {"slug": "the-boundary-stone-at-aschendale", "title": "The boundary stone at Aschendale",
             "alt": "On an autumn hillside grey-bearded elders and villagers stand around a lichen-covered boundary stone carved with a sunburst, one elder with his palm open toward a black-and-gold robed official holding a great book with a gold sunburst on its cover, armed guards at the official's side and a hooded woman standing quietly behind the stone",
             "caption_html": """At Aschendale's boundary stone the elders face an official of the Crown with a great book and an escort of soldiers, and choose a hard truth over an easy lie. <a href="../characters/anchorite-of-ardwen.html">The Anchorite</a> stands among the villagers behind them. No purge is ever ordered here."""},
            {"slug": "the-anchorite-is-taken-at-reinfeld", "title": "The Anchorite is taken at Reinfeld",
             "alt": "Soldiers in dark helmets and cloaks marked with a sunburst take a hooded woman in ragged grey by the wrists beside a harbor where smoke rises from a distant village, a young spearman in the foreground looking away, banners behind them and a crowd of villagers watching",
             "caption_html": """At Reinfeld soldiers of the Crown take <a href="../characters/anchorite-of-ardwen.html">the Anchorite</a> on charges of vagrancy and obstruction. She asks the one who binds her wrists whether he was at Halstead."""},
            {"slug": "the-anchorite-asks-to-come", "title": "The Anchorite asks to come",
             "alt": "A hooded woman in a ragged grey robe kneels in a narrow stone cell, one wrist in an iron cuff on a chain, her hands lifted into a shaft of moonlight from a single barred window that shows stars and a full moon",
             "caption_html": """In a cell too narrow to lie down in, <a href="../characters/anchorite-of-ardwen.html">the Anchorite</a> kneels toward the one barred slit and asks, not for rescue or vindication, only to be let come."""},
            {"slug": "the-anchorite-rises-above-aldemark", "title": "The Anchorite rises above Aldemark",
             "alt": "A hooded figure in a pale cloak floats upright above the curve of a blue-and-white world, a glowing path of stars and golden suns spiralling away overhead, a walled city and a river valley below",
             "caption_html": """<a href="../characters/anchorite-of-ardwen.html">The Anchorite</a> rises above Aldemark, past the globe, the furnace of the sun and a river of suns, farther than any dreamer in the kingdom's history has been given."""},
            {"slug": "the-dormant-figure", "title": "The dormant figure",
             "alt": "A colossal pale figure with long straight black hair and unblinking red eyes, its white robe spreading like a mountain across the whole frame, fills the darkness; at its feet, on black water, a tiny hooded figure stands",
             "caption_html": """At the top of the ascent <a href="../characters/anchorite-of-ardwen.html">the Anchorite</a> stands before a dormant figure with straight black hair, a white too fine to name and red unblinking eyes. She asks whether it called her. It does not answer."""},
            {"slug": "the-eleventh-dream-over-dornhal", "title": "The eleventh dream over Dornhal",
             "alt": "A cathedral city lit gold under a starry night beside a river with a stone bridge; the faint translucent figures of three robed rulers, one in red and cream, one in dark with gold and one in pale blue, rise above it with crowds of ghostly faces among the stars while soldiers and townsfolk fill the street below",
             "caption_html": """The eleventh selection falls on the capital itself. Dornhal dreams wall to wall, and the Triarchs <a href="../characters/ansovald.html">Ansovald</a>, <a href="../characters/sigward.html">Sigward</a> and <a href="../characters/adaltrude.html">Adaltrude</a> rise above it among the faces of its sleepers."""},
            {"slug": "hraban-finds-the-anchorite", "title": "Hraban finds the Anchorite",
             "alt": "A weathered man in a plain grey coat and a hooded woman in tattered grey sit on a ruined stone ledge on either side of a vine-covered wayside shrine with a candle lit in its niche, a river valley and a distant castle under a sunset sky behind them",
             "caption_html": """Within the year <a href="../characters/hraban.html">Hraban</a>, in a plain grey coat with no insignia, finds <a href="../characters/anchorite-of-ardwen.html">the Anchorite</a> at a crossroads shrine and asks whether she dreamed what the city dreamed."""},
        ],
    },
    {
        "slug": "0202", "title": "Fossa",
        "status": ["coming-soon"],
        "cover_file": "0202.jpg",
        "hook": "Swarm. Ditch. Signature. Tithe. Miracle.",
        "case_tag": "Case 0202",
        "catalyst": {
            "name": "Strain H-202",
            "meta": "A banded fungal parasite of a migrating swarm",
            "page": "characters/strain-h-202.html",
            "img": "characters/strain-h-202-thumb.jpg",
            "html": "<p>A banded fungal parasite of an orthopteran swarm, broken open by hand from a single sealed clay bait-pot in the roosting scrub ahead of a migrating swarm of red grasshoppers. It spreads by contact alone, and the longer the swarm is held in one place the faster it goes; at first light it turns every animal it has taken from the line of the swarm's advance to the line of the sun, up the nearest east-facing surface, where they grip, spread their wings and die with a chalk-white collar of thirty-three bands (1, 1, 2, 3, 5, 8, 13) at the neck. The dead are edible. What a kingdom and its three altars do with four hundred feet of cliff hung with them, bright and motionless in the morning sun, is the case.</p>"
        },
        "envoy": {
            "name": "Observer 551",
            "meta": "&ldquo;Ratièr&rdquo;, an itinerant rat-catcher",
            "page": "characters/observer-551.html",
            "img": "characters/observer-551-thumb.jpg",
            "html": "<p>Custodian of record for Strain H-202, working under cover as a rat-catcher called Ratièr, which in the dialect is a trade and not a name: a plain brown-cloaked man with a pack and a long bait-spoon who passes through every mill, barn and cellar of a grain valley without question. He seeds the culture on the eleventh of Garren in a clay bait-pot of the kind his cover sells to mills, files three Envoy's Notes, sells nothing, and never applies his translation array to the stranger who is displaced into the case from another file. He passes that file's Custodian on the quarry road with an exact courtesy, and walks away down the south road to another posting when the case is done.</p>"
        },
        "pages": EDITOR_PAGES,
        "genre": EDITOR_GENRE,
        "synopsis_html": EDITOR_SYNOPSIS,
        "characters": [
            {
                "slug": "observer-551", "name": "Observer 551",
                "epithets": "Cultivator Envoy and Custodian of record for Case 0202 &middot; cover: Ratièr, an itinerant rat-catcher &middot; appears about 45 by his sheet",
                "teaser": "Seeds one clay pot of fungus on a mountain pass, files three notes, and sells nothing.",
                "bio_html": """<p>A thin, plain, forgettable man in a brown travelling cloak with a pack, a long bait-spoon and a satchel of clay pots, who has walked the Lauze for nineteen days by the evening of the twentieth of Garren under the name Ratièr, which in the dialect is a trade and not a name. A rat-catcher passes through every mill, barn and cellar of a grain valley without question, which is the access the study needs and the only access it needs. On the eleventh of Garren he breaks a sealed clay bait-pot with the spoon, by hand, in the upper broom-scrub of the saddle called the Port, where the swarm's first night's roost will fall, in the manner of a man laying poison for vermin in a place that has none. He supplies no knowledge; he introduces one organism and lets it do what it does, and the banding on its fruiting collar is the only signature he leaves.</p>
          <p>He attends the weighing at the mill offering bait, sits at the table by the door in <a href="../characters/brunissen.html">Brunissen</a>'s tavern with a mug of ale he does not drink and takes <a href="../characters/gaucelm.html">Gaucelm</a>'s tin ward, turns it over with great gravity and hands it back, and on the fifth night stands on the lip of the second rank with a bait-pot and sells nothing. He files three Envoy's Notes. He records an apology on an instrument not calibrated to record one, does not apply his translation array to the stranger's speech because the Prime Directive bars supplying a framework, and finds he cannot stop knowing the syllables of a five-line verse he did not translate. Three times he passes the other Custodian, <a href="../characters/observer-618.html">Observer 618</a> of Case 2231, once on the quarry road, once at the quarrymen's wall and once on the lane below Vilarnau walking toward the mill with a lantern, each in the character of a man with nothing to say to the other, and the courtesy is exact. In a later spring he goes down the long south road with his pack and his bait-spoon to a country where the rats are of a different kind. The sheet's 5'8&quot;, thin brown hair, pale grey eyes and apparent age of forty-five are its own; the manuscript has only &ldquo;thin, middle-aged, brown-cloaked, with a pack.&rdquo;</p>""",
                "quote": "He is not supposed to find that difficult to put down. Filed.",
            },
            {
                "slug": "strain-h-202", "name": "Strain H-202",
                "epithets": "Catalyst of Case 0202 &middot; Heliotropic Orthopteran Mycosis, strain H-202 &middot; seeded on the eleventh of Garren",
                "teaser": "A banded fungus that turns a swarm toward the sun and leaves a cliff hung with the dead.",
                "bio_html": """<p>A banded fungal parasite of an orthopteran swarm, broken open from a sealed clay bait-pot in the upper broom-scrub of the Port on the eleventh of Garren, where the swarm's line of descent will place its first night's roost. It carries no instructions and no Cultivator knowledge. It reaches its conidial stage within thirty hours of contact and spreads by contact alone, which is why the trenches matter: held animals crowd, and crowded animals in a population carrying a contact-transmitted spore infect one another faster than any open-field swarm could in a season. The Log puts contact density in the gorge at eleven times free-flight baseline and infection at an estimated eighty-eight in a hundred by the end of the fourth day. At dusk of the fifth the infected animals begin to climb; at first light on the twenty-seventh of Havren they turn, as one, from the line of the swarm's advance to the line of the sun, go up the nearest east-facing surface, grip with the forelegs, spread their wings and die.</p>
          <p>On each body a chalk-white fruiting collar forms within the hour, thirty-three pale bands in the order one, one, two, three, five, eight, thirteen, so that a sufficiently rigorous investigator may infer a non-natural origin without any disclosure from the Observer's desk. The flesh of the dead is edible, an inherited feature and not an intended one, and tastes of roasted chestnuts and butter. The strain is self-limiting and was never recovered; the animals that leaked through in the first days, infected more slowly in open country, died singly over the next fortnight on the east-facing walls of the valley, and every preserved specimen in the Order's cabinet at Montclar carries the bands, beside which the clerk Matteo wrote <em>same on all; curious</em> in pencil. By the Log's reckoning the works at the Throat held the swarm in the gorge five point one days longer than an open crossing would have, long enough for the strain to do what it does; without them the swarm would have passed the Narrow in a morning and ended in open country after the crop was gone. The manuscript gives no length for the insect; the sheet's rust-red body of about five centimetres is its own.</p>""",
            },
            {
                "slug": "the-accord-of-montclar", "name": "The Accord of Montclar",
                "epithets": "Royal charter of Auvarre &middot; the Right of First Naming &middot; two centuries old &middot; drafted in the reign of the second Ramon",
                "teaser": "Promises a tenth of the realm's grain, forever, to whichever altar the realm can be found to owe, and ends on the numeral one.",
                "bio_html": """<p>A charter drafted by a committee of two altars and a notary after the Drowning of the Lower Fields, when a river went back in the night with no one's leave and three temples each told their flocks by morning that it was theirs. Its remedy was elegant: whichever altar the realm could be found to owe its salvation to should have the Right of First Naming, to name the deliverance in the law and liturgy of the realm and take a tenth of the grain of the realm, year by year, for as long as the realm lasted. The seventh article is where the verb is, <em>owe</em>. The eighth gives the arbiters seven days to decide which altar that is; the ninth gives a divided table to the king's casting voice, <em>saving the king's own interest</em>; and the tenth says that if the arbiters stand divided and the throne be silent, each altar shall name one man, sworn to no other altar, to bear one edge before the three doors until one man yield or fall. The arbiters sit each for the whole of an altar and not for one chapter, and the tithe is of the grain of the realm and not only of the March, since the second Ramon reasoned that a danger to any field was a danger to every field. It had been tested once, with two altars, and ended in a quiet agreement. It had never been tested with three.</p>
          <p>On the first of Iverin <a href="../characters/arnaut.html">Arnaut</a> reads it aloud at the oak table from a bad copy in a clerk's cramped hand, three smudges and a stain, in the flat voice of a man who cannot improve the text. The Hierarch and the Provost each ask for the Naming; the Keeper says she does not know; the king's recusal comes out of the bailiff's sleeve; and the tenth article, which he reads in a voice gone flat, asks for one edge from a stranger who carries two. &ldquo;The Observer introduced no numeral,&rdquo; says the Log, and the numeral in the tenth article is the whole of what the case turns on. The sheet draws the charter on calfskin vellum in brown-black ink with three hanging wax seals and the word ONE under the tenth numeral; the manuscript does not say how many seals it carries or what the vellum is.</p>""",
                "quote": "One man. One edge.",
            },
            {
                "slug": "king-ramon-iii", "name": "King Ramon III",
                "epithets": "King of Auvarre, third of his name, seated at Montclar &middot; twenty-six years on the throne &middot; 54 years old by his sheet",
                "teaser": "A poor man and an honest one, who declines the casting voice in advance and signs his kingdom in two with a hand that does not shake.",
                "bio_html": """<p>The king of Auvarre, who sits at Montclar in a palace the court jokes was built by a committee of the dead, and who is, in the letter that opens the case, the one person in the realm with no grain, no gold and no soldiers who says so. He commands every baron of the southern marches to do what his own hand can find to do, summons the three altars of the Accord of Montclar to the March, and offers them, being poor, the only coin a poor king can mint without leaving a mark on his treasury, which is credit: the Right of First Naming. On the twenty-sixth of Garren, the day a clerk of the Last Order calls at the palace to remind him, with perfect courtesy, of the date the wall-loan falls due, he signs a second letter and sends it south without waiting to learn what the altars have done. Being a poor man and an honest one, and in debt to one of them, he cannot in conscience give a casting voice in a cause in which he is himself a debtor. A debtor who cast for his creditor would be a king bought, and one who cast against him a king foreclosed; he chooses, as poor men do, the course that costs him nothing, which is to be absent from the Accord in advance.</p>
          <p>He signs the partition on the ninth of Lorren in the third winter, in a room above the wall the Order's money built, with a brazier at his feet and the Provost-Examiner of the Montclar chapter at his elbow holding the pen: eleven articles recognising two countries, the Lit Reach and the Baronies, and releasing the crown from the loan in return for acknowledging the Naming of the Last Order on one side of a line and of the Threefold on the other. He reads all eleven, which no one asked him to do, with his lips moving slightly, as men read who were taught to read late, and then looks at the wall of the room and says that it is a good wall. His hand does not shake; it is the one thing in the room that remains under his command, and he spends it as a man spends his last coin. He dies four months later and is buried in the spring beneath a stone the Order paid for. The manuscript gives his twenty-six years and his late reading, not his age; the sheet's fifty-four, near-sighted watery grey eyes, thin brushed-back grey hair and short beard are its own.</p>""",
                "quote": "It is a good wall.",
            },
            {
                "slug": "pons", "name": "Pons",
                "epithets": "Herald of King Ramon III &middot; 19 at the opening, 22 at the Throat &middot; later keeper of the royal archive at Montclar",
                "teaser": "Sees a smear the color of dried blood on the southern horizon, and in a long life is never asked to describe it.",
                "bio_html": """<p>A herald of nineteen who rides four days from Montclar to arrive on the twenty-fourth of Garren, with the king's letter in an oiled satchel strapped against his chest and his chin tucked down against a wind that has turned, unseasonably, warm. On the morning of the fourth day, from the crest of the last ridge before the Lauze, he sees on the southern horizon a smear the color of dried blood, no larger than a thumbprint, that neither moves nor fades, and looks at it for a long time with the clear feeling of a boy who has been given a message and has just found out what it weighs. He delivers the letter to the bailiff in the correct form, and then, when the formalities are over, asks in a small voice whether he might sit down.</p>
          <p>Three years later, at twenty-two, he is sent down the south road in sleet on the thirteenth of Lorren with the sealed duplicate of the partition strapped where the king's letter once was, to read it at the Throat to a hundred of the Baronies' levy in the red of the Son and a hundred and twenty lay-brothers of the Last Order in grey, with <a href="../characters/gaucelm.html">Gaucelm</a> vending roasted nago between them at the same price to both. He reads it in the clear carrying voice the College of Heralds taught him, watches the masons set an unlettered stone, and looks up, because it is the only direction nobody else is looking, at what is left of the Dawn Wall: a fringe of the dead along the brow, so exactly the color of the smear that his horse lays its ears back. He has no wish to describe it, and does not. He becomes, forty years on, a very old man and the keeper of the royal archive at Montclar, and among the thousand times he is asked about the partition of Auvarre he is never once asked about the wall. The manuscript gives him no face; the sheet's freckles, hazel eyes and royal-blue herald's tabard are its own.</p>""",
            },
            {
                "slug": "ibrahim-ibn-nasr", "name": "Ibrahim ibn Nasr",
                "epithets": "Wool-factor of the port of Almariya &middot; first bearer of the news of the Red Weather &middot; 38 years old by his sheet",
                "teaser": "Rides eleven days north on a mule he means to sell, and tells a bailiff a sentence nobody believes.",
                "bio_html": """<p>A wool-factor from the southern coast who rides eleven days up through the Serra on a mule he intends to sell and a horse he does not, and arrives at the inn below the castle spur on the seventeenth of Garren with a cup of thin red wine and the expression of a man composing, with some care, a sentence he knows no one will believe. He tells it to the bailiff <a href="../characters/arnaut.html">Arnaut</a> in the dialect of the district, which he speaks well and with a slight stiffness, as of a man handling a tool borrowed from a neighbor: that the Red Weather has come up out of the dry country beyond the southern mountains, eaten the barley of the coast in early summer and the olives and vines of the hill-country in late, and that on the quay of Almariya he watched a cloud the color of rust come over the sea-wall at noon without a sound that a man could have named, and the market's awnings turn into something that moved. It did not stop at the stubble. Arnaut, who has been handed a figure that fits none of his columns, pays for the wine himself, the first time in the factor's recollection that an official of any country has done so.</p>
          <p>On the first of Havren he is at <a href="../characters/brunissen.html">Brunissen</a>'s tavern, persuaded after much wine to be a guest, and tells the room, with a certain defiant humor, that in the south the people have grown so tired of the Weather that they have begun to eat it: dried on hot stones with salt, fried in oil and sold by the bowl, the fat ones of the early swarm tasting something like toasted nuts. The room answers with a long and affectionate silence, and then someone laughs. It is the most consequential throwaway line in the case. On the afternoon of the twenty-seventh, with the dead heaped round her ankles and the Vigil's porridge gone, the miller's widow <a href="../characters/ermengarda.html">Ermengarda</a> says to the stranger, in the flat tone of a woman discharging an obligation, that in the south, so the factor had said, they ate them. The manuscript does not say what became of him. It gives his name, his trade and his manner; the sheet's thirty-eight years, dust-striped cloak, white cap and neatly trimmed black beard are its own.</p>""",
                "quote": "It stopped when there was nothing left that it could stand on.",
            },
            {
                "slug": "ottavio-brandi", "name": "Ottavio Brandi",
                "epithets": "Provost-Examiner of the Solar Temple's chapter at Montclar &middot; arbiter of the second altar, the Last Order &middot; 50 years old",
                "teaser": "Judges a wall of dead grasshoppers by lens, writes &ldquo;Lit&rdquo; in the Book, and spends the rest of his life writing the date, the weather and the town.",
                "bio_html": """<p>A lean, fastidiously dressed man of fifty in the undyed grey of the Last Order, with a high narrow forehead, a pinched mouth and a pair of cold clever hands, who arrives at Castelmaur on the twenty-sixth of Garren in a closed grey carriage with two clerks, a portable strongroom, a brazier he will not be parted from and a ground lens the thickness of a man's palm in a padded case on his knees. At the council of the three altars he proposes that all the grain of the valley, green or ripe, be reaped into the strongroom of the Solar Temple under seal and receipt, since what is ledgered cannot be eaten by an enemy that has no clerks. He asks the foreigner for the names of his swords, hears <em>Yoake</em> and <em>Yoiyami</em>, Daybreak and Evening Dark, the hour the light comes back and the hour it is spent, and enters in the margin of his own mind, as an accident of nomenclature and nothing more, that the stranger has a certain presence. He passes him the roll headed <em>Works done under the Reading</em>, under the maxim every novice copies forty times, <em>the hand that signs must answer</em>, and keeps the signature.</p>
          <p>On the morning of the twenty-seventh of Havren he has the lens sent for before anyone has understood there is anything to judge, throws the sun through it onto the Dawn Wall, and sees, in the length of a held breath, that the wall is returning the beam rather than making any, as a polished basin returns a candle. An Examiner who writes his doubt into the margin of a Judgment has made himself the next thing the Judgment must be applied to; he says to the clerk with the pen, &ldquo;Enter it. Lit.&rdquo; On the twentieth of Iverin he reads the second line of his sister's letter, learns that his daughter died on the ninth of Garren, and goes down on the boards of his room in front of the brazier; in the morning he turns Arnaut's compromise paper face down on the newel-post and orders the granary sealed. He holds the chapter at Montclar eleven years more, never again enters a debt in the name of a feeling, writes the date, the weather and the name of the town at the head of every document that leaves his hand, and on every ninth of Garren rides four days south to read the evening office alone at the foot of the Dawn Wall, to no one, with nothing entered. He writes every week, beginning with the weather, to a girl who is dead; the Examiners who clear his desk find five hundred and seventy-two of the letters. The Book still says the Throat was lit.</p>""",
                "quote": "Credit is not a feeling, Hierarch. It is an entry.",
            },
            {
                "slug": "matteo", "name": "Matteo",
                "epithets": "Clerk to the Provost-Examiner of the Last Order &middot; a baker's son from the hills behind Montclar &middot; 23 years old",
                "teaser": "Carries the Order's flame three leagues up a valley in a clay lamp, counts the bands on the dead, and writes the date in a margin.",
                "bio_html": """<p>A fat, pale young man with a face like a boiled egg, twenty-three, a baker's son from the hills behind Montclar who joined the Last Order for the sake of its ovens and counts everything unprompted: a sack, a stair, a flock of sheep, a row of loaves. For fifteen days at the Narrow he carries the Order's flame, kindled each noon at the focus of the ground lens on the flat roof of the inn at Vilarnau, three leagues up the valley in a small covered clay lamp pressed against his chest like a baby, glancing down at it every dozen paces with the anxious tenderness of a young father, and never lets it go out. He keeps the labor-tally in a fair hand every evening; he enters the leakage of the first day at three in a hundred and is told by the bailiff to enter it at two.</p>
          <p>On the morning of the twenty-seventh of Havren he climbs a barrel in the shadow of the Provost's platform and counts the pale rings on the dead: forty, a hundred, thirty-three bands on each, in the order one, one, two, three, five, eight, thirteen, the nursery progression his mother used to teach him to add. He thinks nothing of it that he would say to a Provost, since a baker's boy knows what it means when every loaf in an oven comes out alike, and writes in the margin of his roll in pencil <em>same on all; curious</em>. On the night of the twentieth of Iverin he comes in at a sound with a candle and sees the Provost on the floor; he sits against the wall in the dark until morning, says nothing then or ever, and in the grey takes the day's roll and writes in its margin, where the Order's rule allows only a number, the date, a word for the weather, and the name of the town. He does not strike it out, though he is a young man with a living to make. The Order's system files it with the rest. The manuscript gives his age, his bakery and his pallor; the sheet's bowl-cut light brown hair, mild blue eyes, ink-stained fingers and pencil behind the ear are its own.</p>""",
                "quote": "Same on all; curious.",
            },
            {
                "slug": "alazais", "name": "Alazaïs",
                "epithets": "Keeper of the House of Vigil at Sant-Sever &middot; arbiter of the third altar, the Vigil of Ardwen &middot; 61 years old, 64 at her death",
                "teaser": "Offers hands instead of a remedy, answers the council with &ldquo;I do not know,&rdquo; and feeds both altars without asking which they serve.",
                "bio_html": """<p>A small, brown-faced woman of sixty-one with a bad hip, a worn grey cloak and a face that gives the impression of having been left out in the weather and improved by it, who arrives at the temple gate at dusk on the twenty-seventh of Garren by mule, tells the servant who cannot decide whether to bow that she has a perfectly good pair of legs somewhere beneath the saddle, and asks to be shown where she is to sleep. She keeps the House of Vigil at Sant-Sever, one of some forty in the realm, and she has no remedy, no lamp, no lens, no ram and no pyre; she has hands. She says so to the council as one reports the weather: the Vigil does not command the sky, but its ten houses within a day's walk have a great many hands, and digging is not a claim. She sends six hundred of them, goes up and down the trenches through fifteen days with a can of water and a heel of bread, and where someone has stopped, sits down beside him. In the evenings she runs through her fingers a knotted cord, one knot for every child she has baptized in forty years, a hundred and fifty-three of them, tied a little looser than a knot ought to be, so that a child who comes back might be found.</p>
          <p>Asked on the first of Iverin, as arbiter of the third altar, which of the other two the realm owes, she says &ldquo;I do not know,&rdquo; and says it again more slowly for the clerk: that Ardwen answers the honest but never on command, and that she will not put a name on the table for the sake of a tenth of anyone's grain. Asked, in the Accord's own form, whether the Vigil will name a man for the Edge, she says that Ardwen does not send a man to answer a question she has not asked. That midnight she walks to the mill on her bad hip and tries, with a hundred and fourteen words of his language, to tell the stranger what he has signed, <em>grain</em>, <em>tithe</em>, a sack and a hand and a falling coin, <em>Edge</em>, <em>war</em>; he hears every word and understands none, and takes her <em>Do not</em> for <em>do not be afraid</em>. Every word was true, and it was a kind of silence. On the twentieth of Iverin she opens the doors at Sant-Sever without announcement and feeds the families of the dead, the levy's wives and children and the hungry of the Last Order out of a store scraped to the stone, never asking which altar they serve. She dies in the third year, at sixty-four, of a fever she takes from a child, having fed eleven thousand four hundred persons by <a href="../characters/joan.html">Joan</a>'s count; her cord has a hundred and sixty-nine knots. What she told the young Keeper who asked whether the goddess had turned the Weather is carved above the door of the House in the next century, and the pilgrims who come to read it are disappointed. The manuscript gives her age, her hip, her face and her cloak; the sheet's iron-grey hair and warm light-brown eyes are its own.</p>""",
                "quote": "I do not know.",
            },
            {
                "slug": "joan", "name": "Joan",
                "epithets": "Lay-brother of the House of Vigil at Sant-Sever &middot; 20 at the opening, about 23 at the Keeper's death",
                "teaser": "Is afraid of the mule, counts the fed and then the buried, and asks the one question nobody else would.",
                "bio_html": """<p>A lay-brother of twenty who carries the Keeper's saddlebag, is afraid of her mule, and stands behind her chair at the council with an air of respectful terror. He counts, as it turns out, with his lips moving, on his fingers when he works. On the third morning of the burying of the swarm <a href="../characters/gersenda.html">Gersenda</a> observes that he has stopped being afraid of the mule and is now afraid of nothing, working with a look on his face of a man who has been shown, quite suddenly, the inside of a word. He carries the lantern behind the Keeper on her midnight walk to the mill; and in the second winter, behind the refectory at Sant-Sever, where the ground is frozen to the depth of a hand and a grave takes four mornings and a fire, he begins to count the buried in the margin of the page on which he has counted the fed, and stops adding at a figure he never repeats.</p>
          <p>At the Keeper's bed in the third year he asks her the question he has carried since the first of Iverin and never found the hour for: whether she might not simply have picked one. &ldquo;Two to one,&rdquo; says Joan, &ldquo;and over by noon.&rdquo; She considers it a long time with her hand on the cord, says that she was very tired that day, had not thought of it, and does not know. It was not an answer, and Joan, who loved her, does not pretend that it was. He goes on keeping the count of the fed at Sant-Sever, with Gersenda's second column of the dead beside it. The manuscript gives his age and his fear of the mule; the sheet's six feet of height, prominent nose, ragged fair fringe and light blue eyes are its own.</p>""",
                "quote": "Two to one, and over by noon.",
            },
            {
                "slug": "paciencia", "name": "Paciència",
                "epithets": "The Keeper's mule &middot; carries Alazaïs from Sant-Sever &middot; 12 years old by her sheet",
                "teaser": "Possesses none of the virtue she is named for, and frightens a lay-brother by standing there.",
                "bio_html": """<p>The mule on which <a href="../characters/alazais.html">Alazaïs</a> rides the two days from the House of Vigil at Sant-Sever to the temple at Castelmaur, and on which she leaves the mill gate in the cold light of the second of Iverin. Her name means patience, and the manuscript is careful to record that she possesses none: she has not been consulted about the Keeper's midnight walk to the mill, and grumbles in the rear of it. The lay-brother <a href="../characters/joan.html">Joan</a>, who carries the Keeper's saddlebag, is afraid of her through the whole of the digging, until the burying of the swarm leaves him afraid of nothing.</p>
          <p>The manuscript gives her no age, colour or build. The sheet's twelve years, stocky four-foot-ten, dusty grey-brown coat, notched left ear, drooping lips, patched wool saddle-cloth and dark, unimpressed eyes are its own, and its captions, Suspicion, Alarmed by Joan, Stubborn Resolve, Impatient Grumble, are the nearest the file comes to her opinion of any of it.</p>""",
            },
            {
                "slug": "bertran-0202", "name": "Bertran de Lanta",
                "epithets": "Sir Bertran de Lanta &middot; master-at-arms of Castelmaur &middot; knight &middot; 41 years old by this sheet",
                "teaser": "Fights a stranger to a draw, to a yield and to a gap in the second rank, and finds no column to enter any of it in.",
                "bio_html": """<p>The master-at-arms of Castelmaur, tall and broad, &ldquo;as grave and unreadable as an oak&rdquo;, knighted at nineteen and sworn to Auron in the temple at Montclar, who has spent twenty-two years learning that a knight does not say what he is thinking. On the twentieth of Garren, from the saddle, he drew on the stranger on the green at Vilarnau and had his long sword turned out of his hand in three point one seconds by a motion his eyes could not follow, and was left alive. On the sixth of Havren he lays two practice swords of ash on the gravel at the Narrow, takes up a buckler of boiled leather and fights him for most of an hour to a draw, a conversation, and a remarkably fluent one; he goes to bed with a cracked rib under a blanket his sister has embroidered with horses, and carves the beginning of a small pearwood horse with its ears laid back and one forefoot raised. On the night of the twenty-sixth he goes down into the gap in the second rank with a burning brand and holds it beside the foreigner through a night; toward the end, when the foreigner's left arm begins to tremble, he takes the brand from his fingers and puts his own sword into them, and they say each other's names, <em>Ber-tran</em>, <em>Higa</em>.</p>
          <p>On the second of Iverin the Hierarch names him champion of the Threefold for the Edge, for a tithe whose price he was not told. He asks for the night, goes down the lane to the mill gate with the first of the pearwood horses in his fist, stands there as long as it takes a bell to ring Prime with the goose regarding him, and goes back up the lane, since nothing in his training told a man how to knock. On the third, in the temple yard, he fights the best he has ever fought, some three hundred strokes, takes a cut along the left forearm that opens the mail, has the stranger's blade hang a hand's breadth from his bare head for exactly as long as it takes a man to decide something, is disarmed by a left hand that answers before it is consulted, is spared a second time, and says to the foreigner, and not to the doors, &ldquo;I yield. Let it be entered.&rdquo; In the third winter, on the sixteenth of Kerren, he rides out of the gate of Castelmaur alone at night, without a banner and without his sword, to pay a debt of a kind this account does not record, with a grey gelding of pearwood, one hoof raised, in the pouch at his belt, which he carries for the rest of his life. The Lauze says he was never beaten. He would have said that he was spared twice in front of everyone and handed a sword once, and that the last was the only entry he ever found a way to carry. His <a href="../characters/bertrans-sister.html">sister</a> has four children he has met twice. The same man has a page under <a href="../characters/bertran.html">Case 2231</a>, whose sheet makes him thirty-eight; this one makes him forty-one, which is what twenty-two years of service from a knighting at nineteen come to. The two pages are not reconciled.</p>""",
                "quote": "I yield. Let it be entered.",
            },
            {
                "slug": "baron-of-saint-aventin", "name": "Baron of Saint-Aventin",
                "epithets": "Eldest of the Threefold barons &middot; unnamed in the manuscript &middot; 62 years old by his sheet",
                "teaser": "Appears only as a letter, written in a hand that does not trouble with courtesy.",
                "bio_html": """<p>He is a letter. The war, says the manuscript, took the better part of two winters to discover that it was one, and the discoveries came in the order in which a ledger reveals a loss: first a letter, then a date, then a wall. The letter comes on the ninth of Iverin under the colors of the Baron of Saint-Aventin, eldest of the Threefold barons, who writes to the Hierarch at Castelmaur in a hand that does not trouble with courtesy that eleven barons of the south will pay a tenth of their grain to no creditor in grey, and asks how many men the temple can put on a road by the spring. He writes four days after the Hierarch has declared the Accord of Montclar void on the fifth of Iverin, and what he asks for is soldiers. The date is the Last Order's, calling the crown's loan on the first of Kerren; the wall is at Montclar.</p>
          <p>That is the whole of what the manuscript gives him: a title, a seniority, a colour, a number of fellow barons and a tone of voice. He has no name, no face, no age, and no reply is recorded, though the Hierarch has been believed by eleven of the realm's seventeen barons, who are Threefold. The sheet's sixty-two years, stout five-foot-eight, florid jowled face, sharp dark-brown eyes, silver hair worn long to the collar, forked silver beard, gold ring on every finger of the right hand, scarlet-and-gold quilted surcoat, fur mantle and jeweled sword are its own, and so is the line it prints beside him, <em>No creditor in grey shall take our grain</em>, which is the sheet's gloss on the letter and not a quotation from it.</p>""",
            },
            {
                "slug": "the-provosts-daughter", "name": "The Provost's Daughter",
                "epithets": "Daughter of Ottavio Brandi &middot; unnamed &middot; died on the ninth of Garren, aged 16",
                "teaser": "Writes to her father every week for nine years, and is dead for the whole of the case before he is told.",
                "bio_html": """<p>She is seven when her father puts her hand into her aunt's in the cathedral at Montclar and says, in the voice he uses for ledgers, that the Order's work will take him some years, which in the Order's practice means the circuits of the provincial houses and no more than the three weeks of each Reckoning-tide at home. She says, quite calmly, that she will write. She writes once a week for nine years, in a round clear child's hand that grows with the years into a young woman's, and he answers every letter on the day he opens it, in a hand that does not change, beginning with the weather he is not in. He has never once missed; the manuscript calls it the only discipline of his life that he was not taught. In the autumn he remarks to the brazier that the hand in her latest letters has grown a little steadier than a girl of sixteen might be expected to make it, and decides, as a man decides who has been cold for a very long time and does not wish to learn why, that a daughter is permitted to improve.</p>
          <p>She never appears in the manuscript alive. She dies of a fever of three days on the ninth of Garren, not painfully; on the second night she asks for her father once, and does not ask again. Her letter of the sixth is still unsealed in the drawer of her desk, because there was no time, and her <a href="../characters/the-provosts-sister.html">aunt</a>, who knows what the news would do to him, seals it afterward and sends it, and writes every one that follows in the child's hand and the child's voice. The case learns what the letters were on the twentieth of Iverin, when <a href="../characters/ottavio-brandi.html">Ottavio Brandi</a> reads the second line of his sister's letter. He goes on writing to her, weekly, beginning with the weather, and keeps the letters unsealed in a drawer; the Examiners who clear his desk find five hundred and seventy-two of them. The manuscript gives her age and her handwriting. The sheet's slim five-foot-three, narrow serious face with her father's high forehead, two dark braids, pale grey eyes, ink-stained fingertips and grey-blue wool dress with a white collar are its own.</p>""",
            },
            {
                "slug": "the-provosts-sister", "name": "The Provost's Sister",
                "epithets": "Sister of Ottavio Brandi &middot; the aunt who raised his daughter &middot; unnamed &middot; 55 years old by her sheet",
                "teaser": "Writes a dead girl's weekly letters in the dead girl's hand, and then writes the true one.",
                "bio_html": """<p>She is the aunt into whose hand the Provost put his seven-year-old daughter in the cathedral at Montclar, and she is the one who taught the child to write. When the girl dies of a fever on the ninth of Garren, with a weekly letter lying unsealed in her desk, the aunt seals it and sends it, and then writes every letter that follows herself, in the round clear hand as nearly as an aunt who had taught it could make it and in the voice of a girl who was dead, so that her brother should not have to be told until the Order's business allowed him to come home. She thought it kind. She had meant, her letter says, to keep her silence until the spring.</p>
          <p>It gives out on the twenty-second of Havren, the morning after his answer of the seventeenth arrives and asks, at the foot, whether the girl has her winter cloak. She writes the true letter in her own hand, so that he may know it from the first stroke, and says that she is very sorry. He reads the first line on the first of Iverin and carries the rest, unread, in the sleeve of his grey coat until it falls out on the twentieth; the manuscript does not record that she is told what it did to him, or whether she is ever answered. It never names her. The sheet's fifty-five years, spare five-foot-six, severe tired face, pale skin, grey hair pinned tight, grey eyes, black wool dress and grey shawl are its own, and so is the teacher's hand it draws, steady and exact, which is inferred from the manuscript's remark that she had taught the girl's.</p>""",
            },
            {
                "slug": "smith-of-vilarnau", "name": "The Smith of Vilarnau",
                "epithets": "The village smith &middot; unnamed &middot; 42 years old by his sheet",
                "teaser": "Brings a hammer to the green on the first night, and later makes a drum from a cask for the boys at the Throat.",
                "bio_html": """<p>The village comes out onto the moot-green at Vilarnau at full dark on the nineteenth of Garren with rushlights and crooks and, in the case of the smith, a hammer, and stands in a ragged half-ring forty paces from the oak, and nobody goes closer. It has been nine years since the last man came out of the stone, and he died. The old women of the church remember him in the tavern on the first of Havren: a thin small man with ink on his fingers who had lived eleven days in the smith's loft and died on the twelfth, of nothing in particular, apologizing. <a href="../characters/kaneyoshi.html">Case 2231's page for Kaneyoshi</a> gives the same man three days and a burial on the third night; the two accounts are not reconciled. In the same room the smith offers his verdict on the Keeper of Sant-Sever, who has asked for nothing: a priest who asks for nothing, he says, &ldquo;has a purpose that he is keeping to himself.&rdquo;</p>
          <p>At the Throat he makes a drum from a cask, and by the third morning of the digging the line of boys with the wooden harvest-rattles has been taught to keep time to it; when the swarm comes down on the gorge, a hundred drums behind the second rank, beaten by boys in a long line, keep the main flood from settling. His wife, <a href="../characters/smiths-wife.html">the smith's wife</a>, made the stranger sausages and was turned down. Case 2231 has the same man at the green with his hammer among <a href="../characters/villagers-of-vilarnau.html">the villagers</a>, and has him not living to reach the ridge after Vilarnau burns, when his son, <a href="../characters/smiths-son.html">the Smith's Son</a>, carries the hammer up the quarry road; this manuscript does not say what became of him. The sheet's forty-two years, massive six-foot-one frame, square soot-smudged face, black hair tied back, thick beard singed at the ends, dark eyes, burn-scarred forearms, leather apron and sleeveless tunic are its own.</p>""",
            },
            {
                "slug": "smiths-wife", "name": "The Smith's Wife",
                "epithets": "Wife of the village smith &middot; unnamed &middot; 40 years old by her sheet",
                "teaser": "Made sausages for the stranger and was turned down, and says what the village is afraid of out loud.",
                "bio_html": """<p>She has made sausages for the stranger, and he has turned them down. On the twenty-seventh of Garren, on the moot-green, he draws a long deep line in the dust with a row of small flames beside it and a cloud of marks on the farther side; Old Bernat takes the pipe from his mouth and says, quite quietly, &ldquo;Fossa&rdquo;; a woman makes the sign of Elara, and a second woman does; and then the smith's wife says in a high voice that the Moon-Man is telling them what to dig. It goes through the ring in a murmur. He is a prophet, or an angel, or the Eastern Dead come back to warn them; he has drawn them a grave, and beside it the pyres, and on the farther side the Red Weather itself coming down to fill the valley.</p>
          <p>She does not say, or the manuscript does not record, what she thinks of him after that; her one line is the whole of her part, and it names what everyone had been afraid to. Why the sausages were refused is not given here either. <a href="../characters/villagers-of-vilarnau.html">Case 2231 draws her</a> among the village chorus, sending round a dish of boiled sausage and weeping when it comes back untouched. Her husband is <a href="../characters/smith-of-vilarnau.html">the smith</a>. The sheet's forty years, plump five-foot-three, round ruddy face quick to take offense, brown eyes, brown hair under a kerchief, wool dress, greasy apron, tray of sausages and shrill voice are its own; the manuscript has only &ldquo;a high voice.&rdquo;</p>""",
            },
            {
                "slug": "arnal", "name": "Arnal",
                "epithets": "Smallholder of the lower terrace at Vilarnau &middot; two fields &middot; 38 years old by his sheet",
                "teaser": "Cuts his millet by night, hides it in the loft like a birth, and is entered in the Book on the fourteenth.",
                "bio_html": """<p>A smallholder of the lower terrace at Vilarnau, who cuts his two fields by night in the second week of Iverin and hides the sheaves in his loft under a layer of straw, like a man concealing a birth. The harvest stands that autumn. The sickles of the Threefold are blessed and the seals of the Last Order are on the barns, and nobody can cut a sheaf in the barony without committing an offense against one altar or the other; the Order writes the name of any household that cuts or carries without receipt into the Book, under those <em>spending a favor that was not theirs</em>, and a name once entered can be struck out only by a further entry that no one in the barony has the means to buy. The Order's clerk enters Arnal's name on the fourteenth.</p>
          <p>The hearth-priests of the Threefold, for their part, withhold their rites from any house that sells the Son's grain into a grey box, so that a man might cut, and store, and eat, and then bury his mother in silence. In the third week of Jorren Father Guiraut, who has a conscience and a basket of honey-cakes and no instruction that allows him to use either, withholds the burial blessing from Arnal's father, with his sleeve in both hands and his eyes on the ground, as a man draws a tooth of his own. The millet is cut in the end, in the last week of Jorren, in the rain, by whoever has a sickle and no priest, a little better than half of what it was. The manuscript gives Arnal a village, a terrace, two fields, a loft and a father; the sheet's wiry five-foot-seven frame, narrow sun-lined face with a permanent squint, thinning straw-colored hair, pale blue eyes, peeling nose, two days' stubble, missing top joint on the left little finger and patched russet tunic are its own.</p>""",
            },
            {
                "slug": "bernat-the-younger", "name": "Bernat the Younger",
                "epithets": "Farmer of Vilarnau with a field on the south terrace &middot; 50 years old &middot; the eleventh of Iverin",
                "teaser": "Stands an hour at the edge of his ripe field with a sickle, waiting for somebody to tell him whose it is.",
                "bio_html": """<p>A farmer of Vilarnau, a stout man of fifty with a field of his own on the south terrace, who stands at the edge of it on the evening of the eleventh of Iverin with a sickle in his hand and his wife at his elbow, for an hour, and does not cut. When his wife asks him why, he says that he is waiting for somebody to tell him whose it is. It is not an answer, the manuscript says; it is an accounting. Both altars have named a price, and he has worked out, as plainly as any bailiff, that he is being asked to choose between a granary and a grave: the Order will enter his name in the Book if he cuts or carries without receipt, and the hearth-priests of the Threefold will withhold christening, marriage and funeral blessing from any house that sells the Son's grain into a grey box.</p>
          <p>The manuscript does not say what he does when the hour is over, though the millet is cut in the end, in the last week of Jorren, in the rain, by whoever has a sickle and no priest. He is not <a href="../characters/bernat.html">Old Bernat</a>, the reeve who says <em>Fossa</em> on the green and whose page is in Case 2231; the manuscript does not say whether the two are kin, and the pages are kept apart. It gives the Younger his age, his build, his terrace and his hour. The sheet's thick neck, square ruddy heavy-browed face, cropped grey-brown hair, hazel eyes, weathered red-brown skin, grey stubble, swollen knuckles and russet tunic are its own.</p>""",
            },
            {
                "slug": "bernat-the-youngers-wife", "name": "Bernat the Younger's Wife",
                "epithets": "Wife of Bernat the Younger &middot; unnamed &middot; 48 years old by her sheet",
                "teaser": "Stands at her husband's elbow for an hour and asks the only question anyone puts to him.",
                "bio_html": """<p>She stands beside her husband at the edge of the ripe field on the south terrace on the evening of the eleventh of Iverin, and for an hour, while he does not cut, she says nothing that the manuscript records. Then she asks him why. His answer, that he is waiting for somebody to tell him whose it is, is the case in a sentence, and she is the only person in it to whom he gives it. Behind them the millet stands ripening past ripeness through the cold clear weeks of Iverin, because the sickles of the Threefold are blessed and the seals of the Last Order are on the barns, and the sickle in his hand stays idle.</p>
          <p>The manuscript names her only as his wife, gives her no age, and does not say what she says after his answer, nor what the household does. The stakes for her house are the ones it sets out for every house in the barony: the Book on one side, and on the other no christening, no marriage and no funeral blessing. The sheet's forty-eight years, sturdy five-foot-three, round anxious face with deep dimples, dark brown hair going grey beneath a linen kerchief, dark brown eyes, chapped reddened hands, brown wool dress and shawl clutched at the throat are its own. Her husband is <a href="../characters/bernat-the-younger.html">Bernat the Younger</a>.</p>""",
            },
            {
                "slug": "sergeant-of-the-levy", "name": "Sergeant of the Levy",
                "epithets": "Sergeant of the Baronies' levy, in the red of the Son &middot; unnamed &middot; 36 years old by his sheet",
                "teaser": "Asks for porridge at the mill in the second autumn, and later goes away without the stranger.",
                "bio_html": """<p>The war reaches the Mill of the Two Weirs in the second autumn, and it comes as a request for porridge, made by a sergeant of the Baronies' levy in the red of the Son, who stands in the kitchen doorway with his helmet under his arm and the expression of a man who has been told that hunger is no excuse and has not been told what is. <a href="../characters/ermengarda.html">Ermengarda</a> gives him a bowl. An hour later she gives one to <a href="../characters/corporal-of-the-order.html">a corporal of the Order</a> in grey, who has come on the same errand by the other road, and sets the two of them at opposite ends of the same bench with the kettle between them; neither man can bring himself to be the first to refuse.</p>
          <p>He has seen the stranger before. The manuscript says that the Baronies' sergeant had stood in the yard on the third of Iverin and knew what he could do with a pair of ash swords, and that the levy came for the stranger twice that winter. When the sergeant finds him in the mill-yard at the slaughter with both blades hung on a nail in the byre and his hands open at his sides, in the posture of a man waiting to be told where to report, he goes away without his name. It does not identify him with <a href="../characters/sicard.html">Sicard</a> of Case 2231, the bailiff's sergeant at Castelmaur, or with any other sergeant in the case. The sheet's thirty-six years, stocky five-foot-eight frame, broad sunburned face, cropped dark hair, brown eyes, stubble, slight limp, short spear and leather jerkin are its own.</p>""",
            },
            {
                "slug": "corporal-of-the-order", "name": "Corporal of the Order",
                "epithets": "Corporal of the Last Order's lay-brothers, in grey &middot; unnamed &middot; 34 years old by his sheet",
                "teaser": "Comes for the stranger a month after the sergeant, and goes away with the same nothing and a second bowl of porridge.",
                "bio_html": """<p>He arrives an hour after the sergeant, by the other road, on the same errand, and <a href="../characters/ermengarda.html">Ermengarda</a> sets him at the opposite end of the same bench, with the kettle between them, on the single principle that a house which fed one altar's soldiers and not the other's would shortly be a house that had chosen, and that nobody had asked her to. It is an older law than the Accord, the manuscript says, and it holds in that kitchen for fifteen months, as the oldest laws hold, because no one can remember who drafted it. He is the Last Order's side of it, a corporal in grey.</p>
          <p>A month after the sergeant, he comes for the stranger on the same errand; the levy has come for him twice that winter, and the stranger keeps a vow of no steel in that house. The manuscript has the corporal go away with the same nothing and a second bowl of porridge. Nothing in it identifies him further. The sheet's thirty-four years, lean five-foot-nine frame with the stoop of long marches, long tired polite face, pale skin, close-cropped brown hair, grey eyes, clean-shaven jaw, sun-in-a-circle badge at the breast, undyed grey wool tunic and worn leather jerkin are its own, and so is its note that he is a lay-brother. <a href="../characters/sergeant-of-the-levy.html">The sergeant of the levy</a> sits at the other end of the bench.</p>""",
            },
            {
                "slug": "goose", "name": "The Goose",
                "epithets": "The yard goose of the Mill of the Two Weirs &middot; 4 years old by its sheet",
                "teaser": "Holds a view of the world that a Provost finds presumptuous, and stands in the gate on two nights when nobody else can.",
                "bio_html": """<p>The mill's yard goose, which has a view of the world that <a href="../characters/ottavio-brandi.html">Ottavio Brandi</a> finds presumptuous. On the night of the first of Iverin, when he walks down the lane to present the Order's roll to a stranger through the mouth of a sixteen-year-old miller's daughter, it is in his way at the gate when he leaves, and he stops; the clerk <a href="../characters/matteo.html">Matteo</a>, waiting by the lantern, says in a low voice that it will be all right, sir. &ldquo;It will be entered,&rdquo; says the Provost, and walks up the lane in the dark. He has been cold since the tenth of Garren, and he does not yet know why.</p>
          <p>On the evening of the second it comes out again, and regards <a href="../characters/bertran-0202.html">Sir Bertran de Lanta</a>, who has come down the lane as far as the gate with the first of his pearwood horses in his fist and no idea how to knock. He stands there for as long as it takes a bell to ring Prime, with the kitchen's lamplight on the gravel at his boots, and goes back up the lane. It takes no side. The manuscript gives it no sex, colour or build. The sheet's four years, large white body with a grey back, flat orange bill, small hard black eyes, orange legs, raised neck and hiss are its own, and its captions, Watchful, Severe, Hissing, Gatekeeper, are the nearest the file comes to its opinion of any of it.</p>""",
            },
            {
                "slug": "elis-mother", "name": "Elis's Mother",
                "epithets": "Mother of Elis &middot; unnamed &middot; Solan's Fire in the thirty-ninth year &middot; 33 years old by her sheet",
                "teaser": "Carves the feast pig, says that nago means a bite to eat, and then tells the one story she never believed.",
                "bio_html": """<p>She is carving the pig. On the twenty-eighth of Havren, in the thirty-ninth year, at the evening feast of Solan's Fire in Vilarnau, her daughter Elis, six, has been given a small dish of roasted nago with salt by her great-grandmother and told that it is the gift of the gods; she eats it, considers the matter, and asks her mother what the word means and whether it has always been the name of the thing. Her mother, who is busy, says that it means a bite to eat, and that it is a funny old word and nobody knows where it came from. The girl says that it is a funny word for a locust. Her mother says that it is a funny sort of locust.</p>
          <p>Then, because the child is still looking at her with the large grave attention of a person who has been given part of an answer and wishes for the rest, she says the one thing she was told by her own mother, who was told it by someone who was told it by a girl called <a href="../characters/gersenda.html">Gersenda</a>, and that she has never believed: that it is a foreign word, given to the valley by a man who once came in from very far away, and was made welcome, and, this being the part that nobody in the family has ever been able to believe, went home. The manuscript gives her a pig, a knife and a daughter. The sheet's thirty-three years, strong five-foot-five build, oval flushed face, dark brown hair under a kerchief, hazel eyes, grease-spattered forearms and linen apron are its own, and so is the line it prints beside her, <em>Nago meant a bite to eat</em>.</p>""",
            },
            {
                "slug": "vara", "name": "Vara",
                "epithets": "The hermit of Val Muta &middot; looks no older than thirty &middot; true age unknown",
                "teaser": "Eats salted river shrimp from a twist of paper, reads a drawing in the dust by the direction of its marks, and agrees.",
                "bio_html": """<p>The people of Val Muta call him Vara, when they call him anything: a hermit in a high green hollow of the hills, in a season when something is in flower, in a shack of his own building at a river bend. He looks no older than thirty and is, by every account, a good deal less in a hurry. He lives beside the river because he likes the river, and eats salted river shrimp out of a twist of paper with the unhurried attention of a man for whom it is the main event of the day. He hears out the whole of the foreigner's account, the Stone, the Law, the hand that signs and a child asleep with her fist closed on a sleeve, in gestures, in the several hundred words of the Lauze dialect that Tomobe no Higaide has to give, and in a drawing in the dust of a road, a bridge, and two stones with a line between them. He reads it as a miller's daughter once read a ditch, not by the shape of the line but by the direction in which the marks are going. He agrees. His reasons are in no file, the manuscript says, since he is not a man who enters things.</p>
          <p>He comes back with the foreigner by the long road, and on an evening in a spring that nobody in the valley has marked as particular he is standing a little apart on the green at Vilarnau, a lean young-looking man eating something out of a twist of paper, while the village comes out and stands in a half-ring forty paces off. When <a href="../characters/gersenda.html">Gersenda</a> has said <em>Two seconds</em> and been answered, he finishes his shrimp, folds the twist of paper into a neat square, and kneels at <a href="../characters/the-kiyote-pair.html">the Stone</a> with a short bent thing from his sleeve that nobody is looking at. What he does takes about as long as a bell takes to ring Prime, and nothing in it is visible; for the length of that dusk the Stone is not one-way. He asks the nearest person which way the river lies and is gone by morning. The manuscript gives him the name, the apparent age, the shrimp and the hollow. The sheet's slim five-foot-ten frame, unlined calm face, pale skin, pale grey eyes, fine white-silver hair, undyed wool jerkin and sheepskin vest are its own.</p>""",
            },
            {
                "slug": "genzo", "name": "Genzō",
                "epithets": "Steward of the Tomobe estate at Himuro &middot; seen only in Higaide's memory, twenty-three years back &middot; 55 years old as remembered, by his sheet",
                "teaser": "Reads the weather in his knees, and digs a trench along the whole eastern bank against the red hoppers.",
                "bio_html": """<p>A stolid grey man who reads the weather in his knees, steward of the Tomobe estate in the last season that Higaide's father held it in good standing, and he appears nowhere but in a memory. Higaide, eleven that summer, calls it up on the night of the twenty-sixth of Garren, at the smell of barley-chaff: the red-backed hoppers coming over the ridge from the dry country in an afternoon, turning the paddies the color of rust and setting the temple bell tolling of its own accord, which is the bell's way in that district of reporting a thing that no one can stop. The steward does not ring it. He puts every able hand in the district, a hundred and sixty men, women and boys, along the paddy dikes, and sets them to dig from the first hour of the afternoon until the last of the light a trench along the whole length of the eastern bank, a man's height deep and two paces wide, with the spoil thrown up on the outer side.</p>
          <p>At dusk, when the hoppers settle in the cold, he sets fires along the lip of it, small fires of damp straw and green brush that give more smoke than flame, with a line of boys with drums and the great clacking wooden rattles of the harvest-dance behind them; in the red dark the hoppers come to the light as moths come, and go down into the trench in tens of thousands, and are covered over with earth in the morning by the same hundred and sixty hands. It is the sending-off, the villagers say, and they burn a straw figure at the boundary stone. Twenty-three years later it is what Higaide draws with a stick on the green at Vilarnau, and the word for it in that country is <em>fossa</em>. After the Turning he bows to a dead grasshopper and eats it, recalling that he ate one once, at twelve, parched in a pan with salt and a little plum vinegar, from Genzō's own hand, in the year the weir was lost. The manuscript gives him two adjectives, a post, a shovel's worth of orders and his knees. The sheet's fifty-five years, square five-foot-three build, broad impassive face, iron-grey topknot, thin grey moustache and faded indigo hemp robe are its own.</p>""",
            },
            {
                "slug": "yo-su", "name": "Yō Sū",
                "epithets": "Minister of the Great Tang &middot; referenced only, three centuries before the case &middot; 60 years old by his sheet",
                "teaser": "Dug pits and lit fires against the locusts, against the whole of his court, and was right.",
                "bio_html": """<p>He is a name in a book. Higaide's father Nariyuki, a scholar in a family of soldiers, borrowed a brittle old book of the continent from the Left Ministry's library for the sake of its binding, and in it read the account of a minister of the Great Tang who faced a plague of locusts three centuries before, against the learned opinion of every scholar at his court, who held that insects were the heavens' business and not to be interfered with by a man; and who dug pits, and lit fires at night, and killed the creatures in their millions, and buried them, and was right. The name of the minister was Yō Sū. Nariyuki pronounced it to his son with a kind of private relish. A man who has read a thing in a book, he said, is permitted to be pleased when it works.</p>
          <p>That is all the manuscript has of him, and it reaches the valley of the Lauze through one boy's memory of holding a torch. Twenty-three years later it is the ditch Higaide draws on the green, and then the one he digs, and on the morning of the twenty-seventh of Havren, standing among the dead below the Dawn Wall, he sets what his father's book was worth against the bulk of the swarm and finds, with the cool clarity of an exact mind, that it is about a fiftieth part. The Log's own reckoning is that the works at the Throat held the swarm in the gorge five point one days longer than an open crossing would have, long enough for the strain to do what it does. He was right, as the minister was right, about the wrong thing. The manuscript gives Yō Sū a name, a country, an office and an act. The sheet's sixty years, medium five-foot-six build with a scholar's stoop, lean stern fair-skinned face, grey hair under a black cap, thin grey beard, dark eyes and dark-red official's robe are its own.</p>""",
            },
        ],
        "scenes": [
            {"slug": "the-news-from-the-south", "title": "The news from the south",
             "alt": "A lean bearded wool-factor in a dust-striped cloak and a plain white cap sits at a plank table in a smoky inn holding a cup of red wine in both hands, a heavy man in a dark green wool gown with a ring of keys at his belt listening across the table with his back half turned to the viewer, drinkers blurred in the smoke behind them, a lit wall sconce at the upper left and a castle on a crag and a domed red roof glimpsed through the open doorway",
             "caption_html": """On the seventeenth of Garren, in the inn below the castle spur, <a href="../characters/ibrahim-ibn-nasr.html">Ibrahim ibn Nasr</a> holds his cup of thin red wine in both hands and tells the bailiff <a href="../characters/arnaut.html">Arnaut</a> a sentence nobody will believe: the Red Weather has come up out of the south."""},
            {"slug": "the-stone-at-mikusa", "title": "The stone at Mikusa",
             "alt": "A tall lean man in a blue-black robe and a tall black cap bends over a waist-high grey granite block with his left palm flat on its top as a stream of pale glittering grain pours off his body and sleeves down frosted stone steps, a rope-hung wooden gate at the upper left, rows of white-robed priests in tall black caps standing on the steps behind him with one hand half raised, tall cedars and misty blue mountains under a pink sunrise",
             "caption_html": """At the grey of dawn on the twentieth of Garren Tomobe no Higaide lays his left palm on <a href="../characters/the-kiyote-pair.html">the Stone</a> of Mikusa, and a pale grain like sand through the neck of a glass pours out of him into it, swords and all, before nine witnesses."""},
            {"slug": "the-bowl-on-the-green", "title": "The bowl on the green",
             "alt": "A tall lean man in a dark robe with a long sword across his knees sits upright on the end of a waist-high grey granite block beneath a great oak at night, a tiny old woman in a black headscarf and long apron crossing the grass toward him with a steaming bowl in both hands, a ragged half-ring of villagers holding rushlights behind her, a small boy with a switch at the right edge, and thatched roofs, a church spire and a thread of woodsmoke below a deep blue sky of stars",
             "caption_html": """On the night of the nineteenth of Garren a tiny old woman with a wooden spoon crosses the green at Vilarnau through the whole watching village and puts a bowl of something warm into the hands of Tomobe no Higaide, seated on <a href="../characters/the-kiyote-pair.html">the Stone</a>; <a href="../characters/smith-of-vilarnau.html">the smith</a> and the rest stand forty paces off."""},
            {"slug": "the-lesson-at-the-mill", "title": "The lesson at the mill",
             "alt": "A young woman with a heavy dark braid and a gap-toothed smile sits on a bench holding up a wooden ladle toward a tall dark-haired man in a brown wool tunic with a dried gourd at his belt who sits with his head bowed and his hands open on his knees, a small tough woman in a white kerchief stirring an iron kettle at a glowing hearth behind them, a small fair boy at her elbow, strings of onions hanging from the beams and a huge rust-red ox looking in at the byre doorway at the back",
             "caption_html": """In the mill kitchen, in his second week in that country, <a href="../characters/gersenda.html">Gersenda</a> holds up a wooden ladle and says the word for it, slowly and flatly, while <a href="../characters/ermengarda.html">Ermengarda</a> stirs the kettle, the ox Lo Rog looks in, and Tomobe no Higaide tries to say it back."""},
            {"slug": "what-the-tavern-knew", "title": "What the tavern knew",
             "alt": "A packed low-ceilinged tavern lit orange by a hearth and candles, a broad laughing woman in a dark bodice and white sleeves at the upper left holding up a mug, a lean bearded man in a white head-cloth and striped cloak at the centre with a cup of red wine glancing aside, a leathery man in a brown cloak holding a small tin disk up between finger and thumb, other drinkers leaning on elbows on benches and barrels, coins and tin cups on the stained table in the foreground and a window of dark blue night at the upper right",
             "caption_html": """On the first of Havren the tavern at Vilarnau holds forty on benches and barrels: <a href="../characters/brunissen.html">Brunissen</a> says somebody has to dig a hole, <a href="../characters/ibrahim-ibn-nasr.html">Ibrahim ibn Nasr</a> has just told the room that in the south they eat the Weather, <a href="../characters/gaucelm.html">Gaucelm</a> sells tin wards, and <a href="../characters/observer-551.html">Observer 551</a>, as a rat-catcher, listens by the door."""},
            {"slug": "the-fire-in-the-ditch", "title": "The fire in the ditch",
             "alt": "Night in a gorge between black cliffs under a few cold stars, terraced lines of trench crossing the slope with long low lines of glowing fire and grey smoke along the lip of each, a river of rust-red grasshoppers pouring down the lit slope into a timber-edged trench in the foreground, a crowd of diggers with spades and sacks bent along the bank, a row of boys in white shirts with raised drums and rattles on the upper terrace, and at the right a lean man in a pale robe with a drawn sword beside a knight in dark mail swinging a burning brand",
             "caption_html": """On the twenty-sixth of Havren, with the line broken in the second rank at the Throat, <a href="../characters/bertran-0202.html">Sir Bertran</a> goes down into the gap with a burning brand and Tomobe no Higaide with a drawn tachi, and the two hold it for the whole of a night."""},
            {"slug": "the-dawn-wall", "title": "The Dawn Wall",
             "alt": "Sunrise in a gorge: a cliff face four hundred feet high covered ledge by ledge with dead red grasshoppers gripping the rock with wings spread, lit gold by the low sun, a bright beam from a great glass lens on a tripod on a plank platform under a grey awning falling on the wall, a dark-robed man and a pale young clerk at the lens, a red-robed man kneeling among kneeling peasants in the gravel, and in the foreground a lean man in a dark robe with a sword held down along his leg holding up one stiff red body beside a young woman with a braid in a white blouse and blue skirt who looks up, the gravel strewn with the dead",
             "caption_html": """On the morning of the twenty-seventh of Havren the Dawn Wall hangs with the dead, and Tomobe no Higaide holds one up and says <em>inago</em> to <a href="../characters/gersenda.html">Gersenda</a>, while <a href="../characters/ottavio-brandi.html">Ottavio Brandi</a> and <a href="../characters/matteo.html">Matteo</a> turn the ground lens on the wall and the Hierarch <a href="../characters/odilo.html">Odilo</a> kneels in the gravel."""},
            {"slug": "the-long-graves", "title": "The long graves",
             "alt": "A snow-covered field behind a Gothic refectory wall on a grey winter morning, a lean man in a mud-stained brown tunic with a sword at his hip bending over a deep sloped trench and paying out a knotted cord along it, grey-habited lay-brothers digging in the black earth beyond, a tall young lay-brother with an open book standing at the margin, a young woman with her arms folded and a flour sack at her hip watching at the right, carts and horses with children sitting on top drawn up along the wall at the upper left, breath fogging, and a cathedral spire on the misty horizon",
             "caption_html": """In the second winter, behind the refectory at Sant-Sever, Tomobe no Higaide lays out the trench for the famine's dead with a knotted cord; <a href="../characters/joan.html">Joan</a> counts the buried at the margin of his page, and <a href="../characters/gersenda.html">Gersenda</a> hears the word said anyway."""},
            {"slug": "the-cairn-on-the-ridge", "title": "The cairn on the ridge",
             "alt": "Autumn rain on a ridge: a long low storehouse of squared logs raised on stout wooden posts with a pegged wooden door stands against a heavy grey sky, three boys and a girl in rain-dark ragged wool carry grey fieldstones to a waist-high cairn in the foreground, wet russet bracken fills the slope, and a shepherd in a hooded cloak leans on a crook beside a dry-stone wall with a dog at his heel at the right, a river valley and a thread of smoke falling away behind them",
             "caption_html": """By the fifth winter the boys of three hamlets are carrying fieldstones up the ridge to raise a waist-high cairn over nobody, beside the log storehouse Tomobe no Higaide built and left pegged shut from the outside; a shepherd watches from the wall."""},
            {"slug": "the-hermit-of-val-muta", "title": "The hermit of Val Muta",
             "alt": "In a green hollow beside a bright river bend under willows, a pale slim man with white hair in an undyed wool jerkin and a sheepskin vest sits on a log outside a log shack eating a shrimp from a paper twist in his lap, a folded square of paper on the ground beside his foot, while a lean grey-templed man in a brown tunic with two swords at his hip kneels in the dust and draws with one finger a winding road, a bridge and two small stones with a line between them, wildflowers in the grass and a wicker basket and a pole against the shack",
             "caption_html": """In a green hollow of Val Muta the hermit <a href="../characters/vara.html">Vara</a> eats salted river shrimp from a twist of paper while Tomobe no Higaide kneels in the dust and draws a road, a bridge and two stones with a line between them; the hermit agrees."""},
        ],
    },
]

LORE = [
    {
        "slug": "cultivator", "name": "Cultivator", "roster": "envoy",
        "teaser": "The observers who deliver Catalysts to chosen subjects across worlds.",
        "definition_html": """<p>A loose, still-forming collective of offices and field agents &mdash; simply &ldquo;observers&rdquo; in the earliest records &mdash; who select subjects across many worlds and deliver a Catalyst directly into their hands, then spend the rest of that subject's life quietly filing reports on what the world does with it. The name &ldquo;Cultivator&rdquo; wasn't settled on until long after the practice began.</p>
          <p>Their field agents are called Envoys, or Observers. Nearly every case has its own, and &mdash; with a single exception on file, an Envoy posted to two cases in succession &mdash; no two are the same person: each works through a numbered &ldquo;deployment archetype&rdquo; and a disguise suited to the world they enter &mdash; a woman on a hilltop, a traveling confectioner, an ordinary old man at the bottom of a hole, a wandering hermit, an ascetic kneeling at a drainage ditch, a court astronomer-priest who keeps a kingdom's calendar from a tower, a shipwreck survivor who has kept the same flooded ruin for a hundred and forty years. Every Envoy on file is listed below.</p>
          <p>Not every case resolves within a single lifetime: in at least one instance on file, a Catalyst sat untouched in one family's keeping for four centuries before its case ever closed, and the Envoy assigned to it counts eleven centuries of comparable postings behind him. Redundancy is standard practice on others: one Envoy's own field notes cite several thousand comparable seedings, on the reasoning that a single object left in open ground is recovered by its intended finder only slightly more often than it's carried off by a flood, a jackdaw, or a passing child who simply wants it for its color. One Envoy on file sells her entire remaining stock to a single buyer in an ordinary afternoon of trade and is three postings distant before anyone drinks what she sold them. Another looks like a child of twelve, has not aged in four generations, and is forbidden by protocol to do anything about what she logs. A third is recalled from a tower parapet on the one evening he exceeds his instructions, and leaves a lamp burning behind him. Another, a mute stonecutter, dresses both ends of a matched pair of stones, spends thirty-one years as a quarry-hand beside the one that receives, and is asked, in notches drawn in the dust, the one question he may not answer. Another, a rat-catcher with a bait-spoon, breaks open a single clay pot in the broom-scrub of a mountain pass, files three notes, sells nothing, and passes that stonecutter on a quarry road with an exact courtesy. Another, a shrine-keeper whose watch the valley below cannot date, sits beside a spring that copies one man's whole life into the next to drink, and says the same two words to the master who comes to die at it and to the disciple who comes looking for what he left. And one, a clockmaker in two successive postings, goes on watching his second subject from a rented room two valleys away for eighteen years after the posting has formally ended. One case has none posted in person at all: a network of probes does the delivering, and an analytical office, not a field agent, files the closing log.</p>""",
    },
    {
        "slug": "catalyst", "name": "Catalyst", "roster": "catalyst",
        "teaser": "The single object at the center of every case.",
        "definition_html": """<p>The one object a Cultivator puts into a society to see what the society does with it. A Catalyst is rarely dangerous in itself &mdash; a jar of candy, a pair of shoes, a sword no one else can lift, a hole in a hillside, a flask that never lets its contents go cold, a traffic cone, an eight-foot electric eel &mdash; and it arrives with no explanation and no instructions. What matters is everything that happens after: the miracle someone declares, the heresy someone else does, the pride that takes offense, and the office that quietly writes it all down.</p>
          <p>Each Catalyst belongs to one case, is placed by one Envoy, and is filed under a number and a class of its own. Some are handed to one person, some are slipped into a court, and one is a hundred-level structure left in a hillside for someone to find, and one is a living animal, released into a flooded ruin and left to be found. Redundancy is standard on some cases: one Catalyst was seeded three times over in the same ditch, so that a single unit lost to a flood or an incurious passerby wouldn't end the case before it began. One Catalyst on file grants nothing but another creature's own perception, on loan for a quarter of an hour at a time, and is never once used by the same hand twice. Another is a buried chamber that rebuilds whatever enters it, exact in everything that can be measured. Another, left beneath a threshing-floor, cuts a circle of clear noon with a ruler's edge out of a sky of ash and holds it open for four hundred and twenty-one days. Another is a pair of stones, one in a shrine and one on a village green, that carries whoever lays a bare palm on the first to the second, and no one ever back. Another is a banded fungus, broken open from one sealed clay pot ahead of a migrating swarm, that turns every animal it takes toward the sun and leaves four hundred feet of cliff hung with the dead. Another is a mountain spring, fed by nothing and drained by nothing, that copies the whole memory and skill of the last person to touch it into the next person who drinks, and overwrites itself each time. Another is a prosthetic left hand with eleven fingers, grafted onto a prince over three nights, that a kingdom spends eighteen years deciding is not a hand at all. Another is not an object but a network: a field of dormant probes in the high air over a kingdom that, on a schedule fixed before they were seeded, lets one village at a time sleep its way up to see the shape of its own world, and gives nothing else. Every Catalyst on file is listed below.</p>""",
    },
    {
        "slug": "faith-of-ardwen", "name": "The Faith of Ardwen", "group": "Religion",
        "teaser": "A monotheism built on waiting, honest prayer, and a sword no one else can lift.",
        "definition_html": """<p>A monotheism built around a single historical miracle: an honest prayer, answered from the sky. Ardwen &mdash; the Unhastening, the Sky-Answered &mdash; is worshipped as the one eternal goddess, without rival, consort, or divine family, and asks less of her followers than most faiths do: wait, ask honestly, keep your promises, and act responsibly without pretending to know a god's mind for her. Her clergy are careful to distinguish what is known from what is merely mysterious, and the faith's own maxim is built to resist any shortcut: <em>Ardwen answers the honest, but never on command.</em></p>
          <p>Her institutional church, the Vigil of Ardwen, is led by a First Keeper and organized into regional Houses of Vigil, with confession, baptism, marriage, funerals, and pilgrimage among its sacred rites. The faith reveres its founding miracle &mdash; and the sword that came with it &mdash; as a sacred sign of that day, never as a rival object of worship. Whatever else it is, Valeria is not a god.</p>""",
        "appears_html": """<p>The founding faith of <a href="../books/0000.html">The Sword of Valeria</a>, where the goddess herself and the relic she left behind both have entries of their own: <a href="../characters/ardwen.html">Ardwen</a> and <a href="../characters/valeria.html">Valeria</a>. Generations later, in <a href="../books/0157.html">The Stolen Prince War</a>, the Vigil's doctrine of unearned, uncommandable grace is tested to its limit by a dungeon that answers the same chest the same way every single time &mdash; a contradiction its own Keeper, <a href="../characters/yudith.html">Yudith</a>, spends eleven years trying to preach around. In <a href="../books/0156.html">The Purging of Charsianon</a>, a Byzantine-styled river valley keeps the Vigil in a plain House of stone and candles, and a Keeper of the Dorylaion Vigil turns a name for a strange calm &mdash; the Doctrine of the Stolen Vessel &mdash; into an army. In <a href="../books/1153.html">The Second Hand</a>, a hidden mountain fold called Otsane keeps the Vigil in a plain house with no cathedral, where its Keeper, <a href="../characters/amets.html">Amets</a>, gives an exile a new name and an open door, and the cathedral at Ardenwake turns a distant rumor into a question about <a href="../characters/anchorite-of-ardenwake.html">the Anchorite</a>, <a href="../characters/the-founding-wielder.html">the founding wielder</a> and a sword no one else can lift. And in <a href="../books/1268.html">Independent Observation</a>, a single unaffiliated anchorite of the Vigil, <a href="../characters/anchorite-of-ardwen.html">the Anchorite of Ardwen</a>, walks from burning to burning through a Threefold kingdom that files her faith among the empty crowns, asks the silence beyond the heavens to let her come, and takes the silence that meets her as an answer, which is the only kind Ardwen gives: never on command. And in <a href="../books/0202.html">Fossa</a>, the Keeper <a href="../characters/alazais.html">Alazaïs</a> of the House of Vigil at Sant-Sever, asked which of the other two altars the realm owes its deliverance, says only &ldquo;I do not know,&rdquo; sends six hundred hands to dig, and feeds the families of both sides when the war comes.</p>""",
    },
    {
        "slug": "threefold-crown", "name": "The Threefold Crown", "group": "Religion",
        "teaser": "Three gods, or one god wearing three faces &mdash; the Crown has never resolved which.",
        "definition_html": """<p>An old pagan faith built around three supreme gods who may, or may not, be one god wearing three faces &mdash; a contradiction its own believers call the Threefold Mystery and have never been in any hurry to resolve. <strong>Auron</strong> the Father governs heaven, law, kingship, judgment, and oaths; <strong>Elara</strong> the Mother governs earth, birth, fertility, harvest, and hearth; <strong>Solan</strong> the Son governs the sun, fire, youth, passion, and sacrifice. A believer may favor one god over the other two without ever quite denying that all three are, somehow, the same throne. The formula recited at its temples leaves the contradiction standing on purpose: <em>Father above. Mother beneath. Son beside us. Three crowns. One Heaven.</em></p>
          <p>Ritual-heavy and elaborately hierarchical, with wine treated as sacred and pork freely eaten, the Threefold Crown holds that its own throne is the one true one &mdash; a claim that makes its temple politics every bit as susceptible to ambition as any earthly court, and its priesthood just as capable of turning a private grief, or a private embezzlement, into doctrine.</p>""",
        "appears_html": """<p>Vantashen's state religion in <a href="../books/0157.html">The Stolen Prince War</a>, where Hierarch <a href="../characters/doreth.html">Doreth</a> turns a private grief into a war he tells himself is a monument, and the guardian at Level 40 is known to delvers as <a href="../characters/the-ember-judge.html">the Trial of Solan</a>. In <a href="../books/4417.html">The Iron Stiletto War</a>, the Order of the Pale Cloth's High Cleric <a href="../characters/ambrose.html">Ambrose</a> declares a pair of shoes heretical on the Crown's own authority. In <a href="../books/2140.html">The Third Grain</a>, a legal claim over a county mill is argued and won entirely inside the Crown's own law, under a courtroom ceiling painted with <a href="../characters/eldest-witness-of-the-writ.html">a judge</a> who has spent thirty years complaining that Auron's three scales were never painted quite level. And in <a href="../books/2231.html">The Stone of the Clean Hand</a>, a hearth-priest's honest report of a stranger's bow to Solan's Fire and refusal of the feast-pig reaches Hierarch <a href="../characters/odilo.html">Odilo</a> at Castelmaur, who lays the temple's interdict on a whole lane until its idol is cast down. And in <a href="../books/1153.html">The Second Hand</a>, the kingdom of Sarkveti keeps the Crown as its faith the way it keeps its terraces, and Hierarch <a href="../characters/demna.html">Demna</a> of Auron's temple in Tavgora rules, on <a href="../characters/the-doctrine-of-the-unbroken-hand.html">the Doctrine of the Unbroken Hand</a>, that a prince's grafted hand is not his own. And in <a href="../books/1268.html">Independent Observation</a>, the Crown is Aldemark's actual government, its Triarchs <a href="../characters/ansovald.html">Ansovald</a>, <a href="../characters/adaltrude.html">Adaltrude</a> and <a href="../characters/sigward.html">Sigward</a> holding the seats of Auron, Elara and Solan, until a decade of dreams of a round world, and an eleventh selection that falls on their own capital, leave them three answers to one fact and the Crown a faith rather than a government. And in <a href="../books/0202.html">Fossa</a>, the kingdom of Auvarre keeps the Threefold Crown at its temple of Auron in Castelmaur, where Hierarch <a href="../characters/odilo.html">Odilo</a> weeps sincerely at every response, declares <a href="../characters/the-accord-of-montclar.html">the Accord of Montclar</a> void on the fifth of Iverin, and is believed by eleven of the realm's seventeen barons.</p>""",
    },
    {
        "slug": "decree-of-luminescence", "name": "The Decree of Luminescence", "group": "Religion",
        "teaser": "A theology of measured light: what is favored is lit, and what is lit has been favored.",
        "definition_html": """<p>The youngest of the faiths on file, promulgated after a kingdom-threatening catastrophe: years of ash-blotted sky broken, at the exact point of famine, by a single standing column of true daylight over the capital. <strong>Sol-Invictus, the Unconquered Sun,</strong> is worshipped as the one eternal, lending light, and its doctrine is unusually literal for a religion: light is not read as a sign of favor, it <em>is</em> favor, measured out to every soul at birth as a store of borrowed fire and returned, spent or unspent, at death. It is a creditor's theology at bottom, and its own clergy don't pretend otherwise. The doctrine's core article states the idea plainly: <em>Whatever was favored was lit, and whatever was lit had been favored.</em></p>
          <p>Its church, the Last Order, is led by a High Pontiff and keeps its own doctrine correctable only by further entry, never by erasure. A claimant to real favor stands before a lens that concentrates true daylight onto them, to see whether they visibly glow; a crown is carried through open flame, to see whether the gold endures. What three centuries of both tests have never quite worked out is how to tell light that's generated from light that's merely, cleverly, reflected.</p>""",
        "appears_html": """<p>Its founding is the subject of <a href="../books/2365.html">The Decree of Luminescence</a>. Three centuries on, in <a href="../books/4555.html">The Vessel of Unmediated Grace</a>, where King <a href="../characters/aethelgard.html">Aethelgard</a>'s death without an heir turns the succession into a lit competition, High Pontiff <a href="../characters/sarel.html">Sarel</a> presides over the Grand Basilica's Great Judgment, and a peddler named <a href="../characters/fenn.html">Fenn</a> makes an honest living selling pilgrims small shards of warmed river quartz as splinters of the crown. The <a href="../characters/anchorite-of-the-drowned-road.html">Anchorite of the Drowned Road</a> sect keeps its own small, tolerated counter-doctrine on the Sun's behalf, practicing His absence rather than His favor. The kingdom's map, drawn under both its names, is filed as the <a href="illumaria.html">Gazetteer of Illumaria</a>. In <a href="../books/0202.html">Fossa</a>, the Decree's Last Order sits in the realm of Auvarre as the second altar of the Accord of Montclar: its Provost-Examiner <a href="../characters/ottavio-brandi.html">Ottavio Brandi</a> turns a ground lens on a cliff of dead grasshoppers, writes &ldquo;Lit&rdquo; in the Book, and spends the rest of his life putting the date, the weather and the name of the town at the head of every document that leaves his hand; the charter that calls it to the table is <a href="../characters/the-accord-of-montclar.html">the Accord of Montclar</a>.</p>""",
    },
    {
        "slug": "illumaria", "name": "Gazetteer of Illumaria", "group": "Gazetteers",
        "teaser": "One kingdom under two names: the map of Vallombra at its founding, and of Illumaria long after.",
        "map": {
            "file": "illumaria",
            "alt": "Parchment map titled Illumaria. A long kingdom labelled Vallombra, Illumaria runs south along a river from mountains and the Saltway Gate to a harbour at the Weirs, with the Torrecalda keep, the Grand Basilica of Sol-Invictus, Mud-Reach marsh and Illmere Ford marked; the March of Verrenhal lies to the north-west, Ashduct hills to the east, unknown lands at the margins and a sea with a ship and serpent to the south",
        },
        "definition_html": """<p>A map of a single kingdom at two moments. <a href="../books/2365.html">Case 2365</a> knows it as Vallombra, in the years of ash when its kings and its Reckoner found a religion; <a href="../books/4555.html">Case 4555</a> knows it as Illumaria, long after, when the religion has a Basilica, a High Pontiff and a succession to settle. The map prints both names together, as <em>Vallombra / Illumaria</em>, and sets the March of Verrenhal beside it to the north-west.</p>
          <p>It is filed here as a gazetteer, not as a subject or a record. The places below are the ones printed on the map, from north to south; each note is drawn from the case files, and a place that no case file yet describes is said to be unfiled rather than guessed at.</p>""",
        "places": [
            ("Unknown Lands", """Printed along the map's northern, western and eastern margins. No case file describes them."""),
            ("March of Verrenhal", """The northern realm of <a href="../characters/ragnvald.html">King Ragnvald</a> and his sister <a href="../characters/sigrid.html">Sigrid</a> in Case 2365, who rules it as regent for eleven years after him. Its host comes down a mountain pass into Vallombra in the ash. The map files it as a March."""),
            ("Saltway Gate", """The northern gate on the Saltway, where <a href="../characters/rufio.html">Rufio</a>'s wardens turn back the people whose names cannot be found, where <a href="../characters/arne.html">Arne</a>'s four thousand are met at the low hour, and where <a href="../characters/sigrid.html">Sigrid</a> finds a row of a hundred and forty-one dead with their feet toward the gold. <a href="../records/the-parley-at-the-saltway-gate.html">The parley</a> is held here."""),
            ("Saltway Quarter", """A parish of the Roll of the Lit. It is the column of three hundred and eleven names that the copyist <a href="../characters/lino.html">Lino</a> skips when his wick gutters, and the quarter to which <a href="../characters/livia.html">Livia</a> sends forty wagons of grain, unlabelled, on the anniversary of the First Furrow for fifty-one years."""),
            ("Ashduct", """The hills in the east. When they breathe and the sun withdraws, <a href="../characters/severin.html">Severin</a> extends the year's grace in Case 2365 from three days to a season."""),
            ("Vallombra / Illumaria", """The kingdom itself. In Case 2365 it is Vallombra, the realm of <a href="../characters/faustin.html">King Faustin</a> and then his daughter <a href="../characters/livia.html">Livia</a>, Princess of Vallombra and later Queen of Illumaria. In Case 4555 it is Illumaria, the High Realm of <a href="../characters/aethelgard.html">King Aethelgard</a> and, in time, of <a href="../characters/blakk.html">High Sovereign Blakk</a>."""),
            ("Torrecalda", """The walled city on the river, drawn with a keep. In Case 2365 it is where the Granary's physician tells <a href="../characters/faustin.html">Faustin</a> that no room is large enough to keep the sick from the well, and the city whose tanning trade <a href="../characters/the-tanners-widow.html">the Tanner's Widow</a> belongs to."""),
            ("Lower Granaries", """The grain-houses below Torrecalda. <a href="../characters/nina.html">Nina</a>, Piero's sister, is the daughter of the Lower Granary clerk and dies in the granary house in the first winter of the ash."""),
            ("Threshing Round", """The Round, where the First Furrow is turned. The Reckoner's tower stands beside it; <a href="../characters/livia.html">Livia</a> is crowned there at nine; and it is the ground on which the sun stands at the sixth hour when <a href="../characters/severin.html">Severin</a> states his one false figure."""),
            ("Grand Basilica of Sol-Invictus", """The seat of the religion the first case founds. In Case 2365 a lens the diameter of a cartwheel is ground to catch the single shaft of sun through its oculus; in Case 4555 the Great Judgment is held here under High Pontiff <a href="../characters/sarel.html">Sarel</a>, and <a href="../characters/observer-902.html">Observer 902</a> watches from an alcove in its black stone."""),
            ("Tanners' Row", """Marked on the map; no case file describes it yet."""),
            ("Wool Lane", """A column on the Roll of the Lit: the next one <a href="../characters/lino.html">Lino</a> copies after the Saltway Quarter."""),
            ("Glassmakers' Row", """The street of <a href="../characters/anselmo.html">Anselmo</a>, master of the guild that grinds the Sol-Focus Arc by hand for eleven years."""),
            ("Furrow reserve", """Marked on the map; no case file describes it yet."""),
            ("Round-bed", """Marked on the map; no case file describes it yet."""),
            ("Mud-Reach", """<a href="../characters/blakk.html">Blakk</a>'s duchy in Case 4555: nine hundred square miles of drained marsh, standing timber and tenant debt."""),
            ("Illmere Ford", """The Standing at Illmere Ford, the engagement that follows <a href="../characters/blakk.html">Blakk</a>'s unread letters of surrender. <a href="../characters/astraea.html">Astraea</a>'s cavalry meets <a href="../characters/ignis.html">Ignis</a>'s raiding column here, and <a href="../characters/cassian.html">Cassian</a> arrives on the fifth day to find no one left worth conquering."""),
            ("Sarn's Crossing", """Where <a href="../characters/astraea.html">Astraea</a> throws herself between <a href="../characters/blakk.html">Blakk</a> and Canon Voss's blade, taking a wound that troubles her for the rest of her life."""),
            ("Weirs", """The harbour at the river's mouth. Lord <a href="../characters/fulvio.html">Fulvio</a> of the Weirs, one of the sixteen lords of Vallombra, offers his grain-ships in Case 2365 as the Order's sole licensed factor for whatever is built on the strength of the noon."""),
        ],
        "appears_html": """<p>Vallombra, at the founding of its religion, is the kingdom of <a href="../books/2365.html">The Decree of Luminescence</a> (Case 2365). The same kingdom, long after and under the name Illumaria, is the kingdom of <a href="../books/4555.html">The Vessel of Unmediated Grace</a> (Case 4555). Their shared faith is <a href="decree-of-luminescence.html">the Decree of Luminescence</a>.</p>""",
    },
    {
        "slug": "iron-stiletto-war", "name": "Gazetteer of the Iron Stiletto War", "group": "Gazetteers",
        "teaser": "The map of Case 4417: Solis, Ironhold, and the country between them.",
        "map": {
            "file": "iron-stiletto-war",
            "alt": "Parchment map titled The Iron Stiletto War, Gazetteer. The coastal kingdom of Solis, with a castle and Great Hall on the Greywater river, lies south-west; the mountain country of Ironhold lies north-east, with House Vell's keep on the forest line between them; the Stonewic Hills lie to the south, the eastern marches to the east, and a sea with ships lies to the west",
        },
        "definition_html": """<p>The country of <a href="../books/4417.html">Case 4417</a>, drawn from the sea inland: Solis on the coast, Ironhold in the mountains to the north-east, and the forest line and the river between them. It is filed here as a gazetteer, not as a subject or a record. The places below are the ones printed on the map; each note is drawn from the case file, and a place the file never mentions is said to be unfiled rather than guessed at.</p>""",
        "places": [
            ("Unknown Lands", """Printed along the map's northern and southern margins. No case file describes them."""),
            ("House Vell", """Shown as a keep north of Solis. House Vell commits to Solis in secret, and its Lord is the brother of <a href="../characters/isolde.html">Isolde</a> of Ironhold, a connection that matters more to the war than she first realizes."""),
            ("Ironhold", """The mountain country of Duke <a href="../characters/aldous.html">Aldous</a> and Duchess <a href="../characters/beatrice.html">Beatrice</a>, whose steward <a href="../characters/osric.html">Osric</a> has kept its accounts for three dukes and whose Lord of the Western Passes is <a href="../characters/fenric.html">Fenric</a>. Beatrice's humiliation at the Great Concord is the war's original grievance."""),
            ("Solis", """The coastal kingdom of Queen <a href="../characters/aurelia.html">Aurelia</a>, where <a href="../characters/vane.html">Vane</a> arrives disguised as a wandering hermit and leaves a pair of chrome heels, and where Chancellor <a href="../characters/wren.html">Wren</a> has served three monarchs. The siege reaches its walls at the war's end."""),
            ("Great Hall", """Shown beneath Solis's castle. Duke <a href="../characters/aldous.html">Aldous</a> goes into the war's final confrontation here unarmed and offering terms, and is killed in it."""),
            ("Greywater", """The river that runs west to the sea below Solis's castle. No case file names it."""),
            ("The Greywater crossing", """Marked with a cross on the river's course. No case file describes it."""),
            ("Stonewic Hills", """The hills in the south. No case file describes them."""),
            ("The eastern marches", """The country of <a href="../characters/corvin.html">Baron Corvin</a>, Baron of the Eastern Marches, patient and outwardly neutral while he works every side of the war he helps prolong."""),
        ],
        "appears_html": """<p>The country of <a href="../books/4417.html">The Iron Stiletto War</a> (Case 4417).</p>""",
    },
    {
        "slug": "vessel-of-the-betrayed-host", "name": "Gazetteer of the Vessel of the Betrayed Host", "group": "Gazetteers",
        "teaser": "The map of Case 4420: Mount Skahr and House Skarth in the far north, the Broken Glacier, and the marches that run south to Sumne.",
        "map": {
            "file": "vessel-of-the-betrayed-host",
            "alt": "Parchment map of a northern country. Mount Skahr rises at the top above a gorge of broken ice; House Skarth's castle lies to its west on the tundra, with House Varga and House Tolvin to the south-west and the keep of Kettish to the east; the Broken Glacier and the ice line lie in the east; Cindale, a ring of small marks, stands at the centre; the walled town of Thornfield lies to the south-east and Sumne, with a castle on a hill, in the south; the western, northern and southern marches and the lowlands are marked around them",
        },
        "definition_html": """<p>The country of <a href="../books/4420.html">Case 4420</a>, drawn from Mount Skahr in the far north southward: House Skarth beneath the mountain, the Broken Glacier and the ice line, and the marches that run on to Sumne and the lowlands. It is filed here as a gazetteer, not as a subject or a record. The places below are the ones printed on the map; each note is drawn from the case file, and a place the file never mentions is said to be unfiled rather than guessed at.</p>""",
        "places": [
            ("Mount Skahr", """The mountain at the head of the map. House Skarth's legend says its steel flask came down from the dragon who keeps the mountain. <a href="../characters/observer-4420.html">Observer 814</a> came down onto its summit in a black, wingless vessel some four centuries before the war and was folded by the clans into that keeper, the Dragon-Speaker. <a href="../characters/yvaine.html">Yvaine</a> climbs it to ask him for a blessing."""),
            ("House Skarth", """Shown as a castle west of the mountain gorge. The house of Baron <a href="../characters/kaelen.html">Kaelen</a> and his twin <a href="../characters/yvaine.html">Yvaine</a>, which has carried one steel flask for four centuries without asking where it came from."""),
            ("Kettish", """Drawn as a small keep at the eastern edge of the mountains. Marked on the map; no case file describes it yet."""),
            ("House Varga", """Drawn as a keep in the western tundra. Marked on the map; no case file describes it yet."""),
            ("House Tolvin", """Drawn as a keep beside House Varga. Marked on the map; no case file describes it yet."""),
            ("Broken Glacier", """The ice east of the mountain. Duke <a href="../characters/maros.html">Maros</a>'s hunt reaches it in the northern winter, and by the fourth week it has cost him every toe on both feet. See the record <a href="../records/the-broken-glacier.html">The Broken Glacier</a>."""),
            ("Cindale", """Drawn as a ring of small marks at the centre of the map. A frightened border holdfast that <a href="../characters/yvaine.html">Yvaine</a> spares on her march south."""),
            ("Thornfield", """Drawn as a walled town in the south-east. Marked on the map; no case file describes it yet."""),
            ("Sumne", """Printed in large letters across the southern country, with a castle on a hill below. The case file says only that <a href="../characters/soren.html">Soren</a>, after delivering the recovered flask to <a href="../characters/vane-4420.html">Duke Vane</a>, leaves Sumne within the month."""),
            ("The tundra", """Printed across the north-west. Duke <a href="../characters/maros.html">Maros</a> drags a royal hunt two hundred miles into the northern tundra to answer a stag's head, and Baron <a href="../characters/kaelen.html">Kaelen</a> joins it on guest-right alone."""),
            ("The ice line", """Printed across the glacier country in the east. The northern clans mark their dead along it with <a href="../records/the-black-fletched-arrow.html">black-fletched arrows</a>."""),
            ("The northern marches", """The country of Duke <a href="../characters/maros.html">Maros</a>, Duke of the Northern March and Lord of Karhold Keep. <a href="../characters/yvaine.html">Yvaine</a> ends the war in the hall of his captured keep, where she finds Vane. The map does not mark the keep by name."""),
            ("The western march", """Marked on the map; no case file describes it yet."""),
            ("The southern marches", """The country of <a href="../characters/vane-4420.html">Duke Vane</a>, Duke of the Southern March and Lord of Vane Keep, who wounds Maros with a summer-killed stag's head and then sells him his rescue. The map does not mark the keep by name."""),
            ("The lowlands", """Marked on the map; no case file describes it yet."""),
        ],
        "appears_html": """<p>The country of <a href="../books/4420.html">The Vessel of the Betrayed Host</a> (Case 4420).</p>""",
    },
]

BIOGRAPHY_PARAGRAPHS = [
    "Dzulfaraaghaini is a writer of speculative fiction concerned with the fragility of human systems.",
    "His novels explore the rise and collapse of kingdoms, the evolution of faiths, and the unintended "
    "consequences of ordinary objects placed in extraordinary circumstances. Rather than focusing on heroes "
    "and villains, his work examines the institutions, beliefs, and social structures that govern entire "
    "societies\u2014and the small moments of pride, fear, vanity, or misunderstanding that can bring those "
    "structures down.",
    "He is particularly interested in the relationship between history and memory: the gap between events "
    "as they occurred, and the stories later generations tell about them.",
]


import time as _t
ASSET_V = _t.strftime("%Y%m%d%H%M")  # cache-buster: changes every build


def rel(depth):
    return "../" * depth


def nav_html(active_file, depth):
    items = []
    for href, label in NAV:
        target = (rel(depth) + href) if depth else href
        current = " aria-current=\"page\"" if href == active_file else ""
        items.append("<li><a href=\"%s\"%s>%s</a></li>" % (target, current, label))
    return "\n          ".join(items)


import struct as _struct
from html import unescape as _unesc

# Every page registered through page() lands here; sitemap.xml is written from it.
SITEMAP_PATHS = []


def plain(html_text):
    """Tags stripped, entities decoded, whitespace collapsed: safe to reuse as share text."""
    return re.sub(r"\s+", " ", _unesc(re.sub(r"<[^>]+>", "", html_text or ""))).strip()


def attr(text):
    """Escape text for use inside a double-quoted HTML attribute."""
    return _esc(plain(text), quote=True)


def abs_url(path):
    """Absolute live URL for a site-relative path ('' or 'index.html' is the site root)."""
    if path in ("", "index.html"):
        return SITE_URL
    return SITE_URL + path


def jpeg_size(rel_path):
    """(width, height) of a JPEG under the project root, read from its header; None if unreadable."""
    try:
        with open(os.path.join(OUT, rel_path), "rb") as f:
            f.read(2)
            while True:
                b = f.read(1)
                while b and b != b"\xff":
                    b = f.read(1)
                while b == b"\xff":
                    b = f.read(1)
                if not b:
                    return None
                m = b[0]
                if 0xC0 <= m <= 0xCF and m not in (0xC4, 0xC8, 0xCC):
                    f.read(3)
                    h, w = _struct.unpack(">HH", f.read(4))
                    return w, h
                ln = _struct.unpack(">H", f.read(2))[0]
                f.read(ln - 2)
    except (OSError, _struct.error):
        return None


def share_image(prefix, original):
    """Square link-preview version of a cover or map (made by tools/make_share_images.py, it
    shows the whole picture instead of a slice cut from the middle of a tall one), or the
    original art itself if that file has not been made yet."""
    candidate = "images/share/%s-%s" % (prefix, os.path.basename(original))
    return candidate if os.path.isfile(os.path.join(OUT, candidate)) else original


def head_html(title, description, depth, path=None, image=None, image_alt=None, og_type="website"):
    r = rel(depth)
    seo = ""
    if path is not None:
        img = image if image and os.path.isfile(os.path.join(OUT, image)) else DEFAULT_OG_IMAGE
        alt = image_alt if (image and img == image and image_alt) else DEFAULT_OG_ALT
        size = jpeg_size(img)
        # The art here is portrait, so a large-image card would be cropped hard: only
        # use it for images at least 1.5x wider than tall.
        card = "summary_large_image" if size and size[0] >= 1.5 * size[1] else "summary"
        url = abs_url(path)
        og_title = attr(title)
        og_desc = attr(description)
        seo = """
  <link rel="canonical" href="%(url)s">
  <meta property="og:site_name" content="%(site)s">
  <meta property="og:type" content="%(type)s">
  <meta property="og:title" content="%(title)s">
  <meta property="og:description" content="%(desc)s">
  <meta property="og:url" content="%(url)s">
  <meta property="og:locale" content="en_US">
  <meta property="og:image" content="%(img)s">%(dims)s
  <meta property="og:image:alt" content="%(alt)s">
  <meta name="twitter:card" content="%(card)s">
  <meta name="twitter:title" content="%(title)s">
  <meta name="twitter:description" content="%(desc)s">
  <meta name="twitter:image" content="%(img)s">
  <meta name="twitter:image:alt" content="%(alt)s">""" % {
            "url": url, "site": attr(AUTHOR), "type": og_type, "title": og_title, "desc": og_desc,
            "img": abs_url(img), "alt": attr(alt), "card": card,
            "dims": ('\n  <meta property="og:image:width" content="%d">\n  <meta property="og:image:height" content="%d">' % size) if size else "",
        }
    return """  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>%s</title>
  <meta name="description" content="%s">
  <meta name="robots" content="noimageindex">%s
  <link rel="icon" href="%sassets/favicon.svg" type="image/svg+xml">
  <link rel="alternate icon" href="%sassets/favicon.ico">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;1,400&family=Playfair+Display:ital,wght@0,400;0,500;1,400&family=Source+Code+Pro:wght@400&display=swap">
  <link rel="stylesheet" href="%scss/style.css?v=%s">""" % (title, attr(description), seo, r, r, r, ASSET_V)


def header_html(active_file, depth):
    r = rel(depth)
    home = (r + "index.html") if depth else "index.html"
    return """  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="header-inner wrap">
      <a class="site-title" href="%s"><img class="mark" src="%sassets/logo-gold-sm.png" alt="" width="85" height="112">%s</a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Menu"><span></span><span></span><span></span></button>
      <nav class="site-nav" id="site-nav" aria-label="Main">
        <ul>
          %s
        </ul>
      </nav>
    </div>
  </header>""" % (home, r, AUTHOR, nav_html(active_file, depth))


def footer_html(depth):
    r = rel(depth)
    contact = (r + "contact.html") if depth else "contact.html"
    socials = "".join('\n        <li><a href="%s" target="_blank" rel="noopener">%s</a></li>' % (u, label) for label, _t, u in SOCIALS)
    return ("""  <footer class="site-footer">
    <p class="footer-quote">Not all stories are meant to be forgotten. Some are kept, for a reason.</p>
    <div class="footer-inner wrap">
      <p>&copy; 2026 %s</p>
      <ul class="footer-links">
        <li><a href="%s">Contact</a></li>@@SOCIALS@@
      </ul>
    </div>
    <p class="build-info wrap">Site last built %s</p>
  </footer>
  <script src="%sjs/site.js?v=%s" defer></script>""" % (AUTHOR, contact, BUILD_TIME, r, ASSET_V)).replace("@@SOCIALS@@", socials)


def page(title, description, depth, active_file, body, path=None, image=None, image_alt=None, og_type="website"):
    """`path` is the page's own site-relative file name; passing it turns on the canonical
    link, the Open Graph / Twitter tags and the sitemap entry for the page."""
    if path is not None:
        SITEMAP_PATHS.append(path)
    return """<!DOCTYPE html>
<html lang="en">
<head>
%s
</head>
<body>
%s
  <main id="main">
%s
  </main>
%s
</body>
</html>
""" % (head_html(title, description, depth, path, image, image_alt, og_type), header_html(active_file, depth), body, footer_html(depth))


def tags_html(book):
    spans = []
    for s in book["status"]:
        cls = "tag tag--live" if s != "coming-soon" else "tag"
        label = TAG_LABELS[s]
        url_field = STATUS_URL_FIELDS.get(s)
        url = book.get(url_field) if url_field else None
        if url:
            spans.append('<li class="%s"><a href="%s" target="_blank" rel="noopener">%s</a></li>' % (cls, url, label))
        else:
            spans.append("<li class=\"%s\">%s</li>" % (cls, label))
    return "<ul class=\"tags\">" + "".join(spans) + "</ul>"


def share_btn(path, title, text, cls=""):
    """One Share button. Hidden until js/site.js shows it, so it never appears inert."""
    return ('<button type="button" class="share-btn%s" hidden data-share-url="%s" data-share-title="%s" data-share-text="%s">Share</button>'
            % (" " + cls if cls else "", abs_url(path), attr(title), attr(text)))


# ---- records (scenes): descriptive line, own pages ------------------------------------
def record_path(sc):
    return "records/%s.html" % sc["slug"]


def record_title(sc):
    """A record's heading, page title and share title. Short records use their caption as is;
    a record with a longer caption carries an optional "title" (the caption is then shown as
    a paragraph on the record's own page, see record_detail_body)."""
    if sc.get("title"):
        return sc["title"]
    t = plain(sc["caption_html"]).rstrip(".")
    return t[:1].upper() + t[1:]


def record_subjects(sc):
    """Subjects a record is about: an explicit "subjects" list on the scene if given, else the
    characters its caption links to. Nothing is guessed beyond that."""
    slugs = sc.get("subjects") or re.findall(r'characters/([\w\-]+)\.html', sc["caption_html"])
    seen, out = set(), []
    for s in slugs:
        if s in CHAR_INDEX and s not in seen:
            seen.add(s)
            out.append(CHAR_INDEX[s][0])
    return out


def record_meta_html(sc, b, depth, short=False):
    """The descriptive line under a record: Subject / Archive. `short` drops the case title
    (used on the case's own page, where the title is already the page heading)."""
    r = rel(depth)
    parts = []
    subs = record_subjects(sc)
    if subs:
        parts.append('<span class="rm-label">Subject</span> ' + ", ".join(
            '<a href="%scharacters/%s.html">%s</a>' % (r, c["slug"], c["name"]) for c in subs))
    parts.append('<span class="rm-label">Archive</span> <a href="%sbooks/%s.html">%s</a>'
                 % (r, b["slug"], b["case_tag"] if short else "%s &middot; %s" % (b["case_tag"], b["title"])))
    return '<p class="record-meta">%s</p>' % ' <span class="rm-sep" aria-hidden="true">/</span> '.join(parts)


def record_actions_html(sc, b, depth):
    r = rel(depth)
    return ('<p class="record-actions"><a class="record-open" href="%s%s">Open record</a>%s</p>'
            % (r, record_path(sc), share_btn(record_path(sc), record_title(sc) + " — " + b["case_tag"], record_title(sc) + ".")))


def character_entry_html(c, depth):
    r = rel(depth)
    href = "%scharacters/%s.html" % (r, c["slug"])
    full_src = "%simages/characters/%s.jpg" % (r, c["slug"])
    thumb_src = "%simages/characters/%s-thumb.jpg" % (r, c["slug"])
    return """      <article class="entry">
        <a class="lightbox-link" data-group="characters" href="#" data-full="%s"><img class="entry-portrait" src="%s" alt="Portrait of %s"></a>
        <div class="entry-body">
          <h3 class="entry-title"><a href="%s">%s</a></h3>
          <p class="entry-meta">%s</p>
          <p>%s</p>
          <p class="entry-links"><a class="entry-link" href="%s">Read the full entry</a></p>
        </div>
      </article>""" % (full_src, thumb_src, c["name"], href, c["name"], c["epithets"], c["teaser"], href)


def characters_index_html(book, depth):
    return "\n".join(character_entry_html(c, depth) for c in book["characters"])


def scene_gallery_html(book, depth):
    r = rel(depth)
    items = []
    for s in book["scenes"]:
        full = "%simages/scenes/%s.jpg" % (r, s["slug"])
        grid = "%simages/scenes/%s-grid.jpg" % (r, s["slug"])
        items.append("""      <li>
        <a class="lightbox-link" data-group="scenes" href="#" data-full="%s"><img src="%s" alt="%s"></a>
        <p class="scene-caption">%s</p>
        %s
        %s
      </li>""" % (full, grid, s["alt"], s["caption_html"], record_meta_html(s, book, depth, short=True), record_actions_html(s, book, depth)))
    return "\n".join(items)


def book_entry_html(book, depth):
    r = rel(depth)
    book_href = "%sbooks/%s.html" % (r, book["slug"])
    cover_src = "%simages/covers/%s" % (r, book["cover_file"])
    return """      <article class="entry entry--book">
        <a class="lightbox-link" data-group="covers" href="#" data-full="%s"><img class="entry-cover" src="%s" alt="Cover of %s"></a>
        <div class="entry-body">
          <h3 class="entry-title"><a href="%s">%s</a></h3>
          %s
          <p>%s</p>
          <p class="entry-links"><a class="entry-link" href="%s">Read the full entry</a></p>
        </div>
      </article>""" % (cover_src, cover_src, book["title"], book_href, book["title"], tags_html(book), book["hook"], book_href)


# ---- case-archive helpers ---------------------------------------------------------
def is_published(b):
    return any(s != "coming-soon" for s in b["status"])


def _n(count, one, many):
    return "%d %s" % (count, one if count == 1 else many)


def case_card_html(b, depth, why=None):
    r = rel(depth)
    href = "%sbooks/%s.html" % (r, b["slug"])
    cover = "%simages/covers/%s" % (r, b["cover_file"])
    extra = "".join('<span class="case-why">%s</span>' % w for w in (why or [])[:2])
    if not extra:
        extra = '<span class="case-hook">%s</span>' % b["hook"]
    cls = "case-card" if is_published(b) else "case-card case-card--muted"
    return ('<li class="%s"><a href="%s"><img src="%s" alt="Cover of %s" loading="lazy">'
            '<span class="case-no">%s</span><span class="case-title">%s</span>%s</a></li>'
            % (cls, href, cover, _esc(b["title"]), b["case_tag"], b["title"], extra))


def case_grid_html(books, depth, cls="", cap=None, why_map=None):
    items = "\n".join("        " + case_card_html(b, depth, (why_map or {}).get(b["slug"])) for b in books)
    return '<ul class="case-grid %s"%s>\n%s\n      </ul>' % (cls, ' data-cap="%d"' % cap if cap else "", items)


def _case_head(title, n):
    return '<header class="case-head"><h2>%s</h2><p class="count">%s</p></header>' % (title, _n(n, "book", "books"))


def published_section_html(depth, teaser=False):
    live = [b for b in BOOKS if is_published(b)]
    more = ""
    if teaser:
        waiting = len(BOOKS) - len(live)
        more = '\n      <p><a href="books.html#awaiting">%s awaiting release &rarr;</a></p>' % _n(waiting, "more case", "more cases")
    return ('<section class="case-section" id="published">\n      %s\n      %s%s\n    </section>'
            % (_case_head("Published Cases", len(live)), case_grid_html(live, depth), more))


def awaiting_band_html(depth):
    wait = [b for b in BOOKS if not is_published(b)]
    return ('<section class="case-band" id="awaiting">\n      <div class="wrap">\n        %s\n        %s\n      </div>\n    </section>'
            % (_case_head("Cases Awaiting Release", len(wait)), case_grid_html(wait, depth, "case-grid--muted")))


def read_buttons(b):
    """[(label, url)] for every place the book can be read, primary first."""
    out = []
    for tag, label, field in (("google-books", "Read on Google Books", "google_books_url"),
                              ("kindle", "Read on Kindle", "kindle_url"),
                              ("royal-road", "Read on Royal Road", "royal_road_url")):
        if tag in b["status"]:
            out.append((label, b.get(field, "#")))
    return out


def cta_html(b, where):
    """The dominant READ button (top of a case page) or the full set (bottom)."""
    btns = read_buttons(b)
    if not btns:
        return ""
    out = []
    for i, (label, url) in enumerate(btns):
        if where == "top" and i:
            break
        cls = "cta cta--primary" if i == 0 else "cta cta--ghost"
        out.append('<a class="%s" href="%s" target="_blank" rel="noopener">%s</a>' % (cls, url, label))
    if where == "top" and b["characters"]:
        out.append('<a class="cta cta--ghost" href="#subjects">Explore subjects</a>')
    if where == "bottom" and b["characters"]:
        out.append('<a class="cta cta--ghost" href="#subjects">Back to subjects</a>')
    return '<div class="cta-row">%s</div>' % "".join(out)


def principals_of(b):
    chars = b["characters"]
    if len(chars) <= SPLIT_MIN:
        return chars, []
    want = PRINCIPALS.get(b["slug"])
    by = dict((c["slug"], c) for c in chars)
    main = [by[s] for s in want if s in by] if want else chars[:6]
    keep = set(c["slug"] for c in main)
    return main, [c for c in chars if c["slug"] not in keep]


def character_rec_html(c, depth):
    r = rel(depth)
    img = c["slug"] + "-thumb.jpg"
    if not os.path.isfile(os.path.join(OUT, "images", "characters", img)):
        img = c["slug"] + ".jpg"
    return ('<li class="rec"><a href="%scharacters/%s.html"><img src="%simages/characters/%s" alt="" loading="lazy">'
            '<span><span class="rec-name">%s</span><span class="rec-meta">%s</span></span></a></li>'
            % (r, c["slug"], r, img, c["name"], c["epithets"]))


def subjects_section_html(b):
    chars = b["characters"]
    if not chars:
        return '<h2>Subjects</h2>\n        <p class="editor-note">Subject roster coming soon.</p>'
    main, extra = principals_of(b)
    out = '<h2>%s</h2>\n        <ul class="catalog-list subjects-list">\n%s\n        </ul>' % (
        "Principal Subjects" if extra else "Subjects", "\n".join(character_entry_html(c, 1) for c in main))
    if extra:
        out += """
        <h3 class="sub-head">Additional Case Records</h3>
        <details class="additional">
          <summary>%d additional %s documented</summary>
          <div class="additional-body">
            <ul class="recs recs--cast">
%s
            </ul>
            <p><a href="../characters.html?case=%s">Open the subject index for %s &rarr;</a></p>
          </div>
        </details>""" % (len(extra), "subject" if len(extra) == 1 else "subjects",
                         "\n".join("              " + character_rec_html(c, 1) for c in extra), b["slug"], b["case_tag"])
    return out


# ---- related cases / subjects / records ---------------------------------------------
CHAR_INDEX = dict((c["slug"], (c, b)) for b in BOOKS for c in b["characters"])


def _class_of(b):
    return b["catalyst"]["meta"] if b.get("catalyst") else None


def _faiths(b):
    return [l for l in LORE if l.get("group") == "Religion" and ("books/%s.html" % b["slug"]) in l.get("appears_html", "")]


def related_cases(b, limit=6):
    rows = []
    mine = set(l["slug"] for l in _faiths(b))
    for o in BOOKS:
        if o is b:
            continue
        why = []
        if _class_of(b) and _class_of(b) == _class_of(o):
            why.append("Same catalyst class: %s" % _class_of(b).replace(" Class", ""))
        for l in _faiths(o):
            if l["slug"] in mine:
                why.append("Shared faith: %s" % l["name"].replace("The ", ""))
        for x, y, text in RELATED_THEMES:
            if set((x, y)) == set((b["slug"], o["slug"])):
                why.append(text)
        if why:
            rows.append((o, why))
    rows.sort(key=lambda t: (-len(t[1]), not is_published(t[0]), BOOKS.index(t[0])))
    return rows[:limit]


def related_cases_html(b, depth):
    rows = related_cases(b)
    if not rows:
        return ""
    return ('<section class="subsection related" id="related">\n        <h2>Related Cases</h2>\n        %s\n      </section>'
            % case_grid_html([o for o, _w in rows], depth, "case-grid--related", cap=4, why_map=dict((o["slug"], w) for o, w in rows)))


def related_subjects(c, b, limit=6):
    def links(x):
        return re.findall(r'href="\.\./characters/([\w\-]+)\.html"', x["bio_html"])
    out = [s for s in links(c) if s in CHAR_INDEX and s != c["slug"]]
    out += [o["slug"] for o in b["characters"] if o["slug"] != c["slug"] and c["slug"] in links(o)]
    if len(set(out)) < 3:
        out += [o["slug"] for o in principals_of(b)[0] if o["slug"] != c["slug"]]
    seen, res = set(), []
    for slug in out:
        if slug not in seen:
            seen.add(slug)
            res.append(CHAR_INDEX[slug][0])
    return res[:limit]


def related_records(c, b, limit=4):
    key = "characters/%s.html" % c["slug"]
    return [sc for sc in b["scenes"] if key in sc["caption_html"]][:limit]


def related_records_html(scenes, depth):
    r = rel(depth)
    items = "\n".join(
        '        <li><a class="lightbox-link" data-group="related-records" href="#" data-full="%simages/scenes/%s.jpg"><img src="%simages/scenes/%s-grid.jpg" alt="%s" loading="lazy"></a><p class="scene-caption">%s</p></li>'
        % (r, sc["slug"], r, sc["slug"], _esc(sc["alt"]), sc["caption_html"]) for sc in scenes)
    return '<ul class="rel-records">\n%s\n      </ul>' % items


def lore_cases(l):
    if l.get("roster"):
        return [b for b in BOOKS if b.get(l["roster"])]
    slugs = re.findall(r'books/([\w]+)\.html', l.get("appears_html", ""))
    return [b for b in BOOKS if b["slug"] in slugs]


def _check_principals():
    for slug, want in PRINCIPALS.items():
        have = set(c["slug"] for b in BOOKS if b["slug"] == slug for c in b["characters"])
        missing = [w for w in want if w not in have]
        assert not missing, "PRINCIPALS[%s] names unknown subjects: %s" % (slug, missing)



def _index_body_base():
    lore_items = "\n".join(
        "          <li><a href=\"lore/%s.html\">%s</a></li>" % (l["slug"], l["name"])
        for l in LORE
    )
    return """    <section class="hero hero--home">
      <div class="wrap">
        <img class="emblem" src="assets/logo-gold.png" alt="" width="396" height="520">
        <h1>%s</h1>
        <p class="tagline">Speculative fiction. The fragility of human systems, one kingdom at a time.</p>
        <p class="lede">%s writes speculative fiction about the rise and collapse of kingdoms, the evolution of faiths, and the small moments of pride, fear, and vanity that bring great structures down. This site collects the novels, and the lore behind them.</p>
        <p><a class="btn" href="books.html">Enter the archive</a> <a class="btn btn--ghost" href="#begin">Where to begin</a></p>
        @@LEDGER@@
      </div>
    </section>

@@FEATURED@@
    <div class="section wrap">
    %s
    </div>

@@SECTIONS@@
    <section class="section wrap">
      <h2>Archive</h2>
      <p>A glossary of terms and systems from the setting.</p>
      <ul class="index-list">
%s
      </ul>
      <p><a href="lore.html">Open the archive &rarr;</a></p>
    </section>

@@BEGIN@@""" % (AUTHOR, AUTHOR, published_section_html(0, teaser=True), lore_items)


ROSTER = {
    "envoy": ("Envoys", "One per case, in the order the books appear on this site."),
    "catalyst": ("Catalysts", "One per case, in the order the books appear on this site."),
}

# One scene per book for the homepage band: (book slug, scene slug).
HOME_SCENES = [("0000", "valeria-full-power"), ("4099", "tower-burning"),
               ("0157", "vartaz-and-the-floor"), ("4417", "the-chrome-heels"),
               ("4420", "yvaine-in-the-south"), ("4555", "the-beam-finds-blakk"), ("4438", "the-solstice-ascension"),
               ("0188", "the-granary-of-rats")]


def roster_html(kind, depth):
    r = rel(depth)
    rows = []
    for b in BOOKS:
        it = b.get(kind)
        if not it:
            continue
        href = r + it["page"]
        rows.append("""      <article class="entry">
        <a class="entry-thumb" href="%s" aria-hidden="true" tabindex="-1"><img class="entry-portrait" src="%simages/%s" alt="" loading="lazy"></a>
        <div class="entry-body">
          <h3 class="entry-title"><a href="%s">%s</a></h3>
          <p class="entry-meta">%s &middot; <a href="%sbooks/%s.html">%s</a> (%s)</p>
          %s
        </div>
      </article>""" % (href, r, it["img"], href, it["name"], it["meta"], r, b["slug"], b["title"], b["case_tag"], it["html"]))
    return "<div class=\"catalog-list\">\n" + "\n".join(rows) + "\n      </div>"


def home_wall_html():
    items = []
    for b in BOOKS:
        n = 0
        for c in b["characters"]:
            if n >= 6:
                break
            if not os.path.isfile(os.path.join(OUT, "images", "characters", c["slug"] + "-thumb.jpg")):
                continue
            items.append('        <li><a href="characters/%s.html"><img src="images/characters/%s-thumb.jpg" alt="" loading="lazy"><span>%s</span></a></li>' % (c["slug"], c["slug"], c["name"]))
            n += 1
    return "\n".join(items)


def home_scenes_html():
    by_slug = dict((b["slug"], b) for b in BOOKS)
    items = []
    for book_slug, scene_slug in HOME_SCENES:
        b = by_slug.get(book_slug)
        if b:
            items.append('        <li><a href="books/%s.html"><img src="images/scenes/%s-grid.jpg" alt="" loading="lazy"><span>%s</span></a></li>' % (b["slug"], scene_slug, b["title"]))
    return "\n".join(items)


def index_body():
    n_chars = sum(len(b["characters"]) for b in BOOKS)
    n_scenes = sum(len(b["scenes"]) for b in BOOKS)
    ledger = '<ul class="ledger-stats"><li><b>%d</b><span>Cases</span></li><li><b>%d</b><span>Subjects</span></li><li><b>%d</b><span>Records</span></li></ul>' % (len(BOOKS), n_chars, n_scenes)
    sections = """    <section class="section wrap">
      <h2>Subjects</h2>
      <p>A few faces from each case &mdash; every subject has a file of their own.</p>
      <ul class="wall" data-cap="12">
%s
      </ul>
      <p><a href="characters.html">View all subjects &rarr;</a></p>
    </section>

    <section class="section wrap">
      <h2>Records</h2>
      <ul class="wall wall--scenes" data-cap="6">
%s
      </ul>
      <p><a href="scenes.html">View all records &rarr;</a></p>
    </section>
""" % (home_wall_html(), home_scenes_html())
    return _index_body_base().replace("@@LEDGER@@", ledger).replace("@@SECTIONS@@", sections).replace("@@BEGIN@@", begin_html(0)).replace("@@FEATURED@@", featured_html())


def contact_body():
    items = "\n".join(
        '            <li><strong>%s</strong> &mdash; <a href="%s" target="_blank" rel="noopener">%s</a></li>' % (label, url, text)
        for label, text, url in SOCIALS)
    return """    <section class="hero hero--compact">
      <div class="wrap">
        <h1>Contact</h1>
      </div>
    </section>

    <section class="wrap page-content">
      <div class="prose">
        <section class="subsection">
          <ul class="detail-list">
%s
          </ul>
        </section>
      </div>
    </section>
""" % items


def gazetteer_body(l):
    """A gazetteer entry: the map first (opens in the lightbox), then About / Places / Appears In."""
    r = rel(1)
    m = l["map"]
    full = "%simages/maps/%s.jpg" % (r, m["file"])
    places = "\n".join("            <dt>%s</dt>\n            <dd>%s</dd>" % (n, note) for n, note in l["places"])
    return """    <div class="wrap page-content">
      <a class="back-link" href="%slore.html">&larr; Archive</a>
      <h1>%s</h1>
      <p class="share-row">%s</p>

      <div class="gazetteer">
        <figure class="map-figure">
          <a class="lightbox-link" data-group="maps" href="#" data-full="%s"><img class="map-image" src="%s" alt="%s"></a>
          <figcaption>Select the map to enlarge it.</figcaption>
        </figure>
        <div class="prose gazetteer-text">
          <section class="subsection">
            <h2>About the Map</h2>
            %s
          </section>

          <section class="subsection">
            <h2>Places</h2>
            <dl class="places">
%s
            </dl>
          </section>

          <section class="subsection">
            <h2>Appears In</h2>
            %s
          </section>
        </div>
      </div>

      <section class="subsection related">
        <h2>Cases Where This Appears</h2>
        %s
      </section>
    </div>
""" % (r, l["name"], share_btn("lore/%s.html" % l["slug"], l["name"], plain(l["teaser"])),
       full, full, _esc(m["alt"]), l["definition_html"], places, l["appears_html"],
       case_grid_html(lore_cases(l), 1, "case-grid--related", cap=4))


def gazetteers_for(b):
    return [l for l in LORE if l.get("map") and b["slug"] in [x["slug"] for x in lore_cases(l)]]


def gazetteer_cards_html(b, depth):
    r = rel(depth)
    gz = gazetteers_for(b)
    if not gz:
        return ""
    items = "\n".join(
        '          <li><a class="gz-card" href="%slore/%s.html"><img src="%simages/maps/%s-thumb.jpg" alt="" loading="lazy">'
        '<span><span class="gz-name">%s</span><span class="gz-meta">%s</span></span></a></li>'
        % (r, l["slug"], r, l["map"]["file"], l["name"], l["teaser"]) for l in gz)
    return ('<section class="subsection" id="gazetteer">\n        <h2>Gazetteer</h2>\n        <ul class="gz-list">\n%s\n        </ul>\n      </section>' % items)


def lore_detail_body(l):
    if l.get("map"):
        return gazetteer_body(l)
    r = rel(1)
    lore_href = "%slore.html" % r
    if l.get("roster"):
        title, note = ROSTER[l["roster"]]
        second = "<h2>%s</h2>\n          <p>%s</p>\n          %s" % (title, note, roster_html(l["roster"], 1))
    else:
        second = "<h2>Appears In</h2>\n          %s" % l["appears_html"]
    return """    <div class="wrap page-content">
      <a class="back-link" href="%s">&larr; Archive</a>
      <h1>%s</h1>

      <div class="prose">
        <section class="subsection">
          <h2>Definition</h2>
          %s
        </section>

        <section class="subsection">
          %s
        </section>
      </div>

      <section class="subsection related">
        <h2>Cases Where This Appears</h2>
        %s
      </section>
    </div>
""" % (lore_href, l["name"], l["definition_html"], second, case_grid_html(lore_cases(l), 1, "case-grid--related", cap=4))


def books_body():
    return """    <section class="hero hero--compact">
      <div class="wrap">
        <h1>Cases</h1>
        <p class="lede">Every novel is filed as a case. Open one to read its file: principal subjects, records, and where to read it.</p>
        <p class="lede">There is no required order. Each case stands alone, so start with whichever promise draws you &mdash; <a href="index.html#begin">here is a short guide</a>.</p>
      </div>
    </section>

    <div class="wrap page-content">
    %s
    </div>
    %s
""" % (published_section_html(0), awaiting_band_html(0))


def lore_index_html(depth):
    r = rel(depth)

    def li(l):
        href = "%slore/%s.html" % (r, l["slug"])
        return "<li><strong><a href=\"%s\">%s</a></strong> &mdash; %s</li>" % (href, l["name"], l["teaser"])

    # Entries with no "group" key stay in the plain list at the top (Cultivator,
    # Catalyst). Entries carrying a "group" (currently "Religion") are collected
    # under that group's own heading, in the order the groups first appear.
    parts = []
    ungrouped = [l for l in LORE if not l.get("group")]
    if ungrouped:
        parts.append("<ul class=\"detail-list\">" + "".join(li(l) for l in ungrouped) + "</ul>")
    groups = []
    for l in LORE:
        g = l.get("group")
        if g and g not in groups:
            groups.append(g)
    for g in groups:
        members = "".join(li(l) for l in LORE if l.get("group") == g)
        parts.append("<section class=\"subsection\"><h2>%s</h2><ul class=\"detail-list\">%s</ul></section>" % (g, members))
    return "\n      ".join(parts)


def lore_body():
    return """    <section class="hero hero--compact">
      <div class="wrap">
        <h1>Archive</h1>
        <p class="lede">A glossary of terms and systems from the setting &mdash; growing as new cases are filed.</p>
      </div>
    </section>

    <section class="wrap page-content">
      %s
    </section>
""" % lore_index_html(0)


def about_body():
    paras = "\n          ".join("<p>%s</p>" % p for p in BIOGRAPHY_PARAGRAPHS)
    return """    <section class="hero hero--compact">
      <div class="wrap">
        <h1>About</h1>
      </div>
    </section>

    <section class="wrap page-content">
      <div class="prose">
        <section class="subsection">
          <h2>Biography</h2>
          %s
        </section>
      </div>
    </section>
""" % paras


def book_detail_body(book):
    b = book
    r = rel(1)
    cover_src = "%simages/covers/%s" % (r, b["cover_file"])
    books_href = "%sbooks.html" % r

    if is_published(b):
        bottom = "<h2>Read This Book</h2>\n          " + cta_html(b, "bottom")
    else:
        bottom = "<h2>Awaiting Release</h2>\n          <p>Not yet available &mdash; this panel will link out once there is somewhere to read it.</p>"
    top_cta = cta_html(b, "top")
    if not top_cta and b["characters"]:
        top_cta = '<div class="cta-row"><a class="cta cta--ghost" href="#subjects">Explore subjects</a></div>'
    share = share_btn("books/%s.html" % b["slug"], "%s — %s" % (b["title"], b["case_tag"]), b["hook"], "share-btn--cta")
    if top_cta:
        top_cta = top_cta.replace("</div>", share + "</div>")
    else:
        top_cta = '<div class="cta-row">%s</div>' % share
    standalone = ""
    if is_published(b):
        standalone = ('<p class="standalone-note">Stands alone. No other case needs to be read first. '
                      '<a href="%sindex.html#begin">Choose another by its promise</a>.</p>\n          ' % r)

    case_tag_html = '<p class="case-tag">%s</p>\n          ' % b["case_tag"] if b.get("case_tag") else ""

    if b["scenes"]:
        scenes_section = """<div class="scene-header">
          <h2>Records</h2>
          <div class="scene-nav">
            <button type="button" class="scene-btn scene-btn--prev" aria-label="Previous record">&lsaquo;</button>
            <button type="button" class="scene-btn scene-btn--next" aria-label="Next record">&rsaquo;</button>
          </div>
        </div>
        <ul class="scene-gallery" tabindex="0" aria-label="Records, %d images, scroll horizontally or use the buttons above">
%s
        </ul>""" % (len(b["scenes"]), scene_gallery_html(b, 1))
    else:
        scenes_section = """<h2>Records</h2>
        <p class="editor-note">Record illustrations will be filed here once they are ready.</p>"""

    return """    <div class="wrap page-content">
      <a class="back-link" href="%s">&larr; All Cases</a>
      <div class="detail-header">
        <a class="lightbox-link" data-group="covers" href="#" data-full="%s"><img class="detail-cover" src="%s" alt="Cover of %s"></a>
        <div class="detail-meta">
          %s<h1>%s</h1>
          %s
          %s
        </div>
      </div>

      <div class="prose">
        <section class="subsection">
          <h2>Case File</h2>
          %s<ul class="detail-list">
            <li><strong>Pages</strong> &mdash; %s</li>
            <li><strong>Genre</strong> &mdash; %s</li>
          </ul>
          <div class="synopsis" data-collapse="15">
          %s
          </div>
        </section>
      </div>

      <section class="subsection" id="subjects">
        %s
      </section>

      <section class="subsection" id="records">
        %s
      </section>

      %s

      <div class="prose">
        <section class="subsection purchase-panel">
          %s
        </section>
      </div>

      %s
    </div>
""" % (books_href, cover_src, cover_src, _esc(b["title"]), case_tag_html, b["title"], tags_html(b), top_cta,
       standalone, b["pages"], b["genre"], b["synopsis_html"], subjects_section_html(b), scenes_section,
       gazetteer_cards_html(b, 1), bottom, related_cases_html(b, 1))


def character_detail_body(c, book):
    r = rel(1)
    book_href = "%sbooks/%s.html" % (r, book["slug"])
    full_src = "%simages/characters/%s.jpg" % (r, c["slug"])
    quote_html = "<blockquote>&ldquo;%s&rdquo;</blockquote>" % c["quote"] if c.get("quote") else ""
    subj = related_subjects(c, book)
    recs = related_records(c, book)
    more = '\n      <section class="subsection related">\n        <h2>Appears In</h2>\n        %s\n      </section>' % case_grid_html([book], 1, "case-grid--one")
    if subj:
        more += '\n      <section class="subsection related">\n        <h2>Related Subjects</h2>\n        <ul class="recs recs--cast">\n%s\n        </ul>\n      </section>' % "\n".join("          " + character_rec_html(x, 1) for x in subj)
    if recs:
        more += '\n      <section class="subsection related">\n        <h2>Related Records</h2>\n        %s\n      </section>' % related_records_html(recs, 1)
    return """    <div class="wrap page-content">
      <a class="back-link" href="%s">&larr; %s &middot; %s</a>
      <div class="character-entry">
        <a class="lightbox-link" data-group="characters" href="#" data-full="%s"><img class="character-portrait" src="%s" alt="Character reference sheet for %s"></a>
        <div>
          <h1>%s</h1>
          <p class="character-epithets">%s</p>
          <p class="share-row">%s</p>
          %s
          %s
        </div>
      </div>
%s
    </div>
""" % (book_href, book["case_tag"], book["title"], full_src, full_src, c["name"], c["name"], c["epithets"],
       share_btn("characters/%s.html" % c["slug"], "%s — %s" % (c["name"], book["case_tag"]), plain(c["teaser"])),
       c["bio_html"], quote_html, more)


from html import escape as _esc
import re as _re


def _search_text(*parts):
    """Lower-cased, tag-free, entity-decoded text for a data-text search attribute.
    Entities must be decoded *before* the attribute is escaped, otherwise the
    haystack holds literal '&middot;' / '&mdash;' strings and curly quotes never match."""
    txt = " ".join(_unesc(_re.sub(r"<[^>]+>", "", p)) for p in parts)
    return _esc(_re.sub(r"\s+", " ", txt).strip().lower(), quote=True)


def record_detail_body(sc, b):
    r = rel(1)
    scenes = b["scenes"]
    i = scenes.index(sc)
    full = "%simages/scenes/%s.jpg" % (r, sc["slug"])
    title = record_title(sc)
    step = []
    if i:
        step.append('<a href="%s.html">&larr; Previous record</a>' % scenes[i - 1]["slug"])
    if i + 1 < len(scenes):
        step.append('<a href="%s.html">Next record &rarr;</a>' % scenes[i + 1]["slug"])
    steps = '<p class="record-step">%s</p>' % " ".join(step) if step else ""
    read = read_buttons(b)
    cta = ('<p><a class="cta cta--primary" href="%s" target="_blank" rel="noopener">%s</a></p>' % (read[0][1], read[0][0].replace("Read on", "Read this case on"))) if read else ""
    return """    <div class="wrap page-content">
      <a class="back-link" href="%sbooks/%s.html#records">&larr; %s &middot; %s</a>
      <div class="character-entry record-entry">
        <a class="lightbox-link" data-group="records" href="#" data-full="%s"><img class="character-portrait record-image" src="%s" alt="%s"></a>
        <div>
          <p class="case-tag">Record %d of %d</p>
          <h1>%s</h1>
          %s%s
          <p>%s</p>
          <p class="share-row">%s</p>
          %s
          %s
        </div>
      </div>
      <section class="subsection related">
        <h2>Appears In</h2>
        %s
      </section>
    </div>
""" % (r, b["slug"], b["case_tag"], b["title"], full, full, _esc(title), i + 1, len(scenes), title,
       ('<p class="record-caption">%s</p>\n          ' % sc["caption_html"]) if sc.get("title") else "",
       record_meta_html(sc, b, 1), _esc(sc["alt"]) + ".",
       share_btn(record_path(sc), "%s — %s" % (title, b["case_tag"]), title + "."),
       steps, cta, case_grid_html([b], 1, "case-grid--one"))


def begin_html(depth=0):
    """Home-page 'Where to begin': tells a new reader there is no required first book."""
    rows = []
    for b in BOOKS:
        if not is_published(b):
            continue
        genre = plain(re.sub(r'<span class="editor-note">.*?</span>', "", b["genre"]))
        rows.append('        <li><a href="%sbooks/%s.html"><span class="begin-hook">%s</span>'
                    '<span class="begin-meta">%s &middot; %s</span><span class="begin-genre">%s</span></a></li>'
                    % (rel(depth), b["slug"], b["hook"], b["case_tag"], b["title"], genre))
    return """    <section class="section wrap begin" id="begin">
      <h2>Where to begin</h2>
      <p class="begin-lede">There is no first book. Every case stands alone, and every case is connected to the rest. Open any of them cold &mdash; choose the promise that pulls at you.</p>
      <ul class="begin-list">
%s
      </ul>
    </section>
""" % "\n".join(rows)


def featured_html():
    b = next(x for x in BOOKS if x["slug"] == "4555")
    return """    <section class="section wrap featured">
      <h2>Featured case</h2>
      <a class="featured-cover" href="books/%s.html"><img class="entry-cover" src="images/covers/%s" alt="Cover of %s"></a>
      <div class="featured-body">
        <p class="featured-label">%s</p>
        <h3 class="featured-title"><a href="books/%s.html">%s</a></h3>
        <p>%s</p>
        <p><a class="btn btn--ink" href="books/%s.html">Open case</a></p>
      </div>
    </section>
""" % (b["slug"], b["cover_file"], _esc(b["title"]), b["case_tag"], b["slug"], b["title"], b["hook"], b["slug"])


def filter_page_body(title, count, noun, ph, books, items, cls):
    chips = '<button type="button" class="chip is-on" data-book="">All</button>' + "".join(
        '<button type="button" class="chip" data-book="%s" title="%s">%s</button>' % (b["slug"], _esc(b["title"]), b["case_tag"].replace("Case ", ""))
        for b in books)
    return """    <section class="hero hero--compact">
      <div class="wrap">
        <h1>%s</h1>
        <p class="count">%d %s</p>
      </div>
    </section>

    <section class="wrap page-content" data-filter>
      <input class="f-search" type="search" placeholder="%s" aria-label="%s">
      <div class="chips" role="group" aria-label="Filter by case">%s</div>
      <p class="f-empty" hidden>No records match.</p>
      <ul class="recs %s" data-cap="%d">
%s
      </ul>
    </section>
""" % (title, count, noun, ph, ph, chips, cls, 24 if cls == "recs--cast" else 8, "\n".join(items))


def characters_page_body():
    items, books = [], [b for b in BOOKS if b["characters"]]
    for b in books:
        for c in b["characters"]:
            img = c["slug"] + "-thumb.jpg"
            if not os.path.isfile(os.path.join(OUT, "images", "characters", img)):
                img = c["slug"] + ".jpg"
            txt = _search_text(c["name"], c["epithets"], c["teaser"], b["title"])
            items.append('        <li class="rec" data-book="%s" data-text="%s"><a href="characters/%s.html"><img src="images/characters/%s" alt="" loading="lazy"><span><span class="rec-name">%s</span><span class="rec-meta">%s &middot; %s</span></span></a></li>' % (b["slug"], txt, c["slug"], img, c["name"], c["epithets"], b["case_tag"]))
    return filter_page_body("Subjects", len(items), "subjects", "Search subjects...", books, items, "recs--cast")


def scenes_page_body():
    items, books = [], [b for b in BOOKS if b["scenes"]]
    for b in books:
        for sc in b["scenes"]:
            txt = _search_text(sc["alt"], sc["caption_html"], b["title"], b["case_tag"], *[c["name"] for c in record_subjects(sc)])
            items.append('        <li class="rec-scene" data-book="%s" data-text="%s"><a class="lightbox-link" data-group="scenes" href="#" data-full="images/scenes/%s.jpg"><img src="images/scenes/%s-grid.jpg" alt="%s" loading="lazy"></a><p class="scene-caption">%s</p>%s%s</li>' % (b["slug"], txt, sc["slug"], sc["slug"], _esc(sc["alt"]), sc["caption_html"].replace('href="../', 'href="'), record_meta_html(sc, b, 0), record_actions_html(sc, b, 0)))
    return filter_page_body("Records", len(items), "records", "Search records...", books, items, "recs--scenes")


def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", path, len(content), "bytes")


_check_principals()

# ---- top-level pages ---------------------------------------------------------
write("index.html", page("%s \u2014 Speculative Fiction Author" % AUTHOR,
                          "Standalone speculative-fiction novels about the fragility of kingdoms, faiths and human systems, filed as cases. "
                          "Start with any book; each one stands alone.", 0, "index.html", index_body(), path="index.html"))
write("books.html", page("Cases \u2014 %s" % AUTHOR,
                          "Every case in the archive: published novels and cases awaiting release. Each stands alone, so start with any.",
                          0, "books.html", books_body(), path="books.html"))
write("lore.html", page("Archive \u2014 %s" % AUTHOR,
                         "A glossary of terms and systems from the setting.", 0, "lore.html", lore_body(), path="lore.html"))
write("about.html", page("About \u2014 %s" % AUTHOR,
                          "%s %s" % (plain(BIOGRAPHY_PARAGRAPHS[0]), plain(BIOGRAPHY_PARAGRAPHS[1]).split(". ")[0] + "."),
                          0, "about.html", about_body(), path="about.html"))
write("contact.html", page("Contact \u2014 %s" % AUTHOR,
                            "Where to find %s online: %s." % (AUTHOR, ", ".join(label for label, _t, _u in SOCIALS)),
                            0, "contact.html", contact_body(), path="contact.html"))

# ---- book detail pages, and each book's characters ----------------------------
write("characters.html", page("Subjects \u2014 %s" % AUTHOR, "Every subject documented across the cases.", 0, "characters.html", characters_page_body(), path="characters.html"))
write("scenes.html", page("Records \u2014 %s" % AUTHOR, "Key records across the cases.", 0, "scenes.html", scenes_page_body(), path="scenes.html"))

for book in BOOKS:
    write("books/%s.html" % book["slug"],
          page("%s \u2014 %s" % (book["title"], AUTHOR),
               "%s, %s: %s Case file, principal subjects, records, and where to read it." % (book["title"], book["case_tag"], book["hook"]),
               1, "books.html", book_detail_body(book), path="books/%s.html" % book["slug"],
               image=share_image("cover", "images/covers/%s" % book["cover_file"]), image_alt="Cover of %s" % plain(book["title"]), og_type="book"))

    for c in book["characters"]:
        write("characters/%s.html" % c["slug"],
              page("%s \u2014 %s" % (c["name"], AUTHOR),
                   "%s Subject file from %s, %s." % (plain(c["teaser"]), book["case_tag"], book["title"]),
                   1, "books.html", character_detail_body(c, book), path="characters/%s.html" % c["slug"],
                   image="images/characters/%s.jpg" % c["slug"], image_alt="Character reference sheet for %s" % plain(c["name"]), og_type="article"))

    for sc in book["scenes"]:
        write(record_path(sc),
              page("%s \u2014 %s" % (record_title(sc), AUTHOR),
                   "%s. Record from %s, %s." % (sc["alt"].rstrip("."), book["case_tag"], book["title"]),
                   1, "scenes.html", record_detail_body(sc, book), path=record_path(sc),
                   image="images/scenes/%s.jpg" % sc["slug"], image_alt=sc["alt"], og_type="article"))

# ---- lore detail pages ---------------------------------------------------------
for l in LORE:
    write("lore/%s.html" % l["slug"],
          page("%s \u2014 %s" % (l["name"], AUTHOR),
               "%s Definition and where it appears." % l["teaser"],
               1, "lore.html", lore_detail_body(l), path="lore/%s.html" % l["slug"],
               **({"image": share_image("map", "images/maps/%s.jpg" % l["map"]["file"]), "image_alt": l["map"]["alt"]} if l.get("map") else {})))

# ---- old URLs that now redirect ---------------------------------------------------
REDIRECTS = {"lore/catalyst-tier.html": "catalyst.html"}
for old_path, target in REDIRECTS.items():
    write(old_path, """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="robots" content="noindex">
  <meta http-equiv="refresh" content="0; url=%s">
  <link rel="canonical" href="%s">
  <title>Moved</title>
</head>
<body>
  <p>This page moved to <a href="%s">%s</a>.</p>
</body>
</html>
""" % (target, abs_url(os.path.join(os.path.dirname(old_path), target)), target, target))

# ---- sitemap.xml and robots.txt ---------------------------------------------------
# Every page that went through page(path=...) is listed; the redirect stub is not.
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
      + "".join("  <url><loc>%s</loc></url>\n" % _esc(abs_url(p)) for p in SITEMAP_PATHS)
      + "</urlset>\n")
# Note: crawlers only read robots.txt at the root of a host. On a GitHub Pages project
# address (…github.io/Dzulfaraaghaini/) this file is therefore not picked up; submit
# sitemap.xml in Search Console instead. On a custom domain, or any host where the site
# sits at the root, it works as written.
write("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: %s\n" % abs_url("sitemap.xml"))

print("done")
