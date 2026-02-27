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
        DEMO_DEEPFAKE_RESULT, DEMO_FACT_CHECK_CLAIMS,
        DEMO_AUDIENCE_DATA, DEMO_PRODUCTION_DATA,
        DEMO_BRAND_SAFETY_DATA, DEMO_CARBON_DATA,
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
    },
    "deepfake_provenance": {
        "name": "Deepfake Detection & Content Provenance",
        "description": "Integration with C2PA provenance registries and forensic AI services to authenticate media before broadcast.",
        "capabilities": [
            "C2PA content credentials verification",
            "Audio/video forensic analysis",
            "Metadata trust chain validation",
            "Auto-hold workflow for flagged content",
            "Third-party lab API integration (Truepic, Hive)"
        ],
        "protocols": ["C2PA REST API", "REST API", "Webhooks"],
        "status": "Future Ready"
    },
    "fact_check_databases": {
        "name": "Live Fact-Check & Verification Networks",
        "description": "Real-time claim verification against 8+ authoritative fact-check databases and wire services.",
        "capabilities": [
            "AP & Reuters wire feed integration",
            "PolitiFact, FactCheck.org, Snopes APIs",
            "Full Fact & IFCN network access",
            "WHO & CDC health claim verification",
            "GPT-4 claim extraction pipeline"
        ],
        "protocols": ["REST API", "RSS/Atom", "GraphQL"],
        "status": "Future Ready"
    },
    "audience_analytics": {
        "name": "Audience Intelligence & Analytics",
        "description": "Integration with broadcast ratings and streaming analytics platforms for real-time audience insights.",
        "capabilities": [
            "Nielsen & Comscore ratings sync",
            "Second-by-second retention curve",
            "Demographic breakdown by platform",
            "Competitor migration tracking",
            "Drop-off risk alert webhooks"
        ],
        "protocols": ["REST API", "WebSocket", "Webhooks"],
        "status": "Future Ready"
    },
    "graphics_newsroom": {
        "name": "Graphics Servers & Newsroom Systems",
        "description": "AI Production Director integration with broadcast graphics servers and newsroom computer systems.",
        "capabilities": [
            "Vizrt / ChyronHego lower-thirds automation",
            "iNews & ENPS rundown sync",
            "Camera tally & PTZ control",
            "Real-time graphics triggering",
            "Commercial break automation"
        ],
        "protocols": ["Vizrt DataHub API", "MOS Protocol", "REST API", "WebSocket"],
        "status": "Future Ready"
    },
    "brand_safety_adtech": {
        "name": "Brand Safety & Ad Tech Integration",
        "description": "GARM-compliant brand safety scoring integrated with programmatic ad platforms and verification services.",
        "capabilities": [
            "IAS & DoubleVerify API integration",
            "GARM 10-category compliance checks",
            "IAB Tech Lab 36-category taxonomy",
            "DV360 / The Trade Desk CPM optimization",
            "Real-time ad block / allow webhooks"
        ],
        "protocols": ["OpenRTB", "REST API", "Webhooks"],
        "status": "Future Ready"
    },
    "carbon_esg_reporting": {
        "name": "Carbon Intelligence & ESG Reporting",
        "description": "Integration with electricity grid carbon APIs and ESG reporting frameworks for sustainability compliance.",
        "capabilities": [
            "ElectricityMap / WattTime grid intensity API",
            "GHG Protocol Scope 1/2/3 calculation",
            "GRI 305 / TCFD / SBTi report generation",
            "Verified carbon offset registry (Gold Standard)",
            "Advertiser ESG compliance dashboard"
        ],
        "protocols": ["REST API", "REST API (Carbon APIs)", "PDF Export"],
        "status": "Future Ready"
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
            # ── Phase 1 Pipeline Agents ──
            "📥 Ingest + Transcode", "📡 Signal Quality",
            "📋 Playout Scheduling", "🌐 OTT Distribution",
            "📰 Newsroom Integration",
            # System
            "Integration Showcase",
            "💬 Channel Simulator",
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

    st.success("All 19 Agents Online")
    st.info("💬 Slack + Teams Gateway Active")

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
                {"agent": "📈 Trending Agent",        "interval": "Every 5 min",  "last_run": "2 min ago",  "status": "✅ Active"},
                {"agent": "⚖️ Compliance Agent",      "interval": "Every 10 min", "last_run": "7 min ago",  "status": "✅ Active"},
                {"agent": "📜 Rights Agent",           "interval": "Every 1 hour", "last_run": "34 min ago", "status": "✅ Active"},
                {"agent": "🔍 Archive Agent",          "interval": "Every 6 hours","last_run": "2h ago",     "status": "✅ Active"},
                {"agent": "📡 Signal Quality",         "interval": "Every 2 min",  "last_run": "1 min ago",  "status": "✅ Active"},
                {"agent": "📰 Newsroom Integration",   "interval": "Every 3 min",  "last_run": "2 min ago",  "status": "✅ Active"},
                {"agent": "📋 Playout Scheduling",     "interval": "Every 5 min",  "last_run": "3 min ago",  "status": "✅ Active"},
                {"agent": "🌐 OTT Distribution",       "interval": "Every 10 min", "last_run": "6 min ago",  "status": "✅ Active"},
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
    _jobs = random.randint(138, 162)
    _hrs = round(random.uniform(44.5, 52.3), 1)
    _comp = round(random.uniform(94.8, 97.6), 1)
    _clips = random.randint(9, 16)
    col1.metric("Jobs Processed", str(_jobs), f"+{random.randint(18, 31)} vs yesterday")
    col2.metric("Content Captioned", f"{_hrs} hrs", "of video")
    col3.metric("Compliance Score", f"{_comp}%", f"+{round(random.uniform(1.2, 3.1), 1)}%")
    col4.metric("Viral Clips Found", str(_clips), "this week")
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
        st.metric("Video Processed", f"{round(random.uniform(44.5, 52.3), 1)} hrs")
        st.metric("Captions Generated", f"{random.randint(11800, 13200):,} segments")
        st.metric("Clips Extracted", str(random.randint(42, 56)))
        st.metric("Posts Published", str(random.randint(24, 34)))

        st.divider()

        st.markdown("**System Health**")
        st.progress(0.96, "API Uptime: 99.6%")
        st.progress(0.82, "Processing Queue: 18%")
        st.progress(0.45, "Storage Used: 45%")


elif page == "🚀 All-in-One Workflow":
    st.title("🚀 All-in-One Workflow")
    st.caption("Process content through ALL 14 AI Agents simultaneously | Complete media intelligence in one click")

    st.markdown("""
    **The Complete Media Intelligence Pipeline** - Upload your content once and let all 14 AI agents
    analyze it simultaneously. Get captions, viral clips, compliance checks, social posts,
    translations, rights verification, trending context, deepfake detection, fact-checking,
    audience intelligence, production direction, brand safety, and carbon tracking — all in one workflow.
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
        st.markdown("*Original 8 Agents:*")
        run_caption = st.checkbox("📝 Caption Agent", value=True)
        run_clip = st.checkbox("🎬 Clip Agent", value=True)
        run_compliance = st.checkbox("⚖️ Compliance Agent", value=True)
        run_archive = st.checkbox("🔍 Archive Agent", value=True)
        run_social = st.checkbox("📱 Social Publishing", value=True)
        run_localization = st.checkbox("🌍 Localization", value=True)
        run_rights = st.checkbox("📜 Rights Agent", value=True)
        run_trending = st.checkbox("📈 Trending Agent", value=True)
        st.markdown("*Future-Ready 6 Agents:*")
        run_deepfake = st.checkbox("🕵️ Deepfake Detection", value=True)
        run_fact_check = st.checkbox("✅ Live Fact-Check", value=True)
        run_audience = st.checkbox("👥 Audience Intelligence", value=True)
        run_production = st.checkbox("🎬 AI Production Director", value=True)
        run_brand_safety = st.checkbox("🛡️ Brand Safety", value=True)
        run_carbon = st.checkbox("🌿 Carbon Intelligence", value=True)

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
        if run_deepfake:
            agents_to_run.append({"name": "Deepfake Detection", "icon": "🕵️", "steps": ["C2PA provenance check", "Audio forensics", "Video forensics", "Generating verdict"]})
        if run_fact_check:
            agents_to_run.append({"name": "Live Fact-Check", "icon": "✅", "steps": ["Extracting claims", "Querying databases", "Cross-referencing", "Generating verdicts"]})
        if run_audience:
            agents_to_run.append({"name": "Audience Intelligence", "icon": "👥", "steps": ["Analyzing demographics", "Predicting retention", "Detecting drop-offs", "Generating insights"]})
        if run_production:
            agents_to_run.append({"name": "AI Production Director", "icon": "🎥", "steps": ["Planning shots", "Generating lower-thirds", "Optimizing rundown", "Break strategy"]})
        if run_brand_safety:
            agents_to_run.append({"name": "Brand Safety", "icon": "🛡️", "steps": ["GARM scanning", "IAB categorizing", "Checking advertisers", "CPM optimization"]})
        if run_carbon:
            agents_to_run.append({"name": "Carbon Intelligence", "icon": "🌿", "steps": ["Calculating energy", "Scope 1/2/3 analysis", "ESG scoring", "Generating report"]})

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

        # Sequential agent pipeline — each agent completes before the next starts
        import time as _time
        import random as _rand
        total_steps = sum(len(a['steps']) for a in agents_to_run)
        completed_steps = 0

        for i, agent in enumerate(agents_to_run):
            # Mark agent as active (orange)
            agent_containers[agent['name']].markdown(f"""
            <div style="background: #1e293b; padding: 12px; border-radius: 8px; margin-bottom: 8px; border-left: 3px solid #f59e0b;">
                <strong>{agent['icon']} {agent['name']}</strong><br/>
                <span style="color: #f59e0b;">⚡ Starting...</span>
            </div>
            """, unsafe_allow_html=True)

            for step_num, step_text in enumerate(agent['steps']):
                agent_containers[agent['name']].markdown(f"""
                <div style="background: #1e293b; padding: 12px; border-radius: 8px; margin-bottom: 8px; border-left: 3px solid #f59e0b;">
                    <strong>{agent['icon']} {agent['name']}</strong><br/>
                    <span style="color: #f59e0b;">🔄 {step_text}...</span>
                </div>
                """, unsafe_allow_html=True)
                completed_steps += 1
                overall_progress.progress(completed_steps / total_steps, f"🔄 {agent['name']}: {step_text}...")
                _time.sleep(_rand.uniform(0.15, 0.55))

            # Mark agent complete (green)
            agent_containers[agent['name']].markdown(f"""
            <div style="background: #1e293b; padding: 12px; border-radius: 8px; margin-bottom: 8px; border-left: 3px solid #22c55e;">
                <strong>{agent['icon']} {agent['name']}</strong><br/>
                <span style="color: #22c55e;">✅ Complete</span>
            </div>
            """, unsafe_allow_html=True)

        overall_progress.progress(1.0, "✅ All 14 agents complete!")
        _time.sleep(0.4)

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
            active_deepfake = SAMPLE_DEEPFAKE_RESULT
            active_fact_check = SAMPLE_FACT_CHECK_CLAIMS
            active_audience = SAMPLE_AUDIENCE_DATA
            active_production = SAMPLE_PRODUCTION_DATA
            active_brand_safety = SAMPLE_BRAND_SAFETY_DATA
            active_carbon = SAMPLE_CARBON_DATA
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
            active_deepfake = DEMO_DEEPFAKE_RESULT
            active_fact_check = DEMO_FACT_CHECK_CLAIMS
            active_audience = DEMO_AUDIENCE_DATA
            active_production = DEMO_PRODUCTION_DATA
            active_brand_safety = DEMO_BRAND_SAFETY_DATA
            active_carbon = DEMO_CARBON_DATA
            content_title = "Morning News Broadcast"
            content_duration = "4:02:15"

        # Summary Metrics Row 1 — Original 8 agents
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        col1.metric("Captions", f"{len(active_captions)} segments", f"{sum(c['confidence'] for c in active_captions)/len(active_captions)*100:.1f}% accuracy")
        col2.metric("Viral Clips", f"{len(active_viral)} found", f"Top: {max(m['score'] for m in active_viral)*100:.0f}%")
        col3.metric("Compliance", f"{len(active_compliance)} items", "Reviewed")
        col4.metric("Social Posts", f"{len(active_social)} ready", "5 platforms")
        col5.metric("Translations", f"{len(target_languages)} languages", "95% quality")
        col6.metric("Trending Match", f"{len(active_trends)} topics", f"{active_trends[0]['topic']}" if active_trends else "N/A")

        # Summary Metrics Row 2 — Future-Ready 6 agents
        col7, col8, col9, col10, col11, col12 = st.columns(6)
        _df_verdict = active_deepfake.get("verdict", "N/A")
        _df_risk = active_deepfake.get("risk_score", 0)
        col7.metric("Deepfake", _df_verdict, f"Risk: {_df_risk:.3f}")
        col8.metric("Fact-Check", f"{len(active_fact_check)} claims", "Analyzed" if active_fact_check else "N/A")
        col9.metric("Audience", f"{active_audience.get('current_viewers', 847000):,}", active_audience.get("viewer_trend", "+18K/min"))
        col10.metric("Production", f"{len(active_production.get('shots', []))} shots", "planned")
        col11.metric("Brand Safety", f"{active_brand_safety.get('overall_score', 96)}/100", active_brand_safety.get("level", "Premium Safe"))
        col12.metric("Carbon", f"{active_carbon.get('total_co2e_kg', 12.4)} kg CO₂e", f"ESG: {active_carbon.get('esg_score', 81)}/100")

        # Summary Metrics Row 3 — Phase 1 Pipeline agents
        col13, col14, col15, col16, col17 = st.columns(5)
        col13.metric("Ingest Jobs", "3 complete", "0 errors")
        col14.metric("Signal Quality", "✅ All Clear", "EBU R128 −22.8 LUFS")
        col15.metric("Playout", "12 slots", "Next: 18:00 News")
        col16.metric("OTT Streams", "5 profiles live", "147K viewers")
        col17.metric("Newsroom", "8 stories", "2 wires pending")

        st.divider()

        # Tabbed Results
        (tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10,
         tab11, tab12, tab13, tab14, tab15, tab16, tab17, tab18, tab19) = st.tabs([
            "📝 Captions", "🎬 Viral Clips", "⚖️ Compliance", "🔍 Archive",
            "📱 Social", "🌍 Translations", "📜 Rights", "📈 Trending",
            "🕵️ Deepfake", "✅ Fact-Check", "👥 Audience", "🎥 Production", "🛡️ Brand Safety", "🌿 Carbon",
            "📥 Ingest", "📡 Signal", "📋 Playout", "🌐 OTT", "📰 Newsroom",
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
            import json as _json
            compliance_report = _json.dumps(active_compliance, indent=2)
            st.download_button("📥 Download Compliance Report (JSON)", compliance_report,
                "compliance_report.json", "application/json", use_container_width=True, key="dl_compliance_allinone")

        with tab4:
            st.markdown("**Archive Metadata Generated**")
            st.json(active_archive)
            import json as _json
            st.download_button("📥 Download Archive Metadata (JSON)", _json.dumps(active_archive, indent=2),
                "archive_metadata.json", "application/json", use_container_width=True, key="dl_archive_allinone")
            st.button("📤 Send to MAM System", use_container_width=True, key="mam_sync_allinone")

        with tab5:
            st.markdown(f"**Social Posts Generated** - {len(active_social)} posts across 5 platforms")
            for post in active_social:
                with st.expander(f"**{post['platform']}** - {post['char_count']} chars | Best time: {post['best_time']}"):
                    st.text_area("Post Content", post['content'], height=120, key=f"social_{post['platform']}")
                    st.caption(f"📊 Predicted engagement: {post['predicted_engagement']}")
            import csv, io as _io
            _buf = _io.StringIO()
            _writer = csv.DictWriter(_buf, fieldnames=["platform", "content", "char_count", "best_time", "predicted_engagement"])
            _writer.writeheader()
            _writer.writerows(active_social)
            col1, col2, col3 = st.columns(3)
            col1.button("📤 Post All Now", type="primary", use_container_width=True, key="post_all_allinone")
            col2.button("🕐 Schedule All", use_container_width=True, key="schedule_all_allinone")
            col3.download_button("📥 Export Social Posts (CSV)", _buf.getvalue(),
                "social_posts.csv", "text/csv", use_container_width=True, key="dl_social_allinone")

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

        with tab9:
            st.markdown("**Deepfake Detection Report**")
            verdict = active_deepfake.get("verdict", "N/A")
            risk = active_deepfake.get("risk_score", 0)
            broadcast_safe = active_deepfake.get("broadcast_safe", True)
            verdict_color = "#22c55e" if verdict == "AUTHENTIC" else "#ef4444"
            st.markdown(f"""
            <div style="background: #1e293b; padding: 16px; border-radius: 10px; border-left: 4px solid {verdict_color};">
            <h3 style="color: {verdict_color}; margin:0;">{'✅' if verdict == 'AUTHENTIC' else '🚨'} Verdict: {verdict}</h3>
            <p style="color: #94a3b8; margin: 8px 0 0 0;">Risk Score: {risk:.3f} | Broadcast Safe: {'Yes' if broadcast_safe else 'No'}</p>
            </div>
            """, unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            col1.metric("Audio Authenticity", f"{active_deepfake.get('audio_authenticity', 0.971)*100:.1f}%")
            col2.metric("Video Authenticity", f"{active_deepfake.get('video_authenticity', 0.964)*100:.1f}%")
            col3.metric("Metadata Trust", f"{active_deepfake.get('metadata_trust', 0.989)*100:.1f}%")
            if broadcast_safe:
                st.success("✅ C2PA provenance chain verified. No synthetic media indicators detected.")
            else:
                st.error("🚫 HOLD FOR BROADCAST — Suspicious synthetic media indicators detected. Verify before airing.")
            _df_report = (
                f"DEEPFAKE FORENSIC REPORT\n{'='*50}\n"
                f"Verdict: {verdict}\nRisk Score: {risk:.3f}\nBroadcast Safe: {'Yes' if broadcast_safe else 'No'}\n\n"
                f"Audio Authenticity: {active_deepfake.get('audio_authenticity', 0)*100:.1f}%\n"
                f"Video Authenticity: {active_deepfake.get('video_authenticity', 0)*100:.1f}%\n"
                f"Metadata Trust: {active_deepfake.get('metadata_trust', 0)*100:.1f}%\n\n"
                f"Recommendations:\n" +
                "\n".join(f"  {p}: {a}" for p, a in active_deepfake.get("recommendations", []))
            )
            st.download_button("📥 Download Forensic Report", _df_report,
                "deepfake_report.txt", "text/plain", use_container_width=True, key="dl_deepfake_allinone")

        with tab10:
            st.markdown("**Live Fact-Check Results**")
            if active_fact_check:
                for claim in active_fact_check:
                    st.markdown(f"""
                    <div style="background: #1e293b; padding: 10px 14px; border-radius: 8px; margin: 6px 0; border-left: 4px solid {claim.get('color','#6366f1')};">
                    <span style="color:{claim.get('color','#6366f1')}; font-weight:bold;">{claim.get('icon','ℹ️')} {claim.get('verdict','N/A')}</span>
                    <span style="color:#94a3b8; float:right;">{claim.get('confidence',0)*100:.0f}% confidence</span><br/>
                    <span style="color:#e2e8f0;">{claim.get('claim','')}</span><br/>
                    <small style="color:#64748b;">Source: {claim.get('source','')}</small>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Fact-check results will appear here after running the analysis with demo video selected.")
            if active_fact_check:
                import json as _json
                st.download_button("📥 Download Fact-Check Report (JSON)", _json.dumps(active_fact_check, indent=2),
                    "fact_check_report.json", "application/json", use_container_width=True, key="dl_factcheck_allinone")

        with tab11:
            st.markdown("**Audience Intelligence**")
            col1, col2, col3 = st.columns(3)
            col1.metric("Current Viewers", f"{active_audience.get('current_viewers', 847000):,}", active_audience.get("viewer_trend", "+18K/min"))
            col2.metric("Predicted Peak", f"{active_audience.get('predicted_peak', 1240000):,}", f"in {active_audience.get('peak_in_min', 6)} min")
            col3.metric("Retention Risk", f"{active_audience.get('retention_risk', 12)}%", "Low")
            st.markdown("**Demographics:**")
            for age, pct in active_audience.get("demographics", {}).items():
                st.progress(pct / 100, text=f"{age}: {pct}%")
            import json as _json
            st.download_button("📥 Download Audience Report (JSON)", _json.dumps(active_audience, indent=2),
                "audience_intelligence.json", "application/json", use_container_width=True, key="dl_audience_allinone")

        with tab12:
            st.markdown("**AI Production Director**")
            _shots = active_production.get("shots", [])
            _lt = active_production.get("lower_thirds", [])
            if _shots:
                st.markdown(f"**Camera Shot Plan** — {len(_shots)} shots")
                import pandas as pd
                df_shots = pd.DataFrame([{"Shot": s["shot"], "Camera": s["camera"], "Type": s["type"], "Use": s["use"], "Duration": s["duration"]} for s in _shots])
                st.dataframe(df_shots, use_container_width=True, hide_index=True)
            if _lt:
                st.markdown(f"**Lower Thirds** — {len(_lt)} graphics queued")
                for lt in _lt:
                    st.markdown(f"- **{lt['line1']}** / {lt['line2']} — *{lt['trigger']}*")
            else:
                st.info("Production plan will appear here after running with demo video selected.")
            if _shots:
                import json as _json
                st.download_button("📥 Download Production Plan (JSON)", _json.dumps(active_production, indent=2),
                    "production_plan.json", "application/json", use_container_width=True, key="dl_production_allinone")

        with tab13:
            st.markdown("**Brand Safety Report**")
            bs_score = active_brand_safety.get("overall_score", 96)
            bs_level = active_brand_safety.get("level", "Premium Safe")
            bs_color = active_brand_safety.get("level_color", "#22c55e")
            st.markdown(f"""
            <div style="background: #1e293b; padding: 14px; border-radius: 10px; border-left: 4px solid {bs_color};">
            <h3 style="color: {bs_color}; margin:0;">🛡️ {bs_level} — {bs_score}/100</h3>
            <p style="color: #94a3b8; margin: 8px 0 0 0;">
            Active Advertisers: {active_brand_safety.get('active_advertisers', 42)} |
            Blocked: {active_brand_safety.get('blocked_advertisers', 0)} |
            CPM: ${active_brand_safety.get('current_cpm', 42.50)} → ${active_brand_safety.get('optimized_cpm', 61.80)}
            </p>
            </div>
            """, unsafe_allow_html=True)
            _garm = active_brand_safety.get("garm_flags", [])
            if _garm:
                st.markdown("**GARM Compliance:**")
                cols_g = st.columns(2)
                for i, (cat, level, icon) in enumerate(_garm):
                    cols_g[i % 2].markdown(f"{icon} **{cat}**: {level}")
            import json as _json
            st.download_button("📥 Download Brand Safety Report (JSON)", _json.dumps(active_brand_safety, indent=2),
                "brand_safety_report.json", "application/json", use_container_width=True, key="dl_brandsafety_allinone")

        with tab14:
            st.markdown("**Carbon Intelligence & ESG**")
            col1, col2, col3 = st.columns(3)
            col1.metric("Total CO₂e", f"{active_carbon.get('total_co2e_kg', 12.4)} kg", f"{active_carbon.get('vs_industry_avg_pct', -28)}% vs avg")
            col2.metric("Renewable Mix", f"{active_carbon.get('renewable_pct', 34)}%", f"Grid: {100 - active_carbon.get('renewable_pct', 34)}% fossil")
            col3.metric("ESG Score", f"{active_carbon.get('esg_score', 81)}/100", "Rating: A")
            st.markdown("**Scope Breakdown:**")
            _co2 = active_carbon.get("total_co2e_kg", 12.4)
            st.progress(active_carbon.get("scope1_kg", 1.8) / _co2, text=f"Scope 1 (Direct): {active_carbon.get('scope1_kg', 1.8)} kg")
            st.progress(active_carbon.get("scope2_kg", 6.9) / _co2, text=f"Scope 2 (Grid electricity): {active_carbon.get('scope2_kg', 6.9)} kg")
            st.progress(active_carbon.get("scope3_kg", 3.7) / _co2, text=f"Scope 3 (Supply chain): {active_carbon.get('scope3_kg', 3.7)} kg")
            standards = ", ".join(active_carbon.get("esg_report_standards", ["GRI 305", "TCFD", "SBTi"]))
            st.success(f"📋 Frameworks Aligned: {standards}")
            _co2_val = active_carbon.get("total_co2e_kg", 12.4)
            _esg_val = active_carbon.get("esg_score", 81)
            _ren_val = active_carbon.get("renewable_pct", 34)
            _esg_text = (
                f"ESG CARBON INTELLIGENCE REPORT\n{'='*50}\n"
                f"Report Period: {datetime.now().strftime('%B %Y')}\n\n"
                f"Total CO2e: {_co2_val} kg\n"
                f"ESG Score: {_esg_val}/100\n"
                f"Renewable Mix: {_ren_val}%\n"
                f"Scope 1 (Direct): {active_carbon.get('scope1_kg', 0)} kg\n"
                f"Scope 2 (Grid): {active_carbon.get('scope2_kg', 0)} kg\n"
                f"Scope 3 (Supply chain): {active_carbon.get('scope3_kg', 0)} kg\n\n"
                f"Frameworks Aligned: {standards}\n"
            )
            import json as _json
            st.download_button("📥 Download ESG Report (JSON)", _json.dumps(active_carbon, indent=2),
                "esg_carbon_report.json", "application/json", use_container_width=True, key="dl_carbon_allinone")

        with tab15:
            st.markdown("**Ingest + Transcode — Pipeline Status**")
            col1, col2, col3 = st.columns(3)
            col1.metric("Jobs Today", "3 complete", "0 errors")
            col2.metric("Avg Transcode Time", "7m 24s", "4K HDR: 18m 12s")
            col3.metric("Output Profiles", "6 configured", "Cloud: AWS MediaConvert")
            jobs = [
                {"id": "INJ-001", "file": "wkrn_morningnews_raw.mxf",   "status": "✅ Complete", "duration": "4:02:15", "outputs": "Broadcast HD, OTT HLS, Proxy, Thumbnail"},
                {"id": "INJ-002", "file": "wkrn_sportshighlight_raw.mp4","status": "✅ Complete", "duration": "0:45:30", "outputs": "Broadcast HD, OTT HLS, Web MP4"},
                {"id": "INJ-003", "file": "wkrn_weather_segment_raw.mxf","status": "⏳ In Progress","duration": "0:12:00", "outputs": "Broadcast HD, Proxy (running)"},
            ]
            for j in jobs:
                st.markdown(f"""
                <div style="background:#1e293b;padding:10px 14px;border-radius:8px;margin:6px 0;border-left:3px solid #6366f1;">
                <strong style="color:#e2e8f0;">{j['id']}</strong> — <span style="color:#94a3b8;">{j['file']}</span>
                &nbsp;&nbsp;<span style="color:#22c55e;">{j['status']}</span><br>
                <small style="color:#64748b;">Duration: {j['duration']} &nbsp;|&nbsp; Outputs: {j['outputs']}</small>
                </div>""", unsafe_allow_html=True)

        with tab16:
            st.markdown("**Signal Quality Monitor — Live Broadcast**")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Loudness", "−22.8 LUFS", "✅ Target −23 ±1")
            col2.metric("True Peak", "−1.4 dBTP", "✅ < −1.0 limit")
            col3.metric("Black Frames", "0 detected", "✅ Clear")
            col4.metric("Caption Sync", "±12ms", "✅ < 500ms")
            st.success("📡 WKRN-HD: All Clear | EBU R128 + ATSC A/85 compliant")
            alerts = [
                ("09:23:45", "⚠️ WARNING", "Commercial segment +8 LUFS above program level", "#f59e0b"),
                ("08:15:12", "🔴 CRITICAL", "3.2s black frame during program break — NOC alerted", "#ef4444"),
            ]
            st.markdown("**Alert History (Last 24h):**")
            for ts, sev, msg, col in alerts:
                st.markdown(f"""
                <div style="background:rgba({','.join(['239,68,68' if col=='#ef4444' else '245,158,11,0.1' for _ in [1]])},0.1);
                border-left:3px solid {col};padding:8px 12px;border-radius:6px;margin:4px 0;">
                <small style="color:#94a3b8;">{ts}</small> &nbsp; <strong>{sev}</strong><br>
                <span style="color:#e2e8f0;font-size:13px;">{msg}</span></div>""", unsafe_allow_html=True)

        with tab17:
            st.markdown("**Playout Scheduling — Today's Rundown**")
            schedule = [
                ("06:00", "09:00", "WKRN Morning News LIVE", "news_live", "✅ Aired"),
                ("09:00", "10:00", "Today Show (NBC)",        "network",   "✅ Aired"),
                ("10:00", "12:00", "The Price Is Right",      "syndicated","✅ Aired"),
                ("12:00", "12:30", "WKRN News at Noon",       "news_live", "✅ Aired"),
                ("18:00", "18:30", "WKRN News at 6",          "news_live", "🔵 Scheduled"),
                ("22:00", "22:30", "WKRN News at 10",         "news_live", "🔵 Scheduled"),
                ("22:30", "23:30", "Late Show (CBS)",          "network",   "🔵 Scheduled"),
            ]
            for s, e, title, t, status in schedule:
                type_color = "#6366f1" if "news" in t else "#0891b2"
                st.markdown(f"""
                <div style="display:flex;gap:12px;align-items:center;padding:7px 12px;
                background:#1e293b;border-radius:6px;margin:4px 0;border-left:3px solid {type_color};">
                <span style="color:#94a3b8;font-family:monospace;min-width:110px;">{s} – {e}</span>
                <span style="color:#e2e8f0;flex:1;">{title}</span>
                <span style="color:#64748b;font-size:12px;">{status}</span></div>""", unsafe_allow_html=True)

        with tab18:
            st.markdown("**OTT Distribution — Live Stream Health**")
            col1, col2, col3 = st.columns(3)
            col1.metric("Active Streams", "5 profiles", "All healthy")
            col2.metric("Total Viewers", "147,234", "+2.3K/min")
            col3.metric("CDN", "CloudFront", "99.98% uptime")
            abr = [
                ("4K HDR",   "25 Mbps",  12847,  "✅"),
                ("1080p60",  "8 Mbps",   89234,  "✅"),
                ("720p",     "4 Mbps",   31204,  "✅"),
                ("480p",     "2 Mbps",   10891,  "✅"),
                ("Audio Only","128 kbps", 3058,  "✅"),
            ]
            for profile, br, viewers, health in abr:
                st.markdown(f"""
                <div style="display:flex;gap:12px;align-items:center;padding:6px 12px;
                background:#1e293b;border-radius:6px;margin:3px 0;">
                <span style="color:#e2e8f0;min-width:90px;font-weight:600;">{profile}</span>
                <span style="color:#94a3b8;min-width:80px;">{br}</span>
                <span style="color:#22c55e;flex:1;">{viewers:,} viewers</span>
                <span>{health}</span></div>""", unsafe_allow_html=True)

        with tab19:
            st.markdown("**Newsroom Integration — iNews Rundown**")
            col1, col2 = st.columns(2)
            col1.metric("Stories Ready", "6 / 8", "2 editing")
            col2.metric("Wire Stories", "14 new", "AP: 8, Reuters: 4, AFP: 2")
            rundown = [
                ("FIRE-DOWNTOWN", "Warehouse Fire Nashville",    "Jake Thompson",   "2:30", "✅ Ready", "LEAD"),
                ("COUNCIL-VOTE",  "City Council Budget Vote",    "Maria Sanchez",   "1:45", "✅ Ready", "2ND"),
                ("WEATHER-STORM", "Severe Storm Watch Tonight",  "Weather Team",    "1:15", "✅ Ready", "3RD"),
                ("ECON-REPORT",   "Fed Rate Decision Analysis",  "David Park",      "2:00", "⏳ Editing","4TH"),
                ("SPORTS-WIN",    "Titans Win Playoff Opener",   "Sports Desk",     "1:30", "✅ Ready", "5TH"),
                ("TRAFFIC-ISSUE", "I-24 Closure Update",         "Traffic Desk",    "0:45", "✅ Ready", "KICKER"),
            ]
            for slug, title, reporter, dur, status, pos in rundown:
                status_color = "#22c55e" if "Ready" in status else "#f59e0b"
                pos_color = "#ef4444" if pos == "LEAD" else "#6366f1"
                st.markdown(f"""
                <div style="display:flex;gap:10px;align-items:center;padding:7px 12px;
                background:#1e293b;border-radius:6px;margin:4px 0;">
                <span style="background:{pos_color};color:#fff;padding:2px 8px;border-radius:4px;
                font-size:11px;font-weight:700;min-width:58px;text-align:center;">{pos}</span>
                <span style="color:#94a3b8;font-family:monospace;font-size:12px;min-width:90px;">{slug}</span>
                <span style="color:#e2e8f0;flex:1;">{title}</span>
                <span style="color:#94a3b8;font-size:12px;min-width:55px;">{reporter.split()[0]}</span>
                <span style="color:#64748b;min-width:35px;">{dur}</span>
                <span style="color:{status_color};font-size:13px;">{status}</span></div>""",
                unsafe_allow_html=True)

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

        # Use SAMPLE_ data when demo video available, DEMO_ data on cloud (no video)
        if DEMO_SAMPLE_AVAILABLE:
            df_result = SAMPLE_DEEPFAKE_RESULT
        else:
            df_result = DEMO_DEEPFAKE_RESULT

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

        _df_forensic = (
            f"DEEPFAKE FORENSIC REPORT\n{'='*50}\n"
            f"Verdict: {verdict}\nRisk Score: {risk_score:.3f}\nBroadcast Safe: {'Yes' if broadcast_safe else 'No'}\n\n"
            f"Audio Authenticity: {df_result['audio_authenticity']:.3f}\n"
            f"Video Authenticity: {df_result['video_authenticity']:.3f}\n"
            f"Metadata Trust: {df_result['metadata_trust']:.3f}\n\n"
            f"Provenance:\n" + "\n".join(f"  {s}" for s in df_result.get("provenance", [])) +
            f"\n\nRecommendations:\n" + "\n".join(f"  {p}: {a}" for p, a in df_result.get("recommendations", []))
        )
        st.download_button("📥 Download Forensic Report", _df_forensic,
            "deepfake_forensic_report.txt", "text/plain", use_container_width=True, key="dl_deepfake_page")


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

        claims_data = SAMPLE_FACT_CHECK_CLAIMS if DEMO_SAMPLE_AVAILABLE else DEMO_FACT_CHECK_CLAIMS

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
        import json as _json
        st.download_button("📥 Download Fact-Check Report (JSON)", _json.dumps(claims_data, indent=2),
            "fact_check_report.json", "application/json", use_container_width=True, key="dl_factcheck_page")


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
        _aud = SAMPLE_AUDIENCE_DATA if DEMO_SAMPLE_AVAILABLE else DEMO_AUDIENCE_DATA
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

        aud = SAMPLE_AUDIENCE_DATA if DEMO_SAMPLE_AVAILABLE else DEMO_AUDIENCE_DATA

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

        import json as _json
        st.download_button("📥 Download Audience Report (JSON)", _json.dumps(aud, indent=2),
            "audience_intelligence.json", "application/json", use_container_width=True, key="dl_audience_page")


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
        pd_data = SAMPLE_PRODUCTION_DATA if DEMO_SAMPLE_AVAILABLE else DEMO_PRODUCTION_DATA
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

        import json as _json
        st.download_button("📥 Download Production Plan (JSON)", _json.dumps(pd_data, indent=2),
            "production_plan.json", "application/json", use_container_width=True, key="dl_production_page")


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

    _bs = SAMPLE_BRAND_SAFETY_DATA if DEMO_SAMPLE_AVAILABLE else DEMO_BRAND_SAFETY_DATA
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

        bs = SAMPLE_BRAND_SAFETY_DATA if DEMO_SAMPLE_AVAILABLE else DEMO_BRAND_SAFETY_DATA
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

        import json as _json
        st.download_button("📥 Download Brand Safety Report (JSON)", _json.dumps(bs, indent=2),
            "brand_safety_report.json", "application/json", use_container_width=True, key="dl_brandsafety_page")


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
        c = SAMPLE_CARBON_DATA if DEMO_SAMPLE_AVAILABLE else DEMO_CARBON_DATA

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
            _esg_dl_text = (
                f"ESG CARBON INTELLIGENCE REPORT\n{'='*50}\n"
                f"Report Period: {datetime.now().strftime('%B %Y')}\n\n"
                f"ESG Score: {esg_score}/100 (Rating: {rating})\n"
                f"Total CO2e: {co2_today} kg\n"
                f"Renewable Mix: {renewable_pct}%\n"
                f"Scope 1 (Direct): {scope1} kg\n"
                f"Scope 2 (Grid electricity): {scope2} kg\n"
                f"Scope 3 (Supply chain): {scope3} kg\n\n"
                f"Carbon Intensity: {_carbon_int} {_int_unit}\n"
                f"Frameworks Aligned: {_standards}\n"
                f"Advertiser ESG Compliant: {'Yes' if esg_score >= 60 else 'No'}\n"
                f"Next Audit: {(datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')}\n"
                f"\nNet Zero Target: 2035\n"
            )
            import json as _json
            col_e1, col_e2 = st.columns(2)
            col_e1.download_button("📥 Download ESG Report (TXT)", _esg_dl_text,
                "esg_carbon_report.txt", "text/plain", use_container_width=True, key="dl_carbon_page_txt")
            col_e2.download_button("📥 Download Carbon Data (JSON)", _json.dumps(c, indent=2),
                "carbon_data.json", "application/json", use_container_width=True, key="dl_carbon_page_json")


# ======================================================================
# PHASE 1 PIPELINE AGENTS (Broadcast Pipeline Gaps)
# ======================================================================

elif page == "📥 Ingest + Transcode":
    st.title("📥 Ingest + Transcode Agent")
    st.caption("Broadcast Pipeline — Automated Media Ingest | Multi-Profile Transcoding | MAM Integration | AWS MediaConvert")

    with st.expander("**Agent Capabilities** — Click to expand", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
            **Format Support**
            - MXF (XDCAM, P2, IMX)
            - ProRes 4444 / 422 HQ
            - H.264 / H.265 HEVC
            - DPX, DNxHD, RAW
            """)
        with col2:
            st.markdown("""
            **Output Profiles**
            - Broadcast HD (MXF 50 Mbps)
            - Broadcast 4K (MXF 150 Mbps)
            - OTT HLS (fMP4 ABR)
            - Proxy Edit (ProRes 422)
            - Web MP4 + Thumbnail
            """)
        with col3:
            st.markdown("""
            **Pipeline Steps**
            - NMOS IS-04 discovery
            - Checksum validation (MD5/SHA256)
            - Colour space conversion
            - LUFS / loudness normalise
            - MXF structural validation
            """)
        with col4:
            st.markdown("""
            **Integrations**
            - AWS MediaConvert (cloud)
            - FFmpeg (on-prem)
            - Harmonic Polaris MAM
            - Avid Interplay
            - Frame.io review link
            """)

    st.divider()

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f'<span class="realtime-indicator"></span> **Pipeline Active** — {datetime.now().strftime("%I:%M:%S %p")}', unsafe_allow_html=True)
    with col2:
        ingest_run = st.button("▶️ Simulate Ingest", type="primary", use_container_width=True)

    if ingest_run:
        steps = [
            {"icon": "📡", "text": "NMOS IS-04 discovery — locating source device"},
            {"icon": "✅", "text": "File validation — MD5 checksum OK (42.7 GB)"},
            {"icon": "🎨", "text": "Colour space: BT.709 → BT.2020 HDR conversion"},
            {"icon": "🔊", "text": "Loudness normalization — −22.8 LUFS (EBU R128)"},
            {"icon": "🎬", "text": "Transcoding: Broadcast HD (MXF H.264 50 Mbps)"},
            {"icon": "📺", "text": "Transcoding: OTT HLS (fMP4 8 Mbps ABR)"},
            {"icon": "🗂️", "text": "Transcoding: Proxy Edit (ProRes 422 HQ)"},
            {"icon": "🖼️", "text": "Generating thumbnails (10 keyframes)"},
            {"icon": "🏷️", "text": "Writing MXF metadata + archiving to MAM"},
        ]
        container = st.container()
        simulate_realtime_processing(steps, container)

    # Current jobs table
    st.subheader("Ingest Queue — Today")
    jobs_data = [
        {"ID": "INJ-001", "File": "wkrn_morningnews_raw.mxf",    "Duration": "4:02:15", "Size": "42.7 GB", "Status": "✅ Complete", "Outputs": 4, "Time": "7m 24s"},
        {"ID": "INJ-002", "File": "wkrn_sportshighlight_raw.mp4", "Duration": "0:45:30", "Size": "8.2 GB",  "Status": "✅ Complete", "Outputs": 3, "Time": "3m 11s"},
        {"ID": "INJ-003", "File": "wkrn_weather_segment_raw.mxf", "Duration": "0:12:00", "Size": "2.1 GB",  "Status": "⏳ Running",  "Outputs": 2, "Time": "1m 48s..."},
    ]
    for j in jobs_data:
        status_col = "#22c55e" if "Complete" in j["Status"] else "#f59e0b"
        st.markdown(f"""
        <div style="background:#1e293b;padding:12px 16px;border-radius:8px;margin:6px 0;
        display:flex;gap:16px;align-items:center;border-left:3px solid #6366f1;">
        <span style="color:#6366f1;font-family:monospace;font-weight:700;min-width:70px;">{j['ID']}</span>
        <span style="color:#e2e8f0;flex:2;">{j['File']}</span>
        <span style="color:#94a3b8;min-width:60px;">{j['Duration']}</span>
        <span style="color:#94a3b8;min-width:60px;">{j['Size']}</span>
        <span style="color:#94a3b8;min-width:55px;">{j['Outputs']} outputs</span>
        <span style="color:#94a3b8;min-width:70px;">{j['Time']}</span>
        <span style="color:{status_col};">{j['Status']}</span>
        </div>""", unsafe_allow_html=True)

    st.divider()
    st.subheader("Output Profile Specifications")
    profiles = [
        ("Broadcast HD",   "MXF",   "H.264",  "50 Mbps",  "1920×1080i 50",  "PCM 48kHz", "NLE + Playout"),
        ("Broadcast 4K",   "MXF",   "H.265",  "150 Mbps", "3840×2160p 50",  "PCM 48kHz", "4K Playout"),
        ("OTT HLS",        "fMP4",  "H.264",  "8 Mbps",   "1080p + ABR",    "AAC 192k",  "Streaming CDN"),
        ("Proxy Edit",     "MOV",   "ProRes", "45 Mbps",  "1920×1080p 25",  "PCM 48kHz", "NLE Editing"),
        ("Web MP4",        "MP4",   "H.264",  "4 Mbps",   "1280×720p 25",   "AAC 128k",  "Web / Social"),
        ("Thumbnail",      "JPEG",  "—",      "N/A",      "1920×1080",      "—",          "Archive / CMS"),
    ]
    cols_h = st.columns([2, 1, 1, 1, 2, 1, 2])
    for h, label in zip(cols_h, ["Profile", "Container", "Codec", "Bitrate", "Resolution", "Audio", "Use Case"]):
        h.markdown(f"**{label}**")
    for p in profiles:
        cols_r = st.columns([2, 1, 1, 1, 2, 1, 2])
        for col, val in zip(cols_r, p):
            col.caption(val)


elif page == "📡 Signal Quality":
    st.title("📡 Signal Quality Agent")
    st.caption("EBU R128 / ATSC A/85 Loudness | Black & Freeze Frame Detection | CEA-608/708 Caption Monitoring | 24/7 NOC Alerts")

    with st.expander("**Agent Capabilities** — Click to expand", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
            **Audio (EBU R128)**
            - Integrated loudness (I)
            - True peak (TP) limiter
            - Loudness range (LRA)
            - Momentary / Short-term
            - CALM Act compliance
            """)
        with col2:
            st.markdown("""
            **Video Analysis**
            - Black frame detection
            - Freeze frame detection
            - Bitrate monitoring
            - Motion vector analysis
            - HDR peak luminance
            """)
        with col3:
            st.markdown("""
            **Caption QC**
            - CEA-608 / CEA-708
            - Sync drift alerting
            - Missing caption detect
            - Language track count
            - EIA-608 line 21 verify
            """)
        with col4:
            st.markdown("""
            **Alerting**
            - NOC Slack/Teams alert
            - Auto-hold on critical
            - Email escalation
            - Dashboard notification
            - Log to compliance DB
            """)

    st.divider()

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f'<span class="realtime-indicator"></span> **Live Monitoring** — {datetime.now().strftime("%I:%M:%S %p")}', unsafe_allow_html=True)
    with col2:
        if st.button("🔄 Re-check Now", use_container_width=True):
            st.rerun()

    # Live metrics
    st.subheader("WKRN-HD — Current Signal Status")
    st.success("✅ ALL CLEAR — Signal within broadcast spec")

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Integrated Loudness", "−22.8 LUFS", "✅ −23 ±1")
    col2.metric("True Peak", "−1.4 dBTP", "✅ < −1.0")
    col3.metric("LRA", "8.2 LU", "✅ < 18 LU")
    col4.metric("Black Frames", "0", "✅ Clear")
    col5.metric("Freeze Frames", "0", "✅ Clear")
    col6.metric("Caption Sync", "±12ms", "✅ < 500ms")

    # Loudness timeline
    st.subheader("Loudness Timeline (Last 2 Hours)")
    loudness_samples = [-22.1, -23.4, -22.8, -23.1, -22.5, -23.8, -22.9, -23.2, -22.6, -23.0,
                        -15.2, -22.8, -23.1, -22.7, -23.3, -22.9, -23.0, -22.4, -23.1, -22.8]
    import json as _sq_json
    st.line_chart({"Loudness (LUFS)": loudness_samples, "Target (−23)": [-23.0] * 20, "Upper Limit (−22)": [-22.0] * 20})
    st.caption("⚠️ Spike at sample 11 = commercial segment loudness violation (auto-logged)")

    # Alert history
    st.subheader("Alert History — Last 24 Hours")
    alerts_sq = [
        ("09:23:45", "⚠️ WARNING",  "WKRN-HD", "Loudness",     "Commercial +8 LUFS above program",     "Logged to compliance DB"),
        ("08:15:12", "🔴 CRITICAL", "WKRN-SD", "Black Frame",  "3.2s black frame during program break", "NOC alerted via Slack"),
        ("06:01:00", "ℹ️ INFO",     "WKRN-HD", "Caption",      "Caption track restarted after reboot",  "Auto-recovered"),
    ]
    for ts, sev, ch, typ, msg, action in alerts_sq:
        sev_color = "#ef4444" if "CRITICAL" in sev else "#f59e0b" if "WARNING" in sev else "#3b82f6"
        st.markdown(f"""
        <div style="background:rgba(30,35,41,1);padding:10px 14px;border-radius:8px;margin:5px 0;
        border-left:3px solid {sev_color};display:flex;gap:12px;align-items:center;flex-wrap:wrap;">
        <span style="color:#94a3b8;font-family:monospace;min-width:65px;">{ts}</span>
        <span style="font-weight:700;color:{sev_color};min-width:90px;">{sev}</span>
        <span style="color:#6366f1;min-width:70px;">{ch}</span>
        <span style="color:#94a3b8;min-width:75px;">[{typ}]</span>
        <span style="color:#e2e8f0;flex:1;">{msg}</span>
        <span style="color:#22c55e;font-size:12px;">{action}</span>
        </div>""", unsafe_allow_html=True)


elif page == "📋 Playout Scheduling":
    st.title("📋 Playout Scheduling Agent")
    st.caption("Harmonic Polaris / GV Maestro Integration | 24h Rundown | SCTE-35 Ad Cue Insertion | Auto-Fill on Gaps")

    with st.expander("**Agent Capabilities** — Click to expand", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
            **Schedule Management**
            - 24h rundown import/export
            - AS-11 / MXF playlist
            - Secondary event triggers
            - Pre-roll / post-roll
            - Filler detection + fill
            """)
        with col2:
            st.markdown("""
            **SCTE-35 Cuing**
            - Ad break insertion points
            - Splice_insert commands
            - Segmentation descriptors
            - Out/In timing precision
            - DAI compatibility
            """)
        with col3:
            st.markdown("""
            **Automation Systems**
            - Harmonic Polaris REST API
            - GV Maestro integration
            - Ross Overdrive support
            - Vizrt overlay triggers
            - Graphics event sync
            """)
        with col4:
            st.markdown("""
            **Intelligence**
            - Gap detection + alert
            - Conflict resolution
            - Rating compliance check
            - CPI / rights window verify
            - On-air confidence monitor
            """)

    st.divider()

    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.markdown(f'<span class="realtime-indicator"></span> **Live Schedule** — {datetime.now().strftime("%I:%M:%S %p")}', unsafe_allow_html=True)
    with col2:
        if st.button("🔄 Sync from Polaris", use_container_width=True):
            with st.spinner("Syncing from Harmonic Polaris..."):
                time.sleep(1.5)
            st.success("Schedule synced!")
    with col3:
        if st.button("⚡ Detect Gaps", use_container_width=True):
            st.info("No gaps detected in next 6 hours")

    # Today's schedule
    st.subheader("Today's Broadcast Schedule")
    schedule_full = [
        ("06:00", "09:00", "WKRN Morning News LIVE",   "news_live",  "aired",     False),
        ("09:00", "10:00", "Today Show (NBC Feed)",    "network",    "aired",     False),
        ("10:00", "11:00", "The Price Is Right",       "syndicated", "aired",     False),
        ("11:00", "12:00", "The Young & the Restless", "syndicated", "aired",     False),
        ("12:00", "12:30", "WKRN News at Noon",        "news_live",  "aired",     False),
        ("12:30", "13:00", "Let's Make a Deal",        "syndicated", "aired",     False),
        ("13:00", "15:00", "Days of Our Lives",        "network",    "aired",     False),
        ("15:00", "16:00", "The Kelly Clarkson Show",  "syndicated", "airing",    True),
        ("16:00", "17:00", "Jeopardy!",                "syndicated", "upcoming",  True),
        ("17:00", "17:30", "WKRN News at 5",           "news_live",  "upcoming",  True),
        ("18:00", "18:30", "WKRN News at 6",           "news_live",  "upcoming",  True),
        ("18:30", "19:30", "NBC Nightly News",         "network",    "upcoming",  True),
        ("19:30", "22:00", "NBC Primetime",             "network",    "upcoming",  True),
        ("22:00", "22:30", "WKRN News at 10",          "news_live",  "upcoming",  True),
        ("22:30", "23:30", "The Tonight Show",         "network",    "upcoming",  True),
        ("23:30", "00:30", "Late Night",               "network",    "upcoming",  True),
    ]
    type_colors = {"news_live": "#6366f1", "network": "#0891b2", "syndicated": "#059669"}
    for s, e, title, t, status, scte in schedule_full:
        tc = type_colors.get(t, "#475569")
        status_icon = "🟢" if status == "airing" else "✅" if status == "aired" else "🔵"
        scte_badge = '<span style="background:#7c3aed;color:#fff;font-size:10px;padding:1px 5px;border-radius:3px;margin-left:6px;">SCTE-35</span>' if scte and "news" in t else ""
        st.markdown(f"""
        <div style="display:flex;gap:12px;align-items:center;padding:7px 14px;
        background:#1e293b;border-radius:6px;margin:3px 0;border-left:3px solid {tc};">
        <span style="color:#94a3b8;font-family:monospace;min-width:120px;">{s} – {e}</span>
        <span style="color:#e2e8f0;flex:1;">{title}{scte_badge}</span>
        <span style="color:#64748b;font-size:12px;min-width:80px;">{t.replace('_',' ')}</span>
        <span style="font-size:14px;">{status_icon}</span>
        </div>""", unsafe_allow_html=True)

    st.caption("🟣 SCTE-35 = ad break cue points injected | 🟢 On-Air | ✅ Aired | 🔵 Scheduled")


elif page == "🌐 OTT Distribution":
    st.title("🌐 OTT Distribution Agent")
    st.caption("HLS / DASH Packaging | ABR Ladder | CloudFront / Akamai CDN | DRM | Live + VOD Origin")

    with st.expander("**Agent Capabilities** — Click to expand", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
            **Stream Packaging**
            - HLS (TS + fMP4 segments)
            - DASH (MPEG-DASH MPD)
            - CMAF (single-file)
            - Low-latency HLS (LL-HLS)
            - 7-rung ABR ladder
            """)
        with col2:
            st.markdown("""
            **CDN Management**
            - AWS CloudFront
            - Akamai Media Delivery
            - Fastly Streaming
            - Cache purge on event
            - Geographic restriction
            """)
        with col3:
            st.markdown("""
            **DRM & Security**
            - Widevine (Android/Web)
            - FairPlay (Apple)
            - PlayReady (Windows)
            - Token-based auth
            - Watermarking (NexGuard)
            """)
        with col4:
            st.markdown("""
            **Analytics**
            - Real-time viewer count
            - Bitrate distribution
            - Buffer ratio per rung
            - Geographic heatmap
            - CDN cost per viewer
            """)

    st.divider()

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f'<span class="realtime-indicator"></span> **Live OTT Status** — {datetime.now().strftime("%I:%M:%S %p")}', unsafe_allow_html=True)
    with col2:
        if st.button("🔄 Refresh CDN", use_container_width=True):
            st.rerun()

    # CDN health
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Viewers", "147,234", "+2.3K/min")
    col2.metric("CDN Uptime", "99.98%", "CloudFront + Akamai")
    col3.metric("Avg Bitrate Served", "4.8 Mbps", "+0.3 Mbps vs yesterday")
    col4.metric("Buffer Ratio", "0.12%", "✅ < 0.5% target")

    # ABR ladder
    st.subheader("ABR Ladder — Live Viewer Distribution")
    abr_ladder = [
        ("4K HDR",    "25 Mbps",  "3840×2160", 12847,  0.9,  "✅"),
        ("1080p60",   "8 Mbps",   "1920×1080", 89234,  0.7,  "✅"),
        ("1080p",     "5 Mbps",   "1920×1080", 21043,  0.5,  "✅"),
        ("720p",      "3 Mbps",   "1280×720",  13892,  0.3,  "✅"),
        ("480p",      "1.5 Mbps", "854×480",   7218,   0.2,  "✅"),
        ("360p",      "750 kbps", "640×360",   2941,   0.15, "✅"),
        ("Audio Only","128 kbps", "—",          59,    0.02, "✅"),
    ]
    st.markdown("| Profile | Bitrate | Resolution | Viewers | Buffer Ratio | Status |")
    st.markdown("|---------|---------|------------|---------|--------------|--------|")
    for p, br, res, viewers, buf, status in abr_ladder:
        buf_color = "🟢" if buf < 0.3 else "🟡"
        st.markdown(f"| **{p}** | {br} | {res} | {viewers:,} | {buf_color} {buf:.2f}% | {status} |")

    # CDN pops
    st.subheader("CDN Edge Locations — Request Distribution")
    geo = [("US East",  "43%"), ("US West", "28%"), ("Europe", "16%"), ("APAC", "8%"), ("Other", "5%")]
    cols_geo = st.columns(5)
    for col, (region, pct) in zip(cols_geo, geo):
        col.metric(region, pct)


elif page == "📰 Newsroom Integration":
    st.title("📰 Newsroom Integration Agent")
    st.caption("iNews / ENPS MOS Sync | AP / Reuters / AFP Wire | Story Status Tracking | Urgent Flag Detection | AI Rundown Assist")

    with st.expander("**Agent Capabilities** — Click to expand", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
            **MOS Integration**
            - iNews REST + MOS 2.8
            - ENPS ActiveX bridge
            - Rundown sync (3-min)
            - Story status tracking
            - Script version control
            """)
        with col2:
            st.markdown("""
            **Wire Ingestion**
            - AP (Associated Press)
            - Reuters News Agency
            - AFP (Agence France-Presse)
            - CNN Wire service
            - AI priority scoring
            """)
        with col3:
            st.markdown("""
            **AI Assist**
            - Urgent flag detection
            - Story duplicate filter
            - Auto-topic tagging
            - Source credibility score
            - Suggested coverage angle
            """)
        with col4:
            st.markdown("""
            **Alerting**
            - Breaking wire → Slack
            - Rundown gap alert
            - Story conflict detect
            - Script approval flow
            - Live show countdown
            """)

    st.divider()

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f'<span class="realtime-indicator"></span> **iNews Live** — Synced {datetime.now().strftime("%I:%M:%S %p")}', unsafe_allow_html=True)
    with col2:
        if st.button("🔄 Sync iNews", use_container_width=True):
            with st.spinner("Connecting to iNews MOS..."):
                time.sleep(1.2)
            st.success("Rundown synced (8 stories)")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Stories in Rundown", "8", "6 ready, 2 editing")
    col2.metric("Wire Stories Today", "247", "+14 in last hour")
    col3.metric("Urgent Flags", "2", "AI-detected")
    col4.metric("MOS Connection", "✅ Live", "iNews 8.6.1")

    # Rundown
    st.subheader("Live Rundown — WKRN News at 6 (18:00)")
    rundown_full = [
        ("FIRE-DOWNTOWN",   "Warehouse Fire Nashville",     "Jake Thompson",   "2:30", "✅ Ready",    "LEAD",   "LIVE PKG"),
        ("COUNCIL-VOTE",    "City Council Budget Vote",     "Maria Sanchez",   "1:45", "✅ Ready",    "2ND",    "PKG"),
        ("WEATHER-STORM",   "Severe Storm Watch Tonight",   "Weather Team",    "1:15", "✅ Ready",    "3RD",    "LIVE VOSOT"),
        ("AI-REGULATION",   "Senate AI Bill Vote",          "David Park",      "2:00", "⏳ Editing",  "4TH",    "PKG"),
        ("TITANS-WIN",      "Titans Win Playoff Opener",    "Sports Desk",     "1:30", "✅ Ready",    "5TH",    "PKG"),
        ("FED-RATE",        "Fed Rate Decision Impact",     "Business Desk",   "1:00", "✅ Ready",    "6TH",    "VOSOT"),
        ("TRAFFIC-I24",     "I-24 Closure Update",          "Traffic Cam",     "0:45", "✅ Ready",    "KICKER", "VO"),
        ("WEATHER-TAG",     "7-Day Forecast",               "Meteorologist",   "0:30", "✅ Ready",    "TAG",    "LIVE"),
    ]
    pos_colors = {"LEAD": "#ef4444", "2ND": "#f59e0b", "3RD": "#6366f1", "4TH": "#6366f1",
                  "5TH": "#475569", "6TH": "#475569", "KICKER": "#059669", "TAG": "#059669"}
    for slug, title, reporter, dur, status, pos, story_type in rundown_full:
        pc = pos_colors.get(pos, "#475569")
        sc = "#22c55e" if "Ready" in status else "#f59e0b"
        st.markdown(f"""
        <div style="display:flex;gap:10px;align-items:center;padding:8px 14px;
        background:#1e293b;border-radius:6px;margin:4px 0;">
        <span style="background:{pc};color:#fff;padding:2px 8px;border-radius:4px;
        font-size:11px;font-weight:700;min-width:58px;text-align:center;">{pos}</span>
        <span style="color:#94a3b8;font-family:monospace;font-size:11px;min-width:105px;">{slug}</span>
        <span style="color:#e2e8f0;flex:2;font-weight:500;">{title}</span>
        <span style="color:#94a3b8;min-width:85px;">{reporter.split()[0]}</span>
        <span style="background:#334155;color:#94a3b8;padding:2px 7px;border-radius:4px;
        font-size:11px;min-width:75px;text-align:center;">{story_type}</span>
        <span style="color:#94a3b8;min-width:35px;">{dur}</span>
        <span style="color:{sc};">{status}</span>
        </div>""", unsafe_allow_html=True)

    # Wire stories
    st.divider()
    st.subheader("Breaking Wire Stories — Last Hour")
    wires = [
        ("🔴 URGENT", "AP",      "Senate Passes AI Safety Regulation Bill 67-33",           "2 min ago",  "Politics"),
        ("🔴 URGENT", "Reuters", "Gaza Ceasefire Deal Signed — Hostages to be Released",    "8 min ago",  "World"),
        ("⚠️ HIGH",   "AFP",     "Magnitude 6.1 Earthquake Near Tokyo — No Tsunami Warning","14 min ago", "World"),
        ("ℹ️ NORMAL", "AP",      "Fed Chair: 'Data-dependent' Rate Path for Q2 2026",       "22 min ago", "Finance"),
        ("ℹ️ NORMAL", "Reuters", "SpaceX Starship Test Flight 9 Scheduled for Next Week",   "31 min ago", "Tech"),
    ]
    for priority, source, headline, timing, category in wires:
        p_color = "#ef4444" if "URGENT" in priority else "#f59e0b" if "HIGH" in priority else "#3b82f6"
        st.markdown(f"""
        <div style="background:#0f172a;padding:10px 14px;border-radius:8px;margin:5px 0;
        border-left:3px solid {p_color};">
        <div style="display:flex;gap:10px;align-items:center;">
        <span style="font-weight:700;color:{p_color};min-width:80px;">{priority}</span>
        <span style="background:#1e293b;color:#6366f1;padding:2px 7px;border-radius:4px;
        font-size:11px;font-weight:700;">{source}</span>
        <span style="color:#e2e8f0;flex:1;font-weight:500;">{headline}</span>
        <span style="color:#64748b;font-size:12px;">{timing}</span>
        <span style="color:#94a3b8;font-size:12px;">{category}</span>
        </div>
        </div>""", unsafe_allow_html=True)


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
    col1.metric("Supported Protocols", "21+")
    col2.metric("Integration Types", "12 Categories")
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
    ┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
    │                                    MediaAgentIQ Platform — 14 AI Agents                            │
    │  ┌────────┐ ┌──────┐ ┌─────────┐ ┌──────────┐ ┌────────┐ ┌────────┐ ┌───────┐                    │
    │  │Caption │ │ Clip │ │ Archive │ │Compliance│ │ Social │ │Localiz-│ │Rights │                    │
    │  │ Agent  │ │Agent │ │  Agent  │ │  Agent   │ │Publishing│ │ation  │ │ Agent │                    │
    │  └───┬────┘ └──┬───┘ └────┬────┘ └────┬─────┘ └───┬────┘ └───┬────┘ └──┬────┘                    │
    │  ┌────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │
    │  │Trending│ │Deepfake  │ │ Fact-    │ │Audience  │ │Production│ │  Brand   │ │  Carbon  │        │
    │  │ Agent  │ │Detection │ │ Check    │ │Intellig. │ │ Director │ │  Safety  │ │Intellig. │        │
    │  └───┬────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘        │
    │      │           │            │             │             │            │            │              │
    │  ┌───┴───────────┴────────────┴─────────────┴─────────────┴────────────┴────────────┴──────┐       │
    │  │              Integration Layer — REST API │ WebSocket │ MOS │ NMOS │ gRPC │ Webhooks    │       │
    │  └───┬───────────┬────────────┬─────────────┬─────────────┬────────────┬────────────┬──────┘       │
    └──────┼───────────┼────────────┼─────────────┼─────────────┼────────────┼────────────┼──────────────┘
           │           │            │             │             │            │            │
    ┌──────┴──┐ ┌──────┴──┐ ┌──────┴──┐ ┌────────┴─┐ ┌────────┴─┐ ┌───────┴──┐ ┌──────┴───┐
    │   MAM   │ │Broadcast│ │  NMOS   │ │  Cloud   │ │C2PA/Fact │ │ Brand    │ │  Carbon  │
    │ Systems │ │Automate │ │ Network │ │Platforms │ │Check APIs│ │Safety/Ad │ │ESG APIs  │
    └─────────┘ └─────────┘ └─────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘
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
            {"method": "POST", "endpoint": "/api/v1/deepfake/verify", "description": "Run forensic deepfake & C2PA provenance check"},
            {"method": "POST", "endpoint": "/api/v1/factcheck/analyze", "description": "Extract & verify claims against 8 databases"},
            {"method": "GET", "endpoint": "/api/v1/audience/retention", "description": "Get real-time retention curve & drop-off predictions"},
            {"method": "POST", "endpoint": "/api/v1/production/plan", "description": "Generate shot plan, lower-thirds & rundown"},
            {"method": "POST", "endpoint": "/api/v1/brandsafety/score", "description": "Score content for GARM compliance & CPM optimization"},
            {"method": "GET", "endpoint": "/api/v1/carbon/report", "description": "Get Scope 1/2/3 carbon footprint & ESG score"},
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

// Subscribe to events (all 14 agents)
ws.send(JSON.stringify({
    action: 'subscribe',
    channels: [
        // Original 8 agents
        'trending', 'compliance_alerts', 'processing_status',
        'caption.live', 'clip.detected', 'archive.indexed',
        'social.scheduled', 'rights.alert',
        // Future-Ready 6 agents
        'deepfake.verdict', 'factcheck.claim_flagged',
        'audience.dropoff_risk', 'production.shot_change',
        'brandsafety.score_update', 'carbon.threshold_alert'
    ]
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
        "trending.alert",
        "deepfake.flagged",
        "factcheck.false_claim_detected",
        "audience.drop_off_alert",
        "production.rundown_updated",
        "brandsafety.ad_blocked",
        "carbon.esg_report_ready"
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


# ============== Channel Simulator ==============

elif page == "💬 Channel Simulator":

    # ── Styles ────────────────────────────────────────────────────────────
    st.markdown("""
<style>
/* ── Slack chrome ── */
.sim-slack-workspace {
    background: linear-gradient(160deg,#4a154b 0%,#611f69 100%);
    padding:14px 16px; border-radius:10px 10px 0 0;
    display:flex; align-items:center; gap:10px;
}
.sim-slack-ws-name { color:#fff; font-weight:700; font-size:15px; }
.sim-slack-ws-dot  { width:9px;height:9px;background:#2bac76;border-radius:50%;border:2px solid #4a154b; }
.sim-slack-sidebar {
    background:#19171d; padding:8px 0;
    min-height:500px; border-radius:0 0 0 10px;
}
.sim-slack-section-hdr { color:#9e8da4; font-size:11px; font-weight:700;
    padding:10px 16px 4px; letter-spacing:.06em; text-transform:uppercase; }
.sim-slack-ch { display:flex; align-items:center; gap:6px;
    padding:5px 16px; border-radius:4px; margin:1px 8px;
    color:#c9c3d0; font-size:14px; }
.sim-slack-ch.active { background:rgba(29,155,209,.22); color:#fff; }
.sim-slack-ch-hash { color:#9e8da4; margin-right:2px; }
.sim-slack-badge { background:#e01e5a; color:#fff; border-radius:10px;
    padding:1px 6px; font-size:11px; margin-left:auto; }
/* message area */
.sim-slack-area-hdr {
    background:#1a1d21; border-bottom:1px solid #2d3136;
    padding:11px 16px; display:flex; align-items:center; gap:8px;
    border-radius:10px 10px 0 0;
}
.sim-slack-area-hdr-name { color:#fff; font-weight:700; font-size:15px; }
.sim-slack-area-hdr-desc { color:#9e8da4; font-size:12px; margin-left:6px; }
.sim-slack-msgs {
    background:#1a1d21; padding:12px 16px;
    border-radius:0 0 10px 10px;
    border-top:none;
}
/* individual message */
.sim-slack-msg  { display:flex; gap:12px; padding:7px 0; align-items:flex-start; }
.sim-slack-av   { width:36px;height:36px;border-radius:6px;
    background:linear-gradient(135deg,#9c27b0,#e91e63);
    display:flex;align-items:center;justify-content:center;
    font-size:19px;flex-shrink:0; }
.sim-slack-av.user { background:linear-gradient(135deg,#1164A3,#0b4d91); }
.sim-slack-msg-hdr { display:flex;align-items:baseline;gap:8px;margin-bottom:2px; }
.sim-slack-msg-name  { color:#fff; font-weight:700; font-size:14px; }
.sim-slack-app-badge { background:#1d9bd1;color:#fff;font-size:10px;
    padding:1px 5px;border-radius:3px;font-weight:600; }
.sim-slack-msg-ts    { color:#9e8da4; font-size:11px; }
.sim-slack-msg-text  { color:#d1d2d3; font-size:14px; line-height:1.55; }
.sim-slack-cmd-text  { color:#c9c3d0; font-family:monospace; background:#2d3136;
    padding:2px 7px; border-radius:4px; font-size:13px; }
/* Block Kit card */
.sim-slack-card {
    background:#1e2329; border:1px solid #383c42;
    border-left:3px solid #9c27b0;
    border-radius:6px; padding:12px 16px; margin-top:6px; max-width:700px;
}
.sim-slack-card-title { color:#fff; font-weight:700; font-size:15px; margin-bottom:8px; }
.sim-slack-card-muted { color:#9e8da4; font-size:12px; }
.sim-slack-card-text  { color:#d1d2d3; font-size:13px; line-height:1.6; }
.sim-slack-card-section { padding:7px 0; border-bottom:1px solid #2d3136; }
.sim-slack-card-section:last-of-type { border-bottom:none; }
.sim-slack-divider { border:none; border-top:1px solid #2d3136; margin:8px 0; }
.sim-slack-btn { background:#2d3136; color:#d1d2d3; border:1px solid #4a4f57;
    padding:5px 13px; border-radius:4px; font-size:12px; margin-right:5px; display:inline-block; }
.sim-slack-btn.primary { background:#1164A3; color:#fff; border-color:#1164A3; }
.sim-slack-status-row { display:flex;align-items:center;gap:8px;padding:3px 0; }
.sim-slack-dot-g { width:8px;height:8px;background:#2bac76;border-radius:50%;flex-shrink:0; }
.sim-slack-dot-y { width:8px;height:8px;background:#f59e0b;border-radius:50%;flex-shrink:0; }
.sim-slack-lbl   { color:#d1d2d3;font-size:13px;flex:1; }
.sim-slack-val   { color:#9e8da4;font-size:12px; }
.sbadge-crit { background:#b01121;color:#fff;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600; }
.sbadge-warn { background:#d97706;color:#fff;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600; }
.sbadge-ok   { background:#0f7b42;color:#fff;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600; }
.sbadge-info { background:#1164A3;color:#fff;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600; }

/* ── Teams chrome ── */
.sim-teams-header {
    background:#4f52b2;
    padding:13px 16px; border-radius:10px 10px 0 0;
    display:flex;align-items:center;gap:10px;
}
.sim-teams-title { color:#fff;font-weight:700;font-size:15px; }
.sim-teams-sidebar { background:#292929; min-height:500px; border-radius:0 0 0 10px; padding:8px 0; }
.sim-teams-ch { padding:8px 14px;color:#c0c0c0;font-size:13px;cursor:pointer;border-radius:4px;margin:2px 6px; }
.sim-teams-ch.active { background:rgba(255,255,255,.12);color:#fff; }
.sim-teams-area-hdr {
    background:#fff; border-bottom:1px solid #e0e0e0;
    padding:11px 16px; display:flex;align-items:center;gap:8px;
    border-radius:10px 10px 0 0;
}
.sim-teams-area-hdr-name { color:#252424;font-weight:700;font-size:15px; }
.sim-teams-msgs { background:#f5f5f5; padding:12px 16px; border-radius:0 0 10px 10px; }
.sim-teams-msg  { display:flex;gap:12px;padding:8px 0;align-items:flex-start; }
.sim-teams-av   { width:32px;height:32px;border-radius:50%;
    background:linear-gradient(135deg,#6264A7,#9c27b0);
    display:flex;align-items:center;justify-content:center;
    font-size:16px;flex-shrink:0; }
.sim-teams-av.user { background:linear-gradient(135deg,#1164A3,#0b4d91); }
.sim-teams-msg-name { color:#252424;font-weight:600;font-size:13px; }
.sim-teams-msg-ts   { color:#9e9e9e;font-size:11px;margin-left:8px; }
.sim-teams-msg-text { color:#252424;font-size:14px;line-height:1.5;margin-top:2px; }
/* Adaptive Card */
.sim-teams-card {
    background:#fff; border:1px solid #e0e0e0; border-radius:8px;
    padding:14px 16px; margin-top:6px; max-width:600px;
    box-shadow:0 1px 4px rgba(0,0,0,.08);
}
.sim-teams-card-title  { color:#252424;font-weight:700;font-size:14px;margin-bottom:10px; }
.sim-teams-card-text   { color:#616161;font-size:13px;line-height:1.6; }
.sim-teams-card-section{ padding:6px 0;border-bottom:1px solid #f0f0f0; }
.sim-teams-card-section:last-of-type { border-bottom:none; }
.sim-teams-btn { background:#6264A7;color:#fff;border-radius:4px;
    padding:6px 16px;font-size:13px;margin-right:5px;display:inline-block;margin-top:8px; }
.sim-teams-btn-sec { background:#fff;color:#6264A7;border:1px solid #6264A7;
    border-radius:4px;padding:6px 16px;font-size:13px;margin-right:5px;display:inline-block;margin-top:8px; }
.tbadge-crit { background:#a80000;color:#fff;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600; }
.tbadge-warn { background:#ca5010;color:#fff;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600; }
.tbadge-ok   { background:#107c10;color:#fff;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600; }
.tbadge-info { background:#0078d4;color:#fff;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600; }
</style>
""", unsafe_allow_html=True)

    # ── Card generators ────────────────────────────────────────────────────

    def _sc(html):
        """Wrap HTML in a Slack card div."""
        return f'<div class="sim-slack-card">{html}</div>'

    def _tc(html):
        """Wrap HTML in a Teams adaptive card div."""
        return f'<div class="sim-teams-card">{html}</div>'

    def _slack_welcome():
        return _sc("""
<div class="sim-slack-card-title">👋 Welcome to MediaAgentIQ</div>
<div class="sim-slack-card-section sim-slack-card-text">
  I'm your AI broadcast operations assistant. I can run compliance scans, detect deepfakes,
  find viral clips, monitor trends, and much more — all directly from this channel.<br><br>
  Type <span class="sim-slack-cmd-text">/miq-help</span> to see all available commands,
  or click a <strong>Quick Command</strong> button below to see a live demo.
</div>
<div class="sim-slack-card-section">
  <span class="sbadge-ok">19 Agents Online</span>&nbsp;
  <span class="sbadge-info">Autonomous Mode Active</span>&nbsp;
  <span class="sbadge-ok">Connectors Ready</span>
</div>""")

    def _teams_welcome():
        return _tc("""
<div class="sim-teams-card-title">👋 Welcome to MediaAgentIQ</div>
<div class="sim-teams-card-section sim-teams-card-text">
  I'm your AI broadcast operations assistant — connected to all 19 agents.<br>
  Type <strong>/miq-help</strong> for available commands, or click a Quick Command button to demo live.
</div>
<div class="sim-teams-card-section">
  <span class="tbadge-ok">19 Agents Online</span>&nbsp;
  <span class="tbadge-info">Autonomous Mode Active</span>
</div>""")

    def _slack_help():
        return _sc("""
<div class="sim-slack-card-title">MediaAgentIQ — Available Commands</div>
<div class="sim-slack-card-section">
<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px 24px;">
  <div><span class="sim-slack-cmd-text">/miq-status</span><br>
    <span class="sim-slack-card-muted">System health &amp; all 19 agent statuses</span></div>
  <div><span class="sim-slack-cmd-text">/miq-trending</span><br>
    <span class="sim-slack-card-muted">Live trending topics &amp; breaking news</span></div>
  <div><span class="sim-slack-cmd-text">/miq-compliance</span><br>
    <span class="sim-slack-card-muted">FCC scan with violation details</span></div>
  <div><span class="sim-slack-cmd-text">/miq-deepfake</span><br>
    <span class="sim-slack-card-muted">C2PA provenance + 3-layer forensic</span></div>
  <div><span class="sim-slack-cmd-text">/miq-signal</span><br>
    <span class="sim-slack-card-muted">EBU R128 loudness + signal quality</span></div>
  <div><span class="sim-slack-cmd-text">/miq-caption</span><br>
    <span class="sim-slack-card-muted">Auto-generated captions preview</span></div>
  <div><span class="sim-slack-cmd-text">/miq-clip</span><br>
    <span class="sim-slack-card-muted">Viral moment detection + view predictions</span></div>
  <div><span class="sim-slack-cmd-text">/miq-archive [query]</span><br>
    <span class="sim-slack-card-muted">Natural language archive search</span></div>
</div>
</div>
<div class="sim-slack-card-muted" style="margin-top:8px;">
💡 You can also type plain messages like <em>"check compliance"</em> or <em>"show trends"</em>
</div>""")

    def _teams_help():
        return _tc("""
<div class="sim-teams-card-title">MediaAgentIQ — Available Commands</div>
<div class="sim-teams-card-section">
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr><td style="padding:3px 8px;font-family:monospace;color:#6264A7;">/miq-status</td><td style="color:#616161;">System health &amp; all 19 agent statuses</td></tr>
<tr><td style="padding:3px 8px;font-family:monospace;color:#6264A7;">/miq-trending</td><td style="color:#616161;">Live trending topics &amp; breaking news</td></tr>
<tr><td style="padding:3px 8px;font-family:monospace;color:#6264A7;">/miq-compliance</td><td style="color:#616161;">FCC scan with violation details</td></tr>
<tr><td style="padding:3px 8px;font-family:monospace;color:#6264A7;">/miq-deepfake</td><td style="color:#616161;">C2PA provenance + 3-layer forensic</td></tr>
<tr><td style="padding:3px 8px;font-family:monospace;color:#6264A7;">/miq-signal</td><td style="color:#616161;">EBU R128 loudness + broadcast signal</td></tr>
<tr><td style="padding:3px 8px;font-family:monospace;color:#6264A7;">/miq-caption</td><td style="color:#616161;">Auto-generated captions preview</td></tr>
<tr><td style="padding:3px 8px;font-family:monospace;color:#6264A7;">/miq-clip</td><td style="color:#616161;">Viral moment detection + view predictions</td></tr>
<tr><td style="padding:3px 8px;font-family:monospace;color:#6264A7;">/miq-archive [query]</td><td style="color:#616161;">Natural language archive search</td></tr>
</table>
</div>
<div style="margin-top:8px;">
  <span class="sim-teams-btn">Get Started</span>
</div>""")

    def _slack_status():
        agents_s = [
            ("📝 Caption Agent",         "🟢", "2ms"),
            ("🎬 Clip Agent",            "🟢", "3ms"),
            ("🔍 Archive Agent",         "🟢", "4ms"),
            ("⚖️ Compliance Agent",      "🟢", "1ms"),
            ("📱 Social Publishing",     "🟢", "2ms"),
            ("🌍 Localization Agent",    "🟢", "3ms"),
            ("📜 Rights Agent",          "🟢", "2ms"),
            ("📈 Trending Agent",        "🟢", "1ms"),
            ("🕵️ Deepfake Detection",   "🟢", "5ms"),
            ("✅ Live Fact-Check",       "🟢", "4ms"),
            ("👥 Audience Intelligence","🟢", "3ms"),
            ("🎥 AI Production Director","🟢","2ms"),
            ("🛡️ Brand Safety",         "🟢", "2ms"),
            ("🌿 Carbon Intelligence",  "🟢", "3ms"),
            ("📥 Ingest + Transcode",   "🟢", "6ms"),
            ("📡 Signal Quality",       "🟢", "1ms"),
            ("📋 Playout Scheduling",   "🟢", "2ms"),
            ("🌐 OTT Distribution",     "🟢", "4ms"),
            ("📰 Newsroom Integration", "🟢", "3ms"),
        ]
        rows = "".join(
            f'<div class="sim-slack-status-row">'
            f'<div class="sim-slack-dot-g"></div>'
            f'<div class="sim-slack-lbl">{a}</div>'
            f'<div class="sim-slack-val">{dot} Online &nbsp; {lat}</div>'
            f'</div>'
            for a, dot, lat in agents_s
        )
        return _sc(f"""
<div class="sim-slack-card-title">🟢 MediaAgentIQ — System Status</div>
<div class="sim-slack-card-section">
  <div style="display:flex;gap:24px;flex-wrap:wrap;margin-bottom:6px;">
    <div style="text-align:center;">
      <div style="color:#2bac76;font-size:22px;font-weight:700;">19</div>
      <div class="sim-slack-card-muted">Agents Online</div></div>
    <div style="text-align:center;">
      <div style="color:#d1d2d3;font-size:22px;font-weight:700;">3ms</div>
      <div class="sim-slack-card-muted">Avg Latency</div></div>
    <div style="text-align:center;">
      <div style="color:#d1d2d3;font-size:22px;font-weight:700;">1,247</div>
      <div class="sim-slack-card-muted">Tasks Today</div></div>
    <div style="text-align:center;">
      <div style="color:#2bac76;font-size:22px;font-weight:700;">✅</div>
      <div class="sim-slack-card-muted">Autonomous Mode</div></div>
  </div>
</div>
<div class="sim-slack-card-section">
  <div class="sim-slack-card-muted" style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px;">Agent Status</div>
  {rows}
</div>
<div class="sim-slack-card-section">
  <div class="sim-slack-card-muted" style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px;">Connector Status</div>
  <div class="sim-slack-status-row"><div class="sim-slack-dot-g"></div><div class="sim-slack-lbl">Slack Connector</div><div class="sim-slack-val">🟢 Connected &nbsp; 1ms</div></div>
  <div class="sim-slack-status-row"><div class="sim-slack-dot-g"></div><div class="sim-slack-lbl">Teams Connector</div><div class="sim-slack-val">🟢 Connected &nbsp; 2ms</div></div>
</div>
<div style="margin-top:8px;">
  <span class="sim-slack-btn primary">📊 Full Report</span>
  <span class="sim-slack-btn">⚙️ Configure Alerts</span>
  <span class="sim-slack-btn">📅 View Schedule</span>
</div>""")

    def _teams_status():
        return _tc("""
<div class="sim-teams-card-title">🟢 MediaAgentIQ — System Status</div>
<div class="sim-teams-card-section">
  <table style="width:100%;border-collapse:collapse;font-size:13px;">
    <tr style="color:#252424;font-weight:600;border-bottom:1px solid #e0e0e0;">
      <td style="padding:4px 8px;">Agent</td><td style="padding:4px 8px;">Status</td><td style="padding:4px 8px;">Latency</td></tr>
    <tr><td style="padding:3px 8px;">📝 Caption Agent</td><td><span class="tbadge-ok">Online</span></td><td style="color:#616161;">2ms</td></tr>
    <tr><td style="padding:3px 8px;">⚖️ Compliance Agent</td><td><span class="tbadge-ok">Online</span></td><td style="color:#616161;">1ms</td></tr>
    <tr><td style="padding:3px 8px;">🕵️ Deepfake Detection</td><td><span class="tbadge-ok">Online</span></td><td style="color:#616161;">5ms</td></tr>
    <tr><td style="padding:3px 8px;">📈 Trending Agent</td><td><span class="tbadge-ok">Online</span></td><td style="color:#616161;">1ms</td></tr>
    <tr><td style="padding:3px 8px;">📡 Signal Quality</td><td><span class="tbadge-ok">Online</span></td><td style="color:#616161;">1ms</td></tr>
    <tr><td style="padding:3px 8px;">📰 Newsroom Integration</td><td><span class="tbadge-ok">Online</span></td><td style="color:#616161;">3ms</td></tr>
    <tr><td style="padding:3px 8px;color:#9e9e9e;" colspan="3">+ 13 more agents — all online</td></tr>
  </table>
</div>
<div class="sim-teams-card-section">
  <span style="color:#252424;font-size:13px;font-weight:600;">Total tasks today: </span>
  <span style="color:#107c10;font-weight:700;">1,247</span>&nbsp;&nbsp;
  <span style="color:#252424;font-size:13px;font-weight:600;">Autonomous Mode: </span>
  <span class="tbadge-ok">Active</span>
</div>
<div>
  <span class="sim-teams-btn">📊 Full Report</span>
  <span class="sim-teams-btn-sec">⚙️ Configure</span>
</div>""")

    def _slack_trending():
        topics = [
            ("🚨", "CRITICAL", "sbadge-crit", "AI Regulation Senate Vote",     "+2,847%", "Politics",     "2.1M"),
            ("⚠️", "WARNING",  "sbadge-warn", "Gaza Ceasefire Talks",          "+1,234%", "World",        "1.4M"),
            ("ℹ️", "INFO",     "sbadge-info", "Super Bowl Ad Spending 2026",   "+892%",   "Sports/Biz",   "890K"),
            ("ℹ️", "INFO",     "sbadge-info", "Tech Layoffs Wave Q1",          "+756%",   "Business",     "670K"),
            ("ℹ️", "INFO",     "sbadge-info", "Climate Summit COP30 Prep",     "+612%",   "Environment",  "510K"),
        ]
        rows = "".join(
            f'<div class="sim-slack-card-section">'
            f'<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">'
            f'<span style="font-size:16px;">{ic}</span>'
            f'<span class="{badge}">{sev}</span>'
            f'<span class="sim-slack-card-text" style="font-weight:600;flex:1;">{topic}</span>'
            f'<span class="sim-slack-card-muted">{cat}</span>'
            f'</div>'
            f'<div style="margin-left:30px;margin-top:3px;">'
            f'<span style="color:#2bac76;font-size:12px;font-weight:700;">{spike} spike</span>'
            f'&nbsp;&nbsp;<span class="sim-slack-card-muted">Reach: {reach} posts</span>'
            f'</div>'
            f'</div>'
            for ic, sev, badge, topic, spike, cat, reach in topics
        )
        return _sc(f"""
<div class="sim-slack-card-title">📈 Trending Alerts — WKRN News</div>
<div class="sim-slack-card-section sim-slack-card-muted">
  Live monitoring • {datetime.now().strftime("%b %d %Y, %H:%M")} • 5 topics active
</div>
{rows}
<div style="margin-top:8px;">
  <span class="sim-slack-btn primary">🔔 Alert Newsroom</span>
  <span class="sim-slack-btn">📋 Full Report</span>
  <span class="sim-slack-btn">📊 Analytics</span>
</div>""")

    def _teams_trending():
        return _tc("""
<div class="sim-teams-card-title">📈 Trending Alerts — Live Monitor</div>
<div class="sim-teams-card-section">
  <table style="width:100%;border-collapse:collapse;font-size:13px;">
    <tr style="font-weight:600;color:#252424;border-bottom:1px solid #e0e0e0;">
      <td style="padding:4px 6px;">Severity</td><td style="padding:4px 6px;">Topic</td>
      <td style="padding:4px 6px;">Spike</td><td style="padding:4px 6px;">Category</td></tr>
    <tr><td style="padding:3px 6px;"><span class="tbadge-crit">CRITICAL</span></td>
      <td style="padding:3px 6px;font-weight:600;color:#252424;">AI Regulation Senate Vote</td>
      <td style="padding:3px 6px;color:#107c10;font-weight:700;">+2,847%</td>
      <td style="padding:3px 6px;color:#616161;">Politics</td></tr>
    <tr><td style="padding:3px 6px;"><span class="tbadge-warn">WARNING</span></td>
      <td style="padding:3px 6px;font-weight:600;color:#252424;">Gaza Ceasefire Talks</td>
      <td style="padding:3px 6px;color:#107c10;font-weight:700;">+1,234%</td>
      <td style="padding:3px 6px;color:#616161;">World</td></tr>
    <tr><td style="padding:3px 6px;"><span class="tbadge-info">INFO</span></td>
      <td style="padding:3px 6px;color:#252424;">Super Bowl Ad Spending 2026</td>
      <td style="padding:3px 6px;color:#107c10;font-weight:700;">+892%</td>
      <td style="padding:3px 6px;color:#616161;">Sports</td></tr>
    <tr><td style="padding:3px 6px;"><span class="tbadge-info">INFO</span></td>
      <td style="padding:3px 6px;color:#252424;">Tech Layoffs Wave Q1</td>
      <td style="padding:3px 6px;color:#107c10;font-weight:700;">+756%</td>
      <td style="padding:3px 6px;color:#616161;">Business</td></tr>
    <tr><td style="padding:3px 6px;"><span class="tbadge-info">INFO</span></td>
      <td style="padding:3px 6px;color:#252424;">Climate Summit COP30 Prep</td>
      <td style="padding:3px 6px;color:#107c10;font-weight:700;">+612%</td>
      <td style="padding:3px 6px;color:#616161;">Environment</td></tr>
  </table>
</div>
<div>
  <span class="sim-teams-btn">🔔 Alert Newsroom</span>
  <span class="sim-teams-btn-sec">📋 Full Report</span>
</div>""")

    def _slack_compliance():
        return _sc("""
<div class="sim-slack-card-title">⚖️ Compliance Scan — Morning Broadcast</div>
<div class="sim-slack-card-section">
  <span class="sbadge-crit">2 Critical</span>&nbsp;<span class="sbadge-warn">1 Warning</span>&nbsp;<span class="sbadge-ok">47 Clear</span>&nbsp;
  <span class="sim-slack-card-muted" style="margin-left:8px;">Scan completed in 1.2s • FCC Part 73 / §315</span>
</div>
<div class="sim-slack-card-section">
  <div style="margin-bottom:6px;"><span class="sbadge-crit">🔴 CRITICAL</span>
    <span class="sim-slack-card-text" style="margin-left:8px;font-weight:600;">00:23:45 — Profanity (FCC Part 73)</span></div>
  <div class="sim-slack-card-text">"...hot-mic expletive during live field segment..."</div>
  <div class="sim-slack-card-muted" style="margin-top:4px;">⚡ Auto-hold applied &nbsp;|&nbsp; Segment flagged for review</div>
</div>
<div class="sim-slack-card-section">
  <div style="margin-bottom:6px;"><span class="sbadge-crit">🔴 CRITICAL</span>
    <span class="sim-slack-card-text" style="margin-left:8px;font-weight:600;">01:45:12 — Political Ad Disclosure Missing</span></div>
  <div class="sim-slack-card-text">30-second political spot missing required sponsor identification</div>
  <div class="sim-slack-card-muted" style="margin-top:4px;">FCC §315 violation risk &nbsp;|&nbsp; Estimated fine: $40,000+</div>
</div>
<div class="sim-slack-card-section">
  <div style="margin-bottom:6px;"><span class="sbadge-warn">⚠️ WARNING</span>
    <span class="sim-slack-card-text" style="margin-left:8px;font-weight:600;">00:41:30 — Loudness Violation (EBU R128)</span></div>
  <div class="sim-slack-card-text">Commercial segment +8 LUFS above program level (−15 vs −23 LUFS target)</div>
  <div class="sim-slack-card-muted" style="margin-top:4px;">CALM Act non-compliance &nbsp;|&nbsp; Viewer complaint risk</div>
</div>
<div style="margin-top:8px;">
  <span class="sim-slack-btn primary">✅ Mark Reviewed</span>
  <span class="sim-slack-btn">📄 Full Report</span>
  <span class="sim-slack-btn">📨 Alert Legal</span>
  <span class="sim-slack-btn">⏸️ Hold Broadcast</span>
</div>""")

    def _teams_compliance():
        return _tc("""
<div class="sim-teams-card-title" style="color:#a80000;">⚖️ Compliance Alert — 2 Critical Issues</div>
<div class="sim-teams-card-section">
  <span class="tbadge-crit">CRITICAL</span>&nbsp;
  <span style="color:#252424;font-size:13px;font-weight:600;margin-left:4px;">00:23:45 — Profanity (FCC Part 73)</span><br>
  <span class="sim-teams-card-text">Hot-mic expletive in live field segment. Auto-hold applied.</span>
</div>
<div class="sim-teams-card-section">
  <span class="tbadge-crit">CRITICAL</span>&nbsp;
  <span style="color:#252424;font-size:13px;font-weight:600;margin-left:4px;">01:45:12 — Political Ad Missing Disclosure</span><br>
  <span class="sim-teams-card-text">FCC §315 — sponsor ID required. Estimated fine: $40,000+</span>
</div>
<div class="sim-teams-card-section">
  <span class="tbadge-warn">WARNING</span>&nbsp;
  <span style="color:#252424;font-size:13px;font-weight:600;margin-left:4px;">00:41:30 — Loudness Violation</span><br>
  <span class="sim-teams-card-text">CALM Act — commercial +8 LUFS above program level</span>
</div>
<div>
  <span class="sim-teams-btn">✅ Mark Reviewed</span>
  <span class="sim-teams-btn-sec">📄 Full Report</span>
  <span class="sim-teams-btn-sec">📨 Alert Legal</span>
</div>""")

    def _slack_deepfake():
        return _sc("""
<div class="sim-slack-card-title">🕵️ Deepfake Detection — Forensic Analysis</div>
<div class="sim-slack-card-section">
  <span class="sbadge-ok" style="font-size:13px;padding:4px 12px;">✅ AUTHENTIC</span>
  <span class="sim-slack-card-muted" style="margin-left:10px;">Risk Score: 0.042 (Very Low) &nbsp;|&nbsp; C2PA: Signed ✅</span>
</div>
<div class="sim-slack-card-section">
  <div class="sim-slack-card-muted" style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px;">Layer 1 — Audio Analysis</div>
  <div class="sim-slack-status-row"><div class="sim-slack-dot-g"></div><div class="sim-slack-lbl">Spectral coherence</div><div class="sim-slack-val">0.98 ✅ Pass</div></div>
  <div class="sim-slack-status-row"><div class="sim-slack-dot-g"></div><div class="sim-slack-lbl">Neural artifact score</div><div class="sim-slack-val">0.01 ✅ Pass</div></div>
  <div class="sim-slack-status-row"><div class="sim-slack-dot-g"></div><div class="sim-slack-lbl">Lip-sync correlation</div><div class="sim-slack-val">0.97 ✅ Pass</div></div>
</div>
<div class="sim-slack-card-section">
  <div class="sim-slack-card-muted" style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px;">Layer 2 — Video Analysis</div>
  <div class="sim-slack-status-row"><div class="sim-slack-dot-g"></div><div class="sim-slack-lbl">Face mesh stability</div><div class="sim-slack-val">0.96 ✅ Pass</div></div>
  <div class="sim-slack-status-row"><div class="sim-slack-dot-g"></div><div class="sim-slack-lbl">GAN fingerprint</div><div class="sim-slack-val">None detected ✅</div></div>
  <div class="sim-slack-status-row"><div class="sim-slack-dot-g"></div><div class="sim-slack-lbl">Compression artifacts</div><div class="sim-slack-val">0.03 ✅ Pass</div></div>
</div>
<div class="sim-slack-card-section">
  <div class="sim-slack-card-muted" style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px;">Layer 3 — Metadata + C2PA Provenance</div>
  <div class="sim-slack-status-row"><div class="sim-slack-dot-g"></div><div class="sim-slack-lbl">C2PA provenance chain</div><div class="sim-slack-val">Valid — 3 entries ✅</div></div>
  <div class="sim-slack-status-row"><div class="sim-slack-dot-g"></div><div class="sim-slack-lbl">Edit history</div><div class="sim-slack-val">Unmodified ✅</div></div>
  <div class="sim-slack-status-row"><div class="sim-slack-dot-g"></div><div class="sim-slack-lbl">Camera / timestamp</div><div class="sim-slack-val">Canon EOS R5 • WKRN • 2024-03-15</div></div>
</div>
<div style="margin-top:8px;">
  <span class="sim-slack-btn primary">📋 Full Report</span>
  <span class="sim-slack-btn">🔗 C2PA Certificate</span>
  <span class="sim-slack-btn">📨 Share</span>
</div>""")

    def _teams_deepfake():
        return _tc("""
<div class="sim-teams-card-title">🕵️ Deepfake Detection — Forensic Analysis</div>
<div class="sim-teams-card-section">
  <span class="tbadge-ok" style="font-size:13px;padding:4px 12px;">✅ AUTHENTIC</span>
  <span style="color:#616161;font-size:13px;margin-left:10px;">Risk Score: 0.042 — Very Low</span>
</div>
<div class="sim-teams-card-section">
  <div class="sim-teams-card-text">
    <strong>Audio:</strong> Spectral coherence 0.98 ✅ &nbsp; Neural artifacts 0.01 ✅ &nbsp; Lip-sync 0.97 ✅<br>
    <strong>Video:</strong> Face mesh 0.96 ✅ &nbsp; GAN fingerprint: None ✅ &nbsp; Artifacts 0.03 ✅<br>
    <strong>C2PA:</strong> Provenance chain valid (3 entries) ✅ &nbsp; Camera: Canon EOS R5
  </div>
</div>
<div>
  <span class="sim-teams-btn">📋 Full Report</span>
  <span class="sim-teams-btn-sec">🔗 C2PA Certificate</span>
</div>""")

    def _slack_signal():
        return _sc("""
<div class="sim-slack-card-title">📡 Signal Quality — Live Broadcast Monitor</div>
<div class="sim-slack-card-section">
  <span class="sbadge-ok">✅ ALL CLEAR</span>
  <span class="sim-slack-card-muted" style="margin-left:10px;">Channel: WKRN-HD &nbsp;|&nbsp; Checked 14 seconds ago</span>
</div>
<div class="sim-slack-card-section">
  <div class="sim-slack-card-muted" style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px;">Audio — EBU R128</div>
  <div class="sim-slack-status-row"><div class="sim-slack-dot-g"></div><div class="sim-slack-lbl">Integrated loudness</div><div class="sim-slack-val">−22.8 LUFS &nbsp;✅ (target −23 ±1)</div></div>
  <div class="sim-slack-status-row"><div class="sim-slack-dot-g"></div><div class="sim-slack-lbl">True peak</div><div class="sim-slack-val">−1.4 dBTP &nbsp;✅ (&lt; −1.0 limit)</div></div>
  <div class="sim-slack-status-row"><div class="sim-slack-dot-g"></div><div class="sim-slack-lbl">Loudness range (LRA)</div><div class="sim-slack-val">8.2 LU &nbsp;✅ (&lt; 18 LU)</div></div>
</div>
<div class="sim-slack-card-section">
  <div class="sim-slack-card-muted" style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px;">Video</div>
  <div class="sim-slack-status-row"><div class="sim-slack-dot-g"></div><div class="sim-slack-lbl">Black frames</div><div class="sim-slack-val">0 detected &nbsp;✅</div></div>
  <div class="sim-slack-status-row"><div class="sim-slack-dot-g"></div><div class="sim-slack-lbl">Freeze frames</div><div class="sim-slack-val">0 detected &nbsp;✅</div></div>
  <div class="sim-slack-status-row"><div class="sim-slack-dot-g"></div><div class="sim-slack-lbl">Bitrate</div><div class="sim-slack-val">18.2 Mbps &nbsp;✅ (stable)</div></div>
</div>
<div class="sim-slack-card-section">
  <div class="sim-slack-card-muted" style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px;">Captions (CEA-608)</div>
  <div class="sim-slack-status-row"><div class="sim-slack-dot-g"></div><div class="sim-slack-lbl">Present</div><div class="sim-slack-val">Yes &nbsp;✅</div></div>
  <div class="sim-slack-status-row"><div class="sim-slack-dot-g"></div><div class="sim-slack-lbl">Sync drift</div><div class="sim-slack-val">±12ms &nbsp;✅ (&lt; 500ms limit)</div></div>
</div>
<div style="margin-top:8px;">
  <span class="sim-slack-btn primary">🔄 Re-check Now</span>
  <span class="sim-slack-btn">📊 History</span>
  <span class="sim-slack-btn">🔔 Configure Thresholds</span>
</div>""")

    def _teams_signal():
        return _tc("""
<div class="sim-teams-card-title">📡 Signal Quality — WKRN-HD</div>
<div class="sim-teams-card-section">
  <span class="tbadge-ok">✅ ALL CLEAR</span>
  <span style="color:#616161;font-size:12px;margin-left:8px;">Checked 14s ago</span>
</div>
<div class="sim-teams-card-section">
  <table style="width:100%;border-collapse:collapse;font-size:13px;">
    <tr><td style="padding:3px 8px;color:#252424;font-weight:600;">Audio (EBU R128)</td><td></td></tr>
    <tr><td style="padding:2px 16px;color:#616161;">Integrated loudness</td><td style="color:#107c10;font-weight:600;">−22.8 LUFS ✅</td></tr>
    <tr><td style="padding:2px 16px;color:#616161;">True peak</td><td style="color:#107c10;font-weight:600;">−1.4 dBTP ✅</td></tr>
    <tr><td style="padding:3px 8px;color:#252424;font-weight:600;">Video</td><td></td></tr>
    <tr><td style="padding:2px 16px;color:#616161;">Black frames</td><td style="color:#107c10;font-weight:600;">0 detected ✅</td></tr>
    <tr><td style="padding:2px 16px;color:#616161;">Bitrate</td><td style="color:#107c10;font-weight:600;">18.2 Mbps ✅</td></tr>
    <tr><td style="padding:3px 8px;color:#252424;font-weight:600;">Captions (CEA-608)</td><td></td></tr>
    <tr><td style="padding:2px 16px;color:#616161;">Sync drift</td><td style="color:#107c10;font-weight:600;">±12ms ✅</td></tr>
  </table>
</div>
<div>
  <span class="sim-teams-btn">🔄 Re-check</span>
  <span class="sim-teams-btn-sec">📊 History</span>
</div>""")

    def _slack_caption():
        captions_preview = [
            ("00:00:00", "00:00:04", "Sarah Mitchell (Anchor)", "Good morning, I'm Sarah Mitchell, and this is WKRN Morning News.", "99%"),
            ("00:00:04", "00:00:09", "Sarah Mitchell (Anchor)", "Breaking overnight: A massive fire has destroyed a warehouse in downtown Nashville.", "98%"),
            ("00:00:10", "00:00:15", "Sarah Mitchell (Anchor)", "Fire crews responded around 2 AM and battled the blaze for nearly four hours.", "97%"),
            ("00:00:16", "00:00:20", "Sarah Mitchell (Anchor)", "We go live now to reporter Jake Thompson at the scene.", "98%"),
            ("00:00:21", "00:00:27", "Jake Thompson (Reporter)", "Sarah, as you can see behind me, crews are still working to contain hot spots.", "96%"),
        ]
        rows = "".join(
            f'<div class="sim-slack-card-section" style="font-size:13px;">'
            f'<span style="color:#9c27b0;font-family:monospace;">{s} → {e}</span>'
            f'<span class="sim-slack-card-muted" style="margin-left:10px;">{spk}</span>'
            f'<span style="color:#2bac76;float:right;">{conf}</span><br>'
            f'<span class="sim-slack-card-text">{txt}</span>'
            f'</div>'
            for s, e, spk, txt, conf in captions_preview
        )
        return _sc(f"""
<div class="sim-slack-card-title">📝 Caption Agent — Auto-Generated</div>
<div class="sim-slack-card-section">
  <span class="sbadge-ok">13 segments</span>&nbsp;
  <span class="sim-slack-card-muted">Avg accuracy: 96.8% &nbsp;|&nbsp; Source: Morning News Broadcast</span>
</div>
{rows}
<div class="sim-slack-card-section sim-slack-card-muted">+ 8 more segments...</div>
<div style="margin-top:8px;">
  <span class="sim-slack-btn primary">📥 Download SRT</span>
  <span class="sim-slack-btn">📥 Download VTT</span>
  <span class="sim-slack-btn">✅ Approve All</span>
</div>""")

    def _teams_caption():
        return _tc("""
<div class="sim-teams-card-title">📝 Caption Agent — 13 Segments Generated</div>
<div class="sim-teams-card-section">
  <span class="tbadge-ok">96.8% Accuracy</span>
  <span style="color:#616161;font-size:12px;margin-left:8px;">Morning News Broadcast</span>
</div>
<div class="sim-teams-card-section">
  <div class="sim-teams-card-text">
    <strong>00:00:00 → 00:00:04</strong> [Sarah Mitchell] — "Good morning, I'm Sarah Mitchell..." <span style="color:#107c10;">99%</span><br>
    <strong>00:00:04 → 00:00:09</strong> [Sarah Mitchell] — "Breaking overnight: A massive fire..." <span style="color:#107c10;">98%</span><br>
    <strong>00:00:10 → 00:00:15</strong> [Sarah Mitchell] — "Fire crews responded around 2 AM..." <span style="color:#107c10;">97%</span><br>
    <span style="color:#9e9e9e;">+ 10 more segments...</span>
  </div>
</div>
<div>
  <span class="sim-teams-btn">📥 Download SRT</span>
  <span class="sim-teams-btn-sec">📥 Download VTT</span>
</div>""")

    def _slack_clip():
        clips = [
            ("97%", "#2bac76", "Reporter's Close Call with Debris", "02:25 → 02:42", "TikTok, Twitter/X, Instagram Reels", "500K – 2M views"),
            ("95%", "#2bac76", "Emotional Reunion: Lost Dog Found After Tornado", "14:52 → 15:18", "Facebook, Instagram, TikTok", "1M – 5M views"),
            ("94%", "#f59e0b", "Lightning Strikes During Live Weather Report", "35:05 → 35:25", "Twitter/X, TikTok, YouTube", "300K – 1M views"),
            ("92%", "#f59e0b", "Mayor's Mic Drop Response to Heckler", "25:43 → 26:08", "Twitter/X, TikTok, Reddit", "200K – 800K views"),
        ]
        rows = "".join(
            f'<div class="sim-slack-card-section" style="display:flex;gap:12px;align-items:flex-start;">'
            f'<div style="font-size:18px;font-weight:700;color:{color};min-width:42px;">{score}</div>'
            f'<div style="flex:1;">'
            f'<div class="sim-slack-card-text" style="font-weight:600;">{title}</div>'
            f'<div class="sim-slack-card-muted">{timing} &nbsp;|&nbsp; {platforms}</div>'
            f'<div style="color:#2bac76;font-size:12px;margin-top:2px;">📊 Predicted: {views}</div>'
            f'</div>'
            f'<div><span class="sim-slack-btn">🎬 Export</span><span class="sim-slack-btn">📱 Post</span></div>'
            f'</div>'
            for score, color, title, timing, platforms, views in clips
        )
        return _sc(f"""
<div class="sim-slack-card-title">🎬 Clip Agent — Viral Moments Detected</div>
<div class="sim-slack-card-section">
  <span class="sbadge-ok">4 clips found</span>&nbsp;
  <span class="sim-slack-card-muted">Top score: 97% &nbsp;|&nbsp; Source: Morning News Broadcast</span>
</div>
{rows}
<div style="margin-top:8px;">
  <span class="sim-slack-btn primary">📋 Full Analysis</span>
  <span class="sim-slack-btn">📤 Export All</span>
  <span class="sim-slack-btn">📅 Schedule All</span>
</div>""")

    def _teams_clip():
        return _tc("""
<div class="sim-teams-card-title">🎬 Clip Agent — 4 Viral Moments Found</div>
<div class="sim-teams-card-section">
  <table style="width:100%;border-collapse:collapse;font-size:13px;">
    <tr style="font-weight:600;color:#252424;border-bottom:1px solid #e0e0e0;">
      <td style="padding:4px 8px;">Score</td><td style="padding:4px 8px;">Clip</td><td style="padding:4px 8px;">Predicted Views</td></tr>
    <tr><td style="padding:3px 8px;color:#107c10;font-weight:700;">97%</td>
      <td style="padding:3px 8px;color:#252424;">Reporter's Close Call with Debris</td>
      <td style="padding:3px 8px;color:#107c10;">500K – 2M</td></tr>
    <tr><td style="padding:3px 8px;color:#107c10;font-weight:700;">95%</td>
      <td style="padding:3px 8px;color:#252424;">Emotional Reunion: Lost Dog Found</td>
      <td style="padding:3px 8px;color:#107c10;">1M – 5M</td></tr>
    <tr><td style="padding:3px 8px;color:#ca5010;font-weight:700;">94%</td>
      <td style="padding:3px 8px;color:#252424;">Lightning During Live Weather</td>
      <td style="padding:3px 8px;color:#107c10;">300K – 1M</td></tr>
    <tr><td style="padding:3px 8px;color:#ca5010;font-weight:700;">92%</td>
      <td style="padding:3px 8px;color:#252424;">Mayor's Mic Drop Response</td>
      <td style="padding:3px 8px;color:#107c10;">200K – 800K</td></tr>
  </table>
</div>
<div>
  <span class="sim-teams-btn">📤 Export All</span>
  <span class="sim-teams-btn-sec">📅 Schedule</span>
</div>""")

    def _slack_archive(query="tornado Nashville"):
        results = [
            ("Nashville Tornado Coverage — March 2024", "2024-03-14", "3:45:00", "HD 1080p", "6.7 GB", "weather, tornado, nashville, emergency", "97%"),
            ("Presidential Debate 2024 — Full Coverage", "2024-09-10", "2:15:00", "HD 1080p", "4.2 GB", "politics, election, debate", "61%"),
            ("Hurricane Milton — 72 Hour Coverage", "2024-10-09", "4:30:00", "HD 1080p", "8.1 GB", "weather, hurricane, florida", "54%"),
        ]
        rows = "".join(
            f'<div class="sim-slack-card-section">'
            f'<div style="display:flex;justify-content:space-between;align-items:flex-start;">'
            f'<div class="sim-slack-card-text" style="font-weight:600;">📹 {title}</div>'
            f'<span style="color:#2bac76;font-size:12px;font-weight:700;">Match: {rel}</span>'
            f'</div>'
            f'<div class="sim-slack-card-muted">{date} &nbsp;|&nbsp; {dur} &nbsp;|&nbsp; {fmt} &nbsp;|&nbsp; {size}</div>'
            f'<div class="sim-slack-card-muted">Tags: {tags}</div>'
            f'</div>'
            for title, date, dur, fmt, size, tags, rel in results
        )
        return _sc(f"""
<div class="sim-slack-card-title">🔍 Archive Search — "{query}"</div>
<div class="sim-slack-card-section">
  <span class="sbadge-info">3 results</span>&nbsp;
  <span class="sim-slack-card-muted">Searched 847 indexed assets in 0.3s</span>
</div>
{rows}
<div style="margin-top:8px;">
  <span class="sim-slack-btn primary">🔍 Refine Search</span>
  <span class="sim-slack-btn">📋 Export Metadata</span>
  <span class="sim-slack-btn">📥 Request Clips</span>
</div>""")

    def _teams_archive(query="tornado Nashville"):
        return _tc(f"""
<div class="sim-teams-card-title">🔍 Archive Search — "{query}"</div>
<div class="sim-teams-card-section">
  <span class="tbadge-info">3 results</span>
  <span style="color:#616161;font-size:12px;margin-left:8px;">Searched 847 assets in 0.3s</span>
</div>
<div class="sim-teams-card-section">
  <div class="sim-teams-card-text">
    <strong>📹 Nashville Tornado Coverage — March 2024</strong> <span style="color:#107c10;">97% match</span><br>
    <span style="color:#9e9e9e;">2024-03-14 | 3:45:00 | HD 1080p | 6.7 GB</span><br><br>
    <strong>📹 Presidential Debate 2024</strong> <span style="color:#ca5010;">61% match</span><br>
    <span style="color:#9e9e9e;">2024-09-10 | 2:15:00 | HD 1080p | 4.2 GB</span><br><br>
    <strong>📹 Hurricane Milton — 72 Hour Coverage</strong> <span style="color:#ca5010;">54% match</span><br>
    <span style="color:#9e9e9e;">2024-10-09 | 4:30:00 | HD 1080p | 8.1 GB</span>
  </div>
</div>
<div>
  <span class="sim-teams-btn">📋 Export Metadata</span>
  <span class="sim-teams-btn-sec">📥 Request Clips</span>
</div>""")

    def _slack_unknown(text):
        return _sc(f"""
<div class="sim-slack-card-title">🤖 MediaAgentIQ understood: <em>"{text[:60]}"</em></div>
<div class="sim-slack-card-section sim-slack-card-text">
  I analysed your message and routed it to the <strong>Trending Agent</strong> (best match).<br>
  Here's the live result — or try a specific slash command for more detail.
</div>
{_slack_trending()[len('<div class="sim-slack-card">'):-len('</div>')]}""")

    def _teams_unknown(text):
        return _tc(f"""
<div class="sim-teams-card-title">🤖 Routed: "{text[:50]}"</div>
<div class="sim-teams-card-section sim-teams-card-text">
  Your message was routed to the Trending Agent (best match). Type <strong>/miq-help</strong> to see all commands.
</div>""")

    # ── Command router ────────────────────────────────────────────────────

    def process_cmd(text, platform="slack"):
        t = text.strip().lower()
        # Extract archive query if present
        archive_q = "tornado Nashville"
        if "/miq-archive" in t:
            parts = text.strip().split(None, 1)
            archive_q = parts[1] if len(parts) > 1 else "tornado Nashville"

        if "help" in t or "/miq-help" in t:
            return _slack_help() if platform == "slack" else _teams_help()
        elif "status" in t or "/miq-status" in t:
            return _slack_status() if platform == "slack" else _teams_status()
        elif "trend" in t or "/miq-trend" in t:
            return _slack_trending() if platform == "slack" else _teams_trending()
        elif "compliance" in t or "fcc" in t or "/miq-compliance" in t:
            return _slack_compliance() if platform == "slack" else _teams_compliance()
        elif "deepfake" in t or "fake" in t or "forensic" in t or "/miq-deepfake" in t:
            return _slack_deepfake() if platform == "slack" else _teams_deepfake()
        elif "signal" in t or "loudness" in t or "ebu" in t or "/miq-signal" in t:
            return _slack_signal() if platform == "slack" else _teams_signal()
        elif "caption" in t or "subtitle" in t or "/miq-caption" in t:
            return _slack_caption() if platform == "slack" else _teams_caption()
        elif "clip" in t or "viral" in t or "/miq-clip" in t:
            return _slack_clip() if platform == "slack" else _teams_clip()
        elif "archive" in t or "search" in t or "/miq-archive" in t:
            return (_slack_archive(archive_q) if platform == "slack"
                    else _teams_archive(archive_q))
        else:
            return (_slack_unknown(text) if platform == "slack"
                    else _teams_unknown(text))

    # ── Helpers ───────────────────────────────────────────────────────────

    def _now_ts():
        return datetime.now().strftime("%I:%M %p")

    def _render_slack_msg(msg):
        role = msg["role"]
        ts   = msg.get("ts", "")
        if role == "user":
            av_cls = "sim-slack-av user"
            name   = "You"
            badge  = ""
            body   = (f'<span class="sim-slack-cmd-text">{msg["text"]}</span>'
                      if msg["text"].startswith("/")
                      else f'<span class="sim-slack-msg-text">{msg["text"]}</span>')
        else:
            av_cls = "sim-slack-av"
            name   = "MediaAgentIQ"
            badge  = '<span class="sim-slack-app-badge">APP</span>'
            body   = msg.get("card", "")
        av_icon = "🎬" if role == "bot" else "👤"
        return (
            f'<div class="sim-slack-msg">'
            f'  <div class="{av_cls}">{av_icon}</div>'
            f'  <div style="flex:1;min-width:0;">'
            f'    <div class="sim-slack-msg-hdr">'
            f'      <span class="sim-slack-msg-name">{name}</span>{badge}'
            f'      <span class="sim-slack-msg-ts">{ts}</span>'
            f'    </div>'
            f'    {body}'
            f'  </div>'
            f'</div>'
        )

    def _render_teams_msg(msg):
        role = msg["role"]
        ts   = msg.get("ts", "")
        if role == "user":
            av_cls = "sim-teams-av user"
            name   = "You"
            body   = f'<div class="sim-teams-msg-text">{msg["text"]}</div>'
        else:
            av_cls = "sim-teams-av"
            name   = "MediaAgentIQ"
            body   = f'<div>{msg.get("card", "")}</div>'
        av_icon = "M" if role == "bot" else "Y"
        return (
            f'<div class="sim-teams-msg">'
            f'  <div class="{av_cls}">{av_icon}</div>'
            f'  <div style="flex:1;min-width:0;">'
            f'    <div><span class="sim-teams-msg-name">{name}</span>'
            f'    <span class="sim-teams-msg-ts">{ts}</span></div>'
            f'    {body}'
            f'  </div>'
            f'</div>'
        )

    def _send(text, platform):
        ts = _now_ts()
        key_msgs = f"{platform}_msgs"
        st.session_state[key_msgs].append({"role": "user", "text": text, "card": None, "ts": ts})
        with st.spinner(f"MediaAgentIQ is typing{'...' if platform == 'slack' else ' in Teams...'}"):
            time.sleep(1.1)
            card = process_cmd(text, platform)
        st.session_state[key_msgs].append({"role": "bot", "text": None, "card": card, "ts": _now_ts()})

    # ── Session state init ────────────────────────────────────────────────

    if "slack_msgs" not in st.session_state:
        st.session_state.slack_msgs = [
            {"role": "bot", "text": None, "card": _slack_welcome(), "ts": "09:00 AM"}
        ]
    if "teams_msgs" not in st.session_state:
        st.session_state.teams_msgs = [
            {"role": "bot", "text": None, "card": _teams_welcome(), "ts": "09:00 AM"}
        ]

    # ── Page header ───────────────────────────────────────────────────────

    st.title("💬 Channel Simulator")
    st.caption("Live simulation of Slack & Microsoft Teams integration — agents respond in real time, no external accounts needed")

    sim_info = st.info(
        "💡 **How it works:** Type a slash command or plain message, and MediaAgentIQ routes it to the "
        "correct agent and returns a formatted Block Kit / Adaptive Card — exactly as users would see it "
        "in a real workspace."
    )

    # ── Platform tabs ─────────────────────────────────────────────────────

    slack_tab, teams_tab = st.tabs(["  Slack", "  Microsoft Teams"])

    # ══ SLACK TAB ═══════════════════════════════════════════════════════════
    with slack_tab:

        col_side, col_main = st.columns([1, 4])

        # Slack sidebar
        with col_side:
            st.markdown("""
<div class="sim-slack-workspace">
  <div class="sim-slack-ws-dot"></div>
  <div class="sim-slack-ws-name">WKRN Newsroom</div>
</div>
<div class="sim-slack-sidebar">
  <div class="sim-slack-section-hdr">Channels</div>
  <div class="sim-slack-ch active"><span class="sim-slack-ch-hash">#</span>newsroom
    <span class="sim-slack-badge">3</span></div>
  <div class="sim-slack-ch"><span class="sim-slack-ch-hash">#</span>noc-alerts</div>
  <div class="sim-slack-ch"><span class="sim-slack-ch-hash">#</span>compliance</div>
  <div class="sim-slack-ch"><span class="sim-slack-ch-hash">#</span>brand-safety</div>
  <div class="sim-slack-ch"><span class="sim-slack-ch-hash">#</span>social-publishing</div>
  <div class="sim-slack-ch"><span class="sim-slack-ch-hash">#</span>archive</div>
  <div class="sim-slack-section-hdr" style="margin-top:12px;">Apps</div>
  <div class="sim-slack-ch active" style="color:#fff;">🎬 MediaAgentIQ</div>
</div>""", unsafe_allow_html=True)

        # Slack main area
        with col_main:
            st.markdown("""
<div class="sim-slack-area-hdr">
  <span style="color:#d1d2d3;font-size:18px;">#</span>
  <span class="sim-slack-area-hdr-name">newsroom</span>
  <span class="sim-slack-area-hdr-desc">WKRN News · 24 members · MediaAgentIQ integrated</span>
</div>""", unsafe_allow_html=True)

            # Message history
            all_msgs_html = "".join(_render_slack_msg(m) for m in st.session_state.slack_msgs)
            st.markdown(
                f'<div class="sim-slack-msgs">{all_msgs_html}</div>',
                unsafe_allow_html=True
            )

            # Input form
            with st.form("slack_input_form", clear_on_submit=True):
                col_inp, col_btn = st.columns([6, 1])
                slack_input = col_inp.text_input(
                    "",
                    placeholder="Message #newsroom  —  try: /miq-help, /miq-trending, /miq-compliance ...",
                    label_visibility="collapsed"
                )
                slack_submitted = col_btn.form_submit_button("Send ↵", use_container_width=True)

            if slack_submitted and slack_input.strip():
                _send(slack_input.strip(), "slack")
                st.rerun()

            # Clear button
            if len(st.session_state.slack_msgs) > 1:
                if st.button("🗑️ Clear Chat", key="slack_clear", help="Reset the Slack conversation"):
                    st.session_state.slack_msgs = [
                        {"role": "bot", "text": None, "card": _slack_welcome(), "ts": _now_ts()}
                    ]
                    st.rerun()

        # Quick command buttons — below the two-column layout
        st.markdown("---")
        st.markdown("**⚡ Quick Commands** — click to run instantly:")
        q1, q2, q3, q4, q5, q6, q7, q8, q9 = st.columns(9)
        cmds_s = [
            (q1, "/miq-help",       "sk_help"),
            (q2, "/miq-status",     "sk_status"),
            (q3, "/miq-trending",   "sk_trending"),
            (q4, "/miq-compliance", "sk_compliance"),
            (q5, "/miq-deepfake",   "sk_deepfake"),
            (q6, "/miq-signal",     "sk_signal"),
            (q7, "/miq-caption",    "sk_caption"),
            (q8, "/miq-clip",       "sk_clip"),
            (q9, "/miq-archive",    "sk_archive"),
        ]
        for col, label, key in cmds_s:
            if col.button(label, key=key, use_container_width=True):
                _send(label, "slack")
                st.rerun()

    # ══ TEAMS TAB ═══════════════════════════════════════════════════════════
    with teams_tab:

        col_side_t, col_main_t = st.columns([1, 4])

        # Teams sidebar
        with col_side_t:
            st.markdown("""
<div class="sim-teams-header">
  <span style="font-size:20px;">⊞</span>
  <span class="sim-teams-title">WKRN News</span>
</div>
<div class="sim-teams-sidebar">
  <div style="padding:10px 14px;color:#9e9e9e;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;">Teams</div>
  <div class="sim-teams-ch active">📺 Newsroom</div>
  <div class="sim-teams-ch">🔔 NOC Alerts</div>
  <div class="sim-teams-ch">⚖️ Compliance</div>
  <div class="sim-teams-ch">🛡️ Brand Safety</div>
  <div style="padding:10px 14px;color:#9e9e9e;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;margin-top:8px;">Apps</div>
  <div class="sim-teams-ch active">🎬 MediaAgentIQ Bot</div>
</div>""", unsafe_allow_html=True)

        # Teams main area
        with col_main_t:
            st.markdown("""
<div class="sim-teams-area-hdr">
  <span style="font-size:18px;">📺</span>
  <span class="sim-teams-area-hdr-name">Newsroom</span>
  <span style="color:#9e9e9e;font-size:12px;margin-left:8px;">WKRN News · MediaAgentIQ Bot connected</span>
</div>""", unsafe_allow_html=True)

            # Message history
            all_msgs_html_t = "".join(_render_teams_msg(m) for m in st.session_state.teams_msgs)
            st.markdown(
                f'<div class="sim-teams-msgs">{all_msgs_html_t}</div>',
                unsafe_allow_html=True
            )

            # Input form
            with st.form("teams_input_form", clear_on_submit=True):
                col_inp_t, col_btn_t = st.columns([6, 1])
                teams_input = col_inp_t.text_input(
                    "",
                    placeholder="Type a message or /miq-help ...",
                    label_visibility="collapsed"
                )
                teams_submitted = col_btn_t.form_submit_button("Send ↵", use_container_width=True)

            if teams_submitted and teams_input.strip():
                _send(teams_input.strip(), "teams")
                st.rerun()

            # Clear button
            if len(st.session_state.teams_msgs) > 1:
                if st.button("🗑️ Clear Chat", key="teams_clear", help="Reset the Teams conversation"):
                    st.session_state.teams_msgs = [
                        {"role": "bot", "text": None, "card": _teams_welcome(), "ts": _now_ts()}
                    ]
                    st.rerun()

        # Quick commands for Teams
        st.markdown("---")
        st.markdown("**⚡ Quick Commands** — click to run instantly:")
        t1, t2, t3, t4, t5, t6, t7, t8, t9 = st.columns(9)
        cmds_t = [
            (t1, "/miq-help",       "tm_help"),
            (t2, "/miq-status",     "tm_status"),
            (t3, "/miq-trending",   "tm_trending"),
            (t4, "/miq-compliance", "tm_compliance"),
            (t5, "/miq-deepfake",   "tm_deepfake"),
            (t6, "/miq-signal",     "tm_signal"),
            (t7, "/miq-caption",    "tm_caption"),
            (t8, "/miq-clip",       "tm_clip"),
            (t9, "/miq-archive",    "tm_archive"),
        ]
        for col, label, key in cmds_t:
            if col.button(label, key=key, use_container_width=True):
                _send(label, "teams")
                st.rerun()

    st.divider()
    st.caption("Simulation runs entirely in-browser — no Slack/Teams accounts, no ngrok, no API keys required.")


# ============== Footer ==============

st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("MediaAgentIQ v3.1.0 | Enterprise Edition")
with col2:
    st.caption("AI-Powered Media Operations Platform")
with col3:
    st.caption(f"© {datetime.now().year} | Built for Broadcasters")
