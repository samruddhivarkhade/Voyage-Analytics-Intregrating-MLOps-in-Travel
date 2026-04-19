import React from 'react'
import { Card } from '../components/UI'
import { apiClient } from '../services/apiClient'
import type { PredictionRecord } from '../types'

function PredictionHistory() {
  const [history, setHistory] = React.useState<PredictionRecord[]>([])
  const [loading, setLoading] = React.useState(true)
  const [error, setError] = React.useState<string | null>(null)
  const [filter, setFilter] = React.useState<'all' | 'flight' | 'gender'>('all')

  React.useEffect(() => {
    const fetchHistory = async () => {
      try {
        const data = await apiClient.getPredictionHistory(100)
        setHistory(data)
      } catch (err) {
        setError('Failed to load prediction history')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    fetchHistory()
  }, [])

  const filteredHistory = history.filter((record) => {
    if (filter === 'all') return true
    return record.model_type === filter
  })

  if (loading) {
    return (
      <div className="p-8 flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading history...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-8 text-gray-800">📜 Prediction History</h1>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
          {error}
        </div>
      )}

      <div className="mb-6 flex gap-2">
        {['all', 'flight', 'gender'].map((type) => (
          <button
            key={type}
            onClick={() => setFilter(type as any)}
            className={`px-4 py-2 rounded font-semibold transition ${
              filter === type
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-800 hover:bg-gray-300'
            }`}
          >
            {type === 'all' ? 'All' : type === 'flight' ? '✈️ Flight' : '👤 Gender'}
          </button>
        ))}
      </div>

      {filteredHistory.length === 0 ? (
        <Card title="No Predictions Yet">
          <p className="text-gray-600">
            Start making predictions using the tools above to see them here.
          </p>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredHistory.map((record) => (
            <Card
              key={record.id}
              title={`${
                record.model_type === 'flight' ? '✈️ Flight' : '👤 Gender'
              } Prediction`}
            >
              <div className="space-y-3 text-sm">
                <div>
                  <p className="text-gray-600">Type</p>
                  <p className="font-semibold text-gray-800 capitalize">{record.model_type}</p>
                </div>
                <div>
                  <p className="text-gray-600">Date</p>
                  <p className="font-semibold text-gray-800">
                    {new Date(record.created_at).toLocaleString()}
                  </p>
                </div>

                {record.model_type === 'flight' && (
                  <>
                    <div>
                      <p className="text-gray-600">From → To</p>
                      <p className="font-semibold text-gray-800">
                        {(record.input_data as any).departure_city} → {(record.input_data as any).arrival_city}
                      </p>
                    </div>
                    <div>
                      <p className="text-gray-600">Predicted Price</p>
                      <p className="font-semibold text-green-600">
                        ${(record.output as any).predicted_price?.toFixed(2) || 'N/A'}
                      </p>
                    </div>
                  </>
                )}

                {record.model_type === 'gender' && (
                  <>
                    <div>
                      <p className="text-gray-600">Age</p>
                      <p className="font-semibold text-gray-800">{(record.input_data as any).age}</p>
                    </div>
                    <div>
                      <p className="text-gray-600">Predicted Gender</p>
                      <p className="font-semibold text-purple-600">
                        {(record.output as any).predicted_gender}
                      </p>
                    </div>
                  </>
                )}

                <div>
                  <p className="text-gray-600">Confidence</p>
                  <p className="font-semibold text-blue-600">
                    {((record.output as any).confidence * 100).toFixed(1)}%
                  </p>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}

export default PredictionHistory
