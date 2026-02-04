import '@testing-library/jest-dom'

// Mock environment variables
process.env.NEXT_PUBLIC_API_URL = 'http://localhost:8000/api/v1'

// Mock fetch globally
global.fetch = jest.fn()

beforeEach(() => {
  fetch.mockClear()
})
