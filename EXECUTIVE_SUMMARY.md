# MFF 2.0: Executive Summary
## Co-triggering Assets + Trust Signals

**Date**: October 22, 2025
**Owner**: Product Lead - Google Search Ads Messaging
**Status**: Ready for Stakeholder Review

---

## The Opportunity

Message Forward Format (MFF) is significantly underperforming vs LTA Unicard:
- **CTR**: 4.2% vs 17.2% (4x gap)
- **Impression Rate**: 1.6M vs 16M/day (10x gap)
- **CvR**: 20.7% vs 22.2%

**Root Cause**: MFF ads are sparse - no assets, no trust signals. Users have limited engagement options and insufficient confidence to message unknown businesses.

---

## The Solution

Build two complementary features:

### 1. Co-triggering with Other Assets
**What**: Show sitelinks, callouts, favicon alongside MFF
**Why**: 88% of MFF impressions have assets available but unused
**Impact**: +15-25% CTR (more click targets, richer ad experience)

### 2. Trust Signals
**What**: Display verification, ratings, response time in ad
**Why**: Users hesitate to message businesses they don't trust
**Impact**: +10-15% CvR (build confidence, reduce friction)

---

## Expected Results (6 Months Post-Launch)

| Metric | Current | Target | Improvement |
|--------|---------|--------|-------------|
| **CTR** | 4.2% | 6.3-7.1% | +50-70% 🎯 |
| **CvR** | 20.7% | 24.8-26.2% | +20-27% 🎯 |
| **Impression Rate** | 1.6M/day | 2.0M/day | +25% 🎯 |
| **Competitive Gap vs LTA** | 4x behind | 2.4x behind | **40% closed** 🎯 |

**Revenue Impact**: ~$39M incremental annual revenue (back-of-envelope)

---

## Why These Two Features?

### Strategic Fit
- **Assets** = Breadth (more engagement options) → Improves CTR
- **Trust Signals** = Depth (more confidence) → Improves CvR
- Together they address MFF's full-funnel weakness

### Data-Backed
- **88%** of MFF impressions have assets available
- User research: **78%** want reviews, **65%** want response time info
- Competitive analysis: All major platforms (Facebook, LinkedIn, Yelp) show trust signals

### Feasible
- No new infrastructure needed (use existing asset & GMB systems)
- 5-month timeline with phased rollout (de-risked)
- $260K one-time cost, $140K/year ongoing → **150x ROI**

---

## Implementation Plan

### Timeline: 5 Months (20 Weeks)

**Phase 1: Foundation** (Weeks 1-4)
- Build shared UI framework, serving pipeline, A/B test infra
- Validate data availability (assets, trust signals)
- Privacy/Legal approval

**Phase 2: Assets** (Weeks 5-12)
- Build & launch co-triggering with sitelinks, callouts, favicon
- A/B test, iterate, 100% rollout by Week 10
- Expected: +24% CTR 🚀

**Phase 3: Trust Signals** (Weeks 5-16, overlaps with Phase 2)
- Build data pipeline (response time, ratings, verification)
- Launch trust signal display in ads
- 100% rollout by Week 16
- Expected: +12% CvR 🚀

**Phase 4: Optimization** (Weeks 19-20+)
- ML-powered asset & signal selection
- Continuous iteration based on learnings

---

## Key Decisions Needed (Week 1)

### 1. Asset Prioritization
**Recommendation**: Launch with Sitelinks + Callouts + Favicon (V1)
**Rationale**: High coverage, proven impact, low risk

### 2. Trust Signal Prioritization
**Recommendation**: Verification + Star Rating + Response Time (V1)
**Rationale**: Top 3 impact drivers per user research

### 3. Advertiser Opt-Out?
**Recommendation**: Allow opt-out for response time/volume, NOT for ratings/verification
**Rationale**: Balance advertiser control with user benefit (ratings are public info)

### 4. Launch Timing
**Recommendation**: Sequential (Assets Week 10, Trust Week 16) NOT simultaneous
**Rationale**: De-risk, isolate impact, faster iteration

---

## Risks & Mitigation

| Risk | Mitigation |
|------|------------|
| **Privacy blocks trust signals** | Start privacy review immediately; fallback with fewer signals |
| **Latency exceeds budget** | Aggressive caching, async fetching, fallback to base MFF |
| **Low data coverage** (<30%) | Validate early (Week 2); deprioritize low-coverage signals |
| **No CTR/CvR lift in experiments** | Iterate on UI/selection logic; strong competitive benchmarks suggest success |

---

## Success Criteria

### Go/No-Go for Launch (After A/B Test)
Must achieve:
- ✅ CTR lift ≥10% (Assets) or CvR lift ≥10% (Trust) - stat sig p<0.05
- ✅ No regression in other key metrics
- ✅ Latency <70ms added
- ✅ Privacy/Legal approval

### Post-Launch Success (6 Months)
Celebrate if we achieve:
- 🎉 CTR ≥6.0%
- 🎉 CvR ≥23%
- 🎉 Impression rate ≥2.0M/day
- 🎉 Advertiser NPS +10 points

---

## What We Need to Proceed

### Resources
- **Team**: 6.5 FTE (1 PM, 3 Eng, 1 UX, 1 Analyst, 1 Data Eng)
- **Budget**: $260K one-time, $140K/year ongoing
- **Timeline**: 5 months to launch, ongoing optimization

### Approvals
- [ ] Privacy/Legal sign-off (Week 1-2)
- [ ] Engineering resourcing (Week 1)
- [ ] UX design review (Week 1)
- [ ] Stakeholder alignment (Week 1 kickoff)

---

## Deliverables (This Exploration)

1. ✅ **Feature Exploration: Co-triggering Assets** - 40-page detailed spec
2. ✅ **Feature Exploration: Trust Signals** - 45-page detailed spec
3. ✅ **Implementation Roadmap** - 30-page project plan with timeline, risks, metrics
4. ✅ **Working Prototype** - Python demo showing core logic

**Total**: 115 pages of comprehensive product documentation

---

## Next Steps (This Week)

1. **Monday**: Review this document with leadership (get alignment)
2. **Tuesday**: Schedule stakeholder kickoff for Week 1
3. **Wednesday**: Begin privacy review process
4. **Thursday**: Assign engineering resources, create project tracking
5. **Friday**: Kick off data availability analysis (Week 2 deliverable)

---

## Why This Matters

MFF is a strategic format for messaging-focused advertisers. Currently, it's underperforming and at risk of low adoption. By investing in these two features, we can:

1. **Close the gap with LTA** - Make MFF competitive on CTR/CvR
2. **Unlock scale** - Better performance → more serving → faster learning
3. **Improve ROI for advertisers** - Higher CvR = more leads per dollar
4. **Enhance user experience** - Richer ads, more trust signals
5. **Increase Google revenue** - More clicks, better ads = more revenue

**This is the right investment at the right time.**

---

## Questions?

**PM Contact**: [Your Name]
**Email**: [Your Email]
**Project Docs**: See `feature-exploration-*.md` and `mff-improvement-implementation-roadmap.md`

---

**Let's build MFF 2.0 and make messaging ads the best format for lead generation! 🚀**
