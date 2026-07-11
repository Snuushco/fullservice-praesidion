(() => {
  const measurementId = "G-G1GHCQVBPJ";
  const consentKey = "praesidion-analytics-consent-v1";
  const storedConsent = localStorage.getItem(consentKey);

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function gtag() {
    window.dataLayer.push(arguments);
  };

  window.gtag("consent", "default", {
    analytics_storage: storedConsent === "granted" ? "granted" : "denied",
    ad_storage: "denied",
    ad_user_data: "denied",
    ad_personalization: "denied",
    wait_for_update: 500,
  });
  window.gtag("js", new Date());
  window.gtag("config", measurementId, {
    send_page_view: storedConsent === "granted",
  });

  const loader = document.createElement("script");
  loader.async = true;
  loader.src = `https://www.googletagmanager.com/gtag/js?id=${measurementId}`;
  document.head.appendChild(loader);

  const updateConsent = (value) => {
    localStorage.setItem(consentKey, value);
    window.gtag("consent", "update", {
      analytics_storage: value === "granted" ? "granted" : "denied",
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied",
    });
    if (value === "granted") {
      window.gtag("event", "page_view", {
        page_location: window.location.href,
        page_title: document.title,
      });
    }
    document.getElementById("analytics-consent-banner")?.remove();
  };

  const showConsentBanner = () => {
    if (storedConsent) return;
    const banner = document.createElement("section");
    banner.id = "analytics-consent-banner";
    banner.setAttribute("role", "dialog");
    banner.setAttribute("aria-label", "Analyticsvoorkeur");
    banner.style.cssText = "position:fixed;z-index:9999;left:16px;right:16px;bottom:16px;max-width:720px;margin:auto;padding:16px;background:#111820;color:#fff;border:1px solid rgba(255,255,255,.25);box-shadow:0 14px 50px rgba(0,0,0,.45);font:15px/1.5 system-ui,sans-serif";
    banner.innerHTML = '<strong>Analyticsvoorkeur</strong><p style="margin:8px 0 14px">Met uw toestemming gebruiken we Google Analytics om de website te verbeteren. Advertentiepersonalisatie blijft uit.</p><div style="display:flex;gap:10px;flex-wrap:wrap"><button type="button" data-consent="granted" style="border:0;padding:10px 14px;font-weight:700;cursor:pointer">Analytics toestaan</button><button type="button" data-consent="denied" style="border:1px solid #fff;background:transparent;color:#fff;padding:10px 14px;font-weight:700;cursor:pointer">Alleen noodzakelijk</button></div>';
    banner.addEventListener("click", (event) => {
      const button = event.target.closest("button[data-consent]");
      if (button) updateConsent(button.dataset.consent);
    });
    document.body.appendChild(banner);
  };

  document.addEventListener("DOMContentLoaded", showConsentBanner, { once: true });
  document.addEventListener("submit", () => {
    if (localStorage.getItem(consentKey) !== "granted") return;
    window.gtag("event", "generate_lead", { lead_type: "form_submit" });
  });
  document.addEventListener("click", (event) => {
    if (localStorage.getItem(consentKey) !== "granted") return;
    const link = event.target.closest("a[href^='mailto:'],a[href^='tel:']");
    if (!link) return;
    window.gtag("event", "generate_lead", {
      lead_type: link.href.startsWith("mailto:") ? "email_click" : "phone_click",
    });
  });
})();
