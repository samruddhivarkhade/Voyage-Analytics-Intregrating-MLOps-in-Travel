import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'

function Header() {
  const navigate = useNavigate()
  const location = useLocation()
  const { isAuthenticated, user, logout } = useAuthStore()

  const navLinks = [
    { path: '/', label: 'Dashboard' },
    { path: '/flight-prediction', label: 'Flight Prices' },
    { path: '/gender-classification', label: 'Gender' },
    { path: '/hotel-recommendations', label: 'Hotels' },
  ]

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-surface/95 backdrop-blur-xs border-b border-primary-600/10 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 md:h-20">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 group">
            <div className="text-2xl md:text-3xl font-serif font-bold gradient-text">
              ✈️ Voyage
            </div>
          </Link>

          {/* Center Navigation - Desktop Only */}
          {isAuthenticated && (
            <nav className="hidden md:flex items-center gap-8">
              {navLinks.map((link) => (
                <Link
                  key={link.path}
                  to={link.path}
                  className={`text-sm font-medium transition-colors relative pb-1 ${
                    location.pathname === link.path
                      ? 'text-primary-600'
                      : 'text-dark-200 hover:text-primary-600'
                  } ${
                    location.pathname === link.path
                      ? 'after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-gradient-warm'
                      : ''
                  }`}
                >
                  {link.label}
                </Link>
              ))}
            </nav>
          )}

          {/* Right Actions */}
          <div className="flex items-center gap-4">
            {isAuthenticated && (
              <div className="flex items-center gap-3">
                <span className="text-xs md:text-sm text-dark-200">{user?.email}</span>
                <button
                  onClick={handleLogout}
                  className="px-4 py-2 text-sm font-medium rounded-full bg-red-600 hover:bg-red-700 text-white transition-all duration-200 shadow-md hover:shadow-lg"
                >
                  Logout
                </button>
              </div>
            )}

            {!isAuthenticated && (
              <div className="flex items-center gap-2">
                <Link
                  to="/login"
                  className="px-3 md:px-4 py-1.5 md:py-2 text-sm font-medium text-dark-200 hover:text-primary-600 transition-colors"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="px-3 md:px-4 py-1.5 md:py-2 text-sm font-medium rounded-full bg-gradient-warm text-white font-semibold hover-lift"
                >
                  Sign Up
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
