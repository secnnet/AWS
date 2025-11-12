# Secure Lambda Ingest (ARM64, eu-west-1)

> **Least-privilege • No secrets in logs • Production-ready**

Securely pull credentials from **AWS Secrets Manager**, call a **target SaaS API**, and forward events to **Splunk HEC** — all with minimal IAM, no secret logging, and full comments.

---

## Overview

| Step | Action |
|------|--------|
| 1 | Store `hec_token` + `<TARGET_APP>_api_key` in **Secrets Manager** |
| 2 | IAM: allow **only** `secretsmanager:GetSecretValue` on **one** secret |
| 3 | Lambda (ARM64): fetch once → call API → POST to Splunk HEC |

**Region:** `eu-west-1` | **Arch:** `ARM64` (Graviton)

---

## Setup Checklist

### A. Secrets Manager
- **Name:** `log-ingest/<TARGET_APP>`
- **Value (JSON):**
```json
{ "hec_token": "<SPLUNK_HEC_TOKEN>", "<TARGET_APP>_api_key": "<YOUR_API_KEY>" }
