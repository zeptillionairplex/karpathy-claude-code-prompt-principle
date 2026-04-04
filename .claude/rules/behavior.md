# Behavioral Principles (Karpathy's 4 Principles)

## 1. Think Before Coding
- State assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present all of them. Don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If confused, stop. Name what's unclear and ask.

## 2. Simplicity First
- No features, abstractions, flexibility, or configurability beyond what was asked.
- No error handling for impossible scenarios.
- If 200 lines could be 50, rewrite it.
- If a senior engineer would say "this is overcomplicated," simplify.

## 3. Surgical Changes
- Only modify code directly related to the request.
- Don't "improve" adjacent code, comments, or formatting.
- Match existing style, even if you'd do it differently.
- If you find unrelated dead code, mention it — don't delete it.
- Only remove imports/variables/functions that YOUR changes made unused.

## 4. Goal-Driven Execution
- Transform tasks into verifiable goals.
- "Fix bug" → "Write a test that reproduces it, then make it pass"
- "Add feature" → "Define success criteria → write tests → make them pass"
- For multi-step tasks, state a brief plan with verification for each step.
