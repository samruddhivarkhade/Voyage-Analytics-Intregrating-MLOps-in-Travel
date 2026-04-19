import React from 'react'
import { Card, Input, Button, StatCard } from '../components/UI'
import { apiClient } from '../services/apiClient'
import type { GenderPredictionResponse } from '../types'

function GenderClassification() {
  const [formData, setFormData] = React.useState({
    flight_count: '5',
    total_price: '5000',
    total_distance: '10000',
    total_hotel_spend: '2000',
    total_days: '10',
    age: '35',
  })

  const [result, setResult] = React.useState<GenderPredictionResponse | null>(null)
  const [loading, setLoading] = React.useState(false)
  const [error, setError] = React.useState<string | null>(null)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await apiClient.predictGender({
        flight_count: parseInt(formData.flight_count),
        total_price: parseFloat(formData.total_price),
        total_distance: parseFloat(formData.total_distance),
        total_hotel_spend: parseFloat(formData.total_hotel_spend),
        total_days: parseInt(formData.total_days),
        age: parseInt(formData.age),
      })
      setResult(response)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Prediction failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-8">
      <div className="mb-8">
        <h1 className="text-4xl font-serif font-bold mb-2 text-dark-900">👤 Gender Classification</h1>
        <p className="text-dark-200">Enter your travel profile to get a gender classification prediction</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Form */}
        <div className="lg:col-span-1">
          <Card title="Enter Travel Profile">
            <form onSubmit={handleSubmit} className="space-y-4">
              <Input
                label="Flight Count"
                type="number"
                name="flight_count"
                value={formData.flight_count}
                onChange={handleChange}
                min="0"
                required
              />
              <Input
                label="Total Price ($)"
                type="number"
                name="total_price"
                value={formData.total_price}
                onChange={handleChange}
                min="0"
                step="100"
                required
              />
              <Input
                label="Total Distance (km)"
                type="number"
                name="total_distance"
                value={formData.total_distance}
                onChange={handleChange}
                min="0"
                step="100"
                required
              />
              <Input
                label="Total Hotel Spend ($)"
                type="number"
                name="total_hotel_spend"
                value={formData.total_hotel_spend}
                onChange={handleChange}
                min="0"
                step="100"
                required
              />
              <Input
                label="Total Days"
                type="number"
                name="total_days"
                value={formData.total_days}
                onChange={handleChange}
                min="0"
                required
              />
              <Input
                label="Age"
                type="number"
                name="age"
                value={formData.age}
                onChange={handleChange}
                min="18"
                max="100"
                required
              />
              <Button
                type="submit"
                disabled={loading}
                className="w-full"
              >
                {loading ? 'Classifying...' : 'Classify Gender'}
              </Button>
            </form>

            <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
              <p className="text-sm text-blue-800">
                ℹ️ This classifier uses travel behavior patterns to predict gender classification.
                Use responsibly and respect privacy.
              </p>
            </div>
          </Card>
        </div>

        {/* Results */}
        <div className="lg:col-span-2">
          {error && (
            <Card title="Error">
              <div className="text-red-700">{error}</div>
            </Card>
          )}

          {result && (
            <div className="space-y-6">
              <StatCard
                label="Predicted Gender"
                value={result.predicted_gender}
                icon="👤"
                color="purple"
              />

              <Card title="Classification Details ">
                <div className="space-y-3">
                  <div className="flex justify-between border-b pb-2">
                    <span className="text-gray-600">Flight Count</span>
                    <span className="font-semibold">{formData.flight_count}</span>
                  </div>
                  <div className="flex justify-between border-b pb-2">
                    <span className="text-gray-600">Total Spending</span>
                    <span className="font-semibold">${parseFloat(formData.total_price).toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between border-b pb-2">
                    <span className="text-gray-600">Total Distance</span>
                    <span className="font-semibold">{formData.total_distance} km</span>
                  </div>
                  <div className="flex justify-between border-b pb-2">
                    <span className="text-gray-600">Hotel Spend</span>
                    <span className="font-semibold">${parseFloat(formData.total_hotel_spend).toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between border-b pb-2">
                    <span className="text-gray-600">Total Days</span>
                    <span className="font-semibold">{formData.total_days} days</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Age</span>
                    <span className="font-semibold">{formData.age}</span>
                  </div>
                </div>
              </Card>

              <Card title="Travel Insights">
                <div className="space-y-3 text-gray-700">
                  <p className="flex justify-between">
                    <span>Avg. Spend per Flight:</span>
                    <span className="font-semibold">${(parseFloat(formData.total_price) / parseInt(formData.flight_count)).toFixed(2)}</span>
                  </p>
                  <p className="flex justify-between">
                    <span>Avg. Daily Budget:</span>
                    <span className="font-semibold">${(parseFloat(formData.total_price) / parseInt(formData.total_days)).toFixed(2)}</span>
                  </p>
                  <p className="flex justify-between">
                    <span>Avg. Distance per Flight:</span>
                    <span className="font-semibold">{(parseFloat(formData.total_distance) / parseInt(formData.flight_count)).toFixed(0)} km</span>
                  </p>
                </div>
              </Card>
            </div>
          )}

          {!result && !error && (
            <Card title="About This Model">
              <div className="space-y-3 text-gray-700">
                <p>
                  This machine learning model analyzes travel behavior patterns to classify gender
                  based on spending habits, distance traveled, and demographic factors.
                </p>
                <h3 className="font-semibold text-gray-800 mt-4">Features Analyzed:</h3>
                <ul className="list-disc list-inside space-y-1">
                  <li>Flight frequency and patterns</li>
                  <li>Travel spending behavior</li>
                  <li>Distance preferences</li>
                  <li>Accommodation spending</li>
                  <li>Duration patterns</li>
                  <li>Age demographics</li>
                </ul>
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}

export default GenderClassification
