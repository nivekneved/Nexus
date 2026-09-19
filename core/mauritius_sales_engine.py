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
                "offer": "360° Healthcare Web Portal & Clinic Operations Suite (Live Reference: med360.mu / https://medical360.vercel.app)",
                "setup_fee": 90000,
                "currency": "MUR",
                "retainer_fee": "Rs 10,000 / mo (or Rs 45,000 Front + Rs 45,000 Back = Rs 90,000 Full-Stack)",
                "demo_url": "https://medical360.vercel.app",
                "sold_reference": "med360.mu / medical360.vercel.app (Live-Tested & Sold)",
                "value_prop": "Production-proven healthcare operations suite deployed at med360.mu. Practitioner directory by specialty, 24/7 online consultation booking, blood bank donor registry, and diagnostic lab booking.",
                "sample_pitch_fr": (
                    "Bonjour Dr! 👋\n\n"
                    "C'est Deven de Nexus AI Solutions à Maurice (+230 58169420).\n\n"
                    "Pour un cabinet ou une clinique médicale à Maurice, offrir une prise en charge numérique fluide est essentiel pour désengorger le secrétariat et attirer de nouveaux patients.\n\n"
                    "Notre plateforme médicale 360° a déjà fait ses preuves en production (référence vendue : med360.mu) :\n"
                    "👉 Démo en direct : https://medical360.vercel.app (med360.mu)\n\n"
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
        if sector_id == "ennrevennsourir_ngo":
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
                "Répondez avec le numéro de votre choix ou visitez https://medical360.vercel.app pour réserver directement en ligne."
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
