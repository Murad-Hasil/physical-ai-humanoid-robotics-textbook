/**
 * Custom Navbar Component with Full Auth Integration
 *
 * Features:
 * - Auth state management
 * - Admin-only menu
 * - Responsive design
 * - All project links
 */

import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '@site/src/hooks/useAuth';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

export default function CustomNavbar() {
  const { user, loading, logout } = useAuth();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isAdminMenuOpen, setIsAdminMenuOpen] = useState(false);
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);

  const userMenuRef = useRef<HTMLDivElement>(null);
  const adminMenuRef = useRef<HTMLDivElement>(null);

  // Check if user is admin (SSR-safe localStorage access)
  const isAdmin = user?.is_admin ||
    (typeof window !== 'undefined' && localStorage.getItem('is_admin') === 'true');

  /**
   * Handle logout
   */
  const handleLogout = async () => {
    await logout();
    window.location.href = '/physical-ai-humanoid-robotics-textbook/';
  };

  /**
   * Close all dropdowns
   */
  const closeAllDropdowns = () => {
    setIsAdminMenuOpen(false);
    setIsUserMenuOpen(false);
    setIsMobileMenuOpen(false);
  };

  // Close dropdowns when clicking outside the menu refs
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      const target = event.target as Node;
      const inUser = userMenuRef.current?.contains(target);
      const inAdmin = adminMenuRef.current?.contains(target);
      if (!inUser && !inAdmin) {
        setIsUserMenuOpen(false);
        setIsAdminMenuOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <nav
      className="navbar navbar--fixed-top"
      style={{
        background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)',
        borderBottom: '2px solid #06b6d4',
        boxShadow: '0 4px 6px rgba(6, 182, 212, 0.3)',
      }}
    >
      <div className="navbar__inner" style={{ alignItems: 'center' }}>
        <div className="navbar__items">
          {/* Logo */}
          <Link className="navbar__brand" to="/">
            <span style={{ fontSize: '1.5rem', marginRight: '0.5rem' }}>🤖</span>
            <span className="navbar__title" style={{ 
              color: '#06b6d4',
              fontWeight: 'bold',
              fontSize: '1.25rem'
            }}>
              Physical AI
            </span>
          </Link>

          {/* Desktop Navigation Links */}
          <Link className="navbar__item navbar__link" to="/docs/introduction-to-physical-ai" style={{ color: '#E0E0E0' }}>
            📚 Docs
          </Link>
          <Link className="navbar__item navbar__link" to="/roadmap" style={{ color: '#E0E0E0' }}>
            🗺️ 13-Week Roadmap
          </Link>
          <Link className="navbar__item navbar__link" to="/profile" style={{ color: '#E0E0E0' }}>
            🖥️ Hardware Dashboard
          </Link>
        </div>

        {/* Right Side - Auth & Admin */}
        <div className="navbar__items navbar__items--right">
          {loading ? (
            <span className="navbar__item navbar__link">Loading...</span>
          ) : user ? (
            <>
              {/* Admin Menu (Admin Only) */}
              {isAdmin && (
                <div ref={adminMenuRef} className="navbar__item" style={{ position: 'relative', display: 'flex', alignItems: 'center' }}>
                  <button
                    onClick={() => { setIsAdminMenuOpen(v => !v); setIsUserMenuOpen(false); }}
                    style={{
                      background: 'rgba(255, 107, 53, 0.1)',
                      border: '1px solid #ff6b35',
                      borderRadius: '8px',
                      padding: '0.4rem 0.9rem',
                      color: '#ff6b35',
                      fontWeight: 'bold',
                      cursor: 'pointer',
                      fontSize: '0.875rem',
                      lineHeight: '1.5',
                      whiteSpace: 'nowrap',
                    }}
                  >
                    🛡️ Admin
                  </button>
                  {isAdminMenuOpen && (
                    <div style={{
                      position: 'absolute',
                      top: '100%',
                      right: 0,
                      marginTop: '0.5rem',
                      background: '#1a1a2e',
                      border: '1px solid #ff6b35',
                      borderRadius: '8px',
                      boxShadow: '0 4px 6px rgba(255, 107, 53, 0.3)',
                      zIndex: 1000,
                      minWidth: '180px',
                    }}>
                      <Link
                        className="dropdown__link"
                        to="/admin/ingest"
                        onClick={closeAllDropdowns}
                        style={{ color: '#ff6b35', display: 'block', padding: '0.5rem 1rem' }}
                      >
                        📤 Knowledge Base
                      </Link>
                      <Link
                        className="dropdown__link"
                        to="/admin/status"
                        onClick={closeAllDropdowns}
                        style={{ color: '#ff6b35', display: 'block', padding: '0.5rem 1rem' }}
                      >
                        📊 System Status
                      </Link>
                    </div>
                  )}
                </div>
              )}

              {/* User Menu */}
              <div ref={userMenuRef} className="navbar__item" style={{ position: 'relative', display: 'flex', alignItems: 'center' }}>
                <button
                  onClick={() => { setIsUserMenuOpen(v => !v); setIsAdminMenuOpen(false); }}
                  style={{
                    background: 'rgba(6, 182, 212, 0.1)',
                    border: '1px solid #06b6d4',
                    borderRadius: '8px',
                    padding: '0.4rem 0.9rem',
                    color: '#06b6d4',
                    fontWeight: 'bold',
                    cursor: 'pointer',
                    fontSize: '0.875rem',
                    lineHeight: '1.5',
                    maxWidth: '200px',
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    whiteSpace: 'nowrap',
                  }}
                >
                  👤 {user.email}
                </button>
                {isUserMenuOpen && (
                  <div style={{
                    position: 'absolute',
                    top: '100%',
                    right: 0,
                    marginTop: '0.5rem',
                    background: '#1a1a2e',
                    border: '1px solid #06b6d4',
                    borderRadius: '8px',
                    boxShadow: '0 4px 6px rgba(6, 182, 212, 0.3)',
                    zIndex: 1000,
                    minWidth: '180px',
                  }}>
                    <Link
                      className="dropdown__link"
                      to="/profile"
                      onClick={closeAllDropdowns}
                      style={{ color: '#06b6d4', display: 'block', padding: '0.5rem 1rem' }}
                    >
                      🖥️ My Dashboard
                    </Link>
                    <hr style={{
                      margin: '0.5rem 0',
                      borderColor: 'rgba(6, 182, 212, 0.2)',
                    }} />
                    <button
                      onClick={handleLogout}
                      style={{
                        color: '#ff6b6b',
                        background: 'none',
                        border: 'none',
                        cursor: 'pointer',
                        width: '100%',
                        textAlign: 'left',
                        padding: '0.5rem 1rem',
                        fontWeight: 'bold',
                      }}
                    >
                      🚪 Logout
                    </button>
                  </div>
                )}
              </div>
            </>
          ) : (
            <>
              {/* Login & Signup Buttons */}
              <Link
                className="navbar__item navbar__link"
                to="/login"
                style={{
                  color: '#06b6d4',
                  fontWeight: 'bold',
                }}
              >
                🔐 Login
              </Link>
              <Link
                className="navbar__item navbar__link button button--primary"
                to="/signup"
                style={{
                  background: '#ff6b35',
                  border: 'none',
                  borderRadius: '8px',
                  padding: '0.5rem 1rem',
                  fontWeight: 'bold',
                }}
              >
                ✨ Sign Up
              </Link>
            </>
          )}

          {/* Mobile Menu Toggle */}
          <button
            className="navbar__toggle"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            style={{
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              padding: '0.5rem',
              color: '#06b6d4',
            }}
          >
            {isMobileMenuOpen ? '✕' : '☰'}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <div
          className="navbar-sidebar"
          style={{
            background: '#1a1a2e',
            position: 'fixed',
            top: '60px',
            left: 0,
            right: 0,
            bottom: 0,
            zIndex: 1000,
            padding: '1rem',
            overflowY: 'auto',
          }}
        >
          <div className="navbar-sidebar__items">
            <div className="navbar-sidebar__item menu">
              <Link
                className="menu__link"
                to="/docs/introduction-to-physical-ai"
                onClick={closeAllDropdowns}
                style={{ color: '#06b6d4', padding: '0.75rem 0' }}
              >
                📚 Docs
              </Link>
              <Link
                className="menu__link"
                to="/roadmap"
                onClick={closeAllDropdowns}
                style={{ color: '#06b6d4', padding: '0.75rem 0' }}
              >
                🗺️ Roadmap
              </Link>
              <Link
                className="menu__link"
                to="/profile"
                onClick={closeAllDropdowns}
                style={{ color: '#06b6d4', padding: '0.75rem 0' }}
              >
                🖥️ Dashboard
              </Link>
              
              {isAdmin && (
                <>
                  <hr style={{ 
                    margin: '1rem 0', 
                    borderColor: 'rgba(255, 107, 53, 0.2)' 
                  }} />
                  <div style={{ color: '#ff6b35', fontWeight: 'bold', marginBottom: '0.5rem' }}>
                    🛡️ Admin
                  </div>
                  <Link
                    className="menu__link"
                    to="/admin/ingest"
                    onClick={closeAllDropdowns}
                    style={{ color: '#ff6b35', padding: '0.75rem 0' }}
                  >
                    📤 Knowledge Base
                  </Link>
                  <Link
                    className="menu__link"
                    to="/admin/status"
                    onClick={closeAllDropdowns}
                    style={{ color: '#ff6b35', padding: '0.75rem 0' }}
                  >
                    📊 System Status
                  </Link>
                </>
              )}
              
              <hr style={{ 
                margin: '1rem 0', 
                borderColor: 'rgba(6, 182, 212, 0.2)' 
              }} />
              
              {user ? (
                <button
                  className="menu__link"
                  onClick={handleLogout}
                  style={{ 
                    color: '#ff6b6b',
                    background: 'none',
                    border: 'none',
                    cursor: 'pointer',
                    width: '100%',
                    textAlign: 'left',
                    padding: '0.75rem 0',
                    fontWeight: 'bold',
                  }}
                >
                  🚪 Logout
                </button>
              ) : (
                <>
                  <Link
                    className="menu__link"
                    to="/login"
                    onClick={closeAllDropdowns}
                    style={{ color: '#06b6d4', padding: '0.75rem 0' }}
                  >
                    🔐 Login
                  </Link>
                  <Link
                    className="menu__link"
                    to="/signup"
                    onClick={closeAllDropdowns}
                    style={{ color: '#ff6b35', padding: '0.75rem 0', fontWeight: 'bold' }}
                  >
                    ✨ Sign Up
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </nav>
  );
}
