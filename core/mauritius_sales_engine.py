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
        return [
            {
                "id": "whatsapp_flight_addon",
                "icon": "✈️",
                "is_flagship": True,
                "title": "WhatsApp Flight Addon™ Conversational Booking & Status Bot",
                "status_badge": "🚀 MAIN PRODUCT • LIVE DEMO",
                "locations": "Mauritius & Global Airlines, DMCs, Travel Agents & Booking Portals",
                "offer": "Conversational WhatsApp AI Flight Bot: Live GDS Flight Search, PNR Tracking, Baggage Policy & Instant Booking (Live Demo: https://whatsapp-flight-addon.vercel.app)",
                "setup_fee": 25000,
                "currency": "MUR",
                "retainer_fee": "Rs 5,000 / mo (or Rs 45,000 Full-Stack White-Label Buyout)",
                "demo_url": "https://whatsapp-flight-addon.vercel.app",
                "sold_reference": "whatsapp-flight-addon.vercel.app (Flagship Main Product)",
                "value_prop": "Turnkey conversational WhatsApp flight bot. Allows travelers to search flights, check live PNR status, view baggage allowances, and request booking changes directly on WhatsApp 24/7 without opening slow websites. Seamless MCB Juice and card payments.",
                "sample_pitch_fr": (
                    "Bonjour! 👋\n\n"
                    "Je m'appelle Deven (+230 58169420), ingénieur logiciel à Maurice.\n\n"
                    "Plus de 70% des voyageurs préfèrent recevoir leurs billets, statuts de vol et alertes bagages directement sur WhatsApp plutôt que de télécharger une énième application ou chercher dans leurs emails.\n\n"
                    "Nous avons conçu notre produit phare : **WhatsApp Flight Addon™** :\n"
                    "👉 Démo interactive en direct : https://whatsapp-flight-addon.vercel.app\n\n"
                    "Fonctionnalités prêtes à être connectées à votre agence ou compagnie :\n"
                    "✈️ Recherche de vols en temps réel (Air Mauritius, Emirates, Air France, etc.)\n"
                    "🎫 Consultation instantanée du statut PNR & e-ticket par message WhatsApp\n"
                    "🧳 FAQ intelligente 24/7 sur les franchises bagages & formalités visa\n"
                    "💳 Règlement d'acomptes ou suppléments via MCB Juice (+230 58169420) & Cartes\n"
                    "🤖 Prise en charge automatique des requêtes nocturnes avec bascule conseiller\n\n"
                    "💰 Tarification Découplée Clé-en-main :\n"
                    "• Configuration & intégration WhatsApp Business API : Rs 25,000 MUR\n"
                    "• Forfait maintenance & surveillance 24/7 : Rs 5,000 / mois\n"
                    "• Rachat de licence complète code source propriétaire : Rs 45,000 MUR\n\n"
                    "Seriez-vous disponible pour une démonstration de 5 minutes sur votre téléphone cette semaine ?"
                )
            },
            {
                "id": "whatsapp_restaurant_sme",
                "icon": "🍽️",
                "is_flagship": True,
                "title": "WhatsApp Restaurant, Cafe & SME Retail Booking Bot",
                "status_badge": "🔥 HIGH-DEMAND LOCAL B2B",
                "locations": "Mauritius Restaurants, Cafes, Spas, Salons & SME Retailers",
                "offer": "24/7 Automated WhatsApp Table Reservation, Menu Inquiry & Takeaway Order Bot with Instant Juice Clearing",
                "setup_fee": 15000,
                "currency": "MUR",
                "retainer_fee": "Rs 3,000 / mo (or Rs 25,000 Flat Lifetime Setup)",
                "demo_url": "https://whatsapp-flight-addon.vercel.app",
                "sold_reference": "WhatsApp Commerce Engine (Conversational Booking & Juice Clearing)",
                "value_prop": "Turnkey WhatsApp booking & ordering bot for restaurants and small businesses. Customers reserve tables, browse daily lunch menus, or order takeaway directly in WhatsApp without needing an app. Instant deposit and bill settlement via MCB Juice (+230 58169420).",
                "sample_pitch_fr": (
                    "Bonjour! 👋\n\n"
                    "Je m'appelle Deven (+230 58169420), ingénieur logiciel à Maurice.\n\n"
                    "Combien de clients perd votre restaurant ou commerce aux heures de service parce que votre ligne téléphonique est occupée ou que les messages WhatsApp restent sans réponse ?\n\n"
                    "Nous avons conçu une solution ultra-simple pour les restaurants et commerçants mauriciens :\n"
                    "👉 **Réservation & Commande 100% automatisée sur WhatsApp** :\n\n"
                    "🍽️ Réservation instantanée de table 24/7 avec confirmation automatique du créneau\n"
                    "📋 Envoi interactif de votre Menu du Jour et suggestions du chef\n"
                    "🥡 Prise de commande à emporter (Takeaway / Click & Collect) sans commission tierce de 30%\n"
                    "📱 Règlement sécurisé des acomptes via MCB Juice (+230 58169420) & Cartes\n"
                    "💬 Réduction de 80% du temps passé par vos serveurs au téléphone\n\n"
                    "💰 Offre Spéciale PME / Restauration :\n"
                    "• Installation & configuration complète de votre bot WhatsApp : Rs 15,000 MUR\n"
                    "• Maintenance & mise à jour mensuelle de vos menus : Rs 3,000 / mois\n"
                    "*(Pack Clé-en-main sans abonnement mensuel disponible à Rs 25,000 MUR)*\n\n"
                    "Puis-je vous envoyer une simulation sur votre WhatsApp pour tester vous-même ?"
                )
            },
            {
                "id": "itravellix_saas",
                "icon": "🌟",
                "is_flagship": True,
                "title": "Turnkey Luxury Travel & Booking SaaS",
                "status_badge": "🔥 LIVE-TESTED & SOLD (travellounge.mu)",
                "locations": "Mauritius Inbound DMCs, Tour Operators & Travel Agencies",
                "offer": "Complete White-Label Next.js Booking Platform + Native iOS & Android Apps (Live Reference: travellounge.mu / Demo: https://i-travellix.vercel.app)",
                "setup_fee": 200000,
                "currency": "MUR",
                "retainer_fee": "Rs 10,000 / mo (Rs 100k Front + Rs 100k Back = Rs 200k Web | + Rs 25k iOS & Rs 25k Android = Rs 250k Ecosystem)",
                "demo_url": "https://i-travellix.vercel.app",
                "sold_reference": "travellounge.mu (Successfully Sold & Deployed)",
                "value_prop": "Battle-tested booking engine proven in production at travellounge.mu. Live GDS flight search, resort catalog, catamaran tours, 4K showroom, native iOS & Android apps, and instant MCB Juice checkout.",
                "sample_pitch_fr": (
                    "Bonjour! 👋\n\n"
                    "Je m'appelle Deven (+230 58169420), ingénieur logiciel à Maurice.\n\n"
                    "Beaucoup d'agences et tour-opérateurs réceptifs à Maurice perdent des réservations à cause de portails lents, sans applications mobiles natives ni synchronisation temps réel.\n\n"
                    "Nous avons déjà déployé et vendu avec succès cette plateforme pour travellounge.mu :\n"
                    "👉 Démo en direct : https://i-travellix.vercel.app (Référence vendue : travellounge.mu)\n\n"
                    "Prêt à l'emploi sous votre enseigne :\n"
                    "✈️ Moteur de recherche vols GDS en direct (Air Mauritius, Emirates, etc.)\n"
                    "🏨 Catalogue Hôtels 5 étoiles & Forfaits séjours de luxe\n"
                    "⛵ Réservation d'excursions, catamarans & hélicoptère\n"
                    "💳 Paiement instantané MCB Juice & Cartes internationales\n"
                    "📱 Applications mobiles natives sur mesure iOS & Android\n\n"
                    "💰 Tarification Entreprise Découplée :\n"
                    "• Frontend Web voyageur & réservation en direct : Rs 100,000\n"
                    "• Backend GDS, connexions fournisseurs & gestion agence : Rs 100,000\n"
                    "  *(Total Suite Web Clé-en-main : Rs 200,000)*\n"
                    "• Application Mobile Native iOS (Apple App Store) : Rs 25,000\n"
                    "• Application Mobile Native Android (Google Play) : Rs 25,000\n"
                    "  *(Écosystème Complet Web + Mobile : Rs 250,000 MUR)*\n\n"
                    "Pouvons-nous organiser une démonstration de 10 minutes cette semaine ?"
                )
            },
            {
                "id": "ennrevennsourir_ngo",
                "icon": "❤️",
                "is_flagship": True,
                "title": "Enn Rev Enn Sourir™ Turnkey NGO & CSR Portal",
                "status_badge": "🔥 LIVE-TESTED & SOLD (ennrevennsourir.vercel.app)",
                "locations": "Mauritius NGOs, Charities, Corporate CSR Funds & Foundations",
                "offer": "Transparent Medical Crowdfunding & NGO Management Suite (Live Reference: https://ennrevennsourir.vercel.app)",
                "setup_fee": 90000,
                "currency": "MUR",
                "retainer_fee": "Rs 10,000 / mo (or Rs 45,000 Front + Rs 45,000 Back = Rs 90,000 Full-Stack)",
                "demo_url": "https://ennrevennsourir.vercel.app",
                "sold_reference": "ennrevennsourir.vercel.app (Live-Tested & Sold)",
                "value_prop": "Production-proven humanitarian suite. 100% transparent donation tracking, hospital payouts, patient medical dossiers, MRA Sec 50L 15% tax deduction receipts, and MCB Juice checkout.",
                "sample_pitch_fr": (
                    "Bonjour! 👋\n\n"
                    "Je m'appelle Deven (+230 58169420), ingénieur logiciel basé à Maurice.\n\n"
                    "Beaucoup d'ONGs et fondations caritatives peinent avec la collecte de dons et la conformité vis-à-vis des donateurs et de la MRA.\n\n"
                    "Notre plateforme humanitaire clé-en-main a déjà été testée et vendue avec succès pour ennrevennsourir :\n"
                    "👉 Démo en direct : https://ennrevennsourir.vercel.app\n\n"
                    "Inclus et prêt à être installé sous votre organisation :\n"
                    "❤️ Profils de cas médicaux & chirurgies (pédiatrie, cardiologie, oncologie)\n"
                    "💳 Collecte multicanale instantanée (MCB Juice, Cartes bancaires & Virements)\n"
                    "📜 Émission automatique de reçus fiscaux certifiés MRA (15% de déduction)\n"
                    "📊 Module de transparence totale & audits comptables\n"
                    "🤝 Système de parrainage mensuel (dès Rs 500/mois)\n\n"
                    "💰 Tarification modulaire clé-en-main :\n"
                    "• Frontend public donateurs, parrainages & campagnes : Rs 45,000\n"
                    "• Backend gestion des dossiers, décaissements hôpitaux & rapports MRA : Rs 45,000\n"
                    "• Suite complète Full-Stack sous votre marque : Rs 90,000 (ou abonnement).\n\n"
                    "Seriez-vous ouvert à un échange de 10 minutes cette semaine ?"
                )
            },
            {
                "id": "medical360_portal",
                "icon": "🩺",
                "is_flagship": True,
                "title": "Medical 360™ Complete Hospital & Clinic Operations Suite",
                "status_badge": "🔥 LIVE-TESTED & SOLD (med360.mu)",
                "locations": "Private Clinics, Polyclinics, Diagnostic Labs & Specialists across Mauritius",
                "offer": "360° Healthcare Web Portal & Clinic Operations Suite (Live Reference: med360.mu / https://www.med360.mu/preview)",
                "setup_fee": 90000,
                "currency": "MUR",
                "retainer_fee": "Rs 10,000 / mo (or Rs 45,000 Front + Rs 45,000 Back = Rs 90,000 Full-Stack)",
                "demo_url": "https://www.med360.mu/preview",
                "sold_reference": "https://www.med360.mu/preview (Live-Tested & Deployed)",
                "value_prop": "Production-proven healthcare operations suite deployed at med360.mu. Practitioner directory by specialty, 24/7 online consultation booking, blood bank donor registry, and diagnostic lab booking.",
                "sample_pitch_fr": (
                    "Bonjour Dr! 👋\n\n"
                    "C'est Deven de Nexus AI Solutions à Maurice (+230 58169420).\n\n"
                    "Pour un cabinet ou une clinique médicale à Maurice, offrir une prise en charge numérique fluide est essentiel pour désengorger le secrétariat et attirer de nouveaux patients.\n\n"
                    "Notre plateforme médicale 360° a déjà fait ses preuves en production (référence vendue : med360.mu) :\n"
                    "👉 Démo en direct : https://www.med360.mu/preview\n\n"
                    "Inclus et prêt à être installé sous votre enseigne :\n"
                    "🩺 Annuaire interactif des praticiens par spécialité\n"
                    "📅 Prise de rendez-vous consultations en ligne 24/7\n"
                    "🩸 Registre de la Banque de Sang & donneurs d'urgence\n"
                    "🔬 Module de réservation d'analyses de Laboratoire\n"
                    "💊 Catalogue Pharmacie en ligne & triage d'urgences\n"
                    "🔐 Espace d'administration sécurisé pour la gestion de votre clinique\n\n"
                    "💰 Tarification modulaire clé-en-main :\n"
                    "• Frontend portail patient & réservations en ligne : Rs 45,000\n"
                    "• Backend gestion clinique, dossiers, labo & banque de sang : Rs 45,000\n"
                    "• Suite complète Full-Stack déployée pour votre clinique : Rs 90,000 (payable via Juice).\n\n"
                    "Puis-je vous faire une démonstration rapide de 5 minutes sur votre smartphone ?"
                )
            },
            {
                "id": "villas_hospitality",
                "icon": "🏝️",
                "title": "Luxury Villas & Boutique Hotels",
                "locations": "Grand Baie, Pereybere, Tamarin, Le Morne, Trou aux Biches",
                "offer": "VillaFlow WhatsApp AI Guest Concierge (French/English)",
                "setup_fee": 25000,
                "currency": "MUR",
                "retainer_fee": "Rs 5,000 / mo",
                "value_prop": "Captures midnight tourist bookings, sends digital check-in codes, and books airport transfers automatically 24/7.",
                "sample_pitch_fr": (
                    "Bonjour! 👋\n\n"
                    "Je suis Deven de Nexus AI Solutions à Maurice (+230 58169420).\n\n"
                    "Nous avons remarqué que beaucoup de touristes internationaux vous écrivent sur WhatsApp à toute heure pour des devis de villas et check-in tardifs.\n\n"
                    "Nous avons conçu un *Concierge WhatsApp IA autonome* qui répond en 5 secondes en français et anglais, qualifie les dates et sécurise les réservations directes sans payer les 18% de commission Booking/Airbnb.\n\n"
                    "Le setup est de Rs 25,000 (payable facilement par MCB Juice). Souhaitez-vous que je vous fasse une démo directe sur ce numéro WhatsApp en 2 minutes?"
                )
            },
            {
                "id": "excursions_cruises",
                "icon": "⛵",
                "title": "Catamaran Cruises, Diving & Excursions",
                "locations": "Grand Baie, Blue Bay, Rivière Noire, Belle Mare",
                "offer": "WhatsApp 24/7 Instant Booking & Tariff Calculator",
                "setup_fee": 15000,
                "currency": "MUR",
                "retainer_fee": "Rs 3,000 / mo",
                "value_prop": "Instantly answers questions on dolphin tours, catamaran pricing, dietary options, and weather alerts.",
                "sample_pitch_fr": (
                    "Bonjour l'équipe! 👋\n\n"
                    "Je m'appelle Deven (développeur basé à Maurice).\n\n"
                    "Quand vos skippers sont en mer, vous perdez souvent des clients qui demandent les tarifs d'excursions sur WhatsApp car la réponse tarde de plusieurs heures.\n\n"
                    "Nous installons un *Bot WhatsApp IA dédié aux excursions* qui donne instantanément vos tarifs (Ile aux Cerfs, dauphins, pêche au gros) et réserve les places sans temps d'attente.\n\n"
                    "Installation complète pour Rs 15,000 (MCB Juice). Puis-je vous envoyer une simulation rapide ici même?"
                )
            },
            {
                "id": "car_rentals",
                "icon": "🚗",
                "title": "Tourist Car & Scooter Rentals",
                "locations": "Aéroport SSR, Flic en Flac, Grand Baie, Trou d'Eau Douce",
                "offer": "WhatsApp 24/7 Fleet Availability & Airport Triage",
                "setup_fee": 15000,
                "currency": "MUR",
                "retainer_fee": "Rs 3,000 / mo",
                "value_prop": "Collects tourist flight numbers, checks car availability, and quotes prices in MUR / EUR / USD.",
                "sample_pitch_fr": (
                    "Bonjour! 🚗\n\n"
                    "C'est Deven de Nexus AI Solutions (+230 58169420).\n\n"
                    "Gérer les demandes de location de voitures sur WhatsApp à l'arrivée des vols tardifs à Plaisance est souvent chronophage.\n\n"
                    "Notre *IA WhatsApp pour loueurs de voitures* collecte automatiquement les numéros de vol, permis, dates et calcule le devis instantanément pour le client.\n\n"
                    "Clé-en-main pour Rs 15,000 (règlement Juice). Êtes-vous ouvert à une démo de 2 minutes sur votre smartphone?"
                )
            },
            {
                "id": "accounting_mcb_recon",
                "icon": "📊",
                "is_flagship": True,
                "title": "MCB Statement PDF-to-Excel & Juice Reconciler",
                "status_badge": "⚡ FAST CASH • ONE-TIME B2B",
                "locations": "Ébène Cybercity, Port Louis Financial District, Grand Baie, Moka",
                "offer": "100% Offline Bank Statement to Audit-Ready Excel Parser (No Cloud, Total Privacy)",
                "setup_fee": 1500,
                "currency": "MUR",
                "retainer_fee": "Rs 1,500 MUR one-time buyout (or Rs 4,500 5-User Practice License)",
                "demo_url": "https://nexusbots-nu.vercel.app/store",
                "sold_reference": "nexus_mcb_recon (Tested locally: parses dates, CEB/CWA/MRA/Juice, balance to Excel CSV)",
                "value_prop": "Eliminates 15-20 hours of manual data entry every month. Converts MCB statement PDFs and Juice exports into cleanly categorized Excel / Sage / QuickBooks CSVs in 2 seconds. 100% local execution — zero client financial data leaves the accountant's computer.",
                "sample_pitch_fr": (
                    "Bonjour! 👋\n\n"
                    "Je m'appelle Deven (+230 58169420), ingénieur logiciel à Maurice.\n\n"
                    "Combien d'heures votre équipe comptable passe-t-elle chaque fin de mois à ressaisir manuellement les relevés bancaires MCB et les transactions Juice dans Excel ?\n\n"
                    "Nous avons développé un outil sur mesure pour les cabinets comptables et auditeurs mauriciens :\n"
                    "👉 **Nexus MCB Recon™** :\n\n"
                    "⚡ Convertit instantanément vos relevés bancaires PDF MCB et exports Juice en tableaux Excel prêts pour l'audit\n"
                    "🏷️ Détection et catégorisation automatique : CEB, CWA, MRA TVA/TDS, Mauritius Telecom et virements Juice\n"
                    "🔒 **Confidentialité 100% Hors-Ligne** : Le script tourne directement sur votre PC. Aucune donnée financière ne quitte votre machine ni n'est envoyée dans le cloud\n"
                    "📊 Compatible immédiatement avec Excel, Sage Pastel et QuickBooks\n\n"
                    "💰 Tarif unique sans aucun abonnement :\n"
                    "• Licence permanente cabinet : Rs 1,500 MUR (règlement instantané via MCB Juice au 58169420)\n"
                    "• Pack Multi-Postes (5 comptables) : Rs 4,500 MUR\n\n"
                    "Puis-je vous envoyer un extrait de démonstration sur WhatsApp pour tester avec un relevé type ?"
                )
            },
            {
                "id": "dental_clinics",
                "icon": "🏥",
                "title": "Dental, Medical & Aesthetic Clinics",
                "locations": "Ébène, Floréal, Curepipe, Grand Baie",
                "offer": "WhatsApp Patient Appointment & Intake Triage",
                "setup_fee": 20000,
                "currency": "MUR",
                "retainer_fee": "Rs 4,000 / mo",
                "value_prop": "Filters patient inquiries, schedules appointments, and sends reminder notices, eliminating missed calls.",
                "sample_pitch_fr": (
                    "Bonjour Dr! 👋\n\n"
                    "Je suis Deven de Nexus AI Solutions (Maurice).\n\n"
                    "Votre secrétariat médical est souvent débordé d'appels et messages WhatsApp pour de simples confirmations de rendez-vous ou tarifs.\n\n"
                    "Nous déployons une assistante médicale WhatsApp IA qui trie les urgences et planifie les consultations automatiquement 24/7.\n\n"
                    "Installation complète: Rs 20,000 via Juice. Je serais ravi de vous faire tester l'outil en direct si cela vous intéresse."
                )
            }
        ]

    def generate_whatsapp_link(self, phone: str, text: str) -> str:
        clean_phone = "".join(filter(str.isdigit, phone))
        encoded = urllib.parse.quote(text)
        return f"https://wa.me/{clean_phone}?text={encoded}"

    def simulate_demo_reply(self, guest_message: str, sector_id: str) -> Dict[str, Any]:
        """
        Simulates live AI response to a client / tourist message,
        demonstrating the high quality of the Mauritius WhatsApp Concierge.
        """
        prompt = f"""
You are the Mauritius WhatsApp AI Concierge for a premier business in Mauritius.
Sector: {sector_id}
Company Owner / Contact: Deven Pawaray (+230 58169420)
Currency: MUR (Rs) and EUR (€)
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
                "Bonjour! ✈️ Bienvenue sur le service WhatsApp Flight Addon™.\n\n"
                "Comment puis-je vous assister aujourd'hui ?\n"
                "1️⃣ Vérifier le statut d'un vol en temps réel (ex: MK014)\n"
                "2️⃣ Consulter votre réservation & e-ticket via référence PNR\n"
                "3️⃣ Vérifier les franchises bagages & règles de cabine\n"
                "4️⃣ Demander une modification ou surclassement de siège\n\n"
                "👉 Démo interactive en direct : https://whatsapp-flight-addon.vercel.app\n"
                "Indiquez votre numéro de vol ou référence PNR pour démarrer !"
            )
        elif sector_id == "whatsapp_restaurant_sme":
            fallback = (
                "Bonjour et bienvenue! 🍽️✨\n\n"
                "Nous avons bien reçu votre demande de réservation :\n"
                "1️⃣ Réserver une table (déjeuner / dîner en terrasse)\n"
                "2️⃣ Consulter notre Menu du Jour & suggestions du Chef\n"
                "3️⃣ Commander à emporter (Takeaway / Click & Collect)\n"
                "4️⃣ Régler votre acompte sécurisé via MCB Juice (+230 58169420)\n\n"
                "Indiquez la date, l'heure et le nombre de convives pour confirmer votre table en 30 secondes !"
            )
        elif sector_id == "ennrevennsourir_ngo":
            fallback = (
                "Bonjour! ❤️ Merci pour votre générosité et votre soutien envers les enfants malades.\n\n"
                "Chaque roupie donnée est versée à 100% directement aux hôpitaux partenaires et vous donne droit à 15% de déduction d'impôt MRA (Section 50L).\n\n"
                "💳 Pour faire un don instantané via MCB Juice : +230 58169420 (Réf: SOUTIEN)\n"
                "📜 Pour recevoir votre reçu fiscal officiel ou parrainer un enfant dès Rs 500/mois, visitez https://ennrevennsourir.vercel.app ou répondez ici.\n\n"
                "Ensemble, sauvons des vies à Maurice ! 🌟"
            )
        elif sector_id == "medical360_portal":
            fallback = (
                "Bonjour! 🩺 Bienvenue sur le service de prise en charge Medical 360.\n\n"
                "Comment pouvons-nous vous assister aujourd'hui ?\n"
                "1️⃣ Prendre rendez-vous avec un médecin spécialiste\n"
                "2️⃣ Réserver un bilan sanguin ou analyse de laboratoire\n"
                "3️⃣ Consulter la disponibilité de notre banque de sang\n"
                "4️⃣ Urgence médicale immédiate\n\n"
                "Répondez avec le numéro de votre choix ou visitez https://www.med360.mu/preview pour réserver directement en ligne."
            )
        elif sector_id == "itravellix_saas":
            fallback = (
                "Bonjour et bienvenue chez i-Travellix Luxury Travel! ✈️🏖️\n\n"
                "Nous recherchons pour vous les meilleures disponibilités :\n"
                "🏨 Hôtels 5 étoiles & Beach Resorts à Maurice\n"
                "✈️ Vols directs Air Mauritius / Emirates\n"
                "⛵ Croisières privées en catamaran & survol hélicoptère\n\n"
                "Découvrez notre catalogue en ligne : https://i-travellix.vercel.app ou indiquez vos dates de voyage pour un devis personnalisé."
            )
        elif sector_id == "accounting_mcb_recon":
            fallback = (
                "Bonjour! 📊 Bienvenue sur le service d'automatisation comptable Nexus MCB Recon™.\n\n"
                "Comment pouvons-nous vous assister ?\n"
                "1️⃣ Traitement instantané de votre relevé PDF MCB vers Excel CSV\n"
                "2️⃣ Réconciliation des virements Juice et transactions CEB / CWA / MRA\n"
                "3️⃣ Démonstration de sécurité : 100% hors-ligne (aucune fuite de données bancaires)\n"
                "4️⃣ Commander votre licence cabinet (Rs 1,500 via Juice au +230 58169420)\n\n"
                "Envoyez votre question ou contactez directement Deven au +230 58169420."
            )
        else:
            fallback = (
                "Bonjour! 🌴 Merci de nous contacter.\n\n"
                "Nous avons bien reçu votre demande. Nos disponibilités sont à jour et nous serions ravis de vous accueillir.\n\n"
                "📅 Pourriez-vous nous préciser vos dates exactes ainsi que le nombre de personnes ?\n\n"
                "Nous vous envoyons le devis détaillé immédiatement. Vous pouvez aussi nous joindre au +230 58169420.\n\n"
                "À très vite sous le soleil de l'île Maurice! ☀️"
            )
        return {
            "success": True,
            "engine": "Local Mauritius Concierge Engine",
            "reply": fallback
        }

mauritius_sales_engine = MauritiusSalesEngine()
