import React from 'react'
import { useRouteError, useNavigate } from 'react-router-dom'
import { Button } from '../components/UI'
import Header from '../components/Header'
import Footer from '../components/Footer'

function ErrorPage() {
  const error = useRouteError()
  const navigate = useNavigate()

  const statusCode = error?.status || 500
  const statusText = error?.statusText || 'Error'
  const message = error?.message || 'An unexpected error occurred'

  return (
    <div className="flex flex-col min-h-screen bg-gradient-dark">
      <Header />
      <main className="flex-1 flex items-center justify-center px-4 pt-16 md:pt-20 pb-8">
      <div className="bg-white rounded-lg shadow-2xl p-8 md:p-12 max-w-md w-full text-center space-y-6">
        {/* Error Icon */}
        <div className="text-6xl">
          {statusCode === 404 ? '🗺️' : statusCode === 403 ? '🔒' : '⚠️'}
        </div>

        {/* Error Title */}
        <h1 className="text-4xl font-serif font-bold text-dark-900">
          {statusCode}
        </h1>

        {/* Error Message */}
        <div className="space-y-2">
          <p className="text-xl font-semibold text-dark-800">{statusText}</p>
          <p className="text-dark-200">{message}</p>
        </div>

        {/* Error Details */}
        {statusCode === 404 && (
          <div className="bg-blue-50 border border-blue-200 rounded p-3">
            <p className="text-sm text-blue-700">
              The page you're looking for seems to have taken flight! Let's navigate you back to safety.
            </p>
          </div>
        )}

        {statusCode === 403 && (
          <div className="bg-red-50 border border-red-200 rounded p-3">
            <p className="text-sm text-red-700">
              You don't have permission to access this page. Please contact support if you believe this is an error.
            </p>
          </div>
        )}

        {statusCode === 500 && (
          <div className="bg-red-50 border border-red-200 rounded p-3">
            <p className="text-sm text-red-700">
              Something went wrong on our end. Our team has been notified. Please try again later.
            </p>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-3">
          <Button
            onClick={() => navigate('/')}
            variant="primary"
            className="flex-1"
          >
            Go Home
          </Button>
          <Button
            onClick={() => navigate(-1)}
            variant="secondary"
            className="flex-1"
          >
            Go Back
          </Button>
        </div>

        {/* Support Link */}
        <p className="text-sm text-dark-200">
          Need help?{' '}
          <a href="mailto:support@voyage.com" className="text-primary-600 hover:text-primary-700 font-semibold">
            Contact Support
          </a>
        </p>
        
    </div>
      </main>
      <Footer />
    </div>
  )
}
     

export default ErrorPage
