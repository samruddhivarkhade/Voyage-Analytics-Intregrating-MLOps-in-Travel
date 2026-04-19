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
        <h3 className="text-lg md:text-xl font-serif font-bold text-dark-50 mb-4">
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
    red: 'from-primary-700 to-primary-600',
    orange: 'from-secondary-700 to-secondary-600',
    gold: 'from-accent to-secondary-600',
    green: 'from-emerald-600 to-emerald-500',
    purple: 'from-purple-600 to-purple-500',
  }

  return (
    <div className={`card-dark bg-gradient-to-br ${colorMap[color]} bg-opacity-10 hover-lift ${className}`}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-dark-200 text-sm md:text-base mb-2">{label}</p>
          <p className="text-2xl md:text-3xl font-serif font-bold text-dark-50">
            {value}
          </p>
        </div>
        {icon && <span className="text-3xl md:text-4xl">{icon}</span>}
      </div>
    </div>
  )
}

interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost'
  children: React.ReactNode
}

export function Button({
  variant = 'primary',
  children,
  className = '',
  ...props
}: ButtonProps) {
  const variants = {
    primary:
      'px-6 py-2.5 rounded-full font-semibold bg-gradient-warm text-dark-900 hover:shadow-glow glow-warm hover-lift',
    secondary:
      'px-6 py-2.5 rounded-full font-semibold bg-surface border border-secondary-600 text-secondary-600 hover:bg-secondary-600 hover:text-dark-900 hover-lift',
    ghost:
      'px-6 py-2.5 rounded-full font-semibold text-dark-50 border border-dark-200 hover:border-secondary-600 hover:text-secondary-600 transition-colors',
  }

  return (
    <button
      className={`text-sm md:text-base transition-all duration-300 ${variants[variant]} ${className}`}
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
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-dark-50 mb-2">
          {label}
        </label>
      )}
      <input
        className={`w-full px-4 py-2.5 rounded-lg bg-surface border border-orange-900/20 text-dark-50 placeholder:text-dark-200 focus:border-secondary-600 focus:ring-2 focus:ring-secondary-600/20 focus:outline-none transition-all ${
          error ? 'border-red-500' : ''
        } ${className}`}
        {...props}
      />
      {error && <p className="mt-1 text-xs text-red-400">{error}</p>}
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
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-dark-50 mb-2">
          {label}
        </label>
      )}
      <select
        className={`w-full px-4 py-2.5 rounded-lg bg-surface border border-orange-900/20 text-dark-50 focus:border-secondary-600 focus:ring-2 focus:ring-secondary-600/20 focus:outline-none transition-all appearance-none cursor-pointer ${className}`}
        {...props}
      >
        {options.map((opt) => (
          <option key={opt.value} value={opt.value} className="bg-surface text-dark-50">
            {opt.label}
          </option>
        ))}
      </select>
    </div>
  )
}
