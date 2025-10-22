# Feature Exploration: Co-triggering MFF with Other Ad Assets

**Feature ID**: MFF-005
**Priority**: P1
**Effort**: Large (L)
**Target Metrics**: CTR +15-25%, Impression Quality +30%
**Owner**: Product Lead - Google Search Ads Messaging
**Status**: Exploration Phase
**Last Updated**: October 22, 2025

---

## Executive Summary

Enable Message Forward Format (MFF) ads to co-trigger with existing Google Ads assets (sitelinks, callouts, structured snippets, favicon) to create additional click targets and improve user experience. This addresses the 4x CTR gap between MFF (4.2%) and LTA Unicard (17.2%).

**Key Insight**: 88% of MFF-eligible impressions already have other assets available but currently unused.

---

## Problem Statement

### Current State
- MFF shows only: Image + Non-clickable headline + Message CTA + Optional additional CTAs
- Other proven high-CTR assets (sitelinks, callouts, etc.) are available but not rendered
- Users have limited interaction options compared to traditional search ads

### Impact
- Lower CTR (4.2%) vs standard search ads with full assets
- Reduced ad real estate utilization
- Missed revenue opportunity from additional click targets

### User Pain Points
- **Users**: Limited options to explore business offerings before committing to message
- **Advertisers**: Lower engagement despite having valuable assets configured
- **Google**: Suboptimal revenue per impression

---

## Solution Overview

### What We're Building
A co-triggering framework that intelligently selects and renders compatible assets alongside the base MFF format, creating a richer ad experience with multiple engagement paths.

### Key Principles
1. **Asset Compatibility**: Not all assets work with non-clickable headline format
2. **Visual Hierarchy**: Message CTA remains primary, assets are complementary
3. **Performance-Driven**: Serve asset combinations that maximize CTR
4. **Responsive Design**: Adapts to available screen real estate
5. **Advertiser Control**: Respect asset-level targeting and scheduling

---

## Feature Requirements

### Must-Have (V1)

#### 1. Asset Selection Logic
**User Story**: As a serving system, I need to intelligently select which assets to show with MFF based on availability, compatibility, and predicted performance.

**Acceptance Criteria**:
- [ ] Identify all available assets for a given ad/campaign at impression time
- [ ] Filter assets by compatibility with MFF format
- [ ] Rank assets by predicted incremental CTR contribution
- [ ] Select optimal asset combination within size constraints
- [ ] Respect asset-level scheduling, targeting, and status rules

**Asset Compatibility Matrix**:
| Asset Type | Compatible with MFF? | Rationale | Priority |
|------------|---------------------|-----------|----------|
| **Sitelinks** | ✅ Yes | Additional click targets, high CTR lift | P0 |
| **Callouts** | ✅ Yes | Non-clickable, adds context | P0 |
| **Structured Snippets** | ✅ Yes | Non-clickable, informative | P1 |
| **Favicon** | ✅ Yes | Trust signal, brand recognition | P0 |
| **Price Extensions** | ⚠️ Maybe | Requires UI adaptation | P2 |
| **Promotion Extensions** | ⚠️ Maybe | Requires UI adaptation | P2 |
| **Call Extensions** | ❌ No | Conflicts with message-primary intent | - |
| **Location Extensions** | ✅ Yes | Valuable for local businesses | P1 |

#### 2. UI Layout System
**User Story**: As a user viewing MFF ads, I want to see additional helpful information without visual clutter, so I can make informed engagement decisions.

**Acceptance Criteria**:
- [ ] Design responsive layout that accommodates 0-4 sitelinks
- [ ] Position callouts below message CTA without overlapping
- [ ] Integrate favicon next to business name/domain
- [ ] Maintain visual hierarchy: Image > Headline > Message CTA > Assets
- [ ] Ensure touch targets meet minimum size requirements (48x48dp mobile)
- [ ] Gracefully degrade when assets unavailable

**Layout Variants**:

```
┌─────────────────────────────────────────┐
│  [Favicon] Business Name                │
│  ─────────────────────────────────────  │
│  ┌───────────────────────────────────┐  │
│  │                                   │  │
│  │      Image (16:9)                 │  │
│  │                                   │  │
│  └───────────────────────────────────┘  │
│                                         │
│  Non-clickable headline text            │
│  ─────────────────────────────────────  │
│  [📱 Message Us]  [📞 Call]             │
│  ─────────────────────────────────────  │
│  🔗 Sitelink 1  |  🔗 Sitelink 2        │
│  🔗 Sitelink 3  |  🔗 Sitelink 4        │
│  ─────────────────────────────────────  │
│  • Callout 1 • Callout 2 • Callout 3   │
│  • Structured: Category 1, Item 2, ... │
└─────────────────────────────────────────┘
```

#### 3. Click Tracking & Attribution
**User Story**: As a product analyst, I need granular click tracking to understand which assets drive engagement.

**Acceptance Criteria**:
- [ ] Track clicks on each asset type separately
- [ ] Attribute conversions to specific asset clicks vs message CTA
- [ ] Log asset IDs with impression events
- [ ] Enable A/B testing of asset combinations

#### 4. Serving Integration
**User Story**: As an ad serving system, I need to efficiently retrieve and render assets with MFF within latency budgets.

**Acceptance Criteria**:
- [ ] Asset fetching completes within existing serving SLA (<100ms)
- [ ] Graceful degradation if asset fetch times out
- [ ] Caching strategy for frequently shown assets
- [ ] No increase in serving errors

### Should-Have (V2)

#### 5. ML-Driven Asset Optimization
- [ ] Train model to predict optimal asset combinations per query
- [ ] Personalize asset selection based on user signals
- [ ] A/B test asset presence/absence dynamically

#### 6. Asset Performance Reporting
- [ ] Advertiser-facing dashboard showing asset-level CTR
- [ ] Recommendations for underperforming assets
- [ ] Benchmarking vs other MFF advertisers

#### 7. Location Extension Integration
- [ ] Show distance to business location
- [ ] "Get Directions" CTA
- [ ] Operating hours indicator

### Nice-to-Have (V3)

#### 8. Dynamic Asset Generation
- [ ] Auto-generate callouts from landing page content
- [ ] Suggest sitelinks based on site structure
- [ ] A/B test generated vs manual assets

#### 9. Promotion Extensions Support
- [ ] Adapt UI for promotional badges
- [ ] Urgency indicators (limited time offers)

---

## Technical Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Ad Serving Pipeline                      │
└─────────────────────────────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────┐
│  MFF Eligibility Check (existing)                           │
│  - Has message goal?                                        │
│  - Has AIE/GMB image?                                       │
│  - No pinned headlines? (may be removed per other ideas)   │
└─────────────────────────────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────┐
│  NEW: Asset Co-trigger Module                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ 1. Asset Fetcher                                       │ │
│  │    - Query asset store for campaign/ad                 │ │
│  │    - Filter by status, scheduling, targeting           │ │
│  │    - Timeout: 50ms                                     │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ 2. Compatibility Filter                                │ │
│  │    - Apply MFF compatibility rules                     │ │
│  │    - Check for conflicts (e.g., call ext vs msg)       │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ 3. Asset Selector (ML-powered in V2)                   │ │
│  │    - Rank assets by predicted CTR lift                 │ │
│  │    - Select optimal combination                        │ │
│  │    - Respect size constraints                          │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ 4. Layout Engine                                       │ │
│  │    - Generate responsive HTML/CSS                      │ │
│  │    - Position assets per device type                   │ │
│  │    - Apply brand guidelines                            │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────┐
│  Ad Rendering (Front-end)                                   │
│  - Render MFF with selected assets                          │
│  - Attach click handlers                                    │
│  - Log impression with asset metadata                       │
└─────────────────────────────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────┐
│  Click Tracking & Attribution                               │
│  - Log click events with asset_id, position                 │
│  - Route to appropriate landing page/action                 │
│  - Update CTR models                                        │
└─────────────────────────────────────────────────────────────┘
```

### Data Models

#### AssetCoTriggerConfig
```proto
message AssetCoTriggerConfig {
  bool enable_sitelinks = 1;
  bool enable_callouts = 2;
  bool enable_structured_snippets = 3;
  bool enable_favicon = 4;
  bool enable_location_extension = 5;

  // Asset selection strategy
  enum SelectionStrategy {
    MOST_AVAILABLE = 0;  // Show all available up to limit
    ML_OPTIMIZED = 1;    // Use ML model to select best combo
    ADVERTISER_PRIORITY = 2;  // Respect advertiser-set priorities
  }
  SelectionStrategy strategy = 6;

  // Constraints
  int32 max_sitelinks = 7 [default = 4];
  int32 max_callouts = 8 [default = 6];
  int32 max_structured_snippets = 9 [default = 1];
}
```

#### MFFImpressionLog (Extended)
```proto
message MFFImpressionLog {
  // Existing fields...
  string ad_id = 1;
  string campaign_id = 2;
  string query = 3;

  // NEW: Asset tracking
  repeated string triggered_asset_ids = 10;
  repeated AssetType triggered_asset_types = 11;
  int32 num_sitelinks_shown = 12;
  int32 num_callouts_shown = 13;
  bool favicon_shown = 14;

  // Asset selection metadata
  AssetSelectionStrategy strategy_used = 15;
  float predicted_ctr_lift = 16;  // ML model prediction
}
```

#### ClickEvent (Extended)
```proto
message ClickEvent {
  // Existing fields...
  string click_id = 1;
  string ad_id = 2;

  // NEW: Asset attribution
  enum ClickTarget {
    MESSAGE_CTA = 0;
    CALL_CTA = 1;
    SITELINK = 2;
    LOCATION_EXTENSION = 3;
    IMAGE = 4;
  }
  ClickTarget target = 10;

  optional string asset_id = 11;  // If clicked on asset
  optional int32 asset_position = 12;  // Position in list (for sitelinks)
}
```

### Performance Considerations

**Latency Budget**:
- Asset fetch: 50ms (parallel with image fetch)
- Selection logic: 5ms
- Layout rendering: 10ms client-side
- **Total added latency**: <65ms

**Caching Strategy**:
- Cache asset metadata for 5 minutes (high QPS campaigns)
- Cache layout templates indefinitely
- Serve stale assets if fresh fetch times out

**Fallback Behavior**:
- If asset fetch fails → render base MFF (no assets)
- If layout rendering fails → render base MFF
- Log errors but don't block ad serving

---

## UI/UX Design Considerations

### Visual Hierarchy
1. **Primary**: Message CTA button (largest, highest contrast)
2. **Secondary**: Image, Business name + favicon
3. **Tertiary**: Sitelinks (clear click targets)
4. **Quaternary**: Callouts, structured snippets (informational)

### Accessibility
- [ ] Sufficient color contrast (WCAG AA: 4.5:1)
- [ ] Screen reader labels for all assets
- [ ] Keyboard navigation support
- [ ] Touch target minimum 48x48dp

### Responsive Breakpoints
- **Mobile (<600px)**: Stack sitelinks vertically, show 2-4
- **Tablet (600-1024px)**: 2x2 sitelink grid, full callouts
- **Desktop (>1024px)**: 4 horizontal sitelinks, expanded callouts

### Animation & Interaction
- Subtle hover states on sitelinks (color shift, underline)
- No animations that delay ad rendering
- Instant click response (<100ms visual feedback)

---

## Experimentation Plan

### Phase 1: Asset Availability Analysis (Week 1-2)
**Goal**: Validate 88% asset availability claim

**Method**:
- Log analysis of MFF-eligible impressions
- Count available assets by type
- Segment by campaign type, vertical, advertiser size

**Success Criteria**:
- Confirm >80% have at least 2 asset types available
- Identify most common asset combinations

### Phase 2: Static A/B Test (Week 3-6)
**Goal**: Measure incremental CTR from assets

**Method**:
- **Control**: Base MFF (no assets)
- **Treatment A**: MFF + Sitelinks + Favicon
- **Treatment B**: MFF + Sitelinks + Callouts + Favicon
- **Traffic Split**: 33% / 33% / 33%

**Metrics**:
- Primary: CTR (expect +15-25% lift)
- Secondary: CvR, CPC, Click Split
- Guardrail: Serving latency <65ms added, error rate <0.1%

**Success Criteria**:
- CTR lift ≥10% (stat sig p<0.05)
- No degradation in CvR
- Latency within budget

### Phase 3: ML-Optimized Selection (Week 7-12)
**Goal**: Beat static asset selection with ML

**Method**:
- Train CTR prediction model on Phase 2 data
- Features: query, assets available, user signals, context
- Online learning: update model daily
- **Control**: Static selection (best from Phase 2)
- **Treatment**: ML-optimized selection

**Metrics**:
- Primary: CTR improvement vs static selection
- Model metrics: AUC, calibration

**Success Criteria**:
- ML selection beats static by ≥5%
- Model latency <5ms p99

---

## Success Metrics

### Primary KPIs
| Metric | Baseline (MFF) | Target | Measurement Window |
|--------|---------------|--------|-------------------|
| CTR | 4.2% | 5.5% (+31%) | 30 days post-launch |
| Impression Rate | 1.6M/day | 1.8M/day (+12%) | 30 days |

### Secondary KPIs
| Metric | Baseline | Target | Notes |
|--------|----------|--------|-------|
| CvR | 20.7% | ≥20.7% (no regression) | Guardrail metric |
| CPC | $1.68 | ≤$1.68 | Guardrail metric |
| Click Split | 0.24 | 0.30 (+25%) | More sitelink clicks |
| Asset Click Share | 0% | 20-30% | New metric |

### Leading Indicators
- Asset availability per impression: >1.5 assets/impression
- Asset render success rate: >99%
- Added serving latency: <65ms p95

### Advertiser Satisfaction
- Survey advertisers with MFF + assets enabled
- Target: ≥4.0/5.0 satisfaction score
- Track support ticket volume (expect initial spike, then decrease)

---

## Risks & Mitigation

### Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Asset fetch increases latency beyond budget | High | Medium | Aggressive timeouts, caching, async fetching |
| Layout breaks on edge-case asset combos | Medium | Medium | Extensive device/browser testing, fallback to base MFF |
| Click tracking attribution bugs | Medium | Low | Comprehensive integration tests, gradual rollout |
| Increased serving costs | Medium | High | Optimize asset queries, cache aggressively |

### Product Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Cluttered UI reduces message CTA clicks | High | Medium | Careful visual hierarchy, A/B test variations |
| Advertisers confused by asset performance data | Low | High | Clear documentation, dashboard tooltips |
| Sitelink destinations conflict with message intent | Medium | Low | Compatibility rules, advertiser best practices |
| No incremental CTR lift (experiment fails) | Critical | Low | Phase 1 validation, iterate based on data |

### Business Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Cannibalizes clicks from other ad formats | Medium | Medium | Monitor overall ad CTR, click distribution |
| Sales team unprepared to pitch new format | Low | Medium | Sales enablement materials, internal beta |
| Legal/privacy concerns with asset data usage | High | Low | Privacy review, respect user data policies |

---

## Dependencies

### Internal Teams
- **Ads Serving**: Integration into serving pipeline
- **UI Engineering**: Layout rendering, responsive design
- **ML/Modeling**: CTR prediction model (Phase 3)
- **Privacy/Legal**: Review asset data usage
- **Quality/Testing**: Cross-browser, device testing
- **Sales Enablement**: Training materials

### External Dependencies
- **Asset Management System**: Reliable API, <50ms latency
- **Image CDN**: Existing dependency for MFF images
- **Click Tracking Infrastructure**: Capacity for increased event volume

### Technical Dependencies
- No new infrastructure required (use existing ad serving stack)
- May need schema updates to logging pipelines

---

## Open Questions & Decisions Needed

### Q1: Which assets add most value?
**Status**: ⏳ Needs data analysis
**Owner**: Product Analytics
**Decision By**: Week 2
**Options**:
- A) Start with Sitelinks + Favicon (safest)
- B) Include Callouts from V1 (more comprehensive)
- C) Run multivariate test (slower but thorough)

**Recommendation**: Option B - include callouts in V1, they're low-risk and informative

### Q2: What's the ideal sitelink count?
**Status**: ⏳ Needs experimentation
**Owner**: UX Research
**Decision By**: Week 4
**Options**:
- A) 2 sitelinks (minimal clutter)
- B) 4 sitelinks (standard for search ads)
- C) Dynamic based on screen size

**Recommendation**: Option C - 2 on mobile, 4 on desktop

### Q3: Should we allow advertisers to opt-out?
**Status**: ⏳ Needs product decision
**Owner**: Product Lead
**Decision By**: Week 1
**Options**:
- A) Opt-out available (advertiser control)
- B) No opt-out (simplicity, better performance)
- C) Opt-out only during beta

**Recommendation**: Option C - allow opt-out during beta to gather feedback, remove later if adoption is high

### Q4: How to handle asset-level targeting conflicts?
**Example**: Sitelink A targets "New York", ad shows in "California"
**Status**: 🔴 Blocker
**Owner**: Ads Targeting Team
**Decision By**: Week 1
**Options**:
- A) Respect asset-level targeting (complex, may reduce asset availability)
- B) Ignore asset targeting when co-triggered with MFF (simpler, may show irrelevant assets)
- C) Only show assets without targeting restrictions

**Recommendation**: Option A - respect targeting to avoid user confusion

---

## Timeline & Milestones

### Phase 1: Foundation (Weeks 1-6)
- **Week 1**: Finalize scope, design reviews
- **Week 2**: Asset availability analysis, data collection
- **Week 3**: Engineering kickoff, architecture review
- **Week 4-5**: Backend integration (asset fetcher, selector)
- **Week 6**: UI implementation, internal dogfooding

### Phase 2: Experimentation (Weeks 7-12)
- **Week 7-8**: A/B test setup, ramp to 10% traffic
- **Week 9-10**: Monitor metrics, iterate on UI
- **Week 11-12**: Ramp to 50% if successful, prepare launch

### Phase 3: Launch (Weeks 13-14)
- **Week 13**: Full rollout to 100% MFF traffic
- **Week 14**: Monitor stability, gather advertiser feedback

### Phase 4: Optimization (Weeks 15-20)
- **Week 15-18**: ML model development
- **Week 19-20**: ML-powered selection rollout

**Total Timeline**: ~5 months (20 weeks)

---

## Launch Checklist

### Pre-Launch (Week 12)
- [ ] A/B test shows stat sig CTR improvement ≥10%
- [ ] Latency within budget (<65ms added)
- [ ] Privacy/Legal approval obtained
- [ ] Sales team trained
- [ ] Help Center docs published
- [ ] Rollback plan tested

### Launch (Week 13)
- [ ] Gradual rollout: 10% → 25% → 50% → 100%
- [ ] Monitor dashboards every 2 hours
- [ ] On-call rotation staffed 24/7
- [ ] Stakeholder communication plan active

### Post-Launch (Week 14+)
- [ ] Metrics review meeting (Day 7, 14, 30)
- [ ] Advertiser feedback synthesis
- [ ] Bug triage and prioritization
- [ ] Phase 4 (ML optimization) kickoff

---

## Appendix

### A. Competitive Analysis
- **Meta Lead Ads**: Show business info (hours, rating) + CTA - similar trust signal concept
- **Google LTA Unicard**: Full asset suite (sitelinks, callouts, etc.) - our benchmark
- **LinkedIn Lead Gen**: Minimal assets, CTA-focused - closer to current MFF

**Insight**: Full asset suite is table stakes for competitive CTR

### B. Asset Performance Benchmarks (from other formats)
- Sitelinks: +10-15% CTR lift on average
- Callouts: +5-8% CTR lift
- Favicon: +3-5% CTR lift (trust signal effect)
- **Expected combined lift**: 15-25% (accounting for diminishing returns)

### C. User Research Findings
- Survey of 500 users who saw MFF ads (Sept 2025)
- "Would you like to see more information before messaging?" - 73% yes
- "What info would help?" - Top answers: Business hours (45%), Reviews (38%), Services offered (35%), Location (28%)
- **Insight**: Users want more context before committing to message

### D. Technical Spec References
- Asset API Documentation: [internal link]
- MFF Serving Pipeline: [internal link]
- Click Tracking Schema: [internal link]
- Responsive Layout Guidelines: [internal link]

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | Oct 22, 2025 | PM Lead | Initial draft |

---

**Next Steps**:
1. Review with stakeholders (Eng, UX, Legal)
2. Finalize asset priority decisions (Q1, Q2, Q3, Q4)
3. Kickoff Week 1 activities
