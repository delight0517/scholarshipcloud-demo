# TODO

## 2026-09-10 ScholarshipCloud demo feedback

- [x] Capture requested fields: deadline, eligibility tabs, government/company/overseas source, amount, support period, competition/review signals.
- [x] Build demo UI for personal account matching, BlueCloud-style profile, saved opportunities, comments, source links, and premium report preview.
- [x] Set demo refresh copy to every 3 days while documenting production target of hourly refresh.
- [ ] Connect a real account system and BlueCloud identity binding.
- [ ] Replace demo data with source collectors for Korea Scholarship Foundation, foundation/corporate programs, and overseas-study scholarships.
- [ ] Add notification jobs for matched new opportunities.
- [ ] Add premium report generation from the user's saved profile, schedule, activities, grades, and target countries.
- [ ] Store reviews/spec summaries with citations and moderation.


## 2026-09-10 public deployment feedback

- [x] User requested real public deployment through GitHub or another suitable route.
- [x] GitHub connector install failed, so use local authenticated GitHub CLI instead.
- [x] Publish repository as public GitHub repo and configure GitHub Pages from /docs.

## 2026-09-14 실서비스 기능 요청

- [x] Add browser-side refresh from `scholarships.json` with no-cache timestamp and fallback status.
- [x] Add Google scholarship search link and live refresh UI.
- [x] Add AdSense slot scaffold with a daily three-view cap implementation pending final config.
- [ ] Replace `REPLACE_WITH_PUBLISHER_ID` and `REPLACE_WITH_AD_SLOT_ID` after AdSense approval.
- [ ] Connect an authenticated Google Programmable Search API key if in-page API results are required.
- [ ] Automate the JSON update job from verified official scholarship sources.
- [x] Connect ScholarshipCloud signup/login to the live BlueCloud auth API with CORS and per-account browser session.
- [x] Add saved age, student status, and interest profile matching for scholarship cards.
- [ ] Move scholarship profile fields from browser storage to a BlueCloud server-side profile endpoint.
- [x] Add Korean SEO title, description, keywords, canonical, Open Graph, JSON-LD, robots.txt, and sitemap.xml.
- [ ] Submit the public URL and sitemap in Google Search Console through Aside.
