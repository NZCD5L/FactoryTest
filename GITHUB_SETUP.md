# GitHub Repository Setup Guide

**Your API Key is Safe!** ✅  
It's stored in `.env` file which is gitignored and will NOT be pushed to GitHub.

---

## 📋 Step-by-Step Instructions

### Step 1: Create GitHub Repository

1. **Go to GitHub** → https://github.com/new

2. **Fill in repository details:**
   - **Repository name**: `factorytest` (or your preferred name)
   - **Description**: "AI-powered portfolio analytics platform with LangChain and PostgreSQL"
   - **Visibility**: ⚠️ **PRIVATE** (recommended - contains sensitive business logic)
   - **Initialize**: 
     - ❌ Do NOT add README (you already have one)
     - ❌ Do NOT add .gitignore (you already have one)
     - ❌ Do NOT add license

3. **Click "Create repository"**

---

### Step 2: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
# Add GitHub as remote
git remote add origin https://github.com/YOUR_USERNAME/factorytest.git

# Verify remote was added
git remote -v

# Push your code
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

---

### Step 3: Verify Everything Worked

1. **Refresh your GitHub repository page**
2. **You should see:**
   - ✅ All your Python files
   - ✅ All documentation (.md files)
   - ✅ requirements.txt
   - ✅ .gitignore
   - ✅ .env.example (template)
   
3. **You should NOT see:**
   - ❌ .env (your API key)
   - ❌ CSV files (data)
   - ❌ venv/ folder
   - ❌ Any .log files

---

## 🔐 Security Verification

### After Pushing, Check These:

1. **API Key NOT visible**
   ```bash
   # Search for your API key on GitHub
   # Go to: https://github.com/YOUR_USERNAME/factorytest
   # Press Ctrl+F (or Cmd+F on Mac)
   # Search for: sk-proj-
   # Result should be: NOT FOUND ✅
   ```

2. **CSV files NOT visible**
   - Companies.csv → Should NOT be in repo
   - KPIs_prueba.csv → Should NOT be in repo
   - dealflow_prueba.csv → Should NOT be in repo

3. **.env file NOT visible**
   - .env → Should NOT be in repo
   - .env.example → SHOULD be in repo ✅

---

## 🎯 What IS in Your GitHub Repository

```
factorytest/                      ← Your repo
├── .env.example                 ✅ Template (no real secrets)
├── .gitignore                   ✅ Ignore rules
├── README_PROJECT.md            ✅ Project documentation
├── requirements.txt             ✅ Dependencies
│
├── 📝 Documentation/
│   ├── FINAL_PDR_12WEEKS.md
│   ├── SECURITY_ARCHITECTURE.md
│   ├── INTEGRATION_TEST_RESULTS.md
│   ├── ADVANCED_TEST_RESULTS.md
│   ├── SESSION_SUMMARY.md
│   └── ... (other docs)
│
├── 🐍 Python Scripts/
│   ├── test_integration.py
│   ├── quick_demo.py
│   ├── advanced_test.py
│   └── test_setup.py
│
└── GITHUB_SETUP.md              ← This guide
```

---

## 🚫 What is NOT in Your GitHub Repository

```
❌ .env                          ← Your API key (SAFE!)
❌ venv/                         ← Virtual environment
❌ *.csv                         ← Sensitive data files
❌ *.log                         ← Log files
❌ __pycache__/                  ← Python cache
❌ .DS_Store                     ← macOS files
```

---

## 🔄 Daily Git Workflow (After Setup)

### Making Changes

```bash
# 1. Check what changed
git status

# 2. See detailed changes
git diff

# 3. Add files you want to commit
git add .

# 4. Commit with descriptive message
git commit -m "feat: add investor gatekeeping middleware"

# 5. Push to GitHub
git push
```

### Common Git Commands

```bash
# See commit history
git log --oneline

# Undo uncommitted changes
git checkout -- filename.py

# Create a new branch
git checkout -b feature/new-feature

# Switch branches
git checkout main

# Pull latest changes (when working with team)
git pull
```

---

## 👥 Team Collaboration (Week 5+)

### For Team Members Joining:

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/factorytest.git
cd factorytest

# Set up environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Ask team lead for OPENAI_API_KEY and add it to .env

# Get CSV data files (NOT in Git)
# Download from shared Google Drive or Dropbox

# Set up PostgreSQL
createdb factorytest_local
python test_integration.py  # This loads the data

# Test everything works
python quick_demo.py
```

---

## ⚠️ Important Reminders

### DO:
- ✅ Commit code changes regularly
- ✅ Write descriptive commit messages
- ✅ Pull before pushing (when working with team)
- ✅ Keep .env updated locally (but never commit it)

### DON'T:
- ❌ Commit .env file
- ❌ Commit CSV data files
- ❌ Commit API keys or passwords
- ❌ Force push (`git push -f`) unless you know what you're doing
- ❌ Commit large files (>100MB)

---

## 🆘 If You Accidentally Commit Secrets

**If you accidentally commit your API key:**

1. **Immediately revoke the key** at https://platform.openai.com/api-keys
2. **Generate a new key**
3. **Remove from Git history:**
   ```bash
   # This is complex - ask for help!
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch file-with-secret.py" \
     --prune-empty --tag-name-filter cat -- --all
   
   git push origin --force --all
   ```
4. **Update .env with new key**

---

## 📊 Repository Status Check

After setup, verify:

```bash
# Check remote connection
git remote -v
# Should show: origin  https://github.com/YOUR_USERNAME/factorytest.git

# Check current branch
git branch
# Should show: * main

# Check if everything is committed
git status
# Should show: "nothing to commit, working tree clean"
```

---

## 🎉 Success Checklist

- [ ] GitHub repository created (PRIVATE)
- [ ] Local repo connected to GitHub
- [ ] Initial commit pushed successfully
- [ ] Can see all files on GitHub
- [ ] .env file NOT visible on GitHub ✅
- [ ] CSV files NOT visible on GitHub ✅
- [ ] API key still works locally
- [ ] README displays properly on GitHub

---

## 📞 Next Steps

After GitHub is set up:

1. **Bookmark your repository** for easy access
2. **Add repository URL to .env** (optional):
   ```bash
   GITHUB_REPO=https://github.com/YOUR_USERNAME/factorytest
   ```
3. **Share repository with team** (when ready, Week 5)
4. **Continue with Week 2** tasks (automation + Google Drive)

---

## 🔗 Useful Links

- **Your Repository**: https://github.com/YOUR_USERNAME/factorytest
- **GitHub Docs**: https://docs.github.com/en/get-started
- **Git Cheat Sheet**: https://education.github.com/git-cheat-sheet-education.pdf
- **OpenAI API Keys**: https://platform.openai.com/api-keys

---

**Created**: November 6, 2025  
**Your API Key Location**: `/Users/dannazca/FactoryTest/.env` (LOCAL ONLY - SAFE!)  
**Status**: Ready to push to GitHub! 🚀
