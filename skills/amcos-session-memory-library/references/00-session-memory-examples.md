# Session Memory Examples

## Table of Contents

- [Example 1: Initializing Session Memory](#example-1-initializing-session-memory) - Using `amcos_memory_manager.py init`
- [Example 2: Recovering After Interruption](#example-2-recovering-after-interruption) - Reading activeContext.md to resume work
- [Example 3: Updating Progress After Task Completion](#example-3-updating-progress-after-task-completion) - Marking tasks complete in progress.md
- [Example 4: Updating Active Context](#example-4-updating-active-context) - Switching tasks and recording the change in activeContext.md
- [Example 5: Recording a Discovered Pattern](#example-5-recording-a-discovered-pattern) - Capturing a recurring error-handling pattern into patterns.md

---

## Example 1: Initializing Session Memory

```bash
# Using the amcos_memory_manager.py init subcommand
python scripts/amcos_memory_manager.py init

# Output
Created design/memory/
Created design/memory/activeContext.md
Created design/memory/patterns.md
Created design/memory/progress.md
Session memory initialized successfully
```

## Example 2: Recovering After Interruption

```markdown
# In activeContext.md after recovery
## Current State
- **Last Active Task**: Implementing user login module
- **Current File**: src/auth/login.py:145
- **Pending Operations**: None
- **Recovery Timestamp**: 2025-01-30T10:00:00Z

# Agent reads this and resumes from line 145 of login.py
```

## Example 3: Updating Progress After Task Completion

```markdown
# In progress.md
## Tasks

- [x] Design authentication module (completed: 2025-01-29)
- [x] Implement login endpoint (completed: 2025-01-30)
- [ ] Implement logout endpoint (in progress)
- [ ] Add session management (blocked by: logout endpoint)
```

## Example 4: Updating Active Context

```markdown
# Input: Switching tasks
## Current Focus
- **Active Task:** fix-bug-123
- **Previous Task:** implement-auth (paused)
- **Timestamp:** 2026-02-03T14:30:00Z
# Output: activeContext.md updated
```

## Example 5: Recording a Discovered Pattern

```markdown
# Input: Found error handling pattern
## Pattern: Fail-Fast Error Propagation
**Category:** Error Recovery | **Discovered:** 2026-02-03
**Problem:** Silent failures causing cascading issues
**Solution:** Let errors propagate, handle at boundary layers only
# Output: Pattern added to patterns.md
```

---

**Version:** 1.1
**Last Updated:** 2026-02-15
