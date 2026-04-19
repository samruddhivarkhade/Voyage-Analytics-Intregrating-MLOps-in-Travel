import React from 'react'
import { Card, Input, Select, Button, StatCard } from '../components/UI'
import { apiClient } from '../services/apiClient'
import type { HotelRecommendationRequest, HotelRecommendation } from '../types'

interface RecommendationResult {
  recommendations: HotelRecommendation[]
  total_recommendations: number
}

function HotelRecommendation() {
  const [formData, setFormData] = React.useState<HotelRecommendationRequest>({
    days: 3,
    month: new Date().getMonth() + 1,
    age: 30,
    gender: 'male',
    budget: 'mid',
    company: '4You',
    top_n: 5,
  })

  const [results, setResults] = React.useState<RecommendationResult | null>(null)
  const [loading, setLoading] = React.useState(false)
  const [error, setError] = React.useState<string | null>(null)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: ['days', 'month', 'age', 'top_n'].includes(name) ? parseInt(value) : value,
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResults(null)

    try {
      const response = await apiClient.recommendHotels(formData)
      setResults(response)
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || 'Failed to get recommendations. Please try again.'
      setError(errorMsg)
      console.error('Hotel recommendation error:', err)
    } finally {
      setLoading(false)
    }
  }

  const companies = ['4You', 'Acme Factory', 'Monsters CYA', 'Umbrella LTDA', 'Wonka Company']
  const genders = ['male', 'female', 'unknown']
  const budgets = ['budget', 'mid', 'luxury']

  return (
    <div className="space-y-8">
      <div className="mb-8">
        <h1 className="text-4xl font-serif font-bold mb-2 text-dark-900">🏨 Hotel Recommendations</h1>
        <p className="text-dark-200">Get personalized hotel recommendations based on your profile</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Filters */}
        <div className="lg:col-span-1">
          <Card title="Your Profile">
            <form onSubmit={handleSubmit} className="space-y-4">
              <Input
                label="Days Staying"
                type="number"
                name="days"
                value={formData.days}
                onChange={handleChange}
                min="1"
                max="30"
                required
              />

              <Input
                label="Travel Month"
                type="number"
                name="month"
                value={formData.month}
                onChange={handleChange}
                min="1"
                max="12"
                required
              />

              <Input
                label="Your Age"
                type="number"
                name="age"
                value={formData.age}
                onChange={handleChange}
                min="18"
                max="100"
                required
              />

              <Select
                label="Gender"
                name="gender"
                value={formData.gender}
                onChange={handleChange}
                options={genders.map((g) => ({
                  value: g,
                  label: g.charAt(0).toUpperCase() + g.slice(1),
                }))}
              />

              <Select
                label="Budget Type"
                name="budget"
                value={formData.budget}
                onChange={handleChange}
                options={budgets.map((b) => ({
                  value: b,
                  label: b.charAt(0).toUpperCase() + b.slice(1),
                }))}
              />

              <Select
                label="Company"
                name="company"
                value={formData.company}
                onChange={handleChange}
                options={companies.map((c) => ({
                  value: c,
                  label: c,
                }))}
              />

              <Input
                label="Number of Recommendations"
                type="number"
                name="top_n"
                value={formData.top_n}
                onChange={handleChange}
                min="1"
                max="10"
              />

              <Button type="submit" disabled={loading} className="w-full">
                {loading ? 'Finding Hotels...' : 'Get Recommendations'}
              </Button>
            </form>
          </Card>
        </div>

        {/* Results */}
        <div className="lg:col-span-3">
          {error && (
            <Card title="Error">
              <div className="text-red-700 text-sm">{error}</div>
            </Card>
          )}

          {results && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 ">
                <StatCard
                  className='text-black-700'
                  label="Hotels Found"
                  value={results.total_recommendations.toString()}
                  icon="🏨"
                />
                <StatCard
                  label="Avg Match Score"
                  value={
                    (
                      results.recommendations.reduce((sum, r) => sum + r.match_score, 0) /
                      results.recommendations.length
                    ).toFixed(1)
                  }
                  icon="⭐"
                />
              </div>

              <div className="space-y-4">
                {results.recommendations.map((rec) => (
                  <Card key={rec.rank} title={`#${rec.rank} - ${rec.hotel}`}>
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-gray-600 text-sm">Hotel Name</p>
                          <p className="font-semibold text-lg">{rec.hotel}</p>
                        </div>
                        <div className="text-right">
                          <p className="text-gray-600 text-sm">Match Score</p>
                          <p className="font-bold text-2xl text-green-600">{rec.match_score.toFixed(1)}%</p>
                        </div>
                      </div>

                      <div className="bg-gradient-to-r from-green-100 to-blue-100 rounded-lg p-3">
                        <div className="w-full bg-gray-300 rounded-full h-2.5">
                          <div
                            className="bg-gradient-to-r from-green-500 to-blue-500 h-2.5 rounded-full"
                            style={{ width: `${Math.min(rec.match_score, 100)}%` }}
                          ></div>
                        </div>
                        <p className="text-xs text-gray-600 mt-2">
                          Based on your profile match with this hotel's typical guests
                        </p>
                      </div>

                      <div className="grid grid-cols-2 gap-3 pt-2">
                        <div className="p-2 bg-blue-50 rounded">
                          <p className="text-xs text-gray-600">Rank</p>
                          <p className="font-semibold">#{rec.rank}</p>
                        </div>
                        <div className="p-2 bg-green-50 rounded">
                          <p className="text-xs text-gray-600">Confidence</p>
                          <p className="font-semibold">{(rec.match_score / 100).toFixed(2)}</p>
                        </div>
                      </div>

                      <Button variant="primary" className="w-full mt-4">
                        View Details & Book
                      </Button>
                    </div>
                  </Card>
                ))}
              </div>

              <div className="p-4 bg-blue-50 rounded-lg">
                <p className="text-sm text-gray-700">
                  <strong>💡 Tip:</strong> These recommendations are personalized based on your travel profile,
                  including your company, budget preference, age, and travel duration. Higher match scores indicate
                  better alignment with your preferences.
                </p>
              </div>
            </div>
          )}

          {!results && !error && (
            <Card title="Hotel Recommendations">
              <p className="text-gray-700">
                Fill in your profile information on the left to get AI-powered personalized hotel recommendations.
              </p>
              <div className="mt-4 p-4 bg-blue-50 rounded space-y-2">
                <h3 className="font-semibold text-gray-800">How it works:</h3>
                <ul className="list-disc list-inside text-sm text-gray-700 space-y-1">
                  <li>Enter your travel dates and personal preferences</li>
                  <li>Specify your company and budget type</li>
                  <li>Our ML model analyzes patterns from similar travelers</li>
                  <li>Get ranked hotel recommendations with match scores</li>
                </ul>
              </div>
              <div className="mt-4 p-4 bg-green-50 rounded">
                <h3 className="font-semibold text-gray-800 mb-2">✨ Features:</h3>
                <ul className="text-sm text-gray-700 space-y-1">
                  <li>🤖 ML-powered personalization</li>
                  <li>📊 Match scores based on your profile</li>
                  <li>🏆 Top recommendations ranked by relevance</li>
                  <li>🎯 Company-specific preferences considered</li>
                </ul>
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}

export default HotelRecommendation

