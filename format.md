

 Let me extract the exact design system from our completed calculators. 

Read [](file:///Users/mjaswanth/shramkavachscribbletools/scribbletools-calculator-suite/tools/financial-calculators/401k-calculator.html#1-1), lines 1 to 100

Ran terminal command:  grep -n 'header-icon\|page-header h2\|section-icon\|formula-label\|formula-math\|faq-item\|tool-link\|image-box img' annuity-calculator.html | head -30

Here's the **complete design system & template process** we follow for every financial calculator:

---

### **COLOR SYSTEM (CSS Variables)**

| Variable | Value | Usage |
|----------|-------|-------|
| `--primary-gradient` | `linear-gradient(135deg, #667EEA, #764BA2)` | Buttons, logo, accents, header bar |
| `--page-bg` | `linear-gradient(180deg, #F5F7FA, #E8EEF5, #F0E7F8)` | Body background |
| `--primary-blue` | `#4299E1` | Links, highlights |
| `--secondary-blue` | `#3182CE` | Secondary actions |
| `--success-green` / `--success-alt` | `#48BB78` / `#10B981` | Interest values, positive results |
| `--warning-amber` | `#F59E0B` | Equals sign in formula, amber stat icon |
| `--error-red` | `#EF4444` | Reset hover, errors |
| `--text-main` | `#2D3748` | Headings, primary text |
| `--text-secondary` | `#4A5568` | Body text, descriptions |
| `--text-muted` | `#718096` | Subtitles, labels |
| `--border` | `#E2E8F0` | Card borders, dividers |
| `--surface` | `#F7FAFC` | Light backgrounds |

### **FORMULA DARK-THEME COLORS**

| Element | Color |
|---------|-------|
| Background | `#1e293b → #0f172a` gradient |
| Top accent bar | `#667eea → #764ba2 → #a855f7` |
| Variables | `#93c5fd` (blue italic) |
| Result variable | `#a78bfa` (purple) |
| Operators | `#94a3b8` |
| Equals sign | `#f59e0b` (amber) |
| Superscripts | `#fbbf24` (yellow) |
| Parentheses | `#64748b` / `#475569` |
| Legend text | `#94a3b8` |
| Fraction divider | `2px solid #64748b` |

### **STAT ICON BACKGROUNDS**

| Class | Background | Use for |
|-------|-----------|---------|
| `.blue` | `#ebf5ff` | Money/contributions |
| `.green` | `#f0fdf4` | Interest/growth |
| `.purple` | `#faf5ff` | Ratios/percentages |
| `.amber` | `#fffbeb` | Time/periods |

---

### **PAGE STRUCTURE (top to bottom)**

| # | Component | Details |
|---|-----------|---------|
| 1 | **`<head>`** | SEO meta, OG tags, Twitter card, JSON-LD `WebApplication` schema, favicon |
| 2 | **Sticky Header** | Glassmorphism (`rgba(255,255,255,0.85)` + `blur(20px)`), animated gradient bottom bar, logo with `../../images/logo.webp`, nav links, hamburger for mobile |
| 3 | **Menu Overlay** | `rgba(0,0,0,0.5)` overlay for mobile menu |
| 4 | **Breadcrumb** | Home / Category / Current (bold, no link) |
| 5 | **Page Header** | White card, 5px rainbow top bar, floating emoji icon (3rem, `float` animation), h2 (2.5rem, 800 weight), subtitle paragraph |
| 6 | **Calc Wrapper** | `grid: 1.2fr 1fr`, left = inputs, right = results. Inputs: titled with emoji + h2, `.input-grid` (2-col), fields with label icons, `$` unit prefix, gradient Calculate button with shimmer hover, Reset button |
| 7 | **Results Panel** | Gradient bg `#f8fafc → #f1f5f9 → #eff1fe`, radial glow overlay. Main result: emoji icon + uppercase label + large gradient value (2.8rem). Stat cards: icon box + label + value |
| 8 | **Schedule/Table** | Sticky dark header (`#1e293b → #334155`), alternating rows, green `.interest-val`, bold `.balance-val`, 500px max-height scroll |
| 9 | **Content Card: About** | Section icon emoji + title, paragraphs, styled `<ul>` with gradient dot bullets |
| 10 | **Image Box** | Full-width Unsplash image, 350px height, bottom gradient overlay, zoom on hover |
| 11 | **Content Card: How to Use** | Bullet list explaining each input |
| 12 | **Content Card: Formula** | Dark container with formula rendered in CSS (`.formula-math` with `.fraction`, `.var`, `.operator`, `.equals`, `.sup`), legend below |
| 13 | **Content Card: Example** | Real-world practical calculation walkthrough |
| 14 | **Content Card: FAQ** | 5 collapsible items, `+` toggle rotates to `×`, purple active border with shadow |
| 15 | **Related Tools** | Grid of 6 `tool-link` cards with emoji + name, hover lifts with purple border |
| 16 | **Footer** | 4-column grid (brand, categories, resources, company), dark bg (`#1e293b → #0f172a`), gradient top accent, bottom bar with copyright + links |

---

### **JAVASCRIPT FUNCTIONS (every calculator)**

| Function | Purpose |
|----------|---------|
| `calculate()` | Main computation, updates all result fields |
| `buildTable()` / `buildGrowthTable()` | Generates year-by-year HTML table |
| `resetForm()` | Clears inputs & results, hides table |
| `formatCurrency()` / `formatCurrencyExact()` | `Intl.NumberFormat` USD formatting |
| `toggleFAQ(el)` | Accordion open/close |
| `toggleMenu()` | Mobile hamburger menu |
| Auto-run on `DOMContentLoaded` | Pre-calculates with default values |

---

### **RESPONSIVE BREAKPOINTS**

| Breakpoint | Changes |
|------------|---------|
| `≤992px` | Footer → 2-col, tools grid → 2-col |
| `≤850px` | Calc wrapper → single column, smaller header |
| `≤768px` | Mobile menu activates, footer → 1-col, image 220px |
| `≤480px` | Input grid → single column |

---

This is the exact blueprint. Every new calculator follows this structure — only the **inputs, calculation logic, table columns, formulas, content text, FAQ, and related tools** change per tool. Ready to start the next one?