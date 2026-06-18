# Changelog

All notable changes to this project will be documented in this file.
    ## [2.19.0] - 2026-06-18

### Documentation

- TRDD — RUNTIME COMPLETE (v2.18.2/3/4); COS 100% off direct /api/; only the 4 upstream verb-blocked ops remain (marked)    
- Add TRDD-562b49e3 — propagate governance R26-R40 into COS persona/skills/docs/SCEN (COS#21)    
- R32 — remove agent-held governance-password from approval-coordinator; auth via AID+R28, sudo is USER/UI-only (COS#21)    
- TRDD-562b49e3 STATE — Phase 1 audit done; inline-edit strategy; approval-coordinator R32 done (COS#21)    
- Persona — R29/R30/R31 reversals (MANAGER creates team+COS+5-base; mandate-gated; FREEZE) + add R26-R40 governance section (COS#21)    
- TRDD-562b49e3 STATE — persona R26-R40 done (2/~20) (COS#21)    
- R32 — drop agent-held governance-password from permission-management SKILL + 2 refs; auth via AID/R28 (COS#21)    
- TRDD-562b49e3 STATE — R32 perm-mgmt sub-batch done (5/~20) (COS#21)    
- R32 — finish perm-mgmt cluster; drop password from op-track + governance-details (delete Governance-Password section → R28/R32 authz) (COS#21)    
- TRDD-562b49e3 STATE — R32 perm-mgmt cluster complete (7/~20) (COS#21)    
- R32+R29 — team-spec drops --password; team create/delete marked MANAGER-only (R29.1); COS completes/customizes under mandate (COS#21)    
- R29 — reframe 'COS forms team' → MANAGER creates team+COS+5-base, COS completes/customizes under mandate; add R31 FREEZE to Step 4 (COS#21)    
- R29/R30/R38 — 3 skill examples: team-create routes to MANAGER; COS completes/customizes base under mandate (extra MEMBERs only) (COS#21)    
- TRDD-562b49e3 STATE — ALL R32 + ALL R29 done (13/~20) (COS#21)    
- R27 (install via core skills+CPV scan, not Claude CLI) + R38/R39 (escalate to COS/MANAGER, not user) (COS#21)    
- R38/R39 — fix 3rd escalate-to-user in role-briefing (line 446; audit undercounted) (COS#21)    
- TRDD-562b49e3 STATE — R27+R38/R39 done (16/~20); document the failure-recovery escalate-to-user scope judgment (COS#21)    
- R29/R30/R31 — ROLE_BOUNDARIES fix (MANAGER creates agents directly R29.1; COS mandate-gated R30) + add 5-base-invariant/FREEZE + R26-R40 pointer (COS#21)    
- README — add R26-R40 foundational-security-rules section (MANAGER creates teams, 5-base invariant + FREEZE, no agent sudo) (COS#21)    
- TRDD-562b49e3 STATE — EDIT PHASE COMPLETE (18 files); next = governance-scenarios.md → CPV → publish (COS#21)    
- Sync embedded TOC (Forming Team → Completing the Team) in persona + agent-coordination SKILL after the workflow-checklists rename (clears 2 CPV MINOR) (COS#21)    

### Tests

- Add R26-R40 propagation guard tests (9) — persona table, team-model reversal, no agent password, 5-base/FREEZE, R27 install, R38/R39 comm-routing (COS#21)    


