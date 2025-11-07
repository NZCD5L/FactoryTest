# AWS Self-Managed Architecture - FactoryTest Platform

## 🎯 Design Principles
- Open-source first
- AWS-native services (cost-effective)
- Multi-user data updates
- Python production logic
- LangChain for agent orchestration
- 12-week delivery timeline

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     DATA SOURCES (External)                      │
├──────────────────────────────┬──────────────────────────────────┤
│      Google Drive            │           Dropbox                 │
│  - dealflow_prueba.csv       │   - Companies.csv                 │
│  - KPIs_prueba.csv          │   - (R normalization scripts)     │
│  (Multiple editors)          │   (Multiple editors)              │
└──────────────┬───────────────┴────────────┬─────────────────────┘
               │                            │
               │    ┌──────────────────────┐│
               │    │  Python ETL Scripts  ││
               └────►  (EC2 or Lambda)     │◄┘
                    │  - Data validation   │
                    │  - Transformation    │
                    │  - Duplication     │
                    └──────────┬───────────┘
                               │
               ┌───────────────┴───────────────┐
               ▼                               ▼
    ┌─────────────────────┐       ┌──────────────────┐
    │   AWS RDS           │       │    AWS S3        │
    │   PostgreSQL        │       │  (Data Lake)     │
    │  (Source of Truth)  │       │  - Raw CSVs      │
    │                     │       │  - Backups       │
    │  Tables:            │       │  - Versions      │
    │  - companies        │       └──────────────────┘
    │  - kpis             │
    │  - dealflow         │
    └─────────┬───────────┘
              │
              │ SQL Queries
              │
    ┌─────────▼────────────────────────────────────┐
    │        LangChain Agent Layer (EC2/ECS)       │
    │  ┌──────────────────────────────────────┐   │
    │  │  Agent 1: Portfolio Analyzer          │   │
    │  │  - RAG: Company performance insights  │   │
    │  └──────────────────────────────────────┘   │
    │  ┌──────────────────────────────────────┐   │
    │  │  Agent 2: KPI Tracker                 │   │
    │  │  - RAG: Financial trends & alerts     │   │
    │  └──────────────────────────────────────┘   │
    │  ┌──────────────────────────────────────┐   │
    │  │  Agent 3: Deal Flow Scorer            │   │
    │  │  - RAG: Investment recommendations    │   │
    │  └──────────────────────────────────────┘   │
    └─────────┬────────────────────────────────────┘
              │ REST API / WebSocket
              │
    ┌─────────▼────────────────────────────────────┐
    │           Frontend Layer (EC2/S3+CloudFront) │
    │  - Streamlit Dashboard (Open Source)         │
    │  - User authentication (AWS Cognito)         │
    │  - Real-time updates                         │
    └──────────────────────────────────────────────┘
```

---

## 🗄️ Database Schema (PostgreSQL)

### Table: `companies`
```sql
CREATE TABLE companies (
    company_id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    website_url VARCHAR(500),
    city VARCHAR(100),
    founding_date DATE,
    headcount INTEGER,
    funding_total NUMERIC(15,2),
    description TEXT,
    founders TEXT,
    investors TEXT,
    last_funding_date DATE,
    last_funding_type VARCHAR(50),
    linkedin_followers INTEGER,
    web_traffic INTEGER,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_source VARCHAR(50),
    version INTEGER DEFAULT 1,
    -- Add all 23 columns from Companies.csv
    UNIQUE(company_name, founding_date)
);

CREATE INDEX idx_companies_name ON companies(company_name);
CREATE INDEX idx_companies_updated ON companies(updated_at);
```

### Table: `kpis`
```sql
CREATE TABLE kpis (
    kpi_id SERIAL PRIMARY KEY,
    fondo VARCHAR(100),
    empresa VARCHAR(255) NOT NULL,
    fecha DATE NOT NULL,
    cuarto VARCHAR(10),
    tipo VARCHAR(50),
    indicador VARCHAR(100),
    unidad VARCHAR(50),
    valor NUMERIC(20,2),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_source VARCHAR(50),
    version INTEGER DEFAULT 1,
    UNIQUE(empresa, fecha, indicador, tipo)
);

CREATE INDEX idx_kpis_empresa ON kpis(empresa);
CREATE INDEX idx_kpis_fecha ON kpis(fecha);
CREATE INDEX idx_kpis_indicador ON kpis(indicador);
```

### Table: `dealflow`
```sql
CREATE TABLE dealflow (
    deal_id SERIAL PRIMARY KEY,
    company VARCHAR(255) NOT NULL,
    status VARCHAR(50),
    stage VARCHAR(50),
    funding_round VARCHAR(50),
    deal_size_usd NUMERIC(15,2),
    valuation NUMERIC(15,2),
    industry VARCHAR(100),
    headquarters VARCHAR(100),
    year_founded INTEGER,
    contact_person VARCHAR(255),
    date_of_first_contact DATE,
    date_of_last_contact DATE,
    reason_for_rejection TEXT,
    algorithm_score NUMERIC(5,4),
    -- Add all 142 columns
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_source VARCHAR(50),
    version INTEGER DEFAULT 1,
    UNIQUE(company, funding_round, date_of_first_contact)
);

CREATE INDEX idx_dealflow_company ON dealflow(company);
CREATE INDEX idx_dealflow_status ON dealflow(status);
CREATE INDEX idx_dealflow_stage ON dealflow(stage);
```

### Metadata Table (Version Control)
```sql
CREATE TABLE data_versions (
    version_id SERIAL PRIMARY KEY,
    table_name VARCHAR(50),
    file_name VARCHAR(255),
    s3_path VARCHAR(500),
    rows_imported INTEGER,
    import_timestamp TIMESTAMP,
    imported_by VARCHAR(100),
    checksum VARCHAR(64),
    status VARCHAR(20) -- success, failed, partial
);
```

---

## 🔄 ETL Pipeline Architecture

### Weekly Update (KPIs)
```python
# Runs every Monday 9 AM
1. Check Dropbox/Drive for new KPIs_prueba.csv
2. Download to S3 (raw bucket)
3. Validate data (schema, duplicates, nulls)
4. Transform (normalize dates, currencies)
5. Upsert to PostgreSQL (update existing, insert new)
6. Archive old version to S3
7. Send notification (success/failure)
```

### Monthly Update (Companies, DealFlow)
```python
# Runs 1st of month 9 AM
1. Download Companies.csv + dealflow_prueba.csv
2. Store raw files in S3
3. Run data quality checks
4. Transform and normalize
5. Merge with existing data (conflict resolution)
6. Update PostgreSQL tables
7. Generate change report
8. Notify stakeholders
```

---

## 🛠️ Technology Stack (Open Source)

| Component | Technology | Why |
|-----------|-----------|-----|
| **Database** | PostgreSQL (AWS RDS) | Open source, powerful, scalable |
| **Storage** | AWS S3 | Cost-effective, versioning |
| **ETL** | Apache Airflow or Prefect | Open source, visual DAGs |
| **API** | FastAPI | Fast, modern, Python |
| **Agents** | LangChain + LangGraph | Flexible, RAG-ready |
| **LLM** | OpenAI API | Best performance (can switch to open models later) |
| **Vector DB** | pgvector (PostgreSQL extension) | No extra service needed |
| **Frontend** | Streamlit | Open source, Python-native |
| **Auth** | AWS Cognito | Managed, secure |
| **Scheduling** | Apache Airflow | Open source, robust |
| **Monitoring** | Grafana + Prometheus | Open source |
| **Compute** | EC2 or ECS | Self-managed |

---

## 📅 12-Week Implementation Plan

### **Weeks 1-2: Foundation** (Current)
- [x] Python + pandas setup
- [ ] AWS account setup (RDS, S3, EC2)
- [ ] PostgreSQL schema creation
- [ ] Basic ETL script (CSV → PostgreSQL)
- [ ] Data validation framework
- [ ] Airflow setup for scheduling

**Deliverable**: Data pipeline working, automated updates

---

### **Weeks 3-4: Agent Framework (MVP)**
- [ ] LangChain setup with PostgreSQL integration
- [ ] Vector embeddings for RAG (pgvector)
- [ ] Agent 1: Portfolio Analyzer (basic queries)
- [ ] Agent 2: KPI Tracker (trend analysis)
- [ ] Simple Streamlit UI
- [ ] OpenAI API integration

**Deliverable**: Working prototype with 2 agents

---

### **Weeks 5-8: User Testing & Iteration**
- [ ] Agent 3: Deal Flow Scorer
- [ ] Advanced RAG implementation
- [ ] UI/UX improvements based on feedback
- [ ] Multi-user authentication
- [ ] Performance optimization
- [ ] Error handling and logging

**Deliverable**: Feature-complete beta version

---

### **Weeks 9-10: Production Hardening**
- [ ] Security audit
- [ ] Load testing
- [ ] Documentation
- [ ] Monitoring and alerts
- [ ] Backup and disaster recovery
- [ ] User training materials

**Deliverable**: Production-ready system

---

## 💰 Estimated AWS Costs (Monthly)

| Service | Spec | Cost |
|---------|------|------|
| RDS PostgreSQL | db.t3.medium | ~$60 |
| S3 Storage | 100GB | ~$2 |
| EC2 (Airflow) | t3.small | ~$15 |
| EC2 (Agents+API) | t3.medium | ~$30 |
| EC2 (Streamlit) | t3.small | ~$15 |
| Data Transfer | 50GB/mo | ~$5 |
| CloudWatch Logs | Standard | ~$5 |
| Cognito | Up to 50 users | Free |
| **Total** | | **~$132/month** |

**Note**: Can optimize to ~$70/month using Reserved Instances

---

## 🔐 Security Considerations

1. **Database**: VPC-only, no public access
2. **API**: API Gateway with rate limiting
3. **Auth**: AWS Cognito with MFA
4. **Data**: Encryption at rest (S3, RDS)
5. **Backups**: Automated daily snapshots
6. **Secrets**: AWS Secrets Manager
7. **Network**: VPC, Security Groups, NACLs

---

## 🎯 Next Immediate Steps

1. **Set up AWS infrastructure** (RDS + S3)
2. **Create PostgreSQL schema**
3. **Build ETL script** (CSV → PostgreSQL)
4. **Test with current CSVs**
5. **Set up Airflow for scheduling**

---

## ❓ Decisions Needed From You

1. **AWS Account**: Do you have one ready, or should I guide setup?
2. **Region**: Which AWS region? (us-east-1, us-west-2, etc.)
3. **Database Size**: Start with db.t3.medium or smaller?
4. **Airflow**: Want managed (MWAA ~$300/mo) or self-hosted EC2 (cheaper)?
5. **OpenAI API**: Do you have an account/credits?
6. **Domain**: Will you need custom domain for the UI?

Let me know and I'll start building the ETL pipeline!
