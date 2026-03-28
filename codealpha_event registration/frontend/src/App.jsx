import { useState, useEffect, useCallback } from 'react'
import axios from 'axios'
import './App.css'
import { Calendar, MapPin, User, ChevronRight, X, CheckCircle, LogOut, Mail, Lock, User as UserIcon, ArrowLeft, Loader2 } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

const API_BASE = 'http://localhost:8000/api'

function App() {
  const [events, setEvents] = useState([])
  const [selectedEvent, setSelectedEvent] = useState(null)
  const [loading, setLoading] = useState(true)
  const [isRegistering, setIsRegistering] = useState(false)
  const [registrationSuccess, setRegistrationSuccess] = useState(false)
  
  // Navigation and Domain State
  const [currentView, setCurrentView] = useState('explore') // 'explore' or 'profile'
  const [registrations, setRegistrations] = useState([])
  const [regsLoading, setRegsLoading] = useState(false)

  // Auth state
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(localStorage.getItem('token'))
  const [showAuthModal, setShowAuthModal] = useState(false)
  const [authMode, setAuthMode] = useState('login') // 'login' or 'signup'
  const [authFormData, setAuthFormData] = useState({ username: '', email: '', password: '' })
  const [authError, setAuthError] = useState('')

  useEffect(() => {
    fetchEvents()
    if (token) {
      fetchUser()
    }
  }, [token])

  const fetchEvents = async () => {
    try {
      const response = await axios.get(`${API_BASE}/events/`)
      setEvents(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching events:', error)
      setLoading(false)
    }
  }

  const fetchUser = async () => {
    try {
      const response = await axios.get(`${API_BASE}/me/`, {
        headers: { Authorization: `Token ${token}` }
      })
      setUser(response.data)
    } catch (error) {
      console.error('Token invalid or expired')
      handleLogout()
    }
  }

  const fetchRegistrations = useCallback(async () => {
    if (!token) return
    setRegsLoading(true)
    try {
      const response = await axios.get(`${API_BASE}/registrations/`, {
        headers: { Authorization: `Token ${token}` }
      })
      setRegistrations(response.data)
    } catch (error) {
      console.error('Error fetching registrations:', error)
    } finally {
      setRegsLoading(false)
    }
  }, [token])

  useEffect(() => {
    if (currentView === 'profile') {
      fetchRegistrations()
    }
  }, [currentView, fetchRegistrations])

  const handleAuthSubmit = async (e) => {
    e.preventDefault()
    setAuthError('')
    try {
      let response
      if (authMode === 'login') {
        response = await axios.post(`${API_BASE}/login/`, {
          username: authFormData.username,
          password: authFormData.password
        })
        const newToken = response.data.token
        localStorage.setItem('token', newToken)
        setToken(newToken)
      } else {
        response = await axios.post(`${API_BASE}/register/`, authFormData)
        const newToken = response.data.token
        localStorage.setItem('token', newToken)
        setToken(newToken)
        setUser(response.data.user)
      }
      setShowAuthModal(false)
      setAuthFormData({ username: '', email: '', password: '' })
    } catch (error) {
      const data = error.response?.data
      if (data) {
        if (data.non_field_errors) {
          setAuthError(data.non_field_errors[0])
        } else if (typeof data === 'object') {
          const [field, errors] = Object.entries(data)[0]
          setAuthError(`${field}: ${errors[0]}`)
        } else {
          setAuthError('Authentication failed. Please check your credentials.')
        }
      } else {
        setAuthError('Network error. Is the server running?')
      }
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    setToken(null)
    setUser(null)
    setCurrentView('explore')
  }

  const handleRegister = async (eventId) => {
    if (!token) {
      setShowAuthModal(true)
      return
    }

    setIsRegistering(true)
    try {
      await axios.post(`${API_BASE}/registrations/`, 
        { event: eventId },
        { headers: { Authorization: `Token ${token}` } }
      )
      setRegistrationSuccess(true)
      if (currentView === 'profile') fetchRegistrations()
      setTimeout(() => {
        setRegistrationSuccess(false)
        setSelectedEvent(null)
      }, 4000)
    } catch (error) {
      const msg = error.response?.data?.non_field_errors?.[0] || 'Something went wrong.'
      alert(msg === 'The fields user, event must make a unique set.' ? 'You are already registered!' : msg)
    } finally {
      setIsRegistering(false)
    }
  }

  return (
    <div className="app-container">
      <header className="glass-header">
        <div className="logo-group" onClick={() => setCurrentView('explore')} style={{cursor: 'pointer'}}>
          <div className="logo-icon">E</div>
          <h1>Event<span>Hub</span></h1>
        </div>
        <nav>
          <a 
            href="#" 
            className={currentView === 'explore' ? 'active' : ''} 
            onClick={(e) => { e.preventDefault(); setCurrentView('explore'); }}
          >
            Explore
          </a>
          {user ? (
            <div 
              className={`user-badge ${currentView === 'profile' ? 'active-badge' : ''}`} 
              onClick={() => setCurrentView('profile')}
              style={{cursor: 'pointer'}}
            >
              <div className="avatar-sm">{user.username[0].toUpperCase()}</div>
              <span>{user.username}</span>
              <button className="btn-logout" onClick={(e) => { e.stopPropagation(); handleLogout(); }} title="Logout">
                <LogOut size={16} />
              </button>
            </div>
          ) : (
            <div style={{display: 'flex', gap: '1rem'}}>
              <button className="btn-outline" style={{width: 'auto'}} onClick={() => { setAuthMode('login'); setShowAuthModal(true); }}>
                Sign In
              </button>
              <button className="btn-primary" onClick={() => { setAuthMode('signup'); setShowAuthModal(true); }}>
                Sign Up
              </button>
            </div>
          )}
        </nav>
      </header>

      <main>
        {currentView === 'explore' ? (
          <>
            <section className="hero">
              <motion.h2 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
              >
                Discover Amazing <span>Events</span> Near You
              </motion.h2>
              <p>Join world-class conferences, workshops, and meetups with just one click.</p>
            </section>

            <section className="events-grid">
              {loading ? (
                <div className="loader"><Loader2 className="spinning" /> Loading amazing events...</div>
              ) : (
                events.map((event, index) => (
                  <motion.div 
                    key={event.id}
                    className="event-card glass"
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: index * 0.05 }}
                    onClick={() => setSelectedEvent(event)}
                  >
                    <div className="event-date-badge">
                      {new Date(event.date).toLocaleDateString('en-US', { day: '2-digit', month: 'short' })}
                    </div>
                    <div className="event-content">
                      <h3>{event.title}</h3>
                      <div className="event-info">
                        <span><MapPin size={16} /> {event.location}</span>
                        <span><UserIcon size={16} /> By {event.organizer.username}</span>
                      </div>
                      <p>{event.description.substring(0, 80)}...</p>
                      <button className="btn-outline">
                        View Details <ChevronRight size={18} />
                      </button>
                    </div>
                  </motion.div>
                ))
              )}
            </section>
          </>
        ) : (
          <section className="profile-view">
            <motion.div 
              className="profile-card glass"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <div className="profile-avatar">
                {user?.username[0].toUpperCase()}
              </div>
              <div className="profile-info">
                <h2>{user?.username}</h2>
                <p><Mail size={18} /> {user?.email}</p>
                <button className="btn-outline" style={{width: 'auto', marginTop: '1rem'}} onClick={() => setCurrentView('explore')}>
                  <ArrowLeft size={16} /> Continue Exploring
                </button>
              </div>
            </motion.div>

            <div className="section-header">
              <h3>My Registered Events</h3>
              <span className="badge">{registrations.length} Events</span>
            </div>

            <div className="registrations-grid">
              {regsLoading ? (
                <div className="loader"><Loader2 className="spinning" /> Fetching your registrations...</div>
              ) : registrations.length > 0 ? (
                registrations.map((reg, index) => (
                  <motion.div 
                    key={reg.id}
                    className="registration-card glass"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <div className="reg-info">
                      <h4>{reg.event_details.title}</h4>
                      <div className="reg-meta">
                        <span><Calendar size={14} /> {new Date(reg.event_details.date).toLocaleDateString()}</span>
                        <span><MapPin size={14} /> {reg.event_details.location}</span>
                      </div>
                    </div>
                    <div className="status-badge status-confirmed">
                      {reg.status}
                    </div>
                  </motion.div>
                ))
              ) : (
                <div className="empty-state glass">
                  <Calendar size={48} />
                  <p>You haven't registered for any events yet.</p>
                  <button className="btn-primary" style={{marginTop: '1.5rem'}} onClick={() => setCurrentView('explore')}>
                    Browse Events
                  </button>
                </div>
              )}
            </div>
          </section>
        )}
      </main>

      <AnimatePresence>
        {/* Auth Modal */}
        {showAuthModal && (
          <motion.div 
            className="modal-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <motion.div 
              className="modal-content glass auth-modal"
              initial={{ y: 50, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              exit={{ y: 50, opacity: 0 }}
            >
              <button className="close-btn" onClick={() => setShowAuthModal(false)}>
                <X size={24} />
              </button>
              
              <div className="modal-header">
                <h2>{authMode === 'login' ? 'Welcome Back' : 'Create Account'}</h2>
                <p>{authMode === 'login' ? 'Please enter your details to sign in.' : 'Join us to register for amazing events.'}</p>
              </div>

              <form className="auth-form" onSubmit={handleAuthSubmit}>
                <div className="form-group">
                  <label><UserIcon size={14} /> Username</label>
                  <input 
                    type="text" 
                    required 
                    value={authFormData.username}
                    onChange={(e) => setAuthFormData({...authFormData, username: e.target.value})}
                    placeholder="johndoe"
                  />
                </div>
                
                {authMode === 'signup' && (
                  <div className="form-group">
                    <label><Mail size={14} /> Email Address</label>
                    <input 
                      type="email" 
                      required 
                      value={authFormData.email}
                      onChange={(e) => setAuthFormData({...authFormData, email: e.target.value})}
                      placeholder="john@example.com"
                    />
                  </div>
                )}

                <div className="form-group">
                  <label><Lock size={14} /> Password</label>
                  <input 
                    type="password" 
                    required 
                    value={authFormData.password}
                    onChange={(e) => setAuthFormData({...authFormData, password: e.target.value})}
                    placeholder="••••••••"
                  />
                </div>

                {authError && <p style={{color: '#ef4444', fontSize: '0.85rem'}}>{authError}</p>}

                <button type="submit" className="btn-primary full-width">
                  {authMode === 'login' ? 'Sign In' : 'Sign Up'}
                </button>
              </form>

              <div className="auth-switch">
                {authMode === 'login' ? (
                  <>Don't have an account? <span onClick={() => setAuthMode('signup')}>Sign Up</span></>
                ) : (
                  <>Already have an account? <span onClick={() => setAuthMode('login')}>Sign In</span></>
                )}
              </div>
            </motion.div>
          </motion.div>
        )}

        {/* Event Details Modal */}
        {selectedEvent && !showAuthModal && (
          <motion.div 
            className="modal-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <motion.div 
              className="modal-content glass"
              initial={{ y: 50, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              exit={{ y: 50, opacity: 0 }}
            >
              <button className="close-btn" onClick={() => setSelectedEvent(null)}>
                <X size={24} />
              </button>
              
              <div className="modal-header">
                <h2>{selectedEvent.title}</h2>
                <div className="modal-badges">
                  <span className="badge"><Calendar size={16} /> {new Date(selectedEvent.date).toLocaleString()}</span>
                  <span className="badge"><MapPin size={16} /> {selectedEvent.location}</span>
                </div>
              </div>

              <div className="modal-body">
                <h3>About this event</h3>
                <p>{selectedEvent.description}</p>
                
                <div className="organizer-info">
                  <div className="avatar">{selectedEvent.organizer.username[0].toUpperCase()}</div>
                  <div>
                    <label>Organized by</label>
                    <p>{selectedEvent.organizer.username} ({selectedEvent.organizer.email})</p>
                  </div>
                </div>
              </div>

              <div className="modal-footer">
                <AnimatePresence mode="wait">
                  {registrationSuccess ? (
                    <motion.div 
                      key="success"
                      className="success-container"
                      initial={{ opacity: 0, scale: 0.9 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.9 }}
                    >
                      <CheckCircle size={32} className="success-icon" />
                      <div>
                        <h4>Registration Successful!</h4>
                        <p>We've sent the details to your email.</p>
                      </div>
                    </motion.div>
                  ) : (
                    <motion.button 
                      key="register-btn"
                      className="btn-primary full-width"
                      onClick={() => handleRegister(selectedEvent.id)}
                      disabled={isRegistering}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                    >
                      {token ? (isRegistering ? 'Processing...' : 'Register for Event') : 'Sign in to Register'}
                    </motion.button>
                  )}
                </AnimatePresence>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      <footer>
        <p>&copy; 2026 EventHub. Powered by Django & React.</p>
      </footer>
    </div>
  )
}

export default App
