import React, { ReactNode, ReactElement } from 'react'
import { Button } from './UI'

interface Props {
  children: ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
}

class ErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = {
      hasError: false,
      error: null,
    }
  }

  static getDerivedStateFromError(error: Error): State {
    return {
      hasError: true,
      error,
    }
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error)
    console.error('Error info:', errorInfo)
    // You can log the error to an error reporting service here
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null })
    // Optionally reload the page
    window.location.href = '/'
  }

  render(): ReactElement {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-gradient-to-br from-primary-600 to-secondary-600 flex items-center justify-center px-4">
          <div className="bg-white rounded-lg shadow-2xl p-8 md:p-12 max-w-md w-full text-center space-y-6">
            {/* Error Icon */}
            <div className="text-6xl">💥</div>

            {/* Error Title */}
            <h1 className="text-4xl font-serif font-bold text-dark-900">
              Oops!
            </h1>

            {/* Error Message */}
            <div className="space-y-2">
              <p className="text-xl font-semibold text-dark-800">
                Something went wrong
              </p>
              <p className="text-dark-200">
                An unexpected error occurred. Please try again.
              </p>
            </div>

            {/* Error Details (Development only) */}
            {process.env.NODE_ENV === 'development' && this.state.error && (
              <div className="bg-red-50 border border-red-200 rounded p-3 text-left max-h-40 overflow-auto">
                <p className="text-xs font-mono text-red-700 break-words">
                  {this.state.error.message}
                </p>
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-3">
              <Button
                onClick={this.handleReset}
                variant="primary"
                className="flex-1"
              >
                Go Home
              </Button>
              <Button
                onClick={() => window.location.reload()}
                variant="secondary"
                className="flex-1"
              >
                Reload Page
              </Button>
            </div>

            {/* Support Link */}
            <p className="text-sm text-dark-200">
              Need help?{' '}
              <a
                href="mailto:support@voyage.com"
                className="text-primary-600 hover:text-primary-700 font-semibold"
              >
                Contact Support
              </a>
            </p>
          </div>
        </div>
      )
    }

    return this.props.children as ReactElement
  }
}

export default ErrorBoundary
