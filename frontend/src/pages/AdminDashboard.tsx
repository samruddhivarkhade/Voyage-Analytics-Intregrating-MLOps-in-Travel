import { Card, StatCard } from '../components/UI'

function AdminDashboard() {
  // Placeholder admin data
  const adminStats = {
    total_users: 1234,
    active_users_today: 456,
    total_predictions: 8900,
    avg_model_accuracy: 0.92,
    system_uptime: 99.87,
  }

  const modelMetrics = [
    {
      name: 'Flight Price Predictor',
      version: '2.1.0',
      accuracy: 0.88,
      predictions: 5320,
      confidence: 0.85,
      updated: '2026-04-15',
    },
    {
      name: 'Gender Classifier',
      version: '1.5.0',
      accuracy: 0.95,
      predictions: 3580,
      confidence: 0.89,
      updated: '2026-04-16',
    },
  ]

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-8 text-gray-800">⚙️ Admin Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 mb-8">
        <StatCard label="Total Users" value={adminStats.total_users} icon="👥" color="blue" />
        <StatCard
          label="Active Today"
          value={adminStats.active_users_today}
          icon="✨"
          color="green"
        />
        <StatCard
          label="Total Predictions"
          value={adminStats.total_predictions}
          icon="📊"
          color="purple"
        />
        <StatCard
          label="Avg Accuracy"
          value={`${(adminStats.avg_model_accuracy * 100).toFixed(1)}%`}
          icon="🎯"
          color="orange"
        />
        <StatCard
          label="Uptime"
          value={`${adminStats.system_uptime.toFixed(2)}%`}
          icon="⬆️"
          color="green"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <Card title="Model Performance">
          <div className="space-y-4">
            {modelMetrics.map((metric) => (
              <div key={metric.name} className="border-b pb-4 last:border-b-0">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h3 className="font-semibold text-gray-800">{metric.name}</h3>
                    <p className="text-xs text-gray-500">v{metric.version}</p>
                  </div>
                  <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">
                    Active
                  </span>
                </div>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-gray-600">Accuracy</p>
                    <p className="font-semibold">{(metric.accuracy * 100).toFixed(1)}%</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Predictions</p>
                    <p className="font-semibold">{metric.predictions}</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Avg Confidence</p>
                    <p className="font-semibold">{(metric.confidence * 100).toFixed(1)}%</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Last Updated</p>
                    <p className="font-semibold">{metric.updated}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </Card>

        <Card title="System Health">
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-gray-700">API Server</span>
              <span className="flex items-center gap-2">
                <span className="w-3 h-3 bg-green-500 rounded-full"></span>
                <span className="text-sm font-semibold">Healthy</span>
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-700">Database</span>
              <span className="flex items-center gap-2">
                <span className="w-3 h-3 bg-green-500 rounded-full"></span>
                <span className="text-sm font-semibold">Connected</span>
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-700">Cache (Redis)</span>
              <span className="flex items-center gap-2">
                <span className="w-3 h-3 bg-green-500 rounded-full"></span>
                <span className="text-sm font-semibold">Active</span>
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-700">ML Services</span>
              <span className="flex items-center gap-2">
                <span className="w-3 h-3 bg-green-500 rounded-full"></span>
                <span className="text-sm font-semibold">Running</span>
              </span>
            </div>
          </div>
        </Card>
      </div>

      <Card title="Recent Activity">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b">
                <th className="text-left py-2 px-2 font-semibold text-gray-700">Time</th>
                <th className="text-left py-2 px-2 font-semibold text-gray-700">Event</th>
                <th className="text-left py-2 px-2 font-semibold text-gray-700">User</th>
                <th className="text-left py-2 px-2 font-semibold text-gray-700">Status</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-b hover:bg-gray-50">
                <td className="py-2 px-2 text-gray-600">14:32:15</td>
                <td className="py-2 px-2">Flight Prediction</td>
                <td className="py-2 px-2">user@example.com</td>
                <td className="py-2 px-2">
                  <span className="text-green-600 font-semibold">✓</span>
                </td>
              </tr>
              <tr className="border-b hover:bg-gray-50">
                <td className="py-2 px-2 text-gray-600">14:31:02</td>
                <td className="py-2 px-2">Gender Classification</td>
                <td className="py-2 px-2">demo@example.com</td>
                <td className="py-2 px-2">
                  <span className="text-green-600 font-semibold">✓</span>
                </td>
              </tr>
              <tr className="border-b hover:bg-gray-50">
                <td className="py-2 px-2 text-gray-600">14:29:45</td>
                <td className="py-2 px-2">New User Registration</td>
                <td className="py-2 px-2">newuser@example.com</td>
                <td className="py-2 px-2">
                  <span className="text-green-600 font-semibold">✓</span>
                </td>
              </tr>
              <tr className="hover:bg-gray-50">
                <td className="py-2 px-2 text-gray-600">14:28:30</td>
                <td className="py-2 px-2">Model Update</td>
                <td className="py-2 px-2">system</td>
                <td className="py-2 px-2">
                  <span className="text-blue-600 font-semibold">ⓘ</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  )
}

export default AdminDashboard
