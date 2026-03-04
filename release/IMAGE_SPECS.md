# Play Store Image Specifications (Text-Only)

- **Title:** Adaptive Icon (Foreground)
- **Purpose:** Android adaptive icon foreground layer.
- **Dimensions:** 432 × 432 px source (safe zone centered for mask).
- **Primary Elements:**
  - Stylized tarot card glyph.
  - Crescent moon + star accent.
  - Minimal line details for readability at small sizes.
- **Style:** Flat vector, high contrast, modern mystical aesthetic.
- **Text Content:** None.
- **Notes:** Foreground must work with circle/squircle masks and avoid clipped corners.

- **Title:** Adaptive Icon (Background)
- **Purpose:** Android adaptive icon background layer.
- **Dimensions:** 432 × 432 px source.
- **Primary Elements:**
  - Deep indigo to violet vertical gradient.
  - Subtle grain/noise texture (very low opacity).
- **Style:** Clean gradient background.
- **Text Content:** None.
- **Notes:** Keep background simple to avoid visual clutter with foreground layer.

- **Title:** Legacy App Icon
- **Purpose:** Launcher icon for legacy surfaces and listing usage.
- **Dimensions:** 512 × 512 px.
- **Primary Elements:**
  - Combined adaptive foreground + background composition.
  - Centered tarot glyph.
- **Style:** Crisp, high-contrast, recognizable at 48 px.
- **Text Content:** None.
- **Notes:** Export PNG with transparent-safe edge handling.

- **Title:** Google Play Feature Graphic
- **Purpose:** Required promotional banner for Play listing.
- **Dimensions:** 1024 × 500 px.
- **Primary Elements:**
  - App name "Tarot Teller" centered-left.
  - Abstract celestial background motif (stars/constellation lines).
  - Subtle tarot card silhouette on right side.
- **Style:** Premium, modern mystical; dark purple palette with gold highlights.
- **Text Content:** "Tarot Teller" and optional subtitle "Offline Tarot Readings".
- **Notes:** Avoid busy UI screenshots; prioritize branding and legibility.

- **Title:** Phone Screenshot 1 — Home
- **Purpose:** Showcase primary navigation.
- **Dimensions:** 1080 × 1920 px (portrait).
- **Primary Elements:**
  - Home screen buttons: Daily Draw, 3-Card, Yes/No, History, Settings.
  - Clean spacing and high-contrast controls.
- **Style:** Simple, modern mobile UI.
- **Text Content:** Actual in-app labels only.
- **Notes:** No debug overlays; show real app UI state.

- **Title:** Phone Screenshot 2 — Spread Configuration
- **Purpose:** Show question/seed/reversal controls.
- **Dimensions:** 1080 × 1920 px (portrait).
- **Primary Elements:**
  - Spread label, optional question input, seed input.
  - Reversals toggle and draw action.
- **Style:** Consistent typography and spacing with screenshot 1.
- **Text Content:** "Shuffle + Draw" and relevant field hints.
- **Notes:** Ensure keyboard is hidden in final capture.

- **Title:** Phone Screenshot 3 — Reading Result
- **Purpose:** Demonstrate interpretation output and actions.
- **Dimensions:** 1080 × 1920 px (portrait).
- **Primary Elements:**
  - Drawn card names with upright/reversed orientation.
  - Short + long interpretation text.
  - "Save to History" and "Share text" actions.
- **Style:** Readable text hierarchy with sufficient contrast.
- **Text Content:** Real example reading content from app.
- **Notes:** Avoid personal data; use sample question if needed.
