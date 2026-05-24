"""
generate_ppt.py - Ultra-Premium 'Keynote' Style Presentation
Features: Full-bleed photorealistic AI assets, brutalist typography, pure negative space.
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from lxml import etree

OUTPUT_FILE = "/Users/anuj9009/Downloads/Project_Presentation.pptx"
SS_DIR = "/Users/anuj9009/.gemini/antigravity/brain/87459159-85a1-4477-ab5f-47e7511aafc7"

# The stunning AI generated asset
BG_HERO = "/Users/anuj9009/.gemini/antigravity/brain/03c1ae03-bcde-4e3e-9052-76571198ad3e/bg_blockchain_nodes_1775047833084.png"

# ── APPLE DESIGN SYSTEM (COLORS) ─────────────────────────────
BLACK = RGBColor(0, 0, 0)
WHITE = RGBColor(255, 255, 255)
LIGHT_GRAY = RGBColor(142, 142, 147)
NEON_BLUE = RGBColor(10, 132, 255)
NEON_GREEN = RGBColor(48, 209, 88)
NEON_ORG = RGBColor(255, 159, 10)

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
P_NS = 'http://schemas.openxmlformats.org/presentationml/2006/main'

def add_transition(slide, kind='fade', spd='fast'):
    sld = slide._element
    t = etree.SubElement(sld, f'{{{P_NS}}}transition')
    t.set('spd', spd); t.set('advClick', '1')
    etree.SubElement(t, f'{{{P_NS}}}fade'); e = slide._element.xpath(f'.//p:transition/p:fade', namespaces={'p': P_NS})
    if e: e[0].set('thruBlk', '0')

# ── VISUAL HELPERS ─────────────────────────────────────────────
def add_bg(s, c=BLACK):
    f = s.background.fill; f.solid(); f.fore_color.rgb = c

def add_hero_bg(slide):
    """Adds the AI generated image perfectly scaled to the absolute edges of the slide."""
    if os.path.exists(BG_HERO):
        pic = slide.shapes.add_picture(BG_HERO, 0, -Inches(1.0), width=SLIDE_W)
        # Move image to back of the slide's z-order (simulating background)
        slide.shapes._spTree.remove(pic._element)
        slide.shapes._spTree.insert(2, pic._element)

def ttx(s, txt, l, t, w, h, sz=36, c=WHITE, b=True, al=PP_ALIGN.CENTER):
    """Paints huge, borderless, perfectly aligned text."""
    tb = s.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = txt
    p.font.size = Pt(sz); p.font.color.rgb = c
    p.font.bold = b; p.alignment = al
    return tf

# ── BUILD THE MASTERPIECE ────────────────────────────────────
def create_presentation():
    prs = Presentation(); prs.slide_width = SLIDE_W; prs.slide_height = SLIDE_H

    # SLIDE 1: The Title
    sl = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(sl); add_hero_bg(sl)
    ttx(sl, "Agent-Driven Blockchain", Inches(0.5), Inches(2.8), Inches(12.333), Inches(2.0), 72, WHITE, True)
    ttx(sl, "Next-Generation Digital Trust.", Inches(0.5), Inches(4.5), Inches(12.333), Inches(1.0), 32, LIGHT_GRAY, False)

    # SLIDE 2: The Core Problem (Statement 1)
    sl = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(sl)
    ttx(sl, "Voting systems currently rely on\nblind trust.", Inches(1.0), Inches(2.8), Inches(11.333), Inches(2.0), 60, NEON_ORG, False)

    # SLIDE 3: The Core Problem (Statement 2)
    sl = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(sl)
    ttx(sl, "Single Points of Failure.", Inches(1.0), Inches(3.0), Inches(11.333), Inches(2.0), 80, WHITE, True)

    # SLIDE 4: The Paradigm Shift
    sl = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(sl); add_hero_bg(sl)
    ttx(sl, "Blockchain + AI Agents", Inches(1.0), Inches(3.0), Inches(11.333), Inches(2.0), 80, NEON_BLUE, True)

    # SLIDE 5: The Ledger
    sl = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(sl)
    ttx(sl, "SHA-256 Ledger", Inches(1.0), Inches(2.5), Inches(11.333), Inches(1.5), 72, WHITE, True)
    ttx(sl, "Cryptographic. Immutable. Proof-of-Work.", Inches(1.0), Inches(4.0), Inches(11.333), Inches(1.0), 36, LIGHT_GRAY, False)

    # SLIDE 6: Agent One
    sl = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(sl)
    ttx(sl, "The Gatekeeper", Inches(1.0), Inches(2.5), Inches(11.333), Inches(1.5), 80, NEON_GREEN, True)
    ttx(sl, "Our Consensus Agent constantly guarantees only pure,\nvalidated data enters the chain.", Inches(1.0), Inches(4.2), Inches(11.333), Inches(1.5), 32, LIGHT_GRAY, False)

    # SLIDE 7: Agent Two
    sl = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(sl)
    ttx(sl, "The Watchdog", Inches(1.0), Inches(2.5), Inches(11.333), Inches(1.5), 80, NEON_ORG, True)
    ttx(sl, "Our Auditor Agent persistently recalculates hashes in the background,\ntriggering instant, autonomous self-healing if tampering occurs.", Inches(1.0), Inches(4.2), Inches(11.333), Inches(2.0), 32, LIGHT_GRAY, False)

    # SLIDE 8: The Data - Pure Apple Keynote Flex
    sl = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(sl)
    ttx(sl, "10 / 10", Inches(1.0), Inches(1.8), Inches(11.333), Inches(3.0), 180, NEON_GREEN, True)
    ttx(sl, "Security Breaches Averted. Tests Successfully Passed.", Inches(1.0), Inches(5.2), Inches(11.333), Inches(1.0), 32, LIGHT_GRAY, False)

    # SLIDE 9: Web Interface Screenshot (If available)
    sl = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(sl)
    ss = os.path.join(SS_DIR, "dashboard_redesigned.png")
    if os.path.exists(ss):
        # We borderlessly float the screenshot in the black void
        sl.shapes.add_picture(ss, Inches(1.6), Inches(1.2), Inches(10.1), Inches(5.0))
        ttx(sl, "Real-Time Agent Dashboard", Inches(1.0), Inches(6.5), Inches(11.333), Inches(1.0), 24, LIGHT_GRAY, False)
    else:
        ttx(sl, "Real-Time Agent Dashboard UI", Inches(1.0), Inches(3.0), Inches(11.333), Inches(2.0), 60, NEON_BLUE, True)

    # SLIDE 10: Conclusion
    sl = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(sl); add_hero_bg(sl)
    ttx(sl, "A Fundamentally More Secure\nFoundation For Digital Trust.", Inches(1.0), Inches(2.5), Inches(11.333), Inches(2.5), 52, WHITE, True)
    ttx(sl, "Thank You.", Inches(1.0), Inches(5.5), Inches(11.333), Inches(1.0), 24, LIGHT_GRAY, False)

    prs.save(OUTPUT_FILE)
    print(f"\n{'='*60}")
    print(f"  [OK] Ultra-Premium Cinematic Presentation Generated!")
    print(f"  File: {OUTPUT_FILE}")
    print(f"  Slides: {len(prs.slides)}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    create_presentation()
