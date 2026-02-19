"""
MediaAgentIQ - Streamlit App
AI Agent Platform for Media & Broadcast Operations
Real-world use cases and demos
"""
import streamlit as st
import random
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="MediaAgentIQ",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { background-color: #1e293b; border-radius: 8px; }
    .caption-block { background: #1e293b; padding: 12px; border-radius: 8px; margin-bottom: 8px; border-left: 3px solid #6366f1; }
    .viral-card { background: linear-gradient(135deg, #1e293b, #0f172a); padding: 16px; border-radius: 12px; border: 1px solid #334155; }
    .issue-critical { border-left: 4px solid #ef4444; background: rgba(239,68,68,0.1); padding: 12px; border-radius: 8px; margin: 8px 0; }
    .issue-warning { border-left: 4px solid #f59e0b; background: rgba(245,158,11,0.1); padding: 12px; border-radius: 8px; margin: 8px 0; }
    .breaking-news { background: linear-gradient(90deg, #dc2626, #991b1b); padding: 12px 16px; border-radius: 8px; margin: 8px 0; }
</style>
""", unsafe_allow_html=True)


# ============== REALISTIC DEMO DATA ==============

# Caption Agent - Morning News Broadcast
DEMO_CAPTIONS = [
    {"start": 0.0, "end": 4.2, "text": "Good morning, I'm Sarah Mitchell, and this is WKRN Morning News.", "speaker": "Sarah Mitchell (Anchor)", "confidence": 0.99},
    {"start": 4.5, "end": 9.8, "text": "Breaking overnight: A massive fire has destroyed a warehouse in downtown Nashville.", "speaker": "Sarah Mitchell (Anchor)", "confidence": 0.98},
    {"start": 10.2, "end": 15.5, "text": "Fire crews responded around 2 AM and battled the blaze for nearly four hours.", "speaker": "Sarah Mitchell (Anchor)", "confidence": 0.97},
    {"start": 16.0, "end": 20.3, "text": "We go live now to reporter Jake Thompson at the scene. Jake, what's the latest?", "speaker": "Sarah Mitchell (Anchor)", "confidence": 0.98},
    {"start": 21.0, "end": 27.5, "text": "Sarah, as you can see behind me, crews are still working to contain hot spots.", "speaker": "Jake Thompson (Reporter)", "confidence": 0.96},
    {"start": 28.0, "end": 34.2, "text": "The warehouse, owned by Mitchell Distribution, stored electronics and furniture.", "speaker": "Jake Thompson (Reporter)", "confidence": 0.94},
    {"start": 34.8, "end": 41.0, "text": "Fire Chief Robert Anderson told me moments ago that the cause is under investigation.", "speaker": "Jake Thompson (Reporter)", "confidence": 0.97},
    {"start": 41.5, "end": 48.3, "text": "[Sound of sirens] You can hear additional units arriving now to assist with the operation.", "speaker": "Jake Thompson (Reporter)", "confidence": 0.89},
    {"start": 49.0, "end": 55.8, "text": "Thankfully, no injuries have been reported. The building was unoccupied at the time.", "speaker": "Jake Thompson (Reporter)", "confidence": 0.98},
    {"start": 56.2, "end": 62.0, "text": "We'll have more updates throughout the morning. Back to you, Sarah.", "speaker": "Jake Thompson (Reporter)", "confidence": 0.97},
    {"start": 62.5, "end": 68.4, "text": "Thank you, Jake. Stay safe out there. We'll check back with you at the top of the hour.", "speaker": "Sarah Mitchell (Anchor)", "confidence": 0.98},
    {"start": 69.0, "end": 75.5, "text": "In other news, the city council voted last night to approve the new downtown development project.", "speaker": "Sarah Mitchell (Anchor)", "confidence": 0.97},
    {"start": 76.0, "end": 82.3, "text": "The 500 million dollar project will include affordable housing and retail space.", "speaker": "Sarah Mitchell (Anchor)", "confidence": 0.96},
]

DEMO_QA_ISSUES = [
    {"type": "warning", "severity": "medium", "segment": 8, "timestamp": "00:41.5", "issue": "Low confidence - Background noise", "details": "Sirens affecting speech recognition accuracy (89%)", "suggestion": "Review and manually verify transcript"},
    {"type": "info", "severity": "low", "segment": 4, "timestamp": "00:21.0", "issue": "Speaker change detected", "details": "Transition from Anchor to Field Reporter", "suggestion": "Verify speaker label is correct"},
    {"type": "info", "severity": "low", "segment": 11, "timestamp": "01:02.5", "issue": "Speaker change detected", "details": "Transition back to Anchor", "suggestion": "Verify speaker label is correct"},
    {"type": "success", "severity": "none", "segment": None, "timestamp": None, "issue": "Timing validation passed", "details": "All segments properly synchronized with no gaps >3s", "suggestion": None},
    {"type": "success", "severity": "none", "segment": None, "timestamp": None, "issue": "Profanity scan clear", "details": "No profanity or inappropriate content detected", "suggestion": None},
]

# Clip Agent - Viral Moments from Live Broadcast
DEMO_VIRAL_MOMENTS = [
    {
        "id": 1,
        "start": 145.2,
        "end": 162.8,
        "title": "🔥 Reporter's Close Call with Debris",
        "description": "Live reporter narrowly dodges falling debris during warehouse fire coverage. Dramatic moment captured on air.",
        "transcript": "Whoa! As you can see— [debris falls] —we're moving back now. That was close. The structural integrity is clearly compromised...",
        "score": 0.97,
        "emotion": "shock/drama",
        "predicted_views": "500K - 2M",
        "platforms": ["TikTok", "Twitter/X", "Instagram Reels"],
        "hashtags": ["#Breaking", "#CloseCall", "#LiveTV", "#Reporter", "#Dramatic"]
    },
    {
        "id": 2,
        "start": 892.5,
        "end": 918.0,
        "title": "😢 Emotional Reunion: Lost Dog Found After Tornado",
        "description": "Family reunited with their dog 3 days after tornado destroyed their home. Tearful moment goes viral.",
        "transcript": "Oh my god, Buddy! [crying] We thought we lost you! Thank you, thank you so much to everyone who helped search...",
        "score": 0.95,
        "emotion": "heartwarming",
        "predicted_views": "1M - 5M",
        "platforms": ["Facebook", "Instagram", "TikTok", "YouTube Shorts"],
        "hashtags": ["#Miracle", "#DogRescue", "#Heartwarming", "#GoodNews", "#Tornado"]
    },
    {
        "id": 3,
        "start": 1543.0,
        "end": 1568.5,
        "title": "🎤 Mayor's Mic Drop Response to Heckler",
        "description": "Mayor delivers sharp, witty response to heckler during press conference. Crowd erupts in applause.",
        "transcript": "Sir, I've been in public service for 30 years. I've been called worse by better. Now, as I was saying about the infrastructure bill...",
        "score": 0.92,
        "emotion": "humor/wit",
        "predicted_views": "200K - 800K",
        "platforms": ["Twitter/X", "TikTok", "Reddit"],
        "hashtags": ["#MicDrop", "#Mayor", "#Politics", "#Savage", "#PressConference"]
    },
    {
        "id": 4,
        "start": 2105.0,
        "end": 2125.0,
        "title": "⚡ Lightning Strikes Live During Weather Report",
        "description": "Meteorologist captures dramatic lightning strike on camera during severe weather coverage.",
        "transcript": "And if you look at the radar— [BOOM] WOW! Did you see that?! That lightning just struck maybe 500 yards from our tower!",
        "score": 0.94,
        "emotion": "excitement",
        "predicted_views": "300K - 1M",
        "platforms": ["Twitter/X", "TikTok", "YouTube"],
        "hashtags": ["#Lightning", "#Weather", "#Dramatic", "#LiveTV", "#Storm"]
    },
]

# Archive Agent - Demo Archive Content
DEMO_ARCHIVE = [
    {"id": 1, "title": "Presidential Debate 2024 - Full Coverage", "duration": "2:15:00", "date": "2024-09-10", "speaker": "Multiple", "tags": "politics, election, debate, biden, trump", "description": "Complete coverage of the presidential debate including pre and post analysis"},
    {"id": 2, "title": "Hurricane Milton - 72 Hour Coverage Compilation", "duration": "4:30:00", "date": "2024-10-09", "speaker": "Weather Team", "tags": "weather, hurricane, florida, emergency, milton", "description": "Complete storm coverage from formation to landfall"},
    {"id": 3, "title": "Super Bowl LVIII Halftime Show - Usher", "duration": "00:14:30", "date": "2024-02-11", "speaker": "Commentary Team", "tags": "sports, superbowl, halftime, usher, entertainment", "description": "Full halftime performance with commentary"},
    {"id": 4, "title": "CEO Interview: Tim Cook on Apple Vision Pro", "duration": "00:28:45", "date": "2024-01-15", "speaker": "Tim Cook, Maria Chen", "tags": "tech, apple, interview, visionpro, innovation", "description": "Exclusive interview about Apple's new spatial computing device"},
    {"id": 5, "title": "Nashville Tornado Coverage - March 2024", "duration": "3:45:00", "date": "2024-03-14", "speaker": "News Team", "tags": "weather, tornado, nashville, emergency, breaking", "description": "Live coverage of tornado outbreak across Middle Tennessee"},
    {"id": 6, "title": "Taylor Swift Eras Tour - Nashville Night 3", "duration": "00:45:00", "date": "2024-05-05", "speaker": "Entertainment Desk", "tags": "entertainment, taylorswift, concert, nashville, music", "description": "Highlights and fan reactions from record-breaking concert"},
    {"id": 7, "title": "Stock Market Flash Crash Analysis", "duration": "01:20:00", "date": "2024-08-05", "speaker": "Financial Team", "tags": "finance, markets, crash, economy, breaking", "description": "Expert analysis during market volatility event"},
    {"id": 8, "title": "Olympic Gold: Simone Biles Historic Vault", "duration": "00:08:30", "date": "2024-08-01", "speaker": "Sports Desk", "tags": "sports, olympics, gymnastics, simonebiles, gold", "description": "Historic vault performance and medal ceremony"},
]

# Compliance Agent - Real FCC Violation Scenarios
DEMO_COMPLIANCE_ISSUES = [
    {
        "type": "profanity",
        "severity": "critical",
        "timestamp": "00:23:45",
        "description": "Unbleeped expletive during live interview",
        "context": "Guest said 'What the f***' when surprised by question. Audio was not dumped in time.",
        "fcc_rule": "47 U.S.C. § 326 - Indecent Content",
        "fine_range": "$25,000 - $500,000 per violation",
        "recommendation": "Implement 7-second delay. Train operators on dump button. Issue on-air apology.",
        "precedent": "FCC fined CBS $550,000 for Janet Jackson incident (2004)"
    },
    {
        "type": "political_ad",
        "severity": "high",
        "timestamp": "01:15:30",
        "description": "Political advertisement missing sponsorship disclosure",
        "context": "30-second ad for Senate candidate did not include required 'Paid for by...' statement",
        "fcc_rule": "47 U.S.C. § 315 - Political Broadcasting",
        "fine_range": "$10,000 - $100,000",
        "recommendation": "Pull ad immediately. Contact campaign for compliant version. Log discrepancy.",
        "precedent": "Station liable even if ad provided by campaign without disclosure"
    },
    {
        "type": "sponsorship_disclosure",
        "severity": "medium",
        "timestamp": "02:08:15",
        "description": "Paid product integration without disclosure",
        "context": "Morning show hosts discussed new smartphone for 3 minutes. No disclosure that segment was sponsored.",
        "fcc_rule": "47 U.S.C. § 317 - Sponsorship Identification",
        "fine_range": "$10,000 - $50,000",
        "recommendation": "Add 'Sponsored Content' graphic. Hosts must verbally disclose paid partnerships.",
        "precedent": "FCC increased enforcement of undisclosed paid content in 2023"
    },
    {
        "type": "eas_violation",
        "severity": "critical",
        "timestamp": "03:45:00",
        "description": "Emergency Alert System test not broadcast",
        "context": "Required monthly EAS test was not aired due to sports programming override",
        "fcc_rule": "47 CFR Part 11 - Emergency Alert System",
        "fine_range": "$50,000 - $500,000",
        "recommendation": "Reschedule test within 24 hours. Document cause. Review automation system.",
        "precedent": "FCC fined station $25,000 for single missed EAS test in 2022"
    },
]

# Social Publishing - Real Post Templates
DEMO_SOCIAL_POSTS = {
    "breaking_news": [
        {"platform": "Twitter/X", "content": "🚨 BREAKING: Massive warehouse fire in downtown Nashville. Multiple fire crews responding. No injuries reported. LIVE coverage now on @WKRN\n\n📺 Watch: [link]\n\n#Nashville #Breaking #Fire", "char_count": 198, "best_time": "Immediately"},
        {"platform": "Instagram", "content": "🔴 BREAKING NEWS\n\nMassive warehouse fire erupts in downtown Nashville overnight. Our crew is LIVE on scene.\n\nSwipe for latest updates ➡️\n\nNo injuries reported. Fire crews have been battling the blaze since 2 AM.\n\n📺 Watch live coverage in our bio link\n\n#Nashville #BreakingNews #Fire #WKRN #LocalNews #Tennessee", "char_count": 342, "best_time": "Immediately"},
        {"platform": "TikTok", "content": "MASSIVE fire in Nashville right now 🔥 Our reporter almost got hit by debris LIVE on air 😱 #nashville #fire #breaking #news #reporter #dramatic #fyp", "char_count": 149, "best_time": "Immediately"},
    ],
    "feel_good": [
        {"platform": "Twitter/X", "content": "😭❤️ This will make your day.\n\nFamily reunited with their dog 3 days after tornado destroyed their home.\n\nWatch the emotional moment ⬇️\n\n#GoodNews #Nashville #Tornado #DogRescue", "char_count": 186, "best_time": "12:00 PM"},
        {"platform": "Instagram", "content": "We're not crying, you're crying 😭❤️\n\nThis family lost everything when a tornado destroyed their home. But after 3 days of searching, they found what mattered most - their dog Buddy.\n\nWatch the emotional reunion in our latest reel 🎥\n\n#GoodNews #Heartwarming #DogRescue #Miracle #Nashville #Community #Hope", "char_count": 328, "best_time": "7:00 PM"},
        {"platform": "TikTok", "content": "POV: You find your dog 3 days after a tornado destroyed your home 😭🐕❤️ #emotional #dogsoftiktok #tornado #reunion #crying #fyp #miracle", "char_count": 138, "best_time": "8:00 PM"},
    ]
}

# Localization - Real Broadcast Translations
DEMO_TRANSLATIONS = {
    "es": {
        "name": "Spanish",
        "flag": "🇪🇸",
        "sample_original": "Breaking overnight: A massive fire has destroyed a warehouse in downtown Nashville.",
        "sample_translated": "Noticia de última hora: Un incendio masivo ha destruido un almacén en el centro de Nashville.",
        "quality_score": 96,
        "notes": "Reviewed by native speaker. 'Breaking overnight' localized to Spanish news convention."
    },
    "fr": {
        "name": "French",
        "flag": "🇫🇷",
        "sample_original": "Breaking overnight: A massive fire has destroyed a warehouse in downtown Nashville.",
        "sample_translated": "Flash info: Un incendie majeur a détruit un entrepôt dans le centre-ville de Nashville.",
        "quality_score": 94,
        "notes": "'Breaking overnight' adapted to 'Flash info' per French broadcast standards."
    },
    "de": {
        "name": "German",
        "flag": "🇩🇪",
        "sample_original": "Breaking overnight: A massive fire has destroyed a warehouse in downtown Nashville.",
        "sample_translated": "Eilmeldung: Ein Großbrand hat ein Lagerhaus in der Innenstadt von Nashville zerstört.",
        "quality_score": 95,
        "notes": "German compound words used appropriately. Formal news register maintained."
    },
    "zh": {
        "name": "Chinese (Simplified)",
        "flag": "🇨🇳",
        "sample_original": "Breaking overnight: A massive fire has destroyed a warehouse in downtown Nashville.",
        "sample_translated": "突发新闻：纳什维尔市中心一座仓库在大火中被烧毁。",
        "quality_score": 93,
        "notes": "Simplified Chinese. City name transliterated phonetically."
    },
    "ar": {
        "name": "Arabic",
        "flag": "🇸🇦",
        "sample_original": "Breaking overnight: A massive fire has destroyed a warehouse in downtown Nashville.",
        "sample_translated": "عاجل: حريق ضخم يدمر مستودعاً في وسط مدينة ناشفيل",
        "quality_score": 92,
        "notes": "Modern Standard Arabic. Right-to-left formatting verified."
    },
    "ja": {
        "name": "Japanese",
        "flag": "🇯🇵",
        "sample_original": "Breaking overnight: A massive fire has destroyed a warehouse in downtown Nashville.",
        "sample_translated": "速報：ナッシュビル中心部で大規模火災、倉庫が全焼",
        "quality_score": 94,
        "notes": "Formal news Japanese (です/ます form). Kanji usage appropriate for news broadcast."
    },
}

# Rights Agent - Real Content Licenses
DEMO_LICENSES = [
    {
        "id": "LIC-001",
        "title": "NFL Sunday Ticket - Local Games",
        "licensor": "NFL Media",
        "type": "Exclusive Regional",
        "rights": ["Live broadcast", "Same-day replay", "Highlights up to 2 min"],
        "territories": ["Nashville DMA", "Middle Tennessee"],
        "start_date": "2024-09-01",
        "end_date": "2025-02-15",
        "cost": "$2,400,000/season",
        "status": "active",
        "days_remaining": 45,
        "restrictions": "No streaming without separate digital rights. No broadcast outside DMA."
    },
    {
        "id": "LIC-002",
        "title": "AP Video News Feed",
        "licensor": "Associated Press",
        "type": "Non-Exclusive",
        "rights": ["Broadcast", "Digital", "Archive 90 days"],
        "territories": ["United States"],
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "cost": "$180,000/year",
        "status": "expiring_soon",
        "days_remaining": 18,
        "restrictions": "Must credit 'AP' on all usage. Cannot sublicense."
    },
    {
        "id": "LIC-003",
        "title": "Getty Images Editorial Package",
        "licensor": "Getty Images",
        "type": "Subscription",
        "rights": ["Editorial use", "Broadcast", "Digital", "Social media"],
        "territories": ["Worldwide"],
        "start_date": "2024-06-01",
        "end_date": "2025-05-31",
        "cost": "$45,000/year",
        "status": "active",
        "days_remaining": 165,
        "restrictions": "Editorial use only. No commercial/advertising use."
    },
    {
        "id": "LIC-004",
        "title": "Music Licensing - BMI Blanket",
        "licensor": "BMI",
        "type": "Blanket License",
        "rights": ["Background music", "Broadcast performance"],
        "territories": ["United States"],
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "cost": "$35,000/year",
        "status": "expiring_soon",
        "days_remaining": 18,
        "restrictions": "Does not cover synchronization rights for produced content."
    },
]

DEMO_VIOLATIONS = [
    {
        "content": "NFL Highlights Package",
        "platform": "YouTube",
        "channel": "SportsClipsDaily",
        "url": "youtube.com/watch?v=xxxxx",
        "detected": "2024-12-10",
        "views": "245,000",
        "status": "DMCA Filed",
        "estimated_damages": "$15,000 - $50,000"
    },
    {
        "content": "Tornado Coverage Clip",
        "platform": "TikTok",
        "channel": "@weatherwatcher99",
        "url": "tiktok.com/@weatherwatcher99/video/xxxxx",
        "detected": "2024-12-08",
        "views": "1,200,000",
        "status": "Under Review",
        "estimated_damages": "$5,000 - $25,000"
    },
]

# Trending Agent - Real Trending Topics
DEMO_TRENDS = [
    {
        "topic": "#NashvilleFire",
        "category": "Local Breaking",
        "velocity": "🚀 Exploding",
        "velocity_score": 98,
        "volume": "45K posts/hour",
        "sentiment": "Concerned",
        "sentiment_score": -0.3,
        "top_posts": ["Massive fire downtown", "Hope everyone is safe", "Watching live coverage"],
        "our_coverage": True,
        "recommendation": "Continue live coverage. Post updates every 15 min."
    },
    {
        "topic": "Fed Interest Rate Decision",
        "category": "Finance",
        "velocity": "📈 Rising",
        "velocity_score": 85,
        "volume": "120K posts/hour",
        "sentiment": "Mixed",
        "sentiment_score": 0.1,
        "top_posts": ["Rate cut expected", "Markets reacting", "What this means for mortgages"],
        "our_coverage": False,
        "recommendation": "Prepare financial desk segment. Get local economist reaction."
    },
    {
        "topic": "Titans vs Colts Preview",
        "category": "Sports",
        "velocity": "📊 Steady",
        "velocity_score": 72,
        "volume": "28K posts/hour",
        "sentiment": "Excited",
        "sentiment_score": 0.6,
        "top_posts": ["Game day!", "Titan Up!", "Playoff implications"],
        "our_coverage": True,
        "recommendation": "Sports desk prepared. Pregame show at 11:30 AM."
    },
    {
        "topic": "Taylor Swift Grammy Nominations",
        "category": "Entertainment",
        "velocity": "🚀 Exploding",
        "velocity_score": 95,
        "volume": "890K posts/hour",
        "sentiment": "Very Positive",
        "sentiment_score": 0.85,
        "top_posts": ["She deserves all of them", "Swifties winning", "Album of the year"],
        "our_coverage": False,
        "recommendation": "Entertainment desk to prepare segment. Local Swiftie reaction?"
    },
]

DEMO_BREAKING = [
    {
        "headline": "BREAKING: Fed Announces Interest Rate Decision",
        "summary": "Federal Reserve expected to announce rate decision at 2:00 PM ET. Markets on edge.",
        "source": "Federal Reserve / AP",
        "time": "11:45 AM",
        "urgency": "high",
        "action": "Prepare live cut-in. Financial correspondent standing by."
    },
    {
        "headline": "DEVELOPING: Multi-Vehicle Accident on I-40",
        "summary": "Reports of 6+ vehicle accident on I-40 East near exit 213. Traffic backing up.",
        "source": "TN Highway Patrol",
        "time": "11:52 AM",
        "urgency": "medium",
        "action": "Send traffic reporter. Get helicopter if available."
    },
]


# ============== Helper Functions ==============

def format_srt_time(seconds):
    """Format seconds to SRT timestamp"""
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{ms:03d}"

def generate_srt(captions):
    """Generate SRT file content"""
    srt_content = ""
    for i, cap in enumerate(captions, 1):
        srt_content += f"{i}\n"
        srt_content += f"{format_srt_time(cap['start'])} --> {format_srt_time(cap['end'])}\n"
        srt_content += f"{cap['text']}\n\n"
    return srt_content


# ============== Sidebar ==============

with st.sidebar:
    st.markdown('<p class="main-header">🎬 MediaAgentIQ</p>', unsafe_allow_html=True)
    st.caption("AI Agent Platform for Media & Broadcast")

    st.divider()

    page = st.radio(
        "Select Agent",
        ["🏠 Dashboard", "📝 Caption Agent", "🎬 Clip Agent", "🔍 Archive Agent",
         "⚖️ Compliance Agent", "📱 Social Publishing", "🌍 Localization",
         "📜 Rights Agent", "📈 Trending Agent"],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("**System Status**")
    st.success("● All Agents Online")

    st.markdown("**Demo Mode**")
    st.info("Using realistic broadcast scenarios")

    st.divider()
    st.caption("v1.0.0 | Built for Broadcasters")


# ============== Main Pages ==============

if page == "🏠 Dashboard":
    st.title("🎬 MediaAgentIQ Dashboard")
    st.markdown("**AI-Powered Media Operations • Real Broadcast Workflows**")

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Jobs Today", "47", "+12 vs yesterday")
    col2.metric("Captions Generated", "23 hrs", "of content")
    col3.metric("Compliance Score", "94%", "+2%")
    col4.metric("Viral Clips Found", "8", "this week")

    st.divider()

    # Agent Grid
    st.subheader("Your AI Agents")

    agents_info = [
        ("🎬 Clip Agent", "Find viral moments from live broadcasts", "10x social content"),
        ("📝 Caption Agent", "Auto-caption with QA checks", "80% cost reduction"),
        ("⚖️ Compliance Agent", "FCC monitoring & violation alerts", "Avoid $500K+ fines"),
        ("🔍 Archive Agent", "Natural language archive search", "Instant access"),
        ("📱 Social Publishing", "Auto-generate social posts", "24/7 presence"),
        ("🌍 Localization", "Translate & dub content", "Global reach"),
        ("📜 Rights Agent", "License tracking & violations", "Legal protection"),
        ("📈 Trending Agent", "Real-time trend monitoring", "Never miss a story"),
    ]

    cols = st.columns(4)
    for i, (name, desc, benefit) in enumerate(agents_info):
        with cols[i % 4]:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1e293b, #0f172a); padding: 16px; border-radius: 12px; border: 1px solid #334155; margin-bottom: 12px; min-height: 140px;">
                <h4 style="margin: 0 0 8px 0;">{name}</h4>
                <p style="color: #94a3b8; font-size: 0.85rem; margin: 0 0 12px 0;">{desc}</p>
                <p style="color: #22c55e; font-size: 0.8rem; margin: 0;">✓ {benefit}</p>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Recent Activity
    st.subheader("Recent Activity")
    activity = [
        ("📝 Caption Agent", "Completed morning news broadcast (13 min)", "2 min ago"),
        ("⚖️ Compliance Agent", "Flagged potential FCC violation - Review needed", "15 min ago"),
        ("🎬 Clip Agent", "Found 3 viral moments in warehouse fire coverage", "32 min ago"),
        ("📈 Trending Agent", "Alert: #NashvilleFire trending locally", "45 min ago"),
        ("📜 Rights Agent", "Warning: AP license expires in 18 days", "1 hour ago"),
    ]

    for agent, action, time in activity:
        col1, col2, col3 = st.columns([1, 4, 1])
        col1.write(agent)
        col2.write(action)
        col3.caption(time)


elif page == "📝 Caption Agent":
    st.title("📝 Caption Agent")
    st.caption("Auto-generate broadcast-ready captions with QA checks")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Upload Media")
        uploaded = st.file_uploader("Upload video or audio", type=["mp4", "mov", "wav", "mp3"])

        demo_mode = st.checkbox("Use demo: Morning News Broadcast (1:22)", value=True)

        if st.button("Generate Captions", type="primary"):
            with st.spinner("Transcribing audio... Detecting speakers... Running QA..."):
                import time
                time.sleep(2)
                st.session_state.caption_done = True

    with col2:
        st.subheader("Settings")
        st.selectbox("Language", ["English (US)", "English (UK)", "Spanish"])
        st.checkbox("Speaker diarization", value=True)
        st.checkbox("Profanity filter check", value=True)
        st.slider("Confidence threshold", 0.8, 1.0, 0.90)

    if st.session_state.get("caption_done"):
        st.divider()

        # Stats
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Segments", len(DEMO_CAPTIONS))
        col2.metric("Duration", "1:22")
        col3.metric("Speakers", "2")
        col4.metric("Avg Confidence", "96.2%")

        tab1, tab2, tab3 = st.tabs(["📄 Captions", "✅ QA Report", "⬇️ Export"])

        with tab1:
            for cap in DEMO_CAPTIONS:
                conf_color = "#22c55e" if cap["confidence"] >= 0.95 else "#f59e0b" if cap["confidence"] >= 0.90 else "#ef4444"
                st.markdown(f"""
                <div class="caption-block">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                        <small style="color: #6366f1;">{format_srt_time(cap['start'])} → {format_srt_time(cap['end'])}</small>
                        <small style="color: {conf_color};">{cap['confidence']:.0%}</small>
                    </div>
                    <div style="color: #e2e8f0; margin-bottom: 4px;">{cap['text']}</div>
                    <small style="color: #64748b;">🎤 {cap['speaker']}</small>
                </div>
                """, unsafe_allow_html=True)

        with tab2:
            for issue in DEMO_QA_ISSUES:
                if issue["type"] == "warning":
                    st.warning(f"⚠️ **{issue['issue']}** (Segment {issue['segment']} @ {issue['timestamp']})\n\n{issue['details']}\n\n💡 *{issue['suggestion']}*")
                elif issue["type"] == "info":
                    st.info(f"ℹ️ **{issue['issue']}** (Segment {issue['segment']} @ {issue['timestamp']})\n\n{issue['details']}")
                elif issue["type"] == "success":
                    st.success(f"✅ **{issue['issue']}**\n\n{issue['details']}")

        with tab3:
            srt_content = generate_srt(DEMO_CAPTIONS)
            col1, col2 = st.columns(2)
            with col1:
                st.download_button("📥 Download SRT", srt_content, "morning_news_captions.srt", "text/plain", use_container_width=True)
            with col2:
                st.download_button("📥 Download VTT", srt_content.replace(",", "."), "morning_news_captions.vtt", "text/plain", use_container_width=True)


elif page == "🎬 Clip Agent":
    st.title("🎬 Clip Agent")
    st.caption("AI-powered viral moment detection from live broadcasts")

    uploaded = st.file_uploader("Upload broadcast recording", type=["mp4", "mov"])
    demo_mode = st.checkbox("Use demo: 4-hour morning broadcast", value=True)

    if st.button("Find Viral Moments", type="primary"):
        with st.spinner("Analyzing broadcast... Detecting emotional peaks... Scoring viral potential..."):
            import time
            time.sleep(2)
            st.session_state.clip_done = True

    if st.session_state.get("clip_done"):
        st.divider()
        st.subheader(f"🔥 {len(DEMO_VIRAL_MOMENTS)} Viral Moments Detected")

        for moment in DEMO_VIRAL_MOMENTS:
            with st.expander(f"{moment['title']} — **{moment['score']:.0%} viral score**", expanded=True):
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.markdown(f"**Description:** {moment['description']}")
                    st.markdown(f"**Timestamp:** {moment['start']:.0f}s - {moment['end']:.0f}s ({moment['end']-moment['start']:.0f}s clip)")
                    st.markdown(f"**Transcript excerpt:**")
                    st.code(moment['transcript'], language=None)
                    st.markdown(f"**Hashtags:** {' '.join([f'`{h}`' for h in moment['hashtags']])}")

                with col2:
                    st.metric("Viral Score", f"{moment['score']:.0%}")
                    st.metric("Predicted Views", moment['predicted_views'])
                    st.markdown(f"**Best platforms:**")
                    for p in moment['platforms']:
                        st.write(f"• {p}")

                    st.button(f"Export Clip", key=f"export_{moment['id']}", use_container_width=True)


elif page == "🔍 Archive Agent":
    st.title("🔍 Archive Agent")
    st.caption("Natural language search across your entire archive")

    query = st.text_input("Search your archive", placeholder="Try: 'hurricane coverage from October' or 'Tim Cook interview'")

    st.markdown("**Quick searches:**")
    col1, col2, col3, col4 = st.columns(4)
    if col1.button("Election coverage"):
        query = "election coverage 2024"
    if col2.button("Weather events"):
        query = "hurricane tornado weather"
    if col3.button("Sports highlights"):
        query = "titans superbowl sports"
    if col4.button("Celebrity interviews"):
        query = "interview taylor swift tim cook"

    if query:
        st.divider()

        # Filter results based on query
        results = [r for r in DEMO_ARCHIVE if any(word.lower() in (r['title'] + r['tags'] + r['description']).lower() for word in query.split())]

        if not results:
            results = DEMO_ARCHIVE[:3]  # Show some results anyway for demo

        st.success(f"Found **{len(results)} results** for '{query}'")

        for r in results:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"**{r['title']}**")
                    st.caption(f"{r['description']}")
                    st.caption(f"📅 {r['date']} • 🎤 {r['speaker']} • ⏱️ {r['duration']}")
                    st.caption(f"Tags: {r['tags']}")
                with col2:
                    st.button("Preview", key=f"preview_{r['id']}")
                with col3:
                    st.button("Export", key=f"export_{r['id']}")
                st.divider()


elif page == "⚖️ Compliance Agent":
    st.title("⚖️ Compliance Agent")
    st.caption("24/7 FCC compliance monitoring • Avoid $500K+ fines")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Scan Content")
        uploaded = st.file_uploader("Upload broadcast for scanning", type=["mp4", "mov", "wav"])
        demo_mode = st.checkbox("Use demo: Morning broadcast with violations", value=True)

        if st.button("Run Compliance Scan", type="primary"):
            with st.spinner("Scanning for profanity... Checking political ads... Verifying disclosures..."):
                import time
                time.sleep(2)
                st.session_state.compliance_done = True

    with col2:
        st.subheader("Scan Settings")
        st.checkbox("Profanity/Indecency", value=True)
        st.checkbox("Political Ad Disclosure", value=True)
        st.checkbox("Sponsorship ID", value=True)
        st.checkbox("EAS Compliance", value=True)
        st.checkbox("Caption Requirements", value=True)

    if st.session_state.get("compliance_done"):
        st.divider()

        # Risk Score
        risk_score = 58
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Risk Score", f"{risk_score}/100", "HIGH RISK", delta_color="inverse")
        col2.metric("Critical Issues", "2", "Immediate action")
        col3.metric("Warnings", "2", "Review needed")
        col4.metric("Potential Fines", "$85K - $1.1M", "If not addressed")

        st.divider()
        st.subheader("🚨 Issues Detected")

        for issue in DEMO_COMPLIANCE_ISSUES:
            severity_class = "issue-critical" if issue["severity"] == "critical" else "issue-warning"
            severity_icon = "🔴" if issue["severity"] == "critical" else "🟡" if issue["severity"] == "high" else "🟠"

            with st.expander(f"{severity_icon} {issue['type'].upper()} @ {issue['timestamp']} — {issue['severity'].upper()}", expanded=issue["severity"]=="critical"):
                st.markdown(f"**{issue['description']}**")
                st.markdown(f"*Context:* {issue['context']}")
                st.divider()
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**FCC Rule:** {issue['fcc_rule']}")
                    st.markdown(f"**Potential Fine:** {issue['fine_range']}")
                with col2:
                    st.markdown(f"**Precedent:** {issue['precedent']}")
                st.divider()
                st.info(f"💡 **Recommendation:** {issue['recommendation']}")


elif page == "📱 Social Publishing":
    st.title("📱 Social Publishing Agent")
    st.caption("Auto-generate platform-optimized posts from broadcast content")

    content_type = st.selectbox("Content type", ["Breaking News (Fire Coverage)", "Feel-Good Story (Dog Reunion)"])

    if st.button("Generate Social Posts", type="primary"):
        st.session_state.social_done = True
        st.session_state.social_type = "breaking_news" if "Breaking" in content_type else "feel_good"

    if st.session_state.get("social_done"):
        posts = DEMO_SOCIAL_POSTS[st.session_state.social_type]

        st.divider()

        for post in posts:
            with st.container():
                col1, col2 = st.columns([3, 1])

                with col1:
                    platform_icons = {"Twitter/X": "𝕏", "Instagram": "📸", "TikTok": "🎵"}
                    st.markdown(f"### {platform_icons.get(post['platform'], '📱')} {post['platform']}")
                    st.code(post['content'], language=None)
                    st.caption(f"{post['char_count']} characters • Best time: {post['best_time']}")

                with col2:
                    st.button("📋 Copy", key=f"copy_{post['platform']}", use_container_width=True)
                    st.button("📤 Post Now", key=f"post_{post['platform']}", use_container_width=True)
                    st.button("🕐 Schedule", key=f"schedule_{post['platform']}", use_container_width=True)

                st.divider()


elif page == "🌍 Localization":
    st.title("🌍 Localization Agent")
    st.caption("Auto-translate captions and generate dubs for global distribution")

    st.subheader("Source Content")
    st.info("**Demo:** Morning News Broadcast (1:22) - English")

    languages = st.multiselect(
        "Select target languages",
        list(DEMO_TRANSLATIONS.keys()),
        default=["es", "fr", "de"],
        format_func=lambda x: f"{DEMO_TRANSLATIONS[x]['flag']} {DEMO_TRANSLATIONS[x]['name']}"
    )

    col1, col2 = st.columns(2)
    with col1:
        st.checkbox("Generate subtitles (SRT/VTT)", value=True)
    with col2:
        st.checkbox("Generate AI dubs", value=False)

    if languages and st.button("Start Localization", type="primary"):
        with st.spinner("Translating... Quality checking... Generating files..."):
            import time
            time.sleep(2)
            st.session_state.local_done = True
            st.session_state.local_langs = languages

    if st.session_state.get("local_done"):
        st.divider()

        for lang in st.session_state.local_langs:
            trans = DEMO_TRANSLATIONS[lang]

            with st.expander(f"{trans['flag']} {trans['name']} — Quality: {trans['quality_score']}%", expanded=True):
                st.markdown("**Original:**")
                st.code(trans['sample_original'], language=None)
                st.markdown("**Translated:**")
                st.code(trans['sample_translated'], language=None)
                st.caption(f"📝 Notes: {trans['notes']}")

                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(f"📥 Download SRT ({lang.upper()})", "Demo SRT content", f"captions_{lang}.srt", use_container_width=True)
                with col2:
                    st.download_button(f"📥 Download VTT ({lang.upper()})", "Demo VTT content", f"captions_{lang}.vtt", use_container_width=True)


elif page == "📜 Rights Agent":
    st.title("📜 Rights Agent")
    st.caption("Track content licenses • Monitor unauthorized usage • Avoid legal disputes")

    if st.button("Check All Licenses & Rights", type="primary"):
        with st.spinner("Checking licenses... Scanning for violations..."):
            import time
            time.sleep(1)
            st.session_state.rights_done = True

    if st.session_state.get("rights_done"):
        st.divider()

        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Active Licenses", len(DEMO_LICENSES))
        col2.metric("Expiring Soon", "2", "⚠️ Within 30 days")
        col3.metric("Violations Found", len(DEMO_VIOLATIONS))
        col4.metric("Annual Spend", "$2.66M")

        st.divider()

        # Expiring Soon Alert
        st.subheader("⚠️ Expiring Soon")
        for lic in [l for l in DEMO_LICENSES if l["status"] == "expiring_soon"]:
            st.warning(f"**{lic['title']}** expires in **{lic['days_remaining']} days** ({lic['end_date']})\n\nLicensor: {lic['licensor']} • Cost: {lic['cost']}")

        st.divider()

        # Active Licenses
        st.subheader("📄 Active Licenses")
        for lic in DEMO_LICENSES:
            status_color = "🟢" if lic["status"] == "active" else "🟡"
            with st.expander(f"{status_color} {lic['title']} — {lic['days_remaining']} days remaining"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Licensor:** {lic['licensor']}")
                    st.markdown(f"**Type:** {lic['type']}")
                    st.markdown(f"**Cost:** {lic['cost']}")
                    st.markdown(f"**Period:** {lic['start_date']} to {lic['end_date']}")
                with col2:
                    st.markdown(f"**Rights:** {', '.join(lic['rights'])}")
                    st.markdown(f"**Territories:** {', '.join(lic['territories'])}")
                    st.markdown(f"**Restrictions:**")
                    st.caption(lic['restrictions'])

        st.divider()

        # Violations
        st.subheader("🚨 Unauthorized Usage Detected")
        for v in DEMO_VIOLATIONS:
            st.error(f"""
            **{v['content']}** found on **{v['platform']}**

            Channel: {v['channel']} • Views: {v['views']} • Detected: {v['detected']}

            Status: **{v['status']}** • Est. Damages: {v['estimated_damages']}
            """)


elif page == "📈 Trending Agent":
    st.title("📈 Trending Agent")
    st.caption("Real-time trend monitoring • Never miss a story")

    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.session_state.trending_refresh = True

    # Breaking News Section
    st.markdown("### 🔴 Breaking News Alerts")
    for news in DEMO_BREAKING:
        urgency_color = "#dc2626" if news["urgency"] == "high" else "#f59e0b"
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, {urgency_color}, #991b1b); padding: 12px 16px; border-radius: 8px; margin: 8px 0;">
            <strong>{news['headline']}</strong><br/>
            <span style="opacity: 0.9;">{news['summary']}</span><br/>
            <small>Source: {news['source']} • {news['time']}</small><br/>
            <small style="color: #fef08a;">➡️ {news['action']}</small>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Trending Topics
    st.markdown("### 📊 Trending Topics")

    for trend in DEMO_TRENDS:
        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 2])

        with col1:
            coverage_badge = "✅ Covering" if trend["our_coverage"] else "📝 Not covering"
            st.markdown(f"**{trend['topic']}**")
            st.caption(f"{trend['category']} • {coverage_badge}")

        with col2:
            st.markdown(f"**{trend['velocity']}**")
            st.caption(trend['volume'])

        with col3:
            sentiment_emoji = "😊" if "Positive" in trend["sentiment"] else "😐" if "Mixed" in trend["sentiment"] else "😟"
            st.markdown(f"**{sentiment_emoji}**")
            st.caption(trend['sentiment'])

        with col4:
            st.metric("Score", trend['velocity_score'], label_visibility="collapsed")

        with col5:
            st.caption(f"💡 {trend['recommendation']}")

        st.divider()


# Footer
st.divider()
st.caption("MediaAgentIQ v1.0.0 • AI-Powered Media Operations Platform • Built for Broadcasters")
