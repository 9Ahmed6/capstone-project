# capstone-project

# 📌 Capstone Project — Team Workflow & Git Guide

## 👥 Team Structure
This project is developed by:

Mentor: Patrick Saade

Team Members:
1. Nihal Alzubair
2. Abdulla Mohamed
3. Ahmed Mohamed  

Each task is assigned to **one primary owner** and optionally reviewed by another member.

---

# 🚀 Project Setup

## 1. Clone the Repository
Run this once when starting:

```bash
git clone https://github.com/9Ahmed6/capstone-project.git
cd capstone-project
```

---

## 2. Branch Structure

We use **two main branches**:

- `main` → Stable, final version (for demo/submission)
- `dev` → Active development branch

---

## 3. First-Time Setup (after cloning) (only one person run this once)

```bash
git checkout dev
git pull origin dev
```

---

# 🔁 Daily Workflow

## Step 1: Start a Task

```bash
git checkout dev
git pull origin dev
git checkout -b feature/<task-name>
```


---

## Step 2: Work and Save Changes

```bash
git add .
git commit -m "Clear description of what you did"
git push origin feature/<task-name>
```

---

## Step 3: Create Pull Request (PR)

1. Go to GitHub  
2. Click **“Compare & pull request”**  
3. Set:
   - Base branch → `dev`
   - Compare → your feature branch  
4. Click **Create Pull Request**

---

## Step 4: Review & Merge

- At least **one teammate reviews**
- If everything is fine → **Merge into `dev`**

---

## Step 5: Sync Your Code

After any merge, EVERYONE must run:

```bash
git checkout dev
git pull origin dev
```

---

# ⚠️ Rules

## ❌ Do NOT:
- Commit directly to `main`
- Work directly on `dev`
- Merge your own PR without review
- Push broken code

## ✅ Always:
- Create a new branch for each task
- Use clear commit messages
- Open a Pull Request for every change
- Pull latest `dev` before starting work


---

# 🔀 Handling Merge Conflicts

If Git shows a conflict:

```bash
git checkout dev
git pull origin dev
git checkout <your-branch>
git merge dev
```

1. Open conflicted files  
2. Fix manually  
3. Then:

```bash
git add .
git commit -m "Resolve merge conflict"
git push
```

---

# 📋 Task Management

We use a shared board

Each task must have:
- Clear title
- Description
- **One owner**
- Definition of Done

### Task flow:
Backlog → This Week → In Progress → Done

---

# ✅ Definition of Done

A task is complete only if:
- Code works locally
- No errors
- Matches agreed format 
- Pushed and merged into `dev`
- Can be explained to teammates

---

# 📦 Final Submission Process

When project is stable:

1. Create PR from `dev` → `main`
2. All team members review
3. Merge to `main`

---

# 💬 Communication

Use Slack for:
- Updates
- Quick questions

Optional daily update:
- What I did
- What I’m doing

---

# 🧩 Key Principle

> **No code goes into shared branches without a pull request and review**
