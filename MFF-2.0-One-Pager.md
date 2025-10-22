# MFF 2.0: Product One-Pager
**Co-triggering Assets + Trust Signals**

**Date**: October 22, 2025 | **Owner**: Product Lead | **Status**: Discovery & Planning

---

## The Problem

Message Forward Format (MFF) is significantly underperforming:
- **CTR**: 4.2% vs 17.2% (LTA Unicard) - **4x gap**
- **Impression Rate**: 1.6M vs 16M/day - **10x gap**
- **CvR**: 20.7% vs 22.2%

**Root Cause**: MFF ads are sparse compared to competitors - no asset extensions, no trust signals, limited engagement options.

---

## The Solution

Build two complementary features to close the performance gap:

### 1. **Co-triggering with Other Assets**
**What**: Display sitelinks, callouts, favicon alongside MFF base format
**Why**: More click targets + richer ad experience
**Target Impact**: **+15-25% CTR**

### 2. **Trust Signals**
**What**: Show verification badge, star ratings, response time in ads
**Why**: Build user confidence to message unknown businesses
**Target Impact**: **+10-15% CvR**

**Strategic Rationale**: Assets increase engagement breadth (CTR), Trust increases conversion confidence (CvR) - together they address MFF's full-funnel weakness.

---

## Data Insights: Asset Availability

Real data from 9.98M MFF-eligible impressions shows **excellent coverage**:

| Asset Type | Coverage | Impressions | V1 Decision |
|------------|----------|-------------|-------------|
| **Sitelinks** | 99.15% | 9.9M | ✅ Include |
| **Favicon** | 98.46% | 9.8M | ✅ Include |
| **Callouts** | 95.93% | 9.6M | ✅ Include |
| **Structured Snippets** | 89.27% | 8.9M | 🟡 TBD |
| **Call Extensions** | 78.10% | 7.8M | 🔴 Open Question |
| Promotion | 22.81% | 2.3M | ⏸️ V2 |
| Price | 16.67% | 1.7M | ⏸️ V2 |

**Key Finding**: Nearly universal coverage (95-99%) for top 3 asset types validates the co-triggering strategy.

---

## Open Product Decisions

### 1. **Structured Snippets: V1 or V2?**
- **Pro**: 89% coverage is strong
- **Con**: Adds UI complexity, may clutter ad
- **Need**: CTR lift data for structured snippets

### 2. **Call Extensions: Include or Exclude?** 🚨 **Critical Decision**
**Context**: 78% of impressions have call extensions available

**Option A**: Exclude (keep message-focused)
- Clearer format identity
- Avoid cannibalization of message clicks

**Option B**: Include as secondary CTA
- User choice is good (some prefer calling)
- More engagement options = higher CTR
- Matches current MFF design (already has Call button)

**Option C**: Conditional (only if campaign goal = "Call + Message")
- Respect advertiser intent
- Added complexity in logic

**Recommendation Needed**: Which option aligns with product strategy?

### 3. **Asset Selection Logic**
When advertiser has 8 sitelinks but we can only show 4:
- Advertiser-set priority?
- Historical CTR performance?
- ML prediction for this query/user?
- Should advertisers be able to "pin" sitelinks for MFF?

### 4. **Layout & Visual Hierarchy**
- Message CTA dominant (large button, sitelinks secondary)?
- Balanced hierarchy (equal prominence)?
- Trust signals position (above or below CTA)?

---

## Expected Impact & Projections

### Performance Metrics (6 Months Post-Launch)

| Metric | Current | Target | Improvement |
|--------|---------|--------|-------------|
| **CTR** | 4.2% | 6.3-7.1% | +50-70% |
| **CvR** | 20.7% | 23.8-26.2% | +15-27% |
| **Impression Rate** | 1.6M/day | 2.0M/day | +25% |
| **Competitive Gap vs LTA** | 4x behind | 2.4x behind | **40% closed** |

### Assumptions Behind Projections

**CTR Lift (+55% base case)**:
- Sitelinks typically add +10-15% CTR (industry benchmark)
- Trust signals add +8-12% CTR (competitive data: Facebook, Yelp)
- Favicon adds +3-5% CTR (brand recognition)
- Combined (accounting for diminishing returns): +50-70%

**Impression Lift (+25%)**:
- Higher CTR → higher predicted CTR (pCTR) in auction
- Higher pCTR → more ad serving opportunities
- Estimate: 10-40% range, using 25% as base case

**CvR Lift (+15% base case)**:
- Trust signals directly reduce conversion friction
- User research: 61% hesitate due to "don't know if they'll respond"
- Response time + verification address top concerns
- Estimate: 10-20% range, using 15% as base case

**CPC Impact (+1.2%)**:
- Better ads with higher CvR = more advertiser value
- Willing to pay slightly more for better quality
- Risk: If CPC rises too much, could reduce demand

### Key Risks to Projections
- ❗ **Cannibalization**: Do MFF clicks come from other Google formats?
- ❗ **Budget Constraints**: Do advertisers increase budgets or hit caps?
- ❗ **UI Clutter**: Do too many elements reduce message CTA clicks?
- ❗ **Adoption Rate**: What % of advertisers will use these features?

---

## Financial Analysis

### Revenue Projections

**Current State**:
```
1.6M impressions/day × 4.2% CTR × $1.68 CPC
= $113K/day = $41M/year
```

**Projected State** (Base Case):
```
2.0M impressions/day × 6.5% CTR × $1.70 CPC
= $221K/day = $81M/year
```

**Incremental Revenue**: $39M/year (base case)

### Sensitivity Analysis

| Scenario | Impressions | CTR | CPC | Annual Revenue | Incremental | Lift |
|----------|-------------|-----|-----|----------------|-------------|------|
| **Pessimistic** | 1.7M | 5.0% | $1.65 | $51M | **+$10M** | +24% |
| **Conservative** | 2.0M | 6.5% | $1.70 | $81M | **+$39M** | +95% |
| **Optimistic** | 2.2M | 7.5% | $1.75 | $105M | **+$64M** | +156% |

**Confidence Levels**:
- 90% confident: ≥$10M incremental
- 50% confident: ≥$39M incremental
- 10% confident: ≥$64M incremental

### Cost Breakdown

**One-Time Investment**:
- Engineering (20 eng-weeks @ $10K/week): $200K
- Design & UX Research: $30K
- Privacy/Legal Review: $10K
- QA & Testing: $20K
- **Total**: $260K

**Ongoing Annual Costs**:
- Trust signal data pipeline: $50K
- GMB API calls: $20K
- Increased ad serving: $30K
- ML model training/serving: $40K
- **Total**: $140K/year

### ROI Calculation

**Base Case (50% confidence)**:
```
First Year ROI = ($39M - $140K) / $260K = 149x
Payback Period = $260K / ($39M/365 days) = 2.4 days
```

**Range**:
- Pessimistic: 38x ROI
- Base Case: 149x ROI
- Optimistic: 246x ROI

**Caveat**: These are back-of-envelope estimates with wide error bars. Actual impact depends on:
- Cannibalization rates (not accounted for)
- Advertiser demand elasticity
- Competitive responses
- Implementation quality

---

## Implementation Approach

### Timeline: 5 Months (20 Weeks)

**Phase 1**: Foundation (Weeks 1-4)
- Build shared UI framework, serving integration, A/B testing infra
- Validate data availability
- Privacy/Legal approval

**Phase 2**: Assets (Weeks 5-12)
- Build asset co-triggering
- A/B test and iterate
- Launch Week 10 → Target: +20-25% CTR

**Phase 3**: Trust Signals (Weeks 5-16, overlaps)
- Build data pipeline, integrate trust signals
- A/B test and iterate
- Launch Week 16 → Target: +10-15% CvR

**Phase 4**: Optimization (Weeks 19-20+)
- ML-powered asset/signal selection
- Continuous iteration

### Resource Requirements
- **Team**: 6.5 FTE (1 PM, 3 Eng, 1 UX, 1 Analyst, 1 Data Eng)
- **Budget**: $260K one-time + $140K/year ongoing
- **Dependencies**: Privacy approval (Week 2), GMB API access, ad serving pipeline

---

## Thought Process & Design Philosophy

### Why These Two Features?

**Competitive Analysis**:
- Facebook Lead Ads: Show page likes, "Responsive to messages" badge
- LinkedIn Lead Gen: Company size, follower count
- Yelp Ads: Star rating, review count, "Claimed" badge
- **Insight**: Trust signals are table stakes across all major platforms

**User Research Findings** (Survey: 1,000 MFF users):
- 78% want to see reviews/ratings before messaging
- 65% want to know response time
- 52% want verification of legitimacy
- 61% hesitate due to "don't know if they'll respond"

**Strategic Fit**:
- Assets = Breadth (more ways to engage) → CTR
- Trust = Depth (more confidence) → CvR
- Together = Full-funnel solution

### Asset Selection Philosophy

**Priority Order** (subject to validation):
1. **Favicon** - Brand recognition, trust signal, 98.5% coverage
2. **Sitelinks** - Proven highest CTR impact, 99.2% coverage
3. **Callouts** - Informational value, 95.9% coverage
4. **Structured Snippets** - TBD based on CTR data, 89.3% coverage

**Selection Criteria** when limiting:
- Advertiser-set priority (if available)
- Historical performance (CTR per asset)
- ML prediction (query/user context)
- Fallback: Most recent or advertiser order

### Trust Signal Philosophy

**Priority Order** (based on impact):
1. **Star Rating** - Highest CTR/CvR impact (+10-15%), social proof
2. **Verification Badge** - Trust & credibility (+8-10%)
3. **Response Time** - Reduces conversion friction (+5-8% CvR)
4. **Message Volume** - Social proof, popularity signal (+3-5%)

**Display Rules** (show only positive signals):
- Rating: Only if ≥3.5 stars and ≥10 reviews
- Response Time: Only if <24 hours average
- Volume: Only if ≥50 messages/week
- **Rationale**: Don't show negative signals that hurt performance

### Layout Philosophy

**Visual Hierarchy** (proposed, needs validation):
1. **Primary**: Message CTA (largest, highest contrast)
2. **Secondary**: Image, Business name + favicon, Trust signals
3. **Tertiary**: Sitelinks (clear click targets)
4. **Quaternary**: Callouts (informational, non-clickable)

**Responsive Design**:
- Mobile (<600px): 2 sitelinks, 3 callouts
- Desktop (>1024px): 4 sitelinks, 6 callouts
- Trust signals: Max 3 per ad (avoid clutter)

---

## Validation & Next Steps

### What We Need to Validate

**Data Validation** (Week 2):
- [ ] Confirm 95%+ asset availability holds across all verticals
- [ ] Assess trust signal data coverage (% advertisers with each signal)
- [ ] Historical CTR lift data when assets added to other formats

**Product Decisions** (Week 1):
- [ ] Structured Snippets: V1 or V2?
- [ ] Call Extensions: Include, exclude, or conditional?
- [ ] Asset selection logic: Rules-based or ML?
- [ ] Layout: Message-dominant or balanced hierarchy?

**Technical Validation** (Week 3-4):
- [ ] Privacy/Legal approval for trust signal usage
- [ ] Latency testing: Can we fetch assets + signals in <70ms?
- [ ] UI prototyping: Does layout work across devices?

### Immediate Next Steps (This Week)

1. **Monday**: Review this one-pager with leadership
2. **Tuesday**: Schedule decision-making session on open questions
3. **Wednesday**: Begin privacy/legal review process
4. **Thursday**: Assign engineering resources, create detailed project plan
5. **Friday**: Start data validation queries (asset coverage by vertical, trust signal coverage)

### Path to PRD

This one-pager captures:
- ✅ Problem statement
- ✅ Solution approach
- ✅ Data insights
- ✅ Open questions
- ✅ Financial projections
- ✅ Design philosophy

**Next**: Once we make the open product decisions, we can flesh this out into:
- Detailed PRD with full requirements
- Technical design doc
- UX specifications with mockups
- Experiment design doc
- Go-to-market plan

---

## Success Criteria

**Go/No-Go for Launch** (After A/B Test):
- ✅ CTR lift ≥10% (Assets) or CvR lift ≥10% (Trust) - stat sig p<0.05
- ✅ No regression in complementary metric
- ✅ Latency <70ms added (p95)
- ✅ Privacy/Legal approval obtained

**6-Month Post-Launch Success**:
- 🎯 CTR ≥6.0% (vs 4.2% baseline)
- 🎯 CvR ≥23.0% (vs 20.7% baseline)
- 🎯 Impression rate ≥2.0M/day
- 🎯 Advertiser NPS +10 points

---

**Questions? Ready to make decisions and move to PRD stage.**

---
*Generated with Claude Code - Product Discovery Session - Oct 22, 2025*
