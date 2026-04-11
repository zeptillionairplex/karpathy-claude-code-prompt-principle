---
globs: "**/middleware/**, **/auth/**, **/permission/**, **/policy/**"
---
# Authorization

## Model Selection

Choose based on what drives access decisions:

| Question | Model | Use when |
|---|---|---|
| "What role does this user have?" | **RBAC** | CMS, admin panels, SaaS tiers — roles are stable and ≤ 10 |
| "Do user/resource/environment attributes satisfy a policy?" | **ABAC** | Finance, healthcare, content platforms — dynamic conditions (time, location, device) |
| "Does a relationship exist between this user and this resource?" | **ReBAC** | Docs, file sharing, project tools — ownership and hierarchy matter |
| Multiple conditions apply | **Hybrid** | Start RBAC, layer ReBAC for ownership, ABAC for dynamic gates |

**Default: start with RBAC.** It covers 80% of requirements, is easiest to implement, and AI generates it most reliably. Upgrade only when role explosion becomes real.

---

## RBAC

**Structure:** User → Role → Permission

```
User ──[N:M]──► Role ──[N:M]──► Permission
```

**Permission naming:** `resource:action`

```
post:create  post:read  post:update  post:delete
user:read    file:upload  file:delete
```

**Schema (PostgreSQL):**

```sql
CREATE TABLE permissions (
    id       SERIAL PRIMARY KEY,
    resource VARCHAR(50) NOT NULL,
    action   VARCHAR(50) NOT NULL,
    UNIQUE(resource, action)
);

CREATE TABLE roles (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL   -- 'admin', 'editor', 'author', 'viewer'
);

CREATE TABLE role_permissions (
    role_id       INT REFERENCES roles(id),
    permission_id INT REFERENCES permissions(id),
    PRIMARY KEY (role_id, permission_id)
);

CREATE TABLE user_roles (
    user_id INT REFERENCES users(id),
    role_id INT REFERENCES roles(id),
    PRIMARY KEY (user_id, role_id)
);
```

**Middleware pattern (Go):**

```go
func RequirePermission(resource, action string) gin.HandlerFunc {
    return func(c *gin.Context) {
        userID := c.GetInt("user_id")
        if !hasPermission(userID, resource+":"+action) {
            c.AbortWithStatusJSON(403, gin.H{"error": "forbidden"})
            return
        }
        c.Next()
    }
}
```

**Watch for role explosion.** If you need "Seoul branch + marketing team + night shift" as one role, RBAC is the wrong model.

---

## ReBAC

**Structure:** Graph of relationships between subjects and resources.

```
User:Alice ──[owner]──► Document:spec
User:Alice ──[member]──► Team:eng ──[parent]──► Folder:eng-docs
```

Alice can access all docs under `eng-docs` through graph traversal — no explicit grant needed.

**Use for:** Google Drive-style sharing, GitHub org→team→repo hierarchy, Notion pages.

**Prompt pattern:**
```
Design a ReBAC system for document sharing.
User → Team → Folder → Document hierarchy.
Folder permissions must inherit to child documents.
Reference OpenFGA tuple model.
```

**Open source:** OpenFGA (Auth0), SpiceDB (Authzed), Ory Keto.

---

## ABAC

**Structure:** Policy evaluated against four attribute types.

```
Subject    → department: finance, clearance: 2
Resource   → classification: confidential, created: 2025-01-01
Action     → read, write, delete
Environment → time: 09:00–18:00, ip: 10.0.0.0/8, location: KR
```

**Use for:** AWS IAM-style policies, medical record access, geo-restricted content.

**Prompt pattern:**
```
ABAC policy: allow read only when
  user.department == 'finance'
  AND document.classification == 'confidential'
  AND env.time BETWEEN '09:00' AND '18:00'
  AND env.ip IN '10.0.0.0/8'
Write as OPA Rego policy.
```

**Open source:** OPA (Open Policy Agent), Cedar (AWS).

**Warning:** Hard to debug. If "why was access denied?" takes more than 30 seconds to answer, the policy is too complex.

---

## Hybrid Pattern

RBAC for coarse-grained roles + ReBAC for ownership is the most common real-world combination:

```go
// Admin bypasses ownership check; non-admin must own the resource
func RequireOwnerOrPermission(resource, action string) gin.HandlerFunc {
    return func(c *gin.Context) {
        userID := c.GetInt("user_id")
        resourceID := c.Param("id")

        if hasPermission(userID, resource+":"+action) {  // RBAC: role check
            c.Next()
            return
        }
        if isOwner(userID, resource, resourceID) {        // ReBAC: ownership check
            c.Next()
            return
        }
        c.AbortWithStatusJSON(403, gin.H{"error": "forbidden"})
    }
}
```

---

## Decision Flowchart

```
Need access control?
│
├─ Roles are clear and ≤ 10?               → RBAC
├─ Dynamic conditions (time/location/IP)?  → ABAC
├─ Ownership or hierarchy drives access?   → ReBAC
└─ Multiple of the above?                  → RBAC + ReBAC (ownership)
                                              add ABAC gates only where needed
```

---

## Prompting AI for Authorization

Always name the model explicitly — it dramatically improves output quality:

```
# RBAC
Implement RBAC. Roles: Admin, Editor, Author, Viewer.
Permissions as "resource:action" (e.g., post:create).
JWT-based auth, PostgreSQL, Go Gin middleware.

# ReBAC
Implement ReBAC for file sharing.
User → Team → Folder → File hierarchy.
Use OpenFGA tuple model. Permissions inherit downward.

# ABAC
Write an OPA Rego policy: allow read when
  user.department == 'hr' AND resource.sensitivity != 'public'
  AND env.business_hours == true.
```
