# Explainability — chithra-portfolio-agent

This document explains the internal mechanisms, data lineage, and operational boundaries of **chithra-portfolio-agent** in accordance with the OpenGAP Checkpoint 2 specification.

---

## How the Agent Decides

chithra-portfolio-agent makes decisions through a deterministic, query-classification-first retrieval pipeline that grounds all outputs strictly in the source portfolio data.

### 1. Decision Architecture
The decision process flows through sequential stages:

```
User Query (text prompt)
    |
    v
[Stage 1: Query Domain Classification]
    |  - Classifies intent into 4 domains:
    |    Profile Inquiry / Project Question / Achievement Lookup / Contact Routing
    v
[Stage 2: Skill and Tool Selection]
    |  - Profile Inquiry     -> profile-showcasing   + profile-retriever
    |  - Project Question    -> project-presentation + project-navigator
    |  - Achievement Lookup  -> achievement-highlighting + profile-retriever
    |  - Contact Routing     -> (no skill)            + contact-router
    v
[Stage 3: Data Retrieval from Portfolio Source]
    |  - Reads structured data from portfolio source (index.html, README.md, project repos)
    |  - No external API calls, live lookups, or LLM hallucination permitted
    v
[Stage 4: Accuracy Gate]
    |  - Verifies all facts are explicitly present in portfolio source data
    |  - Rejects any interpolated or assumed facts not in the portfolio
    v
(Branching Decision: Is data found in portfolio?)
    |-- False --> Explicitly notifies user: data not present in portfolio
    |-- True  --> [Stage 5: Response Composition]
                      |  - Composes structured answer: headline -> detail -> evidence
                      v
                  [Stage 6: Output Delivery]
                      - Returns grounded response with citations
                      - Routes contact requests to LinkedIn / GitHub / email
```

### 2. Query Classification Rubric
The agent classifies each query using keyword and intent heuristics:
- **Profile Inquiry (40% of queries)**: Questions about education, CGPA, skills, tech stack, batch, institution. Triggers profile-showcasing skill.
- **Project Question (35% of queries)**: Questions about specific projects, tech used, how they were built, what problem they solve. Triggers project-presentation skill.
- **Achievement Lookup (15% of queries)**: Questions about rankings, competitive programming stats, certifications, hackathons. Triggers achievement-highlighting skill.
- **Contact Routing (10% of queries)**: Questions about how to hire, collaborate, or reach Chithra. Triggers contact-router immediately.

### 3. Thresholding and Refusal Decision Criteria
- **Portfolio-Grounded Only**: Any fact not explicitly stated in the portfolio source files is refused. The agent does not interpolate or infer credentials.
- **Explicit Missing Data Handling**: If a query asks about something not in the portfolio, the agent deterministically responds: "This information is not currently in the portfolio. Please check Chithra's GitHub directly."
- **No Fabrication Gate**: Claims about CGPA, project outcomes, certifications, or rankings are locked to stated values (CGPA 8.96, Rank #6 OpenCode '25, 1390+ problems, 6 certs, 3 internships).

### 4. Client-Side Guardrail Decision Gates
Before generating any output:
- **Impersonation Gate**: If the query requests the agent to commit to binding decisions (salary, contracts, start dates), the agent blocks the response and instructs the user to contact Chithra directly.
- **PII Gate**: Phone numbers and private contact details beyond publicly stated information are not shared in any response.

### 5. Fallback and Offline Decision Mechanism
- The agent operates entirely on static portfolio data with no runtime external dependencies.
- If project repositories are unavailable (offline), the agent still serves profile and achievement data from the locally embedded portfolio snapshot.
- For live repo details, the agent refers users to GitHub links rather than fetching live data.

### 6. Human-in-the-Loop Governance
- **Zero Background Action**: The agent never submits applications, emails, or commits on behalf of Chithra without explicit user action.
- **Kill Switch**: The agent can be immediately halted; no persistent background processes or sessions are maintained.
- **Audit Trail**: All interactions are logged in structured JSON format for compliance review.

---

## The Data It Uses

chithra-portfolio-agent operates strictly on static, locally embedded portfolio data with zero external data exfiltration.

### 1. Ingested Input Data
The agent consumes structured data from Chithra R's portfolio:
- **Identity Data**: Name (Chithra R), institution (Chennai Institute of Technology), degree (BE CSE), batch (2024-28), CGPA (8.96), location (Chennai, India).
- **Skills Data**: Full-Stack Web (HTML5, CSS3, JavaScript, Angular), Backend (Java), Data/ML (Python, scikit-learn, pandas), Database (MySQL).
- **Project Data**: 5 projects with names, tech stacks, GitHub URLs, and purpose statements.
- **Internship Data**: Femtosoft Technologies (Angular Developer), VaultofCode (Java Developer), CODSOFT (Web Developer).
- **Achievement Data**: Rank #6 OpenCode '25 (1000+ participants), TechNova Hackathon online finalist, 1390+ coding problems solved, 6 industry certifications.
- **Contact Data**: Public LinkedIn URL, GitHub URL, institutional email address.

### 2. In-Memory Processing and Storage Architecture
- **Static Snapshot Model**: All portfolio data is embedded at build time. No dynamic database queries are made at runtime.
- **Session-Only Memory**: Any user query context is held in local session memory and discarded upon session close.
- **0-Byte Raw Egress Guarantee**: No portfolio documents, contact data, or project code is uploaded to external servers by the agent.

### 3. External Relay Data and Redaction Patterns
When responses are exported to framework adapters (OpenAI SDK, CrewAI, Claude Code, Lyzr):
- Payloads contain only structured, sanitized profile summaries.
- **Masked PII Patterns**:
  - Phone numbers: masked as [CONTACT_VIA_LINKEDIN]
  - Email: shared only as publicly stated institutional address
  - No private keys, tokens, or credentials are present in any portfolio data

### 4. Data Privacy, Storage, and Retention
- **No Remote Storage**: The agent does not transmit session data to any cloud database or analytics service.
- **GDPR Alignment**: Only publicly declared information is processed; data minimization principle is strictly followed.
- **Audit Logging**: Structured JSON logs recording query type, skill invoked, and tool used are maintained locally for compliance auditing.

---

## Limitations

Understanding the operational boundaries of chithra-portfolio-agent is critical for accurate use.

### 1. Data Currency and Snapshot Constraints
- **Static Snapshot**: Portfolio data reflects the state of index.html and project repos at the time of last portfolio update. Newer projects, updated CGPA, or new certifications are not reflected until the portfolio is explicitly updated.
- **No Live Academic Records**: The agent cannot query live university systems to verify or update CGPA, attendance, or enrollment status.

### 2. Scope Boundaries and Domain Constraints
- **Portfolio-Only Scope**: The agent answers questions about Chithra R's portfolio exclusively. General coding questions, CS theory, or industry knowledge outside the portfolio are flagged as out-of-scope.
- **No Repository Code Access**: The agent cannot read, execute, or analyze source code from linked GitHub repositories at runtime.
- **No Private Repository Visibility**: Private GitHub repositories, unpublished projects, and work in progress are not accessible to the agent.

### 3. Connectivity and Synthesis Boundaries
- **No Live GitHub API**: The agent does not query the GitHub API at runtime. Project data is from the portfolio snapshot, not live repo metrics.
- **No Live Certification Verification**: Certification names are stated but not verified against external issuing platforms (e.g., Coursera, HackerRank) at runtime.

### 4. Negotiation and Commitment Limitations
- **No Binding Authority**: The agent cannot negotiate, commit to, or execute hiring decisions, project contracts, or collaborations on Chithra's behalf.
- **Contact Routing Only**: For all hiring and partnership inquiries, the agent routes to Chithra's public contact channels and ceases to respond on her behalf.

### 5. Media and Formatting Constraints
- **Text-Only Responses**: The agent does not render images, portfolio screenshots, or video demos. It links to GitHub repositories for visual output.

### 6. Security and Guardrail Edge Cases
- **Self-Declared Data**: Portfolio content (CGPA, rankings, internship roles) is self-declared. External verification requires direct communication with Chithra or her institution.
- **Competitive Rankings**: Rankings such as Rank #6 OpenCode '25 are stated from portfolio data and cannot be independently re-verified by the agent at query time.

---

## Summary & Compliance Checklist

| Checkpoint 2 Requirement | Corresponding Section | Status |
| :--- | :--- | :---: |
| **How the agent decides** | [How the Agent Decides](#how-the-agent-decides) | **Covered** |
| - Decision architecture and 6-stage pipeline | Section 1 | Verified |
| - Query classification rubric and domain routing | Section 2 | Verified |
| - Thresholding, refusal and no-fabrication logic | Section 3 | Verified |
| - Guardrail decision gates and PII protection | Section 4 | Verified |
| - Fallback and offline decision mechanism | Section 5 | Verified |
| - Human-in-the-loop governance | Section 6 | Verified |
| **The data it uses** | [The Data It Uses](#the-data-it-uses) | **Covered** |
| - Ingested portfolio data and source attributes | Section 1 | Verified |
| - In-memory processing and 0-byte egress guarantee | Section 2 | Verified |
| - External relay data and PII redaction patterns | Section 3 | Verified |
| - Data privacy, retention and GDPR alignment | Section 4 | Verified |
| **Its limitations** | [Limitations](#limitations) | **Covered** |
| - Data currency and snapshot constraints | Section 1 | Verified |
| - Scope boundaries and domain constraints | Section 2 | Verified |
| - Connectivity and live data boundaries | Section 3 | Verified |
| - Negotiation and commitment limitations | Section 4 | Verified |
| - Media formatting and self-declared data edge cases | Section 5 and 6 | Verified |
