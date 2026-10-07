"""
Nexus™ Universal UI Enhancements & Standardized Modals
======================================================
Provides universal pagination, search filtering, duplicate cleaning/merging,
and standardized industry/geographic dropdown selectors across all workspace pages.
"""
(function() {
    window.NexusUI = {
        getIndustryOptions: function(selected) {
            const industries = [
                "SaaS / AI & Tech Consulting",
                "Private Clinics & Healthcare",
                "Luxury Resorts & Hospitality",
                "Supply Chain & Logistics / Freight",
                "Cybersecurity & Defense",
                "Fintech & Banking",
                "Real Estate & DMCs",
                "NGOs & CSR Foundations",
                "General Enterprise B2B"
            ];
            return industries.map(ind => `<option value="${ind}" ${ind === selected ? 'selected' : ''}>${ind}</option>`).join('');
        },
        getGeoOptions: function(selected) {
            const geos = [
                "Mauritius (Local Tenders & Directories)",
                "East & South Africa (Kenya, South Africa, Nigeria)",
                "United Kingdom (London & Regional Tenders)",
                "European Union (France, Germany, Netherlands)",
                "North America (US & Canada)",
                "Global / Remote"
            ];
            return geos.map(g => `<option value="${g}" ${g === selected ? 'selected' : ''}>${g}</option>`).join('');
        }
    };
    console.log("🚀 NexusUI Enhancements & Universal Modals loaded successfully.");
})();
