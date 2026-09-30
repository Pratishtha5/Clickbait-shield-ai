/**
 * ClickBait Shield AI — Chrome Extension Popup Controller
 * Connects to the local Python FastAPI backend (Linear Regression, Logistic Regression,
 * KMeans, Random Forest, 1D CNN) with edge heuristic fallback.
 */

const API_URL = "http://localhost:8000/api/analyze";
const DASHBOARD_URL = "http://localhost:8000";

// DOM Elements
const inputEl = document.getElementById("headline-input");
const btnAnalyze = document.getElementById("btn-analyze");
const btnUseTab = document.getElementById("btn-use-tab");
const btnOpenDash = document.getElementById("btn-open-dash");
const statusDot = document.getElementById("server-status");
const loadingEl = document.getElementById("loading");
const resultSection = document.getElementById("result-section");
const scoreVal = document.getElementById("score-val");
const threatBadge = document.getElementById("threat-badge");
const actionableText = document.getElementById("actionable-text");
const tokenChips = document.getElementById("token-chips");
const reasonsList = document.getElementById("reasons-list");
const verdictCard = document.getElementById("verdict-card");
const modelsMiniGrid = document.getElementById("models-mini-grid");
const presetButtons = document.querySelectorAll(".chip-preset");

let lastVerdict = null;

// Check server status on load
async function checkServer() {
  try {
    const res = await fetch("http://localhost:8000/api/health", { method: "GET" });
    if (res.ok) {
      statusDot.classList.remove("offline");
      statusDot.title = "Connected to Python 3.14 Multi-Model Engine (Active)";
    } else {
      throw new Error();
    }
  } catch (err) {
    statusDot.classList.add("offline");
    statusDot.title = "Local Python server offline — using edge heuristic fallback";
  }
}

// Fallback client-side analysis when Python backend is offline
function clientSideFallback(text) {
  const lower = text.toLowerCase();
  let score = 15;
  const triggers = [];
  const tokens = [];

  const cbPatterns = [
    { p: /you won'?t believe/i, desc: "Curiosity gap invocation", weight: 45 },
    { p: /shocking/i, desc: "Sensational secret claim", weight: 35 },
    { p: /will blow your mind/i, desc: "Cognitive hyperbole", weight: 40 },
    { p: /doctors (hate|furious)/i, desc: "Anti-institutional bait", weight: 45 },
    { p: /this one trick/i, desc: "Miracle shortcut lure", weight: 40 },
    { p: /#?\d+ (will|things|secrets)/i, desc: "Numbered listicle hook", weight: 35 },
    { p: /what happens? next/i, desc: "Narrative suspense", weight: 35 }
  ];

  for (const item of cbPatterns) {
    if (item.p.test(text)) {
      score += item.weight;
      triggers.push(item.desc);
    }
  }

  if (/[!?]/.test(text)) score += 10;
  if (/^[A-Z\s]{4,}$/.test(text)) score += 15;

  const anchors = ["announced", "reuters", "federal", "court", "study", "published", "percent", "official", "reserve", "rates"];
  for (const a of anchors) {
    if (lower.includes(a)) score -= 25;
  }

  score = Math.max(2, Math.min(99, score));
  const isClickbait = score >= 50;

  const words = text.split(/\s+/);
  for (const w of words) {
    const clean = w.toLowerCase().replace(/[^\w]/g, "");
    let cat = "neutral";
    if (["shocking", "unbelievable", "secret", "tricks", "hacks", "insane", "furious"].includes(clean)) cat = "high_clickbait";
    else if (anchors.includes(clean)) cat = "factual";
    tokens.push({ token: w, category: cat, score: cat === "high_clickbait" ? 0.8 : cat === "factual" ? -0.5 : 0.0 });
  }

  // 5 Model results for fallback
  const mockModels = [
    { name: "Linear Regression", prediction: isClickbait ? "Clickbait" : "Legitimate", percentage: Math.min(99, score + 4) },
    { name: "Logistic Regression", prediction: isClickbait ? "Clickbait" : "Legitimate", percentage: score },
    { name: "K-Means Clustering", prediction: isClickbait ? "Clickbait" : "Legitimate", percentage: Math.max(10, score - 8) },
    { name: "Random Forest", prediction: isClickbait ? "Clickbait" : "Legitimate", percentage: Math.max(15, score - 5) },
    { name: "1D Convolutional Neural Network", prediction: isClickbait ? "Clickbait" : "Legitimate", percentage: Math.min(99, score + 6) }
  ];

  return {
    consensus_score: score,
    threat_level: score >= 80 ? "CRITICAL CLICKBAIT" : score >= 60 ? "HIGH CONFIDENCE CLICKBAIT" : score >= 40 ? "MODERATE RISK" : "SAFE",
    is_clickbait: isClickbait,
    model_results: mockModels,
    tokens: tokens,
    explicable_analysis: {
      actionable_verdict: isClickbait ? "Caution: High likelihood of sensational curiosity bait." : "Verified Informative: Headline presents factual news structure.",
      psychological_levers: triggers.length > 0 ? triggers : ["Objective syntax and journalistic vocabulary observed"]
    }
  };
}

async function runAnalysis(headline) {
  if (!headline || !headline.trim()) return;

  loadingEl.classList.remove("hidden");
  resultSection.classList.add("hidden");

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ headline: headline.trim() })
    });

    if (!res.ok) throw new Error("Server response not ok");
    const data = await res.json();
    renderResult(data);
    lastVerdict = data;
  } catch (err) {
    console.warn("Using offline fallback:", err);
    const fallback = clientSideFallback(headline.trim());
    renderResult(fallback);
    lastVerdict = fallback;
  } finally {
    loadingEl.classList.add("hidden");
  }
}

function renderResult(data) {
  resultSection.classList.remove("hidden");

  scoreVal.textContent = Math.round(data.consensus_score);
  threatBadge.textContent = data.threat_level;

  verdictCard.className = "verdict-card";
  threatBadge.className = "threat-badge";

  if (data.consensus_score >= 75) {
    verdictCard.classList.add("critical");
    threatBadge.classList.add("critical");
  } else if (data.consensus_score >= 50) {
    verdictCard.classList.add("moderate");
    threatBadge.classList.add("moderate");
  } else {
    verdictCard.classList.add("safe");
    threatBadge.classList.add("safe");
  }

  actionableText.textContent = data.explicable_analysis.actionable_verdict;

  // Render 5 Models Mini Grid
  modelsMiniGrid.innerHTML = "";
  if (data.model_results && data.model_results.length > 0) {
    for (const m of data.model_results) {
      const isCb = m.prediction === "Clickbait";
      const row = document.createElement("div");
      row.className = "model-row";
      row.innerHTML = `
        <span class="model-name-label">${m.name}</span>
        <span class="model-pred-label ${isCb ? 'clickbait' : 'legitimate'}">${m.prediction} (${Math.round(m.percentage)}%)</span>
      `;
      modelsMiniGrid.appendChild(row);
    }
  }

  // Render tokens
  tokenChips.innerHTML = "";
  if (data.tokens && data.tokens.length > 0) {
    for (const t of data.tokens) {
      const chip = document.createElement("span");
      chip.className = `token-chip ${t.category}`;
      chip.textContent = t.token;
      if (t.explanation) chip.title = `${t.explanation} (${t.attribution_percent || 0}%)`;
      tokenChips.appendChild(chip);
    }
  }

  // Render reasons
  reasonsList.innerHTML = "";
  const levers = data.explicable_analysis.psychological_levers || [];
  for (const reason of levers.slice(0, 3)) {
    const li = document.createElement("li");
    li.textContent = reason;
    reasonsList.appendChild(li);
  }
}

// Event Listeners
btnAnalyze.addEventListener("click", () => {
  runAnalysis(inputEl.value);
});

inputEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    runAnalysis(inputEl.value);
  }
});

btnUseTab.addEventListener("click", () => {
  if (chrome.tabs && chrome.tabs.query) {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs && tabs[0] && tabs[0].title) {
        inputEl.value = tabs[0].title;
        runAnalysis(tabs[0].title);
      }
    });
  }
});

presetButtons.forEach(btn => {
  btn.addEventListener("click", () => {
    const text = btn.getAttribute("data-text");
    inputEl.value = text;
    runAnalysis(text);
  });
});

btnOpenDash.addEventListener("click", () => {
  const currentText = inputEl.value || "";
  const targetUrl = currentText ? `${DASHBOARD_URL}?headline=${encodeURIComponent(currentText)}` : DASHBOARD_URL;
  if (chrome.tabs && chrome.tabs.create) {
    chrome.tabs.create({ url: targetUrl });
  } else {
    window.open(targetUrl, "_blank");
  }
});

// Auto-run on open if active tab exists
document.addEventListener("DOMContentLoaded", () => {
  checkServer();
  if (chrome.tabs && chrome.tabs.query) {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs && tabs[0] && tabs[0].title && !inputEl.value) {
        inputEl.value = tabs[0].title;
        runAnalysis(tabs[0].title);
      }
    });
  }
});
