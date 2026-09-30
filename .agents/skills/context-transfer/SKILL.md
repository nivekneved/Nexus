---
name: context-transfer
description: Generates a Context Transfer Handover to seamlessly resume a session in a new window by serializing all critical state into a single markdown code block.
---

Generate a "Context Transfer Handover" to seamlessly resume this session in a new window.
Your sole job is to serialize all critical state into a SINGLE markdown code block. 
Do NOT include any introductory or concluding text outside the block.

The block must follow this exact template:

```markdown
# SESSION HANDOVER CONTEXT

## 1. Primary Goal & Tech Context
- **Goal / Problem Statement**: [What we are building or solving]
- **Environment & Stack**: [OS, Framework, Models, key versions]

## 2. Key Decisions & Rationale
- **Chosen Architectures / Solutions**: [What we decided and why]
- **Rejected Paths / Dead Ends**: [What failed or what NOT to try again]

## 3. Progress Tracker
- [x] **Completed**: [Done items]
- [/] **In Progress**: [Exact active task right now]
- [ ] **Not Started**: [Upcoming queued tasks]

## 4. Referenced Files, Assets & Exact Locations
- [Exact file paths, key functions, endpoints, figures, and important identifiers]

## 5. Immediate Next Steps & Continuation Directive
- **Where We Left Off**: [The exact line, error, or state we stopped at]
- **Immediate Action**: [Concrete task for the receiving assistant to execute next]
```