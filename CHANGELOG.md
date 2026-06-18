# Changelog

All notable changes to this project will be documented in this file.
    ## [2.18.2] - 2026-06-18

### Bug Fixes

- Amcos_notify_agent resolve parse → tmuxSessionName (was session_name); drop dead list branch    

### Documentation

- #20 scope extended to hooks (USER rule) — COS hooks already compliant    
- #20 transfer verb BUILT (d946e0dc) — gap closed, all COS pass-2 CLIs now in source    
- #20 PIVOT to do-now commit-not-publish + verified CLI verbs (resume checkpoint)    
- TRDD STATE — pass-2 mechanical complete (25 components, 5 commits); residual design-blocked + deploy-gated    
- TRDD STATE — team_registry done (a318976, 3 residuals); approval_manager held on password env-fallback; resolve bug fixed    
- TRDD — MANAGER confirmed both findings; locked repoint recipe for the 4 #36 residual classes    

### Miscellaneous

- Drop literal /api/ from amcos_notify_agent comment (now grep-clean)    

### Refactor

- Repoint agent/command PROMPTS off direct /api/ → frozen CLI verbs    
- Repoint 5 top-level SKILL.md off direct /api/ → frozen CLI verbs    
- Repoint amcos_notify_agent.py name-resolve → aimaestro-agent.sh resolve    
- Repoint amcos_generate_team_report.py teams-fetch → aimaestro-teams.sh list    
- Repoint 14 teams-only skill reference docs off direct /api/teams → aimaestro-teams.sh list    
- Repoint amcos_team_registry.py off direct /api/ → frozen CLIs    


