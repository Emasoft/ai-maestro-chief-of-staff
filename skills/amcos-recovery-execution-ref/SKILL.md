---
name: amcos-recovery-execution-ref
description: Use when consulting detailed recovery execution references. Trigger with recovery execution lookups.
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Recovery Execution Reference

## Overview

Reference material for recovery execution. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-recovery-execution` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-recovery-execution` for error handling.

## Examples

See referenced files for step-by-step examples.

## Resources

- [recovery-operations](references/recovery-operations.md) — Topics: Recovery Operations Reference, Contents, 1. Detecting Agent Failures Using Health Checks, 1.1 Checking AI Maestro Registry, 1.2 Verifying tmux Session Existence, Verify tmux session exists, 1.3 Checking Process Health, Check if Claude Code process is running in the session, 1.4 Testing Message Response, 1.5 Checking Host Reachability for Remote Agents, If agent is on remote host, 2. Classifying Failure Severity (Transient/Recoverable/Terminal), 2.1 Failure Classification Criteria Table, 2.2 Classification Algorithm, 3. Executing Recovery Strategies Based on Failure Type, 3.1 Recovery Strategy Decision Tree, 3.2 Transient Recovery (Automatic), 3.3 Recoverable Recovery (Automatic with Notification), 3.4 Terminal Recovery (Requires Approval Unless Pre-Authorized), 4. Restarting Unresponsive Agents, 4.1 Soft Restart Procedure, Get the process PID, Send SIGTERM, Wait for restart, 4.2 Wake via Lifecycle Manager, 4.3 Full Agent Replacement, 5. Configuring Recovery Policies, 5.1 Recovery Policy File Location, 5.2 Recovery Policy Parameters, 6. Logging All Recovery Actions, 6.1 Recovery Log File Format, 6.2 Recovery Event Schema, 7. Coordinating with Other Agents During Recovery, 7.1 Sending Recovery Warnings, 7.2 Notifying Orchestrator of Orphaned Tasks, 7.3 Escalating to Manager for Approval, 7.4 Requesting Agent Replacement, 8. Monitoring Agent Health Continuously, 8.1 Continuous Health Check Loop, 8.2 On-Demand Health Check, Integration with Other Agents
- [recovery-strategies](references/recovery-strategies.md) — Topics: Recovery Strategies for Agent Failures, Table of Contents, 3.1 When to Use This Document, 3.2 Overview of Recovery Strategies, 3.3 Strategy: Wait and Retry, 3.3.1 When to Use Wait and Retry, 3.3.2 Implementation Procedure, 3.3.3 Retry Backoff Schedule, 3.3.4 Success and Failure Criteria, 3.4 Strategy: Restart Agent, 3.4.1 When to Use Restart, 3.4.2 Soft Restart Procedure, 3.4.3 Hard Restart Procedure, 3.4.4 Post-Restart Verification, 3.5 Strategy: Hibernate-Wake Cycle, 3.5.1 When to Use Hibernate-Wake, 3.5.2 Checking Agent Hibernation Status, Check for tmux session, 3.5.3 Wake Procedure, 3.5.4 Post-Wake Verification, 3.6 Strategy: Resource Adjustment, 3.6.1 When to Use Resource Adjustment, 3.6.2 Common Resource Issues and Fixes, 3.6.3 Requesting Resource Changes, 3.7 Strategy: Replace Agent, 3.7.1 When to Proceed to Replacement, 3.7.2 Pre-Replacement Checklist, 3.7.3 Initiating Replacement Protocol, 3.8 Strategy Selection Flowchart, Troubleshooting, Soft restart never receives acknowledgment, Hard restart fails because process not found, Wake succeeds but agent immediately goes back to sleep, Resource adjustment denied by manager
