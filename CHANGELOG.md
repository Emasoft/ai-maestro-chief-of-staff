# Changelog

All notable changes to this project will be documented in this file.
    ## [2.12.6] - 2026-04-10

### Bug Fixes

- Add AMP communication restriction to all sub-agents    
- Add 'Loaded by' to all 53 skill descriptions for CPV validation    
- Publish.py runs CPV validation remotely + pre-push enforces --strict    
- Ruff F541 — remove extraneous f-prefix in publish.py    
- Remove CPV_PUBLISH_PIPELINE bypass from pre-push hook — CPV --strict always runs    
- Publish.py + pre-push use cpv-remote-validate via uvx    
- Rename duplicate validate_skill.py + align version to 2.12.4    

### Features

- Add compatible-titles and compatible-clients to agent profile    
- Add communication permissions from title-based graph    
- Add smart publish pipeline + pre-push hook enforcement    
- Add R12 minimum team composition rule to COS persona    

### Miscellaneous

- Update uv.lock    
- Update uv.lock    
- V2.12.5    
- Update uv.lock    

### Ci

- Update validate.yml to use cpv-remote-validate --strict    
- Strict publish.py + pre-push hook + release.yml propagation    


