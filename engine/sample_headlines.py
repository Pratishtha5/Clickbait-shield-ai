"""
ClickBait Shield AI — Curated Sample Headlines for Testing
"""
from typing import List, Dict

SAMPLE_HEADLINES: List[Dict[str, str]] = [
    {
        "title": "You Won't Believe What She Looked Like After Drinking Celery Juice For 30 Days!",
        "category": "Clickbait",
        "expectedRisk": "Critical Clickbait (98%)",
        "source": "Viral Health Trends"
    },
    {
        "title": "15 Shocking Secrets Flight Attendants Don't Want You To Know (#7 Will Stun You!)",
        "category": "Clickbait",
        "expectedRisk": "High Confidence Clickbait (95%)",
        "source": "BuzzFeed Travel"
    },
    {
        "title": "This One Simple Kitchen Hack Will Melt Belly Fat Overnight, Doctors Are Furious!",
        "category": "Clickbait",
        "expectedRisk": "Critical Clickbait (99%)",
        "source": "DailyMiracleFeed"
    },
    {
        "title": "Federal Reserve Cuts Benchmark Interest Rates by 25 Basis Points Amid Easing Inflation",
        "category": "Legitimate",
        "expectedRisk": "Safe (4%)",
        "source": "Reuters Financial"
    },
    {
        "title": "James Webb Space Telescope Detects Water Vapor in Rocky Exoplanet Atmosphere, NASA Reports",
        "category": "Legitimate",
        "expectedRisk": "Safe (2%)",
        "source": "Nature Astronomy"
    },
    {
        "title": "Supreme Court Hands Down 6-3 Ruling on Clean Air Act Regulatory Authority",
        "category": "Legitimate",
        "expectedRisk": "Safe (5%)",
        "source": "Associated Press"
    },
    {
        "title": "Why Tech Giants Are Quietly Investing Billions Into Nuclear Micro-Reactors",
        "category": "Borderline",
        "expectedRisk": "Moderate Risk (48%)",
        "source": "Tech Wire Analysis"
    },
    {
        "title": "He Walked Into An Abandoned Bank Vault. What He Discovered Inside Shocked The Entire Internet!",
        "category": "Clickbait",
        "expectedRisk": "Critical Clickbait (97%)",
        "source": "UrbanExplorers"
    },
    {
        "title": "European Central Bank Holds Monetary Policy Meeting to Assess Eurozone Growth Outlook",
        "category": "Legitimate",
        "expectedRisk": "Safe (3%)",
        "source": "Financial Times"
    }
]
