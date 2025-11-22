# Void Neon Design Language

---

## Overview

This design language channels the visceral, hallucinogenic aesthetic of filmmaker Gaspar Noé (particularly "Enter the Void") into a functional web design system. The core philosophy: create an immersive, psychedelic experience that assaults the senses while maintaining usability.

**Key Principles:**
- Neon colors against deep blacks create maximum contrast
- Everything glows, pulses, and moves subtly
- Layer visual effects to build depth
- Prioritize atmosphere over conventional clarity (while maintaining accessibility)

---

## Color Palette

### Primary Neons
Use these at high saturation for interactive elements, headings, and accents:

| Color Name | Hex Code | Usage |
|------------|----------|-------|
| Electric Magenta | `#FF0080` | Primary brand color, CTAs, main headings |
| Cyber Blue | `#00F0FF` | Secondary color, body text, links |
| Acid Green | `#39FF14` | Success states, accents, tertiary elements |
| Warning Pink | `#FF10F0` | Alerts, special callouts, highlights |
| Toxic Yellow | `#FFFF00` | Warnings, rare accent use only |

### Dark Foundation
Backgrounds must be very dark to make neons pop:

| Color Name | Hex Code | Usage |
|------------|----------|-------|
| Void Black | `#0A0A0A` | Primary background |
| Deep Charcoal | `#1A1A1A` | Card backgrounds, secondary surfaces |
| Shadow Purple | `#1A0F1F` | Subtle background variation |

### Glow Effects
Apply to text and elements for the signature neon aesthetic:

```css
/* Magenta Glow */
box-shadow: 0 0 20px rgba(255, 0, 128, 0.6),
            0 0 40px rgba(255, 0, 128, 0.4),
            0 0 60px rgba(255, 0, 128, 0.2);

/* Cyan Glow */
box-shadow: 0 0 20px rgba(0, 240, 255, 0.6),
            0 0 40px rgba(0, 240, 255, 0.4),
            0 0 60px rgba(0, 240, 255, 0.2);

/* Green Glow */
box-shadow: 0 0 20px rgba(57, 255, 20, 0.6),
            0 0 40px rgba(57, 255, 20, 0.4),
            0 0 60px rgba(57, 255, 20, 0.2);
```

### Color Combinations
- **Never** use more than 2-3 neon colors simultaneously in one section
- Always pair neons with dark backgrounds (never light)
- Use color to create hierarchy: brightest = most important

---

## Typography

### Font Stack

**Primary Font (Body & UI):**
- Space Grotesk (recommended)
- Alternative: Inter, Archivo, Syne
- Fallback: system-ui, sans-serif

**Display Font (Headings & Hero):**
- Bebas Neue (recommended)
- Alternative: Druk, Archivo Black
- Fallback: Impact, sans-serif

### Type Specifications

| Element | Size | Weight | Transform | Letter Spacing |
|---------|------|--------|-----------|----------------|
| Hero H1 | 72-96px | Bold/900 | UPPERCASE | 0.1em |
| H1 | 48-64px | Bold/900 | UPPERCASE | 0.08em |
| H2 | 32-48px | Bold/700 | UPPERCASE | 0.05em |
| H3 | 24-32px | Bold/700 | UPPERCASE | 0.05em |
| Body | 16-18px | Regular/400 | - | 0.02em |
| Small | 12-14px | Regular/400 | - | 0.02em |

### Text Effects

```css
/* Neon text glow (headings) */
text-shadow: 0 0 20px rgba(255, 0, 128, 0.6),
             0 0 40px rgba(255, 0, 128, 0.4);

/* Subtle body text glow */
text-shadow: 0 0 10px rgba(0, 240, 255, 0.4);

/* Flickering animation (use sparingly) */
@keyframes flicker {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.8; }
}
```

### Typography Rules
- Headlines: Always ALL CAPS with aggressive letter spacing
- Body text: Increased line-height (1.6-1.8) for readability
- Never use more than 3 font sizes per page
- Ensure minimum contrast ratio of 4.5:1 for body text

---

## Motion & Animation

### Core Animation Principles

1. **Everything moves** - Static elements feel dead in this aesthetic
2. **Slow and fluid** - Movements should feel dreamlike, not snappy
3. **Continuous loops** - Many animations never stop (pulses, floats)

### Timing Functions

```css
/* Primary easing - elastic feel */
cubic-bezier(0.68, -0.55, 0.265, 1.55)

/* Alternative - smooth ease */
cubic-bezier(0.4, 0, 0.2, 1)

/* Duration guidelines */
--duration-fast: 200ms;
--duration-normal: 400ms;
--duration-slow: 800ms;
--duration-ambient: 2-3s;
```

### Key Animations

**Neon Pulse** (continuous breathing glow)
```css
@keyframes neonPulse {
  0%, 100% {
    box-shadow: 0 0 20px rgba(255, 0, 128, 0.4);
  }
  50% {
    box-shadow: 0 0 40px rgba(255, 0, 128, 0.8);
  }
}
animation: neonPulse 2s infinite;
```

**Float/Drift** (subtle vertical movement)
```css
@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}
animation: float 3s ease-in-out infinite;
```

**Chromatic Aberration** (hover effect)
```css
/* Apply on hover to create RGB split */
.element:hover {
  text-shadow: -2px 0 #FF0080,
               2px 0 #00F0FF;
}
```

**Strobe Flash** (button active state)
```css
@keyframes strobe {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
/* Trigger on click, duration 100ms */
```

**Rotate/Spin** (loading, ambient backgrounds)
```css
@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
animation: rotate 20s linear infinite;
```

### Animation Usage Guidelines
- Hover states: 400-600ms transition
- Page transitions: 800ms
- Ambient effects (pulses, floats): 2-6s
- Loading indicators: 1-2s loops
- Always provide `prefers-reduced-motion` fallback

---

## UI Components

### Buttons

**Primary Button**
```css
.neon-button {
  background: transparent;
  border: 2px solid #FF0080;
  color: #FF0080;
  padding: 16px 40px;
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 700;
  font-size: 18px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  box-shadow: 0 0 20px rgba(255, 0, 128, 0.4),
              inset 0 0 20px rgba(255, 0, 128, 0.1);
  transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.neon-button:hover {
  background: #FF0080;
  color: #0A0A0A;
  box-shadow: 0 0 60px rgba(255, 0, 128, 0.8),
              0 0 100px rgba(255, 0, 128, 0.4);
  transform: translateY(-2px);
}

.neon-button:active {
  animation: strobe 0.1s;
}
```

**Button Variants**
- Primary: Electric Magenta border/fill
- Secondary: Cyber Blue border/fill
- Success: Acid Green border/fill
- Danger: Warning Pink border/fill

**Button States**
- Default: Transparent with glowing border
- Hover: Filled with intense glow
- Active: Quick strobe flash
- Disabled: 40% opacity, no glow
- Loading: Pulsing border animation

---

### Cards

**Base Card Style**
```css
.card {
  background: rgba(26, 26, 26, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 0, 128, 0.5);
  padding: 40px;
  box-shadow: 0 0 40px rgba(255, 0, 128, 0.3);
  transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.card:hover {
  transform: translateY(-8px);
  box-shadow: 0 0 60px rgba(255, 0, 128, 0.6);
  border-color: rgba(255, 0, 128, 0.8);
}
```

**Card Variations**
- Use different neon colors for different card types
- Vary border colors to create visual hierarchy
- Apply subtle float animation to static cards

---

### Form Inputs

**Text Input**
```css
.neon-input {
  background: rgba(26, 26, 26, 0.8);
  border: 1px solid rgba(0, 240, 255, 0.5);
  color: #00F0FF;
  padding: 12px 20px;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 16px;
  transition: all 0.3s;
}

.neon-input::placeholder {
  color: rgba(0, 240, 255, 0.4);
}

.neon-input:focus {
  outline: none;
  border-color: #00F0FF;
  box-shadow: 0 0 30px rgba(0, 240, 255, 0.6);
}
```

**Input States**
- Default: Dim border glow
- Focus: Intense glow expansion
- Error: Red glow with shake animation
- Success: Green glow with checkmark icon
- Disabled: 50% opacity, no interaction

---

### Navigation

**Fixed Header Nav**
```css
nav {
  position: fixed;
  top: 0;
  width: 100%;
  padding: 24px 40px;
  background: rgba(26, 26, 26, 0.6);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 0, 128, 0.3);
  z-index: 1000;
}

nav a {
  color: #00F0FF;
  text-transform: uppercase;
  font-weight: 700;
  letter-spacing: 0.05em;
  position: relative;
}

nav a::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 0;
  height: 2px;
  background: #00F0FF;
  box-shadow: 0 0 10px #00F0FF;
  transition: width 0.4s;
}

nav a:hover::after {
  width: 100%;
}
```

**Navigation Patterns**
- Always use glass morphism (blur + transparency)
- Active state: Neon underline that morphs in
- Sticky header that fades backdrop on scroll
- Mobile: Hamburger menu with slide-in overlay

---

## Layout & Spacing

### Grid System

**Base Unit:** 8px

**Spacing Scale:**
- xs: 8px
- sm: 16px
- md: 24px
- lg: 40px
- xl: 64px
- 2xl: 96px

### Layout Principles

1. **Asymmetry preferred** - Avoid perfectly centered layouts
2. **Overlapping elements** - Layer components using z-index
3. **Full-bleed sections** - Let backgrounds extend edge-to-edge
4. **Generous negative space** - Dark space is as important as content

### Container Widths
- Desktop max-width: 1200px
- Content max-width: 800px (for reading)
- Full-bleed: 100vw (for hero sections)

### Responsive Breakpoints
```css
/* Mobile first approach */
--mobile: 320px;
--tablet: 768px;
--desktop: 1024px;
--wide: 1440px;
```

---

## Visual Effects

### Grain Texture Overlay

```css
/* Apply to body as ::before pseudo-element */
.grain-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0.05;
  pointer-events: none;
  background-image: url('noise-texture.png');
  animation: grain 8s steps(10) infinite;
}

@keyframes grain {
  0%, 100% { transform: translate(0, 0); }
  10% { transform: translate(-5%, -10%); }
  /* ... continue pattern ... */
}
```

### Scanlines

```css
.scanlines {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: repeating-linear-gradient(
    0deg,
    rgba(0, 0, 0, 0.15),
    rgba(0, 0, 0, 0.15) 1px,
    transparent 1px,
    transparent 2px
  );
  pointer-events: none;
}
```

### Vignette

```css
.vignette {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(
    circle at center,
    transparent 0%,
    rgba(10, 10, 10, 0.7) 100%
  );
  pointer-events: none;
}
```

### Gradient Backgrounds

**Radial Blob Gradients**
```css
.gradient-blob {
  position: absolute;
  width: 600px;
  height: 600px;
  background: radial-gradient(
    circle,
    rgba(255, 0, 128, 0.3) 0%,
    transparent 70%
  );
  filter: blur(80px);
  animation: float 6s ease-in-out infinite;
}
```

**Conic Gradient (Rotating)**
```css
.conic-gradient {
  background: conic-gradient(
    from 0deg,
    #FF0080,
    #00F0FF,
    #39FF14,
    #FF10F0,
    #FF0080
  );
  filter: blur(120px);
  animation: rotate 20s linear infinite;
}
```

### Glow Halos (Multi-layer)

```css
/* Apply to important elements */
.glow-halo {
  box-shadow: 
    /* Inner tight glow */
    inset 0 0 20px rgba(255, 0, 128, 0.4),
    /* Mid spread glow */
    0 0 40px rgba(255, 0, 128, 0.6),
    /* Outer soft glow */
    0 0 80px rgba(255, 0, 128, 0.3);
}
```

---

## Interaction Patterns

### Scrolling Behavior

**Parallax Effect**
```javascript
window.addEventListener('scroll', () => {
  const scrolled = window.pageYOffset;
  element.style.transform = `translateY(${scrolled * 0.5}px)`;
});
```

**Fade-in on Scroll**
- Elements enter viewport with upward drift + opacity fade
- Stagger animations for multiple elements
- Use Intersection Observer API for performance

### Cursor Effects

**Custom Cursor**
```css
body {
  cursor: none;
}

.custom-cursor {
  position: fixed;
  width: 20px;
  height: 20px;
  border: 2px solid #FF0080;
  border-radius: 50%;
  pointer-events: none;
  box-shadow: 0 0 20px #FF0080;
}
```

**Neon Trail**
```javascript
document.addEventListener('mousemove', (e) => {
  const trail = document.createElement('div');
  trail.style.position = 'fixed';
  trail.style.left = e.pageX + 'px';
  trail.style.top = e.pageY + 'px';
  trail.style.background = '#FF0080';
  trail.style.boxShadow = '0 0 20px #FF0080';
  // ... animate and remove
});
```

### Loading States

**Spinner**
```css
.neon-spinner {
  width: 60px;
  height: 60px;
  border: 3px solid rgba(255, 0, 128, 0.3);
  border-top-color: #FF0080;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  box-shadow: 0 0 30px rgba(255, 0, 128, 0.6);
}
```

**Progress Bar**
```css
.neon-progress {
  height: 4px;
  background: rgba(255, 0, 128, 0.2);
  position: relative;
  overflow: hidden;
}

.neon-progress::after {
  content: '';
  position: absolute;
  height: 100%;
  width: 40%;
  background: linear-gradient(90deg, #FF0080, #00F0FF);
  box-shadow: 0 0 20px #FF0080;
  animation: progress 1.5s ease-in-out infinite;
}
```

### Hover States (Summary)

**Standard Hover Transitions:**
- Glow intensification (20px → 60px spread)
- Slight lift (translateY: -4px to -8px)
- Color shift or chromatic aberration
- Scale increase (1.02-1.05)
- Cursor change to custom design

### Micro-interactions

**Success Feedback**
```css
@keyframes success-pulse {
  0% { 
    box-shadow: 0 0 0 0 rgba(57, 255, 20, 0.7);
  }
  100% {
    box-shadow: 0 0 0 40px rgba(57, 255, 20, 0);
  }
}
```

**Error Shake**
```css
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-10px); }
  75% { transform: translateX(10px); }
}
```

---

## Do's and Don'ts

### ✅ DO

- **Layer glows aggressively** - Multiple box-shadow values create depth
- **Use very dark backgrounds** - Black/near-black makes neons pop
- **Create contrast through light intensity** - Not color value
- **Animate subtly and continuously** - Everything should feel alive
- **Use transparency and blur liberally** - Glass morphism is key
- **Mix 2-3 neon colors per section** - Creates visual interest
- **Test on multiple displays** - Ensure glows render correctly
- **Provide dark mode toggle** - (This IS dark mode, but some may want darker)

### ❌ DON'T

- **Use light backgrounds** - Completely kills the neon effect
- **Exceed 3 neon colors simultaneously** - Creates visual chaos
- **Sacrifice readability** - Body text must still be legible
- **Overuse strobe effects** - Can trigger seizures, use sparingly
- **Forget accessibility** - Provide reduced motion alternatives
- **Use pure complementary colors** - (red/green for colorblind users)
- **Make everything glow equally** - Hierarchy is still important
- **Ignore performance** - Multiple filters/blurs can be expensive

---

## Accessibility Guidelines

### Critical Requirements

**Color Contrast**
- Text contrast must meet WCAG AA standards (4.5:1 minimum)
- Neon text on dark = usually passes, but test each combination
- Use tools like WebAIM Contrast Checker

**Reduced Motion**
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

**Photosensitivity Warning**
- If using strobe effects > 3 flashes/second, display warning
- Provide option to disable all flashing
- Default to safer animations

**Screen Reader Support**
- Visual effects shouldn't break semantic HTML
- Use ARIA labels where needed
- Ensure keyboard navigation works
- Test with VoiceOver/NVDA

**Focus States**
```css
*:focus-visible {
  outline: 2px solid #00F0FF;
  outline-offset: 4px;
  box-shadow: 0 0 0 4px rgba(0, 240, 255, 0.3);
}
```

---

## Performance Optimization

### Critical Considerations

**GPU Acceleration**
```css
/* Use transform and opacity for animations */
.animated-element {
  will-change: transform, opacity;
  transform: translateZ(0); /* Force GPU layer */
}
```

**Blur Performance**
- Limit `backdrop-filter: blur()` to 10-20px max
- Avoid animating blur values (expensive)
- Use static blurred backgrounds where possible

**Shadow Optimization**
- Combine multiple shadows in one declaration
- Avoid animating shadow spread aggressively
- Use opacity changes instead of shadow intensity changes

**Asset Loading**
- Lazy load non-critical visual effects
- Use CSS instead of images for gradients/effects
- Compress any texture overlays (noise, grain)

---

## Example Component Specs

### Hero Section

```css
.hero {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  background: #0A0A0A;
}

.hero::before {
  /* Gradient blob 1 */
  content: '';
  position: absolute;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(255, 0, 128, 0.3), transparent);
  top: 50%;
  left: 30%;
  transform: translate(-50%, -50%);
  filter: blur(80px);
  animation: float 6s ease-in-out infinite;
}

.hero h1 {
  font-family: 'Bebas Neue', sans-serif;
  font-size: clamp(48px, 8vw, 96px);
  color: #FF0080;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  text-shadow: 
    0 0 20px rgba(255, 0, 128, 0.6),
    0 0 40px rgba(255, 0, 128, 0.4),
    0 0 60px rgba(255, 0, 128, 0.2);
  animation: neonPulse 2s infinite;
}
```

### Feature Card

```css
.feature-card {
  background: rgba(26, 26, 26, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 240, 255, 0.5);
  padding: 40px;
  border-radius: 0; /* Sharp corners preferred */
  transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  position: relative;
}

.feature-card::before {
  /* Hover glow effect */
  content: '';
  position: absolute;
  inset: -2px;
  background: linear-gradient(45deg, #FF0080, #00F0FF);
  opacity: 0;
  filter: blur(20px);
  transition: opacity 0.4s;
  z-index: -1;
}

.feature-card:hover::before {
  opacity: 0.5;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 0 60px rgba(0, 240, 255, 0.6);
}

.feature-icon {
  font-size: 48px;
  color: #00F0FF;
  text-shadow: 0 0 20px rgba(0, 240, 255, 0.8);
  animation: neonPulse 2s infinite;
}
```

---

## Design Tokens (CSS Variables)

```css
:root {
  /* Colors */
  --color-electric-magenta: #FF0080;
  --color-cyber-blue: #00F0FF;
  --color-acid-green: #39FF14;
  --color-warning-pink: #FF10F0;
  --color-toxic-yellow: #FFFF00;
  --color-void-black: #0A0A0A;
  --color-deep-charcoal: #1A1A1A;
  --color-shadow-purple: #1A0F1F;
  
  /* Spacing */
  --space-xs: 8px;
  --space-sm: 16px;
  --space-md: 24px;
  --space-lg: 40px;
  --space-xl: 64px;
  --space-2xl: 96px;
  
  /* Typography */
  --font-display: 'Bebas Neue', Impact, sans-serif;
  --font-body: 'Space Grotesk', system-ui, sans-serif;
  
  /* Animation */
  --duration-fast: 200ms;
  --duration-normal: 400ms;
  --duration-slow: 800ms;
  --easing-elastic: cubic-bezier(0.68, -0.55, 0.265, 1.55);
  --easing-smooth: cubic-bezier(0.4, 0, 0.2, 1);
  
  /* Effects */
  --blur-sm: 10px;
  --blur-md: 20px;
  --blur-lg: 40px;
  --blur-xl: 80px;
}
```

---

## Browser Support

### Minimum Requirements
- Chrome/Edge 88+
- Firefox 85+
- Safari 14+

### Critical Features Used
- `backdrop-filter` (requires fallback for older browsers)
- CSS Grid and Flexbox
- CSS Custom Properties (variables)
- CSS Animations and Transitions
- `calc()`, `clamp()` for responsive sizing

### Fallbacks

```css
/* Backdrop filter fallback */
@supports not (backdrop-filter: blur(10px)) {
  .glass-element {
    background: rgba(26, 26, 26, 0.95); /* More opaque */
  }
}
```

---

## Tools & Resources

### Recommended Design Tools
- **Figma** - Primary design tool
- **Spline** - For 3D gradient mockups
- **Rive** - For complex animations
- **After Effects** - For motion design references

### Color Tools
- [Coolors](https://coolors.co) - Palette generation
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) - Accessibility testing

### Development Tools
- Chrome DevTools - Animation debugging
- Lighthouse - Performance auditing
- axe DevTools - Accessibility testing

### Inspiration References
- "Enter the Void" (2009) - Film by Gaspar Noé
- Cyberpunk aesthetic archives
- Tokyo neon photography
- Synthwave/Vaporwave art movements

---

## Version History

**v1.0** - Initial design language specification  
Date: 2025  
Created by: [Your Name/Studio]

---

## License & Usage

This design language is provided as a guide for creating psychedelic, neon-inspired web interfaces. Adapt and modify as needed for your projects.

**Attribution:** When using this design language, attribution to the Gaspar Noé aesthetic inspiration is appreciated but not required.

---

## Questions & Support

For questions about implementing this design language or for additional examples, contact:
[Your contact information]

---

*"Enter the void. Transcend reality. Design with light."*