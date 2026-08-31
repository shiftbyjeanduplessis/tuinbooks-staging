TUINBOOKS STABILITY STAGING v60.8.3 — AGENT TEST CANDIDATE
==========================================================

THIS IS NOT A PRODUCTION RELEASE.
It is a deterministic staging cutover package for the CURRENT TuinBooks repository.

WHY THIS PACKAGE EXISTS
-----------------------
The live Schedule accumulated multiple competing render/drag/basket authorities. This staging build stops
loading the known external legacy Schedule authority chain and installs one visible Schedule V2 renderer.
It deliberately does NOT replace app/app.js, Work, Clients, Billing, Mobile or Management.

IMPORTANT SOURCE LIMITATION
---------------------------
The large current app ZIP uploaded in chat was not mounted into the file-building runtime. Therefore this
package does not pretend to be a full rebuilt copy of your exact repository. Instead it applies the staging
cutover to the CURRENT repository you already have, backs up index.html first, and verifies the result.

APPLY
-----
1. Unzip this package.
2. Keep your current TuinBooks repository as-is.
3. Run:
       python APPLY-STAGING.py C:\path\to\TUINBOOKS-main
   or drag the repository folder onto APPLY-STAGING-WINDOWS.bat.
4. Run VERIFY-STAGING.py (the BAT does this automatically).
5. Commit/deploy that resulting repository to STAGING ONLY.
6. Hard-refresh staging in a clean browser profile.
7. Give AGENT-QA-CHECKLIST.md to the testing agent.

WHAT THE INSTALLER CHANGES
--------------------------
- app/index.html: removes known external legacy Schedule renderer/drag/basket script tags and adds v60.8.3 staging files.
- app/schedule-v2/schedule-v2.js + .css: one visible Schedule renderer, Basket and Rearrange owner.
- app/stability-staging-v6083.js + .css: staging diagnostics and logo fallback only.
- app/VERSION-STAGING.txt: staging marker.

WHAT IT DOES NOT CHANGE
-----------------------
- app/app.js
- Supabase schema/RPCs
- Clients logic
- Work logic
- Billing logic
- Mobile logic
- Management logic
- production service worker

ROLLBACK
--------
APPLY-STAGING.py creates .tb-staging-backup-YYYYMMDD-HHMMSS in the repository root containing the
pre-cutover app/index.html and service-worker.js (if present). Restore index.html from that folder to turn
the old Schedule load order back on in staging.

PROMOTION RULE
--------------
Do not promote this candidate until every Critical/P0 item in AGENT-QA-CHECKLIST.md passes, with three
complete cross-feature loops and persistence after reload/logout-login.
