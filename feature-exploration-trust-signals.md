# Feature Exploration: Trust Signals for MFF

**Feature ID**: MFF-006
**Priority**: P1
**Effort**: Large (L)
**Target Metrics**: CTR +10-15%, CvR +10-15%
**Owner**: Product Lead - Google Search Ads Messaging
**Status**: Exploration Phase
**Last Updated**: October 22, 2025

---

## Executive Summary

Display trust-building signals in Message Forward Format (MFF) ads to increase user confidence and improve both click-through and conversion rates. Trust signals include business verification status, ratings, response time, messaging volume, and other credibility indicators.

**Key Insight**: Users hesitate to message businesses they don't know. Trust signals reduce friction and increase conversion likelihood.

---

## Problem Statement

### Current State
- MFF shows minimal business information (name, image, message CTA)
- No credibility indicators to help users assess business legitimacy
- Users must click and wait for response to evaluate business quality

### Impact
- Lower conversion rates (20.7% vs 22.2% for LTA Unicard)
- User hesitation to message unknown businesses
- Higher bounce rates from low-quality or unresponsive advertisers

### User Pain Points
- **Users**: "Is this business legitimate? Will they respond? Are they well-reviewed?"
- **Advertisers**: High-quality businesses can't differentiate themselves from low-quality ones
- **Google**: Poor experiences with unresponsive businesses damage platform trust

---

## Solution Overview

### What We're Building
A trust signal framework that surfaces verified business information, social proof, and responsiveness indicators directly in the ad, reducing user uncertainty before the first message.

### Key Principles
1. **Authenticity**: Only show verified, accurate information
2. **Relevance**: Display signals most predictive of user satisfaction
3. **Privacy**: Respect user data policies and business privacy
4. **Performance**: No degradation in ad serving latency
5. **Configurability**: Advertisers can control which signals to show

---

## Trust Signal Taxonomy

### Tier 1: High-Impact Signals (Must-Have for V1)

#### 1. Business Verification Badge
**What**: Visual indicator that business identity has been verified
**Source**: Google Business Profile verification status, domain ownership, historical advertiser status
**Display**: ✓ Verified badge next to business name
**Impact**: +8-12% CTR (based on similar verification badges in other products)
**Privacy Risk**: Low (publicly available verification status)

**Verification Levels**:
- **Verified Business**: Has verified GMB, domain, consistent info across sources
- **Established Advertiser**: >6 months advertising history, good standing
- **Domain Verified**: Confirmed domain ownership

**UI Example**:
```
[✓] Joe's Plumbing
Verified Business
```

#### 2. Average Response Time
**What**: How quickly business typically replies to messages
**Source**: Historical message response data from past MFF interactions
**Display**: "Usually responds in <2 hours" / "Responds within a day"
**Impact**: +5-8% CvR (reduces uncertainty about response wait time)
**Privacy Risk**: Low (aggregated data, no PII)

**Response Time Buckets**:
- "Usually responds in minutes" (<30 min average)
- "Usually responds in a few hours" (30min - 4hr)
- "Usually responds within a day" (4hr - 24hr)
- No label if >24hr average (don't show negative signals)

**Data Requirements**:
- Minimum 20 message interactions in past 90 days
- Exclude outliers (>7 days)
- Update weekly

#### 3. Star Ratings
**What**: Aggregate user ratings of the business
**Source**: Google Business Profile ratings, Google Ads reviews, seller ratings
**Display**: ★★★★☆ 4.5 (234 reviews)
**Impact**: +10-15% CTR, +5-10% CvR (strong social proof)
**Privacy Risk**: Low (publicly available ratings)

**Display Rules**:
- Require minimum 10 reviews for display
- Show 0.5-star precision (4.5, not 4.47)
- Link to reviews page on click (optional)
- Only show if rating ≥3.5 stars (don't show negative signals)

#### 4. Messaging Volume Indicator
**What**: Social proof of business popularity via message counts
**Source**: Aggregated MFF message volume (past 30 days)
**Display**: "Receives 100+ messages per week" / "Popular"
**Impact**: +3-5% CTR (popularity signals quality)
**Privacy Risk**: Medium (reveals business performance, use coarse buckets)

**Volume Buckets**:
- "Popular" (50-200 messages/week)
- "Very Popular" (200-500 messages/week)
- "Highly Responsive" (>500 messages/week)
- No label if <50/week (only show positive signals)

### Tier 2: Medium-Impact Signals (Nice-to-Have for V1 or V2)

#### 5. Business Category/Services
**What**: What the business offers
**Source**: GMB categories, ad campaign categories, website scraping
**Display**: "Plumbing Services • 24/7 Emergency"
**Impact**: +2-5% CTR (helps users confirm relevance)
**Privacy Risk**: Low

#### 6. Operating Hours
**What**: Current open/closed status and hours
**Source**: GMB hours, ad scheduling
**Display**: "Open now • Closes at 9 PM" / "Opens tomorrow at 9 AM"
**Impact**: +5-8% CvR (users more likely to message when business is open)
**Privacy Risk**: Low

#### 7. Years in Business
**What**: How long business has been operating
**Source**: GMB creation date, domain registration date, advertising history
**Display**: "Established in 2015" / "10+ years in business"
**Impact**: +3-5% CTR (longevity = credibility)
**Privacy Risk**: Low

#### 8. WhatsApp Business Verification
**What**: For businesses using WhatsApp for messaging, show WA verified badge
**Source**: Scrape whatsapp.com/business or message_url metadata
**Display**: WhatsApp verified badge + business name/avatar from WA
**Impact**: +8-10% CvR (WA users trust verified accounts)
**Privacy Risk**: Medium (requires scraping third-party URL)

**Implementation Complexity**: High
- Need to fetch WA business profile data at serving time
- Handle rate limits, timeouts
- Parse WA HTML/API for verification status

### Tier 3: Advanced Signals (V2+)

#### 9. Customer Testimonials
**What**: Short text reviews from past customers
**Source**: GMB reviews, extracted from website, advertiser-provided
**Display**: "Great service!" - Jane D.
**Impact**: +5-10% CvR (specific social proof)
**Privacy Risk**: Medium (review attribution, user consent)

#### 10. Industry Certifications
**What**: Professional licenses, certifications, affiliations
**Source**: Advertiser-provided, verified against public databases
**Display**: "Licensed & Insured • BBB A+ Rated"
**Impact**: +5-8% CTR (especially high-trust industries: medical, legal, financial)
**Privacy Risk**: Low (publicly verifiable)

#### 11. Price Range Indicator
**What**: Relative price positioning ($ / $$ / $$$)
**Source**: Price extensions, website scraping, GMB price range
**Display**: $$ • Mid-range pricing
**Impact**: +3-5% CvR (sets expectations, reduces price-based bounces)
**Privacy Risk**: Low

---

## Feature Requirements

### Must-Have (V1)

#### 1. Trust Signal Selection Engine
**User Story**: As a serving system, I need to select the most relevant trust signals for each advertiser based on data availability and predicted impact.

**Acceptance Criteria**:
- [ ] For each MFF ad, identify all available trust signals
- [ ] Prioritize signals based on:
  - Data quality (freshness, sample size)
  - Predicted incremental CvR impact
  - Visual layout constraints (max 2-3 signals)
- [ ] Fallback gracefully if data unavailable
- [ ] Respect advertiser opt-outs

**Selection Logic**:
```
IF rating ≥ 4.0 AND review_count ≥ 10:
  SHOW star rating (highest priority)

IF response_time_avg < 4 hours AND message_count ≥ 20:
  SHOW response time

IF verified_status = TRUE:
  SHOW verification badge

IF remaining_space AND message_volume ≥ 50/week:
  SHOW volume indicator

MAX 3 signals per ad (avoid clutter)
```

#### 2. Data Infrastructure
**User Story**: As a data engineer, I need pipelines to compute trust signals at scale with acceptable latency.

**Acceptance Criteria**:
- [ ] **Response Time**: Batch job computes avg response time per advertiser, runs daily
- [ ] **Message Volume**: Streaming aggregation of message counts (30-day rolling window)
- [ ] **Verification Status**: Sync with GMB API daily
- [ ] **Ratings**: Sync with Seller Ratings and GMB API daily
- [ ] All data refreshed within 24 hours
- [ ] Serving latency: trust signals fetched in <30ms (cached)

**Data Freshness**:
| Signal | Update Frequency | Acceptable Staleness |
|--------|-----------------|----------------------|
| Response Time | Daily | 24 hours |
| Message Volume | Hourly | 1 hour |
| Verification Status | Daily | 7 days |
| Star Ratings | Daily | 7 days |

#### 3. UI Integration
**User Story**: As a user viewing an MFF ad, I want to see trust signals prominently without clutter.

**Acceptance Criteria**:
- [ ] Trust signals positioned between headline and message CTA
- [ ] Use icons + short text (e.g., ★ 4.5, ✓ Verified)
- [ ] Responsive design: adapt to screen size
- [ ] Graceful degradation if signals unavailable
- [ ] Accessible: screen reader labels, sufficient contrast

**Layout Example**:
```
┌─────────────────────────────────────────┐
│  [✓] Joe's Plumbing                     │
│  ─────────────────────────────────────  │
│  ┌───────────────────────────────────┐  │
│  │      Image (plumber fixing pipe)  │  │
│  └───────────────────────────────────┘  │
│                                         │
│  Emergency Plumbing Services            │
│  ─────────────────────────────────────  │
│  ★★★★☆ 4.7 (189)  •  Usually responds │
│  in minutes  •  Very Popular            │
│  ─────────────────────────────────────  │
│  [📱 Message Us]  [📞 Call]             │
└─────────────────────────────────────────┘
```

#### 4. Privacy & Compliance
**User Story**: As a privacy lead, I need assurance that trust signals respect user and advertiser privacy.

**Acceptance Criteria**:
- [ ] Privacy review completed
- [ ] No PII displayed (names, specific message content)
- [ ] Advertisers can opt-out of specific signals
- [ ] Data retention policy documented
- [ ] Comply with GDPR, CCPA requirements

**Opt-Out Controls**:
- Advertiser settings: "Don't show my response time" (checkbox)
- Advertiser settings: "Don't show message volume" (checkbox)
- Cannot opt-out of verification badge (it's a trust/quality indicator)

#### 5. Tracking & Measurement
**User Story**: As a product analyst, I need to measure the impact of each trust signal on CTR and CvR.

**Acceptance Criteria**:
- [ ] Log which trust signals shown per impression
- [ ] Track click/conversion rates by signal presence
- [ ] A/B test individual signals
- [ ] Advertiser-facing report: "Your trust score"

**Logging Schema**:
```proto
message TrustSignalImpression {
  string ad_id = 1;
  repeated TrustSignal signals_shown = 2;

  message TrustSignal {
    enum SignalType {
      VERIFICATION_BADGE = 0;
      STAR_RATING = 1;
      RESPONSE_TIME = 2;
      MESSAGE_VOLUME = 3;
      OPERATING_HOURS = 4;
    }
    SignalType type = 1;
    string value = 2;  // e.g., "4.5", "2 hours", "Verified"
  }
}
```

### Should-Have (V2)

#### 6. Advertiser Trust Dashboard
- [ ] Show advertisers their trust score (0-100)
- [ ] Breakdown by signal (verification ✓, rating 4.5/5, response time: excellent)
- [ ] Recommendations to improve (e.g., "Respond 20% faster to improve score")
- [ ] Benchmarking vs competitors

#### 7. Dynamic Trust Signal Optimization
- [ ] ML model predicts best signal combination per user
- [ ] Personalization based on user history (new users see ratings, repeat users see response time)
- [ ] Continuous A/B testing of signal variations

#### 8. WhatsApp Business Integration
- [ ] Scrape WhatsApp URL to fetch business profile
- [ ] Display WA verified badge + business avatar
- [ ] Show WA-specific trust signals (chat encryption notice)

### Nice-to-Have (V3)

#### 9. Real-Time Trust Signals
- [ ] "Available now" indicator (business is online right now)
- [ ] "Responding to messages" live status
- [ ] Current wait time estimate

#### 10. Negative Signal Handling
- [ ] "Slow to respond" warning if avg response >24hr
- [ ] "Low rating" flag if <3.5 stars
- [ ] Option to filter out low-trust advertisers entirely

---

## Technical Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                Trust Signal Data Pipeline                    │
└─────────────────────────────────────────────────────────────┘
                             │
      ┌──────────────────────┼──────────────────────┐
      ↓                      ↓                      ↓
┌──────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ GMB API      │  │ Message Response │  │ Seller Ratings   │
│ - Ratings    │  │ Logger           │  │ API              │
│ - Verified   │  │ - Response times │  │ - Star ratings   │
│ - Hours      │  │ - Message counts │  │ - Review counts  │
└──────────────┘  └──────────────────┘  └──────────────────┘
      │                      │                      │
      └──────────────────────┼──────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│           Trust Signal Aggregation (Daily Batch)             │
│  - Compute avg response times per advertiser                │
│  - Aggregate message volumes (rolling 30 days)              │
│  - Fetch latest ratings, verification status                │
│  - Assign trust score (0-100)                               │
│  - Store in Trust Signal Store                              │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│               Trust Signal Store (Key-Value)                 │
│  Key: advertiser_id                                          │
│  Value: {                                                    │
│    verified: true,                                           │
│    rating: 4.5,                                              │
│    review_count: 234,                                        │
│    avg_response_time_minutes: 45,                            │
│    message_volume_weekly: 120,                               │
│    trust_score: 85,                                          │
│    last_updated: timestamp                                   │
│  }                                                           │
│  TTL: 24 hours (refresh daily)                               │
└─────────────────────────────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────┐
│                   Ad Serving (Real-Time)                     │
│  1. MFF ad selected for impression                           │
│  2. Fetch trust signals from Trust Signal Store (cached)     │
│  3. Select top 2-3 signals based on priority logic           │
│  4. Render ad with signals                                   │
│  5. Log impression with signals shown                        │
│  Latency: <30ms (trust signal fetch cached)                  │
└─────────────────────────────────────────────────────────────┘
```

### Data Models

#### TrustSignalStore
```proto
message TrustSignalData {
  string advertiser_id = 1;

  // Verification
  bool is_verified = 2;
  VerificationType verification_type = 3;
  enum VerificationType {
    NONE = 0;
    DOMAIN_VERIFIED = 1;
    GMB_VERIFIED = 2;
    ESTABLISHED_ADVERTISER = 3;  // 6+ months, good standing
  }

  // Ratings
  optional float star_rating = 4;  // 0.0 - 5.0
  optional int32 review_count = 5;

  // Responsiveness
  optional int32 avg_response_time_minutes = 6;
  optional int32 message_count_last_90_days = 7;  // For confidence

  // Popularity
  optional int32 message_volume_weekly = 8;  // Last 30 days avg

  // Business Info
  optional string business_category = 9;
  optional bool is_open_now = 10;
  optional string operating_hours_today = 11;  // "9 AM - 9 PM"

  // Aggregated Trust Score
  optional int32 trust_score = 12;  // 0-100

  // Metadata
  int64 last_updated_timestamp = 13;
  repeated string opted_out_signals = 14;  // e.g., ["response_time"]
}
```

#### TrustScore Calculation
```python
def calculate_trust_score(data: TrustSignalData) -> int:
    score = 0

    # Verification (0-30 points)
    if data.verification_type == ESTABLISHED_ADVERTISER:
        score += 30
    elif data.verification_type == GMB_VERIFIED:
        score += 25
    elif data.verification_type == DOMAIN_VERIFIED:
        score += 15

    # Ratings (0-30 points)
    if data.review_count >= 10:
        score += (data.star_rating / 5.0) * 30

    # Responsiveness (0-25 points)
    if data.message_count_last_90_days >= 20:
        if data.avg_response_time_minutes < 30:
            score += 25
        elif data.avg_response_time_minutes < 240:  # 4 hours
            score += 20
        elif data.avg_response_time_minutes < 1440:  # 24 hours
            score += 10

    # Popularity (0-15 points)
    if data.message_volume_weekly >= 500:
        score += 15
    elif data.message_volume_weekly >= 200:
        score += 10
    elif data.message_volume_weekly >= 50:
        score += 5

    return min(score, 100)  # Cap at 100
```

---

## UI/UX Design Variations

### Variation A: Inline Text (Recommended)
```
Joe's Plumbing [✓]
★★★★☆ 4.7 (189) • Usually responds in minutes
[📱 Message Us]  [📞 Call]
```
**Pros**: Clean, scannable, familiar pattern
**Cons**: Limited space for multiple signals

### Variation B: Icon Grid
```
Joe's Plumbing
[✓ Verified]  [★ 4.7]  [⚡ Fast Reply]
[📱 Message Us]  [📞 Call]
```
**Pros**: Visual, easy to parse
**Cons**: Takes more vertical space

### Variation C: Expandable Details
```
Joe's Plumbing [ⓘ]  ← Click to expand trust details
[📱 Message Us]  [📞 Call]

→ [Expanded]
Joe's Plumbing
✓ Verified Business
★★★★☆ 4.7 (189 reviews)
⏱ Usually responds in minutes
📊 Very Popular (200+ messages/week)
[📱 Message Us]  [📞 Call]
```
**Pros**: Doesn't add clutter, power users get details
**Cons**: Requires click, most users won't expand

**Recommendation**: **Variation A** for V1 (simplicity, no extra interaction)

---

## Experimentation Plan

### Phase 1: Trust Signal Availability Analysis (Week 1-2)
**Goal**: Understand what % of MFF advertisers have each signal

**Method**:
- Query Trust Signal Store for all MFF advertisers
- Calculate coverage per signal type
- Identify gaps (e.g., 60% have ratings, 30% have response time data)

**Expected Coverage** (estimates):
- Verification status: 80% (most have GMB or domain)
- Star ratings: 40-50% (many small businesses lack reviews)
- Response time: 30% (only if advertiser has used MFF before)
- Message volume: 30% (same as above)

**Decision**: If coverage <30% for any signal, deprioritize for V1

### Phase 2: Single-Signal A/B Tests (Week 3-8)
**Goal**: Measure isolated impact of each trust signal

**Method**:
- Run 4 parallel A/B tests, each testing one signal
- **Test 1**: Star Rating (50% control, 50% show rating if available)
- **Test 2**: Verification Badge (50/50 split)
- **Test 3**: Response Time (50/50 split)
- **Test 4**: Message Volume (50/50 split)
- Duration: 2 weeks each (can run in parallel)

**Metrics**:
- Primary: CTR, CvR
- Secondary: CPC, Click Split
- Segment by: signal quality (e.g., 5-star vs 4-star ads)

**Success Criteria** (per signal):
- CTR lift ≥5% OR CvR lift ≥5%
- Stat sig p<0.05
- No negative impact on advertiser metrics (CPC, conversion value)

**Expected Results**:
- Star rating: +10% CTR, +8% CvR (highest impact)
- Verification: +8% CTR, +5% CvR
- Response time: +3% CTR, +10% CvR (huge CvR impact)
- Volume: +5% CTR, +3% CvR

### Phase 3: Multi-Signal Combination Test (Week 9-12)
**Goal**: Find optimal signal combination

**Method**:
- **Control**: No trust signals (baseline MFF)
- **Treatment A**: Verification + Rating (if available)
- **Treatment B**: Rating + Response Time
- **Treatment C**: All 3 signals (Verification + Rating + Response Time)
- **Traffic Split**: 25% / 25% / 25% / 25%

**Metrics**: Same as Phase 2

**Success Criteria**:
- Best treatment shows ≥15% CTR lift and ≥10% CvR lift vs control
- Identify winning combination for V1 launch

**Expected Winner**: Treatment C (all signals) if no cluttered UI issues

### Phase 4: Rollout (Week 13-16)
- **Week 13**: Gradual rollout 10% → 25% → 50%
- **Week 14**: Monitor stability, gather feedback
- **Week 15-16**: 100% rollout, post-launch monitoring

---

## Success Metrics

### Primary KPIs
| Metric | Baseline (MFF) | Target | Measurement Window |
|--------|----------------|--------|-------------------|
| CTR | 4.2% | 4.8% (+14%) | 30 days post-launch |
| CvR | 20.7% | 23.3% (+12%) | 30 days post-launch |

### Secondary KPIs
| Metric | Baseline | Target | Notes |
|--------|----------|--------|-------|
| Click Split | 0.24 | 0.28 (+17%) | Longer engagement |
| CPC | $1.68 | ≤$1.75 (+4% ok) | Expect slight increase due to better quality |
| Advertiser Satisfaction | Baseline survey | +10 NPS points | Quarterly survey |

### Leading Indicators
- Trust signal availability: ≥70% of impressions show ≥1 signal
- Trust signal render success rate: >99.5%
- Data freshness: <24hr staleness for 95% of data

---

## Risks & Mitigation

### Data Quality Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| Response time data inaccurate | Medium | Require min 20 interactions, exclude outliers, manual QA |
| Ratings out of date | Low | Daily sync with GMB, show last_updated date |
| Verification status false positives | High | Multi-source verification (GMB + domain + history) |

### Product Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| Low trust signals reduce clicks (negative social proof) | High | Only show signals if positive (rating ≥3.5, response <24hr) |
| Advertisers game the system (fake reviews) | Medium | Use Google's existing review fraud detection |
| User expectations set too high | Medium | Use conservative language ("usually responds", not "always") |

### Privacy Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| Message volume reveals business performance | Medium | Use coarse buckets (50-200, not exact count) |
| Response time reveals staffing patterns | Low | Aggregated 90-day average, not real-time |
| Advertiser objects to signal display | Low | Provide opt-out controls in advertiser settings |

---

## Dependencies

### Internal Teams
- **Ads Data**: Response time aggregation pipeline
- **GMB Team**: API access for ratings, verification, hours
- **Privacy/Legal**: Review trust signal usage
- **Seller Ratings Team**: Integrate existing ratings infrastructure
- **UX Research**: Test signal variations with users

### External Dependencies
- **GMB API**: Reliable access, rate limits
- **Message Response Logger**: Accurate timestamp logging
- **WhatsApp (optional)**: Business profile scraping (if we pursue WA integration)

### Technical Dependencies
- Trust Signal Store infrastructure (new key-value store or use existing)
- Daily batch jobs for aggregation (use existing data pipeline framework)
- A/B testing framework (use existing experiment platform)

---

## Open Questions & Decisions Needed

### Q1: What specific trust signals should we prioritize for V1?
**Status**: ⏳ Needs decision
**Owner**: Product Lead
**Decision By**: Week 1
**Options**:
- A) Verification + Rating (safest, highest coverage)
- B) Verification + Rating + Response Time (comprehensive)
- C) Start with just Verification (iterate fast)

**Recommendation**: Option B - all three are high-impact and achievable

### Q2: What are the data sources for each signal?
**Status**: 🟢 Mostly resolved
| Signal | Primary Source | Fallback Source |
|--------|---------------|-----------------|
| Verification | GMB API | Domain WHOIS + advertiser history |
| Ratings | GMB API | Seller Ratings API |
| Response Time | Message Logger | (none - require min data) |
| Volume | Message Logger | (none) |

### Q3: How should trust signals be displayed in the UI?
**Status**: ⏳ Needs UX research
**Owner**: UX Lead
**Decision By**: Week 2
**Recommendation**: See "UI/UX Design Variations" section - lean toward Variation A

### Q4: Should advertisers be able to opt-out of trust signals?
**Status**: ⏳ Needs product decision
**Owner**: Product Lead
**Decision By**: Week 1
**Options**:
- A) Full opt-out (advertisers can hide all signals)
- B) Partial opt-out (can hide volume/response time, but not verification/rating)
- C) No opt-out (trust signals mandatory for transparency)

**Recommendation**: Option B
- **Rationale**: Verification and ratings are public info (user benefit)
- Performance metrics (response time, volume) are business-sensitive (allow opt-out)

### Q5: How to handle negative trust signals (low ratings, slow response)?
**Status**: ⏳ Needs decision
**Owner**: Product Lead
**Decision By**: Week 2
**Options**:
- A) Show all signals honestly (even negative)
- B) Only show positive signals (hide if rating <3.5, response >24hr)
- C) Show all but with explanations ("Working to improve response time")

**Recommendation**: Option B for V1 (positive-only), Option C for V2
- **Rationale**: V1 goal is to lift MFF performance; negative signals hurt CTR/CvR
- V2 can experiment with transparent negative signals to build platform trust

---

## Timeline & Milestones

### Phase 1: Data Pipeline & Infrastructure (Weeks 1-4)
- **Week 1**: Finalize signal prioritization, design reviews
- **Week 2**: Data availability analysis, coverage assessment
- **Week 3**: Build response time aggregation pipeline
- **Week 4**: Build Trust Signal Store, backfill data

### Phase 2: UI Implementation (Weeks 5-7)
- **Week 5**: UI design finalization, prototypes
- **Week 6**: Frontend implementation, responsive layouts
- **Week 7**: Integration with ad serving, internal dogfood

### Phase 3: Experimentation (Weeks 8-12)
- **Week 8-9**: Single-signal A/B tests (parallel)
- **Week 10-11**: Multi-signal combination tests
- **Week 12**: Analyze results, finalize launch config

### Phase 4: Launch (Weeks 13-16)
- **Week 13-14**: Gradual rollout, monitor metrics
- **Week 15**: 100% rollout
- **Week 16**: Post-launch analysis, gather feedback

**Total Timeline**: ~4 months (16 weeks)

---

## Advertiser Enablement

### Advertiser Dashboard: "Your Trust Score"

**Goal**: Help advertisers understand and improve their trust signals

**Features**:
- **Trust Score**: 0-100 overall score with breakdown
- **Signal Status**:
  - ✓ Verified Business (complete)
  - ★ 4.7 Rating (strong)
  - ⏱ Response Time: 1.5 hours (excellent)
  - 📊 Message Volume: 80/week (good)
- **Recommendations**:
  - "You're doing great! 85/100 trust score."
  - "Respond 30 minutes faster to reach 'excellent' tier"
  - "Encourage customers to leave reviews (currently 23)"
- **Benchmarking**:
  - "Your trust score is better than 70% of businesses in your category"

### Help Center Articles
- "What are trust signals?"
- "How to improve your business verification status"
- "How to get more reviews"
- "Understanding your average response time"
- "Trust signal best practices"

### Sales Enablement
- Training deck: "Selling MFF with Trust Signals"
- ROI calculator: "How trust signals improve your ad performance"
- Case studies: Businesses that improved CvR with trust signals

---

## Future Enhancements (Beyond V2)

### Trust Signal Personalization
- Show different signals based on user intent
  - High-intent users → Response time (want fast answers)
  - Browsing users → Ratings (building confidence)
  - Local searches → Operating hours, location

### Real-Time Trust Signals
- "Available now" (business has app open)
- Current wait time estimate based on queue
- Live response rate (last 24 hours)

### Negative Signal Transparency
- Experiment with showing low ratings with context
  - "3.2 stars • Working to improve service"
- Warning labels for consistently unresponsive businesses
  - "This business has slow response times"

### Trust Signal Auctions
- Allow advertisers to "boost" certain trust signals
- Pay extra to highlight verification badge or rating
- Trust signals as ad rank factors

---

## Appendix

### A. Competitive Analysis

| Platform | Trust Signals Shown | Learnings |
|----------|-------------------|-----------|
| **Facebook Lead Ads** | Page likes, follower count, "Responsive to messages" badge | Simple, effective social proof |
| **Meta Messenger Ads** | "Usually responds instantly" | Response time is critical |
| **LinkedIn Lead Gen** | Company size, industry, follower count | B2B-specific signals |
| **Yelp Ads** | Star rating, review count, price range, "Claimed" badge | Rating dominates (shown prominently) |

**Key Insight**: All major platforms show at least one trust signal - it's table stakes.

### B. User Research: What Builds Trust?

**Survey**: 1,000 users who saw MFF ads (Sept 2025)

**Q: "What would make you more likely to message a business?"**
1. Good reviews / high rating (78%)
2. Quick response time (65%)
3. Verified/official business (52%)
4. See how popular they are (38%)
5. Know their hours (34%)

**Q: "What makes you hesitate to message?"**
1. Don't know if they'll respond (61%)
2. Might be a scam / not legitimate (48%)
3. Don't know their quality (45%)
4. Unclear if they're open (22%)

**Insight**: Response time and verification directly address top hesitations.

### C. Trust Signal Impact Estimates (Industry Benchmarks)

Based on similar features in other Google products:

| Signal | Expected CTR Lift | Expected CvR Lift | Confidence |
|--------|------------------|------------------|-----------|
| Star Rating (≥4.0) | +10-15% | +8-12% | High |
| Verification Badge | +5-10% | +5-8% | Medium |
| Response Time (<4hr) | +3-6% | +10-15% | High |
| Message Volume (Popular) | +3-5% | +2-5% | Medium |
| **Combined (All 4)** | **+18-25%** | **+15-20%** | Medium |

Note: Combined impact has diminishing returns (not additive).

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | Oct 22, 2025 | PM Lead | Initial draft |

---

**Next Steps**:
1. Review with stakeholders (Data, Privacy, UX)
2. Data availability deep dive (Week 1)
3. Privacy/legal approval (Week 1)
4. Kickoff data pipeline work (Week 2)
