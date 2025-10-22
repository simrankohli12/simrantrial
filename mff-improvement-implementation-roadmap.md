# MFF Improvement Initiative: Implementation Roadmap
## Co-triggering Assets + Trust Signals

**Program Name**: MFF 2.0 - Trust & Engagement Enhancement
**Owner**: Product Lead - Google Search Ads Messaging
**Timeline**: 5 months (20 weeks)
**Target**: Close CTR and CvR gap with LTA Unicard
**Status**: Planning Phase
**Last Updated**: October 22, 2025

---

## Executive Summary

This document outlines the combined implementation strategy for two high-priority MFF improvements:
1. **Co-triggering with Other Assets** (Feature MFF-005)
2. **Trust Signals** (Feature MFF-006)

By building these features in parallel with strategic sequencing, we can accelerate time-to-value and create synergistic benefits.

### Expected Impact (Combined)
| Metric | Current | Target | Improvement |
|--------|---------|--------|-------------|
| **CTR** | 4.2% | 6.3-7.1% | +50-70% |
| **CvR** | 20.7% | 24.8-26.2% | +20-27% |
| **Impression Rate** | 1.6M/day | 2.0M/day | +25% |
| **Competitive Gap** | 4x behind LTA | 2.4x behind | 40% closed |

**Strategic Rationale**: Assets increase engagement opportunities (CTR), trust signals increase conversion confidence (CvR) - together they address MFF's full funnel weakness.

---

## Why Build Both Together?

### Synergies
1. **Shared Infrastructure**: Both features need UI layout engine updates, serving pipeline changes, A/B testing framework
2. **Complementary UX**: Assets provide breadth (more options), trust signals provide depth (more confidence)
3. **Unified Story**: "MFF now offers richer, more trustworthy ads" is stronger than separate pitches
4. **Data Leverage**: Trust signals help users choose which asset to click (e.g., "4.7 stars" makes sitelinks more appealing)

### Risks of Building Separately
- ❌ Two separate UI redesigns (wasteful)
- ❌ Delayed impact (wait 10 months instead of 5)
- ❌ Fragmented advertiser messaging
- ❌ Two separate experiment cycles (opportunity cost)

### Risk Mitigation
- **Phased Rollout**: Assets first (Week 10), Trust Signals second (Week 16) - de-risk sequentially
- **Shared Ownership**: Single PM, single eng lead, unified roadmap
- **Incremental Value**: Each feature adds value independently; failure of one doesn't block the other

---

## Integrated Timeline

```
Months:     1         2         3         4         5
Weeks:   1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20
         │                                                         │
Assets:  [───Foundation───][─UI/Exp─][L][────Optimization────────]
Trust:   [──Data Pipeline──][─UI─][───Exp───][L][──Optimization──]
         │                         │          │
         └─ Shared infra work      │          └─ Trust Signals Launch
                                   └─ Assets Launch (Week 10)

Legend: [─] = Active work, [L] = Launch
```

### Key Milestones
- **Week 4**: Shared UI framework ready (layout engine, A/B test infra)
- **Week 10**: Co-triggering Assets launches to 100% traffic 🚀
- **Week 16**: Trust Signals launches to 100% traffic 🚀
- **Week 20**: Combined optimization (ML-powered asset + signal selection)

---

## Phase-by-Phase Plan

### Phase 0: Foundation (Weeks 1-4)
**Goal**: Build shared infrastructure, validate data availability

#### Week 1: Planning & Alignment
**Activities**:
- Kickoff meeting with all stakeholders (Eng, UX, Legal, Data, Sales)
- Finalize asset prioritization (Sitelinks + Callouts + Favicon vs. more)
- Finalize trust signal prioritization (Verification + Rating + Response Time)
- Privacy/Legal review kickoff for both features
- Design review: unified UI that accommodates both features

**Deliverables**:
- ✅ PRD approved by stakeholders
- ✅ Privacy review scheduled (Week 2 delivery)
- ✅ Engineering architecture doc (high-level)

**Risks**:
- Privacy blocks trust signal usage → Mitigation: Start privacy review immediately, have fallback (fewer signals)

---

#### Week 2: Data Validation
**Activities**:
- **Assets**: Log analysis - confirm 88% of MFF impressions have assets available
- **Trust**: Query GMB API, message logger to assess trust signal coverage
  - % of advertisers with verification: ?
  - % with ratings (≥10 reviews): ?
  - % with response time data (≥20 messages): ?
- Segment analysis: coverage by vertical, campaign size, advertiser type

**Deliverables**:
- ✅ Data availability report with segment breakdowns
- ✅ Decision: Go/no-go for each asset type and trust signal type
- ✅ Coverage gaps identified (e.g., only 30% have response time → decide if OK for V1)

**Success Criteria**:
- Asset availability ≥80% (confirmed)
- Trust signal coverage ≥40% for at least 2 signals (e.g., 60% have ratings, 50% have verification)

---

#### Week 3-4: Shared Infrastructure
**Activities**:
- **UI Framework**: Build responsive layout engine
  - Component: MFF base (image, headline, message CTA)
  - Component: Asset slot (sitelinks, callouts)
  - Component: Trust signal bar (icons + text)
  - Layout rules: mobile vs desktop, max height constraints
- **Serving Pipeline**: Add hooks for asset/trust signal fetching
  - Parallel fetch: assets + trust signals alongside image
  - Timeout handling: 50ms for assets, 30ms for trust signals
  - Fallback logic: render base MFF if fetch fails
- **A/B Testing Framework**: Setup experiment configs
  - Traffic splitting by ad_id (stable assignment)
  - Logging schema: assets shown, trust signals shown, clicks per asset/signal
- **Caching Layer**: Setup caching for assets and trust signals
  - Asset cache: 5 min TTL (high QPS campaigns)
  - Trust signal cache: 24 hour TTL (daily refresh)

**Deliverables**:
- ✅ UI framework deployed to staging
- ✅ Serving pipeline changes reviewed and approved
- ✅ A/B test configs ready for both features
- ✅ Caching layer tested (latency <30ms p95)

**Risks**:
- Latency budget exceeded → Mitigation: Aggressive caching, async fetching, fallback to base MFF

---

### Phase 1: Assets - Build & Launch (Weeks 5-12)

#### Week 5-6: Asset Selection & Rendering
**Activities**:
- Implement asset fetcher (query asset store, filter by status/targeting)
- Implement compatibility filter (only MFF-compatible assets)
- Implement asset selector (rank by predicted CTR, select best combination)
- Build UI layouts: 4 sitelinks + callouts + favicon
- Click tracking: log asset_id with each click event

**Deliverables**:
- ✅ Asset serving backend complete
- ✅ UI rendering works on all devices/browsers
- ✅ Internal dogfood: Googlers see MFF with assets

**Testing**:
- Unit tests: asset selection logic (100 edge cases)
- Integration tests: end-to-end serving pipeline
- Manual QA: 10 devices x 5 browsers = 50 configs tested

---

#### Week 7-9: Assets Experimentation
**Activities**:
- **Week 7**: Launch A/B test at 10% traffic
  - Control: Base MFF (no assets)
  - Treatment: MFF + Sitelinks + Callouts + Favicon
  - Monitor: CTR, CvR, latency, errors
- **Week 8**: Ramp to 50% traffic if metrics positive
  - Daily metric reviews
  - Iterate on asset selection logic if needed
- **Week 9**: Analyze results, prepare launch decision
  - Statistical significance check (p<0.05)
  - Segment analysis (by vertical, device, position)
  - Advertiser feedback survey

**Success Criteria for Launch**:
- CTR lift ≥10% (stat sig)
- CvR no regression
- Latency <65ms added (p95)
- Error rate <0.1%

---

#### Week 10-12: Assets Launch & Stabilization
**Activities**:
- **Week 10**: 100% rollout 🚀
  - Gradual: 50% → 75% → 100% over 3 days
  - Monitor dashboards 24/7
  - Rollback plan ready (flip kill switch)
- **Week 11**: Monitor stability
  - Daily metric snapshots
  - Investigate anomalies (e.g., unexpected CTR drop in one vertical)
  - Publish internal blog post: "Assets launch success"
- **Week 12**: Advertiser enablement
  - Help Center article: "MFF now shows your sitelinks and callouts"
  - Sales enablement: Updated pitch deck
  - Collect feedback via support tickets, surveys

**Expected Results**:
- CTR: 4.2% → 5.2% (+24% lift) ✅
- Impression rate: 1.6M → 1.8M/day (+12% from better engagement) ✅

---

### Phase 2: Trust Signals - Build & Launch (Weeks 5-16)
*Note: Starts Week 5, overlaps with Assets work*

#### Week 5-8: Trust Signal Data Pipeline
**Activities**:
- Build response time aggregation (batch job, runs daily)
  - Query message logger for all MFF clicks → message timestamps
  - Group by advertiser_id, compute avg response time (exclude outliers)
  - Store in Trust Signal Store
- Build message volume aggregation (streaming, 1-hour latency)
  - Count messages per advertiser (rolling 30 days)
  - Update Trust Signal Store hourly
- Integrate GMB API (ratings, verification, hours)
  - Daily batch sync
  - Handle rate limits, retries
- Build Trust Signal Store (key-value, 24hr TTL)
  - Key: advertiser_id
  - Value: {verified, rating, review_count, response_time, volume, trust_score}
- Backfill historical data (past 90 days)

**Deliverables**:
- ✅ Trust Signal Store populated with data for all MFF advertisers
- ✅ Data freshness <24 hours for 95% of advertisers
- ✅ Trust score calculation validated against manual samples

**Testing**:
- Data quality audit: manual review of 100 random advertisers
- Latency test: fetch trust signals <30ms p95 (cached)

---

#### Week 9-11: Trust Signal UI & Integration
**Activities**:
- Implement trust signal selector (pick top 2-3 signals based on priority)
- Build UI components: verification badge, star rating, response time label
- Integrate with ad serving (fetch trust signals in parallel with assets)
- Click tracking: log which trust signals were shown per impression

**Deliverables**:
- ✅ Trust signals render correctly on all devices
- ✅ Internal dogfood: Googlers see MFF with trust signals
- ✅ A/B test config ready

**Testing**:
- Visual QA: 50 device/browser combinations
- Accessibility audit: screen readers, keyboard navigation, color contrast

---

#### Week 12-15: Trust Signals Experimentation
**Activities**:
- **Week 12-13**: Single-signal tests (parallel, can overlap)
  - Test A: Verification badge (50% on/off)
  - Test B: Star rating (50% on/off)
  - Test C: Response time (50% on/off)
  - Measure: CTR, CvR per signal
- **Week 14**: Multi-signal combination test
  - Control: No trust signals
  - Treatment A: Verification + Rating
  - Treatment B: Rating + Response Time
  - Treatment C: All 3 signals
  - Traffic split: 25% each
- **Week 15**: Analyze results, prepare launch
  - Identify winning combination
  - Segment analysis (does rating matter more for some verticals?)

**Success Criteria for Launch**:
- CTR lift ≥8% OR CvR lift ≥10% (stat sig)
- Winning signal combination identified

---

#### Week 16-18: Trust Signals Launch & Stabilization
**Activities**:
- **Week 16**: 100% rollout 🚀
  - Gradual: 50% → 75% → 100% over 3 days
  - Monitor metrics (CTR, CvR, trust signal coverage)
  - Rollback plan ready
- **Week 17**: Monitor stability
  - Address any data quality issues (e.g., stale response times)
  - Publish case studies: "How trust signals improved CvR by 12%"
- **Week 18**: Advertiser enablement
  - Launch "Your Trust Score" dashboard
  - Help Center: "What are trust signals?"
  - Sales training: "Selling trust signals"

**Expected Results**:
- CvR: 20.7% → 23.2% (+12% lift) ✅
- CTR: 5.2% → 5.9% (+13% lift on top of assets) ✅

---

### Phase 3: Combined Optimization (Weeks 19-20+)

#### Week 19-20: ML-Powered Selection
**Activities**:
- Train CTR/CvR prediction model
  - Features: query, available assets, trust signals, user context
  - Target: predict CTR/CvR for each asset + signal combination
  - Data: 10 weeks of experiment data (Weeks 10-20)
- Deploy ML-powered selection
  - Asset selector: ML picks best assets per impression
  - Trust signal selector: ML picks best signals per impression
  - Online learning: update model daily
- A/B test: ML selection vs static selection
  - Expect: +5-10% further CTR improvement

**Deliverables**:
- ✅ ML model deployed (latency <5ms p99)
- ✅ Online learning pipeline active (daily retraining)

---

#### Week 20+: Continuous Optimization
**Ongoing Activities**:
- Monitor metrics weekly
- A/B test UI variations (e.g., 2 sitelinks vs 4)
- Expand asset types (location extensions, price extensions)
- Add more trust signals (operating hours, certifications)
- Advertiser education campaigns
- Iterate on trust score algorithm

---

## Resource Plan

### Team Structure

**Core Team** (Dedicated):
- 1x Product Manager (PM Lead) - 100% allocated
- 1x Engineering Lead (Backend) - 100%
- 1x Frontend Engineer - 100%
- 1x Data Engineer - 100%
- 1x UX Designer - 100%
- 1x Product Analyst - 100%

**Supporting Team** (Part-Time):
- 1x ML Engineer - 50% (Phase 3)
- 1x Privacy Counsel - 20% (Weeks 1-2)
- 1x QA Engineer - 50% (Weeks 6-9, 12-15)
- 1x UX Researcher - 30% (User testing)
- 1x Technical Writer - 20% (Documentation)

**Total Headcount**: 6.5 FTE (full-time equivalent)

---

### Engineering Effort Estimate

| Component | Complexity | Estimate | Risk |
|-----------|----------|----------|------|
| **Shared Infrastructure** | | | |
| - UI Layout Engine | Medium | 2 weeks | Low |
| - Serving Pipeline Integration | High | 2 weeks | Medium |
| - A/B Test Framework | Low | 1 week | Low |
| **Asset Co-triggering** | | | |
| - Asset Fetcher & Selector | Medium | 2 weeks | Low |
| - UI Rendering (Assets) | Medium | 2 weeks | Low |
| - Click Tracking | Low | 1 week | Low |
| **Trust Signals** | | | |
| - Data Pipeline (Response Time) | High | 2 weeks | Medium |
| - GMB API Integration | Medium | 1 week | Low |
| - Trust Signal Store | Medium | 1 week | Low |
| - UI Rendering (Trust) | Medium | 1 week | Low |
| **ML Optimization** | | | |
| - CTR Prediction Model | High | 3 weeks | High |
| - Online Learning Pipeline | High | 2 weeks | High |

**Total Engineering**: ~20 eng-weeks (spread across 5 months with 2-3 eng)

---

## Budget & Costs

### One-Time Costs
| Item | Cost | Notes |
|------|------|-------|
| Engineering (20 eng-weeks) | $200K | Loaded cost ~$10K/eng-week |
| Design & UX Research | $30K | User testing, prototypes |
| Privacy/Legal Review | $10K | External counsel if needed |
| QA & Testing | $20K | Device lab, accessibility audit |
| **Total One-Time** | **$260K** | |

### Ongoing Costs (Annual)
| Item | Cost | Notes |
|------|------|-------|
| Trust Signal Data Pipeline | $50K/year | Compute, storage for daily batch jobs |
| GMB API Calls | $20K/year | ~1M API calls/day at $0.05/1000 |
| Increased Ad Serving Costs | $30K/year | Marginal compute for asset/signal fetching |
| ML Model Training & Serving | $40K/year | GPU for training, inference servers |
| **Total Ongoing** | **$140K/year** | |

### Revenue Impact (Back-of-Envelope)
- Current: 1.6M impressions/day x 4.2% CTR x $1.68 CPC = **$113K revenue/day**
- Post-Launch: 2.0M impr/day x 6.5% CTR x $1.70 CPC = **$221K revenue/day**
- **Incremental Revenue**: $108K/day = **$39M/year** 🎉

**ROI**: ($39M - $140K) / $260K = **150x first-year ROI**

*Note: This is a simplified model; actual impact depends on advertiser demand, competitive dynamics, etc.*

---

## Success Metrics & KPIs

### Primary Metrics (OKRs for this Initiative)

**Objective**: Close the performance gap between MFF and LTA Unicard

**Key Results** (6 months post-launch):
1. **CTR**: Increase from 4.2% to ≥6.5% (+55%) 🎯
2. **CvR**: Increase from 20.7% to ≥23% (+11%) 🎯
3. **Impression Rate**: Increase from 1.6M to ≥2.0M per day (+25%) 🎯
4. **Advertiser Satisfaction (NPS)**: Improve by +15 points 🎯

### Secondary Metrics

| Metric | Baseline | Target | Measurement |
|--------|----------|--------|-------------|
| Click Split (Long/Short) | 0.24 | 0.30 | Monthly avg |
| CPC | $1.68 | ≤$1.75 | Weekly avg |
| Ad Serving Latency (p95) | 200ms | ≤270ms (+70ms budget) | Daily |
| Asset Availability per Impression | 0 | 1.5+ | Weekly avg |
| Trust Signal Coverage | 0% | 70% | Weekly avg |

### Leading Indicators (Early Signals of Success)

**Week 2-4** (Foundation):
- ✅ Asset availability confirmed ≥85%
- ✅ Trust signal coverage ≥40% (for ≥2 signals)
- ✅ Privacy approval obtained

**Week 10** (Assets Launch):
- ✅ CTR lift ≥10% in A/B test
- ✅ Asset render success rate >99%
- ✅ Latency within budget

**Week 16** (Trust Signals Launch):
- ✅ CvR lift ≥10% in A/B test
- ✅ Trust score data quality >95% accurate

**Week 20** (Combined):
- ✅ Combined CTR+CvR lifts meet targets
- ✅ No increase in advertiser support tickets (or positive feedback)

---

## Risk Register

### Critical Risks (Red)

| ID | Risk | Impact | Likelihood | Mitigation | Owner |
|----|------|--------|-----------|------------|-------|
| R1 | Privacy blocks trust signal usage | 🔴 High | 🟡 Medium | Start privacy review immediately; have fallback with fewer signals | PM + Legal |
| R2 | Assets increase latency >100ms | 🔴 High | 🟡 Medium | Aggressive caching, async fetching, fallback to base MFF | Eng Lead |
| R3 | Trust signal data coverage <30% | 🔴 High | 🟡 Medium | Validate early (Week 2); deprioritize low-coverage signals | Data Eng |
| R4 | Experiment shows no CTR/CvR lift | 🔴 High | 🟢 Low | Phase 1 validation; iterate based on user feedback | PM + Analyst |

### Moderate Risks (Yellow)

| ID | Risk | Impact | Likelihood | Mitigation | Owner |
|----|------|--------|-----------|------------|-------|
| R5 | UI cluttered, reduces message CTA clicks | 🟡 Medium | 🟡 Medium | A/B test multiple layouts; maintain visual hierarchy | UX Designer |
| R6 | GMB API rate limits | 🟡 Medium | 🟡 Medium | Batch requests, cache aggressively, graceful degradation | Data Eng |
| R7 | Advertiser confusion about new features | 🟡 Medium | 🟠 High | Clear documentation, sales training, proactive comms | PM + Marketing |
| R8 | Timeline slips due to resource constraints | 🟡 Medium | 🟡 Medium | Weekly status reviews, escalate blockers early | PM |

### Low Risks (Green)

| ID | Risk | Impact | Likelihood | Mitigation | Owner |
|----|------|--------|-----------|------------|-------|
| R9 | Advertiser gaming trust signals (fake reviews) | 🟢 Low | 🟡 Medium | Leverage Google's existing fraud detection | Data Eng |
| R10 | Competitive response (others copy features) | 🟢 Low | 🟠 High | Acceptable - we benefit from being first mover | PM |

---

## Launch Plan

### Pre-Launch (Week 9 for Assets, Week 15 for Trust)

**Checklist**:
- [ ] A/B test shows stat sig improvement (CTR/CvR)
- [ ] Latency within budget (<70ms added)
- [ ] Error rate <0.1% in experiment
- [ ] Privacy/Legal sign-off obtained
- [ ] Rollback plan tested (can revert in <5 minutes)
- [ ] On-call rotation staffed (24/7 for launch week)
- [ ] Launch communication drafted (internal blog, sales email)
- [ ] Help Center docs published
- [ ] Monitoring dashboards set up (Grafana/Tableau)

---

### Launch Day (Week 10 for Assets, Week 16 for Trust)

**Hour-by-Hour Plan**:

**9 AM PT**: Kickoff meeting
- Final go/no-go decision
- Review metrics baseline
- Confirm team availability

**10 AM PT**: Ramp to 10%
- Push config change (traffic dial to 10%)
- Monitor dashboards every 15 minutes
- Check for errors, latency spikes

**12 PM PT**: Review 2-hour metrics
- CTR/CvR trending as expected?
- Latency OK? Errors OK?
- Go/no-go for 50% ramp

**2 PM PT**: Ramp to 50%
- Push config change
- Continue monitoring every 30 minutes

**5 PM PT**: Review 6-hour metrics
- Full day of 10% + half day of 50%
- If all green, plan 100% ramp for next day

**Next Day, 10 AM PT**: Ramp to 100%
- Push config change
- Monitor closely for 4 hours
- Declare launch success or rollback

---

### Post-Launch (Weeks 11-12 for Assets, 17-18 for Trust)

**Day 1-3**:
- Monitor metrics every 4 hours
- Triage any issues (bugs, advertiser confusion)
- Publish internal launch announcement

**Day 4-7**:
- Daily metric snapshots
- Synthesize early feedback from support tickets
- Write launch retrospective doc

**Week 2**:
- Publish external blog post: "Introducing MFF 2.0"
- Sales enablement webinar
- Advertiser email campaign: "Your ads just got better"

**Week 3-4**:
- Analyze segment performance (which verticals benefited most?)
- Plan Phase 3 (ML optimization)
- Celebrate with team! 🎉

---

## Stakeholder Communication Plan

### Internal Stakeholders

**Weekly Status Updates** (Email to leadership):
- Sent: Every Friday
- Audience: VP Product, Director of Ads, Eng Director
- Content: Progress vs plan, key metrics, risks, decisions needed

**Monthly Business Review** (Meeting):
- Frequency: Last Monday of each month
- Audience: Cross-functional leads (Product, Eng, Sales, Marketing, Legal)
- Content: Deep dive on metrics, roadmap adjustments, resource needs

**Launch Announcements** (Internal blog):
- Week 10: "Assets Launch Success - MFF CTR Up 24%"
- Week 16: "Trust Signals Launch - MFF CvR Up 12%"
- Week 20: "MFF 2.0 Complete - Closing the Gap with LTA"

---

### External Stakeholders (Advertisers)

**Pre-Launch** (Week 8 for Assets, Week 14 for Trust):
- Blog post: "Coming soon: Richer messaging ads"
- Email to beta advertisers: "You're getting early access"

**Launch Week** (Week 10 / 16):
- Blog post: "Introducing [Feature Name]"
- Help Center article: "How [Feature] works"
- In-product notification: "Your ads now show [feature]"

**Post-Launch** (Week 12 / 18):
- Email campaign: "Your messaging ads are performing better - here's why"
- Case studies: "How [Advertiser X] increased leads by 25%"
- Quarterly webinar: "Best practices for MFF 2.0"

---

### Sales Enablement

**Materials Needed**:
- **Week 9 / 15**: Sales deck (updated pitch with new features)
- **Week 10 / 16**: FAQ doc (anticipated advertiser questions)
- **Week 11 / 17**: ROI calculator (show expected performance lift)
- **Week 12 / 18**: Case studies (3-5 success stories)

**Training Sessions**:
- **Week 9 / 15**: Live webinar for sales team (1 hour)
  - What's new, why it matters, how to pitch
  - Demo of new ad formats
  - Q&A
- **Ongoing**: Office hours (weekly 30-min drop-in sessions)

---

## Success Criteria & Go/No-Go Decision Framework

### Experiment Go/No-Go (Before Launch)

**Must-Have** (blockers if not met):
- ✅ CTR lift ≥8% (Assets) or CvR lift ≥8% (Trust) - stat sig p<0.05
- ✅ No regression in CvR (Assets) or CTR (Trust)
- ✅ Latency <70ms added (p95)
- ✅ Error rate <0.1%
- ✅ Privacy/Legal approval obtained

**Nice-to-Have** (launch anyway, but monitor):
- 🟡 Positive advertiser feedback (if survey response rate low)
- 🟡 Improvement across all verticals (OK if some segments neutral)

**Decision Maker**: PM Lead + Eng Lead (joint decision)

---

### Post-Launch Success (Week 20 - Final Assessment)

**Celebrate if**:
- 🎉 CTR ≥6.0% (achieved)
- 🎉 CvR ≥23% (achieved)
- 🎉 Impression rate ≥2.0M/day (achieved)
- 🎉 Advertiser NPS improved ≥10 points

**Iterate if**:
- 🔄 Partial success (1-2 metrics met, but not all)
- 🔄 Positive direction but targets missed by <20%
- Action: Double down on optimization (Phase 3)

**Pivot if**:
- 🚨 No improvement or regression in key metrics
- 🚨 Advertiser backlash (NPS drops)
- Action: Roll back, conduct post-mortem, revisit strategy

*Note: Given the strong rationale and competitive benchmarks, "pivot" scenario is very unlikely.*

---

## Learnings & Iteration Plan

### Experiment Learnings (Capture During Phase)

**Questions to Answer**:
1. Which asset types drive the most incremental clicks? (Sitelinks vs callouts vs favicon)
2. Which trust signals have the biggest CvR impact? (Rating vs response time vs verification)
3. Do trust signals work better for certain verticals? (e.g., ratings matter more for restaurants?)
4. What's the optimal number of sitelinks? (2 vs 4)
5. Does asset/signal impact vary by device? (Mobile vs desktop)

**Method**:
- A/B tests designed to answer these questions
- Segment analysis (vertical, device, position, advertiser size)
- User surveys and interviews

**Output**:
- Learnings doc (Week 12 for assets, Week 18 for trust)
- Feed into Phase 3 optimization priorities

---

### Post-Launch Iteration Roadmap (Month 6-12)

Based on learnings, prioritize:

**High Priority** (Month 6-9):
- [ ] ML-powered asset + trust signal selection (Week 19-20)
- [ ] Expand to more asset types (location extensions, price)
- [ ] Add more trust signals (operating hours, certifications)
- [ ] Advertiser trust score dashboard

**Medium Priority** (Month 9-12):
- [ ] Dynamic asset generation (auto-generate callouts from landing page)
- [ ] Personalized signal selection (show different signals based on user)
- [ ] Real-time trust signals ("Available now")
- [ ] Negative signal transparency experiments

**Low Priority** (Month 12+):
- [ ] WhatsApp business profile integration
- [ ] Trust signal auctions (advertisers pay to highlight signals)
- [ ] Video assets in MFF
- [ ] Chatbot preview in ad

---

## Appendix

### A. Terminology

- **MFF**: Message Forward Format (the ad format we're improving)
- **LTA Unicard**: Lead Type Ad Unicard (the benchmark format, 17.2% CTR)
- **CTR**: Click-Through Rate (% of impressions that result in clicks)
- **CvR**: Conversion Rate (% of clicks that result in message sends)
- **Asset**: Ad extension (sitelink, callout, etc.)
- **Trust Signal**: Credibility indicator (rating, verification, etc.)
- **pCTR**: Predicted CTR (used by serving models to select ads)

### B. Related Documents

- [Feature Exploration: Co-triggering with Other Assets](feature-exploration-co-triggering-assets.md)
- [Feature Exploration: Trust Signals](feature-exploration-trust-signals.md)
- [MFF Improvement Ideas (Original Notes)](improvement notes)
- MFF Technical Spec (internal link)
- MFF Serving Architecture (internal link)

### C. FAQ

**Q: Why not fix eligibility barriers first (pinned headlines, fallback images)?**
A: Those are great ideas, but deemed "not product initiatives" per leadership. We're focusing on features that enhance the core format experience.

**Q: Can we launch both features at the same time?**
A: Risky. Sequential launches (Assets in Week 10, Trust in Week 16) de-risks and allows us to isolate impact.

**Q: What if experiments fail?**
A: We iterate. The competitive analysis and user research strongly suggest these features work, so more likely we need to refine execution (e.g., better signal selection, clearer UI).

**Q: How does this affect Google's revenue?**
A: Positively. Higher CTR = more clicks = more revenue. Slight CPC increase is acceptable if CvR improves (advertisers get better ROI).

**Q: What about international markets?**
A: V1 focuses on US (where MFF currently serves). V2 can expand to other English-speaking markets. Trust signals may need localization (e.g., different review sources per country).

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | Oct 22, 2025 | PM Lead | Initial draft |

---

## Next Steps (Immediate Actions)

**This Week**:
1. [ ] Schedule stakeholder kickoff (Week 1)
2. [ ] Begin privacy review process (Legal team)
3. [ ] Assign engineering resources (Eng Lead)
4. [ ] Draft data availability query (Data Eng)
5. [ ] Create project Gantt chart (PM)

**Week 1 Deliverables**:
- [ ] Kickoff meeting complete ✅
- [ ] Engineering architecture doc (v0.1) ✅
- [ ] Data availability queries running ✅
- [ ] Privacy review scheduled ✅

---

**Let's build MFF 2.0 and close the gap with LTA! 🚀**
