import React from 'react'
import { Card, Input, Select, Button, StatCard } from '../components/UI'
import { apiClient } from '../services/apiClient'
import type { FlightPredictionResponse } from '../types'

function FlightPrediction() {
  const [formData, setFormData] = React.useState({
    flightType: 'economic',
    agency: 'Rainbow',
    gender: 'male',
    distance: '1000',
    time: '5',
    age: '30',
  })

  const [result, setResult] = React.useState<FlightPredictionResponse | null>(null)
  const [loading, setLoading] = React.useState(false)
  const [error, setError] = React.useState<string | null>(null)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await apiClient.predictFlightPrice({
        flightType: formData.flightType as 'economic' | 'firstClass' | 'premium',
        agency: formData.agency as 'Rainbow' | 'CloudFy' | 'FlyingDrops',
        gender: formData.gender as 'male' | 'female',
        distance: parseFloat(formData.distance),
        time: parseFloat(formData.time),
        age: parseInt(formData.age),
      })
      setResult(response)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Prediction failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const flightTypes = [
    { value: 'economic', label: 'Economic' },
    { value: 'firstClass', label: 'First Class' },
    { value: 'premium', label: 'Premium' },
  ]

  const agencies = [
    { value: 'Rainbow', label: 'Rainbow' },
    { value: 'CloudFy', label: 'CloudFy' },
    { value: 'FlyingDrops', label: 'FlyingDrops' },
  ]

  const genders = [
    { value: 'male', label: 'Male' },
    { value: 'female', label: 'Female' },
  ]

  return (
    <div className="space-y-8">
      <div className="mb-8">
        <h1 className="text-4xl font-serif font-bold mb-2 text-dark-900">✈️ Flight Price Prediction</h1>
        <p className="text-dark-200">Enter your flight details to get a price prediction</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Form */}
        <div className="lg:col-span-1">
          <Card title="Enter Flight Details">
            <form onSubmit={handleSubmit} className="space-y-4">
              <Select
                label="Flight Type"
                name="flightType"
                value={formData.flightType}
                onChange={handleChange}
                options={flightTypes}
              />
              <Select
                label="Agency"
                name="agency"
                value={formData.agency}
                onChange={handleChange}
                options={agencies}
              />
              <Select
                label="Gender"
                name="gender"
                value={formData.gender}
                onChange={handleChange}
                options={genders}
              />
              <Input
                label="Distance (km)"
                type="number"
                name="distance"
                value={formData.distance}
                onChange={handleChange}
                min="0"
                step="100"
                required
              />
              <Input
                label="Time (hours)"
                type="number"
                name="time"
                value={formData.time}
                onChange={handleChange}
                min="0"
                step="0.5"
                required
              />
              <Input
                label="Age"
                type="number"
                name="age"
                value={formData.age}
                onChange={handleChange}
                min="0"
                max="120"
                required
              />
              <Button
                type="submit"
                disabled={loading}
                className="w-full"
              >
                {loading ? 'Predicting...' : 'Predict Price'}
              </Button>
            </form>
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
                label="Predicted Price"
                value={`$${result.predicted_price.toFixed(2)}`}
                icon="💰"
                color="green"
              />

              <Card title="Prediction Details">
                <div className="space-y-3 text-dark-900">
                  <div className="flex justify-between border-b pb-2">
                    <span className="text-dark-200">Flight Type</span>
                    <span className="font-semibold capitalize text-primary-600">{formData.flightType}</span>
                  </div>
                  <div className="flex justify-between border-b pb-2">
                    <span className="text-gray-600">Agency</span>
                    <span className="font-semibold">{formData.agency}</span>
                  </div>
                  <div className="flex justify-between border-b pb-2">
                    <span className="text-gray-600">Distance</span>
                    <span className="font-semibold">{formData.distance} km</span>
                  </div>
                  <div className="flex justify-between border-b pb-2">
                    <span className="text-gray-600">Time</span>
                    <span className="font-semibold">{formData.time} hours</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Age</span>
                    <span className="font-semibold">{formData.age}</span>
                  </div>
                </div>
              </Card>
            </div>
          )}

          {!result && !error && (
            <Card title="Flight Price Prediction">
              <p className="text-gray-700">
                Enter flight details on the left and our ML model will predict the price based on historical data patterns.
              </p>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}

export default FlightPrediction
