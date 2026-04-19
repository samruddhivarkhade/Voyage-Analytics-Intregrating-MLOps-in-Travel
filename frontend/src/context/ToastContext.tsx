import React, { ReactNode, createContext, useContext } from 'react'
import ToastContainer from '../components/ToastContainer'
import { useToast, ToastType } from '../hooks/useToast'

interface ToastContextType {
  success: (message: string, duration?: number) => string
  error: (message: string, duration?: number) => string
  info: (message: string, duration?: number) => string
  warning: (message: string, duration?: number) => string
}

const ToastContext = createContext<ToastContextType | undefined>(undefined)

interface ToastProviderProps {
  children: ReactNode
}

export const ToastProvider: React.FC<ToastProviderProps> = ({ children }) => {
  const toast = useToast()

  return (
    <ToastContext.Provider
      value={{
        success: toast.success,
        error: toast.error,
        info: toast.info,
        warning: toast.warning,
      }}
    >
      {children}
      <ToastContainer toasts={toast.toasts} onRemove={toast.removeToast} />
    </ToastContext.Provider>
  )
}

export const useToastContext = (): ToastContextType => {
  const context = useContext(ToastContext)
  if (!context) {
    throw new Error('useToastContext must be used within a ToastProvider')
  }
  return context
}
