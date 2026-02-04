/**
 * Home Page Tests
 * Tests for the main landing page component
 */

import { render, screen } from '@testing-library/react'
import Home from '../../src/app/page'

describe('Home Page', () => {
  test('should render the main heading', () => {
    render(<Home />)

    const heading = screen.getByRole('heading', { name: /방화벽 로그 모니터링 시스템/i })
    expect(heading).toBeInTheDocument()
  })

  test('should render the subtitle', () => {
    render(<Home />)

    const subtitle = screen.getByText(/실시간 방화벽 로그 조회 및 분석 시스템/i)
    expect(subtitle).toBeInTheDocument()
  })

  test('should render three feature cards', () => {
    render(<Home />)

    // Check for feature headings
    expect(screen.getByText(/실시간 모니터링/i)).toBeInTheDocument()
    expect(screen.getByText(/알림 설정/i)).toBeInTheDocument()
    expect(screen.getByText(/통계 및 분석/i)).toBeInTheDocument()
  })

  test('should render feature descriptions', () => {
    render(<Home />)

    expect(screen.getByText(/방화벽 로그를 실시간으로 모니터링하고 분석합니다/i)).toBeInTheDocument()
    expect(screen.getByText(/특정 이벤트 발생 시 즉시 알림을 받을 수 있습니다/i)).toBeInTheDocument()
    expect(screen.getByText(/로그 데이터를 시각화하고 패턴을 분석합니다/i)).toBeInTheDocument()
  })

  test('should render dashboard link', () => {
    render(<Home />)

    const dashboardLink = screen.getByRole('link', { name: /대시보드로 이동/i })
    expect(dashboardLink).toBeInTheDocument()
    expect(dashboardLink).toHaveAttribute('href', '/dashboard')
  })

  test('should apply correct styling classes', () => {
    render(<Home />)

    const dashboardLink = screen.getByRole('link', { name: /대시보드로 이동/i })
    expect(dashboardLink).toHaveClass('bg-primary-600')
    expect(dashboardLink).toHaveClass('text-white')
  })

  test('should have proper semantic structure', () => {
    const { container } = render(<Home />)

    // Check for grid layout
    const grid = container.querySelector('.grid')
    expect(grid).toBeInTheDocument()
    expect(grid).toHaveClass('grid-cols-1')
    expect(grid).toHaveClass('md:grid-cols-3')
  })

  test('should render feature cards with proper styling', () => {
    const { container } = render(<Home />)

    // Check for feature cards
    const cards = container.querySelectorAll('.bg-white.p-6.rounded-lg.shadow-md')
    expect(cards).toHaveLength(3)
  })
})
