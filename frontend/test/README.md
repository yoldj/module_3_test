# Frontend Testing Guide

## 개요

이 디렉토리는 방화벽 로그 모니터링 시스템의 프론트엔드 테스트 코드를 포함합니다.

## 디렉토리 구조

```
test/
├── lib/              # 유틸리티 및 API 클라이언트 테스트
│   └── api.test.js  # API 클라이언트 테스트
├── app/             # 페이지 컴포넌트 테스트
│   └── page.test.js # Home 페이지 테스트
├── components/      # 재사용 가능한 컴포넌트 테스트 (향후 추가)
└── README.md       # 이 파일
```

## 테스트 환경 설정

### 필수 패키지

- `jest`: 테스트 프레임워크
- `@testing-library/react`: React 컴포넌트 테스팅
- `@testing-library/jest-dom`: DOM 매처 확장
- `@testing-library/user-event`: 사용자 이벤트 시뮬레이션
- `jest-environment-jsdom`: 브라우저 환경 시뮬레이션

### 설치 방법

```bash
npm install --save-dev jest @testing-library/react @testing-library/jest-dom @testing-library/user-event jest-environment-jsdom
```

## 테스트 실행

### 기본 실행
```bash
npm test
```

### Watch 모드 (파일 변경 감지)
```bash
npm run test:watch
```

### 커버리지 리포트 생성
```bash
npm run test:coverage
```

## 테스트 작성 가이드

### 1. API 테스트

API 클라이언트 테스트는 `test/lib/` 디렉토리에 작성합니다.

```javascript
// test/lib/api.test.js 예시
import api from '../../src/lib/api'

describe('API Client', () => {
  beforeEach(() => {
    fetch.mockClear()
  })

  test('should fetch data', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      headers: new Headers({ 'content-type': 'application/json' }),
      json: async () => ({ data: 'test' })
    })

    const result = await api.logs.getAll()
    expect(result).toEqual({ data: 'test' })
  })
})
```

### 2. 컴포넌트 테스트

React 컴포넌트 테스트는 `test/app/` 또는 `test/components/` 디렉토리에 작성합니다.

```javascript
// test/app/page.test.js 예시
import { render, screen } from '@testing-library/react'
import Home from '../../src/app/page'

describe('Home Page', () => {
  test('should render heading', () => {
    render(<Home />)
    const heading = screen.getByRole('heading', { name: /방화벽/i })
    expect(heading).toBeInTheDocument()
  })
})
```

### 3. Mock 사용

`jest.setup.js`에서 전역 mock이 설정되어 있습니다:

- `fetch`: 모든 API 호출을 mock
- 환경 변수: `NEXT_PUBLIC_API_URL` 등

추가 mock이 필요한 경우 각 테스트 파일에서 설정할 수 있습니다.

## 베스트 프랙티스

### 1. 테스트 격리
각 테스트는 독립적으로 실행되어야 합니다. `beforeEach`를 사용하여 테스트 간 상태를 초기화하세요.

```javascript
beforeEach(() => {
  fetch.mockClear()
})
```

### 2. 의미 있는 테스트 이름
테스트 이름은 명확하고 구체적이어야 합니다.

```javascript
// Good
test('should fetch all logs with pagination parameters', ...)

// Bad
test('test logs', ...)
```

### 3. AAA 패턴 사용
- **Arrange**: 테스트 설정
- **Act**: 테스트할 동작 실행
- **Assert**: 결과 검증

```javascript
test('should create a new user', async () => {
  // Arrange
  const newUser = { username: 'test' }
  fetch.mockResolvedValueOnce({ ok: true, json: async () => newUser })

  // Act
  const result = await api.users.create(newUser)

  // Assert
  expect(result).toEqual(newUser)
})
```

### 4. 접근성 우선 쿼리 사용
React Testing Library의 권장 쿼리 우선순위:
1. `getByRole`
2. `getByLabelText`
3. `getByPlaceholderText`
4. `getByText`
5. `getByTestId` (최후의 수단)

```javascript
// Good
const button = screen.getByRole('button', { name: /submit/i })

// Avoid
const button = screen.getByTestId('submit-button')
```

## 문제 해결

### Jest가 ES6 모듈을 인식하지 못하는 경우
`jest.config.js`에서 `transformIgnorePatterns`를 확인하세요.

### fetch is not defined 에러
`jest.setup.js`에서 fetch mock이 설정되어 있는지 확인하세요.

### React 컴포넌트 렌더링 오류
`testEnvironment`가 `jest-environment-jsdom`으로 설정되어 있는지 확인하세요.

## 커버리지 목표

- **Line Coverage**: 80% 이상
- **Branch Coverage**: 75% 이상
- **Function Coverage**: 80% 이상
- **Statement Coverage**: 80% 이상

## 참고 자료

- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [Testing Library Queries](https://testing-library.com/docs/queries/about)
- [Jest DOM Matchers](https://github.com/testing-library/jest-dom)
