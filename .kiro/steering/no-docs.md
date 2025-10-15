<!------------------------------------------------------------------------------------
   Add Rules to this file or a short description and have Kiro refine them for you:   
-------------------------------------------------------------------------------------> 
---
inclusion: always
---

# Code-Only Implementation Mode

## Core Principles

- Generate and modify source code files ONLY
- Do NOT create README.md, CHANGELOG.md, or any documentation files unless explicitly requested
- Do NOT generate summary documents after code implementation
- Do NOT update documentation automatically
- Focus exclusively on functional code implementation

## Response Behavior

After completing code implementation:
- Confirm completion in chat response
- Do not create markdown summaries or documentation files
- Do not explain implementation in separate files
- Keep all explanations in chat responses only

## File Creation Guidelines

### Allowed Files
- Source code files (`.ts`, `.tsx`, `.js`, `.jsx`, `.py`, etc.)
- Configuration files (`.json`, `.yaml`, `.toml`, `.env`, etc.)
- Test files when explicitly requested
- Data files required for functionality (`.sql`, `.csv`, etc.)
- Build and tooling files (`Dockerfile`, `.dockerignore`, etc.)

### Prohibited Files
- `README.md` or any `.md` documentation files
- `CHANGELOG.md` or version documentation
- API documentation files
- Implementation summaries or overviews
- Tutorial or guide files
- Summary of thw works in .txt file

## Exceptions

Documentation files may be created only when:
- User explicitly requests documentation
- User asks to update existing documentation files
- Project scaffolding specifically requires a README