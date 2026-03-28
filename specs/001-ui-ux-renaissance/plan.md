# Implementation Plan: Phase 6 UI/UX Renaissance - Cyber Theme Overhaul

**Branch**: `001-ui-ux-renaissance` | **Date**: 2026-03-18 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-ui-ux-renaissance/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a comprehensive cyber-theme overhaul for the Physical AI Docusaurus textbook platform. The implementation includes custom CSS animations (glow, float, pulse-cyan), glassmorphic components (glass-panel, neon-border, cyber-button), redesigned navigation with admin badges, split-screen hero layout, mission log timeline for roadmap, bento box grid for dashboard, and immersive auth pages. All styling uses Tailwind CSS with Inter font for UI and JetBrains Mono for system labels.

## Technical Context

**Language/Version**: TypeScript 5.6, React 19, JavaScript ES2022
**Primary Dependencies**: Tailwind CSS 3+, Docusaurus 3.9+, React 19
**Storage**: N/A (frontend-only feature)
**Testing**: Visual regression testing, cross-browser compatibility testing
**Target Platform**: Web browsers (Chrome, Firefox, Safari, Edge - latest 2 versions)
**Project Type**: Web application (frontend only)
**Performance Goals**: 60 FPS animations, <100ms interaction response, <3s page load time
**Constraints**: Maintain accessibility (WCAG 2.1 AA), support reduced motion preferences, graceful degradation for older browsers
**Scale/Scope**: 10+ pages redesigned, 20+ custom CSS classes, 10+ custom animations

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate 1: Library-First Principle
**Status**: ✅ PASS
- Custom CSS utilities are self-contained and reusable
- Component designs are modular and can be composed
- No hardcoded values - all using CSS custom properties

### Gate 2: CLI Interface (if applicable)
**Status**: N/A
- This is a frontend UI feature, not a CLI tool

### Gate 3: Test-First (NON-NEGOTIABLE)
**Status**: ✅ COMMITTED
- Visual regression tests before implementation
- Cross-browser testing checklist
- Accessibility validation for all components

### Gate 4: Integration Testing
**Status**: ✅ COMMITTED
- Test navbar integration across all pages
- Verify auth pages work without navbar/footer
- Test chatbot HUD integration with existing chat system

### Gate 5: Observability & Simplicity (YAGNI)
**Status**: ✅ PASS
- CSS custom properties for easy theming
- Documented design system in custom.css
- Start with core animations, extend as needed

## Project Structure

### Documentation (this feature)

```text
specs/001-ui-ux-renaissance/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (N/A for UI feature)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (N/A for UI feature)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
docusaurus-textbook/
├── src/
│   ├── css/
│   │   ├── custom.css              # Custom CSS utilities and components
│   │   └── tailwind.css            # Tailwind imports
│   ├── theme/
│   │   ├── Navbar.tsx              # Redesigned navbar component
│   │   ├── Footer.tsx              # Redesigned footer component
│   │   ├── Root.tsx                # Auth provider wrapper
│   │   └── ChatBot/
│   │       └── ChatWidget.tsx      # Redesigned robotic assistant
│   ├── components/
│   │   ├── Admin/
│   │   │   ├── HealthCard.tsx      # Existing component
│   │   │   └── ...
│   │   ├── UI/
│   │   │   ├── GlassPanel.tsx      # NEW: Reusable glass panel
│   │   │   ├── NeonButton.tsx      # NEW: Button with glow effects
│   │   │   ├── CyberCard.tsx       # NEW: 3D floating card
│   │   │   └── MissionStep.tsx     # NEW: Timeline step component
│   │   └── Homepage/
│   │       ├── HeroSection.tsx     # NEW: Split-screen hero
│   │       └── FeatureCards.tsx    # NEW: 3D feature cards
│   └── pages/
│       ├── index.tsx               # Homepage with hero
│       ├── roadmap.tsx             # Mission log timeline
│       ├── profile.tsx             # Bento box dashboard
│       ├── login.tsx               # Immersive auth page
│       └── signup.tsx              # Immersive auth page
├── tailwind.config.js              # Extended with custom animations
└── docusaurus.config.ts            # Theme configuration
```

**Structure Decision**: Using existing Docusaurus structure with new UI components in `src/components/UI/`. Custom CSS in `src/css/custom.css` with Tailwind extensions in `tailwind.config.js`.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Custom animations | Core to cyber-theme aesthetic | Standard Tailwind animations insufficient for neon glow effects |
| Immersive auth pages | Focus user attention during signup | Adding navbar would distract from conversion goal |
| Bento box layout | Modern, scannable dashboard design | Simple grid doesn't convey "tactical HUD" aesthetic |

## Phase 0: Research & Discovery

### Unknowns to Resolve

1. **Browser Support for Backdrop Filter**: Which browsers support backdrop-filter and what's the fallback strategy?
   - Research: Can I Use compatibility data, graceful degradation patterns
   - Decision: Use backdrop-filter with solid background fallback

2. **Animation Performance**: How to ensure 60 FPS animations on mid-range devices?
   - Research: CSS animation best practices, GPU acceleration techniques
   - Decision: Use transform/opacity only, avoid layout thrashing

3. **Accessibility with Dark Mode**: How to maintain WCAG contrast ratios in dark theme?
   - Research: Dark mode accessibility guidelines, contrast ratio calculators
   - Decision: Test all color combinations, maintain 4.5:1 minimum contrast

4. **Font Loading Strategy**: How to load Inter and JetBrains Mono without FOUT?
   - Research: Font loading strategies, font-display options
   - Decision: Use font-display: swap with local fallbacks

### Research Dispatch

**Task 1**: Research backdrop-filter browser support and fallback strategies
- Focus: CSS backdrop-filter compatibility, graceful degradation
- Output: research.md section on browser support

**Task 2**: Research CSS animation performance optimization
- Focus: GPU-accelerated properties, will-change usage
- Output: research.md section on animation performance

**Task 3**: Research dark mode accessibility best practices
- Focus: WCAG 2.1 AA compliance, contrast ratios for dark backgrounds
- Output: research.md section on accessibility

**Task 4**: Research font loading strategies for custom fonts
- Focus: font-display options, preload strategies
- Output: research.md section on typography

## Phase 1: Design & Contracts

### Design System (replaces data-model.md for UI feature)

**Custom Animations** (tailwind.config.js):
- `glow`: Pulsing neon glow animation
- `float`: Floating 3D card animation
- `pulse-cyan`: Cyan pulse for loading states
- `scanline`: Horizontal scanline sweep
- `slide-in-up`: Smooth entrance animation

**Utility Classes** (custom.css):
- `.glass-panel`: Semi-transparent card with backdrop blur
- `.neon-border`: Glowing border effect
- `.cyber-button`: Button with hover glow effects
- `.tactical-hud`: Dashboard grid layout
- `.mission-timeline`: Vertical timeline styles

### Component Contracts

**Navbar Component**:
- Props: user (object), isAdmin (boolean), onLogout (function)
- Renders: Transparent navbar with backdrop blur, cyan bottom border
- Admin badge: Neon orange badge for admin users

**Hero Section Component**:
- Props: title (string), subtitle (string), ctaText (string)
- Layout: Split-screen (text left, UI preview right)
- Animations: Floating elements, neon glow on CTA

**Mission Step Component**:
- Props: status ('completed' | 'current' | 'locked'), title (string), date (string)
- Renders: Timeline node with color based on status
- Animation: Pulse effect for current step

### Quickstart (quickstart.md)

**For Developers**:
1. Install dependencies: `npm install`
2. Start dev server: `npm start`
3. View components: Navigate to `/`, `/roadmap`, `/profile`

**For Testing**:
1. Test animations: Check 60 FPS on target devices
2. Test accessibility: Run axe DevTools audit
3. Test responsive: Mobile, tablet, desktop breakpoints

## Phase 2: Implementation Tasks

*Note: Tasks will be created by /sp.tasks command*

### CSS Architecture Tasks (anticipated)

1. Define custom animations in tailwind.config.js
2. Create glass-panel utility class in custom.css
3. Create neon-border utility class in custom.css
4. Create cyber-button component styles
5. Add scanline animation for hover states

### Component Tasks (anticipated)

1. Redesign Navbar with user dropdown and admin badge
2. Create HeroSection component with split-screen layout
3. Create FeatureCards component with 3D floating effect
4. Create MissionTimeline component for roadmap
5. Create BentoBox grid for profile/dashboard page
6. Create immersive Login page (no navbar/footer)
7. Create immersive Signup page (no navbar/footer)
8. Redesign ChatBot as Robotic Assistant HUD

### Integration Tasks (anticipated)

1. Update homepage to use new HeroSection
2. Update roadmap page to use MissionTimeline
3. Update profile page to use BentoBox layout
4. Update auth pages to be full-screen immersive
5. Integrate robotic chat widget

## Success Metrics

- **SC-001**: All animations run at 60 FPS on mid-range devices
- **SC-002**: All pages pass WCAG 2.1 AA contrast audit
- **SC-003**: Page load time under 3 seconds on 3G connection
- **SC-004**: Backdrop blur degrades gracefully on unsupported browsers
- **SC-005**: All interactive elements have visible focus states

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Performance issues on low-end devices | High | Use will-change sparingly, test on target devices |
| Accessibility violations | High | Audit with axe DevTools, manual keyboard testing |
| Browser compatibility issues | Medium | Graceful degradation, feature detection |
| Font loading delays | Low | Use font-display: swap, preload critical fonts |

---

**Next Step**: Run `/sp.tasks` to break this plan into actionable implementation tasks.
