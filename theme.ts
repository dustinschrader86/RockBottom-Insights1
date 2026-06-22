// src/theme.ts
export const theme = {
  colors: {
    background: '#0A0A0A',
    surface: '#121212',
    card: '#1A1A1A',
    text: '#FFFFFF',
    textSecondary: '#AAAAAA',
    primary: '#00FF9F',        // Neon Green
    accent: '#7C3AED',         // Purple
    danger: '#FF3B5C',         // Risk Red
    gold: '#D4AF37',           // Metallic gold from your icon
  },
  spacing: {
    xs: 4,
    sm: 8,
    md: 16,
    lg: 24,
    xl: 32,
  },
  borderRadius: {
    sm: 12,
    md: 20,
    lg: 28,
  },
  shadows: {
    glow: {
      shadowColor: '#00FF9F',
      shadowOffset: { width: 0, height: 0 },
      shadowOpacity: 0.6,
      shadowRadius: 12,
      elevation: 10,
    },
  },
};

export type Theme = typeof theme;