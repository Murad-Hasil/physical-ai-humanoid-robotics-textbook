import type {ReactNode} from 'react';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import CyberFooter from '@site/src/components/CyberFooter';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={`hero hero--dark ${styles.heroBanner}`}>
      {/* Cyber Grid Overlay */}
      <div className="cyber-grid-overlay" />
      
      <div className="container" style={{ position: 'relative', zIndex: 1 }}>
        <div className="row hero-content-row">
          {/* Left Side - Text Content */}
          <div className="col col--6">
            <Heading as="h1" className="hero__title" style={{ 
              fontSize: '3.5rem',
              fontWeight: 'bold',
              color: '#00F3FF',
              textShadow: '0 0 20px rgba(0, 243, 255, 0.5)',
              marginBottom: '1.5rem'
            }}>
              Physical AI: The Humanoid Robotics OS
            </Heading>
            
            <p className="hero__subtitle" style={{ 
              fontSize: '1.25rem',
              color: '#E0E0E0',
              marginBottom: '2rem',
              lineHeight: '1.6'
            }}>
              Master the future of robotics with our comprehensive curriculum covering Edge AI, RAG systems, and Sim-to-Real deployment.
            </p>
            
            <div className={styles.buttons} style={{ display: 'flex', gap: '1rem' }}>
              <Link
                className="cyber-button cyber-button-primary"
                to="/docs/introduction-to-physical-ai"
                style={{ 
                  display: 'inline-block',
                  textDecoration: 'none',
                  fontSize: '1.1rem',
                  padding: '14px 32px'
                }}>
                🚀 Get Started
              </Link>
              <Link
                className="cyber-button cyber-button-secondary"
                to="/roadmap"
                style={{ 
                  display: 'inline-block',
                  textDecoration: 'none',
                  fontSize: '1.1rem',
                  padding: '14px 32px'
                }}>
                📊 View Roadmap
              </Link>
            </div>
            
            {/* GIAIC Stats */}
            <div className="row" style={{ marginTop: '3rem', paddingTop: '2rem', borderTop: '1px solid rgba(0, 243, 255, 0.2)' }}>
              <div className="col col--4">
                <div className="glass-panel" style={{ textAlign: 'center', padding: '1rem' }}>
                  <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#00F3FF' }}>13</div>
                  <div style={{ fontSize: '0.9rem', color: '#A0A0B0' }}>Weeks Program</div>
                </div>
              </div>
              <div className="col col--4">
                <div className="glass-panel" style={{ textAlign: 'center', padding: '1rem' }}>
                  <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#00F3FF' }}>50+</div>
                  <div style={{ fontSize: '0.9rem', color: '#A0A0B0' }}>Lessons</div>
                </div>
              </div>
              <div className="col col--4">
                <div className="glass-panel" style={{ textAlign: 'center', padding: '1rem' }}>
                  <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#00F3FF' }}>100%</div>
                  <div style={{ fontSize: '0.9rem', color: '#A0A0B0' }}>Hands-on</div>
                </div>
              </div>
            </div>
          </div>
          
          {/* Right Side - UI Preview */}
          <div className="col col--6">
            <div className="glass-panel animate-float" style={{ 
              padding: '2rem',
              animation: 'float 3s ease-in-out infinite'
            }}>
              <div style={{ 
                background: 'linear-gradient(135deg, rgba(0, 243, 255, 0.1) 0%, rgba(0, 128, 255, 0.1) 100%)',
                borderRadius: '12px',
                padding: '2rem',
                border: '1px solid rgba(0, 243, 255, 0.3)'
              }}>
                <h3 style={{ color: '#00F3FF', marginBottom: '1rem', fontSize: '1.5rem' }}>
                  🤖 Edge AI + RAG + Sim-to-Real
                </h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                  <div className="glass-panel" style={{ 
                    padding: '1rem',
                    border: '1px solid rgba(0, 243, 255, 0.2)',
                    transition: 'all 0.2s ease-in-out'
                  }}>
                    <strong style={{ color: '#00F3FF' }}>NVIDIA Jetson Orin</strong>
                    <p style={{ margin: '0.5rem 0 0', fontSize: '0.9rem', color: '#A0A0B0' }}>
                      Deploy AI models on edge devices with real-time inference
                    </p>
                  </div>
                  <div className="glass-panel" style={{ 
                    padding: '1rem',
                    border: '1px solid rgba(0, 243, 255, 0.2)',
                    transition: 'all 0.2s ease-in-out'
                  }}>
                    <strong style={{ color: '#00F3FF' }}>Unitree Go1</strong>
                    <p style={{ margin: '0.5rem 0 0', fontSize: '0.9rem', color: '#A0A0B0' }}>
                      Program humanoid robots with ROS 2 and Gazebo
                    </p>
                  </div>
                  <div className="glass-panel" style={{ 
                    padding: '1rem',
                    border: '1px solid rgba(0, 243, 255, 0.2)',
                    transition: 'all 0.2s ease-in-out'
                  }}>
                    <strong style={{ color: '#00F3FF' }}>RAG Pipeline</strong>
                    <p style={{ margin: '0.5rem 0 0', fontSize: '0.9rem', color: '#A0A0B0' }}>
                      Build intelligent chatbots with vector databases
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title="Physical AI: The Humanoid Robotics OS"
      description="Master Physical AI with our comprehensive curriculum covering Edge AI, RAG, and Sim-to-Real deployment">
      <HomepageHeader />
      <main>
        {/* Feature Cards Section */}
        <section style={{ 
          padding: '4rem 0',
          background: 'linear-gradient(180deg, #111111 0%, #1A1A2E 100%)'
        }}>
          <div className="container">
            <h2 style={{ 
              textAlign: 'center',
              color: '#00F3FF',
              fontSize: '2.5rem',
              marginBottom: '3rem',
              textShadow: '0 0 20px rgba(0, 243, 255, 0.5)'
            }}>
              🚀 Core Technologies
            </h2>
            <div className="row feature-cards-row" style={{ justifyContent: 'center' }}>
              {/* Card 1: Edge AI */}
              <div className="col col--4">
                <div className="glass-panel cyber-card animate-float" style={{
                  height: '100%',
                  padding: '2rem',
                  border: '1px solid rgba(0, 243, 255, 0.3)',
                  transition: 'all 0.3s ease-in-out',
                  animation: 'float 3s ease-in-out infinite'
                }}>
                  <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🤖</div>
                  <h3 style={{ color: '#00F3FF', marginBottom: '1rem', fontSize: '1.5rem' }}>
                    Edge AI
                  </h3>
                  <p style={{ color: '#A0A0B0', lineHeight: '1.6' }}>
                    Deploy AI models on resource-constrained devices like NVIDIA Jetson Orin Nano. Learn optimization techniques for real-time inference.
                  </p>
                  <ul style={{ color: '#E0E0E0', marginTop: '1.5rem', paddingLeft: '1.2rem' }}>
                    <li style={{ marginBottom: '0.5rem' }}>NVIDIA Jetson Platform</li>
                    <li style={{ marginBottom: '0.5rem' }}>TensorRT Optimization</li>
                    <li style={{ marginBottom: '0.5rem' }}>Real-time Inference</li>
                  </ul>
                </div>
              </div>
              
              {/* Card 2: RAG Systems */}
              <div className="col col--4">
                <div className="glass-panel cyber-card animate-float" style={{
                  height: '100%',
                  padding: '2rem',
                  border: '1px solid rgba(0, 243, 255, 0.3)',
                  transition: 'all 0.3s ease-in-out',
                  animation: 'float 3s ease-in-out infinite',
                  animationDelay: '0.5s'
                }}>
                  <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🧠</div>
                  <h3 style={{ color: '#00F3FF', marginBottom: '1rem', fontSize: '1.5rem' }}>
                    RAG Systems
                  </h3>
                  <p style={{ color: '#A0A0B0', lineHeight: '1.6' }}>
                    Build intelligent chatbots with Retrieval-Augmented Generation. Combine vector databases with LLMs for accurate responses.
                  </p>
                  <ul style={{ color: '#E0E0E0', marginTop: '1.5rem', paddingLeft: '1.2rem' }}>
                    <li style={{ marginBottom: '0.5rem' }}>Qdrant Vector DB</li>
                    <li style={{ marginBottom: '0.5rem' }}>Grok API Integration</li>
                    <li style={{ marginBottom: '0.5rem' }}>Hardware-Aware Context</li>
                  </ul>
                </div>
              </div>
              
              {/* Card 3: Sim-to-Real */}
              <div className="col col--4">
                <div className="glass-panel cyber-card animate-float" style={{
                  height: '100%',
                  padding: '2rem',
                  border: '1px solid rgba(0, 243, 255, 0.3)',
                  transition: 'all 0.3s ease-in-out',
                  animation: 'float 3s ease-in-out infinite',
                  animationDelay: '1s'
                }}>
                  <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🦾</div>
                  <h3 style={{ color: '#00F3FF', marginBottom: '1rem', fontSize: '1.5rem' }}>
                    Sim-to-Real
                  </h3>
                  <p style={{ color: '#A0A0B0', lineHeight: '1.6' }}>
                    Bridge the gap between simulation and reality. Deploy policies trained in Gazebo to real Unitree robots.
                  </p>
                  <ul style={{ color: '#E0E0E0', marginTop: '1.5rem', paddingLeft: '1.2rem' }}>
                    <li style={{ marginBottom: '0.5rem' }}>Gazebo Simulation</li>
                    <li style={{ marginBottom: '0.5rem' }}>Unitree Go1 Robot</li>
                    <li style={{ marginBottom: '0.5rem' }}>ROS 2 Integration</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </section>
        
        {/* Removed old HomepageFeatures - replaced with cyber theme content above */}
      </main>
      {/* Custom Cyber Footer */}
      <CyberFooter />
    </Layout>
  );
}
