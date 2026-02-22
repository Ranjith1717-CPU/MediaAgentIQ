"""
MediaAgentIQ - Enhanced Streamlit App
AI Agent Platform for Media & Broadcast Operations
Real-time demos showcasing full agent capabilities
"""
import streamlit as st
import random
import time
import os
from datetime import datetime, timedelta
from pathlib import Path

# Import demo sample configuration
try:
    from demo_config import (
        DEMO_SAMPLE_VIDEO,
        SAMPLE_CAPTIONS, SAMPLE_QA_ISSUES, SAMPLE_VIRAL_MOMENTS,
        SAMPLE_COMPLIANCE_ISSUES, SAMPLE_SOCIAL_POSTS, SAMPLE_TRANSLATIONS,
        SAMPLE_LICENSES, SAMPLE_VIOLATIONS, SAMPLE_TRENDS, SAMPLE_ARCHIVE_METADATA,
        SAMPLE_BREAKING_NEWS,
        SAMPLE_DEEPFAKE_RESULT, SAMPLE_FACT_CHECK_CLAIMS,
        SAMPLE_AUDIENCE_DATA, SAMPLE_PRODUCTION_DATA,
        SAMPLE_BRAND_SAFETY_DATA, SAMPLE_CARBON_DATA,
        get_demo_video_path, is_demo_video_available
    )
    DEMO_SAMPLE_AVAILABLE = is_demo_video_available()
except ImportError:
    DEMO_SAMPLE_AVAILABLE = False

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
    {"id": 0, "title": "Entertainment Showcase - Dynamic Performance (DEMO)", "duration": "0:15", "date": "2025-02-22", "speaker": "Performance Artist", "tags": "entertainment, music, performance, viral, trending, high-energy", "description": "High-energy 15-second entertainment clip — viral potential score 92%. Indexed from demo_sample_video.mp4", "format": "HD 1080p", "size": "1.5 GB"},
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

def parse_engagement(value):
    """Parse engagement values like '250K', '1.5M', '85K' to integers"""
    try:
        if isinstance(value, (int, float)):
            return int(value)
        value = str(value).strip().upper()
        if 'M' in value:
            return int(float(value.replace('M', '').replace(',', '')) * 1000000)
        elif 'K' in value:
            return int(float(value.replace('K', '').replace(',', '')) * 1000)
        else:
            return int(float(value.replace(',', '')))
    except:
        return 0

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


def show_demo_video_player(label="🎬 Demo Video — Entertainment Showcase (15s)", auto_expand=True):
    """Show the demo video player inline on any agent page."""
    if not DEMO_SAMPLE_AVAILABLE:
        return
    video_path = get_demo_video_path()
    if not video_path.exists():
        return
    with st.expander(label, expanded=auto_expand):
        col1, col2 = st.columns([2, 1])
        with col1:
            st.video(str(video_path))
        with col2:
            st.markdown(f"**{DEMO_SAMPLE_VIDEO['title']}**")
            st.caption(f"⏱ Duration: {DEMO_SAMPLE_VIDEO['duration']}")
            st.caption(f"📐 Resolution: {DEMO_SAMPLE_VIDEO['resolution']}")
            st.caption(f"🎞 Format: {DEMO_SAMPLE_VIDEO['format']}")
            st.caption(f"📦 Size: {DEMO_SAMPLE_VIDEO['size_mb']} MB")
            st.caption(f"🎭 Type: {DEMO_SAMPLE_VIDEO['content_type']}")
            st.success("✅ Agent analyzing this video")


# ============== Sidebar ==============

with st.sidebar:
    st.markdown('<p class="main-header">MediaAgentIQ</p>', unsafe_allow_html=True)
    st.caption("AI Agent Platform for Media & Broadcast")

    st.divider()

    page = st.radio(
        "Select Agent",
        [
            # Core
            "Dashboard", "🚀 All-in-One Workflow",
            # Original 8 agents
            "Caption Agent", "Clip Agent", "Archive Agent", "Compliance Agent",
            "Social Publishing", "Localization", "Rights Agent", "Trending Agent",
            # ── Future-Ready Agents ──
            "🔍 Deepfake Detection", "✅ Live Fact-Check",
            "📊 Audience Intelligence", "🎬 AI Production Director",
            "🛡️ Brand Safety", "🌿 Carbon Intelligence",
            # System
            "Integration Showcase",
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("**System Status**")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<span class="realtime-indicator"></span> Live', unsafe_allow_html=True)
    with col2:
        st.caption(f"{datetime.now().strftime('%H:%M:%S')}")

    st.success("All 14 Agents Online")
    st.info("🔮 6 Future-Ready Agents Active")

    # Mode selector
    st.markdown("**Processing Mode**")
    mode = st.radio("Mode", ["Demo Mode", "Production Mode"], label_visibility="collapsed", horizontal=True)
    if mode == "Production Mode":
        st.warning("Requires API keys in .env")

    st.divider()
    st.caption("v3.0.0 | Future-Ready Edition")


# ============== Main Pages ==============

if page == "Dashboard":
    st.title("MediaAgentIQ Dashboard")
    st.markdown("**AI-Powered Media Operations Platform** | Real-time Broadcast Intelligence")

    # Demo Sample Video Section (if available)
    if DEMO_SAMPLE_AVAILABLE:
        with st.expander("🎬 **Demo Sample Video Available** - Click to preview and process", expanded=False):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"**{DEMO_SAMPLE_VIDEO['title']}**")
                st.caption(f"Duration: {DEMO_SAMPLE_VIDEO['duration']} | Format: {DEMO_SAMPLE_VIDEO['format']} | Size: {DEMO_SAMPLE_VIDEO['size_mb']} MB")
                video_path = get_demo_video_path()
                if video_path.exists():
                    st.video(str(video_path))
            with col2:
                st.markdown("**Quick Process Options:**")
                if st.button("🚀 Process with All Agents", key="demo_process_all"):
                    st.session_state.demo_processing = True
                    st.session_state.demo_process_start = datetime.now()
                if st.button("📝 Generate Captions Only", key="demo_caption_only"):
                    st.session_state.demo_caption_processing = True
                if st.button("🎬 Find Viral Clips", key="demo_clip_only"):
                    st.session_state.demo_clip_processing = True

                if st.session_state.get("demo_processing"):
                    with st.spinner("Processing demo video through all agents..."):
                        time.sleep(2)
                    st.success("✅ Demo video processed! Check 'All-in-One Workflow' for results.")
                    st.session_state.demo_processing = False

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
            # Use sample video activity if demo is available
            if DEMO_SAMPLE_AVAILABLE:
                auto_activity = [
                    {"time": "Just now", "event": f"📈 Trending Agent matched content to #Innovation", "action": "Recommended optimal posting time"},
                    {"time": "1 min ago", "event": f"🎬 Clip Agent processed '{DEMO_SAMPLE_VIDEO['title'][:30]}...'", "action": "Found 2 viral moments (94% score)"},
                    {"time": "2 min ago", "event": "📝 Caption Agent completed transcription", "action": f"Generated {len(SAMPLE_CAPTIONS)} segments, triggered Localization"},
                    {"time": "3 min ago", "event": "⚖️ Compliance scan on demo video", "action": "Identified as advertisement - disclosure recommended"},
                    {"time": "5 min ago", "event": "📱 Social Publishing generated posts", "action": f"5 platforms ready: {', '.join([p['platform'] for p in SAMPLE_SOCIAL_POSTS['product_launch'][:3]])}..."},
                    {"time": "8 min ago", "event": "🌍 Localization completed", "action": f"8 languages translated, voice dub available"},
                    {"time": "10 min ago", "event": "📜 Rights Agent verified licenses", "action": "All content cleared for use"},
                ]
            else:
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

    # ── Future-Ready Agents ──────────────────────────────────────────────────
    st.subheader("🔮 Future-Ready Agents — Market Gap Innovation")
    st.caption("Capabilities that don't yet exist in the broadcast market")

    future_agents = [
        {
            "icon": "🔍",
            "name": "Deepfake Detection",
            "tagline": "Synthetic Media Forensics",
            "capabilities": ["Voice clone detection", "Face swap analysis", "Metadata provenance", "Chain of custody", "Real-time scoring"],
            "benefit": "News integrity protection",
            "market_gap": "No integrated broadcast solution exists"
        },
        {
            "icon": "✅",
            "name": "Live Fact-Check",
            "tagline": "Real-time Claim Verification",
            "capabilities": ["Auto claim extraction", "8+ fact databases", "Live anchor alerts", "Graphic suggestions", "Historical tracking"],
            "benefit": "On-air accuracy assurance",
            "market_gap": "All tools require manual journalist input"
        },
        {
            "icon": "📊",
            "name": "Audience Intelligence",
            "tagline": "Viewer Retention AI",
            "capabilities": ["Drop-off prediction", "Intervention generator", "Demographic analysis", "Competitive migration", "Live pacing advice"],
            "benefit": "Prevent viewer loss before it happens",
            "market_gap": "No real-time live broadcast solution"
        },
        {
            "icon": "🎬",
            "name": "AI Production Director",
            "tagline": "Autonomous Live Direction",
            "capabilities": ["Camera cut AI", "Lower-third generation", "Rundown optimization", "Break timing", "Audio mix advice"],
            "benefit": "Human director co-pilot",
            "market_gap": "No autonomous broadcast director exists"
        },
        {
            "icon": "🛡️",
            "name": "Brand Safety",
            "tagline": "Contextual Ad Intelligence",
            "capabilities": ["GARM risk scoring", "IAB classification", "Advertiser impact", "CPM optimization", "Revenue protection"],
            "benefit": "+15-28% ad revenue uplift",
            "market_gap": "Digital only - no live TV solution"
        },
        {
            "icon": "🌿",
            "name": "Carbon Intelligence",
            "tagline": "ESG Broadcast Tracking",
            "capabilities": ["Energy monitoring", "Scope 1/2/3 carbon", "Green scheduling", "Offset management", "ESG reporting"],
            "benefit": "ESG compliance & advertiser trust",
            "market_gap": "No broadcast ESG tracking tool"
        },
    ]

    future_cols = st.columns(3)
    for i, agent in enumerate(future_agents):
        with future_cols[i % 3]:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1e1b4b, #0f172a); padding: 16px; border-radius: 12px;
                        border: 1px solid #7c3aed; margin-bottom: 12px;">
                <h3 style="margin: 0; color: #c4b5fd;">{agent['icon']} {agent['name']}</h3>
                <p style="color: #a78bfa; margin: 4px 0; font-size: 0.9rem;">{agent['tagline']}</p>
                <ul style="color: #94a3b8; font-size: 0.8rem; margin: 8px 0; padding-left: 16px;">
                    {''.join([f'<li>{cap}</li>' for cap in agent['capabilities'][:3]])}
                </ul>
                <p style="color: #22c55e; font-size: 0.85rem; margin: 4px 0 0 0;">✓ {agent['benefit']}</p>
                <p style="color: #f59e0b; font-size: 0.75rem; margin: 4px 0 0 0;">⚡ Gap: {agent['market_gap']}</p>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Live Activity Feed
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Live Activity Feed")
        activity = [
            {"agent": "📝 Caption Agent", "action": "Completed morning news broadcast transcription", "time": "Just now", "status": "success"},
            {"agent": "🔍 Deepfake Detect", "action": "⚠️ SUSPICIOUS content flagged — UGC clip risk score 0.68 — HOLD for review", "time": "1 min ago", "status": "warning"},
            {"agent": "⚖️ Compliance", "action": "ALERT: Potential FCC violation detected - Review needed", "time": "2 min ago", "status": "warning"},
            {"agent": "✅ Fact-Check", "action": "FALSE claim detected at 14:32 — anchor alert sent to producer", "time": "3 min ago", "status": "warning"},
            {"agent": "🎬 Clip Agent", "action": "Found 3 viral moments in warehouse fire coverage", "time": "5 min ago", "status": "success"},
            {"agent": "📊 Audience Intel", "action": "DROP-OFF RISK at 22:00 — intervention: tease exclusive story", "time": "6 min ago", "status": "warning"},
            {"agent": "🎬 AI Director", "action": "Camera 3 cut suggested → accepted | Lower-third auto-generated", "time": "7 min ago", "status": "success"},
            {"agent": "📈 Trending", "action": "#NashvilleFire trending - 45K posts/hour", "time": "8 min ago", "status": "info"},
            {"agent": "🛡️ Brand Safety", "action": "BLOCKED: Pharma ads during crime segment (score: 52/100)", "time": "10 min ago", "status": "warning"},
            {"agent": "📜 Rights", "action": "WARNING: Wire Service license expires in 18 days", "time": "15 min ago", "status": "warning"},
            {"agent": "🌿 Carbon Intel", "action": "Daily CO₂e: 428 kg | Renewable: 34% | Optimization: -15% available", "time": "20 min ago", "status": "info"},
            {"agent": "🌍 Localization", "action": "Spanish dub completed for breaking news segment", "time": "22 min ago", "status": "success"},
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

        # Demo content selection
        demo_options = ["None - Use uploaded file"]
        if DEMO_SAMPLE_AVAILABLE:
            demo_options.insert(0, f"🎬 Sample Video: {DEMO_SAMPLE_VIDEO['title']} ({DEMO_SAMPLE_VIDEO['duration']})")
        demo_options.append("📺 News Broadcast Demo (4 hrs)")

        demo_selection = st.radio("**Or use demo content:**", demo_options, index=0 if DEMO_SAMPLE_AVAILABLE else len(demo_options)-1)
        use_sample_video = DEMO_SAMPLE_AVAILABLE and "Sample Video" in demo_selection
        use_news_demo = "News Broadcast" in demo_selection

        # Show video preview if sample video selected
        if use_sample_video:
            st.markdown("---")
            st.markdown("**📹 Demo Video Preview:**")
            video_path = get_demo_video_path()
            if video_path.exists():
                st.video(str(video_path))
                st.caption(f"📁 {DEMO_SAMPLE_VIDEO['filename']} | {DEMO_SAMPLE_VIDEO['resolution']} | {DEMO_SAMPLE_VIDEO['size_mb']} MB")

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

        # Select data source based on demo selection
        if use_sample_video:
            active_captions = SAMPLE_CAPTIONS
            active_viral = SAMPLE_VIRAL_MOMENTS
            active_compliance = SAMPLE_COMPLIANCE_ISSUES
            active_trends = SAMPLE_TRENDS
            active_archive = SAMPLE_ARCHIVE_METADATA
            active_social = SAMPLE_SOCIAL_POSTS.get("product_launch", [])
            active_translations = SAMPLE_TRANSLATIONS
            active_licenses = SAMPLE_LICENSES
            content_title = DEMO_SAMPLE_VIDEO['title']
            content_duration = DEMO_SAMPLE_VIDEO['duration']
        else:
            active_captions = DEMO_CAPTIONS
            active_viral = DEMO_VIRAL_MOMENTS
            active_compliance = DEMO_COMPLIANCE_ISSUES
            active_trends = DEMO_TRENDS
            active_archive = {
                "title": "Morning News Broadcast - Fire Coverage",
                "duration": "4:02:15",
                "speakers": ["Sarah Mitchell", "Jake Thompson", "Weather Team"],
                "topics": ["warehouse fire", "downtown Nashville", "breaking news"],
                "ai_tags": ["fire", "emergency", "reporter", "live coverage", "breaking"],
                "sentiment": "urgent/concerned",
                "quality": "HD 1080p"
            }
            active_social = DEMO_SOCIAL_POSTS.get("breaking_news", [])
            active_translations = DEMO_TRANSLATIONS
            active_licenses = DEMO_LICENSES
            content_title = "Morning News Broadcast"
            content_duration = "4:02:15"

        # Summary Metrics - Dynamic based on content
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        col1.metric("Captions", f"{len(active_captions)} segments", f"{sum(c['confidence'] for c in active_captions)/len(active_captions)*100:.1f}% accuracy")
        col2.metric("Viral Clips", f"{len(active_viral)} found", f"Top: {max(m['score'] for m in active_viral)*100:.0f}%")
        col3.metric("Compliance", f"{len(active_compliance)} items", "Reviewed")
        col4.metric("Social Posts", f"{len(active_social)} ready", "5 platforms")
        col5.metric("Translations", f"{len(target_languages)} languages", "95% quality")
        col6.metric("Trending Match", f"{len(active_trends)} topics", f"{active_trends[0]['topic']}" if active_trends else "N/A")

        st.divider()

        # Tabbed Results
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "📝 Captions", "🎬 Viral Clips", "⚖️ Compliance", "🔍 Archive",
            "📱 Social", "🌍 Translations", "📜 Rights", "📈 Trending"
        ])

        with tab1:
            st.markdown(f"**Generated Captions** - {len(active_captions)} segments from '{content_title}'")
            for cap in active_captions:
                conf_color = "#22c55e" if cap["confidence"] >= 0.95 else "#f59e0b" if cap["confidence"] >= 0.90 else "#ef4444"
                st.markdown(f"""
                <div style="background: #1e293b; padding: 8px 12px; border-radius: 6px; margin: 4px 0; border-left: 3px solid #6366f1;">
                    <small style="color: #6366f1;">{format_srt_time(cap['start'])} → {format_srt_time(cap['end'])}</small>
                    <span style="color: #94a3b8; margin-left: 12px;">{cap['speaker']}</span>
                    <span style="color: {conf_color}; float: right;">{cap['confidence']*100:.0f}%</span><br/>
                    <span style="color: #e2e8f0;">{cap['text']}</span>
                </div>
                """, unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            col1.download_button("📥 Download SRT", generate_srt(active_captions), "captions.srt", use_container_width=True)
            col2.download_button("📥 Download VTT", generate_srt(active_captions).replace(",", "."), "captions.vtt", use_container_width=True)

        with tab2:
            st.markdown(f"**Viral Moments Detected** - {len(active_viral)} clips ready for export")
            for moment in active_viral:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{moment['title']}** ({moment['end']-moment['start']:.0f}s)")
                    st.caption(moment['description'])
                    st.markdown(f"**Platforms:** {', '.join(moment['platforms'])}")
                    st.markdown(f"**Hashtags:** {' '.join(moment['hashtags'])}")
                with col2:
                    st.metric("Viral Score", f"{moment['score']:.0%}")
                    st.caption(f"📈 {moment['predicted_views']}")
                st.divider()
            st.button("📤 Export All Clips", use_container_width=True, key="export_clips_allinone")

        with tab3:
            st.markdown(f"**Compliance Scan Results** - {len(active_compliance)} items reviewed")
            for issue in active_compliance:
                severity_icon = "🔴" if issue["severity"] == "critical" else "🟠" if issue["severity"] in ["high", "medium"] else "🟢" if issue["severity"] == "info" else "ℹ️"
                if issue["severity"] in ["critical", "high"]:
                    st.error(f"{severity_icon} **{issue['type'].upper()}** @ {issue['timestamp']}\n\n{issue['description']}\n\n**FCC Rule:** {issue['fcc_rule']}\n\n**Recommendation:** {issue['recommendation']}")
                elif issue["severity"] == "medium":
                    st.warning(f"{severity_icon} **{issue['type'].upper()}** @ {issue['timestamp']}\n\n{issue['description']}\n\n**Recommendation:** {issue['recommendation']}")
                else:
                    st.info(f"{severity_icon} **{issue['type'].upper()}** @ {issue['timestamp']}\n\n{issue['description']}\n\n**Recommendation:** {issue['recommendation']}")
            st.button("📝 Generate Compliance Report", use_container_width=True, key="compliance_report_allinone")

        with tab4:
            st.markdown("**Archive Metadata Generated**")
            st.json(active_archive)
            st.button("📤 Send to MAM System", use_container_width=True, key="mam_sync_allinone")

        with tab5:
            st.markdown(f"**Social Posts Generated** - {len(active_social)} posts across 5 platforms")
            for post in active_social:
                with st.expander(f"**{post['platform']}** - {post['char_count']} chars | Best time: {post['best_time']}"):
                    st.text_area("Post Content", post['content'], height=120, key=f"social_{post['platform']}")
                    st.caption(f"📊 Predicted engagement: {post['predicted_engagement']}")
            col1, col2 = st.columns(2)
            col1.button("📤 Post All Now", type="primary", use_container_width=True, key="post_all_allinone")
            col2.button("🕐 Schedule All", use_container_width=True, key="schedule_all_allinone")

        with tab6:
            st.markdown(f"**Translations Complete** - {len(target_languages)} languages")
            for lang in target_languages:
                lang_key = {"Spanish": "es", "French": "fr", "German": "de", "Chinese": "zh"}.get(lang, "es")
                if lang_key in active_translations:
                    trans = active_translations[lang_key]
                    with st.expander(f"{trans['flag']} **{trans['name']}** - {trans['quality_score']}% quality"):
                        st.markdown(f"**Original:** {trans['sample_original']}")
                        st.markdown(f"**Translated:** {trans['sample_translated']}")
                        st.caption(f"📝 {trans['notes']}")
                        if trans['voice_available']:
                            st.success("🎙️ AI Voice Dubbing Available")
            st.button("📥 Download All Subtitle Files", use_container_width=True, key="download_subs_allinone")

        with tab7:
            st.markdown("**Rights Verification**")
            if use_sample_video:
                for lic in active_licenses:
                    status_color = "🟢" if lic['status'] == 'active' else "🟡"
                    st.success(f"{status_color} **{lic['title']}**\n\nType: {lic['type']} | Licensor: {lic['licensor']}\n\nRights: {', '.join(lic['rights'])}\n\nCompliance: {lic['compliance_score']}%")
            else:
                st.success("✅ Content cleared for broadcast use")
                st.info("ℹ️ 2 licenses used: Wire Service Feed, Stock Images")
                st.warning("⚠️ Reminder: Wire Service license expires in 18 days")

        with tab8:
            st.markdown("**Trending Context**")
            st.markdown("Your content matches these trending topics:")
            for trend in active_trends:
                velocity_color = "#22c55e" if trend['velocity_score'] > 80 else "#f59e0b" if trend['velocity_score'] > 60 else "#94a3b8"
                with st.expander(f"**{trend['topic']}** - {trend['velocity']} ({trend['volume']})"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Velocity Score", f"{trend['velocity_score']}/100")
                        st.metric("Sentiment", trend['sentiment'], f"{trend['sentiment_score']:.2f}")
                    with col2:
                        st.markdown("**Demographics:**")
                        for age, pct in trend['demographics'].items():
                            st.progress(pct/100, f"{age}: {pct}%")
                    st.info(f"💡 **Recommendation:** {trend['recommendation']}")
            st.success("💡 **AI Analysis:** Content aligns well with current trends. Optimal for immediate publication.")

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
    show_demo_video_player()

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
        uploaded = st.file_uploader("Upload video or audio file", type=["mp4", "mov", "wav", "mp3", "m4a"], key="caption_upload")

        # Demo selection with sample video option
        caption_demo_options = ["Upload your own file"]
        if DEMO_SAMPLE_AVAILABLE:
            caption_demo_options.insert(0, f"🎬 Sample Video: {DEMO_SAMPLE_VIDEO['title']} ({DEMO_SAMPLE_VIDEO['duration']})")
        caption_demo_options.append("📺 News Broadcast Demo (1:22)")

        caption_demo_selection = st.radio("**Or use demo content:**", caption_demo_options, index=0 if DEMO_SAMPLE_AVAILABLE else len(caption_demo_options)-1, key="caption_demo_select")
        use_sample_video_caption = DEMO_SAMPLE_AVAILABLE and "Sample Video" in caption_demo_selection
        demo_mode = "News Broadcast" in caption_demo_selection

        # Show video preview if sample video selected
        if use_sample_video_caption:
            video_path = get_demo_video_path()
            if video_path.exists():
                st.video(str(video_path))
                st.caption(f"📁 {DEMO_SAMPLE_VIDEO['filename']} | {DEMO_SAMPLE_VIDEO['resolution']}")

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

        # Select data based on demo type
        if use_sample_video_caption:
            caption_data = SAMPLE_CAPTIONS
            qa_data = SAMPLE_QA_ISSUES
            content_title = DEMO_SAMPLE_VIDEO['title']
            content_duration = DEMO_SAMPLE_VIDEO['duration']
            speakers = ["Narrator"]
            speaker_data = {"Narrator": 30}
        else:
            caption_data = DEMO_CAPTIONS
            qa_data = DEMO_QA_ISSUES
            content_title = "Morning News Broadcast"
            content_duration = "1:22"
            speakers = ["Sarah Mitchell (Anchor)", "Jake Thompson (Reporter)"]
            speaker_data = {"Sarah Mitchell (Anchor)": 45, "Jake Thompson (Reporter)": 37}

        # Results Summary
        st.subheader(f"Results - {content_title}")
        avg_confidence = sum(c['confidence'] for c in caption_data) / len(caption_data) * 100
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Segments", len(caption_data))
        col2.metric("Duration", content_duration)
        col3.metric("Speakers", len(speakers))
        col4.metric("Avg Confidence", f"{avg_confidence:.1f}%")
        col5.metric("Words/Min", "152")

        tab1, tab2, tab3, tab4 = st.tabs(["📄 Captions", "✅ QA Report", "📊 Analytics", "⬇️ Export"])

        with tab1:
            # Interactive caption editor
            st.markdown("**Interactive Caption Editor** - Click any segment to edit")
            for cap in caption_data:
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
            issues_count = {"Critical": 0, "Warning": 0, "Info": 0, "Passed": 0}
            for issue in qa_data:
                if issue["severity"] == "critical":
                    issues_count["Critical"] += 1
                elif issue["severity"] in ["medium", "warning"]:
                    issues_count["Warning"] += 1
                elif issue["severity"] == "low" or issue["type"] == "info":
                    issues_count["Info"] += 1
                elif issue["type"] == "success":
                    issues_count["Passed"] += 1

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Critical", issues_count["Critical"], delta_color="inverse")
            col2.metric("Warnings", issues_count["Warning"])
            col3.metric("Info", issues_count["Info"])
            col4.metric("Passed", issues_count["Passed"])

            st.divider()
            for issue in qa_data:
                if issue["type"] == "warning":
                    st.warning(f"⚠️ **{issue['issue']}** (Segment {issue.get('segment', 'N/A')} @ {issue.get('timestamp', 'N/A')})\n\n{issue['details']}\n\n💡 *{issue.get('suggestion', '')}*")
                elif issue["type"] == "info":
                    st.info(f"ℹ️ **{issue['issue']}** (Segment {issue.get('segment', 'N/A')} @ {issue.get('timestamp', 'N/A')})\n\n{issue['details']}")
                elif issue["type"] == "success":
                    st.success(f"✅ **{issue['issue']}**\n\n{issue['details']}")

        with tab3:
            st.markdown("**Transcription Analytics**")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Speaker Distribution**")
                total_time = sum(speaker_data.values())
                for speaker, seconds in speaker_data.items():
                    st.progress(seconds / total_time if total_time > 0 else 0, f"{speaker}: {seconds}s")

            with col2:
                st.markdown("**Confidence Distribution**")
                high_conf = len([c for c in caption_data if c['confidence'] >= 0.95]) / len(caption_data)
                med_conf = len([c for c in caption_data if 0.90 <= c['confidence'] < 0.95]) / len(caption_data)
                low_conf = len([c for c in caption_data if c['confidence'] < 0.90]) / len(caption_data)
                st.progress(high_conf, f"High (>95%): {high_conf*100:.0f}%")
                st.progress(med_conf, f"Medium (90-95%): {med_conf*100:.0f}%")
                st.progress(low_conf, f"Low (<90%): {low_conf*100:.0f}%")

            st.markdown("**Words per Speaker**")
            cols = st.columns(len(speakers))
            for i, speaker in enumerate(speakers):
                word_count = sum(len(c['text'].split()) for c in caption_data if c['speaker'] == speaker)
                cols[i].metric(speaker.split(" (")[0], f"{word_count} words")

        with tab4:
            st.markdown("**Export Options**")
            srt_content = generate_srt(caption_data)
            filename_base = "sample_video" if use_sample_video_caption else "morning_news"

            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button("📥 Download SRT", srt_content, f"{filename_base}_captions.srt", "text/plain", use_container_width=True, key="cap_srt")
            with col2:
                st.download_button("📥 Download VTT", srt_content.replace(",", "."), f"{filename_base}_captions.vtt", "text/plain", use_container_width=True, key="cap_vtt")
            with col3:
                import json
                json_content = json.dumps(caption_data, indent=2)
                st.download_button("📥 Download JSON", json_content, f"{filename_base}_captions.json", "application/json", use_container_width=True, key="cap_json")

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
    show_demo_video_player()

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

    col1, col2 = st.columns([2, 1])
    with col1:
        uploaded = st.file_uploader("Upload broadcast recording", type=["mp4", "mov", "avi"], key="clip_upload")

        # Demo selection with sample video option
        clip_demo_options = ["Upload your own file"]
        if DEMO_SAMPLE_AVAILABLE:
            clip_demo_options.insert(0, f"🎬 Sample Video: {DEMO_SAMPLE_VIDEO['title']} ({DEMO_SAMPLE_VIDEO['duration']})")
        clip_demo_options.append("📺 News Broadcast Demo (4 hrs)")

        clip_demo_selection = st.radio("**Or use demo content:**", clip_demo_options, index=0 if DEMO_SAMPLE_AVAILABLE else len(clip_demo_options)-1, key="clip_demo_select")
        use_sample_video_clip = DEMO_SAMPLE_AVAILABLE and "Sample Video" in clip_demo_selection
        demo_mode = "News Broadcast" in clip_demo_selection

        # Show video preview if sample video selected
        if use_sample_video_clip:
            video_path = get_demo_video_path()
            if video_path.exists():
                st.video(str(video_path))
                st.caption(f"📁 {DEMO_SAMPLE_VIDEO['filename']} | {DEMO_SAMPLE_VIDEO['resolution']}")

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

        # Select data based on demo type
        viral_data = SAMPLE_VIRAL_MOMENTS if use_sample_video_clip else DEMO_VIRAL_MOMENTS
        high_viral_count = len([m for m in viral_data if m['score'] >= 0.90])
        total_clip_time = sum(m['end'] - m['start'] for m in viral_data)

        # Summary metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Moments Found", len(viral_data))
        col2.metric("High Viral (>90%)", high_viral_count)
        col3.metric("Total Clip Time", f"{total_clip_time:.0f}s")
        col4.metric("Est. Total Reach", viral_data[0]['predicted_views'] if viral_data else "N/A")
        col5.metric("Platforms Optimized", len(platforms))

        st.subheader(f"Viral Moments Detected")

        for moment in viral_data:
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
    show_demo_video_player()

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

    # Demo Video Indexing Section
    if DEMO_SAMPLE_AVAILABLE:
        with st.expander("🎬 **Index Demo Video** - AI tagging and metadata extraction", expanded=False):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"**{DEMO_SAMPLE_VIDEO['title']}**")
                video_path = get_demo_video_path()
                if video_path.exists():
                    st.video(str(video_path))
            with col2:
                st.markdown("**AI-Generated Metadata:**")
                st.json(SAMPLE_ARCHIVE_METADATA)
                if st.button("📥 Index to Archive", key="index_demo_archive"):
                    with st.spinner("Indexing with AI..."):
                        time.sleep(1)
                    st.success("✅ Demo video indexed to archive!")
                    st.markdown(f"**Tags:** {', '.join(SAMPLE_ARCHIVE_METADATA['ai_tags'])}")

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
    show_demo_video_player()

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
        compliance_demo_options = ["Upload your own file"]
        if DEMO_SAMPLE_AVAILABLE:
            compliance_demo_options.insert(0, f"🎬 Sample Video: {DEMO_SAMPLE_VIDEO['title']} ({DEMO_SAMPLE_VIDEO['duration']})")
        compliance_demo_options.append("📺 News Broadcast Demo (4 hrs)")
        compliance_demo_sel = st.radio("**Or use demo content:**", compliance_demo_options, index=0 if DEMO_SAMPLE_AVAILABLE else len(compliance_demo_options)-1, key="compliance_demo_sel")
        use_sample_compliance = DEMO_SAMPLE_AVAILABLE and "Sample Video" in compliance_demo_sel
        demo_mode = "News Broadcast" in compliance_demo_sel

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

        # Select data based on demo type
        compliance_data = SAMPLE_COMPLIANCE_ISSUES if use_sample_compliance else DEMO_COMPLIANCE_ISSUES
        critical_count = sum(1 for i in compliance_data if i["severity"] == "critical")
        high_count = sum(1 for i in compliance_data if i["severity"] == "high")
        medium_count = sum(1 for i in compliance_data if i["severity"] == "medium")
        risk_score = 8 if use_sample_compliance else 42  # Entertainment video is much safer

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Risk Score", f"{risk_score}/100", "CLEAR" if risk_score < 20 else "ELEVATED", delta_color="inverse" if risk_score > 20 else "normal")
        col2.metric("Critical Issues", str(critical_count), "None" if critical_count == 0 else "Immediate action")
        col3.metric("High Issues", str(high_count), "None" if high_count == 0 else "Review needed")
        col4.metric("Medium Issues", str(medium_count), "Monitor" if medium_count > 0 else "None")
        col5.metric("Potential Fines", "$0" if use_sample_compliance else "$85K - $1.1M", "Compliant" if use_sample_compliance else "If not addressed")

        st.divider()

        # Visual risk indicator
        st.markdown("**Compliance Risk Level**")
        risk_color = "#ef4444" if risk_score > 60 else "#f59e0b" if risk_score > 30 else "#22c55e"
        st.progress(risk_score / 100, f"Risk: {risk_score}%")

        if use_sample_compliance:
            st.success("✅ **Entertainment content scan complete** — Demo video (Entertainment Showcase) passes compliance checks")

        st.divider()
        st.subheader("Issues Detected")

        for issue in compliance_data:
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
    show_demo_video_player()

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
        social_options = ["Breaking News - Fire Coverage", "Feel-Good Story - Dog Reunion"]
        if DEMO_SAMPLE_AVAILABLE:
            social_options.insert(0, f"🎬 Entertainment Showcase — {DEMO_SAMPLE_VIDEO['title']}")
        content_type = st.selectbox("Select content type", social_options, index=0)

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
        if "Entertainment" in content_type:
            st.session_state.social_type = "entertainment"
        elif "Breaking" in content_type:
            st.session_state.social_type = "breaking_news"
        else:
            st.session_state.social_type = "feel_good"

    if st.session_state.get("social_done"):
        if st.session_state.social_type == "entertainment":
            posts = SAMPLE_SOCIAL_POSTS.get("product_launch", [])
        else:
            posts = DEMO_SOCIAL_POSTS[st.session_state.social_type]
        filtered_posts = [p for p in posts if p['platform'] in target_platforms]

        st.divider()

        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Posts Generated", len(filtered_posts))
        col2.metric("Platforms", len(set(p['platform'] for p in filtered_posts)))
        col3.metric("Est. Total Reach", f"{sum([parse_engagement(p['predicted_engagement']) for p in filtered_posts]):,}")
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
    show_demo_video_player()

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
        if DEMO_SAMPLE_AVAILABLE:
            st.info(f"**Demo:** {DEMO_SAMPLE_VIDEO['title']} ({DEMO_SAMPLE_VIDEO['duration']}) - English (US)")
        else:
            st.info("**Demo:** Morning News Broadcast (1:22) - English (US)")

        local_translations = SAMPLE_TRANSLATIONS if DEMO_SAMPLE_AVAILABLE else DEMO_TRANSLATIONS
        languages = st.multiselect(
            "Select target languages",
            list(local_translations.keys()),
            default=["es", "fr", "de", "zh"],
            format_func=lambda x: f"{local_translations[x]['flag']} {local_translations[x]['name']}"
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
        _loc_trans = SAMPLE_TRANSLATIONS if DEMO_SAMPLE_AVAILABLE else DEMO_TRANSLATIONS
        col2.metric("Avg Quality", f"{sum([_loc_trans[l]['quality_score'] for l in st.session_state.local_langs if l in _loc_trans]) / max(1, len([l for l in st.session_state.local_langs if l in _loc_trans])):.0f}%")
        col3.metric("Files Generated", len(st.session_state.local_langs) * 2)
        col4.metric("Processing Time", "2.4s")

        st.subheader("Localization Results")

        for lang in st.session_state.local_langs:
            trans = _loc_trans.get(lang, {})
            if not trans:
                continue
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
    show_demo_video_player()

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

        # Use demo video data when available
        rights_licenses = SAMPLE_LICENSES if DEMO_SAMPLE_AVAILABLE else DEMO_LICENSES
        rights_violations = SAMPLE_VIOLATIONS if DEMO_SAMPLE_AVAILABLE else DEMO_VIOLATIONS
        expiring_count = sum(1 for l in rights_licenses if l["status"] == "expiring_soon")

        # Dashboard metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Active Licenses", len(rights_licenses))
        col2.metric("Expiring Soon", str(expiring_count), f"Within 30 days" if expiring_count > 0 else "All clear", delta_color="inverse" if expiring_count > 0 else "normal")
        col3.metric("Violations Found", len(rights_violations))
        col4.metric("Annual Spend", "$499" if DEMO_SAMPLE_AVAILABLE else "$2.66M")
        col5.metric("Compliance Score", "100%" if DEMO_SAMPLE_AVAILABLE else "97%")

        st.divider()

        # Tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(["⚠️ Alerts", "📄 Licenses", "🚨 Violations", "📊 Analytics"])

        with tab1:
            st.subheader("Urgent Alerts")

            # Expiring soon alerts
            expiring_list = [l for l in rights_licenses if l["status"] == "expiring_soon"]
            if expiring_list:
                for lic in expiring_list:
                    st.warning(f"""
                    **License Expiring: {lic['title']}**

                    Expires in **{lic['days_remaining']} days** ({lic['end_date']})

                    Licensor: {lic['licensor']} | Cost: {lic['cost']}

                    **Action Required:** Initiate renewal negotiations immediately
                    """)
            else:
                st.success("✅ No licenses expiring in the next 30 days")

            # Violation alerts
            active_violations = [v for v in rights_violations if v['status'] in ['Under Review', 'DMCA Filed']]
            if active_violations:
                for v in active_violations:
                    st.error(f"""
                    **Violation Detected: {v['content']}**

                    Platform: {v['platform']} | Views: {v['views']} | Status: {v['status']}

                    Estimated Damages: {v['estimated_damages']}
                    """)
            else:
                st.success("✅ No active violations detected")

        with tab2:
            st.subheader("License Portfolio")

            for lic in rights_licenses:
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

            if not rights_violations:
                st.success("✅ No violations detected for this content")
            else:
                for v in rights_violations:
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
                if DEMO_SAMPLE_AVAILABLE:
                    costs = {"Original Content": 0, "Music License": 499}
                else:
                    costs = {"Sports": 2400000, "News Feeds": 180000, "Stock Media": 45000, "Music": 35000}
                max_cost = max(costs.values()) if max(costs.values()) > 0 else 1
                for license_type, cost in costs.items():
                    st.progress(cost / max_cost if max_cost > 0 else 0, f"{license_type}: ${cost:,}")

            with col2:
                st.markdown("**Compliance by License**")
                for lic in rights_licenses:
                    st.progress(lic['compliance_score'] / 100, f"{lic['title'][:25]}...: {lic['compliance_score']}%")


elif page == "Trending Agent":
    st.title("Trending Agent")
    st.caption("Real-time Trend Monitoring | Breaking News Alerts | Story Suggestions")
    show_demo_video_player()

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
    trending_breaking = SAMPLE_BREAKING_NEWS if DEMO_SAMPLE_AVAILABLE else DEMO_BREAKING
    trending_topics = SAMPLE_TRENDS if DEMO_SAMPLE_AVAILABLE else DEMO_TRENDS
    st.subheader("Breaking News Alerts")
    for news in trending_breaking:
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

    for trend in trending_topics:
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


# ======================================================================
# FUTURE-READY AGENTS (Market Gaps - Not Yet Available in the Industry)
# ======================================================================

elif page == "🔍 Deepfake Detection":
    st.title("🔍 Deepfake & Synthetic Media Detection")
    st.caption("MARKET GAP: No broadcast-integrated deepfake detection exists | 900% deepfake growth in 2025 | Real-time forensic analysis")
    show_demo_video_player()

    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e1b4b, #0f172a); padding: 16px; border-radius: 12px; border: 1px solid #7c3aed; margin-bottom: 16px;">
    <h4 style="color: #a78bfa; margin: 0 0 8px 0;">⚡ Why This Doesn't Exist Yet</h4>
    <p style="color: #c4b5fd; margin: 0;">
    Deepfake detection capacity continues to <strong>lag far behind creation</strong>. Deepfakes grew 900% in 2025
    (500K → 8M online). Voice cloning crossed the "indistinguishable threshold". No end-to-end broadcast-integrated
    detection tool exists — this agent fills that critical gap.
    </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Deepfakes in 2025", "~8 Million", "+900% YoY")
    with col2:
        st.metric("Voice Clone Detection", "< 65% accuracy", "Industry average")
    with col3:
        st.metric("Real-time Detection", "First in market", "Integrated broadcast")

    st.divider()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Submit Content for Forensic Scan")
        default_input = DEMO_SAMPLE_VIDEO['filename'] if DEMO_SAMPLE_AVAILABLE else "breaking_news_interview_clip.mp4"
        content_input = st.text_area("Content path / URL / description",
                                      value=default_input,
                                      height=80)
        scan_type = st.multiselect("Detection layers",
                                   ["Audio Layer (Voice Clone)", "Video Layer (Face Swap)", "Metadata Layer (Provenance)"],
                                   default=["Audio Layer (Voice Clone)", "Video Layer (Face Swap)", "Metadata Layer (Provenance)"])
        sensitivity = st.select_slider("Detection sensitivity", ["Lenient", "Balanced", "Strict"], value="Balanced")

        if st.button("🔍 Run Forensic Scan", use_container_width=True, type="primary"):
            with st.spinner("Running multi-layer forensic analysis..."):
                import time as _time
                steps = [
                    ("🎵 Analyzing audio spectral fingerprint", 0.4),
                    ("🎭 Scanning facial consistency & temporal artifacts", 0.7),
                    ("🔗 Verifying metadata chain of custody", 0.85),
                    ("🔄 Cross-modal consistency check (A/V sync)", 0.95),
                    ("📊 Computing risk assessment", 1.0),
                ]
                prog = st.progress(0, text="Initializing scan...")
                for step_text, prog_val in steps:
                    _time.sleep(0.5)
                    prog.progress(prog_val, text=step_text)
                _time.sleep(0.3)
                prog.empty()
                st.session_state["deepfake_scanned"] = True

    with col2:
        st.subheader("Detection Layers")
        st.markdown("""
        | Layer | What's Checked | Indicator |
        |---|---|---|
        | 🎵 Audio | Spectral smoothness, prosody, breath sounds | GAN fingerprints |
        | 🎭 Video | Facial blending, eye blinks, temporal flicker | Face swap seams |
        | 📋 Metadata | File timestamps, GPS, C2PA chain | Provenance gaps |
        | 🔄 Cross-modal | A/V sync, noise floor matching | Source mismatch |
        """)

    if st.session_state.get("deepfake_scanned"):
        st.divider()

        # Use SAMPLE_ data when demo video available, random otherwise
        if DEMO_SAMPLE_AVAILABLE:
            df_result = SAMPLE_DEEPFAKE_RESULT
        else:
            _rs = round(random.uniform(0.15, 0.72), 3)
            df_result = {
                "risk_score": _rs,
                "verdict": "AUTHENTIC" if _rs < 0.25 else "SUSPICIOUS - REVIEW" if _rs < 0.60 else "LIKELY SYNTHETIC",
                "broadcast_safe": _rs < 0.25,
                "audio_authenticity": round(random.uniform(0.72, 0.96), 3),
                "video_authenticity": round(random.uniform(0.68, 0.94), 3),
                "metadata_trust": round(random.uniform(0.75, 0.99), 3),
                "audio_findings": [],
                "video_findings": {},
                "metadata_findings": {},
                "provenance": ["📱 Source reported: UGC Upload", "🔗 C2PA chain: Not present"],
                "recommendations": [("🚨 Urgent", "Submit to secondary verification before broadcast")]
            }

        risk_score = df_result["risk_score"]
        broadcast_safe = df_result["broadcast_safe"]
        verdict = df_result["verdict"]
        icon = "✅" if broadcast_safe else "⚠️" if risk_score < 0.60 else "🚫"

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Overall Risk Score", f"{risk_score:.3f}", "Safe ✅" if broadcast_safe else "Not Safe ⚠️")
        with col2:
            st.metric("Audio Authenticity", f"{df_result['audio_authenticity']:.3f}", "Spectral analysis")
        with col3:
            st.metric("Video Authenticity", f"{df_result['video_authenticity']:.3f}", "Frame analysis")
        with col4:
            st.metric("Metadata Trust", f"{df_result['metadata_trust']:.3f}", "Chain of custody")

        st.markdown(f"""
        <div style="background: {'rgba(34,197,94,0.1)' if broadcast_safe else 'rgba(239,68,68,0.1)'};
                    border-left: 4px solid {'#22c55e' if broadcast_safe else '#ef4444'};
                    padding: 16px; border-radius: 8px; margin: 16px 0;">
            <h3 style="margin: 0; color: {'#22c55e' if broadcast_safe else '#ef4444'};">{icon} Verdict: {verdict}</h3>
            <p style="margin: 8px 0 0 0; color: #e2e8f0;">
            {'✅ Content cleared for broadcast — Demo video authenticated as original production' if broadcast_safe else '🚫 HOLD: Route to verification team before broadcast'}
            </p>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("📋 Full Forensic Report", expanded=not broadcast_safe):
            tabs = st.tabs(["Audio Analysis", "Video Analysis", "Metadata", "Provenance", "Recommendations"])

            with tabs[0]:
                st.markdown("**Audio Layer Findings**")
                audio_findings = df_result.get("audio_findings", [])
                if audio_findings:
                    for ind in audio_findings:
                        sev_color = {"high": "#ef4444", "medium": "#f59e0b", "low": "#22c55e", "none": "#22c55e"}.get(ind.get("severity", "none"), "#94a3b8")
                        st.markdown(f"**{ind['type']}** — <span style='color:{sev_color}'>{ind['detail']}</span>", unsafe_allow_html=True)
                else:
                    st.info("No audio layer findings available for this scan type.")

            with tabs[1]:
                st.markdown("**Video Layer Findings**")
                vf = df_result.get("video_findings", {})
                if vf:
                    for k, v in vf.items():
                        st.markdown(f"- **{k.replace('_', ' ').title()}**: {v}")
                else:
                    st.info("No video layer findings available.")

            with tabs[2]:
                st.markdown("**Metadata Analysis**")
                mf = df_result.get("metadata_findings", {})
                if mf:
                    st.json(mf)
                else:
                    st.json({"camera_model": "Unknown", "c2pa_manifest": "Not present"})

            with tabs[3]:
                st.markdown("**Chain of Custody**")
                for step in df_result.get("provenance", []):
                    st.markdown(f"- {step}")

            with tabs[4]:
                st.markdown("**Recommendations**")
                for priority, action in df_result.get("recommendations", []):
                    st.markdown(f"**{priority}:** {action}")


elif page == "✅ Live Fact-Check":
    st.title("✅ Live Fact-Check Agent")
    st.caption("MARKET GAP: No broadcast-integrated real-time fact-checking | Automated claim verification during live broadcasts")
    show_demo_video_player()

    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e1b4b, #0f172a); padding: 16px; border-radius: 12px; border: 1px solid #0891b2; margin-bottom: 16px;">
    <h4 style="color: #67e8f9; margin: 0 0 8px 0;">⚡ Why This Doesn't Exist Yet</h4>
    <p style="color: #a5f3fc; margin: 0;">
    Current fact-checking tools require <strong>manual journalist input</strong>. No system autonomously extracts claims
    from live broadcasts and cross-references them in real-time. This agent enables on-air fact-checking
    with anchor alerts and producer cues — without any manual intervention.
    </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Live Broadcast Transcript Input")
        default_transcript = (
            f"Auto-extracted captions from: {DEMO_SAMPLE_VIDEO['title']}\n\n"
            "Music content identified as original composition — live performance recording.\n"
            "Crowd attendance confirmed as live event — venue capacity 5,000+.\n"
            "Content rated suitable for all audiences — no mature content detected.\n"
            "Video quality: 1080p broadcast grade — confirmed by technical metadata.\n"
            "Clip duration: 15 seconds — optimal format for viral social distribution."
        ) if DEMO_SAMPLE_AVAILABLE else (
            "The unemployment rate is currently at 3.7%, the lowest in 50 years.\n"
            "This bill received bipartisan support with 67 votes in the Senate.\n"
            "Climate scientists confirm global temperatures have risen 1.2 degrees since pre-industrial times.\n"
            "The new vaccine shows 94% efficacy in Phase 3 clinical trials according to the manufacturer.\n"
            "The city's population has grown by 18% over the last decade, making it one of the fastest growing cities."
        )
        transcript = st.text_area("Paste live broadcast transcript or captions",
                                   value=default_transcript,
                                   height=150)
        if st.button("✅ Run Live Fact-Check", use_container_width=True, type="primary"):
            with st.spinner("Extracting claims and verifying..."):
                import time as _time
                _time.sleep(1.8)
                st.session_state["fact_checked"] = True

    with col2:
        st.subheader("Fact-Check Sources")
        sources = ["AP Fact Check", "Reuters Fact Check", "PolitiFact", "FactCheck.org",
                   "Snopes", "Full Fact", "IFCN Network", "WHO Mythbusters"]
        for src in sources:
            st.markdown(f"🔗 {src}")

    if st.session_state.get("fact_checked"):
        st.divider()
        st.subheader("Fact-Check Results")

        claims_data = SAMPLE_FACT_CHECK_CLAIMS if DEMO_SAMPLE_AVAILABLE else [
            {"claim": "Unemployment rate at 3.7%, lowest in 50 years", "verdict": "MOSTLY TRUE", "color": "#22c55e", "icon": "✔️",
             "confidence": 0.87, "source": "Bureau of Labor Statistics", "note": "3.7% confirmed but 'lowest in 50 years' was 2019 level (3.5%)"},
            {"claim": "Bill received 67 votes in the Senate", "verdict": "UNVERIFIED", "color": "#94a3b8", "icon": "❓",
             "confidence": 0.62, "source": "Congressional Record", "note": "Unable to verify current bill vote count in real-time"},
            {"claim": "Global temps risen 1.2°C since pre-industrial", "verdict": "TRUE", "color": "#22c55e", "icon": "✅",
             "confidence": 0.97, "source": "IPCC AR6 Report", "note": "Confirmed by IPCC 2023 report: 1.1-1.2°C increase"},
            {"claim": "Vaccine shows 94% efficacy in Phase 3 trials", "verdict": "MISLEADING", "color": "#f59e0b", "icon": "⚠️",
             "confidence": 0.79, "source": "FDA Clinical Trial Database", "note": "94% was initial trial data; updated analysis shows 89.7%"},
            {"claim": "City population grew 18% over last decade", "verdict": "FALSE", "color": "#ef4444", "icon": "❌",
             "confidence": 0.83, "source": "US Census Bureau", "note": "Census data shows 12.3% growth, not 18%"},
        ]

        for i, claim in enumerate(claims_data):
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"""
                    <div style="background: rgba(30,41,59,0.8); padding: 12px; border-radius: 8px;
                                border-left: 4px solid {claim['color']}; margin: 4px 0;">
                        <strong>{claim['icon']} {claim['verdict']}</strong><br>
                        <span style="color: #e2e8f0;">{claim['claim']}</span><br>
                        <span style="color: #94a3b8; font-size: 0.85rem;">📚 {claim['source']} | {claim['note']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.metric("Confidence", f"{claim['confidence']:.0%}")
                with col3:
                    if claim["verdict"] in ["FALSE", "MISLEADING"]:
                        st.button(f"🔔 Alert Anchor", key=f"alert_{i}", use_container_width=True)

        st.divider()
        col1, col2, col3 = st.columns(3)
        false_count = sum(1 for c in claims_data if c["verdict"] in ["FALSE", "MISLEADING"])
        with col1:
            st.metric("Claims Checked", len(claims_data))
        with col2:
            st.metric("Problematic Claims", false_count, delta=f"{'🚨 Alert Producers' if false_count > 0 else 'Clear'}")
        with col3:
            st.metric("Avg Confidence", f"{sum(c['confidence'] for c in claims_data)/len(claims_data):.0%}")


elif page == "📊 Audience Intelligence":
    st.title("📊 Audience Intelligence & Retention Prediction")
    st.caption("MARKET GAP: No real-time viewer drop-off prediction for live broadcast | Predict & prevent audience loss BEFORE it happens")
    show_demo_video_player()

    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e1b4b, #0f172a); padding: 16px; border-radius: 12px; border: 1px solid #0d9488; margin-bottom: 16px;">
    <h4 style="color: #5eead4; margin: 0 0 8px 0;">⚡ Why This Doesn't Exist Yet</h4>
    <p style="color: #99f6e4; margin: 0;">
    Streaming platforms have basic recommendation engines, but <strong>no real-time viewer retention prediction
    exists for live broadcast TV</strong>. This agent predicts second-by-second drop-off risk and generates
    producer interventions <em>before viewers leave</em>, protecting ratings in real-time.
    </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        content_type = st.selectbox("Content Type", ["entertainment", "hard_news", "breaking_news", "weather", "sports", "human_interest", "interview"], index=0 if DEMO_SAMPLE_AVAILABLE else 1)
    with col2:
        _aud = SAMPLE_AUDIENCE_DATA if DEMO_SAMPLE_AVAILABLE else {}
        st.metric("Current Viewers", f"{_aud.get('current_viewers', random.randint(250000, 850000)):,}", _aud.get('viewer_trend', f"+{random.randint(2, 15)}K/min"))
    with col3:
        st.metric("Retention Risk", f"{_aud.get('retention_risk', random.randint(18, 45))}%", "next 10 min")
    with col4:
        st.metric("Predicted Peak", f"{_aud.get('predicted_peak', random.randint(480000, 1200000)):,}", f"in {_aud.get('peak_in_min', random.randint(8, 22))} min")

    if st.button("📊 Generate Audience Prediction", use_container_width=True, type="primary"):
        with st.spinner("Generating retention curve & intervention plan..."):
            import time as _time
            _time.sleep(1.5)
            st.session_state["audience_done"] = True

    if st.session_state.get("audience_done"):
        st.divider()

        aud = SAMPLE_AUDIENCE_DATA if DEMO_SAMPLE_AVAILABLE else {}

        # Retention curve data
        if DEMO_SAMPLE_AVAILABLE:
            curve = aud["retention_curve"]
            time_axis = curve["seconds"]
            ret_values = curve["values"]
            time_label = "Seconds"
        else:
            time_axis = list(range(0, 60, 5))
            base_ret = {"hard_news": 72, "breaking_news": 88, "weather": 65, "sports": 78, "entertainment": 95, "human_interest": 71, "interview": 69}.get(content_type, 72)
            ret_values = [min(100, base_ret + random.randint(-3, 8) - i * 0.8) for i in range(len(time_axis))]
            time_label = "Minutes"

        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Predicted Retention Curve")
            import pandas as pd
            chart_data = pd.DataFrame({time_label: time_axis, "Retention %": [round(r, 1) for r in ret_values]})
            st.line_chart(chart_data.set_index(time_label), color="#0d9488")
            if DEMO_SAMPLE_AVAILABLE and aud["retention_curve"].get("note"):
                st.caption(f"💡 {aud['retention_curve']['note']}")

            # Drop-off warnings
            st.subheader("⚠️ Drop-off Risk Points")
            drop_risks = aud.get("drop_risks", [
                {"second": 15, "risk": "high", "drop_pct": 8.2, "cause": "Single-topic coverage fatigue", "intervention": "Cut to field reporter for new angle"},
                {"second": 25, "risk": "medium", "drop_pct": 5.1, "cause": "Pre-commercial break natural exit", "intervention": "Tease exclusive story to hold viewers"},
            ])
            time_key = "second" if DEMO_SAMPLE_AVAILABLE else "minute"
            for risk in drop_risks:
                risk_color = "#ef4444" if risk["risk"] == "high" else "#f59e0b"
                t_val = risk.get(time_key, risk.get("second", risk.get("minute", "?")))
                st.markdown(f"""
                <div style="background: rgba(30,41,59,0.8); padding: 12px; border-radius: 8px;
                            border-left: 4px solid {risk_color}; margin: 8px 0;">
                    <strong>{t_val}s - {risk['risk'].upper()} RISK: -{risk['drop_pct']}% drop predicted</strong><br>
                    <span style="color: #94a3b8;">Cause: {risk['cause']}</span><br>
                    <span style="color: #5eead4;">💡 Intervention: {risk['intervention']}</span>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.subheader("Demographic Breakdown")
            demos = aud.get("demographics", {"18-34": random.randint(55, 75), "35-54": random.randint(70, 88), "55-64": random.randint(65, 82), "65+": random.randint(58, 78)})
            for demo, pct in demos.items():
                st.progress(pct / 100, text=f"Age {demo}: {pct}% of audience")

            st.subheader("Competitive Analysis")
            competitors = aud.get("competitors", {"CNN": random.randint(8, 25), "Fox News": random.randint(10, 30), "Streaming": random.randint(15, 40)})
            for ch, pct in competitors.items():
                st.markdown(f"→ {pct}% of dropoffs go to **{ch}**")

            st.subheader("Live Metrics")
            lm = aud.get("live_metrics", {})
            st.metric("Social Chatter", f"{lm.get('social_chatter', random.randint(1200, 8500)):,}/min")
            st.metric("Second Screen", f"{lm.get('second_screen_pct', random.randint(18, 42))}%")
            st.metric("Sentiment", f"{lm.get('sentiment_score', round(random.uniform(0.45, 0.82), 2))}")


elif page == "🎬 AI Production Director":
    st.title("🎬 AI Production Director")
    st.caption("MARKET GAP: No autonomous AI production director exists for live broadcast | Camera cuts, graphics, rundown optimization")
    show_demo_video_player()

    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e1b4b, #0f172a); padding: 16px; border-radius: 12px; border: 1px solid #d97706; margin-bottom: 16px;">
    <h4 style="color: #fcd34d; margin: 0 0 8px 0;">⚡ Why This Doesn't Exist Yet</h4>
    <p style="color: #fde68a; margin: 0;">
    Every camera cut, graphics call, and break decision currently requires a human director.
    This agent acts as an <strong>autonomous AI co-pilot</strong> for the production director —
    suggesting real-time camera cuts, auto-generating lower-thirds, optimizing rundown order,
    and timing commercial breaks for maximum viewer retention.
    </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🎬 Generate Production Direction Package", use_container_width=True, type="primary"):
        with st.spinner("Analyzing rundown and generating production directions..."):
            import time as _time
            _time.sleep(1.5)
            st.session_state["prod_done"] = True

    if st.session_state.get("prod_done"):
        pd_data = SAMPLE_PRODUCTION_DATA if DEMO_SAMPLE_AVAILABLE else {}
        tabs = st.tabs(["📷 Camera Plan", "📝 Lower Thirds", "📋 Rundown", "⏰ Break Strategy", "🔊 Audio", "⚙️ Technical"])

        with tabs[0]:
            st.subheader("Recommended Camera Shot Plan — Entertainment Showcase (15s)" if DEMO_SAMPLE_AVAILABLE else "Recommended Camera Shot Plan (Next 15 min)")
            shots = pd_data.get("shots", [
                {"shot": 1, "camera": "Camera 2", "type": "Medium", "use": "Anchor open", "duration": "8s", "confidence": 0.94},
                {"shot": 2, "camera": "Camera 4", "type": "Wide", "use": "Studio establishing", "duration": "5s", "confidence": 0.88},
                {"shot": 3, "camera": "Camera 1", "type": "Close-up", "use": "Anchor emphasis", "duration": "6s", "confidence": 0.91},
                {"shot": 4, "camera": "Remote Feed", "type": "Remote Guest", "use": "Washington DC guest", "duration": "45s", "confidence": 0.96},
            ])
            import pandas as pd
            df = pd.DataFrame(shots)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption(f"AI acceptance rate today: 89% | Human overrides: 2")

        with tabs[1]:
            st.subheader("Auto-Generated Lower Thirds")
            lowers = pd_data.get("lower_thirds", [
                {"line1": "SARAH JOHNSON", "line2": "Chief Political Correspondent", "style": "Standard", "trigger": "On cut to reporter"},
                {"line1": "BREAKING NEWS", "line2": "Economic Announcement Expected", "style": "⚡ Breaking (Red)", "trigger": "Manual"},
            ])
            for lt in lowers:
                st.markdown(f"""
                <div style="background: #1e293b; padding: 10px; border-radius: 6px; margin: 6px 0; border-left: 3px solid #d97706;">
                    <strong>{lt['line1']}</strong> | <span style="color: #94a3b8;">{lt['line2']}</span><br>
                    <small>Style: {lt['style']} | Trigger: {lt['trigger']}</small>
                </div>
                """, unsafe_allow_html=True)

        with tabs[2]:
            st.subheader("Rundown Analysis & Optimization")
            rundown = pd_data.get("rundown", [
                {"pos": 1, "slug": "ELECTION-UPDATE", "type": "Hard News", "planned": "3:00", "score": 9.2, "suggestion": "✅ Keep as lead"},
                {"pos": 2, "slug": "WEATHER-LEAD", "type": "Weather", "planned": "2:00", "score": 7.1, "suggestion": "⬇️ Move to pos 3"},
                {"pos": 3, "slug": "MARKET-CLOSE", "type": "Business", "planned": "2:30", "score": 8.0, "suggestion": "⬆️ Move to pos 2"},
                {"pos": 4, "slug": "SPORTS-HIGHLIGHTS", "type": "Sports", "planned": "4:00", "score": 6.8, "suggestion": "✂️ Trim to 3:00"},
            ])
            import pandas as pd
            df = pd.DataFrame(rundown)
            st.dataframe(df, use_container_width=True, hide_index=True)

        with tabs[3]:
            st.subheader("Commercial Break Optimization")
            breaks = pd_data.get("break_strategy", [
                {"break": 1, "planned": "10:00", "ai_suggest": "11:30", "reason": "Post story-arc completion at 11:30 creates natural exit", "return_rate": "76%"},
                {"break": 2, "planned": "24:00", "ai_suggest": "22:45", "reason": "Competitor breaking story emerging — break early, tease exclusive", "return_rate": "71%"},
            ])
            for b in breaks:
                st.markdown(f"""
                <div style="background: #1e293b; padding: 12px; border-radius: 8px; margin: 8px 0;">
                    <strong>Break {b['break']}:</strong> Planned {b['planned']} →
                    <span style="color: #fcd34d;">AI Suggests {b['ai_suggest']}</span><br>
                    <span style="color: #94a3b8;">{b['reason']}</span><br>
                    <span style="color: #22c55e;">Projected return rate: {b['return_rate']}</span>
                </div>
                """, unsafe_allow_html=True)

        with tabs[4]:
            st.subheader("Audio Mix Recommendations")
            audio_recs = pd_data.get("audio_recommendations", [
                {"source": "Studio anchor mic", "level": "-16.0 dBFS", "status": "✅ Good"},
                {"source": "Remote guest", "level": "-21.5 dBFS", "status": "⚠️ Boost +5dB"},
                {"source": "Studio ambient", "level": "-38.0 dBFS", "status": "✅ Good"},
            ])
            for a in audio_recs:
                st.markdown(f"**{a['source']}** — {a['level']} — {a['status']}")

        with tabs[5]:
            st.subheader("Technical Health")
            tech = pd_data.get("technical", {})
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Main Feed", f"{tech.get('main_feed_mbps', round(random.uniform(12, 22), 1))} Mbps", "Healthy")
                st.metric("Stream Latency", f"{tech.get('stream_latency_ms', random.randint(80, 320))}ms", "Remote feed")
            with col2:
                st.metric("Graphics Latency", f"{tech.get('graphics_latency_ms', random.randint(12, 35))}ms", "Online")
                st.metric("Chyron", f"{random.randint(10, 25)}ms", "Online")
            with col3:
                st.metric("Loudness", f"{tech.get('loudness_lufs', round(random.uniform(-22, -18), 1))} LUFS", "ITU-R BS.1770")
                st.metric("Stream Health", tech.get("stream_health", "Excellent"), "All CDNs stable")


elif page == "🛡️ Brand Safety":
    st.title("🛡️ Brand Safety & Contextual Ad Intelligence")
    st.caption("MARKET GAP: No real-time brand safety scoring for live broadcast | Protect advertiser relationships & maximize ad revenue")
    show_demo_video_player()

    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e1b4b, #0f172a); padding: 16px; border-radius: 12px; border: 1px solid #dc2626; margin-bottom: 16px;">
    <h4 style="color: #fca5a5; margin: 0 0 8px 0;">⚡ Why This Doesn't Exist Yet</h4>
    <p style="color: #fecaca; margin: 0;">
    Brand safety tools exist for <strong>digital/programmatic</strong> advertising, but NO real-time
    contextual brand safety scoring exists for <strong>live broadcast TV</strong>. Advertisers currently
    have zero visibility into adjacent content until AFTER air. This agent scores content in real-time
    to protect brand relationships and optimize CPM pricing.
    </p>
    </div>
    """, unsafe_allow_html=True)

    _bs = SAMPLE_BRAND_SAFETY_DATA if DEMO_SAMPLE_AVAILABLE else {}
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Current Safety Score", f"{_bs.get('overall_score', random.randint(68, 94))}/100", "GARM compliant")
    with col2:
        st.metric("Active Advertisers", f"{_bs.get('active_advertisers', random.randint(18, 45))}", f"{_bs.get('blocked_advertisers', random.randint(2, 6))} blocked")
    with col3:
        st.metric("Premium Windows", f"{_bs.get('premium_windows_today', random.randint(3, 8))} today", f"+{_bs.get('cpm_uplift_pct', round(random.uniform(12, 28), 1))}% CPM")
    with col4:
        st.metric("Revenue Protected", f"${_bs.get('premium_opportunity', random.randint(8000, 65000)):,}", "This broadcast")

    default_content = (
        f"Entertainment content from: {DEMO_SAMPLE_VIDEO['title']}\n\n"
        "High-energy 15-second performance clip. Original music. Live crowd. "
        "Family-safe entertainment content suitable for all advertisers. "
        "No violence, hate speech, adult content or controversial topics detected."
    ) if DEMO_SAMPLE_AVAILABLE else (
        "Tonight on WKRN: We continue to follow the developing story on the federal economic announcement. "
        "Markets have responded sharply to today's Fed decision. Our financial correspondent breaks down "
        "what this means for your portfolio. Later: the city council votes on the downtown development project, "
        "and a heartwarming story of community resilience."
    )
    content_input = st.text_area("Paste current broadcast segment transcript for analysis",
                                  value=default_content,
                                  height=100)

    if st.button("🛡️ Run Brand Safety Analysis", use_container_width=True, type="primary"):
        with st.spinner("Scoring content for brand safety..."):
            import time as _time
            _time.sleep(1.3)
            st.session_state["brand_safety_done"] = True

    if st.session_state.get("brand_safety_done"):
        st.divider()

        bs = SAMPLE_BRAND_SAFETY_DATA if DEMO_SAMPLE_AVAILABLE else {}
        overall_score = bs.get("overall_score", random.randint(72, 92))
        level = bs.get("level", "Premium Safe" if overall_score >= 85 else "Standard Safe" if overall_score >= 70 else "Caution")
        level_color = bs.get("level_color", "#22c55e" if overall_score >= 85 else "#f59e0b" if overall_score >= 70 else "#ef4444")

        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown(f"""
            <div style="background: rgba(30,41,59,0.8); padding: 20px; border-radius: 12px; text-align: center; border: 2px solid {level_color};">
                <h1 style="color: {level_color}; margin: 0;">{overall_score}</h1>
                <p style="color: {level_color}; margin: 4px 0; font-size: 1.1rem;">{level}</p>
                <p style="color: #94a3b8; margin: 0; font-size: 0.85rem;">GARM Standard Score</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("**GARM Risk Flags**")
            garm_items = bs.get("garm_flags", [
                ("Controversial News", "medium", "⚠️"), ("Violence/Gore", "none", "✅"),
                ("Hate Speech", "none", "✅"), ("Adult Content", "none", "✅"), ("Profanity", "none", "✅")
            ])
            for item, sev, icon in garm_items:
                color = "#f59e0b" if sev == "medium" else "#22c55e"
                st.markdown(f"<span style='color:{color}'>{icon} {item}</span>", unsafe_allow_html=True)

        with col2:
            st.subheader("Advertiser Impact Assessment")
            advertisers = bs.get("advertisers", [
                {"name": "Luxury Auto", "min_score": 80, "status": "Safe" if overall_score >= 80 else "Blocked", "cpm": f"${round(random.uniform(45, 85), 2)}"},
                {"name": "Pharmaceutical", "min_score": 75, "status": "Safe" if overall_score >= 75 else "Blocked", "cpm": f"${round(random.uniform(38, 72), 2)}"},
                {"name": "Financial Services", "min_score": 70, "status": "Safe" if overall_score >= 70 else "Blocked", "cpm": f"${round(random.uniform(30, 65), 2)}"},
                {"name": "Family Products", "min_score": 85, "status": "Safe" if overall_score >= 85 else "⚠️ Review", "cpm": f"${round(random.uniform(25, 55), 2)}"},
                {"name": "Fast Food", "min_score": 60, "status": "Safe", "cpm": f"${round(random.uniform(18, 40), 2)}"},
            ])
            import pandas as pd
            df = pd.DataFrame(advertisers)
            st.dataframe(df, use_container_width=True, hide_index=True)

            st.subheader("Revenue Optimization")
            col3, col4 = st.columns(2)
            with col3:
                st.metric("Current CPM", f"${bs.get('current_cpm', round(random.uniform(22, 45), 2))}")
                st.metric("Optimized CPM", f"${bs.get('optimized_cpm', round(random.uniform(35, 68), 2))}", f"+{bs.get('cpm_uplift_pct', round(random.uniform(15, 38), 1))}%")
            with col4:
                st.metric("Revenue at Risk", f"${bs.get('revenue_at_risk', random.randint(2000, 15000)):,}")
                st.metric("Premium Opportunity", f"+${bs.get('premium_opportunity', random.randint(3000, 18000)):,}")


elif page == "🌿 Carbon Intelligence":
    st.title("🌿 Carbon Intelligence & ESG Broadcast Agent")
    st.caption("MARKET GAP: No integrated carbon tracking for broadcast operations | ESG compliance for advertisers & regulators")
    show_demo_video_player()

    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e1b4b, #0f172a); padding: 16px; border-radius: 12px; border: 1px solid #16a34a; margin-bottom: 16px;">
    <h4 style="color: #86efac; margin: 0 0 8px 0;">⚡ Why This Doesn't Exist Yet</h4>
    <p style="color: #bbf7d0; margin: 0;">
    The broadcast industry faces increasing <strong>ESG pressure from advertisers and regulators</strong>, but
    NO integrated carbon tracking tool exists for broadcast operations. This agent provides real-time
    energy monitoring, Scope 1/2/3 emissions tracking, and auto-generates ESG reports for
    stakeholders — a genuine first-to-market capability.
    </p>
    </div>
    """, unsafe_allow_html=True)

    _carbon_types = (["entertainment_clip", "standard_news", "breaking_news", "live_event", "sports_broadcast", "remote_production"] if DEMO_SAMPLE_AVAILABLE
                     else ["standard_news", "breaking_news", "live_event", "sports_broadcast", "remote_production"])
    broadcast_type = st.selectbox("Broadcast Type", _carbon_types)

    if st.button("🌿 Generate Carbon Intelligence Report", use_container_width=True, type="primary"):
        with st.spinner("Calculating broadcast carbon footprint..."):
            import time as _time
            _time.sleep(1.5)
            st.session_state["carbon_done"] = True

    if st.session_state.get("carbon_done"):
        st.divider()
        c = SAMPLE_CARBON_DATA if DEMO_SAMPLE_AVAILABLE else {}

        # Key metrics
        co2_today = c.get("total_co2e_kg", round(random.uniform(320, 780), 1))
        renewable_pct = c.get("renewable_pct", round(random.uniform(22, 58), 1))
        esg_score = c.get("esg_score", round(random.uniform(58, 82), 1))
        scope1 = c.get("scope1_kg", round(co2_today * 0.15, 1))
        scope2 = c.get("scope2_kg", round(co2_today * 0.70, 1))
        scope3 = c.get("scope3_kg", round(co2_today * 0.15, 1))

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            _co2_delta = (f"{c.get('vs_industry_avg_pct', -28)}% vs industry avg"
                          if DEMO_SAMPLE_AVAILABLE else
                          f"vs {round(co2_today*random.uniform(0.9, 1.15), 1)} kg yesterday")
            st.metric("CO₂e — This Clip" if DEMO_SAMPLE_AVAILABLE else "CO₂e Today",
                      f"{co2_today} kg", _co2_delta)
        with col2:
            _annual = (round(co2_today * 4 * 52 / 1000, 1) if DEMO_SAMPLE_AVAILABLE
                       else round(co2_today * 365 / 1000, 1))
            _annual_lbl = "Annual (4 clips/wk)" if DEMO_SAMPLE_AVAILABLE else "Annual CO₂e"
            st.metric(_annual_lbl, f"{_annual} tonnes", "Scope 1+2+3")
        with col3:
            st.metric("Renewable Mix", f"{renewable_pct}%", f"Grid: {100-renewable_pct:.0f}% fossil")
        with col4:
            st.metric("ESG Score", f"{esg_score}/100",
                      f"Rating: {'A' if esg_score >= 80 else 'B+' if esg_score >= 70 else 'B'}")

        tabs = st.tabs(["⚡ Energy Breakdown", "🌍 Carbon Footprint", "📊 Optimizations", "♻️ Offsets", "📋 ESG Report"])

        with tabs[0]:
            st.subheader("Equipment Energy Consumption")
            import pandas as pd
            if DEMO_SAMPLE_AVAILABLE:
                equip_breakdown = c.get("equipment_breakdown", {})
                equipment_rows = [
                    {"Equipment": eq, "kWh (15s clip)": round(kwh, 2),
                     "CO₂e (kg)": round(kwh * 0.386, 3), "Status": "Active"}
                    for eq, kwh in equip_breakdown.items()
                ]
                df = pd.DataFrame(equipment_rows)
                st.dataframe(df, use_container_width=True, hide_index=True)
                _col_e1, _col_e2 = st.columns(2)
                _col_e1.metric("Total Energy (This Clip)", f"{c.get('energy_kwh', 28.4)} kWh")
                _col_e2.metric("Social Distribution CO₂e",
                               f"{c.get('social_distribution_co2e', 4.8)} kg / 1M views")
            else:
                equipment = [
                    {"Equipment": "Main Transmitter (12kW)", "Category": "Broadcast", "kWh Today": round(12*18, 1), "Status": "Active"},
                    {"Equipment": "Server Farm (18kW)", "Category": "IT", "kWh Today": round(18*24, 1), "Status": "Active"},
                    {"Equipment": "Studio HVAC (22kW)", "Category": "Facility", "kWh Today": round(22*18, 1), "Status": "Active"},
                    {"Equipment": "Studio A Lighting (4.5kW)", "Category": "Studio", "kWh Today": round(4.5*10, 1), "Status": "Active"},
                    {"Equipment": "CDN Streaming (5kW)", "Category": "Digital", "kWh Today": round(5*24, 1), "Status": "Active"},
                    {"Equipment": "OB Truck (35kW)" if broadcast_type == "live_event" else "OB Truck (standby)", "Category": "Remote", "kWh Today": round(35*8, 1) if broadcast_type == "live_event" else 0, "Status": "Active" if broadcast_type == "live_event" else "Standby"},
                ]
                df = pd.DataFrame(equipment)
                st.dataframe(df, use_container_width=True, hide_index=True)
                st.metric("Total Energy Today", f"{sum(e['kWh Today'] for e in equipment):,.0f} kWh")

        with tabs[1]:
            st.subheader("Carbon Footprint Breakdown")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Scope Breakdown**")
                st.progress(scope1/co2_today, text=f"Scope 1 (Direct): {scope1} kg")
                st.progress(scope2/co2_today, text=f"Scope 2 (Grid electricity): {scope2} kg")
                st.progress(scope3/co2_today, text=f"Scope 3 (Supply chain, travel): {scope3} kg")
            with col2:
                st.markdown("**Carbon Equivalents**")
                st.markdown(f"🚗 **{round(co2_today * 2.48):,} miles** driven by car")
                st.markdown(f"✈️ **{round(co2_today/286, 2)} flights** NYC → LA")
                st.markdown(f"📱 **{round(co2_today * 121):,} smartphones** charged")
                st.markdown(f"🌳 **{round(co2_today * 365 / 21000, 1)} acres** forest/year to offset")

        with tabs[2]:
            st.subheader("Carbon Reduction Opportunities")
            import pandas as pd
            if DEMO_SAMPLE_AVAILABLE:
                _renew_opts = c.get("renewable_options", [])
                _priorities = ["🔴 High", "🟡 Medium", "🟢 Low"]
                optimizations = [
                    {
                        "Priority": _priorities[min(i, 2)],
                        "Action": opt.get("option", ""),
                        "CO₂ Saving": f"{opt.get('saving_pct', 0)}%",
                        "Est. Cost": opt.get("cost", "TBD"),
                    }
                    for i, opt in enumerate(_renew_opts)
                ]
                df = pd.DataFrame(optimizations)
                st.dataframe(df, use_container_width=True, hide_index=True)
                st.info(f"💡 Total optimization potential: **{c.get('optimization_potential_pct', 18)}%** CO₂e reduction with current technology")
                st.metric("Green Schedule Saving", f"{c.get('green_schedule_saving_pct', 12)}%",
                          "by shifting encoding to off-peak grid hours")
            else:
                optimizations = [
                    {"priority": "🔴 High", "action": "Shift batch video encoding to 2AM-6AM (40% lower grid carbon intensity)", "CO₂ Savings/month": f"{round(random.uniform(180, 450), 0):.0f} kg", "Cost Savings": f"${random.randint(800, 3200):,}"},
                    {"priority": "🔴 High", "action": "Procure 100% renewable energy PPA (current mix 28%)", "CO₂ Savings/month": f"{round(co2_today*0.85*30, 0):.0f} kg", "Cost Savings": f"${random.randint(-500, 2000):,}"},
                    {"priority": "🟡 Medium", "action": "Replace studio HMI/tungsten lighting with LED", "CO₂ Savings/month": f"{round(random.uniform(120, 380), 0):.0f} kg", "Cost Savings": f"${random.randint(600, 2400):,}"},
                    {"priority": "🟡 Medium", "action": "Replace OB truck with cloud REMI production model", "CO₂ Savings/event": f"{round(random.uniform(200, 800), 0):.0f} kg", "Cost Savings": f"${random.randint(5000, 25000):,}"},
                    {"priority": "🟢 Low", "action": "Migrate CDN to AWS eu-west (lower carbon region)", "CO₂ Savings/month": f"{round(random.uniform(40, 180), 0):.0f} kg", "Cost Savings": f"${random.randint(200, 800):,}"},
                ]
                df = pd.DataFrame(optimizations)
                st.dataframe(df, use_container_width=True, hide_index=True)

        with tabs[3]:
            st.subheader("Carbon Offset Recommendations")
            import pandas as pd
            if DEMO_SAMPLE_AVAILABLE:
                _offset_kg = c.get("offset_recommended_kg", 5.0)
                _offset_cost = c.get("offset_cost_usd", 2.50)
                offsets = [
                    {"Project": "US Forestry (Gold Standard)", "Type": "Nature-based", "$/tonne": "$18", "Clip Cost": f"${_offset_kg * 18 / 1000:.4f}", "Rating": "⭐⭐⭐⭐⭐"},
                    {"Project": "Wind Farm Dev - South Asia", "Type": "Renewable Energy", "$/tonne": "$9", "Clip Cost": f"${_offset_kg * 9 / 1000:.4f}", "Rating": "⭐⭐⭐⭐"},
                    {"Project": "Direct Air Capture (Climeworks)", "Type": "Technological", "$/tonne": "$550", "Clip Cost": f"${_offset_kg * 550 / 1000:.3f}", "Rating": "⭐⭐⭐⭐⭐ (permanent)"},
                ]
                df = pd.DataFrame(offsets)
                st.dataframe(df, use_container_width=True, hide_index=True)
                st.info(f"💡 Recommended offset for this 15s clip: **{_offset_kg} kg CO₂e** — Full offset cost: **${_offset_cost:.2f}** via verified nature-based project")
            else:
                annual_tonnes = round(co2_today * 365 / 1000, 1)
                offsets = [
                    {"Project": "US Forestry (Gold Standard)", "Type": "Nature-based", "$/tonne": "$18", "Annual Cost": f"${round(annual_tonnes * 18):,}", "Rating": "⭐⭐⭐⭐⭐"},
                    {"Project": "Wind Farm Dev - South Asia", "Type": "Renewable Energy", "$/tonne": "$9", "Annual Cost": f"${round(annual_tonnes * 9):,}", "Rating": "⭐⭐⭐⭐"},
                    {"Project": "Direct Air Capture (Climeworks)", "Type": "Technological", "$/tonne": "$550", "Annual Cost": f"${round(annual_tonnes * 550):,}", "Rating": "⭐⭐⭐⭐⭐ (permanent)"},
                ]
                df = pd.DataFrame(offsets)
                st.dataframe(df, use_container_width=True, hide_index=True)
                st.info(f"💡 Recommended: US Forestry offset at $18/tonne. Annual cost to offset all Scope 2: **${round(co2_today * 0.7 * 365 / 1000 * 18):,}**")

        with tabs[4]:
            st.subheader("ESG Report Summary")
            rating = "A" if esg_score >= 80 else "B+" if esg_score >= 70 else "B"
            _standards = (", ".join(c.get("esg_report_standards", ["GRI 305", "TCFD", "GHG Protocol"]))
                          if DEMO_SAMPLE_AVAILABLE else "GRI 305, TCFD, GHG Protocol")
            _carbon_int = (c.get("carbon_intensity_per_min", 49.6) if DEMO_SAMPLE_AVAILABLE
                           else round(random.uniform(85, 245), 1))
            _int_label = "Carbon Intensity" if DEMO_SAMPLE_AVAILABLE else "Energy Intensity"
            _int_unit = "kg CO₂e/min" if DEMO_SAMPLE_AVAILABLE else "kWh/broadcast-hour"
            _scope_ctx = ("Entertainment Showcase clip (15s)" if DEMO_SAMPLE_AVAILABLE
                          else "broadcast facility")
            _co2_summary = (f"**{co2_today} kg CO₂e** (this clip)"
                            if DEMO_SAMPLE_AVAILABLE else
                            f"**{round(co2_today * 365 / 1000, 1)} tCO₂e annually**")
            _co2_metric = (f"{co2_today} kg" if DEMO_SAMPLE_AVAILABLE
                           else f"{round(co2_today * 365 / 1000, 1)} tonnes")
            _co2_metric_label = "Clip CO₂e" if DEMO_SAMPLE_AVAILABLE else "Annual CO₂e"
            st.markdown(f"""
            **Report Period:** {datetime.now().strftime('%B %Y')}

            **Executive Summary:**
            This {_scope_ctx} achieved an ESG score of **{esg_score}/100** (Rating: **{rating}**) this period.
            Total carbon footprint: {_co2_summary}.
            Renewable energy mix: **{renewable_pct}%**. Net Zero target: **2035**.

            **Key Metrics:**
            - 📊 {_co2_metric_label}: {_co2_metric}
            - ⚡ Renewable Energy: {renewable_pct}%
            - 🏭 {_int_label}: {_carbon_int} {_int_unit}
            - 📋 Frameworks Aligned: {_standards}
            - ✅ Advertiser ESG Compliant: {'Yes' if esg_score >= 60 else 'No'}
            - 📅 Next Audit: {(datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')}
            """)
            if st.button("📄 Export ESG Report (PDF)", use_container_width=True):
                st.info("Production mode: Generates full GRI 305-compliant PDF report for stakeholder disclosure")


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
