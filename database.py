"""
MediaAgentIQ Database Setup
"""
import aiosqlite
from pathlib import Path
from datetime import datetime

DATABASE_PATH = Path(__file__).parent / "mediaagentiq.db"


async def init_database():
    """Initialize the SQLite database with required tables."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Jobs table - tracks all agent jobs
        await db.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_type TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                input_file TEXT,
                output_file TEXT,
                result_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                error_message TEXT
            )
        """)

        # Archive table - mock video archive for search
        await db.execute("""
            CREATE TABLE IF NOT EXISTS archive (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                duration INTEGER,
                date_recorded DATE,
                tags TEXT,
                speaker TEXT,
                transcript TEXT,
                thumbnail_url TEXT,
                video_url TEXT
            )
        """)

        # Compliance issues table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS compliance_issues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER,
                issue_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                timestamp_start REAL,
                timestamp_end REAL,
                description TEXT,
                suggestion TEXT,
                FOREIGN KEY (job_id) REFERENCES jobs (id)
            )
        """)

        # Activity log
        await db.execute("""
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_type TEXT NOT NULL,
                action TEXT NOT NULL,
                details TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        await db.commit()

        # Seed demo archive data if empty
        cursor = await db.execute("SELECT COUNT(*) FROM archive")
        count = await cursor.fetchone()
        if count[0] == 0:
            await seed_demo_data(db)


async def seed_demo_data(db):
    """Seed the archive with demo video entries."""
    demo_videos = [
        {
            "title": "Morning News Broadcast - Election Coverage",
            "description": "Live coverage of the 2024 election results with expert analysis",
            "duration": 3600,
            "date_recorded": "2024-11-06",
            "tags": "news,election,politics,live",
            "speaker": "Sarah Johnson",
            "transcript": "Good morning viewers. Today we bring you comprehensive coverage of the election results...",
            "thumbnail_url": "/static/demo/news_thumb.jpg",
            "video_url": "/demo/news_broadcast.mp4"
        },
        {
            "title": "Sports Highlights - Championship Game",
            "description": "Exciting moments from the championship finals",
            "duration": 1800,
            "date_recorded": "2024-10-15",
            "tags": "sports,highlights,championship,football",
            "speaker": "Mike Thompson",
            "transcript": "What an incredible game folks! The championship has been decided...",
            "thumbnail_url": "/static/demo/sports_thumb.jpg",
            "video_url": "/demo/sports_highlights.mp4"
        },
        {
            "title": "Weather Report - Storm Warning",
            "description": "Severe weather alert and safety information",
            "duration": 600,
            "date_recorded": "2024-12-01",
            "tags": "weather,storm,alert,safety",
            "speaker": "Jennifer Lee",
            "transcript": "A major storm system is approaching the region. Residents should take precautions...",
            "thumbnail_url": "/static/demo/weather_thumb.jpg",
            "video_url": "/demo/weather_report.mp4"
        },
        {
            "title": "Interview - Tech Industry Leader",
            "description": "Exclusive interview with leading tech CEO on AI developments",
            "duration": 2400,
            "date_recorded": "2024-11-20",
            "tags": "interview,tech,AI,business,innovation",
            "speaker": "David Chen",
            "transcript": "Thank you for joining us today. Let's discuss the future of artificial intelligence...",
            "thumbnail_url": "/static/demo/interview_thumb.jpg",
            "video_url": "/demo/tech_interview.mp4"
        },
        {
            "title": "Breaking News - Market Update",
            "description": "Live market analysis and economic news",
            "duration": 900,
            "date_recorded": "2024-12-10",
            "tags": "news,finance,markets,economy,breaking",
            "speaker": "Robert Martinez",
            "transcript": "Breaking news from Wall Street. Markets are reacting to the latest economic data...",
            "thumbnail_url": "/static/demo/market_thumb.jpg",
            "video_url": "/demo/market_update.mp4"
        },
        {
            "title": "Documentary - Climate Change Impact",
            "description": "In-depth look at climate change effects on coastal communities",
            "duration": 5400,
            "date_recorded": "2024-09-15",
            "tags": "documentary,climate,environment,science",
            "speaker": "Dr. Emily Watson",
            "transcript": "Climate change is reshaping our coastlines. In this documentary, we explore...",
            "thumbnail_url": "/static/demo/climate_thumb.jpg",
            "video_url": "/demo/climate_doc.mp4"
        }
    ]

    for video in demo_videos:
        await db.execute("""
            INSERT INTO archive (title, description, duration, date_recorded, tags, speaker, transcript, thumbnail_url, video_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            video["title"], video["description"], video["duration"],
            video["date_recorded"], video["tags"], video["speaker"],
            video["transcript"], video["thumbnail_url"], video["video_url"]
        ))

    await db.commit()


async def log_activity(agent_type: str, action: str, details: str = None):
    """Log an activity to the activity log."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT INTO activity_log (agent_type, action, details) VALUES (?, ?, ?)",
            (agent_type, action, details)
        )
        await db.commit()


async def get_recent_activity(limit: int = 10):
    """Get recent activity log entries."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM activity_log ORDER BY created_at DESC LIMIT ?",
            (limit,)
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]


async def create_job(agent_type: str, input_file: str = None):
    """Create a new job entry."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO jobs (agent_type, input_file, status) VALUES (?, ?, 'processing')",
            (agent_type, input_file)
        )
        await db.commit()
        return cursor.lastrowid


async def update_job(job_id: int, status: str, output_file: str = None, result_data: str = None, error_message: str = None):
    """Update a job's status and results."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        if status == "completed":
            await db.execute(
                "UPDATE jobs SET status = ?, output_file = ?, result_data = ?, completed_at = CURRENT_TIMESTAMP WHERE id = ?",
                (status, output_file, result_data, job_id)
            )
        else:
            await db.execute(
                "UPDATE jobs SET status = ?, error_message = ? WHERE id = ?",
                (status, error_message, job_id)
            )
        await db.commit()


async def get_job(job_id: int):
    """Get a job by ID."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
        row = await cursor.fetchone()
        return dict(row) if row else None


async def get_stats():
    """Get dashboard statistics."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        stats = {}

        # Total jobs
        cursor = await db.execute("SELECT COUNT(*) FROM jobs")
        stats["total_jobs"] = (await cursor.fetchone())[0]

        # Completed jobs
        cursor = await db.execute("SELECT COUNT(*) FROM jobs WHERE status = 'completed'")
        stats["completed_jobs"] = (await cursor.fetchone())[0]

        # Jobs by agent type
        cursor = await db.execute("SELECT agent_type, COUNT(*) FROM jobs GROUP BY agent_type")
        stats["jobs_by_agent"] = dict(await cursor.fetchall())

        # Archive size
        cursor = await db.execute("SELECT COUNT(*) FROM archive")
        stats["archive_size"] = (await cursor.fetchone())[0]

        # Compliance issues found
        cursor = await db.execute("SELECT COUNT(*) FROM compliance_issues")
        stats["compliance_issues"] = (await cursor.fetchone())[0]

        return stats
