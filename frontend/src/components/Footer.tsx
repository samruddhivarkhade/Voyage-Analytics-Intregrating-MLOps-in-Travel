function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="relative mt-20 bg-surface-alt border-t border-primary-600/10">
      {/* Main Footer */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 md:gap-12">
          {/* Brand */}
          <div>
            <div className="text-2xl font-serif font-bold gradient-text mb-2">
              ✈️ Voyage
            </div>
            <p className="text-dark-200 text-sm">
              Your intelligent travel analytics companion. Predict prices, discover recommendations, and travel smarter.
            </p>
          </div>

          {/* Product */}
          <div>
            <h3 className="font-serif font-bold text-dark-900 mb-4">Product</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="/#" className="text-dark-200 hover:text-primary-600 transition-colors">
                  Flight Predictions
                </a>
              </li>
              <li>
                <a href="/#" className="text-dark-200 hover:text-primary-600 transition-colors">
                  Gender Classification
                </a>
              </li>
              <li>
                <a href="/#" className="text-dark-200 hover:text-primary-600 transition-colors">
                  Hotel Recommendations
                </a>
              </li>
              <li>
                <a href="/#" className="text-dark-200 hover:text-primary-600 transition-colors">
                  Analytics Dashboard
                </a>
              </li>
            </ul>
          </div>

          {/* Company */}
          <div>
            <h3 className="font-serif font-bold text-dark-900 mb-4">Company</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="/#" className="text-dark-200 hover:text-primary-600 transition-colors">
                  About Us
                </a>
              </li>
              <li>
                <a href="/#" className="text-dark-200 hover:text-primary-600 transition-colors">
                  Blog
                </a>
              </li>
              <li>
                <a href="/#" className="text-dark-200 hover:text-primary-600 transition-colors">
                  Careers
                </a>
              </li>
              <li>
                <a href="/#" className="text-dark-200 hover:text-primary-600 transition-colors">
                  Contact
                </a>
              </li>
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h3 className="font-serif font-bold text-dark-900 mb-4">Legal</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="/#" className="text-dark-200 hover:text-primary-600 transition-colors">
                  Privacy Policy
                </a>
              </li>
              <li>
                <a href="/#" className="text-dark-200 hover:text-primary-600 transition-colors">
                  Terms of Service
                </a>
              </li>
              <li>
                <a href="/#" className="text-dark-200 hover:text-primary-600 transition-colors">
                  Security
                </a>
              </li>
              <li>
                <a href="/#" className="text-dark-200 hover:text-primary-600 transition-colors">
                  Cookie Policy
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Divider */}
        <div className="divider-warm opacity-50"></div>

        {/* Bottom Bar */}
        <div className="flex flex-col md:flex-row items-center justify-between">
          <p className="text-dark-200 text-sm">
            &copy; {currentYear} Voyage Analytics. All rights reserved.
          </p>

          {/* Social Icons */}
          <div className="flex items-center gap-4 mt-6 md:mt-0">
            {['Twitter', 'LinkedIn', 'GitHub'].map((social) => (
              <a
                key={social}
                href="#"
                className="w-9 h-9 rounded-full bg-surface border border-orange-900/20 flex items-center justify-center text-dark-200 hover:bg-secondary hover:text-dark-900 hover-lift"
                aria-label={social}
              >
                {social[0]}
              </a>
            ))}
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer
