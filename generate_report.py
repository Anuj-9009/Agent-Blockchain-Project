"""
generate_report.py - Refined PDF project report for Agent-Driven Blockchain Voting System.
"""
import os
from fpdf import FPDF

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = "/Users/anuj9009/Downloads/Project_Report.pdf"

SOURCE_FILES = [
    ("blockchain/block.py", "Block Class - Core Data Structure"),
    ("blockchain/chain.py", "Blockchain Class - Chain Management"),
    ("agents/consensus.py", "Consensus Agent - Vote Validation"),
    ("agents/auditor.py", "Auditor Agent - Integrity Monitor"),
    ("app.py", "Flask Application - Dashboard and API"),
    ("requirements.txt", "Project Dependencies"),
]

def safe(text):
    reps = {'\u2014':'-','\u2013':'-','\u2018':"'",'\u2019':"'",'\u201c':'"','\u201d':'"',
            '\u2026':'...','\u2192':'->','\u2190':'<-','\u00b7':'.','\u2022':'*'}
    for k,v in reps.items(): text=text.replace(k,v)
    return ''.join(ch for ch in text if ord(ch)<256)


class Report(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=18)

    def header(self):
        if self.page_no() <= 2:
            return
        self.set_font("Helvetica","I",7)
        self.set_text_color(140,140,140)
        self.cell(95,5,safe("Agent-Driven Blockchain Voting System"),align="L")
        self.cell(95,5,"Project Report",align="R")
        self.ln(2)
        self.set_draw_color(200,200,200)
        self.line(10,self.get_y(),200,self.get_y())
        self.ln(4)

    def footer(self):
        if self.page_no() <= 1:
            return
        self.set_y(-13)
        self.set_font("Helvetica","I",7)
        self.set_text_color(160,160,160)
        self.cell(0,8,f"- {self.page_no()} -",align="C")

    def ch_title(self, num, title):
        # Blue accent bar + chapter title
        self.set_fill_color(20,60,120)
        self.rect(10, self.get_y(), 190, 0.8, 'F')
        self.ln(3)
        self.set_font("Helvetica","B",14)
        self.set_text_color(20,60,120)
        self.cell(0,8,safe(f"{num}.  {title}"),new_x="LMARGIN",new_y="NEXT")
        self.ln(3)

    def sec(self, title):
        self.set_font("Helvetica","B",11)
        self.set_text_color(30,70,130)
        self.ln(2)
        self.cell(0,6,safe(title),new_x="LMARGIN",new_y="NEXT")
        self.ln(1)

    def subsec(self, title):
        self.set_font("Helvetica","BI",9.5)
        self.set_text_color(60,60,60)
        self.cell(0,5,safe(title),new_x="LMARGIN",new_y="NEXT")
        self.ln(1)

    def txt(self, text):
        self.set_font("Helvetica","",9.5)
        self.set_text_color(35,35,35)
        self.multi_cell(0,5,safe(text))
        self.ln(2)

    def bullet(self, text, indent=14):
        self.set_font("Helvetica","",9.5)
        self.set_text_color(35,35,35)
        x0 = self.get_x()
        self.set_x(indent)
        # draw small filled circle
        self.set_fill_color(20,60,120)
        self.ellipse(indent, self.get_y()+1.8, 1.5, 1.5, 'F')
        self.set_x(indent+4)
        self.multi_cell(190-indent-4, 5, safe(text))
        self.ln(0.5)

    def numbr(self, num, text):
        self.set_font("Helvetica","B",9.5)
        self.set_text_color(20,60,120)
        self.set_x(14)
        self.cell(6,5,f"{num}.")
        self.set_font("Helvetica","",9.5)
        self.set_text_color(35,35,35)
        self.multi_cell(170,5,safe(text))
        self.ln(0.5)

    def code(self, code_text, max_lines=None):
        # thin border code block
        self.set_draw_color(200,200,210)
        self.set_font("Courier","",6.8)
        self.set_text_color(40,40,40)
        lines = code_text.split("\n")
        if max_lines and len(lines) > max_lines:
            lines = lines[:max_lines]
            lines.append("    ... (truncated)")
        start_y = self.get_y()
        for line in lines:
            if self.get_y() > 275:
                self.add_page()
            self.set_fill_color(247,247,250)
            self.cell(190,3.6,"  "+safe(line[:135]),fill=True,new_x="LMARGIN",new_y="NEXT")
        self.ln(2)
        self.set_font("Helvetica","",9.5)

    def trow(self, cells, widths, bold=False, header=False, alt=False):
        if header:
            self.set_font("Helvetica","B",8)
            self.set_fill_color(20,60,120)
            self.set_text_color(255,255,255)
        else:
            self.set_font("Helvetica","B" if bold else "",8)
            self.set_text_color(35,35,35)
            if alt:
                self.set_fill_color(242,245,252)
            else:
                self.set_fill_color(255,255,255)
        for cell_text, w in zip(cells, widths):
            self.cell(w,6,safe(str(cell_text)),border=1,fill=True)
        self.ln()


def build():
    pdf = Report()

    # =========== COVER PAGE ===========
    pdf.add_page()
    # decorative top bar
    pdf.set_fill_color(20,60,120)
    pdf.rect(0,0,210,8,'F')
    pdf.set_fill_color(40,100,180)
    pdf.rect(0,8,210,2,'F')
    pdf.ln(30)
    pdf.set_font("Helvetica","B",30)
    pdf.set_text_color(20,60,120)
    pdf.cell(0,14,"PROJECT REPORT",align="C",new_x="LMARGIN",new_y="NEXT")
    pdf.ln(2)
    pdf.set_draw_color(20,60,120)
    pdf.set_line_width(0.5)
    pdf.line(55,pdf.get_y(),155,pdf.get_y())
    pdf.set_line_width(0.2)
    pdf.ln(6)
    pdf.set_font("Helvetica","B",14)
    pdf.set_text_color(40,40,40)
    pdf.cell(0,8,"Agent-Driven Blockchain Voting System",align="C",new_x="LMARGIN",new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("Helvetica","I",9)
    pdf.set_text_color(100,100,100)
    pdf.cell(0,5,"An Intelligent Blockchain System Powered by Autonomous AI Agents",align="C",new_x="LMARGIN",new_y="NEXT")
    pdf.cell(0,5,"for Auditing, Consensus Validation, and Self-Healing",align="C",new_x="LMARGIN",new_y="NEXT")
    pdf.ln(14)

    # Personal detail fields in a box
    pdf.set_draw_color(20,60,120)
    box_y = pdf.get_y()
    pdf.rect(25, box_y, 160, 92)
    pdf.set_fill_color(20,60,120)
    pdf.rect(25, box_y, 160, 7, 'F')
    pdf.set_xy(25, box_y)
    pdf.set_font("Helvetica","B",9)
    pdf.set_text_color(255,255,255)
    pdf.cell(160,7,"STUDENT DETAILS",align="C",new_x="LMARGIN",new_y="NEXT")
    pdf.ln(2)

    for field in ["Name","Roll Number","Enrollment No.","Class / Section",
                   "Course / Subject","Department","College / University","Guided By (Faculty)"]:
        pdf.set_x(32)
        pdf.set_font("Helvetica","B",9.5)
        pdf.set_text_color(50,50,50)
        pdf.cell(42,9,f"{field}:")
        pdf.set_font("Helvetica","",9.5)
        pdf.cell(5,9,"")
        x = pdf.get_x()
        pdf.set_draw_color(160,160,160)
        pdf.dashed_line(x, pdf.get_y()+8, x+95, pdf.get_y()+8, 2, 1.5)
        pdf.ln(9.5)

    pdf.ln(8)
    # Date fields centered
    pdf.set_draw_color(20,60,120)
    pdf.set_line_width(0.3)
    pdf.line(55,pdf.get_y(),155,pdf.get_y())
    pdf.set_line_width(0.2)
    pdf.ln(4)
    pdf.set_font("Helvetica","",9)
    pdf.set_text_color(80,80,80)
    pdf.cell(0,6,"Academic Year: ______________________          Date: ______________________",align="C",new_x="LMARGIN",new_y="NEXT")

    # Bottom bar
    pdf.set_fill_color(20,60,120)
    pdf.rect(0,285,210,8,'F')
    pdf.set_fill_color(40,100,180)
    pdf.rect(0,283,210,2,'F')

    # =========== TABLE OF CONTENTS ===========
    pdf.add_page()
    pdf.set_font("Helvetica","B",16)
    pdf.set_text_color(20,60,120)
    pdf.cell(0,10,"TABLE OF CONTENTS",align="C",new_x="LMARGIN",new_y="NEXT")
    pdf.set_draw_color(20,60,120)
    pdf.line(70,pdf.get_y()+1,140,pdf.get_y()+1)
    pdf.ln(6)

    toc = [
        (1,"Abstract",False),(2,"Introduction",False),(3,"Literature Review",False),
        (4,"System Architecture & Design",False),(5,"Technology Stack",False),
        (6,"Module Descriptions",False),("6.1","Blockchain Core",True),
        ("6.2","Consensus Agent",True),("6.3","Auditor Agent",True),
        ("6.4","Flask Dashboard & API",True),(7,"Source Code",False),
        (8,"Testing & Results",False),(9,"Screenshots",False),
        (10,"Advantages & Limitations",False),(11,"Future Scope",False),
        (12,"Conclusion",False),(13,"References",False),
    ]
    for num, title, sub in toc:
        pdf.set_font("Helvetica","" if sub else "B", 9 if sub else 10)
        pdf.set_text_color(35,35,35)
        pdf.set_x(18 if sub else 12)
        n = str(num)
        pdf.cell(12,6.5,n)
        pdf.cell(140,6.5,title)
        # dotted leader
        pdf.set_font("Helvetica","",8)
        pdf.set_text_color(180,180,180)
        pdf.ln()

    # =========== CH1: ABSTRACT ===========
    pdf.add_page()
    pdf.ch_title(1, "Abstract")
    pdf.txt(
        "This project presents the design and implementation of an Agent-Driven Blockchain "
        "Voting System - an intelligent, tamper-proof electronic voting platform that leverages "
        "autonomous AI agents for real-time auditing, transaction validation, and automatic "
        "self-healing. Unlike conventional database-backed voting systems that rely on "
        "administrator trust and manual auditing, this system employs a SHA-256 hash-chained "
        "blockchain as its core ledger, secured by two intelligent agents: a Consensus Agent "
        "that performs pre-mine validation of vote transactions (including duplicate detection, "
        "format checks, and optional LLM-powered anomaly assessment), and an Auditor Agent "
        "that continuously monitors the chain integrity as a background daemon thread, "
        "automatically detecting tampering and triggering a self-healing revert protocol."
    )
    pdf.txt(
        "The system is built using Python 3.10+ and Flask 3.0, featuring a modern, responsive "
        "web dashboard with real-time agent log visualization, a REST API for programmatic "
        "interaction, and support for optional LLM integration (OpenAI GPT / Anthropic Claude) "
        "to enhance agent reasoning capabilities."
    )
    pdf.set_font("Helvetica","B",9)
    pdf.set_text_color(20,60,120)
    pdf.cell(0,5,"Keywords:",new_x="LMARGIN",new_y="NEXT")
    pdf.set_font("Helvetica","I",9)
    pdf.set_text_color(60,60,60)
    pdf.cell(0,5,"Blockchain, AI Agents, Consensus Protocol, Auditing, Self-Healing, SHA-256, Flask, Python, Voting System",new_x="LMARGIN",new_y="NEXT")
    pdf.ln(3)

    # =========== CH2: INTRODUCTION ===========
    pdf.ch_title(2, "Introduction")
    pdf.sec("2.1  Background")
    pdf.txt(
        "Electronic voting systems are critical to modern democratic processes, yet they face "
        "persistent challenges related to data integrity, transparency, and trust. Traditional "
        "systems store votes in centralized databases where a single compromised administrator "
        "can alter results, audits are performed manually, and recovery from data corruption "
        "requires manual backup restoration."
    )
    # Comparison table
    pdf.sec("Why Blockchain + Agents?")
    w_comp = [45, 65, 80]
    pdf.trow(["Feature","Normal Database","This System"], w_comp, header=True)
    pdf.trow(["Data Integrity","Trust the admin","Cryptographic proof (SHA-256)"], w_comp, alt=True)
    pdf.trow(["Tamper Detection","Manual audits","Real-time Auditor Agent"], w_comp)
    pdf.trow(["Validation","Static SQL constraints","Intelligent Consensus Agent"], w_comp, alt=True)
    pdf.trow(["Recovery","Restore from backup","Automatic self-healing"], w_comp)
    pdf.trow(["Transparency","Query logs manually","Live dashboard + agent logs"], w_comp, alt=True)
    pdf.ln(2)

    pdf.sec("2.2  Problem Statement")
    pdf.txt(
        "How can we build a voting system that is inherently tamper-resistant, self-auditing, "
        "and capable of automatic recovery from integrity violations - without relying on a "
        "trusted central authority?"
    )
    pdf.sec("2.3  Proposed Solution")
    pdf.bullet("A SHA-256 hash-chained blockchain providing cryptographic proof of data integrity.")
    pdf.bullet("A Consensus Agent performing intelligent, multi-layered validation of every vote.")
    pdf.bullet("An Auditor Agent running as a background daemon with automatic self-healing.")
    pdf.sec("2.4  Objectives")
    pdf.numbr(1,"Implement a functional blockchain with Proof-of-Work consensus")
    pdf.numbr(2,"Design autonomous AI agents for real-time chain monitoring")
    pdf.numbr(3,"Build a self-healing mechanism to revert the chain on tamper detection")
    pdf.numbr(4,"Develop a web dashboard for live blockchain and agent log visualization")
    pdf.numbr(5,"Provide REST API endpoints for programmatic access")
    pdf.numbr(6,"Support optional LLM integration for enhanced agent intelligence")

    # =========== CH3: LITERATURE REVIEW ===========
    pdf.add_page()
    pdf.ch_title(3, "Literature Review")
    pdf.sec("3.1  Blockchain Technology")
    pdf.txt(
        "Blockchain technology, first conceptualized by Satoshi Nakamoto in 2008 through the "
        "Bitcoin whitepaper, provides a distributed, immutable ledger secured by cryptographic "
        "hash functions. Each block contains a hash of the previous block, creating a tamper-evident "
        "structure. Key concepts: SHA-256 hashing, Proof-of-Work mining, nonce computation, "
        "and chain validation."
    )
    pdf.sec("3.2  Multi-Agent Systems (MAS)")
    pdf.txt(
        "Multi-Agent Systems consist of autonomous software entities that perceive their "
        "environment, make decisions, and act to achieve goals. The Consensus Agent and "
        "Auditor Agent exhibit key MAS properties: autonomy, reactivity, and pro-activeness, "
        "sharing a common state (the blockchain) while operating independently."
    )
    pdf.sec("3.3  Blockchain-Based Voting")
    pdf.txt(
        "Projects like Voatz, Follow My Vote, and Agora have explored blockchain for voting "
        "but focus on the blockchain layer alone. This project adds an autonomous agent layer "
        "for continuous security monitoring and self-healing - a key differentiator."
    )
    pdf.sec("3.4  LLMs in Security")
    pdf.txt(
        "This project optionally leverages LLMs (GPT/Claude) for: (1) Consensus Agent anomaly "
        "assessment via natural language reasoning, and (2) Auditor Agent human-readable "
        "explanations of integrity violations. Falls back to rule-based logic without API keys."
    )

    # =========== CH4: ARCHITECTURE ===========
    pdf.add_page()
    pdf.ch_title(4, "System Architecture & Design")
    pdf.sec("4.1  Layered Architecture")
    pdf.bullet("Presentation Layer - Flask web dashboard with real-time updates")
    pdf.bullet("API Layer - RESTful endpoints (/mine, /chain, /tamper, /logs, /health)")
    pdf.bullet("Agent Layer - Consensus Agent (pre-mine) + Auditor Agent (background daemon)")
    pdf.bullet("Blockchain Core - Block + Blockchain classes (SHA-256, PoW, validation, self-healing)")
    pdf.sec("4.2  Visual Architecture Data Flow Diagram")
    pdf.ln(4)
    start_y = pdf.get_y()
    
    def box(x, y, w, h, text, color=(242,245,252)):
        pdf.set_fill_color(*color)
        pdf.set_draw_color(20,60,120)
        pdf.set_line_width(0.4)
        pdf.rect(x, y, w, h, 'DF')
        lines = len(text.split('\n'))
        text_h = lines * 4
        pdf.set_xy(x, y + (h - text_h) / 2)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(20,60,120)
        pdf.multi_cell(w, 4, safe(text), align="C")

    # Layer 1
    box(30, start_y, 50, 14, "Web Dashboard\n(HTML/CSS/JS)")
    box(130, start_y, 50, 14, "REST API\n(/mine, /chain, /logs)")
    
    # Inter-layer connections
    pdf.set_draw_color(100,100,100)
    pdf.line(80, start_y+7, 130, start_y+7)
    
    pdf.line(155, start_y+14, 155, start_y+22)
    pdf.line(60, start_y+22, 155, start_y+22)
    
    # Layer 2 Agents
    pdf.line(60, start_y+22, 60, start_y+26)
    pdf.line(155, start_y+22, 155, start_y+26)
    
    box(30, start_y+26, 60, 14, "Consensus Agent\n(Pre-mine Validation)", color=(255,245,235))
    box(125, start_y+26, 60, 14, "Auditor Agent\n(Monitoring & Healing)", color=(255,245,235))
    
    # Base connections
    pdf.line(60, start_y+40, 60, start_y+48)
    pdf.line(155, start_y+40, 155, start_y+48)
    pdf.line(60, start_y+48, 155, start_y+48)
    pdf.line(107, start_y+48, 107, start_y+53)
    
    # Layer 3 Core
    box(77, start_y+53, 60, 14, "Blockchain Core\n(SHA-256 / PoW)", color=(235,250,235))
    
    # Chain Diagram below Core
    pdf.set_draw_color(160,160,160)
    box(30, start_y+78, 28, 12, "Block 0\nGenesis", color=(245,245,245))
    pdf.line(58, start_y+84, 68, start_y+84)
    box(68, start_y+78, 28, 12, "Block 1", color=(245,245,245))
    pdf.line(96, start_y+84, 106, start_y+84)
    box(106, start_y+78, 28, 12, "Block 2", color=(245,245,245))
    pdf.line(134, start_y+84, 144, start_y+84)
    box(144, start_y+78, 28, 12, "Block N", color=(245,245,245))
    
    pdf.set_y(start_y + 95)
    pdf.sec("4.3  Data Flow")
    pdf.numbr(1,"User submits vote via dashboard or API (POST /mine)")
    pdf.numbr(2,"Consensus Agent validates (fields, duplicates, format, optional LLM)")
    pdf.numbr(3,"If approved, blockchain mines block (SHA-256 + Proof-of-Work)")
    pdf.numbr(4,"Auditor Agent (background, every 5s) validates entire chain")
    pdf.numbr(5,"On tamper detection: explanation generated, self-healing triggered")

    # =========== CH5: TECH STACK ===========
    pdf.add_page()
    pdf.ch_title(5, "Technology Stack")
    w = [48,52,90]
    pdf.trow(["Technology","Version","Purpose"], w, header=True)
    rows = [
        ["Python","3.10+","Core programming language"],
        ["Flask","3.0+","Web framework for dashboard & API"],
        ["hashlib (SHA-256)","stdlib","Cryptographic hashing for blocks"],
        ["threading","stdlib","Background daemon for Auditor Agent"],
        ["JSON","stdlib","Block data serialization"],
        ["requests","2.31+","HTTP client for LLM API calls"],
        ["OpenAI API","Optional","LLM for enhanced agent reasoning"],
        ["Anthropic API","Optional","Alternative LLM provider"],
        ["HTML5/CSS3/JS","--","Dashboard UI & frontend logic"],
    ]
    for i,row in enumerate(rows):
        pdf.trow(row, w, alt=(i%2==0))

    # =========== CH6: MODULES ===========
    pdf.add_page()
    pdf.ch_title(6, "Module Descriptions")
    pdf.sec("6.1  Blockchain Core")
    pdf.subsec("Block Class (blockchain/block.py)")
    pdf.txt("Each block stores: index, timestamp, transaction data, previous block's SHA-256 hash, nonce, and its own hash.")
    pdf.bullet("calculate_hash() - Deterministic SHA-256 hash from all block fields")
    pdf.bullet("mine(difficulty) - PoW: increments nonce until hash has leading zeros")
    pdf.bullet("to_dict() - Serializes block for JSON API responses")
    pdf.subsec("Blockchain Class (blockchain/chain.py)")
    pdf.txt("Thread-safe chain manager using threading.Lock:")
    pdf.bullet("_create_genesis_block() - First block with zeroed previous hash")
    pdf.bullet("add_block(data) - Mines and appends new block linked to latest hash")
    pdf.bullet("is_chain_valid() - Verifies hash integrity and chain linkage")
    pdf.bullet("tamper_block() - Corrupts block WITHOUT re-mining (demo)")
    pdf.bullet("revert_to_valid_state() - Self-healing: truncates from first corrupted block")
    pdf.sec("6.2  Consensus Agent (agents/consensus.py)")
    pdf.txt("Pre-mine peer review with four validation layers:")
    pdf.bullet("Required Fields - voter_id and candidate must be present and non-empty")
    pdf.bullet("Duplicate Detection - Thread-safe set rejects double votes")
    pdf.bullet("Format Validation - Length checks + injection character scanning")
    pdf.bullet("LLM Review (Optional) - GPT/Claude anomaly assessment")
    pdf.sec("6.3  Auditor Agent (agents/auditor.py)")
    pdf.txt("Background daemon thread polling every 5 seconds:")
    pdf.numbr(1,"Calls is_chain_valid() each cycle")
    pdf.numbr(2,"On violation: generates explanation (LLM or rule-based fallback)")
    pdf.numbr(3,"Logs violation to shared agent_logs (thread-safe)")
    pdf.numbr(4,"Triggers self-healing: truncates chain, preserves valid blocks")
    pdf.sec("6.4  Flask Dashboard & API (app.py)")
    w2 = [28,16,90,56]
    pdf.trow(["Route","Method","Description","Handler"], w2, header=True)
    api = [
        ["/","GET","Dashboard UI","dashboard()"],
        ["/chain","GET","Full blockchain as JSON","get_chain()"],
        ["/mine","POST","Vote -> Consensus review -> mine block","mine_block()"],
        ["/tamper/<i>","POST","Corrupt a block for demo","tamper()"],
        ["/logs","GET","Agent logs as JSON","get_logs()"],
        ["/health","GET","System health check","health()"],
    ]
    for i,row in enumerate(api):
        pdf.trow(row, w2, alt=(i%2==0))

    # =========== CH7: SOURCE CODE ===========
    pdf.add_page()
    pdf.ch_title(7, "Source Code")
    pdf.txt("Complete source code for all project modules:")
    for i, (filepath, desc) in enumerate(SOURCE_FILES, 1):
        abs_path = os.path.join(PROJECT_DIR, filepath)
        if not os.path.exists(abs_path):
            continue
        pdf.sec(f"7.{i}  {filepath}")
        pdf.set_font("Helvetica","I",8)
        pdf.set_text_color(90,90,90)
        pdf.cell(0,4,safe(desc),new_x="LMARGIN",new_y="NEXT")
        pdf.ln(1)
        with open(abs_path,"r") as f:
            code_text = f.read()
        ml = 180 if filepath == "app.py" else None
        if filepath == "app.py":
            pdf.set_font("Helvetica","I",7.5)
            pdf.set_text_color(120,120,120)
            pdf.cell(0,4,"(First 180 lines shown; full file is ~923 lines including HTML/CSS/JS)",new_x="LMARGIN",new_y="NEXT")
            pdf.ln(1)
        pdf.code(code_text, max_lines=ml)

    # =========== CH8: TESTING ===========
    pdf.add_page()
    pdf.ch_title(8, "Testing & Results")
    pdf.sec("8.1  Functional Test Cases")
    w3 = [8,52,52,42,36]
    pdf.trow(["#","Test Case","Expected","Actual","Status"], w3, header=True)
    tests = [
        ["1","Mine valid vote (VOTER-001)","Block #1 mined","Block #1 mined","PASS"],
        ["2","Mine second vote (VOTER-002)","Block #2 mined","Block #2 mined","PASS"],
        ["3","Duplicate vote (VOTER-001)","Rejected by Consensus","Rejected","PASS"],
        ["4","Empty voter_id","Rejected - missing field","Rejected","PASS"],
        ["5","Injection chars in input","Rejected - suspicious","Rejected","PASS"],
        ["6","Tamper Block #1","Auditor detects","Detected + healed","PASS"],
        ["7","Self-healing after tamper","Chain reverted","Reverted 1 block","PASS"],
        ["8","Health check endpoint","{status: healthy}","healthy","PASS"],
        ["9","Chain validation (clean)","is_valid: true","true","PASS"],
        ["10","Dashboard loads","UI renders, no errors","Renders OK","PASS"],
    ]
    for i,t in enumerate(tests):
        pdf.trow(t, w3, alt=(i%2==0))
    pdf.ln(3)
    pdf.sec("8.2  API Testing (cURL)")
    pdf.subsec("Mining a vote:")
    pdf.code('curl -X POST http://localhost:5001/mine \\\n  -H "Content-Type: application/json" \\\n  -d \'{"voter_id": "VOTER-001", "candidate": "Alice Johnson"}\'')
    pdf.subsec("Success response:")
    pdf.code('{\n  "success": true,\n  "block": {"index":1, "data":{"voter_id":"VOTER-001","candidate":"Alice Johnson"}},\n  "consensus": "APPROVED: Transaction passes all validation checks."\n}')

    # =========== CH9: SCREENSHOTS ===========
    pdf.add_page()
    pdf.ch_title(9, "Screenshots")
    ss_dir = "/Users/anuj9009/.gemini/antigravity/brain/87459159-85a1-4477-ab5f-47e7511aafc7"
    screenshots = [
        ("dashboard_redesigned.png","Dashboard - Main View"),
        ("initial_dashboard_1772923878498.png","Initial State with Genesis Block"),
        ("block_1_mined_1772923909848.png","After Mining Block #1"),
        ("tamper_detection_successful_1772925145986.png","Tamper Detection Alert"),
        ("final_tamper_detection_check_1772925184594.png","Chain Integrity Restored"),
    ]
    for fname, caption in screenshots:
        fp = os.path.join(ss_dir, fname)
        if os.path.exists(fp):
            try:
                pdf.subsec(caption)
                pdf.image(fp, x=15, w=180)
                pdf.ln(3)
                if pdf.get_y() > 220:
                    pdf.add_page()
            except Exception:
                pdf.txt(f"[Screenshot: {caption}]")
        else:
            pdf.txt(f"[Attach: {caption}]")

    # =========== CH10: ADVANTAGES & LIMITATIONS ===========
    pdf.add_page()
    pdf.ch_title(10, "Advantages & Limitations")
    pdf.sec("Advantages")
    pdf.bullet("Tamper-Proof: SHA-256 hash chain makes unauthorized modification immediately detectable")
    pdf.bullet("Self-Healing: Automatic revert to last valid state without human intervention")
    pdf.bullet("Intelligent Validation: Consensus Agent catches anomalies static SQL constraints miss")
    pdf.bullet("Real-Time Monitoring: Auditor Agent runs continuously as a background daemon")
    pdf.bullet("LLM-Enhanced: Optional AI-powered reasoning for deeper security analysis")
    pdf.bullet("Transparent: All agent activity logged and visible on live dashboard")
    pdf.bullet("Modular: Clean separation of blockchain core, agents, and web layer")
    pdf.bullet("Zero-Config: Works out of the box without any API key")
    pdf.sec("Limitations")
    pdf.bullet("Single-Node: Runs on one server (not a distributed network)")
    pdf.bullet("In-Memory: Data lost on server restart (no database persistence)")
    pdf.bullet("Simplified PoW: Difficulty 2 is for demo, not production")
    pdf.bullet("No Voter Auth: Validates format but not voter identity")
    pdf.bullet("LLM Cost: OpenAI/Anthropic APIs incur per-call charges")

    # =========== CH11: FUTURE SCOPE ===========
    pdf.ch_title(11, "Future Scope")
    pdf.bullet("Distributed Network - Multiple nodes with P2P communication and PBFT/Raft consensus")
    pdf.bullet("Persistent Storage - SQLite/PostgreSQL for chain persistence across restarts")
    pdf.bullet("Voter Authentication - Biometric/ID verification using zero-knowledge proofs")
    pdf.bullet("Smart Contracts - Programmable voting rules (ranked-choice, weighted votes)")
    pdf.bullet("Mobile App - Companion app with push notifications for agent events")
    pdf.bullet("Advanced Agents - Prediction Agent for statistical anomaly detection")
    pdf.bullet("Production Security - TLS, rate limiting, proper API authentication")

    # =========== CH12: CONCLUSION ===========
    pdf.add_page()
    pdf.ch_title(12, "Conclusion")
    pdf.txt(
        "This project successfully demonstrates the design, implementation, and testing of an "
        "Agent-Driven Blockchain Voting System - a comprehensive platform integrating blockchain "
        "technology with autonomous AI agents to create a secure, transparent, and self-healing "
        "electronic voting system."
    )
    pdf.txt("Key accomplishments:")
    pdf.bullet("Fully functional blockchain with SHA-256 hashing and PoW mining for cryptographic vote integrity")
    pdf.bullet("Two autonomous AI agents (Consensus + Auditor) providing intelligent, real-time security")
    pdf.bullet("Self-healing mechanism automatically detecting tampering and reverting to last valid state")
    pdf.bullet("Modern web dashboard with real-time blockchain and agent activity visualization")
    pdf.bullet("Optional LLM integration enhancing agent reasoning while maintaining standalone functionality")
    pdf.txt(
        "The system was tested across 10 functional test cases covering normal operation, edge "
        "cases, attack scenarios, and recovery - all passed successfully. The project demonstrates "
        "that blockchain technology combined with intelligent agents can create voting systems "
        "fundamentally more secure than traditional centralized approaches."
    )

    # =========== CH13: REFERENCES ===========
    pdf.ch_title(13, "References")
    refs = [
        '[1]  Nakamoto, S. (2008). "Bitcoin: A Peer-to-Peer Electronic Cash System." bitcoin.org.',
        '[2]  Zheng, Z. et al. (2017). "An Overview of Blockchain Technology." IEEE BigData Congress.',
        '[3]  Wooldridge, M. (2009). "An Introduction to MultiAgent Systems." Wiley, 2nd Ed.',
        '[4]  Hardwick, F.S. et al. (2018). "E-Voting with Blockchain." IEEE ISI.',
        '[5]  Flask Documentation. https://flask.palletsprojects.com/',
        '[6]  Python hashlib. https://docs.python.org/3/library/hashlib.html',
        '[7]  OpenAI API. https://platform.openai.com/docs/api-reference',
        '[8]  Anthropic API. https://docs.anthropic.com/',
        '[9]  NIST FIPS 180-4. "Secure Hash Standard." NIST.',
        '[10] Kshetri & Voas (2018). "Blockchain-Enabled E-Voting." IEEE Software 35(4).',
    ]
    for ref in refs:
        pdf.set_font("Helvetica","",8.5)
        pdf.set_text_color(35,35,35)
        pdf.multi_cell(0,4.5,safe(ref))
        pdf.ln(1.5)

    pdf.output(OUTPUT_FILE)
    print(f"\n{'='*55}")
    print(f"  Report generated!")
    print(f"  File: {OUTPUT_FILE}")
    print(f"  Pages: {pdf.page_no()}")
    print(f"{'='*55}\n")

if __name__ == "__main__":
    build()
