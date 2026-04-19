import { AxiosError } from 'axios'
import { useAuthStore } from '../store/authStore'

interface ErrorResponse {
  status: number
  message: string
  detail?: string
}

/**
 * Handle API errors globally
 * @param error The error object from API call
 * @returns Error response object
 */
export const handleApiError = (error: unknown): ErrorResponse => {
  const authStore = useAuthStore.getState()

  // Handle Axios errors
  if (error instanceof AxiosError) {
    const status = error.response?.status || 500
    const data = error.response?.data as any

    // Handle 401 Unauthorized
    if (status === 401) {
      authStore.logout()
      window.location.href = '/login'
      return {
        status: 401,
        message: 'Session expired. Please log in again.',
      }
    }

    // Handle 403 Forbidden
    if (status === 403) {
      return {
        status: 403,
        message: 'You do not have permission to access this resource.',
        detail: data?.detail,
      }
    }

    // Handle 404 Not Found
    if (status === 404) {
      return {
        status: 404,
        message: 'The requested resource was not found.',
        detail: data?.detail,
      }
    }

    // Handle 422 Unprocessable Entity (Validation error)
    if (status === 422) {
      return {
        status: 422,
        message: 'Invalid input. Please check your data.',
        detail: data?.detail,
      }
    }

    // Handle 500 Server Error
    if (status === 500) {
      return {
        status: 500,
        message: 'Server error. Please try again later.',
        detail: data?.detail,
      }
    }

    // Handle other HTTP errors
    return {
      status,
      message: data?.message || error.message || 'An error occurred',
      detail: data?.detail,
    }
  }

  // Handle generic errors
  if (error instanceof Error) {
    return {
      status: 500,
      message: error.message,
    }
  }

  // Handle unknown errors
  return {
    status: 500,
    message: 'An unexpected error occurred',
  }
}

/**
 * Log error for debugging/monitoring
 * @param error The error object
 * @param context Additional context information
 */
export const logError = (error: unknown, context?: string) => {
  const timestamp = new Date().toISOString()
  const errorResponse = handleApiError(error)

  console.error(`[${timestamp}] Error${context ? ` (${context})` : ''}:`, {
    status: errorResponse.status,
    message: errorResponse.message,
    detail: errorResponse.detail,
    originalError: error,
  })

  // You could send this to an error tracking service like Sentry
  // Example: Sentry.captureException(error, { contexts: { custom: { timestamp, context } } })
}

/**
 * Format error message for user display
 * @param error The error object
 * @returns User-friendly error message
 */
export const formatErrorMessage = (error: unknown): string => {
  const errorResponse = handleApiError(error)

  // Return detail if available, otherwise return message
  return errorResponse.detail || errorResponse.message
}

/**
 * Check if error is a specific status code
 * @param error The error object
 * @param statusCode The status code to check for
 * @returns True if error matches the status code
 */
export const isErrorStatus = (error: unknown, statusCode: number): boolean => {
  if (error instanceof AxiosError) {
    return error.response?.status === statusCode
  }
  return false
}

/**
 * Check if error is a network error (no response)
 * @param error The error object
 * @returns True if it's a network error
 */
export const isNetworkError = (error: unknown): boolean => {
  if (error instanceof AxiosError) {
    return !error.response && error.message === 'Network Error'
  }
  return false
}

/**
 * Redirect to error page with error details
 * @param status HTTP status code
 * @param statusText Human readable status text
 * @param message Error message
 */
export const redirectToErrorPage = (
  status: number = 500,
  statusText: string = 'Error',
  message?: string
) => {
  const errorParams = new URLSearchParams({
    status: status.toString(),
    statusText,
    ...(message && { message }),
  })

  window.location.href = `/error?${errorParams.toString()}`
}
