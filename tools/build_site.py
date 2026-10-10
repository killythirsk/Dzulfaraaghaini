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
    "0000b": ["the-anchorite", "aveline", "halvard", "vasarion", "aimeric", "ganeth"],
}

# Hand-written "Related Cases" links, on top of the automatic ones (same catalyst
# class, shared faith). One tuple per pair: (case slug, case slug, "reason shown").
RELATED_THEMES = [
    ("2231", "4099", "Same subject world: Himuro descends from the court of Case 4099"),
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
                "bio_html": """<p>Never given a name that survives the telling &mdash; only the titles the decades hang on him one at a time. A valley goatherd and ledger-keeper, thirteen years old when a hillside prayer was answered with a sword named Valeria. He carries it for the rest of a long life without once asking to be crowned or believed &mdash; only reckoned with honestly, the way he was raised to keep a column of figures.</p>""",
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
                "bio_html": """<p>A field agent of the <a href="../lore/cultivator.html">Cultivators</a>, deployed to Vardane disguised as a traveling clockmaker with nothing more remarkable about him than a satchel of pocket chronometers. <a href="../characters/garibald.html">Count Garibald</a> shelters him for a night's lodging before asking a single question about his business &mdash; a courtesy no prior posting has required of him, and which his own field note admits, against protocol, he was not required to find noteworthy, and did. He replaces one worn axle joint with a single dull grey sphere, refuses every offer of help, and leaves three days later on foot, forgotten the way useful strangers generally are. The wheel is not.</p>""",
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
                "bio_html": """<p>An anchorite of the <a href="../lore/faith-of-ardwen.html">Vigil of Ardwen</a>, walled in at nineteen; her office and rank are never recorded beyond the vow itself. By the eleventh siege of Ardenwake she has spent eleven years enclosed, and she does what five centuries of attempts had not: she lifts <a href="../characters/valeria.html">Valeria</a>. Afterward she refuses to be named or credited. The sheet files her as the story's second protagonist, alongside Xu Lian, and as the centre of its &ldquo;no want&rdquo; thesis.</p>
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
        "synopsis_html": EDITOR_SYNOPSIS,
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
            "page": "books/2231.html",
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
          <p>When the stranger who came out of the stone draws the column of notches in the dust and turns his palms toward the east, he gives neither answer; the bar on correcting a subject's reading, he reasons, extends to confirming it. His reports record, as a deviation with no operational reason given, that he latches the quarry gate each evening and then walks back up the road to try it, and note that he has begun to leave the heel of his bread on the green's stone at dusk. On the night the village burns he stands at the quarry gate with a lantern and, as the fleeing party reaches it, steps aside and lets it swing open. Nineteen years on, on the first of Averin, he reduces the western stone to dust and recovers the eastern, and the stranger, finding the hollow on the green, walks over and bows to him. He returns the bow, the only answer he is permitted, and leaves the post that night without collecting the bread. The reviewing desk has not yet replied to whether he observed or rescued.</p>""",
            },
            {
                "slug": "shizuka", "name": "Shizuka",
                "epithets": "Tomobe no Shizuka &middot; wife of Tomobe no Higaide, daughter of a provincial scholar &middot; 29 years old at the story's opening",
                "teaser": "The only person who asks how he looked, and who then does the sum and decides, at great cost, not to press it.",
                "bio_html": """<p>A tall woman who walks as though the floor owed her something, and who at nineteen was the only person in the capital to read one of the poems of her future husband, Higaide, aloud, to its author, with a perfectly straight face. She keeps every sheet of his verse in a lacquer box under the dressing-table because they are, she says, the best things in the house. On the night before the ordeal she reads him one about a heron in the rain, tells him that if it is a mistake he will be extremely angry afterward and that she is looking forward to it, and takes his strong left hand and turns it over, as though to learn it like a poem.</p>
          <p>Two days after the notice she goes to Mikusa and asks the Warden, <a href="../characters/jokei.html">Jōkei</a>, how Higaide had looked and whether his sentence was entered, and then to the Bureau of Inquiry, where an Examiner among his sparrows tells her only that a report existed and was eleven sheets long. She does the sum, and does not press it, not with a daughter of six and a court whose beneficiaries would hear a question about the Law's foundations as a confession. She takes the child north to Fort Shirakane, keeps a small school there for the garrison's daughters, and declines the estate offered when the Law lapses. Every first frost she tastes the plum brine with her eyes shut and says, to the empty room, that he would have complained about the salt. She does not learn, within the period of this record, that he lived.</p>""",
            },
            {
                "slug": "jokei", "name": "Jōkei",
                "epithets": "Warden-Priest of Mikusa Shrine &middot; 60 at the story's opening, 79 when the Stone comes apart",
                "teaser": "Sweeps the Stone every morning for eleven years and never once lays his bare palm on it.",
                "bio_html": """<p>A bald, mild, apologetic priest who tended the hillside shrine of Mikusa for thirty years before the Stone arrived, in which time he presided over some seven hundred weddings and a larger number of funerals. He sweeps the ordeal court with a broom and wipes the block with a damp cloth, and has never in eleven years set his bare palm to it; the backs of his fingers have found it cold in summer and, in winter, faintly warm. He sits with the accused as the Law requires, and with <a href="../characters/shizuka.html">Shizuka</a>'s husband he goes further, pointing out a door at the back of the chamber, the most dangerous sentence of his life. He is told there is no door for an innocent man.</p>
          <p>He writes the finding in the Book of the Ordeal and, under it, without being told, the Captain's one sentence. He gives <a href="../characters/shizuka.html">Shizuka</a> the whole account. By the third hand he watches go, <a href="../characters/kanemichi.html">Kanemichi</a>'s, he has begun to keep a tally on the inside of his sleeve with a thumbnail, because someone ought to. At seventy-nine he finds the Stone come apart into a low heap of pale dust in the exact shape of itself, sweeps the last of it into the rill, and enters one line: that the Stone has gone and the kami has given no reason. He leaves untouched the former Minister's signed sheet pasted into the last leaf.</p>""",
            },
            {
                "slug": "sadamune", "name": "Sadamune",
                "epithets": "Ki no Sadamune &middot; Secretary of the Bureau of Inquiry &middot; 43 years old &middot; later Governor of a northern province",
                "teaser": "Reads the Stone's tally to a room pleased with it, and puts a denominator under the figure.",
                "bio_html": """<p>A dry, upright, fastidious man who holds the post of Secretary because nobody else at the Bureau can be trusted to count. For a fortnight he reconciles the Warden of Mikusa's entries against his own, and at the quarterly Reading of the Tally he stands in the Hall of the Two Seals with the Book of the Ordeal open on his forearm and reads it out: nine accused in a little over eleven years, five confessed and beheaded at the Southern Gate, four who put out a hand and were taken. <em>Four for four</em>, says the Deputy Minister, with real pleasure, and the whole dais warms to it.</p>
          <p>He had been told in the corridor that a man who reads a tally and sits has done his duty, and finds he cannot be that man. Either the Stone takes the guilty and refuses the innocent, he says, or it takes whoever puts a hand to it, in which case four of four describes the stone and not the hands. The Bureau has no instrument to tell the two apart. The Right Minister answers him courteously and correctly: a man who has gone cannot be offered in evidence. The remark is entered as &ldquo;a procedural observation, not pursued,&rdquo; and within the month he is made Governor of a northern province whose principal export is weather, where he governs honestly for nineteen years and writes nothing further about stones.</p>""",
            },
            {
                "slug": "kanemichi", "name": "Kanemichi",
                "epithets": "Ono no Kanemichi &middot; rice-warden of the Right Ministry's eastern granary &middot; 52 years old",
                "teaser": "Has never entered a figure he did not count, and will not sign one he did not do.",
                "bio_html": """<p>A broad, plain man with counting-rod calluses on his left hand, who in thirty years has never put a figure in a ledger that he had not counted. A wet autumn rots the thatch over the third bay of his granary and forty koku go to mold; he records the loss in the month it occurs and asks for new thatch. His accurate page is read by someone who needs it to be a theft. At dawn on the twenty-sixth of Jorren he is shown the Stone in the white of the accused, with his warden's tally-token on a cord at his breast, and a decent young clerk of the Bureau holds out a warmed brush and a confession ruled in every column but the signature.</p>
          <p>He reads it, and finds he cannot sign a figure he has not counted; it is not courage, he thinks, since he has none that he knows of. He gives the brush back and puts out his left hand, the one he counts with. <a href="../characters/jokei.html">Jōkei</a> is watching, and counting. The clerk folds the unsigned sheet in thirds and keeps it, to be found forty years later by a daughter who takes it for a laundry list. His ledger is audited the following month by a successor, who finds it exact in every column, and the page about the thatch is filed beneath it with one word in its margin. He had been right in every figure he ever entered. It was the one thing nobody had wanted.</p>""",
            },
            {
                "slug": "kurige", "name": "Kurige",
                "epithets": "Chestnut pony of the Festival of the Small Bow &middot; named only by a stablehand in a hurry &middot; 7 years old by his sheet",
                "teaser": "A pony who bolts at the one small, furious thing he knows by smell.",
                "bio_html": """<p>A chestnut pony whose name means only &ldquo;chestnut-colored,&rdquo; conferred by a stablehand in a hurry. On the twelfth of Eldren, on the meadow below the Shirase River, he carries the Minister of the Left's nine-year-old grandson at a walk and then a canter for the Festival's short course, while a hundred and twenty paces off the boy's teacher watches with his hands in his sleeves. A small russet cat who knows his smell leaps for the saddlecloth, misses, and catches his hock.</p>
          <p>He does not bolt toward the awnings, or toward the river with its water to stop him; he bolts on a diagonal toward the stone footings of the old bridge, which takes him four seconds. The boy goes over his shoulder with an arrow still in his hand. Afterward a patient Examiner finds a scrap of his chestnut hair in the grass at the starting line, with three tufts of russet fur beside it. The sheet's seven years and its white sock are its own; the manuscript gives him only his name, his colour, and the four seconds.</p>""",
            },
            {
                "slug": "bureau-officers", "name": "The Bureau Officers",
                "epithets": "Officers of the Bureau of Inquiry &middot; one about 40, one about 28 by their sheet",
                "teaser": "Two men in dark robes who serve a summons with the regretful courtesy reserved for the condemned.",
                "bio_html": """<p>Two officers of the Bureau of Inquiry, one older and one younger, in dark robes, who come to a compound in the third ward on the twelfth of Garren, a week after the Seven Sevens have ended, and bow with the careful, regretful courtesy kept for the condemned. They bring a summons under the seals of both Ministers: that the Fifth Article obliges the Captain to answer for the day of the Festival, that his motive has been established to the satisfaction of the Left Ministry, that the Bureau has entered no finding to excuse him, and that he may clear his hand at the Stone of Mikusa at dawn on the twentieth.</p>
          <p>Eight days later they walk behind him at a polite distance through the dark to the shrine, with a boy before them carrying a lantern, and are two of the nine witnesses on the dais. The manuscript gives them neither names nor ages, and the figures on their sheet are its own.</p>""",
            },
            {
                "slug": "bertran", "name": "Bertran",
                "epithets": "Sir Bertran de Lanta &middot; master-at-arms of Castelmaur &middot; knight &middot; 38 years old",
                "teaser": "Cannot enter a mercy in any column, so he rides out alone one night to repay it.",
                "bio_html": """<p>A stern, lean, well-made man of thirty-eight who has fought in six minor wars and won five, and who goes through life by double entry: debts incurred and debts paid, blows given and blows returned. On the green at Vilarnau he is disarmed in a single movement by a foreigner who then sheathes both swords and bows with the painful apology of a man who has spilled wine, having left him alive by choice. Bertran has no column in which to enter a mercy. He does not hate the man; it is a respect so complete that it has nowhere to go. In the evenings he carves small pearwood horses and sends them, in rags, to his widowed sister's four children, who have never been told who makes them.</p>
          <p>On the sixteenth of Jorren, when the baron orders the stone broken and the guest taken, he rides down to the mill alone and without a banner, knocks at the door, and tells <a href="../characters/gersenda.html">Gersenda</a> once what is coming. At the end of the yard, without turning, he adds the one line that was not a warning. On the night of the torches he is given forty men and spends forty minutes in a thicket on a perfectly sound hoof. He asks leave to resign his sword, is refused, and rides out of the gate without it. In the fourteenth year he comes to Lasserra on foot, sets a small grey gelding on the bench of the last house, and is not seen again.</p>""",
                "quote": "Tell him that we are even.",
            },
            {
                "slug": "gersenda", "name": "Gersenda",
                "epithets": "Miller's daughter &middot; later wife of the smith's surviving son and leader of the High Ground &middot; 16 at the story's opening, 35 at the departure",
                "teaser": "Teaches a stranger the word for door, and keeps his unreadable poem in the bread-box.",
                "bio_html": """<p>The miller's daughter at the Mill of the Two Weirs, sixteen, with her mother's gap in her front teeth and her late father's long patient face, and the frank clinical interest of a girl who has been told to find something wrong with a person and cannot. She is appointed, by the unspoken vote of the household, to teach the foreigner the language, in the slow flat voice one uses to an elderly, intelligent animal, working through the whole kitchen from the pot to the ladle to the small cracked salt-bowl. She drives a hard bargain at the wool-market, and in return he teaches her his word for stone.</p>
          <p>She is the first to hear him in the barn, and she keeps everyone away from it that afternoon. She answers the door to <a href="../characters/bertran.html">Bertran</a> at night with a candle and an iron ladle held down against her thigh, and on the night of the torches takes the halter, and the others, across the plank into the dark. On the ridge she marries the smith's surviving son and bears five children; she runs the High Ground's affairs with a hard bargain and a long patient face. She keeps a few of the old man's verses, hidden, in a bread-box, and on the day he goes east she hears him say the name at the boundary-stone, as though telling someone where he was going. The morning after, it is she who finds the sheet he has left for her.</p>""",
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
                "slug": "villagers-of-vilarnau", "name": "The Villagers of Vilarnau",
                "epithets": "The village chorus: the cooper, the smith and his wife, a young wife three months gone, a feverish boy, a very old woman, the mill's hired boy &middot; aged 12&ndash;85 by their sheet",
                "teaser": "Touch the stone on the way to somewhere else, and turn a weighing-place into a door.",
                "bio_html": """<p>Forty-one hearths and a hundred and ninety souls, drawn here as the people they are: a wiry cooper who has been drinking and calls the foreigner the Eastern Angel, a broad smith who comes to the green with his hammer, the smith's wife who sends round a dish of boiled sausage and weeps when it is returned untouched, a young wife three months gone who walked three miles that spring to touch a shrine of Elara and now lays her palm where the stranger lays his, a cooper's boy whose fever is said by his mother to have broken at once, a very old woman with four teeth who smiles openly, and the mill's hired boy, who adores the man who mends the sluice. In a fortnight half of them are touching the green's stone on their way to somewhere else, and the top of it begins to take a polish.</p>
          <p>They mean no harm. It is a pious gesture, out of kindness to a stranger and fear of a god, and out of a pleasing sense of being for once in the middle of something; and it is made a plank at a time, by warm people, in a tavern. The smith does not live to reach the ridge; his surviving son, who once read a book, carries the dead man's hammer up on his back and finds no use for it in thirty years. Of the village's hundred and ninety, seventy-four are dead by the second of Kerren, and eight more by the thaw.</p>""",
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
                "slug": "folquet", "name": "Folquet",
                "epithets": "Clerk to the bailiff of Castelmaur &middot; later clerk of record to the Count of Rocafort's assizes &middot; 26 at the distraint, 60 at his death",
                "teaser": "Believes arithmetic is a form of mercy, and writes the one line he would most like to have left blank.",
                "bio_html": """<p>A pale, tidy, ink-fingered young bailiff's clerk of twenty-six, taught from boyhood that a column which does not add is a sin and that arithmetic is a mercy, since it tells people what they owe so that they need not guess. He walks down the lane of Vilarnau behind the cart on the first of Kerren with his book open on his forearm, entering the condition of each hearth in a neat, unemotional shorthand, and does not look at the faces of the people at their doors, since he holds it unprofessional. Of eleven hearths in the east lane, nine are distrained, one is unfortunate, and one is the sort that ought to be put in a ledger. On the tenth line he writes, in clean copperplate, that the widow's hearth violently resisted and that three of the sergeant's men are dead by a foreigner.</p>
          <p>On the third of Kerren he totals the account at sixty-one solidi, and writes in the margin the only comment he permits himself: that the lane would not pay again. He lives to sixty, and becomes clerk of record at the Count of Rocafort's assizes, admired for the exactness of his entries and the economy of his opinions. In the thirty-first year after the burning he is asked to read from the oldest book in his keeping, and reads the tenth line aloud to a room of lawyers. The count's judge supposes it the work of a Saracen mercenary in the late baron's pay, and Folquet, who has never entered an opinion in forty years, says nothing. It is entered. It is the version the district keeps.</p>""",
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
                "slug": "jaume", "name": "Jaume",
                "epithets": "Boy of the High Ground &middot; 9 in the second winter",
                "teaser": "Finds by accident the exact place on a stick where the thumb belongs, and is never told what he was given.",
                "bio_html": """<p>One of the boys of Lasserra who, in the long evenings of the second winter on the ridge, find in the lean old man with the long jaw a master for the sticks. He teaches them with grave patience to hold a wooden sword as one holds a thing that might one day hold one back: the grip, the breath, the settling of the thumb. He teaches them to bow to a stick before they strike it. None of them becomes a swordsman, which he regards as the most successful outcome possible.</p>
          <p>Jaume, nine, finds by pure accident the exact place on the stick where the thumb belongs, and looks up in alarm at the sudden silence. The old man says <em>Perfect</em> in the speech of the High Ground, and then, under his breath, in his own, and goes out to stand a while among the goats. Nobody asks him why. The boy keeps the grip for the rest of his life and is never told what he has been given. The manuscript gives only his age and the moment; the sheet says outright that his appearance is invented.</p>""",
            },
        ],
        "scenes": [],
    },
]

LORE = [
    {
        "slug": "cultivator", "name": "Cultivator", "roster": "envoy",
        "teaser": "The observers who deliver Catalysts to chosen subjects across worlds.",
        "definition_html": """<p>A loose, still-forming collective of offices and field agents &mdash; simply &ldquo;observers&rdquo; in the earliest records &mdash; who select subjects across many worlds and deliver a Catalyst directly into their hands, then spend the rest of that subject's life quietly filing reports on what the world does with it. The name &ldquo;Cultivator&rdquo; wasn't settled on until long after the practice began.</p>
          <p>Their field agents are called Envoys, or Observers. Every case has its own, and no two are the same person: each works through a numbered &ldquo;deployment archetype&rdquo; and a disguise suited to the world they enter &mdash; a woman on a hilltop, a traveling confectioner, an ordinary old man at the bottom of a hole, a wandering hermit, an ascetic kneeling at a drainage ditch, a court astronomer-priest who keeps a kingdom's calendar from a tower, a shipwreck survivor who has kept the same flooded ruin for a hundred and forty years. Every Envoy on file is listed below.</p>
          <p>Not every case resolves within a single lifetime: in at least one instance on file, a Catalyst sat untouched in one family's keeping for four centuries before its case ever closed, and the Envoy assigned to it counts eleven centuries of comparable postings behind him. Redundancy is standard practice on others: one Envoy's own field notes cite several thousand comparable seedings, on the reasoning that a single object left in open ground is recovered by its intended finder only slightly more often than it's carried off by a flood, a jackdaw, or a passing child who simply wants it for its color. One Envoy on file sells her entire remaining stock to a single buyer in an ordinary afternoon of trade and is three postings distant before anyone drinks what she sold them. Another looks like a child of twelve, has not aged in four generations, and is forbidden by protocol to do anything about what she logs. A third is recalled from a tower parapet on the one evening he exceeds his instructions, and leaves a lamp burning behind him. Another, a mute stonecutter, dresses both ends of a matched pair of stones, spends thirty-one years as a quarry-hand beside the one that receives, and is asked, in notches drawn in the dust, the one question he may not answer.</p>""",
    },
    {
        "slug": "catalyst", "name": "Catalyst", "roster": "catalyst",
        "teaser": "The single object at the center of every case.",
        "definition_html": """<p>The one object a Cultivator puts into a society to see what the society does with it. A Catalyst is rarely dangerous in itself &mdash; a jar of candy, a pair of shoes, a sword no one else can lift, a hole in a hillside, a flask that never lets its contents go cold, a traffic cone, an eight-foot electric eel &mdash; and it arrives with no explanation and no instructions. What matters is everything that happens after: the miracle someone declares, the heresy someone else does, the pride that takes offense, and the office that quietly writes it all down.</p>
          <p>Each Catalyst belongs to one case, is placed by one Envoy, and is filed under a number and a class of its own. Some are handed to one person, some are slipped into a court, and one is a hundred-level structure left in a hillside for someone to find, and one is a living animal, released into a flooded ruin and left to be found. Redundancy is standard on some cases: one Catalyst was seeded three times over in the same ditch, so that a single unit lost to a flood or an incurious passerby wouldn't end the case before it began. One Catalyst on file grants nothing but another creature's own perception, on loan for a quarter of an hour at a time, and is never once used by the same hand twice. Another is a buried chamber that rebuilds whatever enters it, exact in everything that can be measured. Another, left beneath a threshing-floor, cuts a circle of clear noon with a ruler's edge out of a sky of ash and holds it open for four hundred and twenty-one days. Another is a pair of stones, one in a shrine and one on a village green, that carries whoever lays a bare palm on the first to the second, and no one ever back. Every Catalyst on file is listed below.</p>""",
    },
    {
        "slug": "faith-of-ardwen", "name": "The Faith of Ardwen", "group": "Religion",
        "teaser": "A monotheism built on waiting, honest prayer, and a sword no one else can lift.",
        "definition_html": """<p>A monotheism built around a single historical miracle: an honest prayer, answered from the sky. Ardwen &mdash; the Unhastening, the Sky-Answered &mdash; is worshipped as the one eternal goddess, without rival, consort, or divine family, and asks less of her followers than most faiths do: wait, ask honestly, keep your promises, and act responsibly without pretending to know a god's mind for her. Her clergy are careful to distinguish what is known from what is merely mysterious, and the faith's own maxim is built to resist any shortcut: <em>Ardwen answers the honest, but never on command.</em></p>
          <p>Her institutional church, the Vigil of Ardwen, is led by a First Keeper and organized into regional Houses of Vigil, with confession, baptism, marriage, funerals, and pilgrimage among its sacred rites. The faith reveres its founding miracle &mdash; and the sword that came with it &mdash; as a sacred sign of that day, never as a rival object of worship. Whatever else it is, Valeria is not a god.</p>""",
        "appears_html": """<p>The founding faith of <a href="../books/0000.html">The Sword of Valeria</a>, where the goddess herself and the relic she left behind both have entries of their own: <a href="../characters/ardwen.html">Ardwen</a> and <a href="../characters/valeria.html">Valeria</a>. Generations later, in <a href="../books/0157.html">The Stolen Prince War</a>, the Vigil's doctrine of unearned, uncommandable grace is tested to its limit by a dungeon that answers the same chest the same way every single time &mdash; a contradiction its own Keeper, <a href="../characters/yudith.html">Yudith</a>, spends eleven years trying to preach around. In <a href="../books/0156.html">The Purging of Charsianon</a>, a Byzantine-styled river valley keeps the Vigil in a plain House of stone and candles, and a Keeper of the Dorylaion Vigil turns a name for a strange calm &mdash; the Doctrine of the Stolen Vessel &mdash; into an army.</p>""",
    },
    {
        "slug": "threefold-crown", "name": "The Threefold Crown", "group": "Religion",
        "teaser": "Three gods, or one god wearing three faces &mdash; the Crown has never resolved which.",
        "definition_html": """<p>An old pagan faith built around three supreme gods who may, or may not, be one god wearing three faces &mdash; a contradiction its own believers call the Threefold Mystery and have never been in any hurry to resolve. <strong>Auron</strong> the Father governs heaven, law, kingship, judgment, and oaths; <strong>Elara</strong> the Mother governs earth, birth, fertility, harvest, and hearth; <strong>Solan</strong> the Son governs the sun, fire, youth, passion, and sacrifice. A believer may favor one god over the other two without ever quite denying that all three are, somehow, the same throne. The formula recited at its temples leaves the contradiction standing on purpose: <em>Father above. Mother beneath. Son beside us. Three crowns. One Heaven.</em></p>
          <p>Ritual-heavy and elaborately hierarchical, with wine treated as sacred and pork freely eaten, the Threefold Crown holds that its own throne is the one true one &mdash; a claim that makes its temple politics every bit as susceptible to ambition as any earthly court, and its priesthood just as capable of turning a private grief, or a private embezzlement, into doctrine.</p>""",
        "appears_html": """<p>Vantashen's state religion in <a href="../books/0157.html">The Stolen Prince War</a>, where Hierarch <a href="../characters/doreth.html">Doreth</a> turns a private grief into a war he tells himself is a monument, and the guardian at Level 40 is known to delvers as <a href="../characters/the-ember-judge.html">the Trial of Solan</a>. In <a href="../books/4417.html">The Iron Stiletto War</a>, the Order of the Pale Cloth's High Cleric <a href="../characters/ambrose.html">Ambrose</a> declares a pair of shoes heretical on the Crown's own authority. In <a href="../books/2140.html">The Third Grain</a>, a legal claim over a county mill is argued and won entirely inside the Crown's own law, under a courtroom ceiling painted with <a href="../characters/eldest-witness-of-the-writ.html">a judge</a> who has spent thirty years complaining that Auron's three scales were never painted quite level. And in <a href="../books/2231.html">The Stone of the Clean Hand</a>, a hearth-priest's honest report of a stranger's bow to Solan's Fire and refusal of the feast-pig reaches Hierarch <a href="../characters/odilo.html">Odilo</a> at Castelmaur, who lays the temple's interdict on a whole lane until its idol is cast down.</p>""",
    },
    {
        "slug": "decree-of-luminescence", "name": "The Decree of Luminescence", "group": "Religion",
        "teaser": "A theology of measured light: what is favored is lit, and what is lit has been favored.",
        "definition_html": """<p>The youngest of the faiths on file, promulgated after a kingdom-threatening catastrophe: years of ash-blotted sky broken, at the exact point of famine, by a single standing column of true daylight over the capital. <strong>Sol-Invictus, the Unconquered Sun,</strong> is worshipped as the one eternal, lending light, and its doctrine is unusually literal for a religion: light is not read as a sign of favor, it <em>is</em> favor, measured out to every soul at birth as a store of borrowed fire and returned, spent or unspent, at death. It is a creditor's theology at bottom, and its own clergy don't pretend otherwise. The doctrine's core article states the idea plainly: <em>Whatever was favored was lit, and whatever was lit had been favored.</em></p>
          <p>Its church, the Last Order, is led by a High Pontiff and keeps its own doctrine correctable only by further entry, never by erasure. A claimant to real favor stands before a lens that concentrates true daylight onto them, to see whether they visibly glow; a crown is carried through open flame, to see whether the gold endures. What three centuries of both tests have never quite worked out is how to tell light that's generated from light that's merely, cleverly, reflected.</p>""",
        "appears_html": """<p>Its founding is the subject of <a href="../books/2365.html">The Decree of Luminescence</a>. Three centuries on, in <a href="../books/4555.html">The Vessel of Unmediated Grace</a>, where King <a href="../characters/aethelgard.html">Aethelgard</a>'s death without an heir turns the succession into a lit competition, High Pontiff <a href="../characters/sarel.html">Sarel</a> presides over the Grand Basilica's Great Judgment, and a peddler named <a href="../characters/fenn.html">Fenn</a> makes an honest living selling pilgrims small shards of warmed river quartz as splinters of the crown. The <a href="../characters/anchorite-of-the-drowned-road.html">Anchorite of the Drowned Road</a> sect keeps its own small, tolerated counter-doctrine on the Sun's behalf, practicing His absence rather than His favor.</p>""",
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


def lore_detail_body(l):
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

      <div class="prose">
        <section class="subsection purchase-panel">
          %s
        </section>
      </div>

      %s
    </div>
""" % (books_href, cover_src, cover_src, _esc(b["title"]), case_tag_html, b["title"], tags_html(b), top_cta,
       standalone, b["pages"], b["genre"], b["synopsis_html"], subjects_section_html(b), scenes_section, bottom, related_cases_html(b, 1))


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
          %s
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
            txt = _esc(" ".join([c["name"], c["epithets"], c["teaser"], b["title"]]).lower(), quote=True)
            items.append('        <li class="rec" data-book="%s" data-text="%s"><a href="characters/%s.html"><img src="images/characters/%s" alt="" loading="lazy"><span><span class="rec-name">%s</span><span class="rec-meta">%s &middot; %s</span></span></a></li>' % (b["slug"], txt, c["slug"], img, c["name"], c["epithets"], b["case_tag"]))
    return filter_page_body("Subjects", len(items), "subjects", "Search subjects...", books, items, "recs--cast")


def scenes_page_body():
    items, books = [], [b for b in BOOKS if b["scenes"]]
    for b in books:
        for sc in b["scenes"]:
            txt = _esc(" ".join([sc["alt"], _re.sub(r"<[^>]+>", "", sc["caption_html"]), b["title"], b["case_tag"]] + [c["name"] for c in record_subjects(sc)]).lower(), quote=True)
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
               image="images/covers/%s" % book["cover_file"], image_alt="Cover of %s" % plain(book["title"]), og_type="book"))

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
               1, "lore.html", lore_detail_body(l), path="lore/%s.html" % l["slug"]))

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
