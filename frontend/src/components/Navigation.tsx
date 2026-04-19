import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'

function Navigation() {
  const navigate = useNavigate()
  const location = useLocation()
  const { user, logout } = useAuthStore()

  const navItems = [
    { path: '/', label: 'Dashboard', icon: '📊' },
    { path: '/flight-prediction', label: 'Flight Prices', icon: '✈️' },
    { path: '/gender-classification', label: 'Gender Classification', icon: '👤' },
    { path: '/hotel-recommendations', label: 'Hotel Recommendations', icon: '🏨' },
  ]

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav className="w-64 bg-gradient-to-b from-blue-600 to-blue-800 text-white shadow-lg">
      <div className="p-6 border-b border-blue-700">
        <h1 className="text-2xl font-bold">🌍 Voyage</h1>
        <p className="text-blue-200 text-sm">Analytics Hub</p>
      </div>

      <div className="p-4 border-b border-blue-700">
        <p className="text-sm text-blue-100">Logged in as</p>
        <p className="font-semibold truncate">{user?.email}</p>
        {user?.role === 'admin' && (
          <span className="inline-block mt-2 px-2 py-1 bg-blue-500 text-xs rounded">Admin</span>
        )}
      </div>

      <ul className="py-4">
        {navItems.map((item) => (
          <li key={item.path}>
            <Link
              to={item.path}
              className={`block px-6 py-3 transition ${
                location.pathname === item.path
                  ? 'bg-blue-500 border-l-4 border-white'
                  : 'hover:bg-blue-700'
              }`}
            >
              <span className="mr-3">{item.icon}</span>
              {item.label}
            </Link>
          </li>
        ))}
      </ul>

      <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-blue-700">
        <button
          onClick={handleLogout}
          className="w-full px-4 py-2 bg-red-600 hover:bg-red-700 rounded transition text-sm font-semibold"
        >
          Logout
        </button>
      </div>
    </nav>
  )
}

export default Navigation
