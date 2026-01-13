
# 🛡️ FinCorp Safe-Chat: Secure RAG with CalypsoAI Guardrails

FinCorp Safe-Chat is a production-ready GenAI interface designed for financial services. It solves the "Black Box" problem by placing a governance layer between enterprise users and Large Language Models.

The application leverages **Retrieval-Augmented Generation (RAG)** to provide accurate, policy-grounded answers while utilizing **CalypsoAI** as a high-performance security gateway to intercept PII leaks and enforce professional moderation.

---

## 🏗️ Architecture & Security Logic

The application follows a **Defense-in-Depth** strategy to ensure that no sensitive FinCorp data ever reaches a third-party model provider:

1. **Contextual Retrieval:** When an analyst enters a query, the system searches a local `ChromaDB` vector store for approved internal policy documents.
2. **Prompt Enrichment:** The system constructs a "grounded" prompt, instructing the model to answer **only** using the retrieved FinCorp context.
3. **The CalypsoAI Gateway:** Before the prompt is sent to the LLM, it is routed through the CalypsoAI API using a specific `PROJECT_ID`.
4. **Real-Time Scanning:** The gateway scans the enriched prompt for:
* **PII (Account Numbers/Credit Cards):** Set to **Block** to prevent data spills.
* **Hostile Content/Profanity:** Set to **Redact** to maintain a professional environment.


5. **Forensic Auditing:** Every interaction is logged with a timestamp and user ID in the CalypsoAI dashboard for compliance reporting.

---

## 🧪 Compliance Validation (Test Vectors)

The application features a built-in **Builder Validation** suite. This allows Security and Engineering teams to perform "Pre-Flight" checks on the security posture before deployment.

| Vector Name | Scenario | CalypsoAI Action | Business Outcome |
| --- | --- | --- | --- |
| **Benign/Safe** | General financial policy query | **Allowed** | Productivity enabled via accurate, grounded info. |
| **PII Attack** | Analyst pastes raw account numbers | **Blocked** | Data breach prevented; six-figure fine avoided. |
| **Moderation** | Frustrated/Hostile language | **Redacted** | Professionalism enforced without stopping work. |

---

## 📊 Business Value: The "Safe-Chat" Outcome

* **Eliminates Shadow AI:** By providing a safe, governed portal, FinCorp brings AI usage "into the light" where it can be monitored.
* **Reduces Liability:** Automated blocking of PII ensures compliance with PCI-DSS and GDPR.
* **Decoupled Security:** Security policies (Scanners) can be updated in the CalypsoAI UI instantly without requiring developers to change or redeploy code.
* **Audit-Ready:** Provides a "Get Out of Jail Free" card for regulators by proving that every prompt was inspected and governed.

---
