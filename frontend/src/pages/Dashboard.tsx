import React from 'react'
import { Link } from 'react-router-dom'
import { Card, StatCard, Button } from '../components/UI'
import { apiClient } from '../services/apiClient'
import type { UserStats } from '../types'

function Dashboard() {
  const [stats, setStats] = React.useState<UserStats | null>(null)
  const [loading, setLoading] = React.useState(true)
  const [error, setError] = React.useState<string | null>(null)

  React.useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await apiClient.getUserStats()
        setStats(data)
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    fetchStats()
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-2 border-primary-600 border-t-secondary-600 mx-auto mb-4"></div>
          <p className="text-dark-200">Loading your dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-12 animate-fadeIn">
      {/* Hero Section */}
      <section className="relative pt-8 pb-16 md:py-20">
        <div className="absolute inset-0 -z-10 bg-gradient-to-br from-primary-600/5 via-transparent to-secondary-600/5 blur-3xl rounded-3xl"></div>
        
        <div className="text-center max-w-3xl mx-auto">
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-serif font-bold mb-4 leading-tight text-dark-900">
            Welcome to <span className="gradient-text">Voyage</span>
          </h1>
          <p className="text-lg md:text-xl text-dark-200 mb-8">
            Your intelligent travel analytics companion. Predict flights, discover hotel recommendations, and unlock travel insights.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/flight-prediction">
              <Button className="w-full sm:w-auto" variant="primary">
                ✈️ Predict Flight Prices
              </Button>
            </Link>
            <Link to="/hotel-recommendations">
              <Button variant="secondary" className="w-full sm:w-auto">
                🏨 Explore Hotels
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Error Message */}
      {error && (
        <div className="card-dark border-l-4 border-red-500 bg-red-50">
          <p className="text-red-700">{error}</p>
        </div>
      )}

      {/* Stats Grid */}
      <section>
        <h2 className="text-2xl md:text-3xl font-serif font-bold text-dark-900 mb-8">Your Activity</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <StatCard
            label="Total Predictions"
            value={stats?.total_predictions || 0}
            icon="📊"
            color="red"
          />
          <StatCard
            label="Flight Predictions"
            value={stats?.flight_predictions || 0}
            icon="✈️"
            color="orange"
          />
          <StatCard
            label="Classifications"
            value={stats?.gender_predictions || 0}
            icon="👤"
            color="purple"
          />
        </div>
      </section>

      {/* Quick Actions */}
      <section>
        <h2 className="text-2xl md:text-3xl font-serif font-bold text-dark-900 mb-8">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Link to="/flight-prediction" className="hover-lift">
            <Card className="h-full">
              <div className="flex flex-col items-center text-center">
                <div className="text-5xl mb-4">✈️</div>
                <h3 className="text-xl font-serif font-bold text-dark-900 mb-2">
                  Flight Prices
                </h3>
                <p className="text-dark-200 text-sm mb-4">
                  Predict flight prices based on your preferences
                </p>
                <Button size="sm" variant="primary">
                  Start Predicting
                </Button>
              </div>
            </Card>
          </Link>

          <Link to="/gender-classification" className="hover-lift">
            <Card className="h-full">
              <div className="flex flex-col items-center text-center">
                <div className="text-5xl mb-4">👤</div>
                <h3 className="text-xl font-serif font-bold text-dark-900 mb-2">
                  Classifications
                </h3>
                <p className="text-dark-200 text-sm mb-4">
                  Analyze travel behavior and predict patterns
                </p>
                <Button size="sm" variant="primary">
                  Analyze Now
                </Button>
              </div>
            </Card>
          </Link>

          <Link to="/hotel-recommendations" className="hover-lift">
            <Card className="h-full">
              <div className="flex flex-col items-center text-center">
                <div className="text-5xl mb-4">🏨</div>
                <h3 className="text-xl font-serif font-bold text-dark-900 mb-2">
                  Hotel Recommendations
                </h3>
                <p className="text-dark-200 text-sm mb-4">
                  Find the perfect hotel for your next trip
                </p>
                <Button size="sm" variant="primary">
                  Explore
                </Button>
              </div>
            </Card>
          </Link>
        </div>
      </section>

      {/* System Status */}
      <section>
        <Card title="System Status">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="flex items-center gap-4">
              <div className="w-3 h-3 rounded-full bg-emerald-500"></div>
              <div>
                <p className="text-dark-200 text-sm">API Status</p>
                <p className="font-semibold text-dark-50">Operational</p>
              </div>
            </div>
            <div>
              <p className="text-dark-200 text-sm mb-1">Last Prediction</p>
              <p className="font-semibold text-dark-50">
                {stats?.last_prediction
                  ? new Date(stats.last_prediction).toLocaleDateString()
                  : 'Never'}
              </p>
            </div>
            <div>
              <p className="text-dark-200 text-sm mb-1">Active Models</p>
              <p className="font-semibold text-dark-50">3 Models</p>
            </div>
          </div>
        </Card>
      </section>
    </div>
  )
}



export default Dashboard
