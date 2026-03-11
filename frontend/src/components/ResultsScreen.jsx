export default function ResultsScreen({ results, onGetPlan, planLoading, onRestart }) {
    const { ability_score, level, accuracy, correct_answers, total_questions, topic_breakdown, student_id } = results;

    const levelClass =
        level === 'Advanced' ? 'level-advanced' :
            level === 'Intermediate' ? 'level-intermediate' : 'level-beginner';

    return (
        <div className="card">
            {/* Logo */}
            <div className="logo-mark" style={{ marginBottom: 8 }}>
                <svg width="22" height="22" viewBox="0 0 28 28" fill="none">
                    <rect width="28" height="28" rx="8" fill="url(#lg3)" />
                    <path d="M8 20L14 8L20 20" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
                    <path d="M10 16h8" stroke="white" strokeWidth="2" strokeLinecap="round" />
                    <defs>
                        <linearGradient id="lg3" x1="0" y1="0" x2="28" y2="28">
                            <stop stopColor="#8b5cf6" />
                            <stop offset="1" stopColor="#06b6d4" />
                        </linearGradient>
                    </defs>
                </svg>
                AdaptIQ
            </div>

            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 8, flexWrap: 'wrap', gap: 8 }}>
                <h2 className="hero-title" style={{ marginBottom: 0, fontSize: '1.75rem' }}>Your Results</h2>
                <span className={`level-badge ${levelClass}`}>{level}</span>
            </div>

            <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem', marginBottom: 24 }}>
                Student: <strong style={{ color: 'var(--text-secondary)' }}>{student_id}</strong>
            </p>

            {/* Stats */}
            <div className="stats-grid">
                <div className="stat-card">
                    <div className="stat-value">{(ability_score * 100).toFixed(0)}</div>
                    <div className="stat-label">Ability Score</div>
                </div>
                <div className="stat-card">
                    <div className="stat-value">{accuracy}%</div>
                    <div className="stat-label">Accuracy</div>
                </div>
                <div className="stat-card">
                    <div className="stat-value">{correct_answers}/{total_questions}</div>
                    <div className="stat-label">Correct</div>
                </div>
            </div>

            {/* Ability bar */}
            <div className="ability-bar-wrap" style={{ margin: '20px 0' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6, fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                    <span>Ability Score (θ)</span>
                    <span style={{ fontWeight: 700, color: 'var(--text-primary)' }}>{ability_score?.toFixed(4)}</span>
                </div>
                <div className="ability-track">
                    <div className="ability-fill" style={{ width: `${ability_score * 100}%` }} />
                </div>
                <div className="ability-labels">
                    <span>0.0 — Beginner</span>
                    <span>0.5</span>
                    <span>1.0 — Advanced</span>
                </div>
            </div>

            <div className="divider" />

            {/* Topic Breakdown */}
            <h3 className="section-title" style={{ marginBottom: 16 }}>Topic Performance</h3>
            {topic_breakdown?.map(t => {
                const fillColor = t.accuracy >= 70 ? 'var(--accent-green)' :
                    t.accuracy >= 40 ? 'var(--accent-orange)' : 'var(--accent-red)';
                return (
                    <div className="topic-row" key={t.topic}>
                        <span className="topic-name">{t.topic}</span>
                        <div className="topic-track">
                            <div className="topic-fill" style={{ width: `${t.accuracy}%`, background: fillColor }} />
                        </div>
                        <span className="topic-pct" style={{ color: fillColor }}>{t.accuracy}%</span>
                    </div>
                );
            })}

            <div className="divider" />

            {/* Actions */}
            <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
                <button
                    className="btn btn-primary"
                    style={{ flex: 1 }}
                    onClick={onGetPlan}
                    disabled={planLoading}
                >
                    {planLoading ? (
                        <>
                            <span className="spinner" style={{ width: 18, height: 18, border: '2px solid rgba(255,255,255,0.3)', borderTopColor: '#fff' }} />
                            Generating AI Plan…
                        </>
                    ) : '🧠 Get AI Study Plan'}
                </button>
                <button className="btn btn-ghost" onClick={onRestart}>
                    Retake Test
                </button>
            </div>
        </div>
    );
}
