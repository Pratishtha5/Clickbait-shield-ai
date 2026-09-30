/**
 * ClickBait Shield AI — In-Page Forensic Content Script
 * Scans headlines on news, social, and video feeds to inject instant explainable risk badges.
 */

const BADGE_CLASS = "cb-shield-badge";
const PROCESSED_ATTR = "data-cb-scanned";
const API_URL = "http://localhost:8000/api/analyze";

// Local cache for scanned headlines to avoid duplicate network calls
const headlineCache = new Map();

// Quick client-side scoring heuristic for immediate badge injection
function quickScore(text) {
  if (!text || text.length < 15) return null;
  const lower = text.toLowerCase();
  let score = 15;

  if (/you won'?t believe/i.test(text)) score += 55;
  if (/shocking/i.test(text)) score += 40;
  if (/will blow your mind/i.test(text)) score += 50;
  if (/doctors (hate|furious|don't want)/i.test(text)) score += 55;
  if (/this one trick/i.test(text)) score += 50;
  if (/(#?\d+|top \d+) (will|secrets|reasons|things)/i.test(text)) score += 45;
  if (/what (he|she|they) did next/i.test(text)) score += 50;
  if (/what happens? next/i.test(text)) score += 45;
  if (/broke the internet/i.test(text)) score += 45;
  if (/stop doing this/i.test(text)) score += 40;
  if (/[!?]{2,}/.test(text)) score += 15;

  // Factual anchors
  const anchors = ["announced", "reuters", "federal", "court", "study", "published", "percent", "official", "quarterly", "minister", "president", "nasa", "reserve", "rates"];
  for (const a of anchors) {
    if (lower.includes(a)) score -= 25;
  }

  return Math.max(2, Math.min(99, score));
}

// Create an interactive forensic badge element
function createBadge(score, headlineText) {
  const badge = document.createElement("span");
  badge.className = BADGE_CLASS;

  let label = "SAFE";
  let cls = "safe";

  if (score >= 75) {
    label = `${score}% BAIT`;
    cls = "critical";
  } else if (score >= 45) {
    label = `${score}% RISK`;
    cls = "moderate";
  } else {
    label = `${score}% SAFE`;
    cls = "safe";
  }

  badge.classList.add(cls);
  badge.textContent = `🛡️ ${label}`;
  badge.title = `ClickBait Shield AI: Threat Score ${score}% (${cls.toUpperCase()})\nClick to inspect in Forensic Studio`;

  badge.addEventListener("click", (e) => {
    e.preventDefault();
    e.stopPropagation();
    window.open(`http://localhost:8000?headline=${encodeURIComponent(headlineText)}`, "_blank");
  });

  return badge;
}

// Asynchronously enhance badge with real 5-model consensus from Python server if online
async function enhanceBadgeWithServer(badge, headlineText) {
  if (headlineCache.has(headlineText)) {
    const cached = headlineCache.get(headlineText);
    updateBadge(badge, cached);
    return;
  }

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ headline: headlineText })
    });
    if (res.ok) {
      const data = await res.json();
      headlineCache.set(headlineText, data);
      updateBadge(badge, data);
    }
  } catch (e) {
    // Keep quickScore heuristic if server offline
  }
}

function updateBadge(badge, data) {
  const score = Math.round(data.consensus_score);
  badge.className = BADGE_CLASS;

  let cls = "safe";
  if (score >= 75) {
    cls = "critical";
  } else if (score >= 45) {
    cls = "moderate";
  }

  badge.classList.add(cls);
  badge.textContent = `🛡️ ${score}% ${cls === 'critical' ? 'BAIT' : cls === 'moderate' ? 'RISK' : 'SAFE'}`;
  badge.title = `ClickBait Shield AI: ${data.threat_level} (${score}%)\nModels: ${data.model_results ? data.model_results.map(m => m.name + ': ' + m.prediction).join(', ') : ''}\nClick to view full forensic report.`;
}

// Headline Scanner across feeds
function scanHeadlines() {
  const selectors = [
    "ytd-rich-grid-media #video-title",
    "ytd-video-renderer #video-title",
    "#video-title",
    "shreddit-post a[slot='title']",
    "div[data-testid='post-container'] h3",
    "article h1, article h2, article h3",
    "main h1, main h2, main h3",
    ".title",
    ".headline"
  ];

  const elements = document.querySelectorAll(selectors.join(", "));
  elements.forEach((el) => {
    if (el.getAttribute(PROCESSED_ATTR)) return;
    el.setAttribute(PROCESSED_ATTR, "true");

    const text = el.innerText ? el.innerText.trim() : "";
    if (text.length > 20 && !el.querySelector(`.${BADGE_CLASS}`)) {
      const initialScore = quickScore(text);
      if (initialScore !== null && initialScore >= 35) {
        const badge = createBadge(initialScore, text);
        el.appendChild(badge);
        enhanceBadgeWithServer(badge, text);
      }
    }
  });

  // Count total clickbaits on page and notify background worker
  const detectedCount = document.querySelectorAll(`.${BADGE_CLASS}.critical, .${BADGE_CLASS}.moderate`).length;
  if (chrome.runtime && chrome.runtime.sendMessage) {
    try {
      chrome.runtime.sendMessage({ type: "UPDATE_CLICKBAIT_COUNT", count: detectedCount });
    } catch (e) {}
  }
}

// Initial scan and observer for infinite-scrolling pages
scanHeadlines();

let throttleTimer = null;
const observer = new MutationObserver(() => {
  if (throttleTimer) return;
  throttleTimer = setTimeout(() => {
    scanHeadlines();
    throttleTimer = null;
  }, 800);
});

if (document.body) {
  observer.observe(document.body, { childList: true, subtree: true });
}
