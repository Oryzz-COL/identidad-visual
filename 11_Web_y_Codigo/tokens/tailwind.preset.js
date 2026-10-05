// Oryzz · design tokens v2.0 (2026-09-29) — GENERADO desde 00_Fuente_Maestra/tokens.json con build/web_tokens.py. No editar a mano.
//
// ── Tailwind v3 ─────────────────────────────────────────────────────────────
//   // tailwind.config.js
//   module.exports = { presets: [require('./tailwind.preset.js')], content: ['./src/**/*.html'] }
//   Clases: bg-grafito-950 text-azul-600 font-display text-h1 rounded-lg bg-grad-ia-oscuro
//   Radios: xs 6 · sm 10 · md 14 · lg 20 · xl 28 · full · app (22,5 %). Eyebrow: text-eyebrow font-mono uppercase
//           y semánticas (dependen de tokens.css): bg-fondo text-texto border-borde text-enlace
//
// ── Tailwind v4 (oryzz.com/tap usa v4) ──────────────────────────────────────
//   v4 no usa presets JS: importa `tailwind-v4.css` (mismo directorio), que declara los
//   tokens con `@theme`. En globals.css:
//       @import "tailwindcss";
//       @import "./tailwind-v4.css";
//   y elimina los `--color-*` y `--font-*` antiguos (#0075FF, #C5F500, Syne, Outfit…).
/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      colors: {
        grafito: {"950": "#0B0D12", "900": "#0E1118", "850": "#12151D", "800": "#171B25", "700": "#232836", "600": "#3A4152", "500": "#5A6172", "400": "#8A90A0", "300": "#C7CBD6", "200": "#D5D9E0", "100": "#E5E8EE", "50": "#F6F7F9", "0": "#FFFFFF"},
        azul: {"50": "#EEF3FF", "300": "#9FB8FF", "400": "#5C8BFF", "500": "#3B72FF", "600": "#2C5BD0", "700": "#1F43A0", "900": "#0F1E4A"},
        cyan: {"50": "#E8FAFC", "300": "#7DE6F2", "500": "#36CFE0", "600": "#17A9C2"},
        lima: {"50": "#F4FCE0", "300": "#E4F7B4", "500": "#BFF24A", "600": "#7FB02E", "900": "#3A4A12"},
        estado: {"exito": "#1F9D55", "aviso": "#F2A33A", "error": "#E5484D"},
        // semánticos (cambian con data-tema="oscuro|claro")
        'fondo': 'var(--color-fondo)',
        'superficie': 'var(--color-superficie)',
        'superficie-2': 'var(--color-superficie-2)',
        'borde': 'var(--color-borde)',
        'texto': 'var(--color-texto)',
        'texto-2': 'var(--color-texto-2)',
        'texto-3': 'var(--color-texto-3)',
        'acento': 'var(--color-acento)',
        'enlace': 'var(--color-enlace)',
        'dato': 'var(--color-dato)',
        'cta-texto': 'var(--color-cta-texto)',
        'cta-2-fondo': 'var(--color-cta-2-fondo)',
        'cta-2-texto': 'var(--color-cta-2-texto)',
        'cta-2-borde': 'var(--color-cta-2-borde)',
        'foco': 'var(--color-foco)',
        'seleccion': 'var(--color-seleccion)',
        'enlace-hover': 'var(--color-enlace-hover)',
        'borde-fuerte': 'var(--color-borde-fuerte)',
        'exito': 'var(--color-exito)',
        'aviso': 'var(--color-aviso)',
        'error': 'var(--color-error)',
        'texto-sobre-dato': 'var(--color-texto-sobre-dato)',
        'dato-texto': 'var(--color-dato-texto)',
      },
      fontFamily: {
        display: ["Space Grotesk", "Arial", "Helvetica", "sans-serif"],
        texto: ["Manrope", "Arial", "Helvetica", "sans-serif"],
        sans: ["Manrope", "Arial", "Helvetica", "sans-serif"],
        mono: ["JetBrains Mono", "Consolas", "Courier New", "monospace"],
      },
      fontSize: {"display-xl": ["6rem", {"lineHeight": "0.95", "letterSpacing": "-0.045em", "fontWeight": "700"}], "display-l": ["4.5rem", {"lineHeight": "1.0", "letterSpacing": "-0.04em", "fontWeight": "700"}], "h1": ["3.5rem", {"lineHeight": "1.05", "letterSpacing": "-0.035em", "fontWeight": "700"}], "h2": ["2.5rem", {"lineHeight": "1.1", "letterSpacing": "-0.03em", "fontWeight": "700"}], "h3": ["1.75rem", {"lineHeight": "1.2", "letterSpacing": "-0.02em", "fontWeight": "600"}], "h4": ["1.25rem", {"lineHeight": "1.3", "letterSpacing": "-0.01em", "fontWeight": "600"}], "lead": ["1.25rem", {"lineHeight": "1.55", "letterSpacing": "0em", "fontWeight": "400"}], "body": ["1rem", {"lineHeight": "1.6", "letterSpacing": "0em", "fontWeight": "400"}], "small": ["0.875rem", {"lineHeight": "1.5", "letterSpacing": "0em", "fontWeight": "500"}], "eyebrow": ["0.75rem", {"lineHeight": "1.2", "letterSpacing": "0.16em", "fontWeight": "500"}], "dato": ["4rem", {"lineHeight": "1.0", "letterSpacing": "-0.03em", "fontWeight": "500"}]},
      borderRadius: {"xs": "6px", "sm": "10px", "md": "14px", "lg": "20px", "xl": "28px", "full": "999px", "app": "22.5%"},
      backgroundImage: {
        'grad-ia-oscuro': 'linear-gradient(135deg, #5C8BFF 0%, #36CFE0 100%)',
        'grad-ia-claro': 'linear-gradient(135deg, #3B72FF 0%, #17A9C2 100%)',
        'cta': 'var(--color-cta-fondo)',
      },
      maxWidth: { contenido: '1200px' },
      transitionTimingFunction: { marca: 'cubic-bezier(.2,.8,.2,1)', salto: 'cubic-bezier(.34,1.4,.5,1)' },
      transitionDuration: { rapido: '160ms', base: '280ms', lento: '560ms' },
      strokeWidth: { icono: '1.75', grafico: '2' },
    },
  },
};
