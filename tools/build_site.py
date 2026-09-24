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

BOOKS = [
    {
        "slug": "0000", "title": "The Sword of Valeria",
        "status": ["published", "google-books", "royal-road"],
        "cover_file": "0000.jpg",
        "hook": "A reckoner's life, and the sword that outlived his name.",
        "case_tag": "Case 0000",
        "pages": "102",
        "genre": """Epic Fantasy <span class="editor-note">(suggested &mdash; confirm or edit)</span>""",
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
        "pages": "96",
        "genre": """Epic Fantasy <span class="editor-note">(suggested &mdash; confirm or edit)</span>""",
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
                "slug": "the-weaver-falls",
                "alt": "A towering pale, veiled guardian with long flowing hair and elongated limbs is run through with a sword by a delver",
                "caption_html": """<a href="../characters/the-weaver-who-outlived-her-thread.html">The Weaver Who Outlived Her Thread</a> falls.""",
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
        "pages": """~105 <span class="editor-note">(estimated from manuscript word count &mdash; confirm or edit)</span>""",
        "genre": """Epic Fantasy &middot; Political Intrigue &middot; War &amp; Military Fiction <span class="editor-note">(suggested &mdash; confirm or edit)</span>""",
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
                "slug": "the-chrome-heels",
                "alt": "A pair of mirror-polished chrome stiletto heels resting on a stone dais, draped in a red and gold cloth",
                "caption_html": """The chrome heels themselves.""",
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
        ],
    },
]

LORE = [
    {
        "slug": "cultivator", "name": "Cultivator",
        "teaser": "The observers who deliver Catalysts to chosen subjects across worlds.",
        "definition_html": """<p>A loose, still-forming collective of offices and field agents &mdash; simply &ldquo;observers&rdquo; in the earliest records &mdash; who select subjects across many worlds and deliver a Catalyst directly into their hands, then spend the rest of that subject's life quietly filing reports on what the world does with it. Field agents appear to work through numbered &ldquo;deployment archetypes&rdquo; &mdash; disguises suited to whatever world they're entering, from an itinerant confectioner to whatever delivered the sword Valeria. The name &ldquo;Cultivator&rdquo; wasn't settled on until long after the practice began.</p>""",
        "appears_html": """<p>In <a href="../books/0000.html">The Sword of Valeria</a>, delivered by <a href="../characters/ardwen.html">Ardwen</a>, Observer 000. In <a href="../books/4099.html">The Ledger of a Single Sweetness</a>, delivered by <a href="../characters/observer-4099.html">an unnamed Envoy</a> posing as a traveling confectioner &mdash; a different, much later field agent, going by his own count. In <a href="../books/0157.html">The Stolen Prince War</a>, the Catalyst is <a href="../characters/the-golden-catacomb.html">the Golden Catacomb</a> itself, delivered less as a gift than as a discovery; its Observer, <a href="../characters/observer-0157.html">presenting as an ordinary old man</a>, keeps a permanent seat at the bottom of his own construction rather than a disguise out in the world. In <a href="../books/4417.html">The Iron Stiletto War</a>, delivered by <a href="../characters/vane.html">Vane</a>, deployed disguised as a wandering hermit.</p>""",
    },
    {
        "slug": "catalyst-tier", "name": "Catalyst Tier",
        "teaser": "A classification system for the cases the Cultivators file.",
        "definition_html": """<p>Cases &mdash; and the Catalysts at the center of them &mdash; appear to be classified by numbered range. <a href="../books/4099.html">The Ledger of a Single Sweetness</a> confirms one such range directly: Case 4099 is filed under &ldquo;Mundane Class&rdquo; (4000&ndash;4999), which suggests a jar of candy counts as a fairly ordinary intervention by Cultivator standards. Case 4417 (<a href="../books/4417.html">The Iron Stiletto War</a>) falls in the same numbered range, which makes it another data point for the same range. <a href="../books/0157.html">The Stolen Prince War</a> confirms a second class, directly: Case 0157 is filed as &ldquo;Mythic Class,&rdquo; with no numbered range given &mdash; a hundred-level structure with a real gold vein under it apparently rates rather higher than a jar of candy.</p>
          <p class="editor-note">Two classes confirmed now (Mundane, Mythic), but not the full system: what separates them, what other classes exist between or beyond them, and where a Catalyst like the sword Valeria (Case 0000) fits by comparison, isn't established yet. Add the rest of the tier system here once it's settled.</p>""",
        "appears_html": """<p><a href="../books/4099.html">The Ledger of a Single Sweetness</a>, where Case 4099's &ldquo;Mundane Class&rdquo; designation is given directly. <a href="../books/4417.html">The Iron Stiletto War</a>, whose Case 4417 falls in the same 4000&ndash;4999 range. <a href="../books/0157.html">The Stolen Prince War</a>, where Case 0157's &ldquo;Mythic Class&rdquo; designation is given directly. Also relevant to <a href="../books/0000.html">The Sword of Valeria</a>, whose Case 0000 has no confirmed classification yet.</p>""",
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
    return """  <footer class="site-footer">
    <div class="footer-inner wrap">
      <p>&copy; 2026 %s</p>
      <ul class="footer-links">
        <li><a href="%s">Contact</a></li>
      </ul>
    </div>
  </footer>
  <script src="%sjs/site.js" defer></script>""" % (AUTHOR, contact, r)


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
        <a class="lightbox-link" data-group="characters" href="%s"><img class="entry-portrait" src="%s" alt="Portrait of %s"></a>
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
        <a class="lightbox-link" data-group="scenes" href="%s"><img src="%s" alt="%s"></a>
        <p class="scene-caption">%s</p>
      </li>""" % (full, grid, s["alt"], s["caption_html"]))
    return "\n".join(items)


def book_entry_html(book, depth):
    r = rel(depth)
    book_href = "%sbooks/%s.html" % (r, book["slug"])
    cover_src = "%simages/covers/%s" % (r, book["cover_file"])
    return """      <article class="entry">
        <a class="lightbox-link" data-group="covers" href="%s"><img class="entry-cover" src="%s" alt="Cover of %s"></a>
        <div class="entry-body">
          <h3 class="entry-title"><a href="%s">%s</a></h3>
          %s
          <p>%s</p>
          <p class="entry-links"><a class="entry-link" href="%s">Read the full entry</a></p>
        </div>
      </article>""" % (cover_src, cover_src, book["title"], book_href, book["title"], tags_html(book), book["hook"], book_href)


def index_body():
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
      </div>
    </section>

    <section class="section wrap">
      <h2>Books</h2>
      <ul class="catalog-list">
%s
      </ul>
    </section>

    <section class="section wrap">
      <h2>Lore</h2>
      <p>A glossary of terms and systems from the setting.</p>
      <ul class="index-list">
%s
      </ul>
      <p><a href="lore.html">See the full glossary</a></p>
    </section>
""" % (AUTHOR, AUTHOR, book_items, lore_items)


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


def contact_body():
    return """    <section class="hero hero--compact">
      <div class="wrap">
        <h1>Contact</h1>
      </div>
    </section>

    <section class="wrap page-content">
      <div class="prose">
        <section class="subsection">
          <!-- Replace the handles and address below with the real accounts. -->
          <ul class="detail-list">
            <li><strong>Instagram</strong> &mdash; <a href="https://instagram.com/yourhandle" target="_blank" rel="noopener">@yourhandle</a></li>
            <li><strong>Threads</strong> &mdash; <a href="https://www.threads.net/@yourhandle" target="_blank" rel="noopener">@yourhandle</a></li>
            <li><strong>Email</strong> &mdash; <a href="mailto:author@example.com">author@example.com</a></li>
          </ul>
        </section>
      </div>
    </section>
"""


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

    return """    <div class="wrap page-content">
      <a class="back-link" href="%s">&larr; All Books</a>
      <div class="detail-header">
        <a class="lightbox-link" data-group="covers" href="%s"><img class="detail-cover" src="%s" alt="Cover of %s"></a>
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
        <h2>Characters</h2>
        <ul class="catalog-list">
%s
        </ul>
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
       b["synopsis_html"], characters_index_html(b, 1), scenes_section, read_section)


def lore_detail_body(l):
    r = rel(1)
    lore_href = "%slore.html" % r
    return """    <div class="wrap page-content">
      <a class="back-link" href="%s">&larr; All Lore</a>
      <h1>%s</h1>

      <div class="prose">
        <section class="subsection">
          <h2>Definition</h2>
          %s
        </section>

        <section class="subsection">
          <h2>Appears In</h2>
          %s
        </section>
      </div>
    </div>
""" % (lore_href, l["name"], l["definition_html"], l["appears_html"])


def character_detail_body(c, book):
    r = rel(1)
    book_href = "%sbooks/%s.html" % (r, book["slug"])
    full_src = "%simages/characters/%s.jpg" % (r, c["slug"])
    quote_html = "<blockquote>&ldquo;%s&rdquo;</blockquote>" % c["quote"] if c.get("quote") else ""
    return """    <div class="wrap page-content">
      <a class="back-link" href="%sbooks.html">&larr; All Books</a>
      <div class="character-entry">
        <a class="lightbox-link" data-group="characters" href="%s"><img class="character-portrait" src="%s" alt="Character reference sheet for %s"></a>
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

print("done")
