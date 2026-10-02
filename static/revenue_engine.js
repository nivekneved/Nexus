/**
 * Nexus Revenue & Conversion Engine Client SDK (v3.0)
 * ===================================================
 * Tracks complete funnel telemetry:
 *   view_item -> preview_code -> initiate_checkout -> lead_captured -> order_bump -> payment_attempt -> purchase
 * Automatically rescues abandoned checkouts via debounced lead capture.
 * Powers viral social referral loops.
 */

(function() {
  let _leadCaptureTimer = null;
  let _lastCapturedEmail = null;

  window.NexusRevenue = {
    // 1. Core Conversion Event Tracker
    track: async function(eventName, payload = {}) {
      try {
        const enrichedPayload = {
          ...payload,
          url: window.location.href,
          path: window.location.pathname,
          referrer: document.referrer || "direct",
          user_agent: navigator.userAgent
        };
        await fetch("/api/revenue/track", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ event_name: eventName, payload: enrichedPayload })
        });
      } catch (e) {
        console.debug("Revenue telemetry note:", e);
      }
    },

    // 2. Specialized Funnel Steps
    trackPageView: function(pageName) {
      this.track("page_view", { page: pageName || window.location.pathname });
    },

    trackViewItem: function(item) {
      this.track("view_item", typeof item === "string" ? { product_id: item } : item);
    },

    trackPreview: function(productId, productName) {
      this.track("preview_code", { product_id: productId, product_name: productName });
    },

    trackInitiateCheckout: function(cart) {
      this.track("initiate_checkout", cart);
    },

    trackOrderBump: function(added, details = {}) {
      this.track("order_bump_toggled", { added: Boolean(added), ...details });
    },

    trackPaymentAttempt: function(method, cart) {
      this.track("payment_attempt", { method: method, ...cart });
    },

    trackPurchase: function(orderId, total, currency = "USD", details = {}) {
      this.track("purchase", {
        order_id: orderId,
        total: total,
        currency: currency,
        ...details
      });
    },

    trackDropoff: function(stepName, meta = {}) {
      this.track("dropoff", { step: stepName, ...meta });
    },

    // 3. Debounced Abandoned Lead Capture
    captureLead: async function(contact, cartDetails = {}) {
      if (!contact || (!contact.includes("@") && contact.length < 7)) return;
      if (contact === _lastCapturedEmail) return;
      _lastCapturedEmail = contact;

      try {
        await fetch("/api/revenue/abandoned-lead", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            contact: contact,
            source: "store_checkout_modal",
            cart_details: cartDetails
          })
        });
      } catch (err) {
        console.debug("Lead capture note:", err);
      }
    },

    attachEmailFieldRecovery: function(inputElementOrSelector, getCartFn) {
      const el = typeof inputElementOrSelector === "string" 
        ? document.querySelector(inputElementOrSelector) 
        : inputElementOrSelector;
      if (!el) return;

      const triggerCapture = () => {
        const val = el.value.trim();
        if (val && val.includes("@")) {
          const cart = typeof getCartFn === "function" ? getCartFn() : {};
          this.captureLead(val, cart);
        }
      };

      el.addEventListener("input", () => {
        clearTimeout(_leadCaptureTimer);
        _leadCaptureTimer = setTimeout(triggerCapture, 1200);
      });

      el.addEventListener("blur", triggerCapture);
    },

    // 4. Dynamic Social Sharing & Viral Links
    getViralShareUrl: function(platform, text, customUrl) {
      const shareUrl = customUrl || "https://nexus-workforce.vercel.app/store";
      const refUrl = `${shareUrl}?ref=nexus_viral&utm_source=${platform}&utm_medium=social_share`;
      const encodedText = encodeURIComponent(`${text}\n\nAutomate locally without monthly subscriptions:`);
      const encodedUrl = encodeURIComponent(refUrl);

      switch(platform) {
        case "whatsapp":
          return `https://api.whatsapp.com/send?text=${encodedText}%20${encodedUrl}`;
        case "linkedin":
          return `https://www.linkedin.com/sharing/share-offsite/?url=${encodedUrl}`;
        case "x":
        case "twitter":
          return `https://twitter.com/intent/tweet?text=${encodedText}&url=${encodedUrl}&hashtags=SelfHosted,Python,DevTools`;
        case "facebook":
          return `https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}&quote=${encodedText}`;
        case "telegram":
          return `https://t.me/share/url?url=${encodedUrl}&text=${encodedText}`;
        default:
          return refUrl;
      }
    },

    shareTo: function(platform, text, customUrl) {
      const targetUrl = this.getViralShareUrl(platform, text, customUrl);
      window.open(targetUrl, "_blank", "width=600,height=520");
      this.track("social_share", { platform: platform, text_preview: (text || "").slice(0, 40) });
    }
  };

  // Track initial page view item
  window.addEventListener("DOMContentLoaded", () => {
    NexusRevenue.trackPageView(window.location.pathname);
  });
})();
