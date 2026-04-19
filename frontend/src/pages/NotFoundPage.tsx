import React from 'react'
import { useNavigate } from 'react-router-dom'
import { Button } from '../components/UI'
import Header from '../components/Header'
import Footer from '../components/Footer'

function NotFoundPage() {
  const navigate = useNavigate()

  return (
    <div className="flex flex-col min-h-screen bg-gradient-dark">
      <Header />
      <main className="flex-1 flex items-center justify-center px-4 pt-16 md:pt-20 pb-8">
      <div className="bg-white rounded-lg shadow-2xl p-8 md:p-12 max-w-md w-full text-center space-y-6">
        {/* 404 Icon */}
        <div className="text-8xl font-bold bg-gradient-to-r from-primary-600 to-secondary-600 bg-clip-text text-transparent">
          404
        </div>

        {/* Lost Airplane */}
        <div className="text-6xl animate-bounce">✈️</div>

        {/* Title */}
        <h1 className="text-3xl font-serif font-bold text-dark-900">
          Page Not Found
        </h1>

        {/* Description */}
        <div className="space-y-2">
          <p className="text-lg text-dark-800">
            Looks like your flight took off without you!
          </p>
          <p className="text-dark-200">
            The page you're looking for doesn't exist or has been moved. Let's get you back on track.
          </p>
        </div>

        {/* Helpful Tips */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-left space-y-2">
          <p className="text-sm font-semibold text-blue-900">Quick navigation:</p>
          <ul className="text-xs text-blue-800 space-y-1">
            <li>• Check the URL for typos</li>
            <li>• Navigate using the menu</li>
            <li>• Return to the homepage</li>
          </ul>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-3">
          <Button
            onClick={() => navigate('/')}
            variant="primary"
            className="flex-1"
          >
            Back Home
          </Button>
          <Button
            onClick={() => navigate(-1)}
            variant="secondary"
            className="flex-1"
          >
            Go Back
          </Button>
        </div>

        {/* Additional Help */}
        <p className="text-sm text-dark-200">
          Still lost?{' '}
          <a
            href="mailto:support@voyage.com"
            className="text-primary-600 hover:text-primary-700 font-semibold"
          >
            Contact us
          </a>
        </p>
      </div>
      </main>
      <Footer />
    </div>
  )
}

export default NotFoundPage
