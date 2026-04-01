---
name: installing-essential-skills
description: |
  Install and manage recommended agent skills for Claude Code projects.
  Covers workflow (Superpowers), documentation (Context7), code quality (SOLID),
  framework best practices (React, Next.js, Python), security, and utility skills.
  Use when setting up a new project, onboarding a new developer, asking
  "what skills should I install", "recommend skills", "setup project skills",
  "essential plugins", or "install baseline tools".
---

# Installing Essential Skills

Guide for installing community-vetted agent skills via the `npx skills` CLI.
All skills listed here are verified on [skills.sh](https://skills.sh/) and follow
the open Agent Skills standard.

## Prerequisites

```bash
# Verify Node.js >= 18
node -v

# No global install needed — npx runs directly
npx skills --version
```

## Quick Start — Minimum Viable Setup

Run these 5 commands to bootstrap any project:

```bash
npx skills add -g obra/superpowers
npx skills add -g BenedictKing/context7-auto-research
npx skills add -g ramziddin/solid-skills
npx skills add -g anthropics/skills --skill skill-creator
npx skills add -g vercel-labs/skills --skill find-skills
```

After install, verify:

```bash
npx skills list
```

## Skill Tiers

### Tier 1 — Universal (install globally with `-g`)

Every project benefits from these regardless of language or framework.

| Skill | Repository | What It Does | Install |
|-------|-----------|--------------|---------|
| **Superpowers** (all-in-one) | `obra/superpowers` | TDD, debugging, planning, sub-agents, code review, git worktrees, verification | `npx skills add -g obra/superpowers` |
| **Context7 Auto Research** | `BenedictKing/context7-auto-research` | Fetches latest library docs via Context7 API automatically — no MCP server needed | `npx skills add -g BenedictKing/context7-auto-research` |
| **SOLID / Clean Code** | `ramziddin/solid-skills` | Enforces SOLID principles, TDD, clean code in every implementation | `npx skills add -g ramziddin/solid-skills` |
| **Skill Creator** | `anthropics/skills` | Meta-skill: generates properly formatted SKILL.md files | `npx skills add -g anthropics/skills --skill skill-creator` |
| **Find Skills** | `vercel-labs/skills` | Search and discover skills from the skills.sh registry | `npx skills add -g vercel-labs/skills --skill find-skills` |

#### Superpowers Sub-Skills Reference

The `obra/superpowers` package installs all of these:

| Sub-Skill | Trigger |
|-----------|---------|
| test-driven-development | Writing new features, "write tests first" |
| systematic-debugging | "debug this", "find the bug", root-cause analysis |
| writing-plans | "plan this feature", architecture decisions |
| executing-plans | "execute the plan", run tasks from plan file |
| subagent-driven-development | Fresh sub-agent per task with 2-stage review |
| dispatching-parallel-agents | Independent tasks that can run concurrently |
| receiving-code-review | "review my code", PR feedback |
| requesting-code-review | Prepare code for external review |
| verification-before-completion | Final check before marking task done |
| finishing-a-development-branch | Merge prep, cleanup, final tests |
| using-git-worktrees | Isolated workspaces for parallel branches |
| writing-skills | Creating new custom skills |
| using-superpowers | Meta: how to invoke superpowers effectively |

### Tier 2 — Framework & Language Best Practices (install per project)

Pick what matches your stack:

| Skill | Repository | Stack | Install |
|-------|-----------|-------|---------|
| **React Best Practices** | `vercel-labs/agent-skills` | React 18+ | `npx skills add vercel-labs/agent-skills --skill vercel-react-best-practices` |
| **Web Design Guidelines** | `vercel-labs/agent-skills` | All front-end | `npx skills add vercel-labs/agent-skills --skill web-design-guidelines` |
| **Next.js Best Practices** | `vercel-labs/next-skills` | Next.js | `npx skills add vercel-labs/next-skills --skill next-best-practices` |
| **TypeScript TDD** | `mattpocock/skills` | TypeScript | `npx skills add mattpocock/skills --skill tdd` |
| **shadcn/ui** | `giuseppe-trisciuoglio/developer-kit` | React + shadcn | `npx skills add giuseppe-trisciuoglio/developer-kit --skill shadcn-ui` |
| **Vue Best Practices** | `hyf0/vue-skills` | Vue 3 | `npx skills add hyf0/vue-skills --skill vue-best-practices` |
| **Python Async Patterns** | `wshobson/agents` | Python | `npx skills add wshobson/agents --skill async-python-patterns` |
| **Python Project Structure** | `wshobson/agents` | Python | `npx skills add wshobson/agents --skill python-project-structure` |
| **Python Testing** | `wshobson/agents` | Python | `npx skills add wshobson/agents --skill python-testing-patterns` |
| **Neon Postgres** | `neondatabase/agent-skills` | PostgreSQL | `npx skills add neondatabase/agent-skills --skill neon-postgres` |
| **Supabase Postgres** | `supabase/agent-skills` | Supabase | `npx skills add supabase/agent-skills` |
| **Java Spring Boot** | `pluginagentmarketplace/custom-plugin-java` | Java | `npx skills add pluginagentmarketplace/custom-plugin-java --skill java-spring-boot` |

### Tier 3 — Specialized / Productivity

| Skill | Repository | Purpose | Install |
|-------|-----------|---------|---------|
| **Context7** (manual) | `intellectronica/agent-skills` | Fetch library docs on demand via curl | `npx skills add intellectronica/agent-skills --skill context7` |
| **Frontend Design** | `anthropics/skills` | High-quality UI generation (anti AI-slop) | `npx skills add anthropics/skills --skill frontend-design` |
| **Design Taste** | `leonxlnx/taste-skill` | Opinionated front-end design sense | `npx skills add leonxlnx/taste-skill` |
| **Firecrawl** | `firecrawl/cli` | Web scraping and crawling | `npx skills add firecrawl/cli --skill firecrawl` |
| **Apify Scraper** | `apify/agent-skills` | Large-scale web scraping | `npx skills add apify/agent-skills --skill apify-ultimate-scraper` |
| **Agent Browser** | `inference-sh-8/skills` | Browser automation for agents | `npx skills add inference-sh-8/skills --skill agent-browser` |
| **Playwright Dev** | `microsoft/playwright` | E2E testing with Playwright | `npx skills add microsoft/playwright --skill playwright-dev` |
| **Deep Research** | `199-biotechnologies/claude-deep-research-skill` | Multi-step research workflows | `npx skills add 199-biotechnologies/claude-deep-research-skill` |
| **PPTX** | `anthropics/skills` | Create PowerPoint presentations | `npx skills add anthropics/skills --skill pptx` |
| **DOCX** | `anthropics/skills` | Create Word documents | `npx skills add anthropics/skills --skill docx` |
| **Static Analysis** | `trailofbits/skills` | Security: CodeQL, Semgrep, SARIF | `npx skills add trailofbits/skills --skill static-analysis` |
| **Insecure Defaults** | `trailofbits/skills` | Detect hardcoded secrets, weak crypto | `npx skills add trailofbits/skills --skill insecure-defaults` |

### Tier 4 — Infrastructure & Platform

| Skill | Repository | Platform | Install |
|-------|-----------|----------|---------|
| **Wrangler** | `cloudflare/skills` | Cloudflare Workers | `npx skills add cloudflare/skills --skill wrangler` |
| **Stripe** | `stripe/ai` | Stripe Payments | `npx skills add stripe/ai --skill stripe-best-practices` |
| **Terraform** | `hashicorp/agent-skills` | Terraform IaC | `npx skills add hashicorp/agent-skills --skill terraform-style-guide` |
| **Expo App Design** | `expo/skills` | React Native / Expo | `npx skills add expo/skills --skill expo-app-design` |
| **Turborepo** | `vercel/turborepo` | Monorepo | `npx skills add vercel/turborepo --skill turborepo` |
| **Railway** | `railwayapp/railway-skills` | Railway deployment | `npx skills add railwayapp/railway-skills --skill central-station` |
| **Better Auth** | `better-auth/skills` | Authentication | `npx skills add better-auth/skills` |
| **Hono** | `yusukebe/hono-skill` | Hono framework | `npx skills add yusukebe/hono-skill --skill hono` |
| **n8n Workflows** | `czlonkowski/n8n-skills` | n8n automation | `npx skills add czlonkowski/n8n-skills --skill n8n-workflow-patterns` |

## CLI Reference

```bash
# Search for skills by keyword
npx skills find <keyword>

# List installed skills
npx skills list

# Install to project only (default)
npx skills add <owner/repo> --skill <name>

# Install globally (all projects)
npx skills add -g <owner/repo> --skill <name>

# Install for Claude Code only
npx skills add <owner/repo> --skill <name> -a claude-code

# Install ALL skills from a repo
npx skills add <owner/repo> --all

# Preview available skills without installing
npx skills add <owner/repo> --list

# Update all installed skills
npx skills update

# Remove a skill
npx skills remove <skill-name>

# Check skill health
npx skills check
```

## Global vs Project Install

| Flag | Path | When to Use |
|------|------|-------------|
| (none) | `.claude/skills/` | Framework-specific, project conventions |
| `-g` | `~/.claude/skills/` | Universal tools (Superpowers, Context7, SOLID) |

Rule of thumb: if you would use it in every project, install globally.

## Context Budget

Skills load on demand (Level 1 metadata ~100 tokens each at startup).
Keep total installed skills reasonable:

| Installed Skills | Startup Token Cost | Risk |
|:---:|:---:|------|
| < 20 | < 2K tokens | Safe |
| 20–50 | 2K–5K tokens | Monitor |
| 50+ | 5K+ tokens | Prune unused skills |

Run `npx skills check` periodically. Remove skills you haven't triggered in 30+ days.

## Why Skills Over MCP

| | MCP Server | Skill |
|---|-----------|-------|
| Context cost | Always resident (~5K–50K tokens) | On-demand (~0 until triggered) |
| Setup | `claude mcp add ...` + API keys | `npx skills add ...` |
| Portability | Claude Code only | 17+ agents (Cursor, Codex, Gemini CLI ...) |
| Maintenance | Server process must run | Static markdown files |

Community consensus (2026): prefer Skills for procedural knowledge; reserve MCP for live data streams (databases, real-time APIs) that truly need persistent connections.

## Starter Recipes

### Recipe: Full-Stack React + Node

```bash
npx skills add -g obra/superpowers
npx skills add -g BenedictKing/context7-auto-research
npx skills add -g ramziddin/solid-skills
npx skills add vercel-labs/agent-skills --skill vercel-react-best-practices
npx skills add vercel-labs/next-skills --skill next-best-practices
npx skills add giuseppe-trisciuoglio/developer-kit --skill shadcn-ui
npx skills add neondatabase/agent-skills --skill neon-postgres
```

### Recipe: Python Data Science

```bash
npx skills add -g obra/superpowers
npx skills add -g BenedictKing/context7-auto-research
npx skills add -g ramziddin/solid-skills
npx skills add wshobson/agents --skill async-python-patterns
npx skills add wshobson/agents --skill python-project-structure
npx skills add wshobson/agents --skill python-testing-patterns
```

### Recipe: Mobile (React Native / Expo)

```bash
npx skills add -g obra/superpowers
npx skills add -g BenedictKing/context7-auto-research
npx skills add vercel-labs/agent-skills --skill react-native-skills
npx skills add expo/skills --skill expo-app-design
npx skills add callstackincubator/agent-skills
```

### Recipe: Security Audit

```bash
npx skills add -g obra/superpowers
npx skills add trailofbits/skills --skill static-analysis
npx skills add trailofbits/skills --skill insecure-defaults
npx skills add trailofbits/skills --skill property-based-testing
npx skills add trailofbits/skills --skill differential-review
```

## Evolving This Skill

1. Run `npx skills find <keyword>` when you discover a repeated workflow gap.
2. If a good community skill exists, add it to the appropriate tier table above.
3. If no skill exists, create one with `/skill-creator` and add it to your project's `.claude/skills/`.
4. Review installed skills quarterly — remove unused, update outdated.
