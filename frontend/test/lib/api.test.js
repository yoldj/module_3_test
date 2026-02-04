/**
 * API Client Tests
 * Tests for the API client module
 */

import api, { APIError } from '../../src/lib/api'

describe('API Client', () => {
  beforeEach(() => {
    fetch.mockClear()
  })

  describe('APIError', () => {
    test('should create APIError with message, status, and data', () => {
      const error = new APIError('Test error', 404, { detail: 'Not found' })

      expect(error.message).toBe('Test error')
      expect(error.status).toBe(404)
      expect(error.data).toEqual({ detail: 'Not found' })
      expect(error.name).toBe('APIError')
    })
  })

  describe('logs API', () => {
    test('getAll should fetch all logs', async () => {
      const mockLogs = [
        { id: 1, message: 'Log 1' },
        { id: 2, message: 'Log 2' }
      ]

      fetch.mockResolvedValueOnce({
        ok: true,
        headers: new Headers({ 'content-type': 'application/json' }),
        json: async () => mockLogs
      })

      const result = await api.logs.getAll()

      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/logs',
        expect.objectContaining({
          headers: expect.objectContaining({
            'Content-Type': 'application/json'
          })
        })
      )
      expect(result).toEqual(mockLogs)
    })

    test('getAll should handle query parameters', async () => {
      const mockLogs = [{ id: 1, message: 'Filtered log' }]

      fetch.mockResolvedValueOnce({
        ok: true,
        headers: new Headers({ 'content-type': 'application/json' }),
        json: async () => mockLogs
      })

      await api.logs.getAll({ page: 1, limit: 10 })

      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/logs?page=1&limit=10',
        expect.any(Object)
      )
    })

    test('getById should fetch a specific log', async () => {
      const mockLog = { id: 1, message: 'Test log' }

      fetch.mockResolvedValueOnce({
        ok: true,
        headers: new Headers({ 'content-type': 'application/json' }),
        json: async () => mockLog
      })

      const result = await api.logs.getById(1)

      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/logs/1',
        expect.any(Object)
      )
      expect(result).toEqual(mockLog)
    })

    test('create should post a new log', async () => {
      const newLog = { message: 'New log' }
      const createdLog = { id: 3, ...newLog }

      fetch.mockResolvedValueOnce({
        ok: true,
        headers: new Headers({ 'content-type': 'application/json' }),
        json: async () => createdLog
      })

      const result = await api.logs.create(newLog)

      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/logs',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(newLog)
        })
      )
      expect(result).toEqual(createdLog)
    })

    test('getStats should fetch log statistics', async () => {
      const mockStats = { total: 100, blocked: 20 }

      fetch.mockResolvedValueOnce({
        ok: true,
        headers: new Headers({ 'content-type': 'application/json' }),
        json: async () => mockStats
      })

      const result = await api.logs.getStats()

      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/logs/stats',
        expect.any(Object)
      )
      expect(result).toEqual(mockStats)
    })
  })

  describe('users API', () => {
    test('getAll should fetch all users', async () => {
      const mockUsers = [
        { id: 1, username: 'user1' },
        { id: 2, username: 'user2' }
      ]

      fetch.mockResolvedValueOnce({
        ok: true,
        headers: new Headers({ 'content-type': 'application/json' }),
        json: async () => mockUsers
      })

      const result = await api.users.getAll()

      expect(result).toEqual(mockUsers)
    })

    test('update should update a user', async () => {
      const updateData = { username: 'updated_user' }
      const updatedUser = { id: 1, ...updateData }

      fetch.mockResolvedValueOnce({
        ok: true,
        headers: new Headers({ 'content-type': 'application/json' }),
        json: async () => updatedUser
      })

      const result = await api.users.update(1, updateData)

      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/users/1',
        expect.objectContaining({
          method: 'PUT',
          body: JSON.stringify(updateData)
        })
      )
      expect(result).toEqual(updatedUser)
    })

    test('delete should delete a user', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        headers: new Headers({ 'content-type': 'application/json' }),
        json: async () => ({ success: true })
      })

      await api.users.delete(1)

      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/users/1',
        expect.objectContaining({
          method: 'DELETE'
        })
      )
    })
  })

  describe('auth API', () => {
    test('login should authenticate user', async () => {
      const mockResponse = { token: 'abc123', user: { id: 1, username: 'test' } }

      fetch.mockResolvedValueOnce({
        ok: true,
        headers: new Headers({ 'content-type': 'application/json' }),
        json: async () => mockResponse
      })

      const result = await api.auth.login('test', 'password')

      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/auth/login',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ username: 'test', password: 'password' })
        })
      )
      expect(result).toEqual(mockResponse)
    })

    test('logout should call logout endpoint', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        headers: new Headers({ 'content-type': 'application/json' }),
        json: async () => ({ success: true })
      })

      await api.auth.logout()

      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/auth/logout',
        expect.objectContaining({
          method: 'POST'
        })
      )
    })

    test('getCurrentUser should fetch current user info', async () => {
      const mockUser = { id: 1, username: 'test' }

      fetch.mockResolvedValueOnce({
        ok: true,
        headers: new Headers({ 'content-type': 'application/json' }),
        json: async () => mockUser
      })

      const result = await api.auth.getCurrentUser()

      expect(result).toEqual(mockUser)
    })
  })

  describe('alerts API', () => {
    test('create should create a new alert', async () => {
      const newAlert = { name: 'Test Alert', condition: 'high_traffic' }
      const createdAlert = { id: 1, ...newAlert }

      fetch.mockResolvedValueOnce({
        ok: true,
        headers: new Headers({ 'content-type': 'application/json' }),
        json: async () => createdAlert
      })

      const result = await api.alerts.create(newAlert)

      expect(result).toEqual(createdAlert)
    })

    test('update should update an alert', async () => {
      const updateData = { name: 'Updated Alert' }
      const updatedAlert = { id: 1, ...updateData }

      fetch.mockResolvedValueOnce({
        ok: true,
        headers: new Headers({ 'content-type': 'application/json' }),
        json: async () => updatedAlert
      })

      const result = await api.alerts.update(1, updateData)

      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/alerts/1',
        expect.objectContaining({
          method: 'PUT'
        })
      )
    })
  })

  describe('settings API', () => {
    test('getByKey should fetch a specific setting', async () => {
      const mockSetting = { key: 'theme', value: 'dark' }

      fetch.mockResolvedValueOnce({
        ok: true,
        headers: new Headers({ 'content-type': 'application/json' }),
        json: async () => mockSetting
      })

      const result = await api.settings.getByKey('theme')

      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/settings/theme',
        expect.any(Object)
      )
      expect(result).toEqual(mockSetting)
    })

    test('update should update a setting', async () => {
      const updateData = { value: 'light' }

      fetch.mockResolvedValueOnce({
        ok: true,
        headers: new Headers({ 'content-type': 'application/json' }),
        json: async () => ({ key: 'theme', ...updateData })
      })

      await api.settings.update('theme', updateData)

      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/settings/theme',
        expect.objectContaining({
          method: 'PUT',
          body: JSON.stringify(updateData)
        })
      )
    })
  })

  describe('Error Handling', () => {
    test('should throw APIError on HTTP error response', async () => {
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 404,
        headers: new Headers({ 'content-type': 'application/json' }),
        json: async () => ({ detail: 'Not found' })
      })

      await expect(api.logs.getById(999)).rejects.toThrow(APIError)
      await expect(api.logs.getById(999)).rejects.toThrow('Not found')
    })

    test('should handle network errors', async () => {
      fetch.mockRejectedValueOnce(new Error('Network error'))

      await expect(api.logs.getAll()).rejects.toThrow(APIError)
    })

    test('should handle non-JSON responses', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        headers: new Headers({ 'content-type': 'text/plain' }),
        text: async () => 'Plain text response'
      })

      const result = await api.logs.getAll()

      expect(result).toBe('Plain text response')
    })

    test('should use fallback error message when detail is not provided', async () => {
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
        headers: new Headers({ 'content-type': 'application/json' }),
        json: async () => ({})
      })

      await expect(api.logs.getAll()).rejects.toThrow('An error occurred')
    })
  })
})
