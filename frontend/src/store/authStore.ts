import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { User } from '../types'

interface AuthStore {
  isAuthenticated: boolean
  token: string | null
  user: User | null
  setAuth: (token: string, user: User) => void
  logout: () => void
  setUser: (user: User) => void
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set) => ({
      isAuthenticated: false,
      token: null,
      user: null,
      
      setAuth: (token: string, user: User) => {
        set({ isAuthenticated: true, token, user })
      },
      
      logout: () => {
        set({ isAuthenticated: false, token: null, user: null })
      },
      
      setUser: (user: User) => {
        set({ user })
      },
    }),
    {
      name: 'auth-store',
    }
  )
)
