# Product Development Roadmap - FactoryTest AI Agent Platform
## 10-Week Delivery Plan (Test Local → Production on AWS)

---

## 🎯 Project Overview

**Mission**: Build an AI-powered agent platform to analyze venture capital data (Companies, KPIs, Deal Flow)

**Team Profile**: Low/vibe coders without deep technical acumen  
**Approach**: Test everything locally (free) → Migrate to AWS when validated  
**Timeline**: 10 weeks to production  
**Cost**: $0 during testing (Weeks 1-6) → $70-132/month production (Weeks 7-10)

---

## 📊 Success Metrics

| Phase | Metric | Target |
|-------|--------|--------|
| **Week 4** | Working local prototype | ✓ 3 agents functional |
| **Week 6** | User acceptance | ✓ 80% positive feedback |
| **Week 8** | AWS deployment | ✓ System running 24/7 |
| **Week 10** | Production launch | ✓ <5 users active daily |

---

# 🗓️ Week-by-Week Breakdown

---

## **PHASE 1: LOCAL FOUNDATION (Weeks 1-2)**
**Goal**: Build core infrastructure on your laptop  
**Cost**: $0  
**Location**: `/Users/dannazca/FactoryTest/`

---

### **Week 1: Database & ETL Setup**

#### Day 1-2: Local PostgreSQL Setup
**Tasks**:
- [ ] Install PostgreSQL on Mac (via Homebrew)
- [ ] Create database `factorytest_db`
- [ ] Create 3 tables: `companies`, `kpis`, `dealflow`
- [ ] Add indexes for performance
- [ ] Create `data_versions` metadata table

**Deliverables**:
```sql
-- Database schema ready
-- Test queries working
-- Sample data loaded
```

**Who Does What**:
- **Developer**: Schema creation, SQL scripts
- **Team**: Review data model, suggest changes

**Tools Installed**:
- PostgreSQL 16
- pgAdmin (visual database manager)
- psycopg2 (Python library)

---

#### Day 3-5: ETL Pipeline (CSV → PostgreSQL)
**Tasks**:
- [ ] Build Python script to read CSVs
- [ ] Data validation rules (check for nulls, duplicates)
- [ ] Data transformation (normalize dates, currencies)
- [ ] Insert data into PostgreSQL
- [ ] Handle conflicts (update vs insert logic)
- [ ] Export PostgreSQL → CSV (for R team compatibility)

**Deliverables**:
```python
# Scripts created:
etl_companies.py     # Loads Companies.csv
etl_kpis.py         # Loads KPIs_prueba.csv  
etl_dealflow.py     # Loads dealflow_prueba.csv
export_to_csv.py    # Exports back to CSV for R team
```

**Test Cases**:
- ✓ Load all 3 CSVs successfully
- ✓ No duplicates in database
- ✓ Exported CSVs match original format
- ✓ Can re-run without errors

**Who Does What**:
- **Developer**: Build ETL scripts
- **Team**: Provide data validation rules, test with real files

---

### **Week 2: Automation & Data Quality**

#### Day 1-3: Scheduling & Automation (Local)
**Tasks**:
- [ ] Install Apache Airflow locally
- [ ] Create DAGs (workflows) for:
  - Weekly KPI updates
  - Monthly Companies/DealFlow updates
- [ ] Add data quality checks
- [ ] Email notifications on success/failure
- [ ] Backup old data to S3-like local folder

**Deliverables**:
```python
# Airflow DAGs created:
dag_weekly_kpis.py       # Runs every Monday
dag_monthly_updates.py   # Runs 1st of month
dag_data_quality.py      # Daily validation checks
```

**Visual Workflow**:
```
Monday 9 AM → Download KPIs_prueba.csv → Validate → Load to DB → Notify
1st of Month → Download Companies + DealFlow → Merge → Load → Notify
```

**Who Does What**:
- **Developer**: Set up Airflow, create DAGs
- **Team**: Test manual triggers, review notifications

---

#### Day 4-5: Integration with Google Drive & Dropbox
**Tasks**:
- [ ] Set up Google Drive API credentials
- [ ] Set up Dropbox API credentials
- [ ] Test automatic download of CSVs
- [ ] Store raw files in `/data/raw/` folder
- [ ] Version control (keep last 10 versions)

**Deliverables**:
- ✓ Scripts can download from Drive/Dropbox automatically
- ✓ No manual intervention needed
- ✓ Historical versions saved

**Who Does What**:
- **You**: Provide API credentials (I'll guide you)
- **Developer**: Integrate APIs into ETL scripts

---

### **Week 2 Milestone: Data Pipeline Working** ✅
**Demo**: 
- CSVs automatically sync to PostgreSQL
- Can query data with SQL
- R team can still use exported CSVs
- Scheduling works (simulated)

---

## **PHASE 2: AI AGENTS & UI (Weeks 3-4)**
**Goal**: Build working prototype with agents  
**Cost**: $0 (still local)

---

### **Week 3: LangChain Agent Framework**

#### Day 1-2: Setup & First Agent
**Tasks**:
- [ ] Install LangChain, OpenAI API
- [ ] Set up pgvector extension (for RAG)
- [ ] Create embeddings for company descriptions
- [ ] Build **Agent 1: Portfolio Analyzer**
  - Answers: "Which companies raised Series A in 2024?"
  - Answers: "Show me top 10 companies by funding"
  - Answers: "Compare growth rates of fintech vs healthtech"

**Deliverables**:
```python
# agents/portfolio_analyzer.py
agent = create_sql_agent(
    llm=ChatOpenAI(model="gpt-4"),
    db=postgres_db,
    agent_type="openai-tools",
    verbose=True
)

# Can chat naturally:
agent.run("Which companies in Mexico raised over $10M?")
```

**Test Cases**:
- ✓ Agent answers basic queries correctly
- ✓ Returns data in under 5 seconds
- ✓ Handles ambiguous questions

**Who Does What**:
- **Developer**: Build agent, train with sample queries
- **Team**: Test with real questions, refine prompts

---

#### Day 3-5: Second & Third Agents
**Tasks**:
- [ ] Build **Agent 2: KPI Tracker**
  - Answers: "Show me revenue trends for Company X"
  - Answers: "Which companies have negative EBITDA?"
  - Answers: "Alert me if any company's headcount drops 20%+"
  
- [ ] Build **Agent 3: Deal Flow Scorer**
  - Answers: "Rank deals by algorithm score"
  - Answers: "Why was Company X rejected?"
  - Answers: "Show me all deals in 'Active' status"

**Deliverables**:
```python
# agents/kpi_tracker.py - Financial analysis agent
# agents/dealflow_scorer.py - Investment decision agent
```

**RAG Implementation**:
- Embeddings stored in pgvector
- Agents search relevant data before answering
- Can reference company descriptions, rejection reasons

**Who Does What**:
- **Developer**: Build agents, implement RAG
- **Team**: Define business rules, test accuracy

---

### **Week 4: Streamlit Dashboard (MVP)**

#### Day 1-3: UI Development
**Tasks**:
- [ ] Build Streamlit app with 4 pages:
  1. **Home**: Overview dashboard (KPIs, charts)
  2. **Portfolio**: Chat with Portfolio Analyzer agent
  3. **Financials**: Chat with KPI Tracker agent
  4. **Deal Flow**: Chat with Deal Flow Scorer agent

- [ ] Add basic charts (revenue, funding, growth trends)
- [ ] Chat interface for each agent
- [ ] Export results to CSV/Excel

**Deliverables**:
```python
# app.py - Main Streamlit application
# pages/portfolio.py
# pages/kpis.py
# pages/dealflow.py
```

**Visual Design** (Low-Code Friendly):
```python
st.title("FactoryTest AI Agent Platform")
st.sidebar.selectbox("Choose Agent", ["Portfolio", "KPIs", "Deal Flow"])

# Chat interface
if prompt := st.chat_input("Ask a question..."):
    response = agent.run(prompt)
    st.write(response)
```

**Who Does What**:
- **Developer**: Build UI, connect agents
- **Team**: Design layout, test user experience

---

#### Day 4-5: User Testing Prep
**Tasks**:
- [ ] Write user documentation
- [ ] Create demo video
- [ ] Prepare test scenarios for team
- [ ] Set up feedback collection form

**Deliverables**:
- User guide (PDF)
- 5-minute demo video
- Test script with 20 sample questions
- Google Form for feedback

**Who Does What**:
- **Developer**: Documentation, video
- **Team**: Review materials, suggest improvements

---

### **Week 4 Milestone: Working MVP** ✅
**Demo**: 
- 3 agents answering questions
- Streamlit dashboard accessible at `localhost:8501`
- Can export results
- Runs on your laptop

---

## **PHASE 3: USER TESTING & ITERATION (Weeks 5-6)**
**Goal**: Validate with real users, refine based on feedback  
**Cost**: $0 (still local)

---

### **Week 5: Internal Testing**

#### Day 1-2: Team Onboarding
**Tasks**:
- [ ] Train 3-5 team members on the system
- [ ] Each person uses it for their real work
- [ ] Collect feedback via form
- [ ] Daily standup to discuss issues

**Test Scenarios**:
1. **Portfolio Manager**: Find investment opportunities
2. **Financial Analyst**: Track KPI trends
3. **Deal Flow Manager**: Review pipeline status

**Success Criteria**:
- ✓ 80%+ can use without help after 10 minutes
- ✓ <5 minutes to get answers to common questions
- ✓ 0 crashes or errors during testing

**Who Does What**:
- **Team**: Use system for real tasks
- **Developer**: Fix bugs, gather feedback
- **You**: Facilitate sessions, prioritize fixes

---

#### Day 3-5: Refinement Sprint
**Tasks**:
- [ ] Fix top 10 bugs reported
- [ ] Improve agent accuracy (retrain prompts)
- [ ] Add requested features (export, filters)
- [ ] Optimize slow queries
- [ ] Improve UI/UX based on feedback

**Priority Matrix**:
| Issue | Priority | Estimated Time |
|-------|----------|----------------|
| Agent gives wrong answers | 🔴 High | 2 days |
| UI is confusing | 🟡 Medium | 1 day |
| Export doesn't work | 🔴 High | 4 hours |
| Need more charts | 🟢 Low | 1 day |

**Who Does What**:
- **Developer**: Implement fixes
- **Team**: Retest after each fix
- **You**: Approve priorities

---

### **Week 6: External Beta Testing**

#### Day 1-3: Beta Deployment
**Tasks**:
- [ ] Invite 5-10 external users (LPs, portfolio companies?)
- [ ] Set up remote access (ngrok for now)
- [ ] Monitor usage patterns
- [ ] Daily check-ins with beta users

**Beta User Checklist**:
- [ ] Can access the system remotely
- [ ] Understand how to ask questions
- [ ] Provide structured feedback
- [ ] Report bugs immediately

**Who Does What**:
- **You**: Recruit beta users
- **Developer**: Enable remote access, monitor
- **Team**: Support beta users

---

#### Day 4-5: Final Refinements
**Tasks**:
- [ ] Analyze beta feedback
- [ ] Fix critical issues
- [ ] Prepare for production deployment
- [ ] Document lessons learned

**Go/No-Go Decision**:
- ✅ 80%+ users satisfied
- ✅ <5 critical bugs remaining
- ✅ Agents accurate 90%+ of time
- ✅ System stable for 48 hours

**Who Does What**:
- **You**: Make go/no-go decision
- **Developer**: Prepare production checklist
- **Team**: Final acceptance testing

---

### **Week 6 Milestone: Validated Product** ✅
**Decision Point**: 
- If successful → Proceed to AWS (Weeks 7-10)
- If needs work → Extend testing, delay AWS

---

## **PHASE 4: AWS MIGRATION (Weeks 7-8)**
**Goal**: Move from laptop to production cloud  
**Cost**: $70-132/month starts here

---

### **Week 7: AWS Infrastructure Setup**

#### Day 1-2: Account & Core Services
**Tasks**:
- [ ] Create AWS account (if needed)
- [ ] Set up billing alerts
- [ ] Create VPC and security groups
- [ ] Launch RDS PostgreSQL (db.t3.small to start)
- [ ] Create S3 buckets (raw data, backups)
- [ ] Set up IAM roles and permissions

**AWS Resources Created**:
```
- RDS PostgreSQL (db.t3.small): $30/month
- S3 Storage (100GB): $2/month
- EC2 for Airflow (t3.small): $15/month
- EC2 for API/Agents (t3.medium): $30/month
- EC2 for Streamlit (t3.small): $15/month

Total: ~$92/month
```

**Who Does What**:
- **You**: Provide AWS credentials, approve costs
- **Developer**: Set up infrastructure
- **Team**: Review architecture diagram

---

#### Day 3-5: Data Migration
**Tasks**:
- [ ] Backup local PostgreSQL
- [ ] Export schema to AWS RDS
- [ ] Migrate all data (companies, kpis, dealflow)
- [ ] Validate data integrity (row counts, checksums)
- [ ] Set up automated backups
- [ ] Configure database monitoring

**Migration Checklist**:
- ✓ All tables migrated
- ✓ Indexes recreated
- ✓ Row counts match
- ✓ Sample queries work
- ✓ Backups configured

**Who Does What**:
- **Developer**: Execute migration
- **Team**: Validate data accuracy

---

### **Week 8: Application Deployment**

#### Day 1-2: ETL & Automation
**Tasks**:
- [ ] Deploy Airflow to EC2
- [ ] Update DAGs to use AWS RDS
- [ ] Configure S3 for raw CSV storage
- [ ] Test weekly/monthly schedules
- [ ] Set up CloudWatch alerts

**Deployed Workflows**:
```
Google Drive/Dropbox → S3 → RDS PostgreSQL
↓
Airflow on EC2 (scheduler)
↓
CloudWatch (monitoring)
↓
Email alerts (SNS)
```

**Who Does What**:
- **Developer**: Deploy and configure
- **Team**: Test scheduled runs

---

#### Day 3-5: Agents & UI Deployment
**Tasks**:
- [ ] Deploy FastAPI backend to EC2
- [ ] Deploy LangChain agents
- [ ] Deploy Streamlit to EC2
- [ ] Configure domain (optional)
- [ ] Set up SSL certificate (Let's Encrypt)
- [ ] Test end-to-end system

**Deployment Architecture**:
```
Users → Load Balancer → Streamlit (Port 8501)
                      ↓
                    FastAPI (Port 8000)
                      ↓
                LangChain Agents
                      ↓
                 RDS PostgreSQL
```

**Who Does What**:
- **Developer**: Deploy applications
- **Team**: Access via public URL, test

---

### **Week 8 Milestone: Production System Live** ✅
**Validation**: 
- System accessible 24/7
- No laptop needed
- All features working
- Monitoring active

---

## **PHASE 5: PRODUCTION HARDENING (Weeks 9-10)**
**Goal**: Make it bulletproof for real users

---

### **Week 9: Security & Performance**

#### Day 1-2: Security Audit
**Tasks**:
- [ ] Enable MFA on AWS account
- [ ] Set up AWS Cognito for user authentication
- [ ] Implement role-based access control (RBAC)
- [ ] Encrypt database at rest
- [ ] Enable VPC private subnets
- [ ] Configure security groups (restrict access)
- [ ] Set up AWS WAF (firewall)

**Security Checklist**:
- ✓ No public database access
- ✓ All traffic encrypted (HTTPS)
- ✓ User authentication required
- ✓ API rate limiting enabled
- ✓ Secrets in AWS Secrets Manager

**Who Does What**:
- **Developer**: Implement security measures
- **You**: Define user roles/permissions

---

#### Day 3-5: Performance Optimization
**Tasks**:
- [ ] Add database indexes for slow queries
- [ ] Implement caching (Redis for common queries)
- [ ] Optimize agent prompts (reduce tokens)
- [ ] Load test with 10 concurrent users
- [ ] Set up auto-scaling (if needed)
- [ ] Monitor query performance

**Performance Targets**:
- Page load: <3 seconds
- Agent response: <10 seconds
- Database query: <1 second
- 99% uptime

**Who Does What**:
- **Developer**: Optimize code, run tests
- **Team**: Stress test with real usage

---

### **Week 10: Launch Preparation**

#### Day 1-2: Documentation & Training
**Tasks**:
- [ ] Write admin documentation
- [ ] Create user video tutorials
- [ ] Prepare troubleshooting guide
- [ ] Train support team (if any)
- [ ] Set up help desk system

**Documentation Deliverables**:
- User Manual (PDF)
- Admin Guide (runbook)
- FAQ page
- Video tutorials (5-10 minutes each)
- API documentation (for developers)

**Who Does What**:
- **Developer**: Technical documentation
- **Team**: User guides, videos
- **You**: Review and approve

---

#### Day 3-4: Monitoring & Alerts
**Tasks**:
- [ ] Set up Grafana dashboards
- [ ] Configure CloudWatch alarms
- [ ] Create Slack/email alerts for:
  - System downtime
  - Database errors
  - Failed ETL jobs
  - High costs
- [ ] Test alert system

**Monitoring Setup**:
```
Grafana Dashboard:
- Active users
- Query performance
- Agent usage
- Database size
- AWS costs

Alerts:
- 🔴 System down
- 🟡 Slow queries
- 🟢 Daily summary
```

**Who Does What**:
- **Developer**: Configure monitoring
- **You**: Define alert thresholds

---

#### Day 5: Production Launch 🚀
**Tasks**:
- [ ] Final go/no-go checklist
- [ ] Announce launch to users
- [ ] Monitor first 24 hours closely
- [ ] Have rollback plan ready
- [ ] Celebrate! 🎉

**Launch Checklist**:
- ✓ All tests passing
- ✓ Backups configured
- ✓ Monitoring active
- ✓ Documentation complete
- ✓ Support team ready
- ✓ Rollback plan tested

**Who Does What**:
- **You**: Make final decision, announce
- **Developer**: On-call for issues
- **Team**: Support early users

---

### **Week 10 Milestone: Production Launch** ✅
**Success**: 
- 5+ active users
- <5 support tickets
- 99%+ uptime
- Positive feedback

---

## 📋 Post-Launch (Week 11+)

### Ongoing Maintenance
**Weekly**:
- [ ] Review system metrics
- [ ] Check AWS costs
- [ ] Update agents based on user feedback

**Monthly**:
- [ ] Security updates
- [ ] Performance review
- [ ] Feature prioritization

**Quarterly**:
- [ ] Cost optimization review
- [ ] Add new agents/features
- [ ] User satisfaction survey

---

## 🛠️ Tools & Technologies Summary

### Development Tools (Installed Weeks 1-2)
```bash
# Already have:
- Python 3.9.6 ✓
- pandas 2.3.3 ✓
- Virtual environment ✓

# Will install:
- PostgreSQL 16
- Apache Airflow
- LangChain
- Streamlit
- FastAPI
- Google Drive API
- Dropbox API
```

### AWS Services (Starting Week 7)
```
- RDS (PostgreSQL)
- S3 (Storage)
- EC2 (Compute)
- CloudWatch (Monitoring)
- Cognito (Auth)
- Secrets Manager
- SNS (Notifications)
```

### AI/ML Stack
```
- LangChain (agent framework)
- OpenAI GPT-4 (LLM)
- pgvector (embeddings)
- RAG (retrieval augmented generation)
```

---

## 💰 Cost Breakdown by Phase

| Phase | Duration | Cost | Notes |
|-------|----------|------|-------|
| **Weeks 1-6** | Local testing | $0 | Runs on your laptop |
| **Week 7** | AWS setup | $0 | Free tier eligible |
| **Week 8** | First month | ~$50 | Partial month |
| **Week 9-10** | Production | $92/mo | Can optimize later |
| **Ongoing** | Monthly | $70-132/mo | Depends on usage |

**First Year Total**: ~$1,200-1,600

---

## 👥 Roles & Responsibilities

### Your Role (Product Owner)
- Make go/no-go decisions
- Approve costs and architecture
- Recruit beta testers
- Define business requirements
- Final approval on launch

### Developer Role
- Build all technical components
- Write code, deploy systems
- Fix bugs, optimize performance
- Set up infrastructure
- On-call support

### Team Role (Vibe Coders)
- Test features, provide feedback
- Create documentation and videos
- Support beta users
- Define data validation rules
- Use system for real work

---

## 🚨 Risk Mitigation

### Technical Risks
| Risk | Mitigation |
|------|------------|
| Data migration fails | Test with sample data first, have backups |
| Agents give wrong answers | Extensive testing phase, human review |
| AWS costs too high | Start small, monitor daily, set billing alerts |
| System goes down | Backups, monitoring, rollback plan |

### Business Risks
| Risk | Mitigation |
|------|------------|
| Users don't adopt it | User testing in Weeks 5-6, iterate |
| R team can't adapt | Keep CSV export working |
| Too complex to maintain | Comprehensive documentation, training |
| Budget overrun | Local testing first, incremental AWS spending |

---

## ✅ Definition of Done (Each Week)

### Week 1-2
- [ ] PostgreSQL running locally
- [ ] All CSVs loaded successfully
- [ ] ETL scripts working
- [ ] Can export back to CSV

### Week 3-4
- [ ] 3 agents answering questions
- [ ] Streamlit UI accessible
- [ ] Demo video recorded
- [ ] Team trained

### Week 5-6
- [ ] 80%+ user satisfaction
- [ ] <5 critical bugs
- [ ] Go/no-go decision made
- [ ] AWS plan approved

### Week 7-8
- [ ] AWS infrastructure live
- [ ] All data migrated
- [ ] System accessible 24/7
- [ ] Monitoring active

### Week 9-10
- [ ] Security audit passed
- [ ] Performance targets met
- [ ] Documentation complete
- [ ] Production launched 🚀

---

## 📞 Support & Escalation

### During Development (Weeks 1-6)
- Daily Slack check-ins
- Weekly demo sessions
- Ad-hoc troubleshooting

### During Migration (Weeks 7-8)
- Daily status updates
- On-call developer
- Backup plan ready

### After Launch (Week 10+)
- Support tickets via email/Slack
- Response time: <4 hours
- Monthly review meetings

---

## 🎯 Success Criteria

### Technical Success
- ✓ System uptime: >99%
- ✓ Query response: <10 seconds
- ✓ Agent accuracy: >90%
- ✓ Zero data loss

### Business Success
- ✓ 5+ daily active users by Week 10
- ✓ 80%+ user satisfaction
- ✓ <10 support tickets/week
- ✓ ROI positive within 6 months

### Team Success
- ✓ R team workflows unchanged
- ✓ No manual CSV syncing needed
- ✓ Questions answered in minutes (not hours)
- ✓ Team can maintain system without developer

---

## 📚 Next Steps (Right Now)

### Immediate Actions
1. **Review this roadmap** - Any concerns or changes?
2. **Confirm budget** - $0 for 6 weeks, then $70-132/month OK?
3. **Get API credentials** - Google Drive + Dropbox access
4. **Set expectations** - Communicate timeline to stakeholders
5. **Start Week 1** - Install PostgreSQL and begin!

---

## 🚀 Ready to Begin?

**Phase 1 starts with**:
```bash
# Install PostgreSQL
brew install postgresql@16

# Start building!
```

---

**Questions? Concerns? Ready to proceed?** Let me know and we'll start Week 1! 🎉
