import React, { createContext, useContext, useEffect, useState } from 'react'
import { ThemeProvider as StyledProvider } from 'styled-components'

interface Theme {
  mode: 'dark' | 'light'
  colors: {
    primary: string
    secondary: string
    accent: string
    warning: string
    error: string
    bgPrimary: string
    bgSecondary: string
    bgGlass: string
    bgGlassLight: string
    textPrimary: string
    textSecondary: string
    borderGlass: string
    shadowGlow: string
  }
  isColorResponsive: boolean
  currentColor: string
}

interface ThemeContextType {
  theme: Theme
  setThemeMode: (mode: 'dark' | 'light') => void
  toggleColorResponsive: () => void
  updateColorResponse: (color: string) => void
}

const defaultDarkTheme: Theme = {
  mode: 'dark',
  colors: {
    primary: '#3b82f6',
    secondary: '#8b5cf6',
    accent: '#22c55e',
    warning: '#f59e0b',
    error: '#ef4444',
    bgPrimary: '#0f0f23',
    bgSecondary: '#1a1a2e',
    bgGlass: 'rgba(26, 26, 46, 0.7)',
    bgGlassLight: 'rgba(26, 26, 46, 0.4)',
    textPrimary: '#e4e4e4',
    textSecondary: '#a8a8a8',
    borderGlass: 'rgba(255, 255, 255, 0.1)',
    shadowGlow: 'rgba(59, 130, 246, 0.3)',
  },
  isColorResponsive: false,
  currentColor: '#3b82f6'
}

const lightTheme: Theme = {
  mode: 'light',
  colors: {
    primary: '#2563eb',
    secondary: '#7c3aed',
    accent: '#16a34a',
    warning: '#d97706',
    error: '#dc2626',
    bgPrimary: '#f8fafc',
    bgSecondary: '#e2e8f0',
    bgGlass: 'rgba(248, 250, 252, 0.8)',
    bgGlassLight: 'rgba(248, 250, 252, 0.5)',
    textPrimary: '#0f172a',
    textSecondary: '#475569',
    borderGlass: 'rgba(15, 23, 42, 0.1)',
    shadowGlow: 'rgba(37, 99, 235, 0.2)',
  },
  isColorResponsive: false,
  currentColor: '#2563eb'
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

export const useTheme = () => {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider')
  }
  return context
}

interface ThemeProviderProps {
  children: React.ReactNode
}

const globalStyles = `
  :root {
    --primary: ${defaultDarkTheme.colors.primary};
    --secondary: ${defaultDarkTheme.colors.secondary};
    --accent: ${defaultDarkTheme.colors.accent};
    --bg-primary: ${defaultDarkTheme.colors.bgPrimary};
    --bg-secondary: ${defaultDarkTheme.colors.bgSecondary};
    --text-primary: ${defaultDarkTheme.colors.textPrimary};
    --text-secondary: ${defaultDarkTheme.colors.textSecondary};
    --border-glass: ${defaultDarkTheme.colors.borderGlass};
    --shadow-glow: ${defaultDarkTheme.colors.shadowGlow};
  }
`

export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  const [theme, setTheme] = useState<Theme>(defaultDarkTheme)

  useEffect(() => {
    const savedTheme = localStorage.getItem('mynfini-theme')
    if (savedTheme === 'light') {
      setTheme(lightTheme)
    }

    // Apply global styles
    const styleElement = document.createElement('style')
    styleElement.textContent = globalStyles
    document.head.appendChild(styleElement)

    return () => {
      document.head.removeChild(styleElement)
    }
  }, [])

  const setThemeMode = (mode: 'dark' | 'light') => {
    const newTheme = mode === 'light' ? lightTheme : defaultDarkTheme
    setTheme(newTheme)
    localStorage.setItem('mynfini-theme', mode)
    document.documentElement.setAttribute('data-theme', mode)
  }

  const toggleColorResponsive = () => {
    setTheme(prev => ({
      ...prev,
      isColorResponsive: !prev.isColorResponsive
    }))
  }

  const updateColorResponse = (color: string) => {
    setTheme(prev => ({
      ...prev,
      currentColor: color,
      isColorResponsive: true
    }))

    // Update CSS variables for color responsiveness
    document.documentElement.style.setProperty('--current-color', color)
  }

  // Color-responsive effects
  useEffect(() => {
    if (theme.isColorResponsive && theme.currentColor) {
      const color = theme.currentColor
      const rgb = hexToRgb(color)
      if (rgb) {
        const shadowColor = `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, 0.3)`
        document.documentElement.style.setProperty('--shadow-glow', shadowColor)
        document.body.style.background = `linear-gradient(135deg, ${theme.colors.bgPrimary} 0%, ${adjustBrightness(color, -20)} 100%)`
      }
    } else {
      document.body.style.background = `linear-gradient(135deg, ${theme.colors.bgPrimary} 0%, #1e293b 100%)`
      document.documentElement.style.setProperty('--shadow-glow', theme.colors.shadowGlow)
    }
  }, [theme.isColorResponsive, theme.currentColor, theme.colors])

  return (
    <ThemeContext.Provider value={{
      theme,
      setThemeMode,
      toggleColorResponsive,
      updateColorResponse
    }}>
      <StyledProvider theme={theme}>
        {children}
      </StyledProvider>
    </ThemeContext.Provider>
  )
}

// Utility functions
function hexToRgb(hex: string): { r: number; g: number; b: number } | null {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  } : null
}

function adjustBrightness(hex: string, percent: number): string {
  const num = parseInt(hex.replace("#", ""), 16)
  const amt = Math.round(2.55 * percent)
  const R = (num >> 16) + amt
  const G = (num >> 8 & 0x00FF) + amt
  const B = (num & 0x0000FF) + amt
  return "#" + (0x1000000 + (R < 255 ? R < 1 ? 0 : R : 255) * 0x10000 +
    (G < 255 ? G < 1 ? 0 : G : 255) * 0x100 +
    (B < 255 ? B < 1 ? 0 : B : 255)).toString(16).slice(1)
}