import { useState } from 'react'
import './index.css'
import StartScreen from './components/StartScreen'
import QuestionCard from './components/QuestionCard'
import ResultsScreen from './components/ResultsScreen'
import StudyPlan from './components/StudyPlan'
import { startSession, getNextQuestion, submitAnswer, getResults, getStudyPlan } from './api'

// App states: 'start' | 'question' | 'loading' | 'results' | 'plan'
export default function App() {
  const [screen, setScreen] = useState('start')
  const [sessionId, setSessionId] = useState(null)
  const [question, setQuestion] = useState(null)
  const [questionNum, setQuestionNum] = useState(1)
  const [currentAbility, setCurrentAbility] = useState(0.5)
  const [feedback, setFeedback] = useState(null)
  const [results, setResults] = useState(null)
  const [studyPlan, setStudyPlan] = useState(null)
  const [submitting, setSubmitting] = useState(false)
  const [planLoading, setPlanLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleStart = async (studentId) => {
    setScreen('loading')
    setError(null)
    try {
      const { session_id } = await startSession(studentId)
      setSessionId(session_id)
      const q = await getNextQuestion(session_id)
      
      if (q.completed || !q.options) {
        setError('No questions available in the database. Please seed the database first.')
        setScreen('start')
        return
      }

      setQuestion(q)
      setCurrentAbility(q.current_ability ?? 0.5)
      setQuestionNum(1)
      setFeedback(null)
      setScreen('question')
    } catch (e) {
      setError(e?.response?.data?.detail || 'Failed to connect to backend. Is the API running?')
      setScreen('start')
    }
  }

  const handleSelect = async (key) => {
    if (submitting || feedback) return
    setSubmitting(true)
    try {
      const fb = await submitAnswer(sessionId, question.question_id, key)
      setCurrentAbility(fb.ability_after)
      setFeedback(fb)
    } catch (e) {
      setError('Error submitting answer.')
    } finally {
      setSubmitting(false)
    }
  }

  const handleNext = async () => {
    setFeedback(null)
    if (questionNum >= (question?.total_questions ?? 10)) {
      // Fetch results
      setScreen('loading')
      try {
        const res = await getResults(sessionId)
        setResults(res)
        setScreen('results')
      } catch (e) {
        setError('Failed to load results.')
        setScreen('start')
      }
      return
    }
    // Fetch next question
    setScreen('loading')
    try {
      const q = await getNextQuestion(sessionId)
      if (q.completed) {
        const res = await getResults(sessionId)
        setResults(res)
        setScreen('results')
        return
      }
      setQuestion(q)
      setCurrentAbility(q.current_ability ?? currentAbility)
      setQuestionNum(prev => prev + 1)
      setScreen('question')
    } catch (e) {
      setError('Failed to load next question.')
      setScreen('start')
    }
  }

  const handleGetPlan = async () => {
    setPlanLoading(true)
    try {
      const plan = await getStudyPlan(sessionId)
      setStudyPlan(plan)
      setScreen('plan')
    } catch (e) {
      setError('Failed to generate study plan. Check your OpenAI API key.')
    } finally {
      setPlanLoading(false)
    }
  }

  const handleRestart = () => {
    setScreen('start')
    setSessionId(null)
    setQuestion(null)
    setQuestionNum(1)
    setCurrentAbility(0.5)
    setFeedback(null)
    setResults(null)
    setStudyPlan(null)
    setError(null)
  }

  return (
    <div className="app-wrapper">
      <div className="container">
        {error && (
          <div style={{
            marginBottom: 16,
            padding: '12px 18px',
            background: 'rgba(239,68,68,0.12)',
            border: '1px solid rgba(239,68,68,0.3)',
            borderRadius: 'var(--radius-md)',
            color: 'var(--accent-red)',
            fontSize: '0.875rem',
          }}>
            ⚠️ {error}
          </div>
        )}

        {screen === 'start' && (
          <StartScreen onStart={handleStart} loading={false} />
        )}

        {screen === 'loading' && (
          <div className="card">
            <div className="loading-wrap">
              <div className="spinner" />
              <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Loading…</p>
            </div>
          </div>
        )}

        {screen === 'question' && question && (
          <QuestionCard
            question={question}
            questionNumber={questionNum}
            totalQuestions={question.total_questions}
            currentAbility={currentAbility}
            feedback={feedback}
            submitting={submitting}
            onSelect={handleSelect}
            onNext={handleNext}
          />
        )}

        {screen === 'results' && results && (
          <ResultsScreen
            results={results}
            onGetPlan={handleGetPlan}
            planLoading={planLoading}
            onRestart={handleRestart}
          />
        )}

        {screen === 'plan' && studyPlan && (
          <StudyPlan plan={studyPlan} onRestart={handleRestart} />
        )}
      </div>
    </div>
  )
}
