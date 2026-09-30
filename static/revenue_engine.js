/**
 * Nexus Revenue & Conversion Engine Client SDK
 * Handles conversion tracking and viral sharing hooks.
 * Exit-intent modals and self-promotional popups have been permanently removed.
 */

(function() {
  // 1. Conversion Event Tracker
  window.NexusRevenue = {
    track: async function(eventName, payload = {}) {
      try {
        await fetch("/api/revenue/track", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ event_name: eventName, payload: payload })
        });
      } catch (e) {
        console.warn("Revenue tracking warning:", e);
      }
    },
    trackViewItem: function(item) {
      this.track("view_item", item);
    },
    trackInitiateCheckout: function(cart) {
      this.track("initiate_checkout", cart);
    },
    trackPurchase: function(orderId, total, currency = "MUR") {
      this.track("purchase", { order_id: orderId, total: total, currency: currency });
    },
    trackDropoff: function(stepName, meta = {}) {
      this.track("dropoff", { step: stepName, ...meta });
    },

    // 2. Dynamic Social Sharing & Viral Links
    getViralShareUrl: function(platform, text, url = window.location.href) {
      const refUrl = `${url}?ref=nexus_share&utm_source=${platform}&utm_medium=viral`;
      const encodedText = encodeURIComponent(`${text}\n\nAutomated with Nexus AI (https://nexus-workforce.vercel.app)`);
      const encodedUrl = encodeURIComponent(refUrl);

      switch(platform) {
        case "whatsapp":
          return `https://api.whatsapp.com/send?text=${encodedText}%20${encodedUrl}`;
        case "linkedin":
          return `https://www.linkedin.com/feed/?shareActive=true&text=${encodedText}`;
        case "facebook":
          return `https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}&quote=${encodedText}`;
        case "x":
          return `https://twitter.com/intent/tweet?text=${encodedText}&url=${encodedUrl}`;
        default:
          return refUrl;
      }
    },

    shareTo: function(platform, text) {
      const targetUrl = this.getViralShareUrl(platform, text);
      window.open(targetUrl, "_blank", "width=600,height=500");
      this.track("social_share", { platform: platform });
    }
  };

  // Track initial page view item
  window.addEventListener("DOMContentLoaded", () => {
    NexusRevenue.trackViewItem({ page: window.location.pathname });
  });
})();
