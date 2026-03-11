import { useState } from 'react';

const OPTION_KEYS = ['A', 'B', 'C', 'D'];

export default function QuestionCard({
    question,
    questionNumber,
    totalQuestions,
    currentAbility,
    feedback,
    submitting,
    onSelect,
    onNext,
}) {
    const [selected, setSelected] = useState(null);

    const handleSelect = (key) => {
        if (feedback || submitting) return;
        setSelected(key);
        onSelect(key);
    };

    const handleNext = () => {
        setSelected(null);
        onNext();
    };

    const progress = ((questionNumber - 1) / totalQuestions) * 100;

    const getOptionClass = (key) => {
        let cls = 'option-btn';
        if (feedback) {
            if (key === feedback.correct_answer) return cls + ' correct';
            if (key === selected && !feedback.is_correct) return cls + ' wrong';
        } else if (key === selected) {
            return cls + ' selected';
        }
        return cls;
    };

    return (
        <div className="card">
            {/* Header */}
            <div className="header-row">
                <div className="logo-mark">
                    <svg width="22" height="22" viewBox="0 0 28 28" fill="none">
                        <rect width="28" height="28" rx="8" fill="url(#lg2)" />
                        <path d="M8 20L14 8L20 20" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
                        <path d="M10 16h8" stroke="white" strokeWidth="2" strokeLinecap="round" />
                        <defs>
                            <linearGradient id="lg2" x1="0" y1="0" x2="28" y2="28">
                                <stop stopColor="#8b5cf6" />
                                <stop offset="1" stopColor="#06b6d4" />
                            </linearGradient>
                        </defs>
                    </svg>
                    AdaptIQ
                </div>
                <span className="topic-badge">📚 {question.topic}</span>
            </div>

            {/* Progress */}
            <div className="progress-meta">
                <span>Question {questionNumber} of {totalQuestions}</span>
                <span>Ability θ = {currentAbility?.toFixed(3)}</span>
            </div>
            <div className="progress-track">
                <div className="progress-fill" style={{ width: `${progress}%` }} />
            </div>

            {/* Ability bar */}
            <div className="ability-bar-wrap" style={{ marginBottom: 24 }}>
                <div className="ability-track">
                    <div className="ability-fill" style={{ width: `${(currentAbility || 0.5) * 100}%` }} />
                </div>
                <div className="ability-labels">
                    <span>Beginner</span>
                    <span>Intermediate</span>
                    <span>Advanced</span>
                </div>
            </div>

            {/* Question */}
            <div className="question-text">{question.text}</div>

            {/* Options */}
            <div className="options-grid">
                {OPTION_KEYS.map(key => (
                    <button
                        key={key}
                        className={getOptionClass(key)}
                        onClick={() => handleSelect(key)}
                        disabled={!!feedback || submitting}
                    >
                        <span className="option-key">{key}</span>
                        <span>{question.options[key]}</span>
                    </button>
                ))}
            </div>

            {/* Feedback */}
            {feedback && (
                <div className={`feedback-banner ${feedback.is_correct ? 'correct' : 'wrong'}`}>
                    <span>{feedback.is_correct ? '✅' : '❌'}</span>
                    <span>
                        {feedback.is_correct
                            ? `Correct! Ability updated: ${feedback.ability_before?.toFixed(3)} → ${feedback.ability_after?.toFixed(3)}`
                            : `Wrong. Correct answer: ${feedback.correct_answer}. Ability: ${feedback.ability_before?.toFixed(3)} → ${feedback.ability_after?.toFixed(3)}`
                        }
                    </span>
                </div>
            )}

            {/* Submit / Next */}
            {!feedback ? (
                <button
                    className="btn btn-primary w-full"
                    onClick={() => selected && onSelect(selected)}
                    disabled={!selected || submitting}
                >
                    {submitting ? 'Checking…' : 'Submit Answer'}
                </button>
            ) : (
                <button className="btn btn-primary w-full" onClick={handleNext}>
                    {questionNumber >= totalQuestions ? 'View Results →' : 'Next Question →'}
                </button>
            )}
        </div>
    );
}
