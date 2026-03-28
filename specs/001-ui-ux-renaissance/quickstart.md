# Quickstart: UI/UX Renaissance - Cyber Theme Implementation

**Created**: 2026-03-18
**Feature**: UI/UX Renaissance - Cyber Theme Overhaul
**Branch**: 001-ui-ux-renaissance

---

## Overview

This guide helps developers quickly set up and test the cyber-theme implementation for the Physical AI Docusaurus textbook platform.

---

## Prerequisites

- Node.js 20.x
- npm or yarn
- Modern browser (Chrome, Firefox, Safari, Edge - latest version)

---

## 1. Install Dependencies

```bash
cd docusaurus-textbook
npm install
```

**Verify Installation**:
```bash
npm list tailwindcss
npm list @docusaurus/core
```

---

## 2. Verify Font Files

Ensure font files are present in `docusaurus-textbook/static/fonts/`:
- `Inter-Regular.woff2`
- `Inter-Bold.woff2`
- `JetBrainsMono-Regular.woff2`
- `JetBrainsMono-Bold.woff2`

If missing, download from:
- Inter: https://rsms.me/inter/
- JetBrains Mono: https://www.jetbrains.com/lp/mono/

---

## 3. Start Development Server

```bash
cd docusaurus-textbook
npm start
```

**Expected Output**:
```
[SUCCESS] Docusaurus website is running at: http://localhost:3000/
```

---

## 4. Test Cyber-Theme Components

### Test Homepage Hero
```
Navigate to: http://localhost:3000/
Expected: Split-screen hero with floating 3D cards, neon glow buttons
```

### Test Mission Timeline
```
Navigate to: http://localhost:3000/roadmap
Expected: Vertical timeline with animated progress nodes
```

### Test Bento Box Dashboard
```
Navigate to: http://localhost:3000/profile
Expected: Tactical HUD layout with GPU/Robot stats in grid
```

### Test Immersive Auth Pages
```
Navigate to: http://localhost:3000/login
Navigate to: http://localhost:3000/signup
Expected: Full-screen glassmorphic forms (no navbar/footer)
```

### Test Robotic Chat Widget
```
Navigate to any page and open chat
Expected: Glowing pulse icon when AI is "thinking"
```

---

## 5. Test Animations

**Floating Animation**:
```bash
# Open browser DevTools > Console
document.querySelector('.cyber-card').style.animation = 'float 3s ease-in-out infinite'
# Expected: Card floats up and down smoothly
```

**Neon Glow**:
```bash
# Hover over any cyber-button
# Expected: Neon glow effect with 0.2s transition
```

**Scanline Effect**:
```bash
# Hover over primary CTA button
# Expected: Horizontal scanline sweeps across button
```

---

## 6. Test Accessibility

**Keyboard Navigation**:
```
1. Press Tab to navigate through interactive elements
2. Verify visible focus indicators (cyan outline)
3. Press Enter to activate buttons
4. Verify all actions accessible via keyboard
```

**Screen Reader Testing**:
```bash
# Enable screen reader (NVDA/JAWS on Windows, VoiceOver on Mac)
# Navigate through page
# Expected: All interactive elements properly announced
```

**Contrast Check**:
```bash
# Install axe DevTools extension
# Run automated accessibility audit
# Expected: No contrast violations
```

---

## 7. Test Browser Compatibility

**Modern Browsers** (should show full effects):
- Chrome 76+
- Firefox 103+
- Safari 9+
- Edge 79+

**Older Browsers** (should degrade gracefully):
- IE11: Solid backgrounds instead of backdrop blur
- Older Firefox: No backdrop-filter, solid fallback

**Test Command**:
```bash
# Use BrowserStack or local VMs
# Verify glassmorphic effects degrade gracefully
# Verify all content remains accessible
```

---

## 8. Performance Testing

**Chrome DevTools Performance**:
```
1. Open DevTools > Performance tab
2. Record while scrolling through homepage
3. Verify 60 FPS (no frame drops)
4. Check for layout thrashing (should be none)
```

**Lighthouse Audit**:
```bash
# Open DevTools > Lighthouse
# Run audit (all categories)
# Expected scores:
# - Performance: 90+
# - Accessibility: 95+
# - Best Practices: 90+
# - SEO: 90+
```

**Animation Performance**:
```bash
# DevTools > Rendering tab
# Enable "Paint flashing"
# Scroll through page
# Expected: Minimal paint rectangles (only on animated elements)
```

---

## 9. Custom CSS Utilities

**Available Classes**:

```css
/* Glassmorphic Components */
.glass-panel        /* Semi-transparent card with blur */
.glass-input        /* Glassmorphic input field */
.glass-button       /* Glass button with hover effects */

/* Neon Effects */
.neon-text          /* Glowing text effect */
.neon-border        /* Glowing border */
.neon-glow          /* Full neon glow box shadow */

/* Cyber Components */
.cyber-button       /* Futuristic button with scanline */
.cyber-card         /* 3D floating card */
.cyber-badge        /* Neon badge */

/* Layout */
.tactical-hud       /* Dashboard grid layout */
.mission-timeline   /* Vertical timeline */
.split-screen       /* Hero split layout */

/* Animations */
.animate-glow       /* Pulsing glow animation */
.animate-float      /* Floating animation */
.animate-pulse-cyan /* Cyan pulse for loading */
.animate-scanline   /* Scanline sweep effect */
```

**Usage Example**:
```jsx
<div className="glass-panel cyber-card animate-float">
  <h2 className="neon-text">Cyber Card</h2>
  <button className="cyber-button neon-glow">
    Click Me
  </button>
</div>
```

---

## 10. Tailwind Custom Classes

**Available in tailwind.config.js**:

```javascript
// Colors
text-neon-blue
text-neon-orange
bg-glass-bg
border-neon-cyan

// Shadows
shadow-neon-blue
shadow-neon-orange
shadow-glass

// Backdrop
backdrop-blur-md
backdrop-blur-sm

// Animations
animate-glow
animate-float
animate-pulse
```

**Usage Example**:
```jsx
<button className="bg-neon-blue text-black shadow-neon-blue hover:shadow-neon-orange transition-all duration-200">
  Neon Button
</button>
```

---

## 11. Common Issues & Solutions

### Issue: Backdrop blur not working
**Solution**: Check browser support, fallback to solid background
```css
/* Fallback is automatic via @supports query */
```

### Issue: Animations janky on mobile
**Solution**: Reduce animation complexity
```css
@media (max-width: 768px) {
  .animate-float {
    animation: none;
    transform: none;
  }
}
```

### Issue: Fonts not loading
**Solution**: Check font file paths, verify preload links
```html
<link rel="preload" href="/fonts/Inter-Regular.woff2" as="font" crossorigin>
```

### Issue: Focus indicators not visible
**Solution**: Check CSS specificity, ensure focus-visible is used
```css
button:focus-visible {
  outline: 2px solid #00FFFF !important;
}
```

---

## 12. Development Workflow

### Adding New Components

1. **Create component** in `src/components/UI/`
2. **Add styles** to `src/css/custom.css`
3. **Add Tailwind config** if needed
4. **Test accessibility** with axe DevTools
5. **Test performance** in DevTools
6. **Document** in this quickstart

### Modifying Existing Styles

1. **Find component** in `src/css/custom.css`
2. **Make changes** following existing patterns
3. **Test** across all breakpoints
4. **Verify** no accessibility regressions
5. **Update** this quickstart if adding utilities

---

## 13. Testing Checklist

Before deploying:

- [ ] All animations run at 60 FPS
- [ ] All text passes contrast audit (4.5:1 minimum)
- [ ] All interactive elements keyboard accessible
- [ ] Focus indicators visible on all elements
- [ ] Backdrop blur degrades gracefully on older browsers
- [ ] Fonts load without FOIT
- [ ] Mobile responsive (test at 320px, 768px, 1024px, 1920px)
- [ ] Reduced motion respected (`prefers-reduced-motion`)
- [ ] Lighthouse scores: Performance 90+, Accessibility 95+
- [ ] Cross-browser tested (Chrome, Firefox, Safari, Edge)

---

## 14. Next Steps

After setup:

1. **Review design system** in `research.md`
2. **Check component documentation** in `src/components/UI/`
3. **Run full test suite**: `npm test`
4. **Deploy to staging** for user testing
5. **Gather feedback** on visual design
6. **Iterate** based on user feedback

---

## Support

For issues or questions:
- Check `research.md` for design decisions
- Review `custom.css` for utility classes
- Check browser DevTools for CSS issues
- Contact design team for visual feedback
