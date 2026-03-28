/**
 * Custom Navbar Component with Full Auth Integration
 *
 * Features:
 * - Auth state management
 * - Admin-only menu
 * - Responsive design with working mobile sidebar
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

  const isAdmin = user?.is_admin ||
    (typeof window !== 'undefined' && localStorage.getItem('is_admin') === 'true');

  const handleLogout = async () => {
    await logout();
    window.location.href = '/physical-ai-humanoid-robotics-textbook/';
  };

  const closeAllDropdowns = () => {
    setIsAdminMenuOpen(false);
    setIsUserMenuOpen(false);
    setIsMobileMenuOpen(false);
  };

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

  // Lock body scroll when mobile menu is open
  useEffect(() => {
    if (typeof document !== 'undefined') {
      document.body.style.overflow = isMobileMenuOpen ? 'hidden' : '';
    }
    return () => {
      if (typeof document !== 'undefined') {
        document.body.style.overflow = '';
      }
    };
  }, [isMobileMenuOpen]);

  return (
    <>
      <nav
        className="navbar navbar--fixed-top"
        style={{
          background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)',
          borderBottom: '2px solid #06b6d4',
          boxShadow: '0 4px 6px rgba(6, 182, 212, 0.3)',
          zIndex: 200,
        }}
      >
        <div className="navbar__inner" style={{ alignItems: 'center' }}>
          {/* Left: Logo + Desktop Nav */}
          <div className="navbar__items">
            <Link className="navbar__brand" to="/">
              <span style={{ fontSize: '1.5rem', marginRight: '0.5rem' }}>🤖</span>
              <span className="navbar__title" style={{
                color: '#06b6d4',
                fontWeight: 'bold',
                fontSize: '1.25rem',
              }}>
                Physical AI
              </span>
            </Link>

            {/* Desktop only links — hidden on mobile via CSS */}
            <Link className="navbar__item navbar__link desktop-nav-link" to="/docs/introduction-to-physical-ai" style={{ color: '#E0E0E0' }}>
              📚 Docs
            </Link>
            <Link className="navbar__item navbar__link desktop-nav-link" to="/roadmap" style={{ color: '#E0E0E0' }}>
              🗺️ Roadmap
            </Link>
            <Link className="navbar__item navbar__link desktop-nav-link" to="/profile" style={{ color: '#E0E0E0' }}>
              🖥️ Dashboard
            </Link>
          </div>

          {/* Right: Auth + Hamburger */}
          <div className="navbar__items navbar__items--right">
            {/* Desktop auth — hidden on mobile */}
            <div className="desktop-auth-items" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              {loading ? (
                <span className="navbar__item navbar__link" style={{ color: '#A0A0B0' }}>Loading...</span>
              ) : user ? (
                <>
                  {isAdmin && (
                    <div ref={adminMenuRef} style={{ position: 'relative', display: 'flex', alignItems: 'center' }}>
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
                          whiteSpace: 'nowrap',
                        }}
                      >
                        🛡️ Admin
                      </button>
                      {isAdminMenuOpen && (
                        <div style={{
                          position: 'absolute',
                          top: 'calc(100% + 0.5rem)',
                          right: 0,
                          background: '#1a1a2e',
                          border: '1px solid #ff6b35',
                          borderRadius: '8px',
                          boxShadow: '0 4px 16px rgba(255, 107, 53, 0.3)',
                          zIndex: 999,
                          minWidth: '180px',
                        }}>
                          <Link className="dropdown__link" to="/admin/ingest" onClick={closeAllDropdowns}
                            style={{ color: '#ff6b35', display: 'block', padding: '0.6rem 1rem' }}>
                            📤 Knowledge Base
                          </Link>
                          <Link className="dropdown__link" to="/admin/status" onClick={closeAllDropdowns}
                            style={{ color: '#ff6b35', display: 'block', padding: '0.6rem 1rem' }}>
                            📊 System Status
                          </Link>
                        </div>
                      )}
                    </div>
                  )}

                  <div ref={userMenuRef} style={{ position: 'relative', display: 'flex', alignItems: 'center' }}>
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
                        maxWidth: '180px',
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
                        top: 'calc(100% + 0.5rem)',
                        right: 0,
                        background: '#1a1a2e',
                        border: '1px solid #06b6d4',
                        borderRadius: '8px',
                        boxShadow: '0 4px 16px rgba(6, 182, 212, 0.3)',
                        zIndex: 999,
                        minWidth: '180px',
                      }}>
                        <Link className="dropdown__link" to="/profile" onClick={closeAllDropdowns}
                          style={{ color: '#06b6d4', display: 'block', padding: '0.6rem 1rem' }}>
                          🖥️ My Dashboard
                        </Link>
                        <hr style={{ margin: '0.25rem 0', borderColor: 'rgba(6, 182, 212, 0.2)' }} />
                        <button onClick={handleLogout} style={{
                          color: '#ff6b6b', background: 'none', border: 'none',
                          cursor: 'pointer', width: '100%', textAlign: 'left',
                          padding: '0.6rem 1rem', fontWeight: 'bold',
                        }}>
                          🚪 Logout
                        </button>
                      </div>
                    )}
                  </div>
                </>
              ) : (
                <>
                  <Link className="navbar__item navbar__link" to="/login"
                    style={{ color: '#06b6d4', fontWeight: 'bold' }}>
                    🔐 Login
                  </Link>
                  <Link className="navbar__item navbar__link" to="/signup"
                    style={{
                      background: '#ff6b35', border: 'none', borderRadius: '8px',
                      padding: '0.4rem 1rem', fontWeight: 'bold', color: '#fff',
                    }}>
                    ✨ Sign Up
                  </Link>
                </>
              )}
            </div>

            {/* Hamburger toggle — visible only on mobile */}
            <button
              className="navbar__toggle"
              aria-label="Toggle navigation"
              onClick={() => setIsMobileMenuOpen(v => !v)}
              style={{
                background: 'none',
                border: '1px solid rgba(6, 182, 212, 0.4)',
                borderRadius: '6px',
                cursor: 'pointer',
                padding: '0.4rem 0.6rem',
                color: '#06b6d4',
                fontSize: '1.2rem',
                lineHeight: 1,
              }}
            >
              {isMobileMenuOpen ? '✕' : '☰'}
            </button>
          </div>
        </div>
      </nav>

      {/* Mobile Sidebar Overlay — completely separate from navbar, no conflicting Docusaurus classes */}
      {isMobileMenuOpen && (
        <div
          onClick={closeAllDropdowns}
          style={{
            position: 'fixed',
            inset: 0,
            background: 'rgba(0,0,0,0.5)',
            zIndex: 199,
          }}
        />
      )}
      <div
        style={{
          position: 'fixed',
          top: 0,
          right: 0,
          bottom: 0,
          width: '280px',
          background: 'linear-gradient(180deg, #1a1a2e 0%, #16213e 100%)',
          borderLeft: '2px solid #06b6d4',
          boxShadow: '-4px 0 24px rgba(6, 182, 212, 0.2)',
          zIndex: 300,
          overflowY: 'auto',
          padding: '1.5rem 1rem',
          transform: isMobileMenuOpen ? 'translateX(0)' : 'translateX(100%)',
          transition: 'transform 0.3s ease',
          display: 'flex',
          flexDirection: 'column',
          gap: '0.25rem',
        }}
      >
        {/* Sidebar header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
          <span style={{ color: '#06b6d4', fontWeight: 'bold', fontSize: '1.1rem' }}>🤖 Physical AI</span>
          <button
            onClick={closeAllDropdowns}
            style={{ background: 'none', border: 'none', color: '#06b6d4', cursor: 'pointer', fontSize: '1.3rem', padding: '0.25rem' }}
          >
            ✕
          </button>
        </div>

        {/* Nav links */}
        {[
          { to: '/docs/introduction-to-physical-ai', label: '📚 Docs' },
          { to: '/roadmap', label: '🗺️ Roadmap' },
          { to: '/profile', label: '🖥️ Dashboard' },
        ].map(({ to, label }) => (
          <Link
            key={to}
            to={to}
            onClick={closeAllDropdowns}
            style={{
              display: 'block',
              color: '#E0E0E0',
              padding: '0.75rem 1rem',
              borderRadius: '8px',
              textDecoration: 'none',
              fontWeight: '500',
              background: 'rgba(6, 182, 212, 0.05)',
              border: '1px solid rgba(6, 182, 212, 0.1)',
              marginBottom: '0.5rem',
            }}
          >
            {label}
          </Link>
        ))}

        {/* Admin section */}
        {isAdmin && (
          <>
            <div style={{ height: '1px', background: 'rgba(255, 107, 53, 0.2)', margin: '0.75rem 0' }} />
            <div style={{ color: '#ff6b35', fontWeight: 'bold', padding: '0.25rem 1rem', fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Admin
            </div>
            {[
              { to: '/admin/ingest', label: '📤 Knowledge Base' },
              { to: '/admin/status', label: '📊 System Status' },
            ].map(({ to, label }) => (
              <Link
                key={to}
                to={to}
                onClick={closeAllDropdowns}
                style={{
                  display: 'block',
                  color: '#ff6b35',
                  padding: '0.75rem 1rem',
                  borderRadius: '8px',
                  textDecoration: 'none',
                  fontWeight: '500',
                  background: 'rgba(255, 107, 53, 0.05)',
                  border: '1px solid rgba(255, 107, 53, 0.15)',
                  marginBottom: '0.5rem',
                }}
              >
                {label}
              </Link>
            ))}
          </>
        )}

        {/* Auth section */}
        <div style={{ height: '1px', background: 'rgba(6, 182, 212, 0.2)', margin: '0.75rem 0' }} />
        {user ? (
          <>
            <div style={{ color: '#A0A0B0', fontSize: '0.8rem', padding: '0.25rem 1rem', marginBottom: '0.5rem' }}>
              {user.email}
            </div>
            <button
              onClick={handleLogout}
              style={{
                display: 'block',
                width: '100%',
                textAlign: 'left',
                color: '#ff6b6b',
                padding: '0.75rem 1rem',
                borderRadius: '8px',
                background: 'rgba(255, 107, 107, 0.05)',
                border: '1px solid rgba(255, 107, 107, 0.15)',
                cursor: 'pointer',
                fontWeight: 'bold',
              }}
            >
              🚪 Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login" onClick={closeAllDropdowns}
              style={{
                display: 'block', color: '#06b6d4', padding: '0.75rem 1rem',
                borderRadius: '8px', textDecoration: 'none', fontWeight: 'bold',
                background: 'rgba(6, 182, 212, 0.05)', border: '1px solid rgba(6, 182, 212, 0.2)',
                marginBottom: '0.5rem',
              }}>
              🔐 Login
            </Link>
            <Link to="/signup" onClick={closeAllDropdowns}
              style={{
                display: 'block', color: '#fff', padding: '0.75rem 1rem',
                borderRadius: '8px', textDecoration: 'none', fontWeight: 'bold',
                background: '#ff6b35', border: 'none', textAlign: 'center',
              }}>
              ✨ Sign Up Free
            </Link>
          </>
        )}
      </div>
    </>
  );
}
