# Explainability — chithra-portfolio-agent

## How the Agent Decides
The agent processes incoming queries by first classifying them into one of four domains:
profile inquiry, project question, achievement lookup, or contact routing. Based on the
domain, it invokes the relevant skill and tool to retrieve structured portfolio data.
All responses are grounded in the source portfolio files (index.html, README.md, project
repositories). No generative fabrication of credentials or outcomes is permitted.

When ambiguity exists (e.g., a question spans multiple projects), the agent surfaces all
relevant entries and asks the user to narrow down, rather than guessing intent.

## The Data It Uses
- **Portfolio source:** `index.html` — personal bio, stats (CGPA 8.96, 1390+ problems, 3 internships, 6 certs)
- **Project data:** Linked GitHub repositories (WaterQualityPrediction, CODSOFT tasks, github-profile-search)
- **Internship records:** Femtosoft Technologies (Angular), VaultofCode (Java), CODSOFT (Web)
- **Achievement records:** Rank #6 OpenCode '25, TechNova Hackathon online finalist
- **Contact data:** Public LinkedIn, GitHub, email as stated in the portfolio

No external databases, live APIs, or private records are accessed at runtime.

## Limitations
- The agent can only confirm information explicitly present in the portfolio. It cannot
  verify or update academic records, certifications, or employment status in real time.
- It does not negotiate on Chithra's behalf (salary, roles, contracts).
- It cannot answer questions outside the portfolio domain without flagging them as out-of-scope.
- Contact routing is limited to publicly stated channels; no private communication is initiated.
- The portfolio data has a snapshot date; newer projects or achievements may not be reflected
  until the portfolio is updated.

## Summary & Compliance Checklist

| Checkpoint | Status | Notes |
|---|---|---|
| Grounded responses only | ✅ PASS | All answers cite portfolio source files |
| No PII leakage | ✅ PASS | Only public contact info shared |
| GDPR compliance | ✅ PASS | Session-only data, no cross-border transfer |
| Human override capability | ✅ PASS | Kill switch and override enabled |
| Audit logging | ✅ PASS | Structured JSON logs, 90-day retention |
| Fabrication prevention | ✅ PASS | Must-never rules enforced |
| Scope acknowledgment | ✅ PASS | Out-of-scope queries explicitly flagged |
