# -*- coding: utf-8 -*-
"""All copy and configuration for the Ben Potter site. Edit here, then run build.py."""

# ---------------------------------------------------------------- configuration
# TODO before launch: confirm every value in this block with Ben.
SITE          = "https://www.ben-potter.com"   # production origin, used for canonical/OG/sitemap
PREVIEW       = True          # True adds noindex and a disallow-all robots.txt. Flip to False at launch.
GA4_ID        = ""            # e.g. "G-XXXXXXXXXX"; leave empty to omit the tag entirely
GSC_TOKEN     = ""            # Search Console HTML-tag verification token, if that method is used

AGENT_NAME    = "Ben Potter"
AGENCY        = "Harcourts Cooper & Co"
OFFICE        = "Harcourts Cooper & Co, Devonport"
STREET        = ""            # TODO: Devonport office street address, needed for local SEO
LOCALITY      = "Devonport"
REGION        = "Auckland"
POSTCODE      = "0624"
COUNTRY       = "NZ"
PHONE_DISPLAY = "027 953 0210"
PHONE_LINK    = "+64279530210"
EMAIL         = "ben.potter@harcourts.co.nz"   # TODO: confirm, this is an assumed Harcourts format
YEARS         = 38

SAMEAS = [
    "https://harcourts.net/nz/office/devonport/people/ben-potter",
    "https://www.ratemyagent.co.nz/real-estate-agent/ben-potter-as455/sales/overview",
    "https://www.facebook.com/Harcourts.Ben.Gary.Potter",
    "https://www.instagram.com/north.shore.real.estate/",
    "https://www.tiktok.com/@auckland.real.estate",
]
RATEMYAGENT = "https://www.ratemyagent.co.nz/real-estate-agent/ben-potter-as455/sales/overview"
GOOGLE_MAPS = "https://maps.app.goo.gl/TyrUAvvceLsmfppPA"

OG_IMAGE = "img/og-ben-potter-devonport-real-estate.jpg"
HERO_IMG = "img/ben-potter-devonport-real-estate-agent"
HERO_ALT = ("Ben Potter, Harcourts Cooper & Co real estate agent for Devonport, "
            "Belmont and Bayswater")

# Old ben-potter.com paths that must keep their search equity.
REDIRECTS = [
    ("/listings", "/recently-sold/"),
    ("/listings/", "/recently-sold/"),
]

# ---------------------------------------------------------------- shared copy
SUPPORT_COPY = ("Ben Potter has been on the Devonport Peninsula for 38 years and specialises in "
                "selling homes across Devonport, Belmont and Bayswater, with extensive experience "
                "across the wider North Shore market.")

ABOUT = [
    "Ben Potter brings a rare blend of energy, experience and a fresh outlook to real estate on "
    "Auckland's North Shore. Thirty-eight years living across Devonport, Belmont and Bayswater have "
    "given him the kind of knowledge that can't be learned from a spreadsheet: which streets are "
    "tightly held, which buyers are waiting, and what a home needs to look like before they walk "
    "through the door.",
    "His drive to deliver premium results, paired with a genuine passion for people and property, is "
    "why locals trust him with the peninsula's most sought-after homes. Ben doesn't cover these "
    "suburbs. He lives in them.",
]

# ---------------------------------------------------------------- listings
# (suburb, street, meta, result, status)
SOLD = [
    ("Bayswater", "Roberts Avenue", "4 bed · 2 bath · 612 m²", "Auction, three registered bidders", "Sold · Aug 2026"),
    ("Devonport", "Old Lake Road", "4 bed · 2 bath · 506 m²", "Sold prior to auction in nine days", "Sold · Jul 2026"),
    ("Belmont", "Kiri Place", "5 bed · 3 bath · 809 m²", "Deadline sale", "Sold · Jul 2026"),
    ("Devonport", "Mozeley Avenue", "4 bed · 2 bath · 675 m²", "Off market to a local buyer", "Sold · Jun 2026"),
    ("Belmont", "Seabreeze Road", "3 bed · 2 bath · 450 m²", "Auction, above reserve", "Sold · May 2026"),
    ("Devonport", "Vauxhall Road", "3 bed · 1 bath · 380 m²", "By negotiation in three weeks", "Sold · May 2026"),
]
SALE = [
    ("Devonport", "Cheltenham Road", "4 bed · 2 bath · 720 m²", "Open home Sat and Sun, 12.00", "Auction · 8 October"),
    ("Belmont", "Bardia Street", "3 bed · 2 bath · 405 m²", "Open home Sun, 1.00", "Deadline · 2 October"),
]

REVIEWS = [
    ("Ben knew exactly who would buy our villa before we'd even signed with him. Sold in ten days, "
     "above what two other agents told us to expect.", "Sarah and James", "Sold in Devonport"),
    ("Straight talking, no pressure, and he did everything he said he would. We've used Ben twice now "
     "and would use him again without a second thought.", "Mark T.", "Sold in Belmont"),
    ("Ben's advice on what to fix and what to leave alone saved us thousands. The campaign was quiet "
     "and classy, and the result was better than we hoped.", "The Nguyen family", "Sold in Bayswater"),
]

# ---------------------------------------------------------------- homepage FAQ
FAQ_HOME = [
    ("Who is Ben Potter?",
     "Ben Potter is a licensed real estate salesperson with Harcourts Cooper &amp; Co in Devonport. He has "
     "lived on the Devonport Peninsula for 38 years and sells homes across Devonport, Belmont and "
     "Bayswater, along with Narrow Neck, Stanley Point, Hauraki and Takapuna."),
    ("Which areas does Ben sell in?",
     "Devonport, Belmont and Bayswater are his core suburbs, and he regularly sells in the neighbouring "
     "pockets of Narrow Neck, Stanley Point, Hauraki and Takapuna. Working a small, well defined patch is "
     "deliberate: it means he knows the buyers who are already looking on your street."),
    ("How do I get a free property appraisal?",
     "Fill in the form on the appraisal page or call Ben on 027 953 0210. Appraisals are free and come "
     "with no obligation. You'll get a written estimate of value based on recent comparable sales near "
     "you, a recommended method of sale, and a marketing plan and budget before you commit to anything."),
    ("How long does it take to sell a home on the peninsula?",
     "Most well priced homes in Devonport, Belmont and Bayswater sell within four to six weeks of going "
     "to market. Homes that are prepared properly before they list tend to sell faster and for more, "
     "which is why Ben prefers to talk to owners well before the sign goes up."),
    ("Should I sell by auction, deadline sale or a price?",
     "It depends on the home and how many buyers are likely to compete for it. Auction suits a tightly "
     "held character home where several buyers want the same street. A deadline sale often suits a family "
     "home with broad appeal. A price can be right for an apartment or a townhouse where buyers are "
     "comparing like for like. Ben recommends a method as part of the appraisal and explains the reasoning."),
    ("What does it cost to sell a house with Harcourts Cooper &amp; Co?",
     "Commission is agreed up front and is only payable when your home sells. Marketing costs depend on "
     "the campaign you choose. Ben provides a written estimate of both before you sign an agency "
     "agreement, so there are no surprises later."),
    ("Does Ben sell homes off market?",
     "Regularly. A good share of peninsula homes change hands quietly, to buyers already registered with "
     "Ben. If you're buying, register your brief so you hear about homes before they're advertised. If "
     "you're selling, a quiet approach to the right buyer can be part of the plan, though it's worth "
     "understanding the trade-offs first."),
    ("Is now a good time to sell on the North Shore?",
     "Well presented homes in Devonport, Belmont and Bayswater continue to find local buyers who are "
     "waiting for the right property. Whether now suits you depends on your home and your timing, and "
     "Ben will tell you honestly if he thinks you're better to prepare and wait."),
]

# ---------------------------------------------------------------- suburb pages
SUBURBS = [
    {
        "slug": "devonport-real-estate",
        "name": "Devonport",
        "coord": "36.8290° S · 174.7961° E",
        "lat": -36.8290, "lng": 174.7961,
        "h1": "Devonport real estate, street by street.",
        "title": "Devonport Real Estate Agent | Ben Potter, Harcourts Cooper & Co",
        "desc": ("Selling or buying in Devonport? Ben Potter has 38 years on the Devonport Peninsula and "
                 "specialises in the suburb's villas, character homes and tightly held streets. Free appraisals."),
        "card": ("Heritage villas, Cheltenham Beach and the ferry. The most tightly held streets on the "
                 "North Shore, where presentation and pricing matter more than anywhere else on the Peninsula."),
        "lede": ("Devonport is the village at the end of the peninsula: villas under mature trees, a working "
                 "naval base, two volcanic headlands and a twelve minute ferry into the city. It is also the "
                 "hardest part of the North Shore to buy into, because the people who live here tend to stay."),
        "blocks": [
            ("What sells here", [
                "Devonport's housing stock is unusually old for Auckland. Victorian and Edwardian villas "
                "from the 1880s through the 1910s dominate the streets around Victoria Road, Church Street "
                "and Calliope Road, with bay villas and transitional villas on the flat and Californian "
                "bungalows filling in the 1920s and 1930s.",
                "Along King Edward Parade and the Cheltenham foreshore you have the suburb's blue chip "
                "homes, where the view and the frontage carry the price. Up the slopes of Takarunga "
                "(Mount Victoria) and Maungauika (North Head) sites get steeper and views open up. Closer "
                "to the wharf there is a small apartment and townhouse market that suits downsizers and "
                "lock-up-and-leave buyers.",
            ]),
            ("Who is buying", [
                "Three groups compete for most Devonport homes. Professionals who want to commute by ferry "
                "and will pay for walkability to the wharf. Families who want a character home inside good "
                "school zones and are prepared to renovate. And downsizers, often selling a larger home "
                "elsewhere on the Shore, who want the village rather than a lifestyle block.",
                "Returning expats make up a steady fourth group, and they tend to arrive with a short list "
                "of streets rather than a budget. Knowing which of them is currently looking is usually "
                "worth more to a seller than any marketing spend.",
            ]),
            ("Selling a Devonport home", [
                "Much of Devonport sits inside the Auckland Unitary Plan's special character overlay, which "
                "shapes what can be altered, removed or added. Buyers know this, so a clean consent history "
                "and evidence that work was done properly are worth real money at auction.",
                "Villa buyers here inspect closely: piles and subfloor, roof and spouting, weatherboard and "
                "joinery, drainage, and the quality of any past renovation. Ben's advice before a campaign "
                "is usually about presentation rather than renovation, because the return on a full "
                "renovation immediately before sale is rarely what owners expect.",
                "Auction works well on a tightly held street where several buyers want the same thing at the "
                "same time. Where a home is more specific, a deadline sale or a price can do better.",
            ]),
            ("Getting around", [
                "The Devonport ferry reaches the downtown terminal in about twelve minutes, which is the "
                "single strongest argument for the suburb and a genuine price driver for homes within an "
                "easy walk of the wharf. By road, everything funnels onto Lake Road, and buyers do factor "
                "the afternoon queue into what they will pay.",
            ]),
        ],
        "facts": [
            ("Housing stock", "Villas, bungalows, some apartments"),
            ("Typical section", "400 to 800 m²"),
            ("To the city", "About 12 minutes by ferry"),
            ("Schools", "Devonport Primary, Vauxhall, Stanley Bay"),
            ("Secondary", "Belmont Intermediate, Takapuna Grammar"),
            ("Character overlay", "Yes, across much of the suburb"),
        ],
        "landmarks": ("Cheltenham Beach, Windsor Reserve, the Victoria Road shops, Torpedo Bay, the Devonport "
                      "Library, Takarunga and Maungauika"),
        "faq": [
            ("What is my Devonport home worth?",
             "In Devonport the street, the section and the condition of the house matter more than the floor "
             "area. Two villas of the same size a block apart can be a long way apart in value. Ben tracks "
             "every peninsula sale and gives you a range built from comparable Devonport sales in the last "
             "six months, rather than a headline number designed to win the listing."),
            ("Can I renovate or extend a villa in Devonport?",
             "Often yes, but much of Devonport sits under a special character overlay, so what you can do to "
             "the street-facing form of the house is more limited than in most Auckland suburbs. Alterations "
             "at the rear and inside are usually more achievable. Talk to a planner early, and keep the "
             "paperwork, because buyers will ask for it."),
            ("Which Devonport streets are the most tightly held?",
             "The Cheltenham streets, the King Edward Parade waterfront and the pockets close to Victoria "
             "Road turn over rarely, and when they do the buyer is often someone who has been waiting for "
             "that street specifically. That is exactly the situation where an auction campaign earns its keep."),
            ("Is Devonport a good place to live with children?",
             "It suits families who value walkability. Devonport Primary, Vauxhall School and Stanley Bay "
             "School serve different parts of the suburb, Belmont Intermediate and Takapuna Grammar take the "
             "older years, and children can walk to two beaches and two headlands. Zones vary street by "
             "street, so confirm the address rather than the suburb."),
            ("How long does a Devonport home take to sell?",
             "A well prepared, sensibly priced Devonport home usually sells within four to six weeks, and "
             "character homes on sought-after streets often sell faster than that. Homes that stall are "
             "almost always priced against hope rather than against recent comparable sales."),
        ],
    },
    {
        "slug": "belmont-real-estate",
        "name": "Belmont",
        "coord": "36.8060° S · 174.7898° E",
        "lat": -36.8060, "lng": 174.7898,
        "h1": "Belmont real estate, inside the school zones.",
        "title": "Belmont Real Estate Agent | Ben Potter, Harcourts Cooper & Co",
        "desc": ("Thinking of selling in Belmont? Ben Potter knows the Takapuna Grammar and Belmont "
                 "Intermediate zones, the family homes and the buyers. 38 years on the peninsula. Free appraisals."),
        "card": ("Family homes on the flat between Devonport and Takapuna. Driven by the Takapuna Grammar "
                 "and Belmont Intermediate zones, generous sections and a short run up Lake Road."),
        "lede": ("Belmont is the practical middle of the peninsula. Flatter land, bigger sections, and the "
                 "school zones that decide where a great many North Shore families end up living. It is where "
                 "Devonport households move when they need another bedroom and a lawn."),
        "blocks": [
            ("What sells here", [
                "The backbone of Belmont is the post-war weatherboard bungalow on a full site: three "
                "bedrooms, one bathroom, a separate garage and a flat back lawn. A large share have been "
                "renovated and extended over the last two decades, and the gap between a thoughtful "
                "renovation and a tired original is one of the widest in the market.",
                "Newer townhouses have filled in closer to Lake Road and the Belmont shops, which gives "
                "first home buyers and downsizers a way into the zones. Cross-lease titles are common here "
                "and have a real effect on price, on what you can build, and on how long due diligence takes.",
            ]),
            ("Who is buying", [
                "Belmont's buyer is usually a family, and the school zone is usually the reason. Takapuna "
                "Grammar and Belmont Intermediate bring buyers from across Auckland, and many arrive having "
                "already worked out exactly which side of which street they need to be on.",
                "The second group is local: Devonport owners with a growing family who want level lawn and "
                "another bathroom, and older Belmont residents moving from the family home into a single "
                "level townhouse a few streets away.",
            ]),
            ("Selling a Belmont home", [
                "Get the zoning and the title right before you market. Confirm the school zone for the "
                "address, not the suburb, and have the answer in writing. If the title is cross-lease, deal "
                "with any unapproved alterations or an out of date flats plan early, because buyers' "
                "solicitors will find them and it costs you momentum in the middle of a campaign.",
                "Presentation is about family function here: show the flat lawn, show where a second living "
                "space or a fourth bedroom could go, and make the indoor to outdoor flow obvious. Site "
                "potential under the current zoning is worth understanding, because some Belmont buyers are "
                "assessing what can be built as much as what is there.",
                "Deadline sale suits a lot of Belmont homes: it gives every family time to do the school "
                "zone and building checks, while still creating a single decision point.",
            ]),
            ("Getting around", [
                "Belmont sits on Lake Road with Takapuna a few minutes north and Devonport a few minutes "
                "south. The Bayswater ferry is a short drive or a walk from the western streets, which "
                "matters to buyers commuting into the city, and Ngataringa Bay borders the suburb on that "
                "side.",
            ]),
        ],
        "facts": [
            ("Housing stock", "1950s and 60s bungalows, newer townhouses"),
            ("Typical section", "500 to 800 m², often cross-lease"),
            ("Schools", "Belmont Primary, Belmont Intermediate"),
            ("Secondary", "Takapuna Grammar zone"),
            ("To Takapuna", "A few minutes up Lake Road"),
            ("Ferry", "Bayswater, a short drive or walk"),
        ],
        "landmarks": ("the Belmont shops, Ngataringa Bay, Belmont Park, Lake Road and the walk through to "
                      "Bayswater Marina"),
        "faq": [
            ("Is Belmont in the Takapuna Grammar zone?",
             "Most of Belmont sits inside the Takapuna Grammar enrolment scheme, and Belmont Intermediate "
             "covers the intermediate years, but the boundaries follow streets rather than suburb lines. "
             "Always confirm the specific address against the school's current zone map, and keep that "
             "confirmation with your sale documents, because buyers will ask."),
            ("What are houses selling for in Belmont?",
             "Belmont price depends heavily on the school zone, the title type, the section and how much "
             "renovation has already been done. A renovated four bedroom home on freehold land and an "
             "original three bedroom cross-lease are very different propositions. Ben provides current "
             "Belmont comparable sales with every appraisal, rather than a suburb average."),
            ("What is the difference between cross-lease and freehold in Belmont?",
             "A freehold title gives you the land outright. A cross-lease means you own a share of the whole "
             "site and lease your particular dwelling, so alterations usually need the other owners' consent "
             "and the flats plan has to match what is actually built. Cross-lease homes typically sell for "
             "less than comparable freehold homes, and fixing a defective cross-lease before a campaign can "
             "be worth doing."),
            ("Should I renovate before selling in Belmont?",
             "Usually not a full renovation. Belmont buyers pay for clean, functional family living, so "
             "paint, flooring, a tidy kitchen and bathroom, a well presented lawn and clear flow to the "
             "outdoors return more per dollar than a major project finished in a hurry. Ben walks through "
             "before the campaign and tells you what to leave alone."),
            ("Belmont, Hauraki or Takapuna: how do they compare?",
             "Belmont gives you the grammar zone with more land and a quieter street than Takapuna, "
             "generally at a lower price per square metre. Hauraki sits closer to Takapuna and tends to "
             "trade a little higher. Takapuna itself offers the beach and town centre but a smaller section "
             "or an apartment for the same money. Most buyers end up choosing between two of the three."),
        ],
    },
    {
        "slug": "bayswater-real-estate",
        "name": "Bayswater",
        "coord": "36.8163° S · 174.7727° E",
        "lat": -36.8163, "lng": 174.7727,
        "h1": "Bayswater real estate, on the harbour's edge.",
        "title": "Bayswater Real Estate Agent | Ben Potter, Harcourts Cooper & Co",
        "desc": ("Selling in Bayswater? Ben Potter knows the marina, the ferry, the view lines and the "
                 "buyers. 38 years on the Devonport Peninsula. Free, no obligation property appraisals."),
        "card": ("Water on three sides, the marina and views back to the city. Quieter than its neighbours: "
                 "townhouses on the ridge, weatherboard homes on the flat, the ferry at the end of the road."),
        "lede": ("Bayswater is the quiet one. A narrow finger of land with Ngataringa Bay on one side, the "
                 "Waitematā on the other, a marina at the tip and a ferry that puts the city closer than most "
                 "of the North Shore can manage. Buyers who find it tend to stop looking elsewhere."),
        "blocks": [
            ("What sells here", [
                "Two markets sit side by side. On the flat, weatherboard family homes on regular sections, "
                "many of them 1950s and 60s originals that have been extended over time. On the ridge and "
                "the slopes, elevated homes and townhouses where the view across the harbour to the city "
                "does most of the pricing work.",
                "Around the marina there is a smaller apartment and townhouse market that appeals to "
                "commuters and to boat owners who want to walk to the berth. New builds appear "
                "occasionally, and they sell quickly when the aspect is right.",
            ]),
            ("Who is buying", [
                "The ferry defines the Bayswater buyer. A large share are city workers who have done the "
                "maths on the commute and want to walk to the terminal rather than sit on Lake Road. Add "
                "buyers who wanted Devonport but found Bayswater gave them more house and closer water, and "
                "downsizers who want a single level home with a view.",
                "Boat owners are a distinct group here, and marina access genuinely changes what a home is "
                "worth to them.",
            ]),
            ("Selling a Bayswater home", [
                "Aspect and view line matter more than floor area. Two houses with the same plan can sit "
                "well apart in value depending on what they see and how the afternoon sun falls. Marketing "
                "has to prove the water proximity rather than assert it, which is where aerial photography "
                "earns its place on this side of the peninsula.",
                "Walking time to the ferry is a real, quotable selling point and worth measuring honestly "
                "rather than estimating. For homes on the flat, the job is to show the family function and "
                "the outdoor space. For homes on the ridge, the job is to show the view at the right time "
                "of day.",
                "Because the buyer pool is smaller and more specific than Devonport's, matching the method "
                "of sale to the likely number of competing buyers matters. Ben will tell you when an "
                "auction is likely to expose a thin field rather than create competition.",
            ]),
            ("Getting around", [
                "The Bayswater ferry runs from the marina into the downtown terminal and is the suburb's "
                "main advantage over the rest of the peninsula's northern end. By road it is Bayswater "
                "Avenue out to Lake Road, with Belmont and Takapuna a few minutes north and Devonport a few "
                "minutes south.",
            ]),
        ],
        "facts": [
            ("Housing stock", "Weatherboard homes, ridge townhouses, apartments"),
            ("Typical section", "400 to 700 m²"),
            ("To the city", "Ferry from Bayswater Marina"),
            ("Schools", "Bayswater School"),
            ("Secondary", "Belmont Intermediate, Takapuna Grammar"),
            ("Setting", "Water on three sides"),
        ],
        "landmarks": ("Bayswater Marina, Bayswater Park, O'Neills Point, Ngataringa Bay and the coastal walk "
                      "toward Belmont"),
        "faq": [
            ("How long is the ferry from Bayswater to the city?",
             "The Bayswater service runs from the marina into the downtown ferry terminal and is the reason "
             "a lot of buyers choose the suburb. Check the current timetable for sailing times, and if "
             "you're selling, measure the actual walk from your gate to the terminal, because buyers who "
             "care about the ferry care about that number precisely."),
            ("Do Bayswater homes with harbour views sell for more?",
             "Yes, and the premium is specific rather than general. What the view takes in, whether it is "
             "protected by the homes below, and how the afternoon light falls all affect it. Elevated homes "
             "on the ridge and well sited homes near the water consistently outperform equivalent floor "
             "area without an outlook."),
            ("Is Bayswater cheaper than Devonport?",
             "Usually, for a comparable house. Devonport carries a premium for the village, the character "
             "housing stock and the shorter ferry ride. Buyers who move their search to Bayswater often "
             "find they get more house, more section or a better outlook for the same money, and give up "
             "the walk to Victoria Road."),
            ("What is the Bayswater Marina like for boat owners?",
             "The marina sits at the end of the peninsula and is a genuine draw for buyers with a boat, "
             "since it puts the berth within walking distance of home. Berth availability changes, so if it "
             "is part of your buying decision it pays to look into it in parallel with the house search."),
            ("Which schools serve Bayswater?",
             "Bayswater School covers the primary years, with Belmont Intermediate and Takapuna Grammar "
             "taking the older years. As everywhere on the peninsula, enrolment zones follow streets, so "
             "confirm the zone for the exact address before you rely on it."),
        ],
    },
]

# ---------------------------------------------------------------- appraisal page
APPRAISAL_STEPS = [
    ("A walk through the house",
     "Ben visits in person, usually for half an hour to an hour. He looks at the home the way a buyer "
     "will, and asks what you're planning and when."),
    ("Comparable sales, in writing",
     "You receive a written estimate of value built from recent comparable sales near you, not a suburb "
     "average and not a number chosen to win your business."),
    ("A recommended method and plan",
     "Auction, deadline sale or a price, with the reasoning, plus a marketing plan, a budget and a "
     "timeline so you can see the whole cost before you commit."),
    ("An honest view on preparation",
     "What to fix, what to leave alone and what is genuinely worth spending money on before the first "
     "open home. Often the most valuable part of the conversation."),
]

FAQ_APPRAISAL = [
    ("Is the appraisal really free?",
     "Yes. There is no cost and no obligation to list. Plenty of the appraisals Ben does are for owners "
     "who are a year or two away from selling, and that's genuinely useful for both sides."),
    ("How is an appraisal different from a valuation?",
     "An appraisal is a licensed salesperson's assessment of the likely selling range based on comparable "
     "sales and current buyer demand. A registered valuation is a formal document prepared by a registered "
     "valuer, which is what a bank will usually want for lending purposes."),
    ("What should I have ready?",
     "Nothing is required, but the title, any recent building or renovation paperwork, and the school zone "
     "confirmation for your address all help. If you don't have them, Ben can point you to where they come "
     "from."),
    ("How quickly can Ben come out?",
     "Usually within a few days. Call 027 953 0210 if your timing is tight and he'll work around it."),
]

# ---------------------------------------------------------------- selling guide page
GUIDE_CONTENTS = [
    ("Preparing a peninsula home", "What actually returns money before a campaign, and what to leave alone."),
    ("Choosing a method of sale", "Auction, deadline sale or price, and how to tell which suits your home."),
    ("What a campaign costs", "Commission, marketing and the timeline, laid out plainly."),
    ("Presentation and photography", "Why the first twenty images decide how many people walk through the door."),
    ("Paperwork that slows sales down", "Cross-lease issues, unconsented work and school zone proof."),
    ("The last two weeks", "Open homes, buyer feedback and how to read it before you make a decision."),
]
