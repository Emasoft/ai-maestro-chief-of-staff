# Plugin Management - Overview, Examples, and Reference

## Table of Contents
- Plugin Lifecycle
- What Is Plugin Management
- Plugin Components
- Examples: Installing from Marketplace
- Examples: Local Plugin Development
- Examples: Plugin Directory Structure
- Examples: Plugin Validation
- Examples: Install Plugin on Remote Agent
- Examples: Restart Agent After Plugin Changes
- Remote Plugin Operations Table
- Key Takeaways
- Task Checklist

## Plugin Lifecycle

```
+---------------+    +---------------+    +---------------+
|   AVAILABLE   |--->|   INSTALLED   |--->|    ENABLED    |
+---------------+    +---------------+    +---------------+
       |                    |                    |
       |                    v                    v
       |             +---------------+    +---------------+
       +------------>|    CACHED     |    |   DISABLED    |
                     +---------------+    +---------------+
```

## What Is Plugin Management

Plugin management is the administration of Claude Code extensions that add commands, agents, skills, hooks, and MCP servers. It includes:

- **Installation**: Adding plugins from marketplaces or local directories
- **Configuration**: Setting plugin options and scope
- **Local management**: Working with development plugins
- **Validation**: Ensuring plugins are correctly structured

## Plugin Components

A plugin can contain any combination of:
- Slash commands (commands/)
- Agent definitions (agents/)
- Agent skills (skills/)
- Hook configurations (hooks/)
- Utility scripts (scripts/)
- MCP server configurations

## Examples: Installing from Marketplace

```bash
# Step 1: Add marketplace (first time only)
claude plugin marketplace add https://github.com/Emasoft/ai-maestro

# Step 2: Install plugin
claude plugin install perfect-skill-suggester@ai-maestro

# Step 3: Verify installation
claude plugin list | grep perfect-skill-suggester

# Step 4: RESTART Claude Code (required!)
# Exit and relaunch claude
```

## Examples: Local Plugin Development

```bash
# Launch Claude Code with local plugin
claude --plugin-dir {baseDir}/OUTPUT_SKILLS/my-plugin

# Launch with multiple local plugins
claude --plugin-dir /path/to/plugin-a --plugin-dir /path/to/plugin-b
```

## Examples: Plugin Directory Structure

```
my-plugin/
+-- .claude-plugin/
|   +-- plugin.json          # REQUIRED: plugin manifest
+-- commands/                 # Slash commands
|   +-- my-command.md
+-- agents/                   # Agent definitions
|   +-- my-agent.md
+-- skills/                   # Agent skills
|   +-- my-skill/
|       +-- SKILL.md
+-- hooks/                    # Hook configurations
|   +-- hooks.json
+-- scripts/                  # Hook and utility scripts
|   +-- my-hook.py
+-- README.md
```

## Examples: Plugin Validation

```bash
# Validate plugin structure
claude plugin validate /path/to/my-plugin

# Check hooks registration
/hooks

# Debug plugin loading
claude --debug
```

## Examples: Install Plugin on Remote Agent

Use the `ai-maestro-agents-management` skill for each step:

1. **Add marketplace** to remote agent `backend-api` with source `bundled with AI Maestro` (auto-restarts agent)
2. **Install plugin** `perfect-skill-suggester` on agent `backend-api` (auto-restarts agent)
3. **List plugins** on agent `backend-api` to verify installation
4. **Uninstall plugin** `my-old-plugin` from agent `backend-api` if no longer needed
5. **Clean plugin cache** on agent `backend-api` if installation is corrupt

**Verify**: plugin appears in the agent's plugin list after installation.

## Examples: Restart Agent After Plugin Changes

After installing on the current agent (self), a manual restart is required (exit and relaunch Claude Code).

For remote agents, restart is automatic after plugin operations. If a manual restart is needed, use the `ai-maestro-agents-management` skill to restart agent `backend-api`.

**Verify**: agent comes back online with the new plugin active.

## Remote Plugin Operations Table

All remote plugin operations are performed using the `ai-maestro-agents-management` skill. Specify the target agent and the operation:

| Operation | Description |
|-----------|-------------|
| List marketplaces | List registered marketplaces on a remote agent |
| Add marketplace | Register a marketplace on a remote agent |
| Update marketplace | Refresh marketplace cache on a remote agent |
| Remove marketplace | Unregister a marketplace from a remote agent |
| Install plugin | Install a plugin from a marketplace on a remote agent |
| Uninstall plugin | Remove a plugin from a remote agent |
| List plugins | List installed plugins on a remote agent |
| Enable plugin | Enable a disabled plugin on a remote agent |
| Disable plugin | Disable a plugin on a remote agent without uninstalling |
| Validate plugin | Validate a plugin's structure on a remote agent |
| Clean cache | Clear corrupt plugin cache on a remote agent |
| Reinstall plugin | Uninstall and reinstall a plugin on a remote agent |

**Verify**: after each operation, confirm the expected state using the list plugins operation.

## Key Takeaways

1. **Always restart after install** - Claude Code caches plugin state
2. **Use --plugin-dir for development** - Fastest local testing method
3. **Validate before publishing** - Catch errors early
4. **Components at root, not in .claude-plugin** - Common structure mistake
5. **Scripts must be executable** - chmod +x for hook scripts
6. **Remote agents auto-restart** - the `ai-maestro-agents-management` skill handles restart for remote installs
7. **Current agent needs manual restart** - Exit and relaunch claude for self-install

## Task Checklist

- [ ] Understand plugin lifecycle states
- [ ] Learn PROCEDURE 1: Install plugin from marketplace
- [ ] Learn PROCEDURE 2: Configure local plugin directory
- [ ] Learn PROCEDURE 3: Validate plugin installation
- [ ] Learn PROCEDURE 4: Manage plugins on remote agents
- [ ] Practice adding a marketplace
- [ ] Practice installing a plugin
- [ ] Practice setting up a local plugin
- [ ] Practice validating a plugin
- [ ] Practice installing plugin on remote agent
- [ ] Practice restarting agent after plugin install
