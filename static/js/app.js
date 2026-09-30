/**
 * ClickBait Shield AI — Client Application Controller
 * Handles headline forensics, token saliency, multi-model consensus, batch processing, and print generation.
 */

// DOM Elements
const inputHeadline = document.getElementById("headline-input");
const btnAnalyze = document.getElementById("btn-analyze");
const btnClear = document.getElementById("btn-clear");
const analysisLoading = document.getElementById("analysis-loading");
const resultsContainer = document.getElementById("results-container");

// Verdict Elements
const scoreCircle = document.getElementById("score-circle");
const consensusScore = document.getElementById("consensus-score");
const threatBadge = document.getElementById("threat-level-badge");
const modelsConsensusText = document.getElementById("models-consensus-text");
const displayHeadline = document.getElementById("display-headline");
const actionableVerdict = document.getElementById("actionable-verdict");
const latencyVal = document.getElementById("latency-val");
const scanIdVal = document.getElementById("scan-id-val");
const timestampVal = document.getElementById("timestamp-val");
const verdictBanner = document.getElementById("verdict-banner");

// Explainability & Saliency Elements
const saliencyHeatmap = document.getElementById("saliency-heatmap");
const primarySummaryText = document.getElementById("primary-summary-text");
const psychologicalList = document.getElementById("psychological-list");
const syntacticList = document.getElementById("syntactic-list");
const factualList = document.getElementById("factual-list");
const modelsGrid = document.getElementById("models-grid");

// Action Buttons
const btnPrintAnalysis = document.getElementById("btn-print-analysis");
const btnCopySummary = document.getElementById("btn-copy-summary");
const printDossier = document.getElementById("print-dossier");

// Navigation Tabs
const navTabs = document.querySelectorAll(".nav-tab");
const viewPanels = {
  single: document.getElementById("view-single"),
  batch: document.getElementById("view-batch"),
  benchmarks: document.getElementById("view-benchmarks")
};

// Extension Modal
const btnShowExtModal = document.getElementById("btn-show-extension-modal");
const extModal = document.getElementById("extension-modal");
const btnCloseModal = document.getElementById("btn-close-modal");
const btnCloseModalBottom = document.getElementById("btn-close-modal-bottom");

// Batch Elements
const batchInput = document.getElementById("batch-input");
const btnRunBatch = document.getElementById("btn-run-batch");
const btnBatchSample = document.getElementById("btn-batch-sample");
const batchStats = document.getElementById("batch-stats");
const batchTableContainer = document.getElementById("batch-results-table-container");
const batchTableBody = document.getElementById("batch-table-body");

// Benchmark Elements
const benchmarksTbody = document.getElementById("benchmarks-tbody");

// Current active verdict state
let currentVerdict = null;

// ================= Tab Navigation =================
navTabs.forEach(tab => {
  tab.addEventListener("click", () => {
    const target = tab.getAttribute("data-tab");
    navTabs.forEach(t => t.classList.remove("active"));
    tab.classList.add("active");

    Object.keys(viewPanels).forEach(key => {
      viewPanels[key].classList.toggle("active", key === target);
    });

    if (target === "benchmarks" && benchmarksTbody.children.length === 0) {
      loadBenchmarks();
    }
  });
});

// ================= Core Analysis Logic =================
async function analyzeHeadline(text) {
  const headline = (text !== undefined ? text : inputHeadline.value).trim();
  if (!headline) return;

  analysisLoading.classList.remove("hidden");
  resultsContainer.style.opacity = "0.4";

  try {
    const res = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ headline })
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Analysis failed");
    }

    const data = await res.json();
    currentVerdict = data;
    renderAnalysis(data);
  } catch (error) {
    alert("Error evaluating headline: " + error.message);
  } finally {
    analysisLoading.classList.add("hidden");
    resultsContainer.style.opacity = "1";
  }
}

function renderAnalysis(data) {
  // Update Header & Verdict
  displayHeadline.textContent = `"${data.headline}"`;
  consensusScore.textContent = Math.round(data.consensus_score);
  threatBadge.textContent = data.threat_level;
  actionableVerdict.textContent = data.explicable_analysis.actionable_verdict;
  latencyVal.textContent = `${data.ensemble_latency_ms} ms`;
  scanIdVal.textContent = data.id;
  timestampVal.textContent = data.timestamp;

  // Visual classes
  verdictBanner.className = "card verdict-card";
  scoreCircle.className = "score-circle";
  threatBadge.className = "threat-pill";

  const agreeingModels = data.model_results.filter(m => (m.score >= 0.5) === data.is_clickbait).length;
  modelsConsensusText.textContent = `${agreeingModels}/5 Models in Strong Consensus`;

  if (data.consensus_score >= 75) {
    verdictBanner.classList.add("critical");
    scoreCircle.classList.add("critical");
    threatBadge.classList.add("critical");
  } else if (data.consensus_score >= 50) {
    verdictBanner.classList.add("moderate");
    scoreCircle.classList.add("moderate");
    threatBadge.classList.add("moderate");
  } else {
    verdictBanner.classList.add("safe");
    scoreCircle.classList.add("safe");
    threatBadge.classList.add("safe");
  }

  // Render Saliency Heatmap
  saliencyHeatmap.innerHTML = "";
  data.tokens.forEach(t => {
    const span = document.createElement("span");
    span.className = `saliency-token ${t.category}`;
    span.textContent = t.token;
    span.title = `${t.token}: ${t.explanation || t.category} (${t.attribution_percent}%)`;
    saliencyHeatmap.appendChild(span);
  });

  // Render Explainable Justification (XAI)
  primarySummaryText.textContent = data.explicable_analysis.primary_summary;

  renderBulletList(psychologicalList, data.explicable_analysis.psychological_levers);
  renderBulletList(syntacticList, data.explicable_analysis.syntactic_signals);
  renderBulletList(factualList, data.explicable_analysis.factual_anchors);

  // Render 5-Model Cards
  modelsGrid.innerHTML = "";
  data.model_results.forEach(m => {
    const isCb = m.prediction === "Clickbait";
    const card = document.createElement("div");
    card.className = "model-card";
    card.innerHTML = `
      <div class="model-card-header">
        <div>
          <h4 class="model-name">${m.name}</h4>
          <span class="model-arch">${m.model_type}</span>
        </div>
        <span class="model-pred-pill ${isCb ? 'clickbait' : 'legitimate'}">${m.prediction}</span>
      </div>

      <div class="model-score-row">
        <span class="model-score-num">${m.percentage}%</span>
        <span class="subtle-tag">${m.confidence} Confidence</span>
      </div>

      <div class="model-meta-row">
        <span>Latency: ${m.latency_ms}ms</span>
        <span>Weight: ${Math.round(m.weight_in_consensus * 100)}%</span>
      </div>

      <ul class="model-factors-list">
        ${m.key_factors.map(f => `<li>${f}</li>`).join('')}
      </ul>
    `;
    modelsGrid.appendChild(card);
  });

  // Prepare Print Dossier for window.print()
  preparePrintDossier(data);
}

function renderBulletList(container, items) {
  container.innerHTML = "";
  if (!items || items.length === 0) {
    const li = document.createElement("li");
    li.textContent = "None detected";
    container.appendChild(li);
    return;
  }
  items.forEach(item => {
    const li = document.createElement("li");
    li.textContent = item;
    container.appendChild(li);
  });
}

// ================= Printable Report Generator =================
function preparePrintDossier(data) {
  printDossier.innerHTML = `
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #000; padding: 20px;">
      <div style="border-bottom: 2px solid #000; padding-bottom: 10px; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: flex-start;">
        <div>
          <h1 style="font-size: 20pt; margin: 0; font-weight: 800;">ClickBait Shield AI</h1>
          <div style="font-size: 10pt; color: #444;">Multi-Model Forensic Verification & Linguistic Attribution Dossier</div>
        </div>
        <div style="text-align: right; font-family: monospace; font-size: 9pt;">
          <div>Scan ID: ${data.id}</div>
          <div>Date: ${data.timestamp}</div>
          <div>Ensemble Latency: ${data.ensemble_latency_ms} ms</div>
        </div>
      </div>

      <div style="background: #f4f4f4; border-left: 4px solid #000; padding: 10px 14px; margin-bottom: 16px;">
        <div style="font-size: 8.5pt; text-transform: uppercase; font-weight: 700; color: #555;">Evaluated Headline Under Forensic Test</div>
        <div style="font-size: 13pt; font-weight: 700; margin-top: 4px;">"${data.headline}"</div>
      </div>

      <div style="border: 1px solid #ccc; padding: 14px; margin-bottom: 16px; display: flex; gap: 20px; align-items: center;">
        <div style="text-align: center; border-right: 1px solid #ccc; padding-right: 20px;">
          <div style="font-size: 32pt; font-weight: 900; line-height: 1;">${data.consensus_score}%</div>
          <div style="font-size: 8pt; text-transform: uppercase; font-weight: 700;">Clickbait Threat Index</div>
          <div style="display: inline-block; font-size: 9pt; font-weight: 800; padding: 3px 8px; border: 1px solid #000; margin-top: 6px;">
            ${data.threat_level}
          </div>
        </div>
        <div style="flex: 1;">
          <div style="font-weight: 700; font-size: 11pt; margin-bottom: 4px;">Forensic Assessment:</div>
          <div style="font-size: 9.5pt; margin-bottom: 6px;">${data.explicable_analysis.primary_summary}</div>
          <div style="font-size: 9pt; color: #333;"><b>Actionable Finding:</b> ${data.explicable_analysis.actionable_verdict}</div>
        </div>
      </div>

      <h3 style="font-size: 11pt; border-bottom: 1px solid #ccc; padding-bottom: 4px; margin: 14px 0 8px 0; text-transform: uppercase;">
        1. 5-Model Multi-Architecture Consensus
      </h3>
      <table style="width: 100%; border-collapse: collapse; font-size: 8.5pt; margin-bottom: 14px;">
        <thead>
          <tr style="background: #eee; border: 1px solid #ccc;">
            <th style="padding: 6px; text-align: left;">Architecture</th>
            <th style="padding: 6px; text-align: left;">Verdict</th>
            <th style="padding: 6px; text-align: left;">Probability</th>
            <th style="padding: 6px; text-align: left;">Confidence</th>
            <th style="padding: 6px; text-align: left;">Latency</th>
            <th style="padding: 6px; text-align: left;">Key Factors & Decision Rules</th>
          </tr>
        </thead>
        <tbody>
          ${data.model_results.map(m => `
            <tr style="border: 1px solid #ccc;">
              <td style="padding: 5px 6px;"><b>${m.name}</b><br><small style="color: #666;">${m.model_type}</small></td>
              <td style="padding: 5px 6px; font-weight: bold;">${m.prediction}</td>
              <td style="padding: 5px 6px; font-weight: bold;">${m.percentage}%</td>
              <td style="padding: 5px 6px;">${m.confidence}</td>
              <td style="padding: 5px 6px;">${m.latency_ms}ms</td>
              <td style="padding: 5px 6px;">${m.key_factors.join('; ')}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>

      <h3 style="font-size: 11pt; border-bottom: 1px solid #ccc; padding-bottom: 4px; margin: 14px 0 8px 0; text-transform: uppercase;">
        2. Word-by-Word Linguistic Attribution Table
      </h3>
      <table style="width: 100%; border-collapse: collapse; font-size: 8.5pt; margin-bottom: 14px;">
        <thead>
          <tr style="background: #eee; border: 1px solid #ccc;">
            <th style="padding: 5px 6px; text-align: left;">Token</th>
            <th style="padding: 5px 6px; text-align: left;">Score</th>
            <th style="padding: 5px 6px; text-align: left;">Classification</th>
            <th style="padding: 5px 6px; text-align: left;">Impact %</th>
            <th style="padding: 5px 6px; text-align: left;">Forensic Role / Explanation</th>
          </tr>
        </thead>
        <tbody>
          ${data.tokens.map(t => `
            <tr style="border: 1px solid #ccc;">
              <td style="padding: 4px 6px;"><b>${t.token}</b></td>
              <td style="padding: 4px 6px;">${t.score}</td>
              <td style="padding: 4px 6px; text-transform: uppercase; font-size: 7.5pt; font-weight: bold;">${t.category}</td>
              <td style="padding: 4px 6px;">${t.attribution_percent}%</td>
              <td style="padding: 4px 6px;">${t.explanation || 'Neutral lexical element'}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>

      <div style="border-top: 1px solid #ccc; padding-top: 8px; font-size: 8pt; color: #666; display: flex; justify-content: space-between;">
        <span>ClickBait Shield AI — Certified Multi-Model Machine Learning Engine</span>
        <span>Page 1 of 1</span>
      </div>
    </div>
  `;
}

// Print Button
btnPrintAnalysis.addEventListener("click", () => {
  if (!currentVerdict) return;
  // Trigger standard browser print which invokes @media print
  window.print();
});

// Copy Summary
btnCopySummary.addEventListener("click", () => {
  if (!currentVerdict) return;
  const summary = `ClickBait Shield AI Forensic Analysis\nHeadline: "${currentVerdict.headline}"\nScore: ${currentVerdict.consensus_score}% (${currentVerdict.threat_level})\nVerdict: ${currentVerdict.explicable_analysis.actionable_verdict}`;
  navigator.clipboard.writeText(summary).then(() => {
    btnCopySummary.textContent = "Copied!";
    setTimeout(() => {
      btnCopySummary.innerHTML = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg> Copy Summary`;
    }, 2000);
  });
});

// Input Event Handlers
btnAnalyze.addEventListener("click", () => analyzeHeadline());
inputHeadline.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    analyzeHeadline();
  }
});

btnClear.addEventListener("click", () => {
  inputHeadline.value = "";
  inputHeadline.focus();
});

// Preset Chips
document.querySelectorAll(".preset-chip").forEach(chip => {
  chip.addEventListener("click", () => {
    const text = chip.getAttribute("data-text");
    inputHeadline.value = text;
    analyzeHeadline(text);
  });
});

// ================= Batch Verification =================
const SAMPLE_BATCH_FEED = [
  "You Won't Believe What She Looked Like After Drinking Celery Juice For 30 Days!",
  "Federal Reserve Cuts Benchmark Interest Rates by 25 Basis Points Amid Easing Inflation",
  "15 Shocking Secrets Flight Attendants Don't Want You To Know (#7 Will Stun You!)",
  "James Webb Space Telescope Detects Water Vapor in Rocky Exoplanet Atmosphere, NASA Reports",
  "This One Simple Kitchen Hack Will Melt Belly Fat Overnight, Doctors Are Furious!",
  "Supreme Court Hands Down 6-3 Ruling on Clean Air Act Regulatory Authority",
  "Why Tech Giants Are Quietly Investing Billions Into Nuclear Micro-Reactors"
];

btnBatchSample.addEventListener("click", () => {
  batchInput.value = SAMPLE_BATCH_FEED.join("\n");
});

btnRunBatch.addEventListener("click", async () => {
  const lines = batchInput.value.split("\n").map(l => l.trim()).filter(l => l.length > 0);
  if (lines.length === 0) {
    alert("Please enter or load headlines to verify.");
    return;
  }

  btnRunBatch.disabled = true;
  btnRunBatch.textContent = "Evaluating Batch...";

  try {
    const res = await fetch("/api/batch", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ headlines: lines })
    });

    if (!res.ok) throw new Error("Batch request failed");
    const data = await res.json();

    batchStats.textContent = `Scanned ${data.total} Headlines: ${data.clickbait_count} Flagged as Clickbait (${Math.round((data.clickbait_count / data.total) * 100)}%), Avg Risk: ${data.average_risk_score}%`;
    batchTableContainer.classList.remove("hidden");
    batchTableBody.innerHTML = "";

    data.results.forEach((r, idx) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td style="color: var(--text-muted); font-family: var(--font-mono);">${idx + 1}</td>
        <td style="max-width: 480px; font-weight: 500;">${r.headline}</td>
        <td>
          <span style="font-weight: 700; color: ${r.consensus_score >= 75 ? 'var(--rose-400)' : r.consensus_score >= 50 ? 'var(--amber-400)' : 'var(--emerald-400)'};">
            ${r.consensus_score}%
          </span>
        </td>
        <td>
          <span class="threat-pill ${r.consensus_score >= 75 ? 'critical' : r.consensus_score >= 50 ? 'moderate' : 'safe'}" style="font-size: 9px;">
            ${r.threat_level}
          </span>
        </td>
        <td>
          <button class="btn-action-secondary btn-inspect" data-headline="${encodeURIComponent(r.headline)}" style="padding: 4px 8px; font-size: 11px;">
            Inspect
          </button>
        </td>
      `;
      batchTableBody.appendChild(tr);
    });

    // Add click listeners to inspect buttons
    document.querySelectorAll(".btn-inspect").forEach(btn => {
      btn.addEventListener("click", () => {
        const text = decodeURIComponent(btn.getAttribute("data-headline"));
        inputHeadline.value = text;
        navTabs[0].click();
        analyzeHeadline(text);
      });
    });

  } catch (err) {
    alert("Batch analysis error: " + err.message);
  } finally {
    btnRunBatch.disabled = false;
    btnRunBatch.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"/></svg> Run Batch Verification`;
  }
});

// ================= Benchmark Matrix =================
async function loadBenchmarks() {
  try {
    const res = await fetch("/api/benchmarks");
    if (!res.ok) throw new Error("Could not fetch benchmarks");
    const list = await res.json();

    benchmarksTbody.innerHTML = "";
    list.forEach(item => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td><strong>${item.name}</strong></td>
        <td><span class="subtle-tag">${item.category}</span></td>
        <td style="color: var(--cyan-400); font-weight: 700;">${item.accuracy}%</td>
        <td>${item.precision}%</td>
        <td>${item.recall}%</td>
        <td style="color: var(--emerald-400); font-weight: 700;">${item.f1_score}%</td>
        <td style="color: var(--amber-400);">${item.latency_ms} ms</td>
        <td>${item.roc_auc.toFixed(3)}</td>
        <td>${item.mcc.toFixed(3)}</td>
      `;
      benchmarksTbody.appendChild(tr);
    });
  } catch (err) {
    console.error("Benchmarks load error:", err);
  }
}

// ================= Modal Handlers =================
btnShowExtModal.addEventListener("click", () => extModal.classList.remove("hidden"));
btnCloseModal.addEventListener("click", () => extModal.classList.add("hidden"));
btnCloseModalBottom.addEventListener("click", () => extModal.classList.add("hidden"));
extModal.addEventListener("click", (e) => {
  if (e.target === extModal) extModal.classList.add("hidden");
});

// Initialize on page load
document.addEventListener("DOMContentLoaded", () => {
  const urlParams = new URLSearchParams(window.location.search);
  const queryHeadline = urlParams.get("headline");
  if (queryHeadline) {
    inputHeadline.value = queryHeadline;
  }
  analyzeHeadline();
});
