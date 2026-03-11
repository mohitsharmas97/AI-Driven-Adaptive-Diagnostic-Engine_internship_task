import axios from 'axios';

const BASE_URL = 'http://localhost:8000';

const api = axios.create({ baseURL: BASE_URL });

export const startSession = (studentId) =>
    api.post('/session/start', { student_id: studentId }).then(r => r.data);

export const getNextQuestion = (sessionId) =>
    api.get(`/session/${sessionId}/next-question`).then(r => r.data);

export const submitAnswer = (sessionId, questionId, selectedAnswer) =>
    api.post(`/session/${sessionId}/submit-answer`, {
        question_id: questionId,
        selected_answer: selectedAnswer,
    }).then(r => r.data);

export const getResults = (sessionId) =>
    api.get(`/session/${sessionId}/results`).then(r => r.data);

export const getStudyPlan = (sessionId) =>
    api.post(`/session/${sessionId}/study-plan`).then(r => r.data);
