# Concurrency & Context

## Context Rules

**ctx-first-arg** — `context.Context` is always the first parameter of any function that does I/O.
```go
// BAD
func (s *Service) GetUser(id string) (*User, error)

// GOOD
func (s *Service) GetUser(ctx context.Context, id string) (*User, error)
```

**ctx-no-store** — Never store a context in a struct field. Pass it as an argument.
```go
// BAD
type Service struct {
    ctx context.Context  // wrong
}

// GOOD: pass ctx at call time
func (s *Service) Process(ctx context.Context) error { ... }
```

**ctx-cancel-defer** — Always defer cancel immediately after creating a derived context.
```go
// BAD: cancel never called if function returns early
ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
// ... lots of code ...
defer cancel()

// GOOD
ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
defer cancel()  // immediately after creation
```

**ctx-values-minimal** — Only put request-scoped values in context (request ID, auth user).
Never put business data, DB connections, or config in context.

## Goroutine Rules

**goroutine-exit** — Every goroutine must have a documented exit condition.
```go
// BAD: goroutine leaks if channel is never closed
go func() {
    for msg := range ch {
        process(msg)
    }
}()

// GOOD: explicit exit via context
go func() {
    for {
        select {
        case <-ctx.Done():
            return
        case msg := <-ch:
            process(msg)
        }
    }
}()
```

**goroutine-waitgroup** — Use `sync.WaitGroup` to wait for goroutines; use `errgroup` for errors.
```go
import "golang.org/x/sync/errgroup"

g, ctx := errgroup.WithContext(ctx)

g.Go(func() error {
    return fetchOrders(ctx, userID)
})
g.Go(func() error {
    return fetchProfile(ctx, userID)
})

if err := g.Wait(); err != nil {
    return fmt.Errorf("fetching user data: %w", err)
}
```

## Synchronization

**sync-mutex-scope** — Keep mutex-protected sections as short as possible.
```go
// BAD: holds lock during slow operation
func (c *Cache) Get(key string) (Value, bool) {
    c.mu.Lock()
    defer c.mu.Unlock()
    v := c.store[key]
    result := expensiveTransform(v)  // slow while holding lock
    return result, true
}

// GOOD: release lock before slow work
func (c *Cache) Get(key string) (Value, bool) {
    c.mu.RLock()
    v, ok := c.store[key]
    c.mu.RUnlock()
    if !ok {
        return Value{}, false
    }
    return expensiveTransform(v), true
}
```

**sync-no-copy** — Never copy a sync type (Mutex, WaitGroup, etc.) after first use.
Use a pointer to pass them around.

## Channels

Prefer channels for signaling; prefer mutexes for shared state.
```go
// Signaling shutdown
quit := make(chan struct{})
go worker(ctx, quit)
// ...
close(quit)  // signals all receivers

// Limiting concurrency with semaphore
sem := make(chan struct{}, maxConcurrency)
sem <- struct{}{}       // acquire
defer func() { <-sem }() // release
```
