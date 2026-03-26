---
name: amcos-memory-initialization-ref
description: Use when consulting detailed memory initialization references. Trigger with memory initialization lookups.
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Memory Initialization Reference

## Overview

Reference material for memory initialization. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-memory-initialization` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-memory-initialization` for error handling.

## Examples

See referenced files for step-by-step examples.

## Resources

- [01-initialize-session-memory](references/01-initialize-session-memory.md) — Topics: Initialize Session Memory, Table of Contents, Purpose, When to Initialize, Initialization Procedure, Step 1: Check Existing Structure, Check if memory directory exists, Check for essential files, Step 2: Create Directory Structure, Create root memory directory, Create subdirectories, Step 3: Create Initial Tracking Files, Active Context, Current Focus, Recent Decisions, Open Questions, Progress Tracker, Active Tasks, Completed Tasks, Blocked Tasks, Dependencies, Pattern Index, Recorded Patterns, Pattern Categories, Step 4: Create Session Metadata, Create session_info.md, Session Information, Environment, Status, Step 5: Add to .gitignore, Check if .gitignore exists, Add session memory to gitignore if not present, Step 6: Validate Initialization, Verify all directories exist, Verify essential files exist, Directory Structure, Initial Files, active_context.md Structure, Active Context, Current Focus, Recent Decisions, Open Questions, Context Notes, progress_tracker.md Structure, Progress Tracker, Active Tasks, Completed Tasks, Blocked Tasks, Dependencies, pattern_index.md Structure, Pattern Index, Recorded Patterns, Pattern Categories, Pattern Statistics, Verification Steps, Examples, Example 1: Clean Initialization, !/bin/bash, Initialize session memory from scratch, Remove any existing structure (if corrupted), Create structure, Create initial files, Active Context, Current Focus, Recent Decisions, Open Questions, Validate, Example 2: Initialization with Existing Data Recovery, !/bin/bash, Initialize while preserving existing data, Create fresh structure, Restore preserved data if backup exists, Example 3: Validation-First Initialization, !/bin/bash, Validate before initializing, Troubleshooting, Problem: "Permission Denied" When Creating Directories, Check current permissions, If needed, adjust permissions, Retry initialization, Problem: "Directory Already Exists" Error, Option 1: Validate existing structure, Option 2: Backup and reinitialize, Run initialization, Option 3: Clean slate (CAUTION: loses data), Run initialization, Problem: Files Created but Empty, Use single quotes to prevent premature expansion, Verify file contents, Problem: .gitignore Not Updated, Check if .gitignore exists and is writable, Add entry manually, Verify, Problem: Initialization Appears Successful but Validation Fails, List all created files, Compare against required files list, Check each file, Problem: Git Shows .session_memory/ in Status, Remove from git if tracked, Ensure .gitignore is correct, Commit .gitignore
- [00-session-memory-examples](references/00-session-memory-examples.md) — Topics: Session Memory Examples, Table of Contents, Example 1: Initializing Session Memory, Using the amcos_memory_manager.py init subcommand, Output, Example 2: Recovering After Interruption, In activeContext.md after recovery, Current State, Agent reads this and resumes from line 145 of login.py, Example 3: Updating Progress After Task Completion, In progress.md, Tasks, Example 4: Updating Active Context, Input: Switching tasks, Current Focus, Output: activeContext.md updated, Example 5: Recording a Discovered Pattern, Input: Found error handling pattern, Pattern: Fail-Fast Error Propagation, Output: Pattern added to patterns.md
