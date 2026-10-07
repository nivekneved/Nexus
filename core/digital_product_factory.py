"""
Nexus™ Digital Product (eBook) Factory
======================================
Automatically authors, formats, and generates PDF eBooks and digital guides
to instantly stock the Shopify-style digital storefront with 100% margin products.
"""

import os
import time
import logging
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

logger = logging.getLogger("Nexus.DigitalProductFactory")

PRODUCTS_DIR = os.path.abspath("products")
if not os.path.exists(PRODUCTS_DIR):
    os.makedirs(PRODUCTS_DIR)

class DigitalProductFactory:
    @staticmethod
    def generate_ebook(title: str, author: str, chapters: dict, filename: str) -> str:
        """Generates a professional PDF eBook."""
        filepath = os.path.join(PRODUCTS_DIR, filename)

        doc = SimpleDocTemplate(filepath, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontSize=28,
            spaceAfter=30,
            textColor=colors.HexColor("#0f172a"),
            alignment=1 # Center
        )
        chapter_style = ParagraphStyle(
            'ChapterStyle',
            parent=styles['Heading2'],
            fontSize=18,
            spaceBefore=20,
            spaceAfter=15,
            textColor=colors.HexColor("#0284c7")
        )
        body_style = styles["BodyText"]
        body_style.fontSize = 12
        body_style.leading = 18

        story = []

        # Title Page
        story.append(Spacer(1, 100))
        story.append(Paragraph(title, title_style))
        story.append(Paragraph(f"By {author}", styles['Normal']))
        story.append(Spacer(1, 200))
        story.append(Paragraph("Published by Nexus Autonomous Ventures", styles['Italic']))

        # We need a page break, but to keep it simple, we just add space
        for _ in range(5):
            story.append(Spacer(1, 50))

        # Chapters
        for chap_title, content in chapters.items():
            story.append(Paragraph(chap_title, chapter_style))
            for paragraph in content.split('\n\n'):
                story.append(Paragraph(paragraph.replace('\n', ' '), body_style))
                story.append(Spacer(1, 12))

            for _ in range(2):
                story.append(Spacer(1, 50))

        doc.build(story)
        logger.info(f"[DigitalProductFactory] Successfully minted eBook: {filename}")
        return filepath

digital_product_factory = DigitalProductFactory()
