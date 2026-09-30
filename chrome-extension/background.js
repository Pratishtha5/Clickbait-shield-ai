/**
 * ClickBait Shield AI — Service Worker (Manifest V3)
 * Handles context menus, badge counts, and communication.
 */

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "check-clickbait-shield",
    title: "🛡️ Analyze Clickbait with Shield AI",
    contexts: ["selection"]
  });
});

// Context menu click opens the Web Studio with prefilled text
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "check-clickbait-shield" && info.selectionText) {
    const query = encodeURIComponent(info.selectionText.trim());
    chrome.tabs.create({
      url: `http://localhost:8000?headline=${query}`
    });
  }
});

// Update extension icon badge count for clickbaits detected on page
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "UPDATE_CLICKBAIT_COUNT" && sender.tab) {
    const count = message.count || 0;
    if (count > 0) {
      chrome.action.setBadgeText({ text: String(count), tabId: sender.tab.id });
      chrome.action.setBadgeBackgroundColor({ color: "#ef4444", tabId: sender.tab.id });
    } else {
      chrome.action.setBadgeText({ text: "", tabId: sender.tab.id });
    }
  }
});
