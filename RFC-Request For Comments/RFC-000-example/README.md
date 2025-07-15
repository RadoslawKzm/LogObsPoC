# RFC-000: Unified Configuration System

- **RFC Number:** 000
- **Title:** Unified Configuration System
- **Author:** Jane Doe (@janedoe)
- **Created:** 2025-07-15
- **Updated:** 2025-07-15
- **Status:** Accepted
- **Discussion:** https://github.com/your-org/rfc-repo/pull/1

---

## 🎯 Summary

Unify all runtime configuration under a single `.config.toml` file instead of environment variables and scattered YAML/JSON files.

---

## 🧩 Motivation

Currently, configuration is inconsistent and hard to discover:
- Environment variables are undocumented
- Different components read from separate YAML/JSON files
- Local development is cumbersome

A single, structured config file makes configuration explicit, portable, and easier to manage across environments.

---

## 🛠️ Detailed Design

Introduce a new top-level `.config.toml` file at the project root.
# RFC-000: Unified Configuration System

- **RFC Number:** 000  
- **Title:** Unified Configuration System  
- **Author:** Jane Doe (@janedoe)  
- **Created:** 2025-07-15  
- **Updated:** 2025-07-15  
- **Status:** Accepted  
- **Discussion:** [RFC PR #1](https://github.com/your-org/rfc-repo/pull/1)

---

## 🎯 Summary

Unify all runtime configuration under a single `.config.toml` file instead of scattered environment variables and YAML/JSON config files.

---

## 🧩 Motivation

Currently, configuration is inconsistent and hard to manage:
- 🔍 Environment variables are undocumented and easy to miss  
- 🧩 Different services use YAML, JSON, or ad-hoc config loaders  
- 🧪 Local development requires custom hacks per service  

A unified `.config.toml` approach makes all configuration:
- **Explicit:** Everything in one place  
- **Structured:** Easier to validate and lint  
- **Portable:** Dev/prod parity via a shared format  

---

## 🛠️ Detailed Design

Introduce a new top-level `.config.toml` file at the project root.

Example:

<triple_quotes>toml
[server]
host = "0.0.0.0"
port = 8000

[database]
url = "postgresql://user:pass@localhost:5432/db"
pool_size = 10
<triple_quotes>

**Implementation details:**
- Config is parsed at startup using **Pydantic Settings**
- `.config.toml` is loaded using **python-decouple**
- Environment variable overrides remain possible but discouraged
- Central `config.py` module replaces ad-hoc `os.getenv()` and `config.yaml` loaders

---

## 🔁 Alternatives Considered

- **Environment variables only:** Inflexible, no schema, difficult to document  
- **YAML/JSON config files:** Supported, but TOML is more readable and developer-friendly for nested structures  

---

## 🔄 Backward Compatibility

- Legacy environment variable and YAML support will remain for **one release cycle**
- Deprecation warnings will guide migration
- All core components (API, CLI, workers) will support both systems during transition

---

## 📈 Drawbacks

- Developers must update their local setup to use `.config.toml`
- CI/CD pipelines and secrets management may need changes
- Risk of duplication if both systems are used inconsistently during migration

---

## ✅ Acceptance Criteria

- `.config.toml` is loaded at runtime via `config.py`
- Legacy configs emit warnings if used
- All core services (API, CLI, background workers) consume config via unified loader
- Schema validation is enforced using Pydantic models
- Documentation is updated with example config file and usage

---

## 🗒️ Unresolved Questions

- Should we support layered config (e.g., `.config.local.toml`, `.config.prod.toml`)?
- Do we want to enforce strict schema validation or allow optional keys?
- Should secrets (e.g., DB passwords) be handled via separate encrypted files?

---

## 📚 References

- [TOML Specification](https://toml.io/en/)
- [Python Decouple](https://pypi.org/project/python-decouple/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)

---

## ✅ Key Benefits

- **Clarity:** All config in a single structured file  
- **Validation:** Pydantic provides runtime checks and type hints  
- **Portability:** Same config file works in local/dev/staging/prod with minimal changes  
- **Onboarding:** New developers can see all required config at a glance  
- **Maintainability:** Changing config keys only needs updates in one file  

> 🧠 Summary: This system simplifies config management and enforces consistency across environments.

---

## ❓ FAQ

> Common developer questions about this RFC. Refer here before asking again.

### Q: Why TOML instead of YAML or JSON?

**A:** TOML is easier to write and read for nested configurations, especially for developers. Unlike YAML, it's less error-prone (no weird indent bugs), and unlike JSON, it's more ergonomic for configuration (supports comments, multiline strings, etc.).

---

### Q: Can I still use environment variables?

**A:** Yes, you can override values from `.config.toml` using env vars, but it's discouraged for anything except secrets and CI use cases.

---

### Q: What about secrets in the config file?

**A:** We recommend keeping secrets out of versioned `.config.toml`. Load them via environment variables or inject a secrets manager integration on top of the config loader.

---

### Q: Do we support different configs per environment?

**A:** Not yet, but we're considering layered configs like `.config.dev.toml`, `.config.prod.toml`. These would override or extend the base config file.

---

> Have a new question? Ask it once — if it's recurring, we’ll add it here.

Example:

```toml
[server]
host = "0.0.0.0"
port = 8000

[database]
url = "postgresql://user:pass@localhost:5432/db"
pool_size = 10
```
The application will use pydantic + python-decouple to parse the file at startup. ENV overrides remain possible but discouraged.

🔁 Alternatives Considered

    - Stick with environment variables (but lacks structure and discoverability)
    - Use JSON/YAML (less ergonomic than TOML for nested config)

🔄 Backward Compatibility

Old environment variable support will remain for one release cycle with deprecation warnings.

📈 Drawbacks

    - Requires all team members to update their workflow
    - Might cause friction in CI/CD integration until adapted

✅ Acceptance Criteria

    - .config.toml is parsed at runtime
    - Legacy config is deprecated
    - All core services (API, worker, CLI) migrate to the new config loader

🗒️ Unresolved Questions

    - Should we allow multiple config layers (e.g. .config.dev.toml)?
    - Do we want schema validation beyond Pydantic?

📚 References

    - TOML Spec: https://toml.io/en/
    - Python Decouple: https://pypi.org/project/python-decouple/
    - Pydantic Settings: https://docs.pydantic.dev/latest/concepts/pydantic_settings/
