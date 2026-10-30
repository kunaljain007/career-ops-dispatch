---
name: dossier
description: Self-hosted, AI-powered career operations and job search hub. Manage applications, tailor resumes, connect Gmail/Calendar, and track applications with Docker Compose and local/hosted LLM providers.
---

# Dossier Skill & Operations Guide

Dossier is an open-source, self-hosted, AI-powered application management system and career operations platform. It runs as a containerized stack with PostgreSQL, an automated job agent, a Chromium-based PDF rendering engine, and multi-model AI integrations.

---

## 1. Quick Start & Local Setup (Docker Compose)

### Folder & Secrets Setup (Windows PowerShell)

```powershell
# Create dossier directory
$dossierDir = "$HOME\dossier"
New-Item -ItemType Directory -Path $dossierDir -Force | Out-Null
Set-Location $dossierDir

# Download production Docker Compose file
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/AienTech/dossier/main/compose.production.yml" -OutFile "compose.yml"

# Generate secure random secrets
$bytes1 = New-Object byte[] 24; (New-Object Security.Cryptography.RNGCryptoServiceProvider).GetBytes($bytes1)
$postgresPass = ($bytes1 | ForEach-Object { "{0:x2}" -f $_ }) -join ""

$bytes2 = New-Object byte[] 32; (New-Object Security.Cryptography.RNGCryptoServiceProvider).GetBytes($bytes2)
$dossierSecret = [Convert]::ToBase64String($bytes2)

Set-Content -Path ".env" -Value "POSTGRES_PASSWORD=$postgresPass`nDOSSIER_SECRET=$dossierSecret"
```

### Password Generation (Argon2id Hash)

Generate the hashed password container without exposing plaintext passwords:

```bash
docker run --rm -it --platform linux/amd64 ghcr.io/aientech/dossier hash-password
```

Append the output line to `.env`:
```text
DOSSIER_PASSWORD=argon2id:...
```

### Launch Container

```bash
docker compose up -d
```

* **Web UI**: Open `http://localhost:3000`
* **Sign In**: Enter your chosen password.

---

## 2. AI Provider Configuration

Dossier connects to local or remote AI models under **Settings → AI Provider**:

* **OmniRoute Local Proxy** *(Recommended)*:
  * **Base URL**: `http://host.docker.internal:20128/v1`
  * **Model**: `auto/coding` or `auto/cheap`
  * Enables zero-cost local routing and 15–95% token compression.
* **Ollama (Local)**:
  * **Base URL**: `http://host.docker.internal:11434/v1`
  * **Model**: `llama3.3`, `mistral`, or `qwen2.5`
* **Claude / Anthropic**: Direct API Key in settings.
* **OpenAI / OpenRouter**: Any OpenAI-compatible endpoint.

---

## 3. Job Sources & Agent Integration

* **Job Portals Supported**: FreeHire, JSearch, Adzuna.
* **Job Agent**: Automated background polling for target roles, keywords, and salary thresholds.
* **Resume Tailoring**: Sub-second tailored PDF generation using built-in headless Chromium.
* **Google Workspace Sync**: Direct OAuth sync with Gmail and Google Calendar for interview tracking.

---

## 4. Lifecycle & Server Management

| Action | Command |
| :--- | :--- |
| **Start Services** | `docker compose up -d` |
| **Stop Services** | `docker compose stop` |
| **Restart Services** | `docker compose restart` |
| **View Live Logs** | `docker compose logs -f app` |
| **Nightly Backups** | Stored in Docker volume `dossier_data` / automated export |
| **Upgrade to Latest** | `docker compose pull && docker compose up -d` |
