import React from 'react'

interface CardProps {
  title?: string
  children: React.ReactNode
  className?: string
}

export function Card({ title, children, className = '' }: CardProps) {
  return (
    <div className={`card-dark hover-lift ${className}`}>
      {title && (
        <h3 className="text-lg md:text-xl font-serif font-bold text-dark-900 mb-4">
          {title}
        </h3>
      )}
      {children}
    </div>
  )
}

interface StatCardProps {
  label: string
  value: string | number
  icon?: string
  color?: 'red' | 'orange' | 'gold' | 'green' | 'purple'
  className?: string
}

export function StatCard({ label, value, icon, color = 'orange', className = '' }: StatCardProps) {
  const colorMap = {
    red: 'from-red-600 to-red-500',
    orange: 'from-orange-600 to-orange-500',
    gold: 'from-amber-600 to-amber-500',
    green: 'from-green-600 to-green-500',
    purple: 'from-purple-600 to-purple-500',
  }

  return (
    <div className={`bg-gradient-to-br ${colorMap[color]} p-6 rounded-lg hover-lift cursor-pointer group shadow-lg ${className}`}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-white font-medium text-sm md:text-base mb-2">{label}</p>
          <p className="text-3xl md:text-4xl font-serif font-bold text-white">
            {value}
          </p>
        </div>
        {icon && <span className="text-4xl md:text-5xl opacity-70 group-hover:opacity-100 transition-opacity">{icon}</span>}
      </div>
    </div>
  )
}

interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger'
  size?: 'sm' | 'md' | 'lg'
}

export function Button({
  variant = 'primary',
  size = 'md',
  children,
  className = '',
  ...props
}: ButtonProps) {
  const variants = {
    primary:
      'bg-blue-600 text-white hover:bg-blue-700 hover:shadow-lg transition-all duration-300',
    secondary:
      'bg-white text-blue-900 border-2 border-blue-600 hover:bg-blue-600 hover:text-white transition-all duration-300',
    ghost:
      'text-gray-900 border-2 border-blue-600 hover:bg-blue-100 transition-colors duration-300',
    danger:
      'bg-red-600 text-white hover:bg-red-700 hover:shadow-lg transition-all duration-300',
  }

  const sizes = {
    sm: 'px-3 py-1.5 text-xs md:text-sm',
    md: 'px-4 md:px-6 py-2 md:py-2.5 text-sm md:text-base',
    lg: 'px-6 md:px-8 py-3 md:py-3 text-base md:text-lg',
  }

  return (
    <button
      className={`rounded-full font-semibold ${variants[variant]} ${sizes[size]} ${className}`}
      {...props}
    >
      {children}
    </button>
  )
}

interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
}

export function Input({
  label,
  error,
  className = '',
  ...props
}: InputProps) {
  return (
    <div className="w-full mb-4">
      {label && (
        <label className="block text-sm font-medium text-dark-900 mb-2">
          {label}
        </label>
      )}
      <input
        className={`w-full px-4 py-2.5 rounded-lg bg-surface border-2 border-primary-600/20 text-dark-900 placeholder:text-dark-200 focus:border-primary-600 focus:ring-2 focus:ring-primary-600/20 focus:outline-none transition-all ${
          error ? 'border-red-500' : ''
        } ${className}`}
        {...props}
      />
      {error && <p className="mt-1 text-xs text-red-500">{error}</p>}
    </div>
  )
}

interface SelectProps
  extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string
  options: { value: string; label: string }[]
}

export function Select({
  label,
  options,
  className = '',
  ...props
}: SelectProps) {
  return (
    <div className="w-full mb-4">
      {label && (
        <label className="block text-sm font-medium text-dark-900 mb-2">
          {label}
        </label>
      )}
      <select
        className={`w-full px-4 py-2.5 rounded-lg bg-surface border-2 border-primary-600/20 text-dark-900 focus:border-primary-600 focus:ring-2 focus:ring-primary-600/20 focus:outline-none transition-all appearance-none cursor-pointer ${className}`}
        {...props}
      >
        {options.map((opt) => (
          <option key={opt.value} value={opt.value} className="bg-surface text-dark-900">
            {opt.label}
          </option>
        ))}
      </select>
    </div>
  )
}
