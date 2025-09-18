import React, { useState } from 'react'

interface CreativityEvaluation {
  tier: 'BASIC' | 'CREATIVE' | 'MASTERFUL' | 'LEGENDARY' | 'BEYOND_LEGENDARY'
  score: number
  creativity_feedback: string
  mechanical_bonuses?: string
  inspiration_earned: number
  timestamp: string
}

interface WorldElement {
  id: string
  title: string
  description: string
  type: 'character' | 'location' | 'item' | 'event' | 'ability'
  discovered_at: string
}

interface WorldState {
  worldId: string
  elements: WorldElement[]
  creativityScore: number
  evolutionStage: string
  discoveries: number
  inspirationStreak: number
}

function App() {
  const [creativeInput, setCreativeInput] = useState('')
  const [isEvaluating, setIsEvaluating] = useState(false)
  const [lastEvaluation, setLastEvaluation] = useState<CreativityEvaluation | null>(null)
  const [world, setWorld] = useState<WorldState>({
    worldId: 'my-creative-universe',
    elements: [],
    creativityScore: 0,
    evolutionStage: 'SEEDLING',
    discoveries: 0,
    inspirationStreak: 0
  })

  // Mock creativity evaluation
  const evaluateCreativity = async (): Promise<CreativityEvaluation> => {
    // Simulate API call with realistic delay
    await new Promise(resolve => setTimeout(resolve, 2000))

    const score = Math.floor(Math.random() * 100) + 1
    let tier: CreativityEvaluation['tier'] = 'BASIC'

    if (score >= 90) tier = 'BEYOND_LEGENDARY'
    else if (score >= 80) tier = 'LEGENDARY'
    else if (score >= 65) tier = 'MASTERFUL'
    else if (score >= 40) tier = 'CREATIVE'

    const feedback = generateFeedback(score)
    const newElement = generateWorldElement()

    return {
      tier,
      score,
      creativity_feedback: feedback,
      mechanical_bonuses: `You discovered: ${newElement.title}`,
      inspiration_earned: Math.floor(score / 20),
      timestamp: new Date().toISOString()
    }
  }

  const generateFeedback = (score: number): string => {
    if (score >= 90) return 'Your creativity transcends ordinary boundaries! This is beyond legendary thinking.'
    if (score >= 80) return 'Truly legendary creativity! Your imagination paints worlds beyond comprehension.'
    if (score >= 65) return 'Masterful creative expression! Your world grows stronger with each inspired choice.'
    if (score >= 40) return 'Creative and thoughtful! Your world responds to your artistic vision.'
    return 'Good foundation! Every creative journey begins with a single step.'
  }

  const generateWorldElement = (): WorldElement => {
    const elements = [
      { title: 'Whispering Woods', description: 'Ancient trees that share their secrets through whispers in the wind', type: 'location' as const },
      { title: 'Dragon Companion', description: 'A wise dragon who guides you through creative challenges', type: 'character' as const },
      { title: 'Inspiration Crystal', description: 'A crystal that amplifies your creative thinking', type: 'item' as const },
      { title: 'Song of Creation', description: 'A melody that transforms thoughts into reality', type: 'ability' as const },
      { title: 'Garden of Ideas', description: 'A magical garden where creative concepts bloom', type: 'location' as const }
    ]

    const randomElement = elements[Math.floor(Math.random() * elements.length)]
    return {
      id: `element-${Date.now()}`,
      discovered_at: new Date().toISOString(),
      ...randomElement
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!creativeInput.trim()) return

    setIsEvaluating(true)
    try {
      const evaluation = await evaluateCreativity()
      setLastEvaluation(evaluation)

      // Update world state
      const newElement = generateWorldElement()
      setWorld(prev => ({
        ...prev,
        elements: [...prev.elements, newElement],
        creativityScore: Math.max(prev.creativityScore, evaluation.score),
        discoveries: prev.discoveries + 1,
        inspirationStreak: prev.inspirationStreak + evaluation.inspiration_earned,
        evolutionStage: evaluation.tier === 'BEYOND_LEGENDARY' ? 'COSMIC' :
                       evaluation.tier === 'LEGENDARY' ? 'ASCENDANT' :
                       evaluation.tier === 'MASTERFUL' ? 'ENLIGHTENED' :
                       evaluation.tier === 'CREATIVE' ? 'AWAKENED' : 'SEEDLING'
      }))

      setCreativeInput('')
    } catch (error) {
      console.error('Error evaluating creativity:', error)
    } finally {
      setIsEvaluating(false)
    }
  }

  const getTierColor = (tier: string) => {
    const colors: Record<string, string> = {
      'BASIC': '#9ca3af',
      'CREATIVE': '#3b82f6',
      'MASTERFUL': '#16a34a',
      'LEGENDARY': '#dc2626',
      'BEYOND_LEGENDARY': 'linear-gradient(45deg, #dc2626, #7c3aed)'
    }
    return colors[tier] || '#6b7280'
  }

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #0f0f23 0%, #1e293b 100%)',
      color: '#e4e4e4',
      fontFamily: 'system-ui, -apple-system, sans-serif'
    }}>
      {/* Header */}
      <header style={{
        padding: '1.5rem',
        background: 'rgba(26, 26, 46, 0.7)',
        backdropFilter: 'blur(20px)',
        borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
        boxShadow: '0 8px 32px rgba(59, 130, 246, 0.3)'
      }}>
        <h1 style={{
          fontSize: '1.8rem',
          fontWeight: '600',
          background: 'linear-gradient(45deg, #3b82f6, #8b5cf6)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent'
        }}>
          🌍 MYNFINI Solo World-Weaver
        </h1>
        <p style={{ color: '#a8a8a8', marginTop: '0.5rem' }}>
          Your personal creative universe awaits
        </p>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: '300px 1fr', gap: '1rem', padding: '1rem', maxWidth: '1400px', margin: '0 auto' }}>
        {/* Sidebar - World State Panel */}
        <aside style={{
          background: 'rgba(26, 26, 46, 0.7)',
          backdropFilter: 'blur(20px)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          borderRadius: '12px',
          padding: '1.5rem',
          boxShadow: '0 8px 32px rgba(59, 130, 246, 0.3)'
        }}>
          <h3 style={{ marginBottom: '1rem', color: '#3b82f6' }}>🌱 World Statistics</h3>

          <div style={{ marginBottom: '0.75rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
              <span style={{ color: '#a8a8a8' }}>Elements Discovered</span>
              <span style={{ fontWeight: '600', fontFamily: 'monospace' }}>{world.elements.length}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
              <span style={{ color: '#a8a8a8' }}>Total Discoveries</span>
              <span style={{ fontWeight: '600', fontFamily: 'monospace' }}>{world.discoveries}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
              <span style={{ color: '#a8a8a8' }}>Inspiration Streak</span>
              <span style={{ fontWeight: '600', fontFamily: 'monospace' }}>{world.inspirationStreak}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: '#a8a8a8' }}>Evolution Stage</span>
              <span style={{ fontWeight: '600', fontFamily: 'monospace' }}>{world.evolutionStage}</span>
            </div>
          </div>

          <h4 style={{ margin: '1rem 0 0.5rem', color: '#3b82f6' }}>🔮 Creative DNA</h4>
          <div style={{
            height: '8px',
            background: 'rgba(255, 255, 255, 0.1)',
            borderRadius: '4px',
            overflow: 'hidden',
            marginBottom: '0.5rem'
          }}>
            <div style={{
              height: '100%',
              width: `${Math.min(world.creativityScore, 100)}%`,
              background: 'linear-gradient(90deg, #3b82f6, #22c55e)',
              borderRadius: '4px',
              transition: 'width 0.5s ease'
            }} />
          </div>
          <div style={{ textAlign: 'right', fontSize: '0.8rem', color: '#a8a8a8', fontFamily: 'monospace' }}>
            {Math.round(world.creativityScore)}%
          </div>
        </aside>

        {/* Main Content */}
        <main style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {/* Creativity Input */}
          <section style={{
            background: 'rgba(26, 26, 46, 0.7)',
            backdropFilter: 'blur(20px)',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            borderRadius: '12px',
            padding: '1.5rem',
            boxShadow: '0 8px 32px rgba(59, 130, 246, 0.3)'
          }}>
            <h3 style={{ marginBottom: '1rem', color: '#3b82f6' }}>🎨 Craft Your World</h3>
            <p style={{ color: '#a8a8a8', marginBottom: '1rem', lineHeight: '1.5' }}>
              Describe your creative action poetically, metaphorically, or precisely.
              The AI will evaluate your creativity and transform it into mechanical benefits for your world.
            </p>

            <form onSubmit={handleSubmit}>
              <textarea
                value={creativeInput}
                onChange={(e) => setCreativeInput(e.target.value)}
                placeholder="Try: 'I whisper to the ancient trees, asking them to share their secrets...'"
                disabled={isEvaluating}
                style={{
                  width: '100%',
                  minHeight: '120px',
                  padding: '1rem',
                  background: 'rgba(255, 255, 255, 0.1)',
                  border: '2px solid rgba(255, 255, 255, 0.2)',
                  borderRadius: '8px',
                  color: 'white',
                  fontSize: '1rem',
                  lineHeight: '1.5',
                  resize: 'vertical'
                }}
              />
              <div style={{ textAlign: 'right', marginTop: '0.5rem', color: '#a8a8a8', fontFamily: 'monospace', fontSize: '0.8rem' }}>
                {creativeInput.trim().split(/\s+/).filter(w => w.length > 0).length} words
              </div>
              <button
                type="submit"
                disabled={isEvaluating || !creativeInput.trim()}
                style={{
                  marginTop: '1rem',
                  padding: '0.75rem 1.5rem',
                  background: 'linear-gradient(45deg, #3b82f6, #8b5cf6)',
                  border: 'none',
                  borderRadius: '8px',
                  color: 'white',
                  fontWeight: '500',
                  fontSize: '1rem',
                  cursor: 'pointer'
                }}
                onMouseOver={(e) => e.currentTarget.style.transform = 'translateY(-2px)'}
                onMouseOut={(e) => e.currentTarget.style.transform = 'none'}
              >
                {isEvaluating ? '✨ Evaluating...' : '✨ Evaluate Creativity'}
              </button>
            </form>

            {lastEvaluation && (
              <div style={{
                marginTop: '1rem',
                padding: '1rem',
                background: 'rgba(255, 255, 255, 0.1)',
                borderRadius: '8px'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                  <span style={{ color: '#a8a8a8' }}>Creativity Tier:</span>
                  <span style={{
                    padding: '0.25rem 0.75rem',
                    background: getTierColor(lastEvaluation.tier),
                    borderRadius: '6px',
                    fontWeight: '600',
                    color: 'white',
                    textTransform: 'uppercase',
                    fontSize: '0.8rem'
                  }}>
                    {lastEvaluation.tier.replace('_', ' ')}
                  </span>
                </div>
                <div style={{ color: '#a8a8a8', fontSize: '0.9rem', lineHeight: '1.5' }}>
                  <strong>Creative Insight:</strong> {lastEvaluation.creativity_feedback}
                </div>
                {lastEvaluation.mechanical_bonuses && (
                  <div style={{ color: '#a8a8a8', fontSize: '0.9rem', lineHeight: '1.5', marginTop: '0.5rem' }}>
                    <strong>World Benefits:</strong> {lastEvaluation.mechanical_bonuses}
                  </div>
                )}
              </div>
            )}
          </section>

          {/* World Canvas */}
          <section style={{
            flex: 1,
            background: 'rgba(26, 26, 46, 0.7)',
            backdropFilter: 'blur(20px)',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            borderRadius: '12px',
            padding: '1.5rem',
            boxShadow: '0 8px 32px rgba(59, 130, 246, 0.3)'
          }}>
            <h3 style={{ marginBottom: '1rem', color: '#3b82f6' }}>🌍 Your Creative Universe</h3>

            {world.elements.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '2rem', color: '#a8a8a8' }}>
                <h4>🌱 Begin Your Journey</h4>
                <p>Your universe is ready to bloom with creativity.</p>
                <p>Use the creativity input to start painting your world.</p>
              </div>
            ) : (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem' }}>
                {world.elements.map((element) => (
                  <div
                    key={element.id}
                    style={{
                      background: 'rgba(255, 255, 255, 0.1)',
                      borderRadius: '8px',
                      padding: '1rem',
                      border: '1px solid rgba(255, 255, 255, 0.2)'
                    }}
                  >
                    <div style={{ fontWeight: 'bold', marginBottom: '0.5rem' }}>{element.title}</div>
                    <div style={{ fontSize: '0.9rem', opacity: 0.9 }}>{element.description}</div>
                    <div style={{
                      marginTop: '0.5rem',
                      fontSize: '0.8rem',
                      opacity: 0.7,
                      textAlign: 'right',
                      textTransform: 'uppercase'
                    }}>
                      {element.type}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </section>
        </main>
      </div>

      <footer style={{
        padding: '1rem',
        textAlign: 'center',
        background: 'rgba(26, 26, 46, 0.7)',
        color: '#a8a8a8',
        fontSize: '0.8rem'
      }}>
        ✨ Every creative choice you make paints your universe • Powered by revolutionary AI creativity evaluation
      </footer>
    </div>
  )
}

export default App