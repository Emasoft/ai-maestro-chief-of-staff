# Changelog

All notable changes to this project will be documented in this file.
    ## [2.22.0] - 2026-08-08

### Bug Fixes

- Drop defunct `Task` from 18 commands' allowed-tools + close the guard hole    
- Pin `background: false` on all 22 forked skills (Claude Code 2.1.218)    
- Stop preloading a skill from another plugin, and give the agent that needs it the Skill tool    
- Collapse the unreachable alternative in the pre-push authorization pattern    

### Documentation

- Add TRDD-4FH9JP4U — R42 drive-vs-lifecycle audit + purge plan    
- Repoint the live DECOUPLE-BLOCKED pointers from ai-maestro#36 to #76    

### Features

- Install commit-msg hook stamping the Agent governance trailer (COS#24 B2)    
- Purge R42-revoked cross-agent session-injection from recovery/lifecycle surface (TRDD-4FH9JP4U, #42)    
- Land the guide-not-a-gate refusal protocol in the COS persona (COS#28)    
- Make agent-replacement decisions kanban-context-aware (COS#11 item 3)    

### Miscellaneous

- Regenerate .githooks/pre-push from the corrected publish.py template    

### Tests

- Block an unpaired `context: fork` instead of only advising against it    
- Lower the forked-skill floor to 15 so a legitimate removal is not a failure    


