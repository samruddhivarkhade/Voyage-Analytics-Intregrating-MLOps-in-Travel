# 🎨 Voyage Analytics - Frontend

Modern React TypeScript web application for the Voyage Analytics platform. Built with Vite, Tailwind CSS, and comprehensive error handling.

**Version:** 1.0.0 | **Status:** Production Ready ✅

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Features](#-features)
- [Development](#-development)
- [Components Guide](#-components-guide)
- [State Management](#-state-management)
- [API Integration](#-api-integration)
- [Error Handling](#-error-handling)
- [Building & Deployment](#-building--deployment)
- [Troubleshooting](#-troubleshooting)

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- npm or pnpm
- Backend API running on port 8000 (local) or accessible URL

### Installation

```bash
cd frontend
npm install
```

### Development Server

```bash
npm run dev
```

Access at **http://localhost:5173**

### Build for Production

```bash
npm run build
npm run preview  # Preview the production build locally
```

---

## 📁 Project Structure

```
frontend/
├── src/
│   ├── main.tsx                    Entry point with providers (ToastProvider, React Router)
│   ├── App.tsx                     Main app with routes, ErrorBoundary
│   ├── index.css                   Global styles
│   │
│   ├── pages/                      Page components (lazy-loaded)
│   │   ├── Login.tsx              Authentication
│   │   ├── Register.tsx           Account creation
│   │   ├── Dashboard.tsx          Main dashboard with stats
│   │   ├── FlightPrediction.tsx   Flight price form
│   │   ├── GenderClassification.tsx Gender prediction form
│   │   ├── HotelRecommendation.tsx Hotel recommendations form
│   │   ├── PredictionHistory.tsx  History viewer (future)
│   │   ├── AdminDashboard.tsx     Admin panel (future)
│   │   ├── ErrorPage.tsx          Generic error display
│   │   └── NotFoundPage.tsx       404 page
│   │
│   ├── components/                Reusable components
│   │   ├── ErrorBoundary.tsx      React error boundary
│   │   ├── Header.tsx             Navigation header
│   │   ├── Footer.tsx             Footer with links
│   │   ├── Layout.tsx             Protected route layout
│   │   ├── Navigation.tsx         Mobile navigation
│   │   ├── ToastContainer.tsx     Toast notifications
│   │   ├── UI.tsx                 Reusable UI components (Button, Card, Input, etc.)
│   │   └── UIEnhanced.tsx         Enhanced components
│   │
│   ├── services/
│   │   └── apiClient.ts           Axios HTTP client with all endpoints
│   │
│   ├── store/
│   │   └── authStore.ts           Zustand auth state management
│   │
│   ├── hooks/
│   │   └── useToast.ts            Custom hook for toast notifications
│   │
│   ├── context/
│   │   └── ToastContext.tsx       Global toast provider & hook
│   │
│   ├── utils/
│   │   └── errorHandler.ts        Error formatting and logging utilities
│   │
│   └── types/
│       └── index.ts               TypeScript type definitions
│
├── public/                         Static assets
├── package.json
├── tsconfig.json
├── vite.config.ts                 Vite configuration
├── tailwind.config.js             Tailwind CSS config
└── README.md
```

---

## ✨ Features

### 🔐 Authentication
- User registration and login
- JWT token management via secure storage
- Protected routes with automatic redirect
- Logout functionality

### 📊 Dashboard
- Real-time statistics (total predictions, by type)
- Quick access to prediction tools
- User profile information

### 🔮 Predictions
- **Flight Price Prediction** - Input form with feature validation
- **Gender Classification** - Multi-option form
- **Hotel Recommendations** - Profile-based suggestions with visualizations

### 🛡️ Error Handling
- Error Boundary catches component crashes
- 404 page for invalid routes
- Toast notifications for user feedback
- Error logging with context
- Graceful fallback UI

### 📱 Responsive Design
- Mobile-first approach with Tailwind CSS
- Works on all screen sizes
- Touch-friendly UI on mobile

### ⚡ Performance
- Lazy-loaded pages with React Router
- Tree-shaking with Vite
- Minified production builds
- ~250KB bundle size

---

## 👨‍💻 Development

### Available Commands

```bash
npm run dev         # Start dev server with HMR
npm run build       # Build for production
npm run preview     # Preview production build
npm run lint        # Run ESLint
npm run type-check  # Check TypeScript errors
npm run format      # Format code with Prettier (if configured)
```

### Code Style

This project uses:
- **ESLint** for code linting
- **Prettier** for formatting (configure in `.prettierrc`)
- **TypeScript** for type safety

---

## 🧩 Components Guide

### Layout Component

```tsx
// Auto-protected route with Header + Footer
import Layout from './components/Layout'

// Inside Route
<Route element={<Layout />}>
  <Route path="/" element={<Dashboard />} />
</Route>
```

### UI Components (in UI.tsx)

```tsx
import { Button, Card, Input, Select, Spinner } from './components/UI'

// Button variants
<Button variant="primary">Primary</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="danger">Danger</Button>

// Card layout
<Card title="Title" className="...">
  Content goes here
</Card>

// Responsive input
<Input type="email" placeholder="Email" />
```

### Toast Notifications

```tsx
import { useToastContext } from './context/ToastContext'

function MyComponent() {
  const toast = useToastContext()
  
  const handleClick = () => {
    toast.success('Operation successful!')
    toast.error('Something went wrong')
    toast.info('Just FYI...')
    toast.warning('Be careful!')
  }
  
  return <button onClick={handleClick}>Show Toast</button>
}
```

### Error Boundary

Automatically wraps the entire app in `App.tsx`:

```tsx
<ErrorBoundary>
  <BrowserRouter>
    {/* routes */}
  </BrowserRouter>
</ErrorBoundary>
```

Catches errors automatically and displays fallback UI.

---

## 🔄 State Management

### Authentication (Zustand)

```tsx
import { useAuthStore } from './store/authStore'

function MyComponent() {
  const { user, isAuthenticated, login, logout } = useAuthStore()
  
  return (
    <>
      {isAuthenticated && <p>Hello, {user?.name}</p>}
      <button onClick={logout}>Logout</button>
    </>
  )
}
```

### Toast Context

Global toast notifications accessible anywhere:

```tsx
const toast = useToastContext()
toast.success('Message', 3000) // Auto-dismiss after 3 seconds
```

---

## 🔌 API Integration

### API Client (services/apiClient.ts)

```tsx
import apiClient from './services/apiClient'

// Authentication
await apiClient.login({ email, password })
await apiClient.register({ email, name, password })
await apiClient.getCurrentUser()

// Predictions
await apiClient.predictFlightPrice({...})
await apiClient.predictGender({...})
await apiClient.recommendHotels({...})

// Statistics
const stats = await apiClient.getUserStats()

// Health check
await apiClient.healthCheck()
```

All requests automatically include JWT token in headers. 401 responses automatically redirect to login.

### Configuration

Edit `src/services/apiClient.ts` to change API base URL:

```typescript
const API_BASE_URL = process.env.VITE_API_URL || 'http://localhost:8000'
```

Or set `VITE_API_URL` in `.env`:
```
VITE_API_URL=http://localhost:8000
```

---

## 🛡️ Error Handling

### Components with Error Handling

All prediction pages use try-catch blocks:

```tsx
try {
  const response = await apiClient.predictFlightPrice(data)
  toast.success('Prediction successful!')
  // Handle response
} catch (error) {
  logError(error, 'FlightPrediction')
  const message = formatErrorMessage(error)
  toast.error(message)
}
```

### Error Utilities (utils/errorHandler.ts)

```tsx
import {
  handleApiError,
  logError,
  formatErrorMessage,
  isErrorStatus,
  isNetworkError,
  redirectToErrorPage
} from './utils/errorHandler'

// Handle any error
const errorResponse = handleApiError(error)
console.log(errorResponse.status, errorResponse.message)

// Check specific error types
if (isNetworkError(error)) {
  toast.warning('Network connection lost')
}

// Redirect to error page
redirectToErrorPage(500, 'Server Error', 'Database connection failed')
```

---

## 🏗️ Building & Deployment

### Local Development Build

```bash
npm run build
npm run preview
```

### Docker Build

```dockerfile
# In Dockerfile (multi-stage)
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM node:18-alpine
RUN npm install -g serve
COPY --from=builder /app/dist /app
EXPOSE 3000
CMD ["serve", "-s", "/app", "-l", "3000"]
```

### Deployment Platforms

#### Vercel (Recommended)
```bash
npm i -g vercel
vercel
```

#### Netlify
```bash
npm i -g netlify-cli
netlify deploy --prod --dir=dist
```

#### Docker Compose
```bash
docker-compose build frontend
docker-compose up frontend
```

#### Static Hosting (AWS S3, GitHub Pages, etc.)
```bash
npm run build
# Upload dist/ folder to your hosting
```

---

## 🐛 Troubleshooting

### "Cannot find module" errors
```bash
# Clear node_modules and reinstall
rm -rf node_modules
npm install
```

### API connection refused
```typescript
// Check API URL in src/services/apiClient.ts
// Verify backend is running on http://localhost:8000

// For Docker:
const API_BASE_URL = 'http://host.docker.internal:8000'
```

### Port 5173 already in use
```bash
# Use a different port
npm run dev -- --port 3000
```

### CORS errors from backend
The backend (ml-service/app/main.py) should have CORS enabled for `http://localhost:5173`

### TypeScript errors
```bash
npm run type-check  # Check errors
# Fix in editor or run
npm run lint -- --fix  # Auto-fix linting issues
```

### Hot Module Replacement (HMR) not working
Add to `vite.config.ts`:
```typescript
export default defineConfig({
  server: {
    middlewareMode: false,
    hmr: {
      host: 'localhost',
      port: 5173
    }
  }
})
```

---

## 📚 TypeScript Types

All types defined in `src/types/index.ts`:

```typescript
interface User {
  id: string
  email: string
  name: string
  is_admin: boolean
  created_at: string
}

interface FlightPrediction {
  airline: string
  route: string
  distance: number
  // ... more fields
}

interface HotelRecommendation {
  hotel_id: string
  hotel_name: string
  match_score: number
  // ... more fields
}
```

Import types:
```tsx
import type { User, FlightPrediction, HotelRecommendation } from './types'
```

---

## 🎨 Styling with Tailwind CSS

All components use Tailwind utility classes. Config in `tailwind.config.js`.

### Common Patterns

```tsx
// Responsive grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">

// Flexbox centering
<div className="flex items-center justify-center min-h-screen">

// Hover states
<button className="bg-primary-600 hover:bg-primary-700 transition">

// Mobile-first
<div className="text-sm md:text-base lg:text-lg">
```

---

## 🚀 Performance Tips

1. **Lazy load pages** - Routes are code-split automatically
2. **Optimize images** - Use WebP format when possible
3. **Cache busting** - Vite handles this automatically
4. **Tree shaking** - Unused code removed in production
5. **Minification** - Automatic in production build

---

## 📱 Browser Support

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

---

## 📞 Support

**Issues?** Check [../README.md](../README.md) for general project info  
**Backend?** See [../ml-service/README.md](../ml-service/README.md)  
**Error handling?** Review [src/utils/errorHandler.ts](src/utils/errorHandler.ts)

---

**Last Updated:** April 19, 2026 | **Version:** 1.0.0

## Project Structure

```
frontend/
├── src/
│   ├── components/        # Reusable UI components
│   │   ├── Layout.tsx     # Main layout wrapper
│   │   ├── Navigation.tsx # Sidebar navigation
│   │   └── UI.tsx         # Common UI components
│   ├── pages/             # Page components
│   │   ├── Login.tsx
│   │   ├── Register.tsx
│   │   ├── Dashboard.tsx
│   │   ├── FlightPrediction.tsx
│   │   ├── GenderClassification.tsx
│   │   ├── PredictionHistory.tsx
│   │   └── AdminDashboard.tsx
│   ├── services/          # API client
│   │   └── apiClient.ts
│   ├── store/             # Zustand stores
│   │   └── authStore.ts
│   ├── types/             # TypeScript types
│   │   └── index.ts
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── public/
├── index.html
├── package.json
├── vite.config.ts
├── tsconfig.json
└── tailwind.config.js
```

## Features

- ✨ User authentication (login/register)
- 🎯 Flight price prediction interface
- 👤 Gender classification interface
- 📊 Dashboard with statistics
- 📜 Prediction history tracking
- ⚙️ Admin dashboard for monitoring
- 🎨 Responsive UI with Tailwind CSS
- 📱 Mobile-friendly design
- 🔒 Protected routes with authentication

## Technologies

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Fast build tool
- **React Router v6** - Routing
- **Zustand** - State management
- **Axios** - HTTP client
- **Tailwind CSS** - Styling
- **React Hook Form** - Form handling
- **Recharts** - Data visualization

## Environment Variables

Create a `.env.local` file:

```
VITE_API_URL=http://localhost:8000/v1
```

## API Integration

The frontend connects to the FastAPI backend at `http://localhost:8000/v1`

### Available Endpoints

- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `GET /auth/me` - Get current user
- `POST /predict` - Flight price prediction
- `POST /predict-gender` - Gender classification
- `GET /predictions` - Get prediction history
- `GET /stats` - Get user statistics
- `GET /health` - Health check

## Building for Production

```bash
npm run build
npm run preview
```

The build output will be in the `dist/` folder.

### Deployment

1. Build the project:
   ```bash
   npm run build
   ```

2. Deploy the `dist/` folder to your hosting service (Vercel, Netlify, etc.)

3. Update the API URL in environment variables to point to production backend

## Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install
COPY . .
RUN pnpm build

FROM node:18-alpine
WORKDIR /app
RUN npm install -g serve
COPY --from=builder /app/dist ./dist
EXPOSE 3000
CMD ["serve", "-s", "dist", "-l", "3000"]
```

Build and run:
```bash
docker build -t voyage-frontend .
docker run -p 3000:3000 voyage-frontend
```

## Troubleshooting

### Port 3000 already in use
```bash
# Change the port in vite.config.ts
# or kill the process on port 3000
```

### API connection failed
- Ensure backend is running on `http://localhost:8000`
- Check `VITE_API_URL` environment variable
- Check browser console for CORS errors

### Build errors
```bash
npm run type-check  # Check TypeScript errors
npm run lint        # Check linting errors
```

## Development Guidelines

- Use TypeScript for all new code
- Follow ESLint rules
- Use Zustand for global state
- Keep components small and reusable
- Use Tailwind CSS for styling
- Add PropTypes for runtime validation

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and linting
4. Submit a pull request

## License

MIT
