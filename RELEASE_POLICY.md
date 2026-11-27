# Release and versioning policy

Record the deployed commit and date; use existing project versions where present or a `deploy-YYYY-MM-DD` tag with a suffix if needed. Validate links, assets and applicable browser checks before production deployment. Confirm the actual live deployment and record rollback commit.

## Release checklist

- Identify the exact commit and review the intended changes.
- Preserve existing version files, changelogs and release automation; update them only when applicable.
- Run the project's relevant checks and document failures or unavailable checks explicitly.
- Record scope, verification evidence, known limitations and rollback or recovery instructions.
- Do not publish a release, deploy, or claim successful validation solely because documentation changed.

Existing tags and historical versions remain authoritative. This policy does not itself create a release or change a version.
