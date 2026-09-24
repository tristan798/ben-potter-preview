# -*- coding: utf-8 -*-
"""All copy and configuration for the Ben Potter site. Edit here, then run build.py."""

# ---------------------------------------------------------------- configuration
# TODO before launch: confirm every value in this block with Ben.
SITE          = "https://www.ben-potter.com"   # production origin, used for canonical/OG/sitemap
PREVIEW       = True          # True adds noindex and a disallow-all robots.txt. Flip to False at launch.
GA4_ID        = ""            # e.g. "G-XXXXXXXXXX"; leave empty to omit the tag entirely
GSC_TOKEN     = ""            # Search Console HTML-tag verification token, if that method is used

# Lead delivery. Appraisal and selling-guide submissions are emailed to LEAD_EMAIL.
# FORM_KEY is a free Web3Forms access key: go to https://web3forms.com, enter LEAD_EMAIL,
# confirm the verification email, paste the key here and rebuild. Until it is set, forms show
# the thank-you state but nothing is sent.
LEAD_EMAIL    = "ben.potter@harcourts.co.nz"
FORM_KEY      = ""

# Ben's Devonport / Belmont / Bayswater reel. Paste a YouTube or Vimeo EMBED url
# (e.g. https://www.youtube.com/embed/VIDEO_ID) and it plays in the About section.
REEL_EMBED    = ""

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
    "Auckland's North Shore. Nearly 40 years living and working around Devonport, Belmont and "
    "Bayswater have given him the kind of knowledge you can't learn online. Which streets are tightly "
    "held, which buyers are waiting, and what a home needs to look like before they walk through the "
    "door.",
    "His drive to deliver premium results, paired with a genuine passion for people and property, is "
    "why locals trust him with the Peninsula's most sought-after homes.",
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
    ("He was professional, helpful, and <mark>always available to answer my questions</mark> throughout "
     "the process. He made everything much less stressful and kept me informed every step of the way",
     "Heidi", "Sold in Devonport"),
    ("Ben helped me from the very beginning, with great advice on staging, marketing and quick responses "
     "throughout the campaign. He is very knowledgeable and professional and <mark>brought me the best "
     "result!</mark>",
     "Alex", "Sold in Bayswater"),
    ("Ben ran a comprehensive campaign. Marketing activities were thoroughly explored and tuned to the "
     "market conditions and time of the year. <mark>He worked hard, actively generating awareness and "
     "interest in the property.</mark>",
     "Trevor", "Sold in Belmont"),
]

# ---------------------------------------------------------------- homepage FAQ
FAQ_HOME = [
    ("Who is Ben Potter?",
     "Ben Potter is a licensed real estate salesperson with Harcourts Cooper &amp; Co in Devonport. He has "
     "been on the Devonport Peninsula for 38 years and sells homes across Devonport, Belmont, and "
     "Bayswater, as well as Narrow Neck, Stanley Point, Hauraki, and Takapuna. His father, Gary Potter, "
     "has been a trusted real estate agent in the same areas for close to 25 years."),
    ("Which areas does Ben sell in?",
     "Devonport, Belmont and Bayswater are his core suburbs, and he regularly sells in the neighbouring "
     "pockets of Narrow Neck, Stanley Point, Hauraki and Takapuna. Working a small, well-defined patch is "
     "deliberate: it means he knows the properties, the streets, and the buyers already looking in the "
     "neighbourhoods."),
    ("How do I get a free property appraisal?",
     "Fill in the form on the appraisal page or call Ben on 027 953 0210. Appraisals are free and "
     "obligation-free. You'll get a written estimate of value based on recent comparable sales near you, "
     "a recommended method of sale, and a marketing plan and budget before you commit to anything."),
    ("How long does it take to sell a home on the peninsula?",
     "Most well-priced homes in Devonport, Belmont and Bayswater sell within four to six weeks of going "
     "to market. Homes that are prepared properly before they list tend to sell faster and for more, "
     "which is why Ben prefers to talk to owners well before the sign goes up."),
    ("Should I sell by auction, deadline sale, tender or a price?",
     "The right method depends on the property, the likely buyer pool and the level of competition we "
     "expect to create. Auction can work particularly well when several buyers are likely to compete for "
     "the same home. A deadline sale can suit properties with broad appeal where buyers need time to "
     "complete their checks, while a priced campaign may work better when buyers are closely comparing "
     "similar properties. Tender can also help when flexibility around terms or timing matters. Ben "
     "recommends the method as part of the appraisal and explains the reasoning behind it, so the "
     "campaign is tailored to the property rather than following a one-size-fits-all approach."),
    ("What does it cost to sell a house?",
     "Commission is agreed up front and is only payable when your home sells. Marketing costs depend on "
     "the campaign you choose. Ben provides a written estimate of both before you sign an agency "
     "agreement, so there are no surprises later."),
    ("Does Ben sell homes off market?",
     "Regularly. A good share of Peninsula homes change hands quietly, to buyers already registered with "
     "Ben. If you're buying, register your brief so you hear about homes before they're advertised. If "
     "you're selling, a quiet approach to the right buyer can be part of the plan, though it's worth "
     "understanding the trade-offs first."),
    ("Is now a good time to sell my home?",
     "Well-presented homes on the North Shore continue to attract local buyers waiting for the right "
     "property. Whether now suits you depends on your home and your timing, and Ben will tell you "
     "honestly if he thinks you're better off preparing and waiting."),
]

# ---------------------------------------------------------------- suburb pages
SUBURBS = [
    {
        "slug": "devonport-real-estate",
        "name": "Devonport",
        "coord": "36.8290° S · 174.7961° E",
        "lat": -36.8290, "lng": 174.7961,
        "h1": "Devonport real estate<br>Street by street.",
        "title": "Devonport Real Estate Agent | Ben Potter, Harcourts Cooper & Co",
        "desc": ("Selling or buying in Devonport? Ben Potter has 38 years on the Devonport Peninsula and "
                 "specialises in the suburb's villas, character homes and tightly held streets. Free appraisals."),
        "card": ("Heritage villas, Cheltenham Beach and the ferry. Some of the North Shore's most tightly "
                 "held streets, where careful presentation, positioning and pricing are especially important."),
        "lede": ("Devonport is the village at the end of the Peninsula: heritage villas beneath mature "
                 "trees, a working naval base, two volcanic headlands and a twelve-minute ferry ride into "
                 "the city. It is one of the North Shore's most tightly held areas, with a strong sense of "
                 "community and relatively few homes changing hands at any one time."),
        "blocks": [
            ("What sells here", [
                "Devonport's housing stock is unusually old for Auckland. Victorian and Edwardian villas "
                "from the 1880s through the 1910s dominate the local streets. Bay villas and transitional "
                "villas on the flat, and Californian bungalows filling in the 1920s and 1930s.",
                "Along King Edward Parade and the Cheltenham foreshore, you have the suburb's blue-chip "
                "homes, where the view and the frontage carry the price. Up the slopes of Takarunga (Mount "
                "Victoria) and Maungauika (North Head), sites get steeper, and views open up. Closer to the "
                "wharf, there is a small apartment market that suits downsizers and lock-up-and-leave buyers.",
            ]),
            ("Who is buying", [
                "Three groups compete for most Devonport homes. Families who want a character home inside "
                "good school zones with safety and community as a priority. Professionals who want to "
                "commute by ferry and will pay for walkability to the wharf and the village. Also, "
                "downsizers, often selling a larger home elsewhere on the Shore, who want the smaller "
                "section rather than a lifestyle block.",
                "Returning expats make up a steady fourth group, and they tend to arrive with a short list "
                "of streets rather than a budget. Knowing which of them is currently looking is usually "
                "worth more to a seller than any marketing spend.",
            ]),
            ("Selling a Devonport home", [
                "Much of Devonport sits inside the Auckland Unitary Plan's special character overlay, which "
                "shapes what can be altered, removed or added. Buyers know this, so a clean consent history "
                "and evidence that work was done properly are worth real money at auction. Many central "
                "Devonport homes sit in the Single Housing Zone and offer some protections against major "
                "future developments in the neighbourhood.",
                "Villa buyers here inspect closely: piles and subfloor, roof and spouting, weatherboard and "
                "joinery, drainage, and the quality of any past renovation. Ben's advice before a campaign "
                "is usually about presentation rather than renovation.",
                "Auction works well on a tightly held street where several buyers want the same thing at "
                "the same time. Where a home is more specific, a deadline sale or tender may be a more "
                "strategic advantage.",
            ]),
            ("Getting around", [
                "The Devonport ferry reaches the downtown terminal in about twelve minutes, the suburb's "
                "strongest argument and a genuine price driver for homes within an easy walk of the wharf. "
                "By road, everything funnels onto Lake Road, and buyers do factor the afternoon queue into "
                "what they will pay.",
            ]),
        ],
        "facts": [
            ("Housing stock", "Villas and bungalows"),
            ("Typical section", "400 to 800 m²"),
            ("To the city", "About 12 minutes by ferry"),
            ("Schools", "Devonport Primary, Vauxhall Primary, Stanley Bay Primary"),
            ("Secondary", "Takapuna Grammar School"),
            ("Character overlay", "Yes, across much of the suburb"),
        ],
        "landmarks": ("Cheltenham Beach, Windsor Reserve, the Victoria Road shops, Torpedo Bay, the Devonport "
                      "Library, Takarunga and Maungauika"),
        "faq": [
            ("What is my Devonport home worth?",
             "In Devonport, the street, the section and the condition of the house can matter more than the "
             "floor area. Two villas of the same size a few blocks apart can be a long way apart in value. "
             "Ben tracks every peninsula sale and gives you a range built from comparable Devonport sales "
             "in the last six months, rather than a headline number designed to win the listing."),
            ("Can I renovate or extend a villa in Devonport?",
             "Often yes, but much of Devonport sits under a special character overlay, so what you can do "
             "to the street-facing form of the house is more limited than in most Auckland suburbs. Rear "
             "and internal alterations are usually more achievable. Talk to a planner and council early, "
             "and keep the paperwork, because buyers will ask for it."),
            ("Which Devonport streets are the most tightly held?",
             "Cheltenham, the waterfront and the streets close to the village are among the areas where "
             "homes can be held for long periods. When a well-positioned property does come to market, it "
             "can attract buyers who have been waiting specifically for that location. In those "
             "situations, a competitive auction campaign can be particularly effective."),
            ("Is Devonport a good place to live with children?",
             "One of the best areas for families. Devonport Primary, Vauxhall School and Stanley Bay School "
             "serve different parts of the suburb; Belmont Intermediate and Takapuna Grammar take the older "
             "years, and children can walk to beaches and parks safely."),
            ("How long does a Devonport home take to sell?",
             "A well-prepared, sensibly priced Devonport home usually sells within four to six weeks, and "
             "character homes on sought-after streets often sell faster. Homes that stall are almost always "
             "priced against hope rather than against recent comparable sales."),
        ],
    },
    {
        "slug": "belmont-real-estate",
        "name": "Belmont",
        "coord": "36.8060° S · 174.7898° E",
        "lat": -36.8060, "lng": 174.7898,
        "h1": "Belmont real estate<br>perfectly positioned.",
        "title": "Belmont Real Estate Agent | Ben Potter, Harcourts Cooper & Co",
        "desc": ("Thinking of selling in Belmont? Ben Potter knows the Takapuna Grammar and Belmont "
                 "Intermediate zones, the family homes and the buyers. 38 years on the peninsula. Free appraisals."),
        "card": ("Perfectly positioned between Devonport and Takapuna. From first-home buyers to the "
                 "ultra-wealthy. Older homes and brand-new offerings. Belmont has it all."),
        "lede": ("Belmont sits at the practical heart of the peninsula. With flat sections, more space and "
                 "easy connections across the North Shore, it has long appealed to families wanting room to "
                 "grow while staying close to the coast."),
        "blocks": [
            ("What sells here", [
                "The backbone of Belmont is the post-war weatherboard bungalow on a full site: three "
                "bedrooms, one bathroom, a garage and a flat back lawn. A large share have been renovated "
                "and extended over the last two decades, and the gap between a thoughtful renovation and a "
                "tired original is one of the widest in the market. Newer townhouses have filled in closer "
                "to Lake Road and the Belmont shops, which gives first home buyers and downsizers a way "
                "into the zones. The landscape is consistently changing, and prices range from first-home "
                "buyers to the ultra-wealthy.",
            ]),
            ("Who is buying", [
                "Belmont buyers are often families, with Takapuna Grammar and Belmont Intermediate a major "
                "part of the appeal. Many arrive already focused on particular streets and pockets within "
                "the suburb.",
                "There is also a strong local buyer pool: Devonport families looking for more space, "
                "Belmont owners downsizing into nearby townhouses, and younger buyers drawn to the "
                "combination of beaches, ferry access and everyday convenience.",
            ]),
            ("Selling a Belmont home", [
                "Presentation in Belmont is often about family function. Make the lawn, indoor-outdoor flow "
                "and flexible living spaces easy to understand. Show buyers how the home works day to day, "
                "where there is room to grow, and any genuine future potential the property may offer.",
                "The method of sale should suit the property and likely buyer pool. Deadline campaigns can "
                "work well where buyers want time to complete their checks while still creating a clear "
                "decision point. In other cases, auction may be more appropriate.",
            ]),
            ("Getting around", [
                "Belmont sits around Lake Road with Takapuna a few minutes north and Devonport a few "
                "minutes south. The Bayswater ferry is a short drive or a walk from the western streets, "
                "which matters to buyers commuting into the city. Numerous bus and cycle routes are easily "
                "available. Motorway access is only a few minutes away.",
            ]),
        ],
        "facts": [
            ("Housing stock", "1950s and 60s bungalows, new townhouses"),
            ("Typical section", "500 to 800 m²"),
            ("Schools", "Belmont Primary School, Belmont Intermediate School"),
            ("Secondary", "Takapuna Grammar School"),
            ("To Takapuna", "A few minutes up Lake Road"),
            ("Ferry", "Bayswater, a short drive or walk"),
        ],
        "landmarks": ("the Belmont shops, Ngataringa Bay, Belmont Park, Lake Road and the walk through to "
                      "Bayswater Marina"),
        "faq": [
            ("Is Belmont in the Takapuna Grammar zone?",
             "Yes, most of Belmont sits inside the Takapuna Grammar and Belmont Intermediate zone."),
            ("What are houses selling for in Belmont?",
             "Belmont prices depend heavily on the property. A renovated four-bedroom home on freehold land "
             "and an original three-bedroom cross-lease are very different propositions. Ben provides "
             "current Belmont comparable sales with every appraisal."),
            ("What is the difference between cross-lease and freehold in Belmont?",
             "A freehold title gives you the land outright. A cross-lease means you own a share of the "
             "whole site and lease your particular dwelling, so alterations usually need the other owners' "
             "consent and the flats plan has to match what is actually built. Cross-lease homes typically "
             "sell for less than comparable freehold homes, and fixing a defective cross-lease before a "
             "campaign can be worth doing. Ben can advise on this before the sale."),
            ("Should I renovate before selling in Belmont?",
             "Usually, not extensively. Belmont buyers tend to respond well to clean, functional family "
             "living, so targeted improvements such as fresh paint, updated flooring, a tidy kitchen or "
             "bathroom, well-presented outdoor areas and good indoor-outdoor flow can often have more "
             "impact than a major renovation rushed through before sale. Ben can walk through the property "
             "before the campaign and help prioritise where money is worth spending and where it may be "
             "better left alone. You can also download his free selling guide for practical advice on "
             "preparing and positioning your home to achieve the most money."),
            ("Belmont, Hauraki or Takapuna: how do they compare?",
             "Belmont offers the grammar zone, more land, and a quieter street than Takapuna, generally at "
             "a lower price per square metre. Hauraki sits closer to Takapuna and can trade a little "
             "higher. Takapuna itself offers the beach and town centre, but you get a smaller section for "
             "the same money."),
        ],
    },
    {
        "slug": "bayswater-real-estate",
        "name": "Bayswater",
        "coord": "36.8163° S · 174.7727° E",
        "lat": -36.8163, "lng": 174.7727,
        "h1": "Bayswater real estate<br>on the harbour's edge.",
        "title": "Bayswater Real Estate Agent | Ben Potter, Harcourts Cooper & Co",
        "desc": ("Selling in Bayswater? Ben Potter knows the marina, the ferry, the view lines and the "
                 "buyers. 38 years on the Devonport Peninsula. Free, no obligation property appraisals."),
        "card": ("Water on three sides: the marina and views back to the city. Larger sections still "
                 "quietly available. Ferry service to Auckland CBD at the end of the road."),
        "lede": ("Bayswater is the quiet one. A narrow finger of land with Ngataringa Bay on one side, the "
                 "Waitematā on the other, a marina at the tip and a ferry that puts the city closer than "
                 "most of the North Shore can manage. Still home of the Kiwi quarter-acre dream!"),
        "blocks": [
            ("What sells here", [
                "Everything from a character villa sitting proudly on a huge quarter-acre section where "
                "families and kids can still play cricket on the back lawn, to townhouses from the 1970s to "
                "modern masterpieces sitting on the water's edge.",
            ]),
            ("Who is buying", [
                "Bayswater attracts a mix of families, boat owners and city commuters. Families are drawn "
                "to the coastal setting, strong local schools, sense of safety and the relaxed community "
                "feel. Boat owners value the marina and immediate connection to the harbour, while "
                "commuters appreciate the convenience of the ferry and easy access to the city.",
            ]),
            ("Selling a Bayswater home", [
                "In Bayswater, value can come from the home itself, the land beneath it, or often a "
                "combination of both. Presentation matters, particularly when a property has a strong "
                "aspect to showcase. On the southern side, some homes capture impressive city skyline "
                "views, while the northern side is often prized for sun and light.",
                "Bayswater also has a remarkably broad range of properties, from modest homes and "
                "townhouses through to substantial waterfront residences. That variety means the marketing "
                "strategy needs to be tailored carefully to the individual property rather than treating "
                "the suburb as one market.",
            ]),
            ("Getting around", [
                "The Bayswater ferry runs from the marina into the downtown terminal and is the suburb's "
                "main advantage over the rest of the peninsula's northern end. By road, it is Bayswater "
                "Avenue out to Lake Road, with Belmont and Takapuna a few minutes north and Devonport a few "
                "minutes south.",
            ]),
        ],
        "facts": [
            ("Housing stock", "Character homes, midcentury and modern"),
            ("Typical section", "400 to 1000 m²"),
            ("To the city", "Ferry from Bayswater Marina"),
            ("Schools", "Bayswater School"),
            ("Secondary", "Belmont Intermediate, Takapuna Grammar"),
            ("Setting", "Water on three sides"),
        ],
        "landmarks": ("Bayswater Marina, Bayswater Park, O'Neills Point, Ngataringa Bay and the coastal walk "
                      "toward Belmont"),
        "faq": [
            ("How long is the ferry from Bayswater to the city?",
             "The ferry from Bayswater Marina to downtown Auckland takes around 10 to 15 minutes, making it "
             "one of the suburb's biggest drawcards for commuters. It is a particularly convenient option "
             "for locals who want quick access to the city while still living in a quieter coastal setting."),
            ("Do Bayswater homes with harbour views sell for more?",
             "Yes, and the premium is specific rather than general. What the view takes in, whether it is "
             "protected by the homes below, and how the afternoon light falls all affect it. Elevated homes "
             "on the ridge and well-sited homes near the water consistently outperform equivalent floor "
             "area without an outlook."),
            ("Is Bayswater cheaper than Devonport?",
             "Usually, for a comparable house. Devonport carries a premium for the village, the character "
             "housing stock and the shorter ferry ride. Buyers who move their search to Bayswater often "
             "find more house, more section, or a better outlook for the same money."),
            ("What is the Bayswater Marina like for boat owners?",
             "The marina sits at the end of the peninsula and is a genuine draw for boat owners, since it "
             "puts the berth within walking distance of home. Berth availability changes, so if it is part "
             "of your buying decision, it pays to look into it alongside the house search."),
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
