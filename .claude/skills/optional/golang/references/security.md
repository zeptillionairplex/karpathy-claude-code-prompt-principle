# Security

## Core Rules

**sec-no-hardcoded-secrets** — Never put secrets in source code or config files checked into git.
```go
// BAD
const dbPassword = "supersecret123"
var apiKey = "sk-live-abc123"

// GOOD: from environment
dbPassword := os.Getenv("DB_PASSWORD")
apiKey := os.Getenv("API_KEY")
// or use a secrets manager (AWS Secrets Manager, Vault, etc.)
```

**sec-bcrypt-passwords** — Always hash passwords. Never store or compare plaintext.
```go
import "golang.org/x/crypto/bcrypt"

// Hashing (cost >= 12 for production)
hash, err := bcrypt.GenerateFromPassword([]byte(password), 12)

// Verification
err := bcrypt.CompareHashAndPassword(hash, []byte(password))
if errors.Is(err, bcrypt.ErrMismatchedHashAndPassword) {
    return ErrInvalidCredentials
}
```

**sec-sql-injection** — Parameterized queries only. Never `fmt.Sprintf` into SQL.
```go
// BAD
q := fmt.Sprintf("SELECT * FROM users WHERE email = '%s'", email)

// GOOD
row := db.QueryRowContext(ctx, "SELECT * FROM users WHERE email = $1", email)
```

**sec-tls-verify** — Never disable TLS verification in production.
```go
// BAD: disables cert verification
client := &http.Client{
    Transport: &http.Transport{
        TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
    },
}

// GOOD: use default transport or provide proper certs
client := &http.Client{Timeout: 10 * time.Second}
```

**sec-log-no-pii** — Never log passwords, tokens, full credit card numbers, or personal data.
```go
// BAD
slog.Info("login attempt", "password", req.Password, "email", req.Email)

// GOOD
slog.Info("login attempt", "email_domain", emailDomain(req.Email))
```

## Input Validation

Validate all external input at the handler layer before passing to services.
```go
type CreateOrderRequest struct {
    UserID   string  `json:"user_id" validate:"required,uuid"`
    Amount   float64 `json:"amount"  validate:"required,gt=0"`
    Currency string  `json:"currency" validate:"required,iso4217"`
}

// Use a validator library (e.g., github.com/go-playground/validator)
if err := validate.Struct(req); err != nil {
    http.Error(w, "invalid request", 400)
    return
}
```

## Authentication & Authorization

- Validate JWT/session tokens in middleware, not in each handler.
- Check authorization (ownership, role) in the service layer, not the handler.
- Use constant-time comparison for tokens to prevent timing attacks.

```go
import "crypto/subtle"

func secureEqual(a, b string) bool {
    return subtle.ConstantTimeCompare([]byte(a), []byte(b)) == 1
}
```

## Dependency Security

- Run `govulncheck ./...` in CI to detect known vulnerabilities in dependencies.
- Pin dependency versions in `go.sum`.
- Review `go mod tidy` changes in PRs.
