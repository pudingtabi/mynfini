import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'
import { resolve } from 'path'

// Production configuration optimized for Render static deployment
export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.ico', 'robots.txt', 'apple-touch-icon.png'],
      manifest: {
        name: 'MYNFINI AI Game Master',
        short_name: 'MYNFINI',
        description: 'AI-powered creative storytelling game with dynamic world evolution',
        theme_color: '#1a1a2e',
        background_color: '#0f0f1e',
        display: 'standalone',
        scope: '/',
        start_url: '/',
        icons: [
          {
            src: '/icon-192x192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: '/icon-512x512.png',
            sizes: '512x512',
            type: 'image/png'
          }
        ],
        screenshots: [
          {
            src: '/screenshot-desktop.png',
            sizes: '1440x900',
            type: 'image/png',
            form_factor: 'wide'
          },
          {
            src: '/screenshot-mobile.png',
            sizes: '390x844',
            type: 'image/png',
            form_factor: 'narrow'
          }
        ]
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg,webp,woff2}'],
        globIgnores: ['**/sitemap.xml', '**/robots.txt', '**/*.map'],
        runtimeCaching: [
          // AI Provider APIs with freshness strategy
          {
            urlPattern: /^https:\/\/api\.openai\.com\/.*/i,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'openai-api-cache',
              cacheableResponse: { statuses: [0, 200] },
              expiration: {
                maxEntries: 50,
                maxAgeSeconds: 60 * 60 // 1 hour
              }
            }
          },
          {
            urlPattern: /^https:\/\/api\.anthropic\.com\/.*/i,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'anthropic-api-cache',
              cacheableResponse: { statuses: [0, 200] },
              expiration: {
                maxEntries: 50,
                maxAgeSeconds: 60 * 60 // 1 hour
              }
            }
          },
          {
            urlPattern: /^https:\/\/api\.groq\.com\/.*/i,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'groq-api-cache',
              cacheableResponse: { statuses: [0, 200] },
              expiration: {
                maxEntries: 50,
                maxAgeSeconds: 60 * 30 // 30 minutes
              }
            }
          },
          // Static assets
          {
            urlPattern: /^https:\/\/fonts\.gstatic\.com\/.*/i,
            handler: 'CacheFirst',
            options: {
              cacheName: 'google-fonts-cache',
              expiration: {
                maxEntries: 30,
                maxAgeSeconds: 60 * 60 * 24 * 365 // 1 year
              }
            }
          }
        ],
        skipWaiting: true,
        clientsClaim: true,
        cleanupOutdatedCaches: true,
        sourcemap: false
      }
    })
  ],

  // Base URL for static deployment
  base: '/',

  // Build Optimization
  build: {
    target: 'es2015',
    outDir: 'dist',
    assetsDir: 'assets',
    assetsInlineLimit: 4096,
    sourcemap: false,
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true,
        pure_funcs: ['console.log', 'console.info'],
        passes: 2
      },
      mangle: {
        toplevel: true,
        properties: {
          regex: /^_/
        }
      }
    },
    cssCodeSplit: true,
    reportCompressedSize: true,
    chunkSizeWarningLimit: 1000,
    rollupOptions: {
      output: {
        manualChunks: {
          // Vendor chunks for better caching
          'react-vendor': ['react', 'react-dom'],
          'ai-vendor': ['lucide-react', 'framer-motion'],
          'utils-vendor': ['axios'],
          'charts-vendor': ['recharts', 'd3'],
          // App-specific chunks
          'app-routes': ['./src/App.tsx', './src/main.tsx'],
          'world-engine': ['./src/components/WorldCanvas', './src/components/WorldStatePanel'],
          'ai-engine': ['./src/components/creativity', './src/components/AIEvaluation']
        },
        entryFileNames: 'assets/[name]-[hash].js',
        chunkFileNames: 'assets/[name]-[hash].js',
        assetFileNames: 'assets/[name]-[hash].[ext]',
        compact: true,
        freeze: false
      }
    },
    lib: {
      formats: ['es']
    }
  },

  // Server configuration optimized for development
  server: {
    port: 3000,
    host: true,
    open: true,
    cors: true,
    headers: {
      'Cache-Control': 'no-cache'
    }
  },

  // Preview server configuration
  preview: {
    port: 4173,
    host: true,
    open: true,
    headers: {
      'X-Powered-By': 'MYNFINI-Game-Master/1.0.0'
    }
  },

  // Define constants for application
  define: {
    __APP_ENV__: JSON.stringify('production'),
    __APP_VERSION__: JSON.stringify('1.0.0'),
    __BUILD_TIME__: JSON.stringify(new Date().toISOString()),
    __RENDER_ENV__: JSON.stringify('true')
  },

  // ESBuild optimization
  esbuild: {
    legalComments: 'none',
    target: 'es2015',
    format: 'iife',
    minifyIdentifiers: true,
    minifySyntax: true,
    minifyWhitespace: true,
    drop: ['console', 'debugger'],
    treeShaking: true
  },

  // Resolve aliases for cleaner imports
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
      '@components': resolve(__dirname, './src/components'),
      '@services': resolve(__dirname, './src/services'),
      '@utils': resolve(__dirname, './src/utils'),
      '@hooks': resolve(__dirname, './src/hooks'),
      '@types': resolve(__dirname, './src/types')
    }
  }
})