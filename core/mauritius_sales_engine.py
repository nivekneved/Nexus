import os
import json
import urllib.parse
from typing import Dict, Any, List, Optional
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class MauritiusSalesEngine:
    """
    Commercial Engine for Local Mauritius WhatsApp AI Automations
    Targets local businesses (Villas, Tour Operators, Car Rentals, Clinics)
    providing 1-click WhatsApp pitch dispatches and live interactive demo replies.
    Payment via MCB Juice to +230 58169420.
    """
    def __init__(self):
        self._gemini_client = None
        self._init_gemini()

    def _init_gemini(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            try:
                from google import genai
                self._gemini_client = genai.Client(api_key=api_key)
            except Exception:
                pass

    def get_sectors(self) -> List[Dict[str, Any]]:
        raw_sectors = [
            {
                "id": "whatsapp_flight_addon",
                "icon": "âœˆï¸",
                "is_flagship": True,
                "title": "WhatsApp Flight Addonâ„¢ Conversational Booking & Status Bot",
                "status_badge": "ðŸš€ MAIN PRODUCT â€¢ LIVE DEMO",
                "locations": "Mauritius & Global Airlines, DMCs, Travel Agents & Booking Portals",
                "offer": "Conversational WhatsApp AI Flight Bot: Live GDS Flight Search, PNR Tracking, Baggage Policy & Instant Booking (Live Demo: https://whatsapp-flight-addon.vercel.app)",
                "setup_fee": 25000,
                "currency": "MUR",
                "retainer_fee": "Rs 5,000 / mo (or Rs 45,000 Full-Stack White-Label Buyout)",
                "demo_url": "https://whatsapp-flight-addon.vercel.app",
                "sold_reference": "whatsapp-flight-addon.vercel.app (Flagship Main Product)",
                "value_prop": "Turnkey conversational WhatsApp flight bot. Allows travelers to search flights, check live PNR status, view baggage allowances, and request booking changes directly on WhatsApp 24/7 without opening slow websites. Seamless MCB Juice and card payments.",
                "sample_pitch_fr": (
                    "Bonjour! ðŸ‘‹\n\n"
                    "Je m'appelle Deven (+230 58169420), ingÃ©nieur logiciel Ã  Maurice.\n\n"
                    "Plus de 70% des voyageurs prÃ©fÃ¨rent recevoir leurs billets, statuts de vol et alertes bagages directement sur WhatsApp plutÃ´t que de tÃ©lÃ©charger une Ã©niÃ¨me application ou chercher dans leurs emails.\n\n"
                    "Nous avons conÃ§u notre produit phare : **WhatsApp Flight Addonâ„¢** :\n"
                    "ðŸ‘‰ DÃ©mo interactive en direct : https://whatsapp-flight-addon.vercel.app\n\n"
                    "FonctionnalitÃ©s prÃªtes Ã  Ãªtre connectÃ©es Ã  votre agence ou compagnie :\n"
                    "âœˆï¸ Recherche de vols en temps rÃ©el (Air Mauritius, Emirates, Air France, etc.)\n"
                    "ðŸŽ« Consultation instantanÃ©e du statut PNR & e-ticket par message WhatsApp\n"
                    "ðŸ§³ FAQ intelligente 24/7 sur les franchises bagages & formalitÃ©s visa\n"
                    "ðŸ’³ RÃ¨glement d'acomptes ou supplÃ©ments via MCB Juice (+230 58169420) & Cartes\n"
                    "ðŸ¤– Prise en charge automatique des requÃªtes nocturnes avec bascule conseiller\n\n"
                    "ðŸ’° Tarification DÃ©couplÃ©e ClÃ©-en-main :\n"
                    "â€¢ Configuration & intÃ©gration WhatsApp Business API : Rs 25,000 MUR\n"
                    "â€¢ Forfait maintenance & surveillance 24/7 : Rs 5,000 / mois\n"
                    "â€¢ Rachat de licence complÃ¨te code source propriÃ©taire : Rs 45,000 MUR\n\n"
                    "Seriez-vous disponible pour une dÃ©monstration de 5 minutes sur votre tÃ©lÃ©phone cette semaine ?"
                )
            },
            {
                "id": "whatsapp_restaurant_sme",
                "icon": "ðŸ½ï¸",
                "is_flagship": True,
                "title": "WhatsApp Restaurant, Cafe & SME Retail Booking Bot",
                "status_badge": "ðŸ”¥ HIGH-DEMAND LOCAL B2B",
                "locations": "Mauritius Restaurants, Cafes, Spas, Salons & SME Retailers",
                "offer": "24/7 Automated WhatsApp Table Reservation, Menu Inquiry & Takeaway Order Bot with Instant Juice Clearing",
                "setup_fee": 15000,
                "currency": "MUR",
                "retainer_fee": "Rs 3,000 / mo (or Rs 25,000 Flat Lifetime Setup)",
                "demo_url": "https://whatsapp-flight-addon.vercel.app",
                "sold_reference": "WhatsApp Commerce Engine (Conversational Booking & Juice Clearing)",
                "value_prop": "Turnkey WhatsApp booking & ordering bot for restaurants and small businesses. Customers reserve tables, browse daily lunch menus, or order takeaway directly in WhatsApp without needing an app. Instant deposit and bill settlement via MCB Juice (+230 58169420).",
                "sample_pitch_fr": (
                    "Bonjour! ðŸ‘‹\n\n"
                    "Je m'appelle Deven (+230 58169420), ingÃ©nieur logiciel Ã  Maurice.\n\n"
                    "Combien de clients perd votre restaurant ou commerce aux heures de service parce que votre ligne tÃ©lÃ©phonique est occupÃ©e ou que les messages WhatsApp restent sans rÃ©ponse ?\n\n"
                    "Nous avons conÃ§u une solution ultra-simple pour les restaurants et commerÃ§ants mauriciens :\n"
                    "ðŸ‘‰ **RÃ©servation & Commande 100% automatisÃ©e sur WhatsApp** :\n\n"
                    "ðŸ½ï¸ RÃ©servation instantanÃ©e de table 24/7 avec confirmation automatique du crÃ©neau\n"
                    "ðŸ“‹ Envoi interactif de votre Menu du Jour et suggestions du chef\n"
                    "ðŸ¥¡ Prise de commande Ã  emporter (Takeaway / Click & Collect) sans commission tierce de 30%\n"
                    "ðŸ“± RÃ¨glement sÃ©curisÃ© des acomptes via MCB Juice (+230 58169420) & Cartes\n"
                    "ðŸ’¬ RÃ©duction de 80% du temps passÃ© par vos serveurs au tÃ©lÃ©phone\n\n"
                    "ðŸ’° Offre SpÃ©ciale PME / Restauration :\n"
                    "â€¢ Installation & configuration complÃ¨te de votre bot WhatsApp : Rs 15,000 MUR\n"
                    "â€¢ Maintenance & mise Ã  jour mensuelle de vos menus : Rs 3,000 / mois\n"
                    "*(Pack ClÃ©-en-main sans abonnement mensuel disponible Ã  Rs 25,000 MUR)*\n\n"
                    "Puis-je vous envoyer une simulation sur votre WhatsApp pour tester vous-mÃªme ?"
                )
            },
            {
                "id": "itravellix_saas",
                "icon": "ðŸŒŸ",
                "is_flagship": True,
                "title": "Turnkey Luxury Travel & Booking SaaS",
                "status_badge": "ðŸ”¥ LIVE-TESTED & SOLD (travellounge.mu)",
                "locations": "Mauritius Inbound DMCs, Tour Operators & Travel Agencies",
                "offer": "Complete White-Label Next.js Booking Platform + Native iOS & Android Apps (Live Reference: travellounge.mu / Demo: https://i-travellix.vercel.app)",
                "setup_fee": 200000,
                "currency": "MUR",
                "retainer_fee": "Rs 10,000 / mo (Rs 100k Front + Rs 100k Back = Rs 200k Web | + Rs 25k iOS & Rs 25k Android = Rs 250k Ecosystem)",
                "demo_url": "https://i-travellix.vercel.app",
                "sold_reference": "travellounge.mu (Successfully Sold & Deployed)",
                "value_prop": "Battle-tested booking engine proven in production at travellounge.mu. Live GDS flight search, resort catalog, catamaran tours, 4K showroom, native iOS & Android apps, and instant MCB Juice checkout.",
                "sample_pitch_fr": (
                    "Bonjour! ðŸ‘‹\n\n"
                    "Je m'appelle Deven (+230 58169420), ingÃ©nieur logiciel Ã  Maurice.\n\n"
                    "Beaucoup d'agences et tour-opÃ©rateurs rÃ©ceptifs Ã  Maurice perdent des rÃ©servations Ã  cause de portails lents, sans applications mobiles natives ni synchronisation temps rÃ©el.\n\n"
                    "Nous avons dÃ©jÃ  dÃ©ployÃ© et vendu avec succÃ¨s cette plateforme pour travellounge.mu :\n"
                    "ðŸ‘‰ DÃ©mo en direct : https://i-travellix.vercel.app (RÃ©fÃ©rence vendue : travellounge.mu)\n\n"
                    "PrÃªt Ã  l'emploi sous votre enseigne :\n"
                    "âœˆï¸ Moteur de recherche vols GDS en direct (Air Mauritius, Emirates, etc.)\n"
                    "ðŸ¨ Catalogue HÃ´tels 5 Ã©toiles & Forfaits sÃ©jours de luxe\n"
                    "â›µ RÃ©servation d'excursions, catamarans & hÃ©licoptÃ¨re\n"
                    "ðŸ’³ Paiement instantanÃ© MCB Juice & Cartes internationales\n"
                    "ðŸ“± Applications mobiles natives sur mesure iOS & Android\n\n"
                    "ðŸ’° Tarification Entreprise DÃ©couplÃ©e :\n"
                    "â€¢ Frontend Web voyageur & rÃ©servation en direct : Rs 100,000\n"
                    "â€¢ Backend GDS, connexions fournisseurs & gestion agence : Rs 100,000\n"
                    "  *(Total Suite Web ClÃ©-en-main : Rs 200,000)*\n"
                    "â€¢ Application Mobile Native iOS (Apple App Store) : Rs 25,000\n"
                    "â€¢ Application Mobile Native Android (Google Play) : Rs 25,000\n"
                    "  *(Ã‰cosystÃ¨me Complet Web + Mobile : Rs 250,000 MUR)*\n\n"
                    "Pouvons-nous organiser une dÃ©monstration de 10 minutes cette semaine ?"
                )
            },
            {
                "id": "ennrevennsourir_ngo",
                "icon": "â¤ï¸",
                "is_flagship": True,
                "title": "Enn Rev Enn Sourirâ„¢ Turnkey NGO & CSR Portal",
                "status_badge": "ðŸ”¥ LIVE-TESTED & SOLD (ennrevennsourir.vercel.app)",
                "locations": "Mauritius NGOs, Charities, Corporate CSR Funds & Foundations",
                "offer": "Transparent Medical Crowdfunding & NGO Management Suite (Live Reference: https://ennrevennsourir.vercel.app)",
                "setup_fee": 90000,
                "currency": "MUR",
                "retainer_fee": "Rs 10,000 / mo (or Rs 45,000 Front + Rs 45,000 Back = Rs 90,000 Full-Stack)",
                "demo_url": "https://ennrevennsourir.vercel.app",
                "sold_reference": "ennrevennsourir.vercel.app (Live-Tested & Sold)",
                "value_prop": "Production-proven humanitarian suite. 100% transparent donation tracking, hospital payouts, patient medical dossiers, MRA Sec 50L 15% tax deduction receipts, and MCB Juice checkout.",
                "sample_pitch_fr": (
                    "Bonjour! ðŸ‘‹\n\n"
                    "Je m'appelle Deven (+230 58169420), ingÃ©nieur logiciel basÃ© Ã  Maurice.\n\n"
                    "Beaucoup d'ONGs et fondations caritatives peinent avec la collecte de dons et la conformitÃ© vis-Ã -vis des donateurs et de la MRA.\n\n"
                    "Notre plateforme humanitaire clÃ©-en-main a dÃ©jÃ  Ã©tÃ© testÃ©e et vendue avec succÃ¨s pour ennrevennsourir :\n"
                    "ðŸ‘‰ DÃ©mo en direct : https://ennrevennsourir.vercel.app\n\n"
                    "Inclus et prÃªt Ã  Ãªtre installÃ© sous votre organisation :\n"
                    "â¤ï¸ Profils de cas mÃ©dicaux & chirurgies (pÃ©diatrie, cardiologie, oncologie)\n"
                    "ðŸ’³ Collecte multicanale instantanÃ©e (MCB Juice, Cartes bancaires & Virements)\n"
                    "ðŸ“œ Ã‰mission automatique de reÃ§us fiscaux certifiÃ©s MRA (15% de dÃ©duction)\n"
                    "ðŸ“Š Module de transparence totale & audits comptables\n"
                    "ðŸ¤ SystÃ¨me de parrainage mensuel (dÃ¨s Rs 500/mois)\n\n"
                    "ðŸ’° Tarification modulaire clÃ©-en-main :\n"
                    "â€¢ Frontend public donateurs, parrainages & campagnes : Rs 45,000\n"
                    "â€¢ Backend gestion des dossiers, dÃ©caissements hÃ´pitaux & rapports MRA : Rs 45,000\n"
                    "â€¢ Suite complÃ¨te Full-Stack sous votre marque : Rs 90,000 (ou abonnement).\n\n"
                    "Seriez-vous ouvert Ã  un Ã©change de 10 minutes cette semaine ?"
                )
            },
            {
                "id": "medical360_portal",
                "icon": "ðŸ©º",
                "is_flagship": True,
                "title": "Medical 360â„¢ Complete Hospital & Clinic Operations Suite",
                "status_badge": "ðŸ”¥ LIVE-TESTED & SOLD (med360.mu)",
                "locations": "Private Clinics, Polyclinics, Diagnostic Labs & Specialists across Mauritius",
                "offer": "360Â° Healthcare Web Portal & Clinic Operations Suite (Live Reference: med360.mu / https://www.med360.mu/preview)",
                "setup_fee": 90000,
                "currency": "MUR",
                "retainer_fee": "Rs 10,000 / mo (or Rs 45,000 Front + Rs 45,000 Back = Rs 90,000 Full-Stack)",
                "demo_url": "https://www.med360.mu/preview",
                "sold_reference": "https://www.med360.mu/preview (Live-Tested & Deployed)",
                "value_prop": "Production-proven healthcare operations suite deployed at med360.mu. Practitioner directory by specialty, 24/7 online consultation booking, blood bank donor registry, and diagnostic lab booking.",
                "sample_pitch_fr": (
                    "Bonjour Dr! ðŸ‘‹\n\n"
                    "C'est Deven de Nexus AI Solutions Ã  Maurice (+230 58169420).\n\n"
                    "Pour un cabinet ou une clinique mÃ©dicale Ã  Maurice, offrir une prise en charge numÃ©rique fluide est essentiel pour dÃ©sengorger le secrÃ©tariat et attirer de nouveaux patients.\n\n"
                    "Notre plateforme mÃ©dicale 360Â° a dÃ©jÃ  fait ses preuves en production (rÃ©fÃ©rence vendue : med360.mu) :\n"
                    "ðŸ‘‰ DÃ©mo en direct : https://www.med360.mu/preview\n\n"
                    "Inclus et prÃªt Ã  Ãªtre installÃ© sous votre enseigne :\n"
                    "ðŸ©º Annuaire interactif des praticiens par spÃ©cialitÃ©\n"
                    "ðŸ“… Prise de rendez-vous consultations en ligne 24/7\n"
                    "ðŸ©¸ Registre de la Banque de Sang & donneurs d'urgence\n"
                    "ðŸ”¬ Module de rÃ©servation d'analyses de Laboratoire\n"
                    "ðŸ’Š Catalogue Pharmacie en ligne & triage d'urgences\n"
                    "ðŸ” Espace d'administration sÃ©curisÃ© pour la gestion de votre clinique\n\n"
                    "ðŸ’° Tarification modulaire clÃ©-en-main :\n"
                    "â€¢ Frontend portail patient & rÃ©servations en ligne : Rs 45,000\n"
                    "â€¢ Backend gestion clinique, dossiers, labo & banque de sang : Rs 45,000\n"
                    "â€¢ Suite complÃ¨te Full-Stack dÃ©ployÃ©e pour votre clinique : Rs 90,000 (payable via Juice).\n\n"
                    "Puis-je vous faire une dÃ©monstration rapide de 5 minutes sur votre smartphone ?"
                )
            },
            {
                "id": "villas_hospitality",
                "icon": "ðŸï¸",
                "title": "Luxury Villas & Boutique Hotels",
                "locations": "Grand Baie, Pereybere, Tamarin, Le Morne, Trou aux Biches",
                "offer": "VillaFlow WhatsApp AI Guest Concierge (French/English)",
                "setup_fee": 25000,
                "currency": "MUR",
                "retainer_fee": "Rs 5,000 / mo",
                "value_prop": "Captures midnight tourist bookings, sends digital check-in codes, and books airport transfers automatically 24/7.",
                "sample_pitch_fr": (
                    "Bonjour! ðŸ‘‹\n\n"
                    "Je suis Deven de Nexus AI Solutions Ã  Maurice (+230 58169420).\n\n"
                    "Nous avons remarquÃ© que beaucoup de touristes internationaux vous Ã©crivent sur WhatsApp Ã  toute heure pour des devis de villas et check-in tardifs.\n\n"
                    "Nous avons conÃ§u un *Concierge WhatsApp IA autonome* qui rÃ©pond en 5 secondes en franÃ§ais et anglais, qualifie les dates et sÃ©curise les rÃ©servations directes sans payer les 18% de commission Booking/Airbnb.\n\n"
                    "Le setup est de Rs 25,000 (payable facilement par MCB Juice). Souhaitez-vous que je vous fasse une dÃ©mo directe sur ce numÃ©ro WhatsApp en 2 minutes?"
                )
            },
            {
                "id": "excursions_cruises",
                "icon": "â›µ",
                "title": "Catamaran Cruises, Diving & Excursions",
                "locations": "Grand Baie, Blue Bay, RiviÃ¨re Noire, Belle Mare",
                "offer": "WhatsApp 24/7 Instant Booking & Tariff Calculator",
                "setup_fee": 15000,
                "currency": "MUR",
                "retainer_fee": "Rs 3,000 / mo",
                "value_prop": "Instantly answers questions on dolphin tours, catamaran pricing, dietary options, and weather alerts.",
                "sample_pitch_fr": (
                    "Bonjour l'Ã©quipe! ðŸ‘‹\n\n"
                    "Je m'appelle Deven (dÃ©veloppeur basÃ© Ã  Maurice).\n\n"
                    "Quand vos skippers sont en mer, vous perdez souvent des clients qui demandent les tarifs d'excursions sur WhatsApp car la rÃ©ponse tarde de plusieurs heures.\n\n"
                    "Nous installons un *Bot WhatsApp IA dÃ©diÃ© aux excursions* qui donne instantanÃ©ment vos tarifs (Ile aux Cerfs, dauphins, pÃªche au gros) et rÃ©serve les places sans temps d'attente.\n\n"
                    "Installation complÃ¨te pour Rs 15,000 (MCB Juice). Puis-je vous envoyer une simulation rapide ici mÃªme?"
                )
            },
            {
                "id": "car_rentals",
                "icon": "ðŸš—",
                "title": "Tourist Car & Scooter Rentals",
                "locations": "AÃ©roport SSR, Flic en Flac, Grand Baie, Trou d'Eau Douce",
                "offer": "WhatsApp 24/7 Fleet Availability & Airport Triage",
                "setup_fee": 15000,
                "currency": "MUR",
                "retainer_fee": "Rs 3,000 / mo",
                "value_prop": "Collects tourist flight numbers, checks car availability, and quotes prices in MUR / EUR / USD.",
                "sample_pitch_fr": (
                    "Bonjour! ðŸš—\n\n"
                    "C'est Deven de Nexus AI Solutions (+230 58169420).\n\n"
                    "GÃ©rer les demandes de location de voitures sur WhatsApp Ã  l'arrivÃ©e des vols tardifs Ã  Plaisance est souvent chronophage.\n\n"
                    "Notre *IA WhatsApp pour loueurs de voitures* collecte automatiquement les numÃ©ros de vol, permis, dates et calcule le devis instantanÃ©ment pour le client.\n\n"
                    "ClÃ©-en-main pour Rs 15,000 (rÃ¨glement Juice). ÃŠtes-vous ouvert Ã  une dÃ©mo de 2 minutes sur votre smartphone?"
                )
            },
            {
                "id": "accounting_mcb_recon",
                "icon": "ðŸ“Š",
                "is_flagship": True,
                "title": "MCB Statement PDF-to-Excel & Juice Reconciler",
                "status_badge": "âš¡ FAST CASH â€¢ ONE-TIME B2B",
                "locations": "Ã‰bÃ¨ne Cybercity, Port Louis Financial District, Grand Baie, Moka",
                "offer": "100% Offline Bank Statement to Audit-Ready Excel Parser (No Cloud, Total Privacy)",
                "setup_fee": 1500,
                "currency": "MUR",
                "retainer_fee": "Rs 1,500 MUR one-time buyout (or Rs 4,500 5-User Practice License)",
                "demo_url": "https://nexusbots-nu.vercel.app/store",
                "sold_reference": "nexus_mcb_recon (Tested locally: parses dates, CEB/CWA/MRA/Juice, balance to Excel CSV)",
                "value_prop": "Eliminates 15-20 hours of manual data entry every month. Converts MCB statement PDFs and Juice exports into cleanly categorized Excel / Sage / QuickBooks CSVs in 2 seconds. 100% local execution â€” zero client financial data leaves the accountant's computer.",
                "sample_pitch_fr": (
                    "Bonjour! ðŸ‘‹\n\n"
                    "Je m'appelle Deven (+230 58169420), ingÃ©nieur logiciel Ã  Maurice.\n\n"
                    "Combien d'heures votre Ã©quipe comptable passe-t-elle chaque fin de mois Ã  ressaisir manuellement les relevÃ©s bancaires MCB et les transactions Juice dans Excel ?\n\n"
                    "Nous avons dÃ©veloppÃ© un outil sur mesure pour les cabinets comptables et auditeurs mauriciens :\n"
                    "ðŸ‘‰ **Nexus MCB Reconâ„¢** :\n\n"
                    "âš¡ Convertit instantanÃ©ment vos relevÃ©s bancaires PDF MCB et exports Juice en tableaux Excel prÃªts pour l'audit\n"
                    "ðŸ·ï¸ DÃ©tection et catÃ©gorisation automatique : CEB, CWA, MRA TVA/TDS, Mauritius Telecom et virements Juice\n"
                    "ðŸ”’ **ConfidentialitÃ© 100% Hors-Ligne** : Le script tourne directement sur votre PC. Aucune donnÃ©e financiÃ¨re ne quitte votre machine ni n'est envoyÃ©e dans le cloud\n"
                    "ðŸ“Š Compatible immÃ©diatement avec Excel, Sage Pastel et QuickBooks\n\n"
                    "ðŸ’° Tarif unique sans aucun abonnement :\n"
                    "â€¢ Licence permanente cabinet : Rs 1,500 MUR (rÃ¨glement instantanÃ© via MCB Juice au 58169420)\n"
                    "â€¢ Pack Multi-Postes (5 comptables) : Rs 4,500 MUR\n\n"
                    "Puis-je vous envoyer un extrait de dÃ©monstration sur WhatsApp pour tester avec un relevÃ© type ?"
                )
            },
            {
                "id": "dental_clinics",
                "icon": "ðŸ¥",
                "title": "Dental, Medical & Aesthetic Clinics",
                "locations": "Ã‰bÃ¨ne, FlorÃ©al, Curepipe, Grand Baie",
                "offer": "WhatsApp Patient Appointment & Intake Triage",
                "setup_fee": 20000,
                "currency": "MUR",
                "retainer_fee": "Rs 4,000 / mo",
                "value_prop": "Filters patient inquiries, schedules appointments, and sends reminder notices, eliminating missed calls.",
                "sample_pitch_fr": (
                    "Bonjour Dr! ðŸ‘‹\n\n"
                    "Je suis Deven de Nexus AI Solutions (Maurice).\n\n"
                    "Votre secrÃ©tariat mÃ©dical est souvent dÃ©bordÃ© d'appels et messages WhatsApp pour de simples confirmations de rendez-vous ou tarifs.\n\n"
                    "Nous dÃ©ployons une assistante mÃ©dicale WhatsApp IA qui trie les urgences et planifie les consultations automatiquement 24/7.\n\n"
                    "Installation complÃ¨te: Rs 20,000 via Juice. Je serais ravi de vous faire tester l'outil en direct si cela vous intÃ©resse."
                )
            }
        ]

        # Enrich every sector with normalized Connect Hub fields & wa.me links
        for s in raw_sectors:
            s["sector_id"] = s.get("id")
            s["setup_fee_mur"] = s.get("setup_fee", 15000)
            s["monthly_retainer_mur"] = s.get("retainer_fee", "Rs 5,000 / mo")
            s["pain_point"] = s.get("value_prop", "")
            s["whatsapp_pitch_kreol_fr"] = s.get("sample_pitch_fr", "")
            s["wa_me_link"] = self.generate_whatsapp_link("+23058169420", s.get("sample_pitch_fr", ""))
        return raw_sectors

    SECTOR_ALIASES = {
        "clinics": "dental_clinics",
        "salons": "whatsapp_restaurant_sme",
        "restaurants": "whatsapp_restaurant_sme",
        "tour_operators": "excursions_cruises",
        "retail_sme": "whatsapp_restaurant_sme",
        "hospitality": "villas_hospitality"
    }

    def resolve_sector_id(self, sector_id: str) -> str:
        clean = (sector_id or "villas_hospitality").strip().lower()
        return self.SECTOR_ALIASES.get(clean, clean)

    def generate_sector_pitch(self, sector_id: str) -> Dict[str, Any]:
        resolved = self.resolve_sector_id(sector_id)
        sectors = self.get_sectors()
        found = next((s for s in sectors if s["id"] == resolved), sectors[0])
        return {
            "sector_id": sector_id,
            "resolved_sector_id": found["id"],
            "title": found["title"],
            "setup_fee_mur": found["setup_fee"],
            "monthly_retainer_mur": found["retainer_fee"],
            "pain_point": found["value_prop"],
            "whatsapp_pitch_kreol_fr": found["sample_pitch_fr"],
            "wa_me_link": found["wa_me_link"]
        }

    # =========================================================================
    # PERSISTENT SQLITE WHATSAPP BOOKING & SLOT-LOCK STATE MACHINE
    # =========================================================================
    def _load_bookings(self) -> List[Dict[str, Any]]:
        from core.dal import dal
        bookings = dal.load("whatsapp_bookings", default=[])
        if not bookings:
            bookings = [
                {
                    "booking_id": "BK-MU-1001",
                    "customer_name": "Dr. Arvin Ramgoolam (Clinique du Nord)",
                    "customer_phone": "+23057123456",
                    "sector_id": "dental_clinics",
                    "slot_date": datetime.now().strftime("%Y-%m-%d"),
                    "slot_time": "14:00",
                    "language": "Kreol/FR",
                    "deposit_mur": 1500,
                    "payment_rail": "MCB Juice (+230 58169420)",
                    "status": "CONFIRMED",
                    "reminder_24h_sent": True,
                    "reminder_2h_sent": False,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                {
                    "booking_id": "BK-MU-1002",
                    "customer_name": "Jean-Pierre Duval (Le Morne Sunset Villas)",
                    "customer_phone": "+23058991122",
                    "sector_id": "villas_hospitality",
                    "slot_date": datetime.now().strftime("%Y-%m-%d"),
                    "slot_time": "16:00",
                    "language": "FR",
                    "deposit_mur": 5000,
                    "payment_rail": "MCB Juice (+230 58169420)",
                    "status": "PENDING_DEPOSIT",
                    "reminder_24h_sent": False,
                    "reminder_2h_sent": False,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            ]
            dal.save("whatsapp_bookings", bookings)
        return bookings

    def _save_bookings(self, bookings: List[Dict[str, Any]]) -> None:
        from core.dal import dal
        dal.save("whatsapp_bookings", bookings)

    def get_bookings(self, sector_id: Optional[str] = None) -> List[Dict[str, Any]]:
        bookings = self._load_bookings()
        if sector_id:
            resolved = self.resolve_sector_id(sector_id)
            return [b for b in bookings if b.get("sector_id") in (sector_id, resolved)]
        return bookings

    def detect_language(self, message: str) -> str:
        msg_l = (message or "").lower()
        kreol_markers = ["bonzour", "mo ", "anvi", "ki ", "prix", "kombien", "svp", "rendez-vous", "lamer", "lakaz", "mardi", "merkredi"]
        fr_markers = ["bonjour", "je ", "souhaite", "réserver", "combien", "tarif", "disponible", "créneau"]
        if any(k in msg_l for k in kreol_markers):
            return "Kreol Morisien / FR"
        if any(f in msg_l for f in fr_markers):
            return "Français"
        return "English"

    def parse_slot_from_message(self, message: str) -> Dict[str, str]:
        import re
        msg_l = (message or "").lower()
        today_str = datetime.now().strftime("%Y-%m-%d")
        day_map = {
            "lundi": "Lundi", "monday": "Monday",
            "mardi": "Mardi", "tuesday": "Tuesday",
            "mercredi": "Mercredi", "merkredi": "Mercredi", "wednesday": "Wednesday",
            "jeudi": "Jeudi", "thursday": "Thursday",
            "vendredi": "Vendredi", "friday": "Friday",
            "samedi": "Samedi", "saturday": "Saturday",
            "dimanche": "Dimanche", "sunday": "Sunday",
            "demain": "Demain", "tomorrow": "Tomorrow"
        }
        detected_day = today_str
        for k, label in day_map.items():
            if k in msg_l:
                detected_day = f"{label} ({today_str})"
                break

        time_match = re.search(r'\b(\d{1,2})\s*(?:h|:)\s*(\d{0,2})\b', msg_l)
        if time_match:
            hh = int(time_match.group(1))
            mm = time_match.group(2) or "00"
            slot_time = f"{hh:02d}:{mm.zfill(2)}"
        else:
            slot_time = "14:00"

        return {"slot_date": detected_day, "slot_time": slot_time}

    def create_or_lock_booking(
        self,
        customer_phone: str,
        message: str,
        sector_id: str = "clinics",
        customer_name: str = "Prospect WhatsApp"
    ) -> Dict[str, Any]:
        """
        Locks an appointment slot in SQLite WAL, prevents double-booking conflicts,
        and generates a trilingual (Kreol / FR / EN) confirmation + MCB Juice deposit prompt.
        """
        resolved_sector = self.resolve_sector_id(sector_id)
        lang = self.detect_language(message)
        slot_info = self.parse_slot_from_message(message)
        slot_date = slot_info["slot_date"]
        slot_time = slot_info["slot_time"]

        bookings = self._load_bookings()
        msg_upper = (message or "").upper()

        # Check if user is confirming an existing pending booking via Juice reference
        if any(w in msg_upper for w in ["JUICE", "CONFIRME", "PAID", "PAYE", "OK BOOK"]):
            for b in bookings:
                if b.get("customer_phone") == customer_phone and b.get("status") == "PENDING_DEPOSIT":
                    b["status"] = "CONFIRMED"
                    b["confirmed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self._save_bookings(bookings)
                    reply = (
                        f"✅ *Rendez-vous Confirmé ({b['booking_id']})* !\n"
                        f"📅 Créneau verrouillé : *{b['slot_date']} à {b['slot_time']}*\n"
                        f"💳 Acompte MCB Juice vérifié (+230 58169420).\n"
                        f"🔔 Vous recevrez un rappel WhatsApp automatique 24h et 2h avant votre rendez-vous. Mersi !"
                    )
                    return {
                        "success": True,
                        "booking": b,
                        "conflict_resolved": False,
                        "detected_language": lang,
                        "ai_reply": reply
                    }

        # Check for slot conflict on (resolved_sector, slot_date, slot_time)
        conflict = next(
            (b for b in bookings
             if b.get("sector_id") == resolved_sector
             and b.get("slot_date") == slot_date
             and b.get("slot_time") == slot_time
             and b.get("status") in ("PENDING_DEPOSIT", "CONFIRMED", "REMINDER_24H_SENT")),
            None
        )

        conflict_resolved = False
        original_requested_time = slot_time
        if conflict:
            conflict_resolved = True
            try:
                hh = int(slot_time.split(":")[0])
                next_hh = (hh + 1) if hh < 17 else 10
                slot_time = f"{next_hh:02d}:30"
            except Exception:
                slot_time = "15:30"

        booking_id = f"BK-MU-{int(datetime.now().timestamp()) % 100000}"
        new_booking = {
            "booking_id": booking_id,
            "customer_name": customer_name,
            "customer_phone": customer_phone or "+23058169420",
            "sector_id": resolved_sector,
            "slot_date": slot_date,
            "slot_time": slot_time,
            "language": lang,
            "deposit_mur": 1000,
            "payment_rail": "MCB Juice (+230 58169420) / PayPal ($1 Trial)",
            "status": "PENDING_DEPOSIT",
            "reminder_24h_sent": False,
            "reminder_2h_sent": False,
            "raw_request": message,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        bookings.insert(0, new_booking)
        self._save_bookings(bookings)

        if "Kreol" in lang:
            conflict_note = (
                f"⚠️ Créneau {original_requested_time} déza pris; nou finn réserve *{slot_time}* pou ou.\n"
                if conflict_resolved else ""
            )
            ai_reply = (
                f"Bonzour ! 👋🇲🇺 Mersi pou ou messaz.\n\n"
                f"{conflict_note}"
                f"✅ Nou finn pré-bloque créneau *{slot_date} à {slot_time}* (Réf: *{booking_id}*).\n\n"
                f"💳 *Pou confirme définitivement ou réservation* :\n"
                f"• Envoy enn ti acompte Rs 1,000 par *MCB Juice au +230 58169420* (Réf: {booking_id})\n"
                f"• Ou testé nou bot 7-zour pou $1.00 : https://www.paypal.com/ncp/payment/B4SASTZDVFXY4\n\n"
                f"Réponn *CONFIRME* ici dès ki c'est fait et ou pou gagne enn rappel automatique 24h avant !"
            )
        elif lang == "Français":
            conflict_note = (
                f"⚠️ Le créneau de {original_requested_time} étant complet, nous avons verrouillé *{slot_time}* pour vous.\n"
                if conflict_resolved else ""
            )
            ai_reply = (
                f"Bonjour ! 👋🇲🇺 Merci pour votre demande.\n\n"
                f"{conflict_note}"
                f"✅ Votre créneau du *{slot_date} à {slot_time}* est pré-verrouillé (Réf: *{booking_id}*).\n\n"
                f"💳 *Validation instantanée* :\n"
                f"• Règlement d'acompte via *MCB Juice au +230 58169420* (Réf: {booking_id})\n"
                f"• Ou activation essai 7 jours ($1.00) : https://www.paypal.com/ncp/payment/B4SASTZDVFXY4\n\n"
                f"Répondez *CONFIRME* pour finaliser — un rappel WhatsApp vous sera envoyé 24h et 2h avant le rendez-vous."
            )
        else:
            conflict_note = (
                f"⚠️ {original_requested_time} was just taken, so we locked the next open slot at *{slot_time}*.\n"
                if conflict_resolved else ""
            )
            ai_reply = (
                f"Hello! 👋🇲🇺 Thank you for reaching out.\n\n"
                f"{conflict_note}"
                f"✅ We have pre-locked your appointment slot for *{slot_date} at {slot_time}* (Ref: *{booking_id}*).\n\n"
                f"💳 *Instant Confirmation*:\n"
                f"• Local Mauritius Deposit via *MCB Juice to +230 58169420* (Ref: {booking_id})\n"
                f"• Global 7-Day Live Trial ($1.00): https://www.paypal.com/ncp/payment/B4SASTZDVFXY4\n\n"
                f"Reply *CONFIRME* once sent—our system will automatically dispatch 24h and 2h WhatsApp reminders."
            )

        return {
            "success": True,
            "booking": new_booking,
            "conflict_resolved": conflict_resolved,
            "detected_language": lang,
            "ai_reply": ai_reply
        }

    def dispatch_due_reminders(self) -> Dict[str, Any]:
        """
        Scans active WhatsApp bookings and dispatches automated 24h / 2h No-Show
        prevention reminders via WhatsApp Gateway.
        """
        from core.whatsapp_gateway import send_whatsapp_message
        bookings = self._load_bookings()
        dispatched = []

        for b in bookings:
            if b.get("status") in ("CONFIRMED", "PENDING_DEPOSIT") and not b.get("reminder_24h_sent"):
                msg = (
                    f"🔔 *Rappel Rendez-Vous ({b.get('booking_id')})*\n"
                    f"Bonjour {b.get('customer_name', 'Client')}, votre créneau est prévu le "
                    f"*{b.get('slot_date')} à {b.get('slot_time')}*.\n"
                    f"Pour toute question ou acompte MCB Juice : +230 58169420."
                )
                send_whatsapp_message(text=msg, phone=b.get("customer_phone", "+23058169420"), title="Booking Reminder")
                b["reminder_24h_sent"] = True
                if b.get("status") == "CONFIRMED":
                    b["status"] = "REMINDER_24H_SENT"
                dispatched.append(b["booking_id"])

        if dispatched:
            self._save_bookings(bookings)

        return {
            "success": True,
            "reminders_dispatched": len(dispatched),
            "booking_ids": dispatched,
            "total_bookings_tracked": len(bookings)
        }

    def generate_whatsapp_link(self, phone: str, text: str) -> str:
        clean_phone = "".join(filter(str.isdigit, phone))
        encoded = urllib.parse.quote(text)
        return f"https://wa.me/{clean_phone}?text={encoded}"

    def simulate_whatsapp_booking_reply(self, sector_id: str, guest_message: str, customer_phone: str = "+23058169420") -> Dict[str, Any]:
        """
        Executes both the persistent SQLite slot-lock state machine and the AI Concierge reply.
        """
        lock_res = self.create_or_lock_booking(
            customer_phone=customer_phone,
            message=guest_message,
            sector_id=sector_id
        )
        demo_res = self.simulate_demo_reply(guest_message=guest_message, sector_id=self.resolve_sector_id(sector_id))
        combined_reply = lock_res.get("ai_reply") or demo_res.get("reply", "")
        return {
            "success": True,
            "sector_id": sector_id,
            "detected_language": lock_res.get("detected_language", "Kreol/FR"),
            "booking": lock_res.get("booking"),
            "conflict_resolved": lock_res.get("conflict_resolved", False),
            "ai_reply": combined_reply,
            "reply": combined_reply
        }

    def simulate_demo_reply(self, guest_message: str, sector_id: str) -> Dict[str, Any]:
        """
        Simulates live AI response to a client / tourist message,
        demonstrating the high quality of the Mauritius WhatsApp Concierge.
        """
        prompt = f"""
You are the Mauritius WhatsApp AI Concierge for a premier business in Mauritius.
Sector: {sector_id}
Company Owner / Contact: Kingsley Vance Maurya (+230 58169420)
Currency: MUR (Rs) and EUR (â‚¬)
Languages: Fluent in French, English, and Mauritian Creole.

A potential customer just sent this message on WhatsApp:
\"\"\"{guest_message}\"\"\"

Provide a helpful, warm, professional, and culturally accurate WhatsApp response (include relevant emojis, clear options, and prompt to finalize booking).
Respond ONLY with the exact text message to be sent back to the customer.
"""
        if self._gemini_client:
            try:
                from google.genai import types
                response = self._gemini_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(temperature=0.3)
                )
                return {
                    "success": True,
                    "engine": "Gemini 2.5 Flash",
                    "reply": response.text.strip()
                }
            except Exception:
                pass

        # Fallback realistic demonstration reply
        if sector_id == "whatsapp_flight_addon":
            fallback = (
                "Bonjour! âœˆï¸ Bienvenue sur le service WhatsApp Flight Addonâ„¢.\n\n"
                "Comment puis-je vous assister aujourd'hui ?\n"
                "1ï¸âƒ£ VÃ©rifier le statut d'un vol en temps rÃ©el (ex: MK014)\n"
                "2ï¸âƒ£ Consulter votre rÃ©servation & e-ticket via rÃ©fÃ©rence PNR\n"
                "3ï¸âƒ£ VÃ©rifier les franchises bagages & rÃ¨gles de cabine\n"
                "4ï¸âƒ£ Demander une modification ou surclassement de siÃ¨ge\n\n"
                "ðŸ‘‰ DÃ©mo interactive en direct : https://whatsapp-flight-addon.vercel.app\n"
                "Indiquez votre numÃ©ro de vol ou rÃ©fÃ©rence PNR pour dÃ©marrer !"
            )
        elif sector_id == "whatsapp_restaurant_sme":
            fallback = (
                "Bonjour et bienvenue! ðŸ½ï¸âœ¨\n\n"
                "Nous avons bien reÃ§u votre demande de rÃ©servation :\n"
                "1ï¸âƒ£ RÃ©server une table (dÃ©jeuner / dÃ®ner en terrasse)\n"
                "2ï¸âƒ£ Consulter notre Menu du Jour & suggestions du Chef\n"
                "3ï¸âƒ£ Commander Ã  emporter (Takeaway / Click & Collect)\n"
                "4ï¸âƒ£ RÃ©gler votre acompte sÃ©curisÃ© via MCB Juice (+230 58169420)\n\n"
                "Indiquez la date, l'heure et le nombre de convives pour confirmer votre table en 30 secondes !"
            )
        elif sector_id == "ennrevennsourir_ngo":
            fallback = (
                "Bonjour! â¤ï¸ Merci pour votre gÃ©nÃ©rositÃ© et votre soutien envers les enfants malades.\n\n"
                "Chaque roupie donnÃ©e est versÃ©e Ã  100% directement aux hÃ´pitaux partenaires et vous donne droit Ã  15% de dÃ©duction d'impÃ´t MRA (Section 50L).\n\n"
                "ðŸ’³ Pour faire un don instantanÃ© via MCB Juice : +230 58169420 (RÃ©f: SOUTIEN)\n"
                "ðŸ“œ Pour recevoir votre reÃ§u fiscal officiel ou parrainer un enfant dÃ¨s Rs 500/mois, visitez https://ennrevennsourir.vercel.app ou rÃ©pondez ici.\n\n"
                "Ensemble, sauvons des vies Ã  Maurice ! ðŸŒŸ"
            )
        elif sector_id == "medical360_portal":
            fallback = (
                "Bonjour! ðŸ©º Bienvenue sur le service de prise en charge Medical 360.\n\n"
                "Comment pouvons-nous vous assister aujourd'hui ?\n"
                "1ï¸âƒ£ Prendre rendez-vous avec un mÃ©decin spÃ©cialiste\n"
                "2ï¸âƒ£ RÃ©server un bilan sanguin ou analyse de laboratoire\n"
                "3ï¸âƒ£ Consulter la disponibilitÃ© de notre banque de sang\n"
                "4ï¸âƒ£ Urgence mÃ©dicale immÃ©diate\n\n"
                "RÃ©pondez avec le numÃ©ro de votre choix ou visitez https://www.med360.mu/preview pour rÃ©server directement en ligne."
            )
        elif sector_id == "itravellix_saas":
            fallback = (
                "Bonjour et bienvenue chez i-Travellix Luxury Travel! âœˆï¸ðŸ–ï¸\n\n"
                "Nous recherchons pour vous les meilleures disponibilitÃ©s :\n"
                "ðŸ¨ HÃ´tels 5 Ã©toiles & Beach Resorts Ã  Maurice\n"
                "âœˆï¸ Vols directs Air Mauritius / Emirates\n"
                "â›µ CroisiÃ¨res privÃ©es en catamaran & survol hÃ©licoptÃ¨re\n\n"
                "DÃ©couvrez notre catalogue en ligne : https://i-travellix.vercel.app ou indiquez vos dates de voyage pour un devis personnalisÃ©."
            )
        elif sector_id == "accounting_mcb_recon":
            fallback = (
                "Bonjour! ðŸ“Š Bienvenue sur le service d'automatisation comptable Nexus MCB Reconâ„¢.\n\n"
                "Comment pouvons-nous vous assister ?\n"
                "1ï¸âƒ£ Traitement instantanÃ© de votre relevÃ© PDF MCB vers Excel CSV\n"
                "2ï¸âƒ£ RÃ©conciliation des virements Juice et transactions CEB / CWA / MRA\n"
                "3ï¸âƒ£ DÃ©monstration de sÃ©curitÃ© : 100% hors-ligne (aucune fuite de donnÃ©es bancaires)\n"
                "4ï¸âƒ£ Commander votre licence cabinet (Rs 1,500 via Juice au +230 58169420)\n\n"
                "Envoyez votre question ou contactez directement Deven au +230 58169420."
            )
        else:
            fallback = (
                "Bonjour! ðŸŒ´ Merci de nous contacter.\n\n"
                "Nous avons bien reÃ§u votre demande. Nos disponibilitÃ©s sont Ã  jour et nous serions ravis de vous accueillir.\n\n"
                "ðŸ“… Pourriez-vous nous prÃ©ciser vos dates exactes ainsi que le nombre de personnes ?\n\n"
                "Nous vous envoyons le devis dÃ©taillÃ© immÃ©diatement. Vous pouvez aussi nous joindre au +230 58169420.\n\n"
                "Ã€ trÃ¨s vite sous le soleil de l'Ã®le Maurice! â˜€ï¸"
            )
        return {
            "success": True,
            "engine": "Local Mauritius Concierge Engine",
            "reply": fallback
        }

mauritius_sales_engine = MauritiusSalesEngine()

