# Security & Access Control Architecture
## Multi-Tenant Platform with 300+ Users and Sensitive Data

---

## 🚨 CRITICAL REQUIREMENTS

### The Challenge
- **300+ users** accessing the platform
- **Highly sensitive** venture capital data
- **Different access levels** per user/role
- **Zero tolerance** for data leaks
- **Agents must respect** gatekeeping rules automatically

**Bottom Line**: One user should NEVER see another user's restricted data, even when asking agents directly.

---

## 🔐 Security Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    LAYER 1: AUTHENTICATION                   │
│  Who are you? (AWS Cognito + MFA)                          │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                    LAYER 2: AUTHORIZATION                    │
│  What can you do? (Role-Based Access Control)              │
│  - Fund Manager, Analyst, LP, External User, Admin         │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                LAYER 3: DATA-LEVEL SECURITY                  │
│  What can you see? (Row-Level Security in PostgreSQL)      │
│  - User can only query their permitted companies/funds     │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                LAYER 4: AGENT GATEKEEPING                    │
│  Agents check permissions BEFORE answering                  │
│  - LangChain filters + PostgreSQL RLS enforcement          │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                    LAYER 5: AUDIT LOG                        │
│  Track everything (who accessed what, when)                 │
│  - Immutable logs for compliance                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 👥 User Roles & Permissions

### Proposed Role Structure

| Role | Access Level | Can See | Can Do |
|------|-------------|---------|--------|
| **Admin** | Full | Everything | Manage users, view all data |
| **Fund Manager** | Fund-wide | All companies in their fund(s) | View, analyze, export |
| **Analyst** | Limited | Assigned companies only | View, analyze (no export) |
| **LP (Investor)** | Portfolio-only | Their invested companies | View financials, reports |
| **External User** | Restricted | Specific companies they're involved with | View only, no exports |
| **Auditor** | Read-only | Everything (time-limited) | View, audit, no modifications |

### Permission Matrix

| Action | Admin | Fund Manager | Analyst | LP | External |
|--------|-------|--------------|---------|-------|----------|
| View all companies | ✅ | ❌ | ❌ | ❌ | ❌ |
| View fund companies | ✅ | ✅ (own fund) | ❌ | ❌ | ❌ |
| View assigned companies | ✅ | ✅ | ✅ | ✅ | ✅ |
| View financials (KPIs) | ✅ | ✅ | ✅ | ✅ (own investments) | ❌ |
| View deal flow | ✅ | ✅ | ✅ (assigned) | ❌ | ❌ |
| Export data | ✅ | ✅ | ❌ | ❌ | ❌ |
| Modify data | ✅ | ❌ | ❌ | ❌ | ❌ |
| Add users | ✅ | ❌ | ❌ | ❌ | ❌ |
| View audit logs | ✅ | ✅ (own actions) | ❌ | ❌ | ❌ |

---

## 🗄️ Database Security Implementation

### Row-Level Security (RLS) in PostgreSQL

**What is RLS?**: Database automatically filters data based on who's asking.

#### Table: `companies`
```sql
-- Enable RLS
ALTER TABLE companies ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see companies they have access to
CREATE POLICY company_access_policy ON companies
FOR SELECT
USING (
    company_id IN (
        SELECT company_id 
        FROM user_company_access 
        WHERE user_id = current_setting('app.current_user_id')::uuid
    )
    OR 
    current_setting('app.user_role') = 'admin'
);

-- Similar policies for kpis and dealflow tables
```

#### Access Control Tables
```sql
-- User permissions table
CREATE TABLE user_permissions (
    user_id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(50) NOT NULL, -- admin, fund_manager, analyst, lp, external
    fund_ids UUID[], -- Which funds can they access
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Company-level access (granular control)
CREATE TABLE user_company_access (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES user_permissions(user_id),
    company_id INTEGER REFERENCES companies(company_id),
    access_level VARCHAR(50), -- full, financials_only, basic_info
    granted_by UUID REFERENCES user_permissions(user_id),
    granted_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP, -- Optional: time-limited access
    UNIQUE(user_id, company_id)
);

-- Fund-level access
CREATE TABLE user_fund_access (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES user_permissions(user_id),
    fund_name VARCHAR(100),
    granted_at TIMESTAMP DEFAULT NOW()
);

-- Audit log (immutable)
CREATE TABLE access_audit_log (
    id SERIAL PRIMARY KEY,
    user_id UUID,
    user_email VARCHAR(255),
    action VARCHAR(100), -- view_company, export_data, query_agent
    resource_type VARCHAR(50), -- company, kpi, dealflow
    resource_id INTEGER,
    query_text TEXT, -- What question they asked the agent
    timestamp TIMESTAMP DEFAULT NOW(),
    ip_address INET,
    user_agent TEXT,
    success BOOLEAN
);
```

---

## 🤖 Agent-Level Security

### LangChain with Security Filters

#### Before Agent Responds
```python
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase

class SecureAgent:
    def __init__(self, user_id, user_role):
        self.user_id = user_id
        self.user_role = user_role
        
        # Set PostgreSQL session variables (enforces RLS)
        self.db = SQLDatabase.from_uri(
            f"postgresql://...",
            engine_args={
                "connect_args": {
                    "options": f"-c app.current_user_id={user_id} -c app.user_role={user_role}"
                }
            }
        )
        
        self.agent = create_sql_agent(
            llm=ChatOpenAI(model="gpt-4"),
            db=self.db,
            agent_type="openai-tools",
            prefix=self._get_security_prefix()
        )
    
    def _get_security_prefix(self):
        """Add security instructions to agent prompt"""
        return f"""
        You are a secure AI assistant with access to sensitive venture capital data.
        
        SECURITY RULES:
        1. You can ONLY access data the current user is permitted to see
        2. NEVER mention companies or data outside user's permissions
        3. If asked about restricted data, respond: "You don't have access to that information"
        4. NEVER try to bypass Row-Level Security
        5. Log all queries to audit trail
        
        User Role: {self.user_role}
        User ID: {self.user_id}
        
        The database will automatically filter results based on permissions.
        """
    
    def query(self, user_question):
        """Process user query with security"""
        
        # Log the attempt
        log_query_attempt(self.user_id, user_question)
        
        try:
            # Agent will only see permitted data due to RLS
            response = self.agent.run(user_question)
            
            # Log success
            log_query_success(self.user_id, user_question, response)
            
            return response
            
        except Exception as e:
            # Log failure
            log_query_failure(self.user_id, user_question, str(e))
            
            return "I couldn't process that request. Please contact support."
```

#### Example Scenarios

**Scenario 1: Analyst asks about restricted company**
```python
user = Analyst(id="analyst_123", assigned_companies=["CompanyA", "CompanyB"])

user.ask_agent("Show me financials for CompanyC")

# Agent response:
"You don't have access to that information. You can only view companies: CompanyA, CompanyB"
```

**Scenario 2: LP asks about their portfolio**
```python
user = LP(id="lp_456", investments=["CompanyX", "CompanyY"])

user.ask_agent("What's the revenue growth for my portfolio?")

# Agent sees only CompanyX and CompanyY data
# Response: "Your portfolio (CompanyX, CompanyY) has 45% average revenue growth..."
```

**Scenario 3: Unauthorized export attempt**
```python
user = ExternalUser(id="ext_789", role="external")

user.ask_agent("Export all company data to CSV")

# Agent response:
"You don't have permission to export data. Please contact an administrator."

# + Audit log: BLOCKED EXPORT ATTEMPT by ext_789
```

---

## 🛡️ Additional Security Measures

### 1. Query Filtering (Double-Check Layer)
```python
def sanitize_agent_response(user_id, response):
    """
    Even if agent leaks data somehow, filter the response
    """
    user_permitted_companies = get_user_companies(user_id)
    
    # Remove mentions of non-permitted companies
    for company in ALL_COMPANIES:
        if company not in user_permitted_companies:
            response = response.replace(company, "[REDACTED]")
    
    return response
```

### 2. Rate Limiting (Prevent Data Scraping)
```python
# Max 100 queries per user per hour
RATE_LIMIT = {
    'admin': 1000,
    'fund_manager': 500,
    'analyst': 100,
    'lp': 50,
    'external': 20
}
```

### 3. Data Masking (Partial Info)
```python
# LPs see company performance but not full financials
if user_role == 'lp':
    df['revenue'] = df['revenue'].apply(lambda x: f"${round(x/1000000)}M")  # Rounded
    df['ebitda'] = "[Not available at your access level]"
```

### 4. Time-Based Access (Temporary Permissions)
```sql
-- Access expires after 30 days
INSERT INTO user_company_access (user_id, company_id, expires_at)
VALUES ('ext_123', 42, NOW() + INTERVAL '30 days');

-- Automatic cleanup
DELETE FROM user_company_access WHERE expires_at < NOW();
```

---

## 🧪 Security Testing Protocol

### Phase 1: Unit Tests (Week 3)
```python
def test_analyst_cannot_see_other_fund():
    analyst = create_test_user(role='analyst', fund='Fund A')
    
    response = analyst.query("Show me companies in Fund B")
    
    assert "You don't have access" in response
    assert no_fund_b_data_in_response(response)

def test_lp_cannot_export():
    lp = create_test_user(role='lp')
    
    response = lp.query("Export all data")
    
    assert "don't have permission" in response.lower()
    assert audit_log_shows_blocked_attempt(lp.id)

def test_rls_enforcement():
    user_a = create_test_user(companies=['CompanyA'])
    user_b = create_test_user(companies=['CompanyB'])
    
    # User A should not see Company B in SQL results
    results = user_a.db.query("SELECT * FROM companies")
    
    assert 'CompanyA' in results
    assert 'CompanyB' not in results
```

### Phase 2: Integration Tests (Week 4)
```python
# Simulate real user scenarios
def test_cross_user_data_leak():
    """Ensure one user can't access another's data through any means"""
    
    users = create_300_test_users()
    
    for user in users:
        # Try to access every other user's data
        for other_user in users:
            if user.id != other_user.id:
                response = user.query(f"Show data for {other_user.companies[0]}")
                assert_no_unauthorized_data(response, other_user.companies)
```

### Phase 3: Penetration Testing (Week 4)
```python
# Try to bypass security
test_sql_injection()
test_prompt_injection()  # "Ignore previous instructions..."
test_rate_limit_bypass()
test_session_hijacking()
test_privilege_escalation()
```

### Phase 4: External Security Audit (Week 4)
- Hire external security firm (OWASP, HackerOne)
- Penetration testing by professionals
- Compliance review (GDPR, SOC 2 if needed)
- Cost: $5,000-15,000 (one-time)

---

## 📊 Access Control Dashboard (Admin View)

### Real-Time Monitoring
```
┌─────────────────────────────────────────────────────────────┐
│                    ADMIN SECURITY DASHBOARD                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Active Users: 287 / 300                                    │
│  Blocked Attempts Today: 12                                 │
│  Average Response Time: 2.3s                                │
│                                                              │
│  🔴 ALERTS (Last 24h)                                       │
│  - User "john@example.com" tried to export restricted data  │
│  - User "jane@example.com" exceeded rate limit (120 queries)│
│  - Suspicious query pattern detected for user "bob@..."     │
│                                                              │
│  📊 USAGE BY ROLE                                           │
│  Fund Managers: 45 users, 2,340 queries                    │
│  Analysts: 180 users, 5,890 queries                        │
│  LPs: 50 users, 234 queries                                │
│  External: 12 users, 45 queries                            │
│                                                              │
│  🔍 TOP QUERIED COMPANIES (This Week)                       │
│  1. CompanyX - 456 queries                                  │
│  2. CompanyY - 342 queries                                  │
│  3. CompanyZ - 289 queries                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Implementation Priority (Weeks 1-4)

### Week 1: Foundation
- [x] PostgreSQL with RLS enabled
- [ ] User permission tables created
- [ ] Basic authentication (AWS Cognito)
- [ ] Admin can add/remove users

### Week 2: Access Control
- [ ] Role-based access working
- [ ] Company-level permissions assignable
- [ ] Test with 10 users, different roles
- [ ] Audit logging functional

### Week 3: Agent Security
- [ ] LangChain respects RLS
- [ ] Security prompts in agents
- [ ] Query filtering and sanitization
- [ ] 100+ automated security tests pass

### Week 4: Hardening & Audit
- [ ] External security audit completed
- [ ] Penetration tests passed
- [ ] Rate limiting active
- [ ] Admin dashboard live
- [ ] 300-user load test successful

---

## ✅ Security Validation Checklist (Before Production Week 5)

### Pre-Launch Gates (All must pass)

- [ ] **RLS Enforcement**: 1000 test queries, 0 unauthorized data leaks
- [ ] **Role Testing**: All 5 roles tested, permissions work correctly
- [ ] **Agent Security**: 500 adversarial queries, all blocked appropriately
- [ ] **Audit Log**: Every query logged, immutable, searchable
- [ ] **Rate Limiting**: Confirmed working for all roles
- [ ] **External Audit**: Security firm gives green light
- [ ] **Load Test**: 300 concurrent users, no performance degradation
- [ ] **Incident Response**: Tested alert system, team knows procedures
- [ ] **Data Backup**: Tested restore from backup, <1 hour RTO
- [ ] **Legal Review**: Terms of service, privacy policy approved

### Launch Day Monitoring (Week 5)
- 24/7 monitoring for first 72 hours
- Security team on standby
- Immediate rollback plan ready
- Daily security reports to stakeholders

---

## 🚨 Incident Response Plan

### If Security Breach Detected

**Minute 0-5**: Detect and alert
- Automated alerts fire
- Security team paged

**Minute 5-15**: Assess and contain
- Identify affected users
- Lock down accounts if needed
- Disable affected features

**Minute 15-60**: Remediate
- Fix vulnerability
- Deploy patch
- Verify fix works

**Hour 1-24**: Notify and document
- Inform affected users
- Document incident
- Post-mortem meeting

**Day 1-7**: Improve
- Implement additional safeguards
- Update security protocols
- Third-party re-audit

---

## 💰 Security Budget

| Item | Cost | When |
|------|------|------|
| **External Security Audit** | $10,000 | Week 4 |
| **Penetration Testing** | $5,000 | Week 4 |
| **AWS WAF (Firewall)** | $10/month | Week 5+ |
| **CloudTrail (Audit Logs)** | $5/month | Week 5+ |
| **Security Monitoring Tools** | $50/month | Week 5+ |
| **Compliance (SOC 2 if needed)** | $15,000/year | Year 1 |
| **Total First 10 Weeks** | ~$15,000 | One-time |
| **Ongoing Monthly** | ~$65/month | After launch |

---

## 🎓 User Training Materials

### For Admins
- How to add/remove users
- How to assign permissions
- How to monitor audit logs
- How to respond to alerts

### For Users
- What you can/can't access (based on role)
- How to request additional access
- Data handling best practices
- What to do if you see unauthorized data

---

## ❓ FAQ: Security Concerns

**Q: Can an agent accidentally reveal restricted data?**  
A: No. PostgreSQL RLS blocks queries at database level. Even if agent tries, database returns empty results.

**Q: What if a user shares their login?**  
A: We log IP addresses and user agents. Anomalies trigger alerts. MFA prevents most account sharing.

**Q: Can a user download all data and leak it?**  
A: Export permissions are role-based. Even if they export, they only get their permitted data. All exports logged.

**Q: What about deleted data?**  
A: Soft deletes (data marked as deleted but not removed). Audit trail preserved forever.

**Q: How do we revoke access quickly?**  
A: Admin dashboard allows instant user deactivation. Takes effect within 60 seconds.

---

## 🔄 Continuous Security

### Monthly
- Review audit logs for anomalies
- Update security patches
- Test backup restores

### Quarterly
- Penetration testing
- Security training for team
- Review and update permissions

### Annually
- Full security audit
- Compliance certification renewal
- Incident response drill

---

**Ready to proceed with the revised timeline?** This security architecture will be built in parallel with the accelerated 5-week production timeline.
