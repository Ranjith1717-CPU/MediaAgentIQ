"""
MediaAgentIQ - Demo Sample Configuration
Customized demo data for showcasing the platform with a real sample video
Entertainment content - Music/Performance/Video content
"""

import os
from pathlib import Path

# Demo Sample Video Configuration
DEMO_SAMPLE_VIDEO = {
    "filename": "demo_sample_video.mp4",
    "path": "demo_assets/demo_sample_video.mp4",
    "title": "Entertainment Showcase - Dynamic Performance",
    "duration": "0:15",
    "duration_seconds": 15,
    "format": "MP4 (H.264)",
    "resolution": "1080p",
    "size_mb": 1.5,
    "description": "High-energy entertainment video clip for demo purposes",
    "content_type": "Entertainment"
}

# ============== CAPTION AGENT DATA ==============
# Captions extracted from the entertainment video
SAMPLE_CAPTIONS = [
    {"start": 0.0, "end": 2.5, "text": "[Music starts - upbeat tempo]", "speaker": "Audio", "confidence": 0.99},
    {"start": 2.5, "end": 5.0, "text": "[Dynamic visual sequence begins]", "speaker": "Audio", "confidence": 0.98},
    {"start": 5.0, "end": 8.0, "text": "[Peak energy moment - crowd cheering]", "speaker": "Audio", "confidence": 0.97},
    {"start": 8.0, "end": 11.0, "text": "[Instrumental break - beat drop]", "speaker": "Audio", "confidence": 0.99},
    {"start": 11.0, "end": 13.5, "text": "[Climax sequence]", "speaker": "Audio", "confidence": 0.98},
    {"start": 13.5, "end": 15.0, "text": "[Fade out - end card]", "speaker": "Audio", "confidence": 0.99},
]

SAMPLE_QA_ISSUES = [
    {"type": "success", "severity": "none", "segment": None, "timestamp": None, "issue": "Audio quality excellent", "details": "High-quality audio track with no distortion detected", "suggestion": None},
    {"type": "success", "severity": "none", "segment": None, "timestamp": None, "issue": "Timing validation passed", "details": "All segments properly synchronized with video", "suggestion": None},
    {"type": "success", "severity": "none", "segment": None, "timestamp": None, "issue": "Content scan clear", "details": "No inappropriate content detected", "suggestion": None},
    {"type": "info", "severity": "low", "segment": 3, "timestamp": "00:05.0", "issue": "High energy peak detected", "details": "Peak audio moment ideal for clip extraction", "suggestion": "Consider as viral clip starting point"},
]

# ============== CLIP AGENT DATA ==============
# Viral moments detected from the entertainment video
SAMPLE_VIRAL_MOMENTS = [
    {
        "id": 1,
        "start": 5.0,
        "end": 11.0,
        "title": "Peak Energy Moment - Perfect for Reels",
        "description": "High-energy sequence with dynamic visuals and beat drop. Ideal for TikTok and Instagram Reels.",
        "transcript": "[Beat drop] [Crowd reaction] [Visual climax]",
        "score": 0.96,
        "emotion": "excitement/energy",
        "predicted_views": "500K - 2M",
        "platforms": ["TikTok", "Instagram Reels", "YouTube Shorts"],
        "hashtags": ["#Viral", "#Entertainment", "#MustWatch", "#Trending", "#ForYou"],
        "audio_peaks": [5.5, 7.2, 9.8],
        "face_emotions": {"excitement": 0.92, "joy": 0.88, "surprise": 0.75}
    },
    {
        "id": 2,
        "start": 0.0,
        "end": 5.0,
        "title": "Opening Hook - Attention Grabber",
        "description": "Strong opening sequence that hooks viewers in the first 3 seconds. Perfect for ads and promos.",
        "transcript": "[Music intro] [Visual hook] [Brand moment]",
        "score": 0.91,
        "emotion": "intrigue/curiosity",
        "predicted_views": "200K - 800K",
        "platforms": ["TikTok", "Twitter/X", "Facebook"],
        "hashtags": ["#Hook", "#Intro", "#MustSee", "#Entertainment", "#Viral"],
        "audio_peaks": [1.2, 3.5, 4.8],
        "face_emotions": {"interest": 0.89, "anticipation": 0.82, "engagement": 0.85}
    },
    {
        "id": 3,
        "start": 8.0,
        "end": 15.0,
        "title": "Climax & Finale - Share-Worthy Ending",
        "description": "Powerful climax leading to memorable ending. High share potential.",
        "transcript": "[Climax build] [Peak moment] [Satisfying conclusion]",
        "score": 0.89,
        "emotion": "satisfaction/awe",
        "predicted_views": "150K - 500K",
        "platforms": ["YouTube Shorts", "Instagram", "TikTok"],
        "hashtags": ["#Climax", "#Satisfying", "#Worth", "#Entertainment", "#Ending"],
        "audio_peaks": [9.0, 11.5, 14.0],
        "face_emotions": {"awe": 0.86, "satisfaction": 0.91, "joy": 0.78}
    },
]

# ============== COMPLIANCE AGENT DATA ==============
# Compliance scan results for entertainment content
SAMPLE_COMPLIANCE_ISSUES = [
    {
        "type": "music_rights",
        "severity": "info",
        "timestamp": "00:00 - 00:15",
        "description": "Music content detected - verify licensing",
        "context": "Audio track contains music. Ensure proper licensing for broadcast/streaming.",
        "fcc_rule": "Music Licensing Requirements",
        "fine_range": "N/A - Licensing required",
        "recommendation": "Verify music rights through ASCAP/BMI or use royalty-free alternatives",
        "precedent": "Standard practice for all music-containing content",
        "auto_detected": True,
        "confidence": 0.97
    },
    {
        "type": "content_rating",
        "severity": "info",
        "timestamp": "Full duration",
        "description": "Content suitable for general audiences",
        "context": "No mature content, violence, or inappropriate material detected.",
        "fcc_rule": "Content Rating Guidelines",
        "fine_range": "N/A",
        "recommendation": "Content cleared for all audiences - G/PG equivalent",
        "precedent": "Safe for broadcast without restrictions",
        "auto_detected": True,
        "confidence": 0.99
    },
]

# ============== SOCIAL PUBLISHING AGENT DATA ==============
# Generated social media posts for the entertainment video
SAMPLE_SOCIAL_POSTS = {
    "product_launch": [
        {
            "platform": "TikTok",
            "content": "This hit different. Wait for the drop.\n\n#fyp #viral #entertainment #mustsee #trending #foryou",
            "char_count": 78,
            "best_time": "7:00 PM",
            "predicted_engagement": "250K"
        },
        {
            "platform": "Instagram",
            "content": "When the beat drops just right.\n\nSave this for later. You'll thank us.\n\n#Entertainment #Viral #MustWatch #Trending #Reels #ForYou #Content #Mood",
            "char_count": 156,
            "best_time": "12:00 PM",
            "predicted_engagement": "85K"
        },
        {
            "platform": "Twitter/X",
            "content": "POV: You just found your new favorite clip.\n\nThe energy in this one is unmatched.\n\n#Viral #Entertainment #MustWatch",
            "char_count": 118,
            "best_time": "6:00 PM",
            "predicted_engagement": "45K"
        },
        {
            "platform": "YouTube Shorts",
            "content": "This is the content you've been waiting for. Full video dropping soon. #shorts #viral #entertainment",
            "char_count": 102,
            "best_time": "3:00 PM",
            "predicted_engagement": "180K"
        },
        {
            "platform": "Facebook",
            "content": "Sometimes you come across content that just hits different.\n\nThis is one of those moments. Watch until the end - trust us.\n\nTag someone who needs to see this!",
            "char_count": 198,
            "best_time": "1:00 PM",
            "predicted_engagement": "35K"
        },
    ]
}

# ============== LOCALIZATION AGENT DATA ==============
# Translations for the entertainment content
SAMPLE_TRANSLATIONS = {
    "es": {
        "name": "Spanish",
        "flag": "\U0001f1ea\U0001f1f8",
        "sample_original": "[Music starts - upbeat tempo] [Dynamic visual sequence begins]",
        "sample_translated": "[Comienza la musica - ritmo animado] [Inicia secuencia visual dinamica]",
        "quality_score": 97,
        "notes": "Entertainment terminology localized for Latin American audience.",
        "voice_available": True,
        "dialect_options": ["Spain", "Mexico", "Argentina"]
    },
    "fr": {
        "name": "French",
        "flag": "\U0001f1eb\U0001f1f7",
        "sample_original": "[Music starts - upbeat tempo] [Dynamic visual sequence begins]",
        "sample_translated": "[La musique commence - tempo entrainant] [Debut de la sequence visuelle dynamique]",
        "quality_score": 96,
        "notes": "Adapted for French entertainment market conventions.",
        "voice_available": True,
        "dialect_options": ["France", "Canada", "Belgium"]
    },
    "de": {
        "name": "German",
        "flag": "\U0001f1e9\U0001f1ea",
        "sample_original": "[Music starts - upbeat tempo] [Dynamic visual sequence begins]",
        "sample_translated": "[Musik beginnt - beschwingendes Tempo] [Dynamische visuelle Sequenz startet]",
        "quality_score": 95,
        "notes": "German localization with appropriate entertainment terminology.",
        "voice_available": True,
        "dialect_options": ["Germany", "Austria", "Switzerland"]
    },
    "zh": {
        "name": "Chinese (Simplified)",
        "flag": "\U0001f1e8\U0001f1f3",
        "sample_original": "[Music starts - upbeat tempo] [Dynamic visual sequence begins]",
        "sample_translated": "[音乐开始 - 欢快节奏] [动态视觉序列开始]",
        "quality_score": 94,
        "notes": "Simplified Chinese adapted for mainland entertainment market.",
        "voice_available": True,
        "dialect_options": ["Mandarin", "Cantonese"]
    },
    "ja": {
        "name": "Japanese",
        "flag": "\U0001f1ef\U0001f1f5",
        "sample_original": "[Music starts - upbeat tempo] [Dynamic visual sequence begins]",
        "sample_translated": "[音楽スタート - アップテンポ] [ダイナミックなビジュアルシーケンス開始]",
        "quality_score": 95,
        "notes": "Japanese entertainment style localization.",
        "voice_available": True,
        "dialect_options": ["Standard Japanese"]
    },
    "ko": {
        "name": "Korean",
        "flag": "\U0001f1f0\U0001f1f7",
        "sample_original": "[Music starts - upbeat tempo] [Dynamic visual sequence begins]",
        "sample_translated": "[음악 시작 - 업비트 템포] [다이나믹한 비주얼 시퀀스 시작]",
        "quality_score": 96,
        "notes": "Korean localization optimized for K-entertainment market.",
        "voice_available": True,
        "dialect_options": ["Standard Korean"]
    },
    "pt": {
        "name": "Portuguese",
        "flag": "\U0001f1e7\U0001f1f7",
        "sample_original": "[Music starts - upbeat tempo] [Dynamic visual sequence begins]",
        "sample_translated": "[Musica comeca - ritmo animado] [Sequencia visual dinamica inicia]",
        "quality_score": 96,
        "notes": "Brazilian Portuguese for entertainment content.",
        "voice_available": True,
        "dialect_options": ["Brazil", "Portugal"]
    },
    "hi": {
        "name": "Hindi",
        "flag": "\U0001f1ee\U0001f1f3",
        "sample_original": "[Music starts - upbeat tempo] [Dynamic visual sequence begins]",
        "sample_translated": "[संगीत शुरू - तेज़ ताल] [गतिशील दृश्य क्रम शुरू]",
        "quality_score": 93,
        "notes": "Hindi localization for Indian entertainment audience.",
        "voice_available": True,
        "dialect_options": ["Standard Hindi"]
    },
}

# ============== RIGHTS AGENT DATA ==============
# License and rights info for the entertainment content
SAMPLE_LICENSES = [
    {
        "id": "LIC-ENT-001",
        "title": "Original Content - Full Rights",
        "licensor": "Internal Production",
        "type": "Full Ownership",
        "rights": ["Broadcast", "Digital", "Social Media", "Streaming", "Modification"],
        "territories": ["Worldwide"],
        "start_date": "2024-01-01",
        "end_date": "Perpetual",
        "cost": "N/A - Original Content",
        "status": "active",
        "days_remaining": 999,
        "restrictions": "None - Full ownership rights",
        "usage_this_month": 28,
        "compliance_score": 100
    },
    {
        "id": "LIC-ENT-002",
        "title": "Background Music License",
        "licensor": "Premium Music Library",
        "type": "Commercial License",
        "rights": ["Broadcast", "Digital", "Social Media", "Advertising"],
        "territories": ["Worldwide"],
        "start_date": "2024-01-01",
        "end_date": "2025-12-31",
        "cost": "$499/year",
        "status": "active",
        "days_remaining": 320,
        "restrictions": "Attribution not required. Cannot resell music separately.",
        "usage_this_month": 15,
        "compliance_score": 100
    },
]

SAMPLE_VIOLATIONS = [
    {
        "content": "Entertainment Clip - Unauthorized Repost",
        "platform": "TikTok",
        "channel": "@content_stealer_123",
        "url": "tiktok.com/@content_stealer_123/video/xxxxx",
        "detected": "2024-12-15",
        "views": "45,000",
        "status": "DMCA Filed",
        "estimated_damages": "$500 - $2,000",
        "match_confidence": 0.94,
        "content_id_match": True
    },
]

# ============== TRENDING AGENT DATA ==============
# Trending topics relevant to the entertainment content
SAMPLE_TRENDS = [
    {
        "topic": "#Entertainment",
        "category": "Entertainment",
        "velocity": "Rising",
        "velocity_score": 82,
        "volume": "125K posts/hour",
        "sentiment": "Positive",
        "sentiment_score": 0.78,
        "top_posts": ["New releases trending", "Viral content today", "Must-watch moments"],
        "our_coverage": True,
        "recommendation": "Perfect timing! Entertainment content is trending. Post now for maximum reach.",
        "related_topics": ["#Viral", "#MustWatch", "#Trending", "#Content"],
        "demographics": {"18-24": 35, "25-34": 32, "35-44": 18, "45-54": 10, "55+": 5}
    },
    {
        "topic": "#ViralContent",
        "category": "Social Media",
        "velocity": "Exploding",
        "velocity_score": 91,
        "volume": "200K posts/hour",
        "sentiment": "Excited",
        "sentiment_score": 0.85,
        "top_posts": ["This is going viral", "Can't stop watching", "Share this now"],
        "our_coverage": True,
        "recommendation": "High viral potential detected. Your content matches current viral patterns.",
        "related_topics": ["#ForYou", "#FYP", "#Trending", "#MustSee"],
        "demographics": {"18-24": 42, "25-34": 35, "35-44": 15, "45-54": 5, "55+": 3}
    },
    {
        "topic": "#WeekendVibes",
        "category": "Lifestyle",
        "velocity": "Steady",
        "velocity_score": 68,
        "volume": "85K posts/hour",
        "sentiment": "Positive",
        "sentiment_score": 0.72,
        "top_posts": ["Weekend mood", "Good vibes only", "Entertainment time"],
        "our_coverage": True,
        "recommendation": "Content aligns with weekend entertainment trends. Schedule for Friday-Sunday.",
        "related_topics": ["#Weekend", "#Mood", "#Vibes", "#Fun"],
        "demographics": {"18-24": 28, "25-34": 38, "35-44": 20, "45-54": 9, "55+": 5}
    },
]

# ============== ARCHIVE AGENT DATA ==============
# Archive metadata for the entertainment content
SAMPLE_ARCHIVE_METADATA = {
    "title": "Entertainment Showcase - Dynamic Performance",
    "duration": "0:15",
    "speakers": ["Audio Track"],
    "topics": ["entertainment", "music", "performance", "visual content"],
    "ai_tags": ["entertainment", "dynamic", "high-energy", "music", "visual", "trending", "viral-potential"],
    "sentiment": "positive/energetic",
    "quality": "HD 1080p",
    "content_type": "Entertainment",
    "target_audience": "General audience, 18-44",
    "brand_safety": "Safe for all audiences",
    "viral_score": 0.92,
    "best_platforms": ["TikTok", "Instagram Reels", "YouTube Shorts"]
}

def get_demo_video_path():
    """Get the full path to the demo sample video."""
    base_dir = Path(__file__).parent
    return base_dir / DEMO_SAMPLE_VIDEO["path"]

def is_demo_video_available():
    """Check if the demo video file exists."""
    return get_demo_video_path().exists()
