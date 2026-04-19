import React from 'react'
import { Outlet, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import Header from './Header'
import Footer from './Footer'

function Layout() {
  const navigate = useNavigate()
  const { isAuthenticated } = useAuthStore()

  React.useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login')
    }
  }, [isAuthenticated, navigate])

  return (
    <div className="flex flex-col min-h-screen bg-gradient-dark">
      <Header />
      <main className="flex-1 pt-16 md:pt-20 pb-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full">
        <Outlet />
      </main>
      <Footer />
    </div>
  )
}

export default Layout
