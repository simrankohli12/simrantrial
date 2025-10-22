"""
Message Forward Format (MFF) 2.0 - Prototype Implementation
Demonstrates Co-triggering Assets + Trust Signals

This is a conceptual prototype showing how the features would work.
Not production-ready, but illustrates the architecture.
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


# ============================================================================
# DATA MODELS
# ============================================================================

class AssetType(Enum):
    """Types of assets that can co-trigger with MFF"""
    SITELINK = "sitelink"
    CALLOUT = "callout"
    STRUCTURED_SNIPPET = "structured_snippet"
    FAVICON = "favicon"
    LOCATION = "location"


class TrustSignalType(Enum):
    """Types of trust signals"""
    VERIFICATION_BADGE = "verification"
    STAR_RATING = "rating"
    RESPONSE_TIME = "response_time"
    MESSAGE_VOLUME = "message_volume"
    OPERATING_HOURS = "operating_hours"


@dataclass
class Asset:
    """Represents an ad asset (sitelink, callout, etc.)"""
    asset_id: str
    asset_type: AssetType
    text: str
    url: Optional[str] = None  # For clickable assets like sitelinks
    status: str = "ENABLED"

    def is_compatible_with_mff(self) -> bool:
        """Check if this asset can be shown with MFF"""
        # Call extensions conflict with message-primary intent
        incompatible_types = []
        return self.asset_type not in incompatible_types and self.status == "ENABLED"


@dataclass
class TrustSignal:
    """Represents a trust signal for an advertiser"""
    signal_type: TrustSignalType
    value: str
    display_text: str
    data_freshness_hours: int = 24

    def should_display(self) -> bool:
        """Only show positive trust signals"""
        # Don't show negative signals (e.g., low ratings, slow response)
        if self.signal_type == TrustSignalType.STAR_RATING:
            rating = float(self.value)
            return rating >= 3.5
        elif self.signal_type == TrustSignalType.RESPONSE_TIME:
            # Only show if response time is reasonable
            minutes = self._parse_response_time(self.value)
            return minutes < 1440  # Less than 24 hours
        return True

    def _parse_response_time(self, value: str) -> int:
        """Parse response time string to minutes"""
        # Simplified parser - production would be more robust
        if "minutes" in value:
            return int(value.split()[0])
        elif "hours" in value:
            return int(value.split()[0]) * 60
        return 0


@dataclass
class MFFAd:
    """Message Forward Format Ad"""
    ad_id: str
    campaign_id: str
    advertiser_id: str

    # Core MFF components
    business_name: str
    headline: str  # Non-clickable
    image_url: str
    message_cta_text: str = "Message Us"

    # Optional components
    call_cta_text: Optional[str] = None
    phone_number: Optional[str] = None

    # NEW: Co-triggered assets
    assets: List[Asset] = None

    # NEW: Trust signals
    trust_signals: List[TrustSignal] = None

    def __post_init__(self):
        if self.assets is None:
            self.assets = []
        if self.trust_signals is None:
            self.trust_signals = []


# ============================================================================
# ASSET SELECTION LOGIC
# ============================================================================

class AssetSelector:
    """Selects optimal assets to co-trigger with MFF"""

    def __init__(self, max_sitelinks: int = 4, max_callouts: int = 6):
        self.max_sitelinks = max_sitelinks
        self.max_callouts = max_callouts

    def select_assets(self, available_assets: List[Asset],
                     device_type: str = "mobile") -> List[Asset]:
        """
        Select best asset combination for this MFF ad

        Args:
            available_assets: All assets available for this ad
            device_type: "mobile" or "desktop" (affects layout constraints)

        Returns:
            List of selected assets
        """
        selected = []

        # Filter for MFF-compatible assets
        compatible = [a for a in available_assets if a.is_compatible_with_mff()]

        # Priority order: Favicon > Sitelinks > Callouts > Structured Snippets

        # 1. Favicon (always show if available)
        favicon = self._find_asset(compatible, AssetType.FAVICON)
        if favicon:
            selected.append(favicon)

        # 2. Sitelinks (high CTR impact)
        sitelinks = self._find_assets(compatible, AssetType.SITELINK)
        num_sitelinks = 2 if device_type == "mobile" else 4
        selected.extend(sitelinks[:num_sitelinks])

        # 3. Callouts (informational, good for context)
        callouts = self._find_assets(compatible, AssetType.CALLOUT)
        num_callouts = 3 if device_type == "mobile" else 6
        selected.extend(callouts[:num_callouts])

        # 4. Structured Snippets (if space allows)
        snippets = self._find_assets(compatible, AssetType.STRUCTURED_SNIPPET)
        if snippets:
            selected.append(snippets[0])  # Max 1 structured snippet

        return selected

    def _find_asset(self, assets: List[Asset], asset_type: AssetType) -> Optional[Asset]:
        """Find first asset of given type"""
        for asset in assets:
            if asset.asset_type == asset_type:
                return asset
        return None

    def _find_assets(self, assets: List[Asset], asset_type: AssetType) -> List[Asset]:
        """Find all assets of given type"""
        return [a for a in assets if a.asset_type == asset_type]


# ============================================================================
# TRUST SIGNAL SELECTION LOGIC
# ============================================================================

class TrustSignalSelector:
    """Selects optimal trust signals to display"""

    def select_signals(self, available_signals: List[TrustSignal],
                      max_signals: int = 3) -> List[TrustSignal]:
        """
        Select top trust signals based on priority and impact

        Priority order (based on expected impact):
        1. Star Rating (highest CTR/CvR impact)
        2. Verification Badge (trust + credibility)
        3. Response Time (reduces CvR friction)
        4. Message Volume (social proof)
        5. Operating Hours (helpful context)
        """
        # Filter for displayable signals
        displayable = [s for s in available_signals if s.should_display()]

        # Priority-based selection
        priority_order = [
            TrustSignalType.STAR_RATING,
            TrustSignalType.VERIFICATION_BADGE,
            TrustSignalType.RESPONSE_TIME,
            TrustSignalType.MESSAGE_VOLUME,
            TrustSignalType.OPERATING_HOURS,
        ]

        selected = []
        for signal_type in priority_order:
            signal = self._find_signal(displayable, signal_type)
            if signal:
                selected.append(signal)
                if len(selected) >= max_signals:
                    break

        return selected

    def _find_signal(self, signals: List[TrustSignal],
                    signal_type: TrustSignalType) -> Optional[TrustSignal]:
        """Find signal of given type"""
        for signal in signals:
            if signal.signal_type == signal_type:
                return signal
        return None

    def calculate_trust_score(self, signals: List[TrustSignal]) -> int:
        """
        Calculate overall trust score (0-100)

        Scoring:
        - Verification: 0-30 points
        - Ratings: 0-30 points
        - Responsiveness: 0-25 points
        - Popularity: 0-15 points
        """
        score = 0

        for signal in signals:
            if signal.signal_type == TrustSignalType.VERIFICATION_BADGE:
                score += 30  # Full points for verified

            elif signal.signal_type == TrustSignalType.STAR_RATING:
                rating = float(signal.value)
                score += int((rating / 5.0) * 30)

            elif signal.signal_type == TrustSignalType.RESPONSE_TIME:
                minutes = signal._parse_response_time(signal.value)
                if minutes < 30:
                    score += 25
                elif minutes < 240:  # 4 hours
                    score += 20
                elif minutes < 1440:  # 24 hours
                    score += 10

            elif signal.signal_type == TrustSignalType.MESSAGE_VOLUME:
                # Assume value is "X messages/week"
                volume = int(signal.value.split()[0])
                if volume >= 500:
                    score += 15
                elif volume >= 200:
                    score += 10
                elif volume >= 50:
                    score += 5

        return min(score, 100)


# ============================================================================
# AD RENDERING
# ============================================================================

class MFFRenderer:
    """Renders MFF ads with assets and trust signals"""

    def __init__(self):
        self.asset_selector = AssetSelector()
        self.trust_selector = TrustSignalSelector()

    def render(self, ad: MFFAd, available_assets: List[Asset],
              available_signals: List[TrustSignal],
              device_type: str = "mobile") -> str:
        """
        Render complete MFF ad with assets and trust signals

        Returns:
            HTML string (simplified for prototype)
        """
        # Select assets and signals
        selected_assets = self.asset_selector.select_assets(
            available_assets, device_type
        )
        selected_signals = self.trust_selector.select_signals(
            available_signals, max_signals=3
        )

        # Build HTML
        html_parts = []
        html_parts.append('<div class="mff-ad">')

        # Business name with favicon
        favicon = next((a for a in selected_assets if a.asset_type == AssetType.FAVICON), None)
        if favicon:
            html_parts.append(f'  <div class="business-name">')
            html_parts.append(f'    <img src="{favicon.url}" class="favicon" />')
            html_parts.append(f'    <span>{ad.business_name}</span>')
            html_parts.append(f'  </div>')
        else:
            html_parts.append(f'  <div class="business-name">{ad.business_name}</div>')

        # Image
        html_parts.append(f'  <img src="{ad.image_url}" class="ad-image" />')

        # Non-clickable headline
        html_parts.append(f'  <div class="headline">{ad.headline}</div>')

        # NEW: Trust signals
        if selected_signals:
            html_parts.append('  <div class="trust-signals">')
            for signal in selected_signals:
                icon = self._get_signal_icon(signal.signal_type)
                html_parts.append(f'    <span class="trust-signal">')
                html_parts.append(f'      {icon} {signal.display_text}')
                html_parts.append(f'    </span>')
            html_parts.append('  </div>')

        # CTAs
        html_parts.append('  <div class="ctas">')
        html_parts.append(f'    <button class="message-cta primary">{ad.message_cta_text}</button>')
        if ad.call_cta_text:
            html_parts.append(f'    <button class="call-cta secondary">{ad.call_cta_text}</button>')
        html_parts.append('  </div>')

        # NEW: Sitelinks
        sitelinks = [a for a in selected_assets if a.asset_type == AssetType.SITELINK]
        if sitelinks:
            html_parts.append('  <div class="sitelinks">')
            for sitelink in sitelinks:
                html_parts.append(f'    <a href="{sitelink.url}" class="sitelink">{sitelink.text}</a>')
            html_parts.append('  </div>')

        # NEW: Callouts
        callouts = [a for a in selected_assets if a.asset_type == AssetType.CALLOUT]
        if callouts:
            html_parts.append('  <div class="callouts">')
            callout_texts = [c.text for c in callouts]
            html_parts.append(f'    • {" • ".join(callout_texts)}')
            html_parts.append('  </div>')

        html_parts.append('</div>')

        return '\n'.join(html_parts)

    def _get_signal_icon(self, signal_type: TrustSignalType) -> str:
        """Get emoji/icon for trust signal type"""
        icons = {
            TrustSignalType.VERIFICATION_BADGE: "✓",
            TrustSignalType.STAR_RATING: "★",
            TrustSignalType.RESPONSE_TIME: "⏱",
            TrustSignalType.MESSAGE_VOLUME: "📊",
            TrustSignalType.OPERATING_HOURS: "🕐",
        }
        return icons.get(signal_type, "•")


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

def create_sample_ad() -> MFFAd:
    """Create sample MFF ad"""
    return MFFAd(
        ad_id="ad_12345",
        campaign_id="camp_67890",
        advertiser_id="adv_11111",
        business_name="Joe's Plumbing",
        headline="Emergency Plumbing Services - 24/7 Available",
        image_url="https://example.com/plumber.jpg",
        message_cta_text="Message Us",
        call_cta_text="Call",
        phone_number="+1-555-0123"
    )


def create_sample_assets() -> List[Asset]:
    """Create sample assets"""
    return [
        Asset("favicon_1", AssetType.FAVICON, "", "https://example.com/favicon.ico"),
        Asset("sitelink_1", AssetType.SITELINK, "Emergency Service", "https://example.com/emergency"),
        Asset("sitelink_2", AssetType.SITELINK, "Pricing", "https://example.com/pricing"),
        Asset("sitelink_3", AssetType.SITELINK, "Service Areas", "https://example.com/areas"),
        Asset("sitelink_4", AssetType.SITELINK, "About Us", "https://example.com/about"),
        Asset("callout_1", AssetType.CALLOUT, "Licensed & Insured"),
        Asset("callout_2", AssetType.CALLOUT, "Same-Day Service"),
        Asset("callout_3", AssetType.CALLOUT, "Free Estimates"),
        Asset("callout_4", AssetType.CALLOUT, "10+ Years Experience"),
    ]


def create_sample_trust_signals() -> List[TrustSignal]:
    """Create sample trust signals"""
    return [
        TrustSignal(
            TrustSignalType.VERIFICATION_BADGE,
            "true",
            "Verified Business"
        ),
        TrustSignal(
            TrustSignalType.STAR_RATING,
            "4.7",
            "★★★★☆ 4.7 (189 reviews)"
        ),
        TrustSignal(
            TrustSignalType.RESPONSE_TIME,
            "45 minutes",
            "Usually responds in minutes"
        ),
        TrustSignal(
            TrustSignalType.MESSAGE_VOLUME,
            "120 messages/week",
            "Very Popular"
        ),
    ]


def demo():
    """Demonstrate the MFF 2.0 prototype"""
    print("=" * 60)
    print("MFF 2.0 PROTOTYPE DEMO")
    print("=" * 60)
    print()

    # Create components
    ad = create_sample_ad()
    assets = create_sample_assets()
    signals = create_sample_trust_signals()

    # Render ad
    renderer = MFFRenderer()

    print("RENDERING MOBILE AD:")
    print("-" * 60)
    html_mobile = renderer.render(ad, assets, signals, device_type="mobile")
    print(html_mobile)
    print()

    print("=" * 60)
    print("RENDERING DESKTOP AD:")
    print("-" * 60)
    html_desktop = renderer.render(ad, assets, signals, device_type="desktop")
    print(html_desktop)
    print()

    # Calculate trust score
    trust_selector = TrustSignalSelector()
    trust_score = trust_selector.calculate_trust_score(signals)
    print("=" * 60)
    print(f"TRUST SCORE: {trust_score}/100")
    print("=" * 60)
    print()

    # Show selected components
    asset_selector = AssetSelector()
    selected_assets = asset_selector.select_assets(assets, device_type="desktop")
    selected_signals = trust_selector.select_signals(signals)

    print("SELECTED ASSETS:")
    for asset in selected_assets:
        print(f"  - {asset.asset_type.value}: {asset.text}")
    print()

    print("SELECTED TRUST SIGNALS:")
    for signal in selected_signals:
        print(f"  - {signal.signal_type.value}: {signal.display_text}")
    print()


if __name__ == "__main__":
    demo()
