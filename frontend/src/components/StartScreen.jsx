export default function StartScreen({ onStart, loading }) {
    const handleSubmit = (e) => {
        e.preventDefault();
        const name = e.target.studentId.value.trim();
        if (name) onStart(name);
    };

    return (
        <div className="card">
            {/* Logo */}
            <div className="logo-mark" style={{ marginBottom: 32 }}>
                <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
                    <rect width="28" height="28" rx="8" fill="url(#lg)" />
                    <path d="M8 20L14 8L20 20" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
                    <path d="M10 16h8" stroke="white" strokeWidth="2" strokeLinecap="round" />
                    <defs>
                        <linearGradient id="lg" x1="0" y1="0" x2="28" y2="28">
                            <stop stopColor="#8b5cf6" />
                            <stop offset="1" stopColor="#06b6d4" />
                        </linearGradient>
                    </defs>
                </svg>
                AdaptIQ
            </div>

            <h1 className="hero-title">AI-Powered Adaptive Diagnostics</h1>
            <p className="hero-subtitle">
                Our 1D Item Response Theory engine dynamically calibrates question difficulty<br />
                in real-time to precisely measure your ability score. Answer 10 questions,<br />
                then get an AI-generated personalised study plan.
            </p>

            {/* Features */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 12, marginBottom: 32 }}>
                {[
                    { icon: '⚡', title: 'Adaptive IRT', desc: 'Questions adapt to your level' },
                    { icon: '🧠', title: 'AI Study Plan', desc: 'Personalised by OpenAI GPT' },
                    { icon: '📊', title: 'Deep Analytics', desc: 'Topic-level performance insights' },
                ].map(f => (
                    <div key={f.title} style={{
                        padding: '14px', background: 'var(--bg-surface)', borderRadius: 'var(--radius-md)',
                        border: '1px solid var(--border)', textAlign: 'center'
                    }}>
                        <div style={{ fontSize: '1.5rem', marginBottom: 6 }}>{f.icon}</div>
                        <div style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: 3 }}>{f.title}</div>
                        <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>{f.desc}</div>
                    </div>
                ))}
            </div>

            <div className="divider" />

            <form onSubmit={handleSubmit}>
                <label className="label" style={{ display: 'block', marginBottom: 8 }}>
                    Your Name / Student ID
                </label>
                <input
                    name="studentId"
                    className="input"
                    placeholder="e.g. Mohit Sharma"
                    required
                    autoComplete="off"
                    style={{ marginBottom: 16 }}
                />
                <button className="btn btn-primary w-full" type="submit" disabled={loading}>
                    {loading ? 'Starting…' : 'Begin Diagnostic Test →'}
                </button>
            </form>

            <p style={{ textAlign: 'center', fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: 16 }}>
                Takes approximately 5–10 minutes · 10 adaptive questions
            </p>
        </div>
    );
}
