"""
MediaAgentIQ - Enhanced Streamlit App
AI Agent Platform for Media & Broadcast Operations
Real-time demos showcasing full agent capabilities
"""
import streamlit as st
import random
import time
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="MediaAgentIQ",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI
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
    .realtime-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        background: #22c55e;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    .capability-card {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        padding: 16px;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 12px;
    }
    .integration-card {
        background: linear-gradient(135deg, #0f172a, #1e1b4b);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #4f46e5;
        margin-bottom: 16px;
    }
    .metric-highlight {
        background: linear-gradient(135deg, #059669, #047857);
        padding: 8px 16px;
        border-radius: 8px;
        display: inline-block;
    }
    .processing-step {
        background: #1e293b;
        padding: 8px 12px;
        border-radius: 6px;
        margin: 4px 0;
        border-left: 3px solid #6366f1;
    }
    .processing-step.complete {
        border-left-color: #22c55e;
    }
    .processing-step.active {
        border-left-color: #f59e0b;
        animation: pulse 1s infinite;
    }
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
        "title": "Reporter's Close Call with Debris",
        "description": "Live reporter narrowly dodges falling debris during warehouse fire coverage. Dramatic moment captured on air.",
        "transcript": "Whoa! As you can see— [debris falls] —we're moving back now. That was close. The structural integrity is clearly compromised...",
        "score": 0.97,
        "emotion": "shock/drama",
        "predicted_views": "500K - 2M",
        "platforms": ["TikTok", "Twitter/X", "Instagram Reels"],
        "hashtags": ["#Breaking", "#CloseCall", "#LiveTV", "#Reporter", "#Dramatic"],
        "audio_peaks": [147.3, 149.8, 155.2],
        "face_emotions": {"surprise": 0.89, "fear": 0.72, "relief": 0.65}
    },
    {
        "id": 2,
        "start": 892.5,
        "end": 918.0,
        "title": "Emotional Reunion: Lost Dog Found After Tornado",
        "description": "Family reunited with their dog 3 days after tornado destroyed their home. Tearful moment goes viral.",
        "transcript": "Oh my god, Buddy! [crying] We thought we lost you! Thank you, thank you so much to everyone who helped search...",
        "score": 0.95,
        "emotion": "heartwarming",
        "predicted_views": "1M - 5M",
        "platforms": ["Facebook", "Instagram", "TikTok", "YouTube Shorts"],
        "hashtags": ["#Miracle", "#DogRescue", "#Heartwarming", "#GoodNews", "#Tornado"],
        "audio_peaks": [895.1, 901.3, 912.7],
        "face_emotions": {"joy": 0.94, "surprise": 0.78, "sadness": 0.45}
    },
    {
        "id": 3,
        "start": 1543.0,
        "end": 1568.5,
        "title": "Mayor's Mic Drop Response to Heckler",
        "description": "Mayor delivers sharp, witty response to heckler during press conference. Crowd erupts in applause.",
        "transcript": "Sir, I've been in public service for 30 years. I've been called worse by better. Now, as I was saying about the infrastructure bill...",
        "score": 0.92,
        "emotion": "humor/wit",
        "predicted_views": "200K - 800K",
        "platforms": ["Twitter/X", "TikTok", "Reddit"],
        "hashtags": ["#MicDrop", "#Mayor", "#Politics", "#Savage", "#PressConference"],
        "audio_peaks": [1545.8, 1552.1, 1560.3],
        "face_emotions": {"neutral": 0.65, "contempt": 0.42, "amusement": 0.38}
    },
    {
        "id": 4,
        "start": 2105.0,
        "end": 2125.0,
        "title": "Lightning Strikes Live During Weather Report",
        "description": "Meteorologist captures dramatic lightning strike on camera during severe weather coverage.",
        "transcript": "And if you look at the radar— [BOOM] WOW! Did you see that?! That lightning just struck maybe 500 yards from our tower!",
        "score": 0.94,
        "emotion": "excitement",
        "predicted_views": "300K - 1M",
        "platforms": ["Twitter/X", "TikTok", "YouTube"],
        "hashtags": ["#Lightning", "#Weather", "#Dramatic", "#LiveTV", "#Storm"],
        "audio_peaks": [2108.5, 2110.2, 2115.8],
        "face_emotions": {"surprise": 0.92, "excitement": 0.85, "fear": 0.31}
    },
]

# Archive Agent - Demo Archive Content
DEMO_ARCHIVE = [
    {"id": 1, "title": "Presidential Debate 2024 - Full Coverage", "duration": "2:15:00", "date": "2024-09-10", "speaker": "Multiple", "tags": "politics, election, debate", "description": "Complete coverage of the presidential debate including pre and post analysis", "format": "HD 1080p", "size": "4.2 GB"},
    {"id": 2, "title": "Hurricane Milton - 72 Hour Coverage Compilation", "duration": "4:30:00", "date": "2024-10-09", "speaker": "Weather Team", "tags": "weather, hurricane, florida, emergency", "description": "Complete storm coverage from formation to landfall", "format": "HD 1080p", "size": "8.1 GB"},
    {"id": 3, "title": "Super Bowl LVIII Halftime Show - Usher", "duration": "00:14:30", "date": "2024-02-11", "speaker": "Commentary Team", "tags": "sports, superbowl, halftime, entertainment", "description": "Full halftime performance with commentary", "format": "4K UHD", "size": "2.8 GB"},
    {"id": 4, "title": "CEO Interview: Tech Leader on Innovation", "duration": "00:28:45", "date": "2024-01-15", "speaker": "Executive, Maria Chen", "tags": "tech, interview, innovation", "description": "Exclusive interview about new technology developments", "format": "HD 1080p", "size": "1.2 GB"},
    {"id": 5, "title": "Nashville Tornado Coverage - March 2024", "duration": "3:45:00", "date": "2024-03-14", "speaker": "News Team", "tags": "weather, tornado, nashville, emergency, breaking", "description": "Live coverage of tornado outbreak across Middle Tennessee", "format": "HD 1080p", "size": "6.7 GB"},
    {"id": 6, "title": "Concert Special - Nashville Night 3", "duration": "00:45:00", "date": "2024-05-05", "speaker": "Entertainment Desk", "tags": "entertainment, concert, nashville, music", "description": "Highlights and fan reactions from record-breaking concert", "format": "4K UHD", "size": "3.5 GB"},
    {"id": 7, "title": "Stock Market Flash Crash Analysis", "duration": "01:20:00", "date": "2024-08-05", "speaker": "Financial Team", "tags": "finance, markets, economy, breaking", "description": "Expert analysis during market volatility event", "format": "HD 1080p", "size": "2.1 GB"},
    {"id": 8, "title": "Olympic Gold: Historic Vault Performance", "duration": "00:08:30", "date": "2024-08-01", "speaker": "Sports Desk", "tags": "sports, olympics, gymnastics, gold", "description": "Historic vault performance and medal ceremony", "format": "4K UHD", "size": "1.8 GB"},
]

# Compliance Agent - Real FCC Violation Scenarios
DEMO_COMPLIANCE_ISSUES = [
    {
        "type": "profanity",
        "severity": "critical",
        "timestamp": "00:23:45",
        "description": "Unbleeped expletive during live interview",
        "context": "Guest said explicit word when surprised by question. Audio was not dumped in time.",
        "fcc_rule": "47 U.S.C. 326 - Indecent Content",
        "fine_range": "$25,000 - $500,000 per violation",
        "recommendation": "Implement 7-second delay. Train operators on dump button. Issue on-air apology.",
        "precedent": "FCC fined major network $550,000 for similar incident (2004)",
        "auto_detected": True,
        "confidence": 0.98
    },
    {
        "type": "political_ad",
        "severity": "high",
        "timestamp": "01:15:30",
        "description": "Political advertisement missing sponsorship disclosure",
        "context": "30-second ad for Senate candidate did not include required 'Paid for by...' statement",
        "fcc_rule": "47 U.S.C. 315 - Political Broadcasting",
        "fine_range": "$10,000 - $100,000",
        "recommendation": "Pull ad immediately. Contact campaign for compliant version. Log discrepancy.",
        "precedent": "Station liable even if ad provided by campaign without disclosure",
        "auto_detected": True,
        "confidence": 0.95
    },
    {
        "type": "sponsorship_disclosure",
        "severity": "medium",
        "timestamp": "02:08:15",
        "description": "Paid product integration without disclosure",
        "context": "Morning show hosts discussed new smartphone for 3 minutes. No disclosure that segment was sponsored.",
        "fcc_rule": "47 U.S.C. 317 - Sponsorship Identification",
        "fine_range": "$10,000 - $50,000",
        "recommendation": "Add 'Sponsored Content' graphic. Hosts must verbally disclose paid partnerships.",
        "precedent": "FCC increased enforcement of undisclosed paid content in 2023",
        "auto_detected": True,
        "confidence": 0.87
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
        "precedent": "FCC fined station $25,000 for single missed EAS test in 2022",
        "auto_detected": True,
        "confidence": 0.99
    },
]

# Social Publishing - Real Post Templates
DEMO_SOCIAL_POSTS = {
    "breaking_news": [
        {"platform": "Twitter/X", "content": "BREAKING: Massive warehouse fire in downtown Nashville. Multiple fire crews responding. No injuries reported. LIVE coverage now.\n\nWatch: [link]\n\n#Nashville #Breaking #Fire", "char_count": 185, "best_time": "Immediately", "predicted_engagement": "12.5K"},
        {"platform": "Instagram", "content": "BREAKING NEWS\n\nMassive warehouse fire erupts in downtown Nashville overnight. Our crew is LIVE on scene.\n\nSwipe for latest updates\n\nNo injuries reported. Fire crews have been battling the blaze since 2 AM.\n\nWatch live coverage in our bio link\n\n#Nashville #BreakingNews #Fire #LocalNews #Tennessee", "char_count": 342, "best_time": "Immediately", "predicted_engagement": "8.2K"},
        {"platform": "TikTok", "content": "MASSIVE fire in Nashville right now. Our reporter almost got hit by debris LIVE on air #nashville #fire #breaking #news #reporter #dramatic #fyp", "char_count": 145, "best_time": "Immediately", "predicted_engagement": "45K"},
        {"platform": "Facebook", "content": "BREAKING: A massive warehouse fire has broken out in downtown Nashville. Our crews are on scene bringing you live coverage.\n\nWhat we know so far:\n- Fire started around 2 AM\n- Multiple fire crews responding\n- No injuries reported\n- Building was unoccupied\n\nStay with us for updates throughout the morning.", "char_count": 358, "best_time": "Immediately", "predicted_engagement": "5.8K"},
        {"platform": "YouTube Shorts", "content": "MASSIVE warehouse fire in Nashville - Reporter's close call with falling debris #shorts #breaking #news", "char_count": 102, "best_time": "Immediately", "predicted_engagement": "125K"},
    ],
    "feel_good": [
        {"platform": "Twitter/X", "content": "This will make your day.\n\nFamily reunited with their dog 3 days after tornado destroyed their home.\n\nWatch the emotional moment\n\n#GoodNews #Nashville #Tornado #DogRescue", "char_count": 186, "best_time": "12:00 PM", "predicted_engagement": "25K"},
        {"platform": "Instagram", "content": "We're not crying, you're crying\n\nThis family lost everything when a tornado destroyed their home. But after 3 days of searching, they found what mattered most - their dog Buddy.\n\nWatch the emotional reunion in our latest reel\n\n#GoodNews #Heartwarming #DogRescue #Miracle #Nashville #Community #Hope", "char_count": 328, "best_time": "7:00 PM", "predicted_engagement": "18K"},
        {"platform": "TikTok", "content": "POV: You find your dog 3 days after a tornado destroyed your home #emotional #dogsoftiktok #tornado #reunion #crying #fyp #miracle", "char_count": 130, "best_time": "8:00 PM", "predicted_engagement": "850K"},
        {"platform": "Facebook", "content": "Sometimes, amid tragedy, we find moments of pure joy.\n\nThis Nashville family lost their home in last week's tornado. For three days, they searched for their beloved dog Buddy, fearing the worst.\n\nYesterday, thanks to the incredible community effort, Buddy was found safe.\n\nWatch the emotional reunion that's touching hearts across the nation.", "char_count": 398, "best_time": "7:00 PM", "predicted_engagement": "12K"},
        {"platform": "YouTube Shorts", "content": "Family finds dog 3 days after tornado - emotional reunion #shorts #goodnews #dog #tornado", "char_count": 89, "best_time": "6:00 PM", "predicted_engagement": "200K"},
    ]
}

# Localization - Real Broadcast Translations
DEMO_TRANSLATIONS = {
    "es": {
        "name": "Spanish",
        "flag": "🇪🇸",
        "sample_original": "Breaking overnight: A massive fire has destroyed a warehouse in downtown Nashville.",
        "sample_translated": "Noticia de ultima hora: Un incendio masivo ha destruido un almacen en el centro de Nashville.",
        "quality_score": 96,
        "notes": "Reviewed by native speaker. 'Breaking overnight' localized to Spanish news convention.",
        "voice_available": True,
        "dialect_options": ["Spain", "Mexico", "Argentina"]
    },
    "fr": {
        "name": "French",
        "flag": "🇫🇷",
        "sample_original": "Breaking overnight: A massive fire has destroyed a warehouse in downtown Nashville.",
        "sample_translated": "Flash info: Un incendie majeur a detruit un entrepot dans le centre-ville de Nashville.",
        "quality_score": 94,
        "notes": "'Breaking overnight' adapted to 'Flash info' per French broadcast standards.",
        "voice_available": True,
        "dialect_options": ["France", "Canada", "Belgium"]
    },
    "de": {
        "name": "German",
        "flag": "🇩🇪",
        "sample_original": "Breaking overnight: A massive fire has destroyed a warehouse in downtown Nashville.",
        "sample_translated": "Eilmeldung: Ein Grossbrand hat ein Lagerhaus in der Innenstadt von Nashville zerstort.",
        "quality_score": 95,
        "notes": "German compound words used appropriately. Formal news register maintained.",
        "voice_available": True,
        "dialect_options": ["Germany", "Austria", "Switzerland"]
    },
    "zh": {
        "name": "Chinese (Simplified)",
        "flag": "🇨🇳",
        "sample_original": "Breaking overnight: A massive fire has destroyed a warehouse in downtown Nashville.",
        "sample_translated": "突发新闻：纳什维尔市中心一座仓库在大火中被烧毁。",
        "quality_score": 93,
        "notes": "Simplified Chinese. City name transliterated phonetically.",
        "voice_available": True,
        "dialect_options": ["Mandarin", "Cantonese"]
    },
    "ar": {
        "name": "Arabic",
        "flag": "🇸🇦",
        "sample_original": "Breaking overnight: A massive fire has destroyed a warehouse in downtown Nashville.",
        "sample_translated": "عاجل: حريق ضخم يدمر مستودعاً في وسط مدينة ناشفيل",
        "quality_score": 92,
        "notes": "Modern Standard Arabic. Right-to-left formatting verified.",
        "voice_available": True,
        "dialect_options": ["MSA", "Egyptian", "Gulf"]
    },
    "ja": {
        "name": "Japanese",
        "flag": "🇯🇵",
        "sample_original": "Breaking overnight: A massive fire has destroyed a warehouse in downtown Nashville.",
        "sample_translated": "速報：ナッシュビル中心部で大規模火災、倉庫が全焼",
        "quality_score": 94,
        "notes": "Formal news Japanese. Kanji usage appropriate for news broadcast.",
        "voice_available": True,
        "dialect_options": ["Standard Japanese"]
    },
    "hi": {
        "name": "Hindi",
        "flag": "🇮🇳",
        "sample_original": "Breaking overnight: A massive fire has destroyed a warehouse in downtown Nashville.",
        "sample_translated": "ब्रेकिंग न्यूज़: नैशविले शहर के केंद्र में एक गोदाम भीषण आग में जलकर खाक",
        "quality_score": 91,
        "notes": "Hindi news broadcast style. English terms retained where standard in Indian media.",
        "voice_available": True,
        "dialect_options": ["Standard Hindi"]
    },
    "pt": {
        "name": "Portuguese",
        "flag": "🇧🇷",
        "sample_original": "Breaking overnight: A massive fire has destroyed a warehouse in downtown Nashville.",
        "sample_translated": "Urgente: Um grande incendio destruiu um armazem no centro de Nashville.",
        "quality_score": 95,
        "notes": "Brazilian Portuguese variant. Formal news register.",
        "voice_available": True,
        "dialect_options": ["Brazil", "Portugal"]
    },
}

# Rights Agent - Real Content Licenses
DEMO_LICENSES = [
    {
        "id": "LIC-001",
        "title": "Sports League - Local Games Package",
        "licensor": "Major Sports League Media",
        "type": "Exclusive Regional",
        "rights": ["Live broadcast", "Same-day replay", "Highlights up to 2 min"],
        "territories": ["Local DMA", "Regional Coverage Area"],
        "start_date": "2024-09-01",
        "end_date": "2025-02-15",
        "cost": "$2,400,000/season",
        "status": "active",
        "days_remaining": 45,
        "restrictions": "No streaming without separate digital rights. No broadcast outside DMA.",
        "usage_this_month": 156,
        "compliance_score": 98
    },
    {
        "id": "LIC-002",
        "title": "Wire Service Video News Feed",
        "licensor": "International News Agency",
        "type": "Non-Exclusive",
        "rights": ["Broadcast", "Digital", "Archive 90 days"],
        "territories": ["United States"],
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "cost": "$180,000/year",
        "status": "expiring_soon",
        "days_remaining": 18,
        "restrictions": "Must credit source on all usage. Cannot sublicense.",
        "usage_this_month": 342,
        "compliance_score": 100
    },
    {
        "id": "LIC-003",
        "title": "Stock Images Editorial Package",
        "licensor": "Stock Media Provider",
        "type": "Subscription",
        "rights": ["Editorial use", "Broadcast", "Digital", "Social media"],
        "territories": ["Worldwide"],
        "start_date": "2024-06-01",
        "end_date": "2025-05-31",
        "cost": "$45,000/year",
        "status": "active",
        "days_remaining": 165,
        "restrictions": "Editorial use only. No commercial/advertising use.",
        "usage_this_month": 89,
        "compliance_score": 95
    },
    {
        "id": "LIC-004",
        "title": "Music Licensing - Blanket Performance",
        "licensor": "Performance Rights Organization",
        "type": "Blanket License",
        "rights": ["Background music", "Broadcast performance"],
        "territories": ["United States"],
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "cost": "$35,000/year",
        "status": "expiring_soon",
        "days_remaining": 18,
        "restrictions": "Does not cover synchronization rights for produced content.",
        "usage_this_month": 1240,
        "compliance_score": 100
    },
]

DEMO_VIOLATIONS = [
    {
        "content": "Sports Highlights Package",
        "platform": "YouTube",
        "channel": "SportsClipsDaily",
        "url": "youtube.com/watch?v=xxxxx",
        "detected": "2024-12-10",
        "views": "245,000",
        "status": "DMCA Filed",
        "estimated_damages": "$15,000 - $50,000",
        "match_confidence": 0.97,
        "content_id_match": True
    },
    {
        "content": "Tornado Coverage Clip",
        "platform": "TikTok",
        "channel": "@weatherwatcher99",
        "url": "tiktok.com/@weatherwatcher99/video/xxxxx",
        "detected": "2024-12-08",
        "views": "1,200,000",
        "status": "Under Review",
        "estimated_damages": "$5,000 - $25,000",
        "match_confidence": 0.89,
        "content_id_match": False
    },
    {
        "content": "Interview Segment",
        "platform": "Facebook",
        "channel": "News Aggregator Page",
        "url": "facebook.com/newsagg/videos/xxxxx",
        "detected": "2024-12-12",
        "views": "89,000",
        "status": "Takedown Requested",
        "estimated_damages": "$2,000 - $8,000",
        "match_confidence": 0.94,
        "content_id_match": True
    },
]

# Trending Agent - Real Trending Topics
DEMO_TRENDS = [
    {
        "topic": "#NashvilleFire",
        "category": "Local Breaking",
        "velocity": "Exploding",
        "velocity_score": 98,
        "volume": "45K posts/hour",
        "sentiment": "Concerned",
        "sentiment_score": -0.3,
        "top_posts": ["Massive fire downtown", "Hope everyone is safe", "Watching live coverage"],
        "our_coverage": True,
        "recommendation": "Continue live coverage. Post updates every 15 min.",
        "related_topics": ["#DowntownNashville", "#BreakingNews", "#FireDepartment"],
        "demographics": {"18-24": 15, "25-34": 35, "35-44": 28, "45-54": 14, "55+": 8}
    },
    {
        "topic": "Fed Interest Rate Decision",
        "category": "Finance",
        "velocity": "Rising",
        "velocity_score": 85,
        "volume": "120K posts/hour",
        "sentiment": "Mixed",
        "sentiment_score": 0.1,
        "top_posts": ["Rate cut expected", "Markets reacting", "What this means for mortgages"],
        "our_coverage": False,
        "recommendation": "Prepare financial desk segment. Get local economist reaction.",
        "related_topics": ["#FederalReserve", "#InterestRates", "#Economy", "#StockMarket"],
        "demographics": {"18-24": 8, "25-34": 28, "35-44": 32, "45-54": 22, "55+": 10}
    },
    {
        "topic": "Local Sports Preview",
        "category": "Sports",
        "velocity": "Steady",
        "velocity_score": 72,
        "volume": "28K posts/hour",
        "sentiment": "Excited",
        "sentiment_score": 0.6,
        "top_posts": ["Game day!", "Let's go!", "Playoff implications"],
        "our_coverage": True,
        "recommendation": "Sports desk prepared. Pregame show at 11:30 AM.",
        "related_topics": ["#GameDay", "#LocalSports", "#Playoffs"],
        "demographics": {"18-24": 22, "25-34": 31, "35-44": 25, "45-54": 15, "55+": 7}
    },
    {
        "topic": "Grammy Nominations",
        "category": "Entertainment",
        "velocity": "Exploding",
        "velocity_score": 95,
        "volume": "890K posts/hour",
        "sentiment": "Very Positive",
        "sentiment_score": 0.85,
        "top_posts": ["Deserves all of them", "Fans winning", "Album of the year"],
        "our_coverage": False,
        "recommendation": "Entertainment desk to prepare segment. Local fan reaction?",
        "related_topics": ["#Grammys", "#MusicAwards", "#Entertainment"],
        "demographics": {"18-24": 42, "25-34": 35, "35-44": 15, "45-54": 6, "55+": 2}
    },
]

DEMO_BREAKING = [
    {
        "headline": "BREAKING: Fed Announces Interest Rate Decision",
        "summary": "Federal Reserve expected to announce rate decision at 2:00 PM ET. Markets on edge.",
        "source": "Federal Reserve / Wire Service",
        "time": "11:45 AM",
        "urgency": "high",
        "action": "Prepare live cut-in. Financial correspondent standing by.",
        "confidence": 0.95
    },
    {
        "headline": "DEVELOPING: Multi-Vehicle Accident on Interstate",
        "summary": "Reports of 6+ vehicle accident on major interstate near exit 213. Traffic backing up.",
        "source": "Highway Patrol",
        "time": "11:52 AM",
        "urgency": "medium",
        "action": "Send traffic reporter. Get helicopter if available.",
        "confidence": 0.88
    },
]

# Integration Showcase Data
INTEGRATION_CAPABILITIES = {
    "mam_systems": {
        "name": "Media Asset Management Integration",
        "description": "Seamless connection to industry-standard MAM systems for asset ingest, metadata enrichment, and automated workflows.",
        "capabilities": [
            "Bi-directional metadata sync",
            "Automated proxy generation",
            "AI-powered tagging on ingest",
            "Workflow trigger integration",
            "Multi-resolution export"
        ],
        "protocols": ["REST API", "SOAP", "MOS Protocol", "BXF"],
        "status": "Production Ready"
    },
    "broadcast_automation": {
        "name": "Broadcast Automation Systems",
        "description": "Direct integration with playout automation for real-time content insertion and scheduling.",
        "capabilities": [
            "Real-time playlist updates",
            "Secondary event triggering",
            "Graphics automation",
            "Emergency override support",
            "Rundown synchronization"
        ],
        "protocols": ["MOS Protocol", "VDCP", "RS-422", "IP Control"],
        "status": "Production Ready"
    },
    "nmos_network": {
        "name": "IP Broadcast Infrastructure (NMOS)",
        "description": "Full NMOS IS-04/IS-05 compliance for modern IP-based broadcast facilities.",
        "capabilities": [
            "Device discovery (IS-04)",
            "Connection management (IS-05)",
            "Network resource allocation",
            "Multi-facility routing",
            "Redundancy failover"
        ],
        "protocols": ["NMOS IS-04", "NMOS IS-05", "NMOS IS-07", "ST 2110"],
        "status": "Production Ready"
    },
    "cloud_services": {
        "name": "Cloud Platform Integration",
        "description": "Native integration with major cloud platforms for scalable processing and storage.",
        "capabilities": [
            "Auto-scaling transcription",
            "Distributed AI processing",
            "Cloud storage tiering",
            "CDN integration",
            "Serverless workflows"
        ],
        "protocols": ["AWS SDK", "Azure SDK", "GCP SDK", "S3 Compatible"],
        "status": "Production Ready"
    },
    "social_platforms": {
        "name": "Social Media Platform APIs",
        "description": "Direct publishing and analytics integration with all major social platforms.",
        "capabilities": [
            "One-click multi-platform publish",
            "Scheduled posting",
            "Real-time analytics",
            "Comment monitoring",
            "Trend tracking"
        ],
        "protocols": ["Platform APIs", "OAuth 2.0", "Webhooks"],
        "status": "Production Ready"
    },
    "transcription_services": {
        "name": "AI Transcription Services",
        "description": "Integration with leading speech-to-text engines for accurate, fast transcription.",
        "capabilities": [
            "Real-time transcription",
            "Speaker diarization",
            "Custom vocabulary",
            "Multi-language support",
            "Punctuation & formatting"
        ],
        "protocols": ["WebSocket", "REST API", "gRPC"],
        "status": "Production Ready"
    }
}


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

def simulate_realtime_processing(steps, container):
    """Simulate real-time processing with visual feedback"""
    progress_bar = container.progress(0)
    status_text = container.empty()

    for i, step in enumerate(steps):
        status_text.markdown(f"**{step['icon']} {step['text']}**")
        time.sleep(step.get('duration', 0.5))
        progress_bar.progress((i + 1) / len(steps))

    status_text.markdown("**✅ Processing complete!**")
    time.sleep(0.3)
    return True


# ============== Sidebar ==============

with st.sidebar:
    st.markdown('<p class="main-header">MediaAgentIQ</p>', unsafe_allow_html=True)
    st.caption("AI Agent Platform for Media & Broadcast")

    st.divider()

    page = st.radio(
        "Select Agent",
        ["Dashboard", "🚀 All-in-One Workflow", "Caption Agent", "Clip Agent", "Archive Agent",
         "Compliance Agent", "Social Publishing", "Localization",
         "Rights Agent", "Trending Agent", "Integration Showcase"],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("**System Status**")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<span class="realtime-indicator"></span> Live', unsafe_allow_html=True)
    with col2:
        st.caption(f"{datetime.now().strftime('%H:%M:%S')}")

    st.success("All 8 Agents Online")

    # Mode selector
    st.markdown("**Processing Mode**")
    mode = st.radio("Mode", ["Demo Mode", "Production Mode"], label_visibility="collapsed", horizontal=True)
    if mode == "Production Mode":
        st.warning("Requires API keys in .env")

    st.divider()
    st.caption("v2.0.0 | Enterprise Edition")


# ============== Main Pages ==============

if page == "Dashboard":
    st.title("MediaAgentIQ Dashboard")
    st.markdown("**AI-Powered Media Operations Platform** | Real-time Broadcast Intelligence")

    # Autonomous Agent Status Section
    st.markdown("---")
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("🤖 Autonomous Agent Orchestrator")
        st.markdown("Agents can run **autonomously in the background** - monitoring, processing, and alerting without manual intervention.")

    with col2:
        # Initialize session state for orchestrator
        if "orchestrator_running" not in st.session_state:
            st.session_state.orchestrator_running = False

        if st.session_state.orchestrator_running:
            if st.button("⏹️ Stop Autonomous Mode", type="secondary", use_container_width=True):
                st.session_state.orchestrator_running = False
                st.rerun()
        else:
            if st.button("▶️ Start Autonomous Mode", type="primary", use_container_width=True):
                st.session_state.orchestrator_running = True
                st.rerun()

    if st.session_state.orchestrator_running:
        st.success("🟢 **Autonomous Mode ACTIVE** - All agents running in background")

        # Show running status
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Queue Size", "3 tasks")
        col2.metric("Processing", "1 active")
        col3.metric("Completed", "47 today")
        col4.metric("Uptime", "2h 34m")

        # Scheduled Jobs
        with st.expander("📅 **Scheduled Background Jobs** (Click to expand)", expanded=True):
            scheduled_jobs = [
                {"agent": "📈 Trending Agent", "interval": "Every 5 min", "last_run": "2 min ago", "status": "✅ Active"},
                {"agent": "⚖️ Compliance Agent", "interval": "Every 10 min", "last_run": "7 min ago", "status": "✅ Active"},
                {"agent": "📜 Rights Agent", "interval": "Every 1 hour", "last_run": "34 min ago", "status": "✅ Active"},
                {"agent": "🔍 Archive Agent", "interval": "Every 6 hours", "last_run": "2h ago", "status": "✅ Active"},
            ]

            for job in scheduled_jobs:
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                col1.write(job["agent"])
                col2.write(job["interval"])
                col3.write(job["last_run"])
                col4.write(job["status"])

        # Event System
        with st.expander("⚡ **Event-Driven Triggers** (Click to expand)"):
            st.markdown("""
            When events occur, agents are **automatically triggered**:

            | Event | Triggers |
            |-------|----------|
            | 📁 New Content Uploaded | Caption, Clip, Compliance, Archive |
            | 📝 Captions Complete | Localization, Social Publishing |
            | 🎬 Viral Clip Detected | Social Publishing |
            | 🚨 Compliance Alert | Social (post notice) |
            | 📈 Trending Spike | Social, Archive |
            | ⚠️ License Expiring | Rights Agent |
            | 🔴 Breaking News | Social, Trending |
            """)

        # Recent Autonomous Activity
        with st.expander("📋 **Recent Autonomous Activity**", expanded=True):
            auto_activity = [
                {"time": "Just now", "event": "📈 Trending Agent detected #NashvilleFire spike", "action": "Triggered Social Publishing"},
                {"time": "2 min ago", "event": "⚖️ Compliance scan completed", "action": "No issues found"},
                {"time": "5 min ago", "event": "📝 Caption Agent auto-processed new upload", "action": "Triggered Localization"},
                {"time": "8 min ago", "event": "🎬 Clip Agent found viral moment (94%)", "action": "Triggered Social Publishing"},
                {"time": "15 min ago", "event": "📜 Rights Agent license check", "action": "Alert: 2 licenses expiring soon"},
            ]

            for act in auto_activity:
                st.markdown(f"**{act['time']}** - {act['event']}")
                st.caption(f"→ {act['action']}")

    else:
        st.info("🔵 **Manual Mode** - Click 'Start Autonomous Mode' to enable background agent processing")
        st.markdown("""
        **In Autonomous Mode, agents will:**
        - 📈 Monitor trends every 5 minutes
        - ⚖️ Run compliance checks every 10 minutes
        - 📜 Check license expirations hourly
        - ⚡ Auto-trigger on events (new content, alerts, etc.)
        - 🔄 Chain workflows (captions → translations → social posts)
        """)

    # Real-time status indicator
    col1, col2 = st.columns([3, 1])
    with col2:
        st.markdown(f'<span class="realtime-indicator"></span> **Live** - {datetime.now().strftime("%I:%M %p")}', unsafe_allow_html=True)

    # Key Metrics
    st.subheader("Today's Performance")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Jobs Processed", "147", "+23 vs yesterday")
    col2.metric("Content Captioned", "48 hrs", "of video")
    col3.metric("Compliance Score", "96.2%", "+2.1%")
    col4.metric("Viral Clips Found", "12", "this week")
    col5.metric("Languages Served", "8", "active")

    st.divider()

    # Agent Grid with Real Capabilities
    st.subheader("AI Agent Suite - Full Capabilities")

    agents_detailed = [
        {
            "icon": "🎬",
            "name": "Clip Agent",
            "tagline": "Viral Moment Detection",
            "capabilities": ["AI scene analysis", "Emotion detection", "Viral scoring", "Auto-clipping", "Platform optimization"],
            "benefit": "10x social content output",
            "status": "active"
        },
        {
            "icon": "📝",
            "name": "Caption Agent",
            "tagline": "Intelligent Transcription",
            "capabilities": ["Real-time transcription", "Speaker diarization", "QA validation", "Multi-format export", "Accuracy scoring"],
            "benefit": "80% cost reduction",
            "status": "active"
        },
        {
            "icon": "⚖️",
            "name": "Compliance Agent",
            "tagline": "FCC Monitoring",
            "capabilities": ["Profanity detection", "Political ad checks", "Sponsorship ID", "EAS compliance", "Real-time alerts"],
            "benefit": "Avoid $500K+ fines",
            "status": "active"
        },
        {
            "icon": "🔍",
            "name": "Archive Agent",
            "tagline": "Intelligent Search",
            "capabilities": ["Natural language search", "AI tagging", "MAM integration", "Semantic matching", "Instant retrieval"],
            "benefit": "90% faster search",
            "status": "active"
        },
        {
            "icon": "📱",
            "name": "Social Publishing",
            "tagline": "Multi-Platform Content",
            "capabilities": ["Platform optimization", "Auto-formatting", "Hashtag AI", "Scheduled posting", "Analytics tracking"],
            "benefit": "24/7 social presence",
            "status": "active"
        },
        {
            "icon": "🌍",
            "name": "Localization",
            "tagline": "Global Distribution",
            "capabilities": ["AI translation", "Voice dubbing", "Cultural adaptation", "8+ languages", "Quality scoring"],
            "benefit": "Global reach instantly",
            "status": "active"
        },
        {
            "icon": "📜",
            "name": "Rights Agent",
            "tagline": "License Management",
            "capabilities": ["License tracking", "Expiry alerts", "Violation detection", "DMCA automation", "Usage reporting"],
            "benefit": "Legal protection",
            "status": "active"
        },
        {
            "icon": "📈",
            "name": "Trending Agent",
            "tagline": "Real-time Intelligence",
            "capabilities": ["Trend monitoring", "Breaking news alerts", "Sentiment analysis", "Story suggestions", "Competitor tracking"],
            "benefit": "Never miss a story",
            "status": "active"
        },
    ]

    cols = st.columns(4)
    for i, agent in enumerate(agents_detailed):
        with cols[i % 4]:
            with st.container():
                st.markdown(f"""
                <div class="capability-card">
                    <h3 style="margin: 0;">{agent['icon']} {agent['name']}</h3>
                    <p style="color: #a855f7; margin: 4px 0;">{agent['tagline']}</p>
                    <ul style="color: #94a3b8; font-size: 0.8rem; margin: 8px 0; padding-left: 16px;">
                        {''.join([f'<li>{cap}</li>' for cap in agent['capabilities'][:3]])}
                    </ul>
                    <p style="color: #22c55e; font-size: 0.85rem; margin: 8px 0 0 0;">✓ {agent['benefit']}</p>
                </div>
                """, unsafe_allow_html=True)

    st.divider()

    # Live Activity Feed
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Live Activity Feed")
        activity = [
            {"agent": "📝 Caption Agent", "action": "Completed morning news broadcast transcription", "time": "Just now", "status": "success"},
            {"agent": "⚖️ Compliance", "action": "ALERT: Potential FCC violation detected - Review needed", "time": "2 min ago", "status": "warning"},
            {"agent": "🎬 Clip Agent", "action": "Found 3 viral moments in warehouse fire coverage", "time": "5 min ago", "status": "success"},
            {"agent": "📈 Trending", "action": "#NashvilleFire trending - 45K posts/hour", "time": "8 min ago", "status": "info"},
            {"agent": "📜 Rights", "action": "WARNING: Wire Service license expires in 18 days", "time": "15 min ago", "status": "warning"},
            {"agent": "🌍 Localization", "action": "Spanish dub completed for breaking news segment", "time": "22 min ago", "status": "success"},
            {"agent": "📱 Social", "action": "Auto-posted fire coverage to 5 platforms", "time": "30 min ago", "status": "success"},
        ]

        for act in activity:
            status_color = {"success": "#22c55e", "warning": "#f59e0b", "info": "#3b82f6"}.get(act["status"], "#94a3b8")
            st.markdown(f"""
            <div style="display: flex; align-items: center; padding: 8px 0; border-bottom: 1px solid #334155;">
                <span style="min-width: 140px;">{act['agent']}</span>
                <span style="flex: 1; color: #e2e8f0;">{act['action']}</span>
                <span style="color: #64748b; font-size: 0.8rem;">{act['time']}</span>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.subheader("Quick Stats")

        # Processing stats
        st.markdown("**Processing Today**")
        st.metric("Video Processed", "48.2 hrs")
        st.metric("Captions Generated", "12,450 segments")
        st.metric("Clips Extracted", "47")
        st.metric("Posts Published", "28")

        st.divider()

        st.markdown("**System Health**")
        st.progress(0.96, "API Uptime: 99.6%")
        st.progress(0.82, "Processing Queue: 18%")
        st.progress(0.45, "Storage Used: 45%")


elif page == "🚀 All-in-One Workflow":
    st.title("🚀 All-in-One Workflow")
    st.caption("Process content through ALL 8 AI Agents simultaneously | Complete media intelligence in one click")

    st.markdown("""
    **The Complete Media Intelligence Pipeline** - Upload your content once and let all 8 AI agents
    analyze it simultaneously. Get captions, viral clips, compliance checks, social posts,
    translations, rights verification, and trending context - all in one workflow.
    """)

    st.divider()

    # Upload Section
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📁 Upload Content")
        uploaded_file = st.file_uploader(
            "Upload video or audio file",
            type=["mp4", "mov", "wav", "mp3", "m4a", "avi"],
            help="Supported formats: MP4, MOV, WAV, MP3, M4A, AVI"
        )

        use_demo = st.checkbox("Use demo content: Morning News Broadcast (4 hrs)", value=True)

        st.markdown("**Or enter content URL:**")
        content_url = st.text_input("Content URL", placeholder="https://your-mam-system.com/asset/12345")

    with col2:
        st.subheader("⚙️ Workflow Settings")

        st.markdown("**Select Agents to Run:**")
        run_caption = st.checkbox("📝 Caption Agent", value=True)
        run_clip = st.checkbox("🎬 Clip Agent", value=True)
        run_compliance = st.checkbox("⚖️ Compliance Agent", value=True)
        run_archive = st.checkbox("🔍 Archive Agent", value=True)
        run_social = st.checkbox("📱 Social Publishing", value=True)
        run_localization = st.checkbox("🌍 Localization", value=True)
        run_rights = st.checkbox("📜 Rights Agent", value=True)
        run_trending = st.checkbox("📈 Trending Agent", value=True)

        target_languages = st.multiselect("Translation Languages", ["Spanish", "French", "German", "Chinese"], default=["Spanish", "French"])

    st.divider()

    # Run All Agents Button
    if st.button("🚀 Run Complete Analysis", type="primary", use_container_width=True):
        st.session_state.all_in_one_running = True
        st.session_state.all_in_one_done = False

        # Create progress tracking
        st.subheader("📊 Processing Status")

        # Agent status containers
        agent_statuses = {}

        # Create columns for parallel status display
        col1, col2 = st.columns(2)

        agents_to_run = []
        if run_caption:
            agents_to_run.append({"name": "Caption Agent", "icon": "📝", "steps": ["Extracting audio", "Detecting speakers", "Transcribing", "Running QA"]})
        if run_clip:
            agents_to_run.append({"name": "Clip Agent", "icon": "🎬", "steps": ["Analyzing frames", "Detecting emotions", "Scoring virality", "Generating clips"]})
        if run_compliance:
            agents_to_run.append({"name": "Compliance Agent", "icon": "⚖️", "steps": ["Scanning audio", "Checking ads", "Validating EAS", "Generating report"]})
        if run_archive:
            agents_to_run.append({"name": "Archive Agent", "icon": "🔍", "steps": ["Extracting metadata", "AI tagging", "Indexing content", "MAM sync"]})
        if run_social:
            agents_to_run.append({"name": "Social Publishing", "icon": "📱", "steps": ["Analyzing content", "Generating posts", "Optimizing hashtags", "Scheduling"]})
        if run_localization:
            agents_to_run.append({"name": "Localization", "icon": "🌍", "steps": ["Translating", "Quality check", "Generating subtitles", "Voice synthesis"]})
        if run_rights:
            agents_to_run.append({"name": "Rights Agent", "icon": "📜", "steps": ["Checking licenses", "Scanning violations", "Verifying usage", "Generating alerts"]})
        if run_trending:
            agents_to_run.append({"name": "Trending Agent", "icon": "📈", "steps": ["Analyzing trends", "Matching topics", "Sentiment analysis", "Recommendations"]})

        # Progress display
        overall_progress = st.progress(0, "Starting all agents...")

        # Create status placeholders for each agent
        agent_containers = {}
        cols = st.columns(4)
        for i, agent in enumerate(agents_to_run):
            with cols[i % 4]:
                agent_containers[agent['name']] = st.empty()
                agent_containers[agent['name']].markdown(f"""
                <div style="background: #1e293b; padding: 12px; border-radius: 8px; margin-bottom: 8px; border-left: 3px solid #6366f1;">
                    <strong>{agent['icon']} {agent['name']}</strong><br/>
                    <span style="color: #f59e0b;">⏳ Waiting...</span>
                </div>
                """, unsafe_allow_html=True)

        # Simulate parallel processing
        import time
        total_steps = sum(len(a['steps']) for a in agents_to_run)
        completed_steps = 0

        for step_num in range(4):  # Max 4 steps per agent
            for i, agent in enumerate(agents_to_run):
                if step_num < len(agent['steps']):
                    current_step = agent['steps'][step_num]
                    with cols[i % 4]:
                        if step_num == len(agent['steps']) - 1:
                            # Last step - mark complete
                            agent_containers[agent['name']].markdown(f"""
                            <div style="background: #1e293b; padding: 12px; border-radius: 8px; margin-bottom: 8px; border-left: 3px solid #22c55e;">
                                <strong>{agent['icon']} {agent['name']}</strong><br/>
                                <span style="color: #22c55e;">✅ Complete</span>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            agent_containers[agent['name']].markdown(f"""
                            <div style="background: #1e293b; padding: 12px; border-radius: 8px; margin-bottom: 8px; border-left: 3px solid #f59e0b;">
                                <strong>{agent['icon']} {agent['name']}</strong><br/>
                                <span style="color: #f59e0b;">🔄 {current_step}...</span>
                            </div>
                            """, unsafe_allow_html=True)
                    completed_steps += 1

            overall_progress.progress(completed_steps / total_steps, f"Processing... {completed_steps}/{total_steps} steps complete")
            time.sleep(0.4)

        overall_progress.progress(1.0, "✅ All agents complete!")
        time.sleep(0.5)

        st.session_state.all_in_one_done = True
        st.session_state.all_in_one_running = False

    # Show Results
    if st.session_state.get("all_in_one_done"):
        st.divider()
        st.subheader("📋 Combined Results")

        # Summary Metrics
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        col1.metric("Captions", "13 segments", "96.2% accuracy")
        col2.metric("Viral Clips", "4 found", "Top: 97%")
        col3.metric("Compliance", "2 issues", "Review needed")
        col4.metric("Social Posts", "15 ready", "5 platforms")
        col5.metric("Translations", f"{len(target_languages)} languages", "94% quality")
        col6.metric("Trending Match", "3 topics", "#NashvilleFire")

        st.divider()

        # Tabbed Results
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "📝 Captions", "🎬 Viral Clips", "⚖️ Compliance", "🔍 Archive",
            "📱 Social", "🌍 Translations", "📜 Rights", "📈 Trending"
        ])

        with tab1:
            st.markdown("**Generated Captions** - 13 segments, 2 speakers detected")
            for cap in DEMO_CAPTIONS[:5]:
                st.markdown(f"""
                <div style="background: #1e293b; padding: 8px 12px; border-radius: 6px; margin: 4px 0; border-left: 3px solid #6366f1;">
                    <small style="color: #6366f1;">{format_srt_time(cap['start'])} → {format_srt_time(cap['end'])}</small>
                    <span style="color: #94a3b8; margin-left: 12px;">{cap['speaker']}</span><br/>
                    <span style="color: #e2e8f0;">{cap['text']}</span>
                </div>
                """, unsafe_allow_html=True)
            st.caption("... and 8 more segments")
            col1, col2 = st.columns(2)
            col1.download_button("📥 Download SRT", generate_srt(DEMO_CAPTIONS), "captions.srt", use_container_width=True)
            col2.download_button("📥 Download VTT", generate_srt(DEMO_CAPTIONS).replace(",", "."), "captions.vtt", use_container_width=True)

        with tab2:
            st.markdown("**Viral Moments Detected** - 4 clips ready for export")
            for moment in DEMO_VIRAL_MOMENTS[:3]:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{moment['title']}** ({moment['end']-moment['start']:.0f}s)")
                    st.caption(moment['description'])
                with col2:
                    st.metric("Viral Score", f"{moment['score']:.0%}")
            st.button("📤 Export All Clips", use_container_width=True)

        with tab3:
            st.markdown("**Compliance Scan Results** - 2 issues require attention")
            for issue in DEMO_COMPLIANCE_ISSUES[:2]:
                severity_icon = "🔴" if issue["severity"] == "critical" else "🟠"
                st.warning(f"{severity_icon} **{issue['type'].upper()}** @ {issue['timestamp']}\n\n{issue['description']}\n\n*Fine range: {issue['fine_range']}*")
            st.button("📝 Generate Compliance Report", use_container_width=True)

        with tab4:
            st.markdown("**Archive Metadata Generated**")
            st.json({
                "title": "Morning News Broadcast - Fire Coverage",
                "duration": "4:02:15",
                "speakers": ["Sarah Mitchell", "Jake Thompson", "Weather Team"],
                "topics": ["warehouse fire", "downtown Nashville", "breaking news"],
                "ai_tags": ["fire", "emergency", "reporter", "live coverage", "breaking"],
                "sentiment": "urgent/concerned",
                "quality": "HD 1080p"
            })
            st.button("📤 Send to MAM System", use_container_width=True)

        with tab5:
            st.markdown("**Social Posts Generated** - 15 posts across 5 platforms")
            platforms = ["Twitter/X", "Instagram", "TikTok", "Facebook", "YouTube Shorts"]
            for platform in platforms:
                st.markdown(f"**{platform}** - 3 posts ready")
            col1, col2 = st.columns(2)
            col1.button("📤 Post All Now", type="primary", use_container_width=True)
            col2.button("🕐 Schedule All", use_container_width=True)

        with tab6:
            st.markdown(f"**Translations Complete** - {len(target_languages)} languages")
            for lang in target_languages:
                lang_data = {"Spanish": ("🇪🇸", 96), "French": ("🇫🇷", 94), "German": ("🇩🇪", 95), "Chinese": ("🇨🇳", 93)}
                flag, score = lang_data.get(lang, ("🌍", 90))
                st.progress(score/100, f"{flag} {lang}: {score}% quality")
            st.button("📥 Download All Subtitle Files", use_container_width=True)

        with tab7:
            st.markdown("**Rights Verification**")
            st.success("✅ Content cleared for broadcast use")
            st.info("ℹ️ 2 licenses used: Wire Service Feed, Stock Images")
            st.warning("⚠️ Reminder: Wire Service license expires in 18 days")

        with tab8:
            st.markdown("**Trending Context**")
            st.markdown("Your content matches these trending topics:")
            for trend in DEMO_TRENDS[:3]:
                if trend['our_coverage']:
                    st.markdown(f"✅ **{trend['topic']}** - {trend['velocity']} ({trend['volume']})")
            st.info("💡 **AI Recommendation:** This content is highly relevant to current trends. Consider immediate publication for maximum reach.")

        st.divider()

        # Export All Results
        st.subheader("📦 Export Complete Package")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.button("📥 Download All Files (ZIP)", type="primary", use_container_width=True)
        with col2:
            st.button("📤 Send to MAM", use_container_width=True)
        with col3:
            st.button("📤 Publish to Social", use_container_width=True)
        with col4:
            st.button("📋 Generate Report (PDF)", use_container_width=True)


elif page == "Caption Agent":
    st.title("Caption Agent")
    st.caption("AI-Powered Transcription with Real-time QA | Speaker Diarization | Multi-format Export")

    # Capabilities showcase
    with st.expander("**Agent Capabilities** - Click to expand", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            **Transcription**
            - Real-time speech-to-text
            - 98%+ accuracy
            - Background noise handling
            - Multiple audio formats
            """)
        with col2:
            st.markdown("""
            **Analysis**
            - Speaker diarization
            - Confidence scoring
            - Profanity detection
            - Timing validation
            """)
        with col3:
            st.markdown("""
            **Export**
            - SRT, VTT, JSON formats
            - Broadcast-ready timing
            - Speaker labels
            - FCC compliance ready
            """)

    st.divider()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Upload Media")
        uploaded = st.file_uploader("Upload video or audio file", type=["mp4", "mov", "wav", "mp3", "m4a"])

        demo_mode = st.checkbox("Use demo: Morning News Broadcast (1:22)", value=True)

        if st.button("Generate Captions", type="primary", use_container_width=True):
            # Real-time processing simulation
            processing_container = st.container()
            with processing_container:
                steps = [
                    {"icon": "🎵", "text": "Extracting audio stream...", "duration": 0.4},
                    {"icon": "🔊", "text": "Detecting speech segments...", "duration": 0.5},
                    {"icon": "🎤", "text": "Identifying speakers (2 detected)...", "duration": 0.6},
                    {"icon": "📝", "text": "Transcribing with Whisper AI...", "duration": 0.8},
                    {"icon": "✅", "text": "Running QA validation...", "duration": 0.4},
                    {"icon": "🔍", "text": "Checking for profanity...", "duration": 0.3},
                    {"icon": "⏱️", "text": "Validating timing sync...", "duration": 0.3},
                ]
                simulate_realtime_processing(steps, processing_container)

            st.session_state.caption_done = True

    with col2:
        st.subheader("Settings")
        st.selectbox("Language", ["English (US)", "English (UK)", "Spanish", "French", "German"])
        st.checkbox("Speaker diarization", value=True)
        st.checkbox("Profanity filter check", value=True)
        st.checkbox("Auto-punctuation", value=True)
        st.slider("Confidence threshold", 0.7, 1.0, 0.90, 0.05)
        st.selectbox("Output format", ["SRT", "VTT", "JSON", "All formats"])

    if st.session_state.get("caption_done"):
        st.divider()

        # Results Summary
        st.subheader("Results")
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Segments", len(DEMO_CAPTIONS))
        col2.metric("Duration", "1:22")
        col3.metric("Speakers", "2")
        col4.metric("Avg Confidence", "96.2%")
        col5.metric("Words/Min", "152")

        tab1, tab2, tab3, tab4 = st.tabs(["📄 Captions", "✅ QA Report", "📊 Analytics", "⬇️ Export"])

        with tab1:
            # Interactive caption editor
            st.markdown("**Interactive Caption Editor** - Click any segment to edit")
            for cap in DEMO_CAPTIONS:
                conf_color = "#22c55e" if cap["confidence"] >= 0.95 else "#f59e0b" if cap["confidence"] >= 0.90 else "#ef4444"
                st.markdown(f"""
                <div class="caption-block">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                        <small style="color: #6366f1;">{format_srt_time(cap['start'])} → {format_srt_time(cap['end'])}</small>
                        <small style="color: {conf_color};">Confidence: {cap['confidence']:.0%}</small>
                    </div>
                    <div style="color: #e2e8f0; margin-bottom: 4px;">{cap['text']}</div>
                    <small style="color: #64748b;">🎤 {cap['speaker']}</small>
                </div>
                """, unsafe_allow_html=True)

        with tab2:
            st.markdown("**Quality Assurance Report**")
            issues_by_type = {"Critical": 0, "Warning": 1, "Info": 2, "Passed": 2}
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Critical", issues_by_type["Critical"], delta_color="inverse")
            col2.metric("Warnings", issues_by_type["Warning"])
            col3.metric("Info", issues_by_type["Info"])
            col4.metric("Passed", issues_by_type["Passed"])

            st.divider()
            for issue in DEMO_QA_ISSUES:
                if issue["type"] == "warning":
                    st.warning(f"⚠️ **{issue['issue']}** (Segment {issue['segment']} @ {issue['timestamp']})\n\n{issue['details']}\n\n💡 *{issue['suggestion']}*")
                elif issue["type"] == "info":
                    st.info(f"ℹ️ **{issue['issue']}** (Segment {issue['segment']} @ {issue['timestamp']})\n\n{issue['details']}")
                elif issue["type"] == "success":
                    st.success(f"✅ **{issue['issue']}**\n\n{issue['details']}")

        with tab3:
            st.markdown("**Transcription Analytics**")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Speaker Distribution**")
                speaker_data = {"Sarah Mitchell (Anchor)": 45, "Jake Thompson (Reporter)": 37}
                for speaker, seconds in speaker_data.items():
                    st.progress(seconds / 82, f"{speaker}: {seconds}s")

            with col2:
                st.markdown("**Confidence Distribution**")
                st.progress(0.85, "High (>95%): 85%")
                st.progress(0.12, "Medium (90-95%): 12%")
                st.progress(0.03, "Low (<90%): 3%")

            st.markdown("**Words per Speaker**")
            col1, col2 = st.columns(2)
            col1.metric("Sarah Mitchell", "98 words")
            col2.metric("Jake Thompson", "109 words")

        with tab4:
            st.markdown("**Export Options**")
            srt_content = generate_srt(DEMO_CAPTIONS)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button("📥 Download SRT", srt_content, "morning_news_captions.srt", "text/plain", use_container_width=True)
            with col2:
                st.download_button("📥 Download VTT", srt_content.replace(",", "."), "morning_news_captions.vtt", "text/plain", use_container_width=True)
            with col3:
                import json
                json_content = json.dumps(DEMO_CAPTIONS, indent=2)
                st.download_button("📥 Download JSON", json_content, "morning_news_captions.json", "application/json", use_container_width=True)

            st.divider()
            st.markdown("**Integration Export**")
            col1, col2 = st.columns(2)
            with col1:
                st.button("📤 Send to MAM System", use_container_width=True)
            with col2:
                st.button("📤 Send to Automation", use_container_width=True)


elif page == "Clip Agent":
    st.title("Clip Agent")
    st.caption("AI-Powered Viral Moment Detection | Emotion Analysis | Multi-Platform Optimization")

    # Capabilities showcase
    with st.expander("**Agent Capabilities** - Click to expand", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
            **Scene Analysis**
            - AI scene detection
            - Visual content analysis
            - Motion tracking
            - Key frame extraction
            """)
        with col2:
            st.markdown("""
            **Emotion Detection**
            - Facial expression analysis
            - Voice emotion detection
            - Sentiment scoring
            - Engagement prediction
            """)
        with col3:
            st.markdown("""
            **Viral Scoring**
            - Multi-factor scoring
            - Platform optimization
            - Hashtag suggestions
            - View predictions
            """)
        with col4:
            st.markdown("""
            **Auto-Clipping**
            - Intelligent boundaries
            - Aspect ratio conversion
            - Thumbnail generation
            - Batch export
            """)

    st.divider()

    uploaded = st.file_uploader("Upload broadcast recording", type=["mp4", "mov", "avi"])
    demo_mode = st.checkbox("Use demo: 4-hour morning broadcast with fire coverage", value=True)

    col1, col2 = st.columns([3, 1])
    with col2:
        st.markdown("**Detection Settings**")
        emotion_threshold = st.slider("Emotion threshold", 0.5, 1.0, 0.7)
        min_score = st.slider("Min viral score", 0.5, 1.0, 0.8)
        platforms = st.multiselect("Target platforms", ["TikTok", "Twitter/X", "Instagram", "YouTube Shorts", "Facebook"], default=["TikTok", "Twitter/X", "Instagram"])

    if st.button("Analyze & Find Viral Moments", type="primary", use_container_width=True):
        processing_container = st.container()
        with processing_container:
            steps = [
                {"icon": "🎬", "text": "Loading video frames...", "duration": 0.5},
                {"icon": "👁️", "text": "Running GPT-4 Vision analysis...", "duration": 0.8},
                {"icon": "😀", "text": "Detecting facial emotions...", "duration": 0.6},
                {"icon": "🔊", "text": "Analyzing audio peaks...", "duration": 0.5},
                {"icon": "📊", "text": "Calculating viral scores...", "duration": 0.4},
                {"icon": "✂️", "text": "Identifying clip boundaries...", "duration": 0.4},
                {"icon": "🏷️", "text": "Generating hashtag suggestions...", "duration": 0.3},
            ]
            simulate_realtime_processing(steps, processing_container)
        st.session_state.clip_done = True

    if st.session_state.get("clip_done"):
        st.divider()

        # Summary metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Moments Found", len(DEMO_VIRAL_MOMENTS))
        col2.metric("High Viral (>90%)", "3")
        col3.metric("Total Clip Time", "1:42")
        col4.metric("Est. Total Reach", "2.5M - 8M")
        col5.metric("Platforms Optimized", len(platforms))

        st.subheader(f"Viral Moments Detected")

        for moment in DEMO_VIRAL_MOMENTS:
            score_color = "#22c55e" if moment['score'] >= 0.9 else "#f59e0b" if moment['score'] >= 0.8 else "#3b82f6"

            with st.expander(f"**{moment['title']}** — Viral Score: {moment['score']:.0%}", expanded=moment['score'] >= 0.95):
                col1, col2, col3 = st.columns([2, 1, 1])

                with col1:
                    st.markdown(f"**Description:** {moment['description']}")
                    st.markdown(f"**Timestamp:** `{moment['start']:.0f}s` - `{moment['end']:.0f}s` ({moment['end']-moment['start']:.0f}s clip)")

                    st.markdown("**Transcript:**")
                    st.code(moment['transcript'], language=None)

                    st.markdown(f"**Suggested Hashtags:**")
                    st.markdown(' '.join([f'`{h}`' for h in moment['hashtags']]))

                with col2:
                    st.markdown("**Viral Metrics**")
                    st.metric("Viral Score", f"{moment['score']:.0%}")
                    st.metric("Predicted Views", moment['predicted_views'])
                    st.metric("Emotion", moment['emotion'].title())

                    st.markdown("**Audio Peaks**")
                    for peak in moment.get('audio_peaks', [])[:3]:
                        st.caption(f"📍 {peak:.1f}s")

                with col3:
                    st.markdown("**Face Emotions**")
                    for emotion, score in moment.get('face_emotions', {}).items():
                        st.progress(score, f"{emotion.title()}: {score:.0%}")

                    st.markdown("**Best Platforms**")
                    for p in moment['platforms']:
                        st.write(f"✓ {p}")

                st.divider()
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.button(f"✂️ Export Clip", key=f"export_{moment['id']}", use_container_width=True)
                with col2:
                    st.button(f"📱 Send to Social", key=f"social_{moment['id']}", use_container_width=True)
                with col3:
                    st.button(f"🖼️ Gen Thumbnail", key=f"thumb_{moment['id']}", use_container_width=True)
                with col4:
                    st.button(f"📤 Send to MAM", key=f"mam_{moment['id']}", use_container_width=True)


elif page == "Archive Agent":
    st.title("Archive Agent")
    st.caption("Natural Language Search | AI-Powered Tagging | MAM Integration")

    # Capabilities showcase
    with st.expander("**Agent Capabilities** - Click to expand", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            **Intelligent Search**
            - Natural language queries
            - Semantic understanding
            - Context-aware results
            - Multi-field search
            """)
        with col2:
            st.markdown("""
            **AI Tagging**
            - Auto-categorization
            - Face recognition
            - Scene detection
            - Topic extraction
            """)
        with col3:
            st.markdown("""
            **MAM Integration**
            - Bi-directional sync
            - Metadata enrichment
            - Proxy generation
            - Workflow triggers
            """)

    st.divider()

    query = st.text_input("Search your archive using natural language", placeholder="Try: 'hurricane coverage from October' or 'interviews with tech executives'")

    st.markdown("**Quick searches:**")
    col1, col2, col3, col4, col5 = st.columns(5)
    if col1.button("Election coverage", use_container_width=True):
        query = "election coverage 2024"
    if col2.button("Weather events", use_container_width=True):
        query = "hurricane tornado weather"
    if col3.button("Sports highlights", use_container_width=True):
        query = "superbowl sports gold"
    if col4.button("Entertainment", use_container_width=True):
        query = "concert entertainment music"
    if col5.button("Breaking news", use_container_width=True):
        query = "breaking emergency"

    if query:
        # Processing simulation
        with st.spinner("Searching with AI semantic matching..."):
            time.sleep(0.8)

        st.divider()

        # Filter results based on query
        results = [r for r in DEMO_ARCHIVE if any(word.lower() in (r['title'] + r['tags'] + r['description']).lower() for word in query.split())]
        if not results:
            results = DEMO_ARCHIVE[:4]

        # Results summary
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Results Found", len(results))
        col2.metric("Total Duration", f"{sum([int(r['duration'].split(':')[0]) for r in results])}+ hrs")
        col3.metric("Storage Size", f"{sum([float(r['size'].replace(' GB', '')) for r in results]):.1f} GB")
        col4.metric("Search Time", "0.8s")

        st.success(f"Found **{len(results)} results** for '{query}'")

        for r in results:
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                with col1:
                    st.markdown(f"**{r['title']}**")
                    st.caption(f"{r['description']}")
                    st.caption(f"📅 {r['date']} • 🎤 {r['speaker']} • ⏱️ {r['duration']} • 📦 {r['format']} • 💾 {r['size']}")
                    st.caption(f"Tags: {r['tags']}")
                with col2:
                    st.button("▶️ Preview", key=f"preview_{r['id']}", use_container_width=True)
                with col3:
                    st.button("📤 Export", key=f"export_{r['id']}", use_container_width=True)
                with col4:
                    st.button("📋 Metadata", key=f"meta_{r['id']}", use_container_width=True)
                st.divider()


elif page == "Compliance Agent":
    st.title("Compliance Agent")
    st.caption("24/7 FCC Compliance Monitoring | Real-time Violation Detection | Avoid $500K+ Fines")

    # Capabilities showcase
    with st.expander("**Agent Capabilities** - Click to expand", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
            **Content Analysis**
            - Profanity detection
            - Indecency scanning
            - Violence detection
            - Hate speech flagging
            """)
        with col2:
            st.markdown("""
            **Ad Compliance**
            - Political ad disclosure
            - Sponsorship ID
            - Product placement
            - Contest rules
            """)
        with col3:
            st.markdown("""
            **Regulatory**
            - EAS compliance
            - Closed caption check
            - Children's programming
            - Loudness standards
            """)
        with col4:
            st.markdown("""
            **Reporting**
            - Real-time alerts
            - Incident logging
            - Audit trails
            - FCC filing support
            """)

    st.divider()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Scan Content")
        uploaded = st.file_uploader("Upload broadcast for compliance scanning", type=["mp4", "mov", "wav", "mp3"])
        demo_mode = st.checkbox("Use demo: Morning broadcast with compliance issues", value=True)

        if st.button("Run Full Compliance Scan", type="primary", use_container_width=True):
            processing_container = st.container()
            with processing_container:
                steps = [
                    {"icon": "🔊", "text": "Analyzing audio for profanity...", "duration": 0.6},
                    {"icon": "👁️", "text": "Scanning video for indecent content...", "duration": 0.7},
                    {"icon": "📺", "text": "Checking political ad disclosures...", "duration": 0.5},
                    {"icon": "💰", "text": "Verifying sponsorship identification...", "duration": 0.4},
                    {"icon": "🚨", "text": "Validating EAS compliance...", "duration": 0.4},
                    {"icon": "📝", "text": "Checking closed caption requirements...", "duration": 0.3},
                    {"icon": "📊", "text": "Generating compliance report...", "duration": 0.3},
                ]
                simulate_realtime_processing(steps, processing_container)
            st.session_state.compliance_done = True

    with col2:
        st.subheader("Scan Settings")
        st.checkbox("Profanity/Indecency", value=True)
        st.checkbox("Political Ad Disclosure (47 U.S.C. 315)", value=True)
        st.checkbox("Sponsorship ID (47 U.S.C. 317)", value=True)
        st.checkbox("EAS Compliance (47 CFR Part 11)", value=True)
        st.checkbox("Caption Requirements (47 CFR 79.1)", value=True)
        st.checkbox("Loudness (CALM Act)", value=True)
        st.slider("Detection sensitivity", 0.7, 1.0, 0.85)

    if st.session_state.get("compliance_done"):
        st.divider()

        # Risk Score Dashboard
        risk_score = 42  # Lower is better
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Risk Score", f"{risk_score}/100", "ELEVATED", delta_color="inverse")
        col2.metric("Critical Issues", "2", "Immediate action")
        col3.metric("High Issues", "1", "Review needed")
        col4.metric("Medium Issues", "1", "Monitor")
        col5.metric("Potential Fines", "$85K - $1.1M", "If not addressed")

        st.divider()

        # Visual risk indicator
        st.markdown("**Compliance Risk Level**")
        risk_color = "#ef4444" if risk_score > 60 else "#f59e0b" if risk_score > 30 else "#22c55e"
        st.progress(risk_score / 100, f"Risk: {risk_score}%")

        st.divider()
        st.subheader("Issues Detected")

        for issue in DEMO_COMPLIANCE_ISSUES:
            severity_icon = "🔴" if issue["severity"] == "critical" else "🟠" if issue["severity"] == "high" else "🟡"
            severity_color = "#ef4444" if issue["severity"] == "critical" else "#f97316" if issue["severity"] == "high" else "#f59e0b"

            with st.expander(f"{severity_icon} **{issue['type'].upper().replace('_', ' ')}** @ {issue['timestamp']} — {issue['severity'].upper()}", expanded=issue["severity"]=="critical"):
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.markdown(f"### {issue['description']}")
                    st.markdown(f"**Context:** {issue['context']}")
                    st.divider()
                    st.markdown(f"**FCC Rule:** `{issue['fcc_rule']}`")
                    st.markdown(f"**Potential Fine:** `{issue['fine_range']}`")
                    st.markdown(f"**Precedent:** {issue['precedent']}")

                with col2:
                    st.markdown("**Detection Info**")
                    st.metric("Confidence", f"{issue['confidence']:.0%}")
                    st.metric("Auto-Detected", "Yes" if issue['auto_detected'] else "No")

                st.divider()
                st.info(f"💡 **Recommended Action:** {issue['recommendation']}")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.button("📝 Create Incident Report", key=f"report_{issue['type']}", use_container_width=True)
                with col2:
                    st.button("✅ Mark Resolved", key=f"resolve_{issue['type']}", use_container_width=True)
                with col3:
                    st.button("👁️ View in Timeline", key=f"view_{issue['type']}", use_container_width=True)


elif page == "Social Publishing":
    st.title("Social Publishing Agent")
    st.caption("AI-Generated Platform-Optimized Content | Multi-Platform Scheduling | Analytics")

    # Capabilities showcase
    with st.expander("**Agent Capabilities** - Click to expand", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
            **Content Generation**
            - AI copywriting
            - Platform-specific tone
            - Character optimization
            - Emoji suggestions
            """)
        with col2:
            st.markdown("""
            **Hashtag Intelligence**
            - Trending hashtags
            - Performance prediction
            - Competition analysis
            - Custom suggestions
            """)
        with col3:
            st.markdown("""
            **Scheduling**
            - Optimal time detection
            - Multi-platform sync
            - Queue management
            - Auto-posting
            """)
        with col4:
            st.markdown("""
            **Analytics**
            - Engagement prediction
            - Performance tracking
            - A/B testing
            - ROI reporting
            """)

    st.divider()

    col1, col2 = st.columns([2, 1])

    with col1:
        content_type = st.selectbox("Select content type", ["Breaking News - Fire Coverage", "Feel-Good Story - Dog Reunion"])

        target_platforms = st.multiselect(
            "Target platforms",
            ["Twitter/X", "Instagram", "TikTok", "Facebook", "YouTube Shorts"],
            default=["Twitter/X", "Instagram", "TikTok"]
        )

    with col2:
        st.markdown("**Generation Settings**")
        tone = st.selectbox("Tone", ["Urgent/Breaking", "Informative", "Emotional", "Casual"])
        include_emojis = st.checkbox("Include emojis", value=True)
        include_hashtags = st.checkbox("Auto-generate hashtags", value=True)
        cta = st.checkbox("Include call-to-action", value=True)

    if st.button("Generate Social Posts", type="primary", use_container_width=True):
        processing_container = st.container()
        with processing_container:
            steps = [
                {"icon": "📝", "text": "Analyzing content context...", "duration": 0.4},
                {"icon": "🎯", "text": "Optimizing for each platform...", "duration": 0.5},
                {"icon": "#️⃣", "text": "Generating trending hashtags...", "duration": 0.4},
                {"icon": "📊", "text": "Predicting engagement rates...", "duration": 0.3},
                {"icon": "⏰", "text": "Calculating optimal post times...", "duration": 0.3},
            ]
            simulate_realtime_processing(steps, processing_container)
        st.session_state.social_done = True
        st.session_state.social_type = "breaking_news" if "Breaking" in content_type else "feel_good"

    if st.session_state.get("social_done"):
        posts = DEMO_SOCIAL_POSTS[st.session_state.social_type]
        filtered_posts = [p for p in posts if p['platform'] in target_platforms]

        st.divider()

        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Posts Generated", len(filtered_posts))
        col2.metric("Platforms", len(set(p['platform'] for p in filtered_posts)))
        col3.metric("Est. Total Reach", f"{sum([int(p['predicted_engagement'].replace('K', '000')) for p in filtered_posts]):,}")
        col4.metric("Optimal Time", filtered_posts[0]['best_time'] if filtered_posts else "N/A")

        st.subheader("Generated Posts")

        for post in filtered_posts:
            platform_icons = {"Twitter/X": "𝕏", "Instagram": "📸", "TikTok": "🎵", "Facebook": "📘", "YouTube Shorts": "▶️"}

            with st.container():
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"### {platform_icons.get(post['platform'], '📱')} {post['platform']}")
                    st.code(post['content'], language=None)

                    # Platform-specific limits
                    max_chars = {"Twitter/X": 280, "Instagram": 2200, "TikTok": 150, "Facebook": 63206, "YouTube Shorts": 100}
                    limit = max_chars.get(post['platform'], 280)
                    char_pct = post['char_count'] / limit
                    char_color = "#22c55e" if char_pct < 0.8 else "#f59e0b" if char_pct < 1.0 else "#ef4444"
                    st.caption(f"Characters: {post['char_count']}/{limit} | Best time: {post['best_time']}")

                with col2:
                    st.metric("Est. Engagement", post['predicted_engagement'])
                    st.button("📋 Copy", key=f"copy_{post['platform']}_{st.session_state.social_type}", use_container_width=True)
                    st.button("📤 Post Now", key=f"post_{post['platform']}_{st.session_state.social_type}", use_container_width=True)
                    st.button("🕐 Schedule", key=f"schedule_{post['platform']}_{st.session_state.social_type}", use_container_width=True)

                st.divider()

        # Batch actions
        st.subheader("Batch Actions")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("📤 Post All Now", type="primary", use_container_width=True)
        with col2:
            st.button("🕐 Schedule All (Optimal Times)", use_container_width=True)
        with col3:
            st.button("📥 Export All to CSV", use_container_width=True)


elif page == "Localization":
    st.title("Localization Agent")
    st.caption("AI Translation | Voice Dubbing | Cultural Adaptation | Global Distribution")

    # Capabilities showcase
    with st.expander("**Agent Capabilities** - Click to expand", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
            **Translation**
            - 50+ languages
            - Context-aware AI
            - Broadcast terminology
            - Style preservation
            """)
        with col2:
            st.markdown("""
            **Voice Dubbing**
            - AI voice synthesis
            - Voice cloning
            - Lip-sync ready
            - Multiple voices
            """)
        with col3:
            st.markdown("""
            **Quality Assurance**
            - Native speaker review
            - Quality scoring
            - Cultural adaptation
            - Brand consistency
            """)
        with col4:
            st.markdown("""
            **Output**
            - SRT/VTT subtitles
            - Dubbed audio tracks
            - Burned-in captions
            - Multiple formats
            """)

    st.divider()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Source Content")
        st.info("**Demo:** Morning News Broadcast (1:22) - English (US)")

        languages = st.multiselect(
            "Select target languages",
            list(DEMO_TRANSLATIONS.keys()),
            default=["es", "fr", "de", "zh"],
            format_func=lambda x: f"{DEMO_TRANSLATIONS[x]['flag']} {DEMO_TRANSLATIONS[x]['name']}"
        )

    with col2:
        st.subheader("Output Options")
        st.checkbox("Generate subtitles (SRT/VTT)", value=True)
        generate_dub = st.checkbox("Generate AI voice dubs", value=False)
        st.checkbox("Burn-in captions option", value=False)
        st.selectbox("Quality level", ["Standard", "Professional", "Broadcast"])

        if generate_dub:
            st.selectbox("Voice style", ["News Anchor", "Reporter", "Conversational"])

    if languages and st.button("Start Localization", type="primary", use_container_width=True):
        processing_container = st.container()
        with processing_container:
            steps = [
                {"icon": "📝", "text": "Preparing source transcript...", "duration": 0.3},
                {"icon": "🌍", "text": f"Translating to {len(languages)} languages...", "duration": 0.8},
                {"icon": "✅", "text": "Running quality validation...", "duration": 0.5},
                {"icon": "🎙️", "text": "Generating subtitle files...", "duration": 0.4},
            ]
            if generate_dub:
                steps.append({"icon": "🔊", "text": "Synthesizing AI voice dubs...", "duration": 0.6})
            simulate_realtime_processing(steps, processing_container)
        st.session_state.local_done = True
        st.session_state.local_langs = languages

    if st.session_state.get("local_done"):
        st.divider()

        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Languages", len(st.session_state.local_langs))
        col2.metric("Avg Quality", f"{sum([DEMO_TRANSLATIONS[l]['quality_score'] for l in st.session_state.local_langs]) / len(st.session_state.local_langs):.0f}%")
        col3.metric("Files Generated", len(st.session_state.local_langs) * 2)
        col4.metric("Processing Time", "2.4s")

        st.subheader("Localization Results")

        for lang in st.session_state.local_langs:
            trans = DEMO_TRANSLATIONS[lang]
            quality_color = "#22c55e" if trans['quality_score'] >= 95 else "#f59e0b" if trans['quality_score'] >= 90 else "#ef4444"

            with st.expander(f"{trans['flag']} **{trans['name']}** — Quality: {trans['quality_score']}%", expanded=True):
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.markdown("**Original (English):**")
                    st.code(trans['sample_original'], language=None)

                    st.markdown(f"**Translated ({trans['name']}):**")
                    st.code(trans['sample_translated'], language=None)

                    st.caption(f"📝 **Translation Notes:** {trans['notes']}")

                with col2:
                    st.metric("Quality Score", f"{trans['quality_score']}%")
                    st.metric("Voice Available", "Yes" if trans['voice_available'] else "No")

                    if trans.get('dialect_options'):
                        st.markdown("**Dialect Options:**")
                        for dialect in trans['dialect_options']:
                            st.caption(f"• {dialect}")

                st.divider()
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.download_button(f"📥 Download SRT", f"Demo SRT content for {lang}", f"captions_{lang}.srt", use_container_width=True)
                with col2:
                    st.download_button(f"📥 Download VTT", f"Demo VTT content for {lang}", f"captions_{lang}.vtt", use_container_width=True)
                with col3:
                    if trans['voice_available']:
                        st.button(f"🔊 Preview Dub", key=f"dub_{lang}", use_container_width=True)


elif page == "Rights Agent":
    st.title("Rights Agent")
    st.caption("License Tracking | Violation Detection | DMCA Automation | Legal Protection")

    # Capabilities showcase
    with st.expander("**Agent Capabilities** - Click to expand", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
            **License Management**
            - Central repository
            - Expiry tracking
            - Renewal alerts
            - Cost analysis
            """)
        with col2:
            st.markdown("""
            **Violation Detection**
            - Content ID matching
            - Platform monitoring
            - Audio fingerprinting
            - Visual matching
            """)
        with col3:
            st.markdown("""
            **Enforcement**
            - DMCA automation
            - Takedown tracking
            - Damage estimation
            - Legal documentation
            """)
        with col4:
            st.markdown("""
            **Reporting**
            - Usage analytics
            - Compliance scoring
            - Cost optimization
            - Audit trails
            """)

    st.divider()

    if st.button("Run Full Rights Audit", type="primary", use_container_width=True):
        processing_container = st.container()
        with processing_container:
            steps = [
                {"icon": "📄", "text": "Loading license database...", "duration": 0.3},
                {"icon": "📅", "text": "Checking expiration dates...", "duration": 0.4},
                {"icon": "🔍", "text": "Scanning platforms for violations...", "duration": 0.7},
                {"icon": "🎵", "text": "Running audio fingerprint matches...", "duration": 0.5},
                {"icon": "📊", "text": "Calculating compliance scores...", "duration": 0.3},
                {"icon": "⚠️", "text": "Generating alerts...", "duration": 0.2},
            ]
            simulate_realtime_processing(steps, processing_container)
        st.session_state.rights_done = True

    if st.session_state.get("rights_done"):
        st.divider()

        # Dashboard metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Active Licenses", len(DEMO_LICENSES))
        col2.metric("Expiring Soon", "2", "Within 30 days", delta_color="inverse")
        col3.metric("Violations Found", len(DEMO_VIOLATIONS))
        col4.metric("Annual Spend", "$2.66M")
        col5.metric("Compliance Score", "97%")

        st.divider()

        # Tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(["⚠️ Alerts", "📄 Licenses", "🚨 Violations", "📊 Analytics"])

        with tab1:
            st.subheader("Urgent Alerts")

            # Expiring soon alerts
            for lic in [l for l in DEMO_LICENSES if l["status"] == "expiring_soon"]:
                st.warning(f"""
                **License Expiring: {lic['title']}**

                Expires in **{lic['days_remaining']} days** ({lic['end_date']})

                Licensor: {lic['licensor']} | Cost: {lic['cost']}

                **Action Required:** Initiate renewal negotiations immediately
                """)

            # Violation alerts
            for v in DEMO_VIOLATIONS:
                if v['status'] in ['Under Review', 'DMCA Filed']:
                    st.error(f"""
                    **Violation Detected: {v['content']}**

                    Platform: {v['platform']} | Views: {v['views']} | Status: {v['status']}

                    Estimated Damages: {v['estimated_damages']}
                    """)

        with tab2:
            st.subheader("License Portfolio")

            for lic in DEMO_LICENSES:
                status_color = "🟢" if lic["status"] == "active" and lic["days_remaining"] > 30 else "🟡" if lic["status"] == "expiring_soon" else "🔴"

                with st.expander(f"{status_color} **{lic['title']}** — {lic['days_remaining']} days remaining"):
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.markdown("**License Details**")
                        st.markdown(f"Licensor: {lic['licensor']}")
                        st.markdown(f"Type: {lic['type']}")
                        st.markdown(f"Cost: {lic['cost']}")
                        st.markdown(f"Period: {lic['start_date']} to {lic['end_date']}")

                    with col2:
                        st.markdown("**Rights Granted**")
                        for right in lic['rights']:
                            st.markdown(f"✓ {right}")
                        st.markdown("**Territories**")
                        for territory in lic['territories']:
                            st.markdown(f"• {territory}")

                    with col3:
                        st.markdown("**Usage & Compliance**")
                        st.metric("This Month", f"{lic['usage_this_month']} uses")
                        st.metric("Compliance", f"{lic['compliance_score']}%")

                    st.caption(f"**Restrictions:** {lic['restrictions']}")

        with tab3:
            st.subheader("Detected Violations")

            for v in DEMO_VIOLATIONS:
                status_color = {"DMCA Filed": "#f59e0b", "Under Review": "#3b82f6", "Takedown Requested": "#ef4444"}.get(v['status'], "#94a3b8")

                with st.container():
                    col1, col2, col3 = st.columns([2, 1, 1])

                    with col1:
                        st.markdown(f"**{v['content']}**")
                        st.markdown(f"Platform: **{v['platform']}** | Channel: {v['channel']}")
                        st.caption(f"Detected: {v['detected']} | URL: {v['url']}")

                    with col2:
                        st.metric("Views", v['views'])
                        st.metric("Match Confidence", f"{v['match_confidence']:.0%}")

                    with col3:
                        st.markdown(f"**Status:** {v['status']}")
                        st.markdown(f"**Est. Damages:** {v['estimated_damages']}")
                        st.button("📝 File DMCA", key=f"dmca_{v['content']}", use_container_width=True)

                    st.divider()

        with tab4:
            st.subheader("Rights Analytics")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**License Cost by Type**")
                costs = {"Sports": 2400000, "News Feeds": 180000, "Stock Media": 45000, "Music": 35000}
                for license_type, cost in costs.items():
                    st.progress(cost / 2500000, f"{license_type}: ${cost:,}")

            with col2:
                st.markdown("**Compliance by License**")
                for lic in DEMO_LICENSES:
                    st.progress(lic['compliance_score'] / 100, f"{lic['title'][:25]}...: {lic['compliance_score']}%")


elif page == "Trending Agent":
    st.title("Trending Agent")
    st.caption("Real-time Trend Monitoring | Breaking News Alerts | Story Suggestions")

    # Capabilities showcase
    with st.expander("**Agent Capabilities** - Click to expand", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
            **Trend Detection**
            - Real-time monitoring
            - Velocity tracking
            - Geographic filtering
            - Topic clustering
            """)
        with col2:
            st.markdown("""
            **Sentiment Analysis**
            - Public opinion tracking
            - Emotion detection
            - Controversy alerts
            - Brand monitoring
            """)
        with col3:
            st.markdown("""
            **Story Suggestions**
            - AI-powered angles
            - Coverage gaps
            - Competitor tracking
            - Audience interest
            """)
        with col4:
            st.markdown("""
            **Alerts**
            - Breaking news
            - Trend spikes
            - Sentiment shifts
            - Custom triggers
            """)

    st.divider()

    # Real-time header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f'<span class="realtime-indicator"></span> **Live Monitoring** - Last updated: {datetime.now().strftime("%I:%M:%S %p")}', unsafe_allow_html=True)
    with col2:
        if st.button("🔄 Refresh Now", use_container_width=True):
            st.rerun()

    # Breaking News Section
    st.subheader("Breaking News Alerts")
    for news in DEMO_BREAKING:
        urgency_color = "#dc2626" if news["urgency"] == "high" else "#f59e0b"
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, {urgency_color}22, {urgency_color}11); border-left: 4px solid {urgency_color}; padding: 16px; border-radius: 8px; margin: 8px 0;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong style="font-size: 1.1rem;">{news['headline']}</strong>
                <span style="background: {urgency_color}; padding: 4px 12px; border-radius: 4px; font-size: 0.8rem;">{news['urgency'].upper()}</span>
            </div>
            <p style="margin: 8px 0; opacity: 0.9;">{news['summary']}</p>
            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; opacity: 0.7;">
                <span>Source: {news['source']} | {news['time']}</span>
                <span>Confidence: {news['confidence']:.0%}</span>
            </div>
            <p style="color: #fef08a; margin-top: 8px; font-size: 0.9rem;">➡️ {news['action']}</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Trending Topics
    st.subheader("Trending Topics")

    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        category_filter = st.selectbox("Category", ["All", "Local Breaking", "Finance", "Sports", "Entertainment"])
    with col2:
        velocity_filter = st.selectbox("Velocity", ["All", "Exploding", "Rising", "Steady"])
    with col3:
        coverage_filter = st.selectbox("Coverage Status", ["All", "Covering", "Not Covering"])

    for trend in DEMO_TRENDS:
        # Apply filters
        if category_filter != "All" and trend['category'] != category_filter:
            continue
        if velocity_filter != "All" and velocity_filter not in trend['velocity']:
            continue
        if coverage_filter == "Covering" and not trend['our_coverage']:
            continue
        if coverage_filter == "Not Covering" and trend['our_coverage']:
            continue

        velocity_icon = "🚀" if "Exploding" in trend['velocity'] else "📈" if "Rising" in trend['velocity'] else "📊"
        coverage_badge = "✅ Covering" if trend["our_coverage"] else "📝 Not covering"
        sentiment_color = "#22c55e" if trend['sentiment_score'] > 0.3 else "#ef4444" if trend['sentiment_score'] < -0.3 else "#f59e0b"

        with st.expander(f"{velocity_icon} **{trend['topic']}** — {trend['velocity']} ({trend['velocity_score']})", expanded=trend['velocity_score'] > 90):
            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                st.markdown(f"**Category:** {trend['category']} | **Status:** {coverage_badge}")
                st.markdown(f"**Volume:** {trend['volume']}")

                st.markdown("**Top Posts:**")
                for post in trend['top_posts']:
                    st.caption(f"• \"{post}\"")

                st.markdown("**Related Topics:**")
                st.markdown(' '.join([f'`{t}`' for t in trend.get('related_topics', [])]))

            with col2:
                st.markdown("**Sentiment Analysis**")
                st.metric("Sentiment", trend['sentiment'])
                st.progress((trend['sentiment_score'] + 1) / 2, f"Score: {trend['sentiment_score']:.2f}")

                st.markdown("**Demographics**")
                for age, pct in trend.get('demographics', {}).items():
                    st.progress(pct / 100, f"{age}: {pct}%")

            with col3:
                st.markdown("**AI Recommendation**")
                st.info(trend['recommendation'])

                if not trend['our_coverage']:
                    st.button("📝 Create Story", key=f"story_{trend['topic']}", use_container_width=True)
                st.button("📊 Full Analysis", key=f"analysis_{trend['topic']}", use_container_width=True)


elif page == "Integration Showcase":
    st.title("Integration Showcase")
    st.caption("Enterprise-Grade Connectivity | Industry-Standard Protocols | Production-Ready APIs")

    st.markdown("""
    MediaAgentIQ seamlessly integrates with your existing broadcast infrastructure.
    Our platform supports industry-standard protocols and can connect to virtually any
    media asset management, broadcast automation, or content delivery system.
    """)

    st.divider()

    # Integration overview metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Supported Protocols", "15+")
    col2.metric("Integration Types", "6 Categories")
    col3.metric("API Uptime", "99.9%")
    col4.metric("Avg Response Time", "<100ms")

    st.divider()

    # Integration Categories
    st.subheader("Integration Capabilities")

    for key, integration in INTEGRATION_CAPABILITIES.items():
        status_color = "#22c55e" if integration['status'] == "Production Ready" else "#f59e0b"

        with st.expander(f"**{integration['name']}** — {integration['status']}", expanded=True):
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown(f"**Description:** {integration['description']}")

                st.markdown("**Key Capabilities:**")
                for cap in integration['capabilities']:
                    st.markdown(f"✓ {cap}")

            with col2:
                st.markdown("**Supported Protocols:**")
                for protocol in integration['protocols']:
                    st.code(protocol, language=None)

                st.markdown(f"""
                <div style="background: {status_color}22; border: 1px solid {status_color}; padding: 8px 16px; border-radius: 8px; text-align: center;">
                    <span style="color: {status_color}; font-weight: bold;">{integration['status']}</span>
                </div>
                """, unsafe_allow_html=True)

    st.divider()

    # Live Integration Demo
    st.subheader("Live Integration Demo")
    st.markdown("Test connectivity to your systems in real-time.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**MAM System Connection Test**")
        mam_endpoint = st.text_input("MAM API Endpoint", placeholder="https://your-mam-system.com/api/v1", key="mam_endpoint")
        mam_auth = st.selectbox("Authentication", ["API Key", "OAuth 2.0", "Basic Auth", "SAML"], key="mam_auth")

        if st.button("Test MAM Connection", use_container_width=True):
            with st.spinner("Testing connection..."):
                time.sleep(1.5)
            st.success("✅ Connection successful! MAM system is accessible.")
            st.json({
                "status": "connected",
                "latency_ms": 45,
                "api_version": "v2.1",
                "capabilities": ["ingest", "search", "metadata", "export"]
            })

    with col2:
        st.markdown("**Broadcast Automation Test**")
        auto_endpoint = st.text_input("Automation Endpoint", placeholder="https://your-automation.com/mos", key="auto_endpoint")
        auto_protocol = st.selectbox("Protocol", ["MOS Protocol", "VDCP", "REST API", "NMOS"], key="auto_protocol")

        if st.button("Test Automation Connection", use_container_width=True):
            with st.spinner("Testing connection..."):
                time.sleep(1.2)
            st.success("✅ Connection successful! Automation system responding.")
            st.json({
                "status": "connected",
                "latency_ms": 32,
                "protocol_version": "MOS 2.8.5",
                "capabilities": ["playlist", "secondary_events", "graphics"]
            })

    st.divider()

    # Architecture Diagram
    st.subheader("Integration Architecture")

    st.markdown("""
    ```
    ┌─────────────────────────────────────────────────────────────────────────────────┐
    │                              MediaAgentIQ Platform                               │
    │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐       │
    │  │ Caption │ │  Clip   │ │ Archive │ │Compliance│ │ Social  │ │Trending │       │
    │  │  Agent  │ │  Agent  │ │  Agent  │ │  Agent  │ │  Agent  │ │  Agent  │       │
    │  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘       │
    │       │           │           │           │           │           │             │
    │  ┌────┴───────────┴───────────┴───────────┴───────────┴───────────┴────┐       │
    │  │                        Integration Layer                             │       │
    │  │   REST API │ WebSocket │ MOS Protocol │ NMOS │ gRPC │ Webhooks      │       │
    │  └────┬───────────┬───────────┬───────────┬───────────┬───────────┬────┘       │
    └───────┼───────────┼───────────┼───────────┼───────────┼───────────┼────────────┘
            │           │           │           │           │           │
    ┌───────┴───┐ ┌─────┴─────┐ ┌───┴───┐ ┌─────┴─────┐ ┌───┴───┐ ┌─────┴─────┐
    │    MAM    │ │ Broadcast │ │  NMOS │ │   Cloud   │ │Social │ │Transcription│
    │  Systems  │ │Automation │ │Network│ │ Platforms │ │  APIs │ │  Services  │
    └───────────┘ └───────────┘ └───────┘ └───────────┘ └───────┘ └────────────┘
    ```
    """)

    st.divider()

    # API Documentation Preview
    st.subheader("API Quick Reference")

    tab1, tab2, tab3 = st.tabs(["REST API", "WebSocket", "Webhooks"])

    with tab1:
        st.markdown("**REST API Endpoints**")
        api_endpoints = [
            {"method": "POST", "endpoint": "/api/v1/caption/generate", "description": "Generate captions for media file"},
            {"method": "POST", "endpoint": "/api/v1/clip/analyze", "description": "Analyze video for viral moments"},
            {"method": "GET", "endpoint": "/api/v1/archive/search", "description": "Search archive with natural language"},
            {"method": "POST", "endpoint": "/api/v1/compliance/scan", "description": "Run compliance scan on content"},
            {"method": "POST", "endpoint": "/api/v1/social/generate", "description": "Generate social media posts"},
            {"method": "GET", "endpoint": "/api/v1/trending/topics", "description": "Get current trending topics"},
        ]

        for api in api_endpoints:
            method_color = "#22c55e" if api['method'] == "GET" else "#3b82f6"
            st.markdown(f"""
            <div style="display: flex; align-items: center; padding: 8px; background: #1e293b; border-radius: 6px; margin: 4px 0;">
                <span style="background: {method_color}; padding: 2px 8px; border-radius: 4px; font-family: monospace; margin-right: 12px;">{api['method']}</span>
                <code style="flex: 1;">{api['endpoint']}</code>
                <span style="color: #94a3b8; font-size: 0.85rem;">{api['description']}</span>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown("**WebSocket Events**")
        st.code("""
// Connect to real-time updates
const ws = new WebSocket('wss://api.mediaagentiq.com/ws');

// Subscribe to events
ws.send(JSON.stringify({
    action: 'subscribe',
    channels: ['trending', 'compliance_alerts', 'processing_status']
}));

// Receive real-time updates
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Event:', data.type, data.payload);
};
        """, language="javascript")

    with tab3:
        st.markdown("**Webhook Configuration**")
        st.code("""
{
    "webhook_url": "https://your-system.com/webhooks/mediaagentiq",
    "events": [
        "caption.completed",
        "clip.detected",
        "compliance.violation",
        "trending.alert"
    ],
    "secret": "your-webhook-secret",
    "retry_policy": {
        "max_retries": 3,
        "backoff_ms": 1000
    }
}
        """, language="json")

    st.divider()

    # Contact for Integration
    st.subheader("Ready to Integrate?")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        **Technical Documentation**

        Access our comprehensive API documentation, SDKs, and integration guides.
        """)
        st.button("📚 View Documentation", use_container_width=True)

    with col2:
        st.markdown("""
        **Integration Support**

        Our integration team can help you connect MediaAgentIQ to your systems.
        """)
        st.button("🤝 Contact Integration Team", use_container_width=True)

    with col3:
        st.markdown("""
        **Custom Development**

        Need a custom integration? We can build it for your specific requirements.
        """)
        st.button("🛠️ Request Custom Integration", use_container_width=True)


# ============== Footer ==============

st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("MediaAgentIQ v2.0.0 | Enterprise Edition")
with col2:
    st.caption("AI-Powered Media Operations Platform")
with col3:
    st.caption(f"© {datetime.now().year} | Built for Broadcasters")
