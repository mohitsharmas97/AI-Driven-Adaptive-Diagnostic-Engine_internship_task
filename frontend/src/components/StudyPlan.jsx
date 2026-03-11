export default function StudyPlan({ plan, onRestart }) {
    if (!plan) return null;

    return (
        <div className="card">
            {/* Logo */}
            <div className="logo-mark" style={{ marginBottom: 16 }}>
                <svg width="22" height="22" viewBox="0 0 28 28" fill="none">
                    <rect width="28" height="28" rx="8" fill="url(#lg4)" />
                    <path d="M8 20L14 8L20 20" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
                    <path d="M10 16h8" stroke="white" strokeWidth="2" strokeLinecap="round" />
                    <defs>
                        <linearGradient id="lg4" x1="0" y1="0" x2="28" y2="28">
                            <stop stopColor="#8b5cf6" />
                            <stop offset="1" stopColor="#06b6d4" />
                        </linearGradient>
                    </defs>
                </svg>
                AdaptIQ
            </div>

            <h2 className="hero-title" style={{ fontSize: '1.75rem', marginBottom: 8 }}>
                🧠 Your AI Study Plan
            </h2>

            <p style={{
                background: 'rgba(139,92,246,0.1)',
                border: '1px solid rgba(139,92,246,0.25)',
                borderRadius: 'var(--radius-md)',
                padding: '14px 16px',
                fontSize: '0.9rem',
                color: 'var(--text-secondary)',
                lineHeight: 1.6,
                marginBottom: 24,
            }}>
                {plan.summary}
            </p>

            <h3 className="section-title" style={{ marginBottom: 8 }}>Your Personalised 3-Step Plan</h3>

            {plan.steps?.map(step => (
                <div className="plan-step" key={step.step}>
                    <div className="step-num">{step.step}</div>
                    <div className="step-content">
                        <div className="step-title">{step.title}</div>
                        <div className="step-desc">{step.description}</div>
                        {step.resources?.length > 0 && (
                            <div className="step-resources">
                                {step.resources.map(r => (
                                    <span className="resource-tag" key={r}>{r}</span>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            ))}

            {plan.estimated_duration && (
                <div style={{
                    marginTop: 24,
                    padding: '12px 16px',
                    background: 'rgba(6,182,212,0.08)',
                    border: '1px solid rgba(6,182,212,0.2)',
                    borderRadius: 'var(--radius-md)',
                    display: 'flex',
                    alignItems: 'center',
                    gap: 10,
                    fontSize: '0.875rem',
                    color: 'var(--accent-cyan)',
                }}>
                    <span>⏱</span>
                    <span><strong>Estimated Duration:</strong> {plan.estimated_duration}</span>
                </div>
            )}

            <div className="divider" />

            <button className="btn btn-primary w-full" onClick={onRestart}>
                ↩ Start New Test
            </button>
        </div>
    );
}
