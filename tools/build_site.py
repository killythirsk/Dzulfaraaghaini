# -*- coding: utf-8 -*-
"""
Generates the author-site static site (v4 — multi-book).
Run with `python3 build_site.py` from anywhere; it locates the project
root relative to this file's own location.
"""
import os

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTHOR = "Dzulfaraaghaini"

NAV = [
    ("index.html", "Home"),
    ("books.html", "Book"),
    ("lore.html", "Lore"),
    ("about.html", "About"),
    ("contact.html", "Contact"),
]

TAG_LABELS = {
    "published": "Published",
    "google-books": "Available on Google Books",
    "kindle": "Available on Kindle",
    "royal-road": "Available on Royal Road",
    "coming-soon": "Coming Soon",
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
        "slug": "4420", "title": "The Thermal Vessel War",
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
          <p>Duke Vane, who wants the relic less for what it can do than for the Regency it could buy him, sells a beaten Maros his rescue at ruinous terms, hires the thief Soren to lift the vessel from the coalition's war-altar, and discovers too late what he has actually been fighting over. The war that follows is a slaughter no southern chronicle will ever name honestly; the scribes settle on the Great Winter Pestilence. <em>The Thermal Vessel War</em> closes on a Cultivator's archival log &mdash; Case Study 4,420: one flask, four centuries idle, and the most efficient war its Observer has recorded in eleven centuries.</p>""",
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
        "slug": "0188", "title": "The Songs Never Mention the Cats",
        "status": ["coming-soon"],
        "cover_file": "0188.jpg",
        "hook": "Arithmetic. Seven. Cats. A debt mistaken for a miracle. Filed.",
        "case_tag": "Case 0188",
        "pages": EDITOR_PAGES,
        "genre": EDITOR_GENRE,
        "synopsis_html": EDITOR_SYNOPSIS,
        "characters": [],
        "scenes": [],
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
        "characters": [],
        "scenes": [],
    },
    {
        "slug": "3115", "title": "The Listening Water",
        "status": ["coming-soon"],
        "cover_file": "3115.jpg",
        "hook": "Reckoning. Rationed. Witnessed. Roster. Closed.",
        "case_tag": "Case 3115",
        "pages": EDITOR_PAGES,
        "genre": EDITOR_GENRE,
        "synopsis_html": EDITOR_SYNOPSIS,
        "characters": [],
        "scenes": [],
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
]

LORE = [
    {
        "slug": "cultivator", "name": "Cultivator", "roster": "envoy",
        "teaser": "The observers who deliver Catalysts to chosen subjects across worlds.",
        "definition_html": """<p>A loose, still-forming collective of offices and field agents &mdash; simply &ldquo;observers&rdquo; in the earliest records &mdash; who select subjects across many worlds and deliver a Catalyst directly into their hands, then spend the rest of that subject's life quietly filing reports on what the world does with it. The name &ldquo;Cultivator&rdquo; wasn't settled on until long after the practice began.</p>
          <p>Their field agents are called Envoys, or Observers. Every case has its own, and no two are the same person: each works through a numbered &ldquo;deployment archetype&rdquo; and a disguise suited to the world they enter &mdash; a woman on a hilltop, a traveling confectioner, an ordinary old man at the bottom of a hole, a wandering hermit, an ascetic kneeling at a drainage ditch. Every Envoy on file is listed below.</p>
          <p>Not every case resolves within a single lifetime: in at least one instance on file, a Catalyst sat untouched in one family's keeping for four centuries before its case ever closed, and the Envoy assigned to it counts eleven centuries of comparable postings behind him. Redundancy is standard practice on others: one Envoy's own field notes cite several thousand comparable seedings, on the reasoning that a single object left in open ground is recovered by its intended finder only slightly more often than it's carried off by a flood, a jackdaw, or a passing child who simply wants it for its color.</p>""",
    },
    {
        "slug": "catalyst", "name": "Catalyst", "roster": "catalyst",
        "teaser": "The single object at the center of every case.",
        "definition_html": """<p>The one object a Cultivator puts into a society to see what the society does with it. A Catalyst is rarely dangerous in itself &mdash; a jar of candy, a pair of shoes, a sword no one else can lift, a hole in a hillside, a flask that never lets its contents go cold, a traffic cone &mdash; and it arrives with no explanation and no instructions. What matters is everything that happens after: the miracle someone declares, the heresy someone else does, the pride that takes offense, and the office that quietly writes it all down.</p>
          <p>Each Catalyst belongs to one case, is placed by one Envoy, and is filed under a number and a class of its own. Some are handed to one person, some are slipped into a court, and one is a hundred-level structure left in a hillside for someone to find. Redundancy is standard on some cases: one Catalyst was seeded three times over in the same ditch, so that a single unit lost to a flood or an incurious passerby wouldn't end the case before it began. Every Catalyst on file is listed below.</p>""",
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


def rel(depth):
    return "../" * depth


def nav_html(active_file, depth):
    items = []
    for href, label in NAV:
        target = (rel(depth) + href) if depth else href
        current = " aria-current=\"page\"" if href == active_file else ""
        items.append("<li><a href=\"%s\"%s>%s</a></li>" % (target, current, label))
    return "\n          ".join(items)


def head_html(title, description, depth):
    r = rel(depth)
    return """  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>%s</title>
  <meta name="description" content="%s">
  <meta name="robots" content="noimageindex">
  <link rel="icon" href="%sassets/favicon.svg" type="image/svg+xml">
  <link rel="alternate icon" href="%sassets/favicon.ico">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,500;0,600;1,500&display=swap">
  <link rel="stylesheet" href="%scss/style.css">""" % (title, description, r, r, r)


def header_html(active_file, depth):
    r = rel(depth)
    home = (r + "index.html") if depth else "index.html"
    return """  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="header-inner wrap">
      <a class="site-title" href="%s">%s</a>
      <nav class="site-nav" aria-label="Main">
        <ul>
          %s
        </ul>
      </nav>
    </div>
  </header>""" % (home, AUTHOR, nav_html(active_file, depth))


def footer_html(depth):
    r = rel(depth)
    contact = (r + "contact.html") if depth else "contact.html"
    socials = "".join('\n        <li><a href="%s" target="_blank" rel="noopener">%s</a></li>' % (u, label) for label, _t, u in SOCIALS)
    return ("""  <footer class="site-footer">
    <div class="footer-inner wrap">
      <p>&copy; 2026 %s</p>
      <ul class="footer-links">
        <li><a href="%s">Contact</a></li>@@SOCIALS@@
      </ul>
    </div>
  </footer>
  <script src="%sjs/site.js" defer></script>""" % (AUTHOR, contact, r)).replace("@@SOCIALS@@", socials)


def page(title, description, depth, active_file, body):
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
""" % (head_html(title, description, depth), header_html(active_file, depth), body, footer_html(depth))


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
      </li>""" % (full, grid, s["alt"], s["caption_html"]))
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


def _index_body_base():
    book_items = "\n".join(book_entry_html(b, 0) for b in BOOKS)
    lore_items = "\n".join(
        "          <li><a href=\"lore/%s.html\">%s</a></li>" % (l["slug"], l["name"])
        for l in LORE
    )
    return """    <section class="hero">
      <div class="wrap">
        <h1>%s</h1>
        <p class="tagline">Speculative fiction. The fragility of human systems, one kingdom at a time.</p>
        <p class="lede">%s writes speculative fiction about the rise and collapse of kingdoms, the evolution of faiths, and the small moments of pride, fear, and vanity that bring great structures down. This site collects the novels, and the lore behind them.</p>
        <ul class="hero-links">
          <li><a href="books.html">Read the books</a></li>
          <li><a href="lore.html">Browse the lore</a></li>
        </ul>
        @@LEDGER@@
      </div>
    </section>

    <section class="section wrap">
      <h2>Books</h2>
      <ul class="catalog-list">
%s
      </ul>
    </section>

@@SECTIONS@@
    <section class="section wrap">
      <h2>Lore</h2>
      <p>A glossary of terms and systems from the setting.</p>
      <ul class="index-list">
%s
      </ul>
      <p><a href="lore.html">See the full glossary</a></p>
    </section>
""" % (AUTHOR, AUTHOR, book_items, lore_items)


ROSTER = {
    "envoy": ("Envoys", "One per case, in the order the books appear on this site."),
    "catalyst": ("Catalysts", "One per case, in the order the books appear on this site."),
}

# One scene per book for the homepage band: (book slug, scene slug).
HOME_SCENES = [("0000", "valeria-full-power"), ("4099", "tower-burning"),
               ("0157", "vartaz-and-the-floor"), ("4417", "the-chrome-heels"),
               ("4420", "yvaine-in-the-south"), ("4555", "the-beam-finds-blakk")]


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
    ledger = '<p class="ledger-line">%d cases on file &middot; %d characters &middot; %d scenes</p>' % (len(BOOKS), n_chars, n_scenes)
    sections = """    <section class="section wrap">
      <h2>Cast</h2>
      <p>A few faces from each case &mdash; every character has a page of their own.</p>
      <ul class="wall">
%s
      </ul>
    </section>

    <section class="section wrap">
      <h2>Scenes</h2>
      <ul class="wall wall--scenes">
%s
      </ul>
    </section>
""" % (home_wall_html(), home_scenes_html())
    return _index_body_base().replace("@@LEDGER@@", ledger).replace("@@SECTIONS@@", sections)


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
      <a class="back-link" href="%s">&larr; All Lore</a>
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
    </div>
""" % (lore_href, l["name"], l["definition_html"], second)


def books_body():
    entries = "\n".join(book_entry_html(b, 0) for b in BOOKS)
    return """    <section class="hero hero--compact">
      <div class="wrap">
        <h1>Book</h1>
        <p class="lede">Each novel below opens into its own page: book info, characters, key scenes, and where to read it.</p>
      </div>
    </section>

    <section class="wrap page-content">
      <ul class="catalog-list">
%s
      </ul>
    </section>
""" % entries


def lore_index_html(depth):
    r = rel(depth)
    items = []
    for l in LORE:
        href = "%slore/%s.html" % (r, l["slug"])
        items.append("<li><strong><a href=\"%s\">%s</a></strong> &mdash; %s</li>" % (href, l["name"], l["teaser"]))
    return "<ul class=\"detail-list\">" + "".join(items) + "</ul>"


def lore_body():
    return """    <section class="hero hero--compact">
      <div class="wrap">
        <h1>Lore</h1>
        <p class="lede">A glossary of terms and systems from the setting &mdash; growing as new books add to it.</p>
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

    if any(s != "coming-soon" for s in b["status"]):
        links = []
        if "google-books" in b["status"]:
            links.append('<li><a class="button-link" href="%s" target="_blank" rel="noopener">View on Google Books</a></li>' % b.get("google_books_url", "#"))
        if "kindle" in b["status"]:
            links.append('<li><a class="button-link" href="%s" target="_blank" rel="noopener">View on Kindle</a></li>' % b.get("kindle_url", "#"))
        if "royal-road" in b["status"]:
            links.append('<li><a class="button-link" href="%s" target="_blank" rel="noopener">Read on Royal Road</a></li>' % b.get("royal_road_url", "#"))
        read_section = "<ul class=\"button-list\">\n            " + "\n            ".join(links) + "\n          </ul>"
    else:
        read_section = "<p>Not yet available &mdash; this panel will link out once there is somewhere to read it.</p>"

    case_tag_html = '<p class="case-tag">%s</p>\n          ' % b["case_tag"] if b.get("case_tag") else ""

    if b["scenes"]:
        scenes_section = """<div class="scene-header">
          <h2>Scenes</h2>
          <div class="scene-nav">
            <button type="button" class="scene-btn scene-btn--prev" aria-label="Previous scene">&lsaquo;</button>
            <button type="button" class="scene-btn scene-btn--next" aria-label="Next scene">&rsaquo;</button>
          </div>
        </div>
        <ul class="scene-gallery" tabindex="0" aria-label="Scenes, %d images, scroll horizontally or use the buttons above">
%s
        </ul>""" % (len(b["scenes"]), scene_gallery_html(b, 1))
    else:
        scenes_section = """<h2>Scenes</h2>
        <p class="editor-note">Add scene illustrations here once they're ready.</p>"""

    if b["characters"]:
        characters_section = """<h2>Characters</h2>
        <ul class="catalog-list">
%s
        </ul>""" % characters_index_html(b, 1)
    else:
        characters_section = """<h2>Characters</h2>
        <p class="editor-note">Character roster coming soon.</p>"""

    return """    <div class="wrap page-content">
      <a class="back-link" href="%s">&larr; All Books</a>
      <div class="detail-header">
        <a class="lightbox-link" data-group="covers" href="#" data-full="%s"><img class="detail-cover" src="%s" alt="Cover of %s"></a>
        <div class="detail-meta">
          %s<h1>%s</h1>
          %s
        </div>
      </div>

      <div class="prose">
        <section class="subsection">
          <h2>Book Info</h2>
          <ul class="detail-list">
            <li><strong>Pages</strong> &mdash; %s</li>
            <li><strong>Genre</strong> &mdash; %s</li>
          </ul>
          %s
        </section>
      </div>

      <section class="subsection">
        %s
      </section>

      <section class="subsection">
        %s
      </section>

      <div class="prose">
        <section class="subsection purchase-panel">
          <h2>Read This Book</h2>
          %s
        </section>
      </div>
    </div>
""" % (books_href, cover_src, cover_src, b["title"], case_tag_html, b["title"], tags_html(b), b["pages"], b["genre"],
       b["synopsis_html"], characters_section, scenes_section, read_section)


def character_detail_body(c, book):
    r = rel(1)
    book_href = "%sbooks/%s.html" % (r, book["slug"])
    full_src = "%simages/characters/%s.jpg" % (r, c["slug"])
    quote_html = "<blockquote>&ldquo;%s&rdquo;</blockquote>" % c["quote"] if c.get("quote") else ""
    return """    <div class="wrap page-content">
      <a class="back-link" href="%sbooks.html">&larr; All Books</a>
      <div class="character-entry">
        <a class="lightbox-link" data-group="characters" href="#" data-full="%s"><img class="character-portrait" src="%s" alt="Character reference sheet for %s"></a>
        <div>
          <h1>%s</h1>
          <p class="character-epithets">%s</p>
          %s
          %s
        </div>
      </div>
      <p>Appears in <a href="%s">%s</a></p>
    </div>
""" % (r, full_src, full_src, c["name"], c["name"], c["epithets"], c["bio_html"], quote_html, book_href, book["title"])


def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", path, len(content), "bytes")


# ---- top-level pages ---------------------------------------------------------
write("index.html", page("%s \u2014 Speculative Fiction Author" % AUTHOR,
                          "Speculative fiction novels and the lore behind them.", 0, "index.html", index_body()))
write("books.html", page("Book \u2014 %s" % AUTHOR,
                          "The novels, and where to read them.", 0, "books.html", books_body()))
write("lore.html", page("Lore \u2014 %s" % AUTHOR,
                         "A glossary of terms and systems from the setting.", 0, "lore.html", lore_body()))
write("about.html", page("About \u2014 %s" % AUTHOR,
                          "Biography.", 0, "about.html", about_body()))
write("contact.html", page("Contact \u2014 %s" % AUTHOR,
                            "Get in touch.", 0, "contact.html", contact_body()))

# ---- book detail pages, and each book's characters ----------------------------
for book in BOOKS:
    write("books/%s.html" % book["slug"],
          page("%s \u2014 %s" % (book["title"], AUTHOR),
               "%s Book info, characters, and where to read it." % book["hook"],
               1, "books.html", book_detail_body(book)))

    for c in book["characters"]:
        write("characters/%s.html" % c["slug"],
              page("%s \u2014 %s" % (c["name"], AUTHOR),
                   "%s" % c["teaser"],
                   1, "books.html", character_detail_body(c, book)))

# ---- lore detail pages ---------------------------------------------------------
for l in LORE:
    write("lore/%s.html" % l["slug"],
          page("%s \u2014 %s" % (l["name"], AUTHOR),
               "%s Definition and where it appears." % l["teaser"],
               1, "lore.html", lore_detail_body(l)))

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
""" % (target, target, target, target))

print("done")
