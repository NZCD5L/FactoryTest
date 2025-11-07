# FactoryTest Project Documentation Index
**Last Updated**: November 5, 2025

---

## 📌 **START HERE: CURRENT ROADMAP**

### **✅ FINAL_PDR_12WEEKS.md** ← **USE THIS ONE**
**The active, approved 12-week plan**
- Local testing first (Weeks 1-5, $0 cost)
- 15 internal team members
- LP agent with gatekeeping (no external audits)
- Total budget: ~$700
- Launch timeline: 12 weeks

**Status**: ✅ APPROVED - Ready to begin Week 1

---

## 📚 **Supporting Documentation**

### **Architecture & Design**

#### **SECURITY_ARCHITECTURE.md**
- Multi-tenant security design (for reference)
- LP gatekeeping strategies
- Row-Level Security (RLS) implementation
- Anti-hallucination techniques
- Testing protocols

**Use for**: Understanding LP security approach

---

#### **aws_architecture.md**
- AWS infrastructure design
- Database schema (PostgreSQL)
- Cost estimates
- Technology stack details

**Use for**: Week 6 AWS deployment reference

---

#### **cost_and_toolstack_explained.md**
- Non-technical explanation of costs
- Why PostgreSQL vs CSV
- Where Python fits in the stack
- Budget breakdowns

**Use for**: Understanding the "why" behind decisions

---

#### **automation_workflows.md**
- Visual workflow diagrams
- ETL pipeline options
- Scheduling strategies
- Tool comparisons

**Use for**: Week 2 automation implementation

---

#### **data_architecture_analysis.md**
- Source of truth options comparison
- Google Drive vs Database vs Hybrid
- Decision criteria

**Use for**: Historical context (decision already made: PostgreSQL)

---

## 🗄️ **Previous Versions (Archive)**

### **REVISED_PDR_5WEEK_PRODUCTION.md**
- Earlier version with accelerated 5-week timeline
- 300-user multi-tenant design
- External security audit requirement
- Cost: $15,367

**Status**: ❌ SUPERSEDED - Too aggressive, too expensive

---

### **PRODUCT_DEVELOPMENT_ROADMAP.md**
- Original 10-week plan
- Test local → AWS production
- No LP considerations yet

**Status**: ❌ SUPERSEDED - Scope changed

---

## 📖 **Quick Start Guides**

### **README.md**
- Basic project overview
- Environment setup instructions
- How to activate virtual environment
- Test script usage

**Use for**: New team member onboarding

---

## 🗂️ **File Organization**

```
FactoryTest/
├── INDEX.md                              ← You are here
├── FINAL_PDR_12WEEKS.md                 ← ACTIVE ROADMAP ✅
├── SECURITY_ARCHITECTURE.md              ← LP security reference
├── README.md                             ← Quick start guide
│
├── Reference Docs (for Week 6+):
│   ├── aws_architecture.md
│   ├── automation_workflows.md
│   ├── cost_and_toolstack_explained.md
│   └── data_architecture_analysis.md
│
├── Archive (previous versions):
│   ├── REVISED_PDR_5WEEK_PRODUCTION.md
│   └── PRODUCT_DEVELOPMENT_ROADMAP.md
│
├── Data Files:
│   ├── Companies.csv                     ← 2,175 rows
│   ├── KPIs_prueba.csv                  ← 21,514 rows
│   └── dealflow_prueba.csv              ← 4,676 rows
│
├── Code:
│   ├── test_setup.py                     ← Environment validator
│   └── venv/                             ← Virtual environment
```

---

## 🎯 **What's Different in the Final Plan?**

| Original Plan | Final Plan (APPROVED) | Why Changed |
|--------------|----------------------|-------------|
| 10 weeks | **12 weeks** | Less rushed, more testing time |
| AWS from Day 1 | **Local first (Weeks 1-5)** | Validate before paying |
| 300 users | **15 internal + LPs** | Realistic scope |
| External security audit ($15k) | **Internal testing** | No budget, internal-only tools |
| $15,367 budget | **~$700 budget** | 95% cost reduction |
| Complex multi-tenant | **Simple LP gatekeeping** | Only LPs need restrictions |

---

## 📅 **Current Status: Week 0 (Planning)**

### ✅ Completed
- [x] Environment setup (Python, pandas, venv)
- [x] CSV files loaded and validated (28k+ rows)
- [x] Architecture designed
- [x] Roadmap approved

### 🔜 Next Steps (Week 1)
- [ ] Install PostgreSQL locally
- [ ] Create database schema
- [ ] Build ETL scripts
- [ ] Load 3 CSV files into database

**Ready to begin!** 🚀

---

## ❓ **Which Document Should I Read?**

### **"I want to start building"**
→ **FINAL_PDR_12WEEKS.md** (Week 1 instructions)

### **"I need to understand LP security"**
→ **SECURITY_ARCHITECTURE.md** (gatekeeping strategies)

### **"I need to explain costs to stakeholders"**
→ **cost_and_toolstack_explained.md** (non-technical)

### **"I need AWS deployment details"**
→ **aws_architecture.md** (Week 6 reference)

### **"I want to understand the workflows"**
→ **automation_workflows.md** (visual diagrams)

### **"I'm a new team member"**
→ **README.md** (quick start)

---

## 🔄 **Document Update Log**

| Date | Document | Change |
|------|----------|--------|
| Nov 5 | FINAL_PDR_12WEEKS.md | Created - approved 12-week plan |
| Nov 5 | SECURITY_ARCHITECTURE.md | Created - LP security design |
| Nov 5 | REVISED_PDR_5WEEK_PRODUCTION.md | Archived - too aggressive |
| Nov 5 | PRODUCT_DEVELOPMENT_ROADMAP.md | Archived - scope changed |
| Nov 5 | aws_architecture.md | Created - reference for Week 6 |
| Nov 5 | cost_and_toolstack_explained.md | Created - non-technical guide |
| Nov 4 | README.md | Created - environment setup |

---

## 📞 **Need Help?**

### **Can't find something?**
- Check this INDEX.md first
- All documents are in `/Users/dannazca/FactoryTest/`

### **Document conflicts?**
- **Use**: FINAL_PDR_12WEEKS.md
- **Ignore**: Other PDR files (archived)

### **Want to update docs?**
- Update FINAL_PDR_12WEEKS.md as the single source of truth
- Update this INDEX.md if adding new files

---

## 🎓 **Key Decisions Made**

1. ✅ **Start local, test free for 5 weeks** before AWS
2. ✅ **PostgreSQL as source of truth** (not CSV)
3. ✅ **Python for all production logic** (R for normalization only)
4. ✅ **LangChain for agents** (not custom framework)
5. ✅ **Streamlit for UI** (open-source, Python-native)
6. ✅ **No external security audits** (internal testing only)
7. ✅ **12-week timeline** (not rushed)
8. ✅ **~$700 budget** (affordable)

---

**Last Updated**: November 5, 2025  
**Active Roadmap**: FINAL_PDR_12WEEKS.md  
**Status**: Ready to begin Week 1! 🚀
