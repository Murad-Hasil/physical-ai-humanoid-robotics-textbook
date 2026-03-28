import type {ReactNode} from 'react';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import CyberFooter from '@site/src/components/CyberFooter';

import styles from './index.module.css';

const TECH_CARDS = [
  {
    icon: '🤖',
    title: 'Edge AI',
    color: '#00F3FF',
    delay: '0s',
    desc: 'Deploy AI models on resource-constrained devices like NVIDIA Jetson Orin Nano with real-time inference.',
    points: ['NVIDIA Jetson Platform', 'TensorRT Optimization', 'Real-time Inference'],
  },
  {
    icon: '🧠',
    title: 'RAG Systems',
    color: '#00F3FF',
    delay: '0.15s',
    desc: 'Build intelligent chatbots with Retrieval-Augmented Generation using vector databases and LLMs.',
    points: ['Qdrant Vector DB', 'Grok LLaMA 3.3 70B', 'Hardware-Aware Context'],
  },
  {
    icon: '🦾',
    title: 'Sim-to-Real',
    color: '#00F3FF',
    delay: '0.3s',
    desc: 'Bridge the gap between simulation and reality — deploy policies trained in Gazebo to real robots.',
    points: ['Gazebo Simulation', 'Unitree Go1 Robot', 'Policy Transfer'],
  },
  {
    icon: '🔧',
    title: 'ROS 2 & Gazebo',
    color: '#A78BFA',
    delay: '0.45s',
    desc: 'Master the Robot Operating System 2 for building modular, production-grade robotic applications.',
    points: ['ROS 2 Humble', 'Nav2 Stack', 'Custom Packages'],
  },
  {
    icon: '🎮',
    title: 'NVIDIA Isaac',
    color: '#A78BFA',
    delay: '0.6s',
    desc: 'Use NVIDIA Isaac Sim for physics-accurate robot simulation and synthetic data generation.',
    points: ['Isaac Sim', 'Synthetic Data', 'GPU Acceleration'],
  },
  {
    icon: '💬',
    title: 'Conversational AI',
    color: '#A78BFA',
    delay: '0.75s',
    desc: 'Give robots a voice — build humanoid conversational interfaces with real-time speech & NLP.',
    points: ['Speech-to-Text', 'LLM Reasoning', 'Text-to-Speech'],
  },
];

const JOURNEY_STEPS = [
  {
    step: '01',
    icon: '⚙️',
    title: 'Hardware Setup',
    desc: 'Configure your hardware profile — RTX GPU, Jetson Orin, or Unitree robot. The curriculum adapts to what you have.',
    link: '/profile',
    linkLabel: 'Configure →',
  },
  {
    step: '02',
    icon: '📚',
    title: 'Learn Foundations',
    desc: 'Start with Physical AI fundamentals, ROS 2 basics, and Python robotics — weeks 1–4 build your core skills.',
    link: '/docs/introduction-to-physical-ai',
    linkLabel: 'Start Week 1 →',
  },
  {
    step: '03',
    icon: '🧠',
    title: 'Build RAG Pipeline',
    desc: 'Wire up Qdrant + Grok LLaMA to build a chatbot that knows your robot docs — weeks 5–9.',
    link: '/roadmap',
    linkLabel: 'View Roadmap →',
  },
  {
    step: '04',
    icon: '🚀',
    title: 'Deploy to Robot',
    desc: 'Take your trained policies from Isaac Sim to a real Unitree Go1 — the full Sim-to-Real pipeline.',
    link: '/roadmap',
    linkLabel: 'See Weeks 10–13 →',
  },
];

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={styles.heroBanner}>
      <div className="cyber-grid-overlay" />
      <div className="container" style={{ position: 'relative', zIndex: 1, paddingTop: '5rem', paddingBottom: '4rem' }}>
        <div className={styles.heroRow}>
          {/* Left — Text */}
          <div className={styles.heroLeft}>
            <Heading as="h1" className={styles.heroTitle}>
              Physical AI: The Humanoid Robotics OS
            </Heading>
            <p className={styles.heroSubtitle}>
              Master the future of robotics with our comprehensive curriculum covering Edge AI, RAG systems, and Sim-to-Real deployment.
            </p>
            <div className={styles.heroButtons}>
              <Link className="cyber-button cyber-button-primary" to="/docs/introduction-to-physical-ai">
                🚀 Get Started
              </Link>
              <Link className="cyber-button cyber-button-secondary" to="/roadmap">
                📊 View Roadmap
              </Link>
            </div>

            {/* Stats */}
            <div className={styles.statsRow}>
              {[
                { value: '13', label: 'Weeks Program' },
                { value: '50+', label: 'Lessons' },
                { value: '100%', label: 'Hands-on' },
              ].map(({ value, label }) => (
                <div key={label} className="glass-panel" style={{ textAlign: 'center', padding: '1rem', flex: 1 }}>
                  <div style={{ fontSize: '1.75rem', fontWeight: 'bold', color: '#00F3FF' }}>{value}</div>
                  <div style={{ fontSize: '0.85rem', color: '#A0A0B0' }}>{label}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Right — Preview panel */}
          <div className={styles.heroRight}>
            <div className="glass-panel" style={{
              padding: '2rem',
              background: 'linear-gradient(135deg, rgba(0,243,255,0.06) 0%, rgba(0,128,255,0.06) 100%)',
              border: '1px solid rgba(0, 243, 255, 0.3)',
              borderRadius: '16px',
            }}>
              <h3 style={{ color: '#00F3FF', marginBottom: '1.25rem', fontSize: '1.3rem' }}>
                🤖 Edge AI + RAG + Sim-to-Real
              </h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
                {[
                  { name: 'NVIDIA Jetson Orin', desc: 'Deploy AI models on edge devices with real-time inference' },
                  { name: 'Unitree Go1', desc: 'Program humanoid robots with ROS 2 and Gazebo' },
                  { name: 'RAG Pipeline', desc: 'Build intelligent chatbots with vector databases' },
                ].map(({ name, desc }) => (
                  <div key={name} className="glass-panel" style={{
                    padding: '0.9rem 1rem',
                    border: '1px solid rgba(0, 243, 255, 0.15)',
                    borderRadius: '10px',
                  }}>
                    <strong style={{ color: '#00F3FF', fontSize: '0.95rem' }}>{name}</strong>
                    <p style={{ margin: '0.35rem 0 0', fontSize: '0.85rem', color: '#A0A0B0', lineHeight: 1.5 }}>{desc}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

export default function Home(): ReactNode {
  return (
    <Layout
      title="Physical AI: The Humanoid Robotics OS"
      description="Master Physical AI with our comprehensive curriculum covering Edge AI, RAG, and Sim-to-Real deployment">
      <HomepageHeader />

      <main style={{ background: 'linear-gradient(180deg, #111111 0%, #1A1A2E 100%)' }}>

        {/* ── Core Technologies — 6 cards ── */}
        <section className={styles.section}>
          <div className="container">
            <h2 className={styles.sectionTitle}>🚀 Core Technologies</h2>
            <p className={styles.sectionSubtitle}>
              Six pillars that form the complete Physical AI stack — from hardware to simulation to deployment.
            </p>
            <div className={styles.cardsGrid}>
              {TECH_CARDS.map((card) => (
                <div key={card.title} className={styles.techCard} style={{ animationDelay: card.delay }}>
                  <div style={{ fontSize: '2.5rem', marginBottom: '0.75rem' }}>{card.icon}</div>
                  <h3 style={{ color: card.color, marginBottom: '0.75rem', fontSize: '1.25rem' }}>{card.title}</h3>
                  <p style={{ color: '#A0A0B0', lineHeight: 1.6, fontSize: '0.9rem', marginBottom: '1rem' }}>{card.desc}</p>
                  <ul style={{ color: '#E0E0E0', paddingLeft: '1.1rem', margin: 0 }}>
                    {card.points.map(p => (
                      <li key={p} style={{ marginBottom: '0.35rem', fontSize: '0.85rem' }}>{p}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── Learning Journey — 4 steps ── */}
        <section className={styles.section} style={{ background: 'rgba(0, 243, 255, 0.02)', borderTop: '1px solid rgba(0,243,255,0.1)', borderBottom: '1px solid rgba(0,243,255,0.1)' }}>
          <div className="container">
            <h2 className={styles.sectionTitle}>🗺️ Your Learning Journey</h2>
            <p className={styles.sectionSubtitle}>Four milestones from zero to deploying AI on a real robot.</p>
            <div className={styles.journeyGrid}>
              {JOURNEY_STEPS.map((step, i) => (
                <div key={step.step} className={styles.journeyCard}>
                  {/* Step number connector */}
                  <div style={{ display: 'flex', alignItems: 'center', marginBottom: '1rem', gap: '1rem' }}>
                    <div style={{
                      width: '48px', height: '48px', borderRadius: '50%',
                      background: 'linear-gradient(135deg, rgba(0,243,255,0.15), rgba(0,128,255,0.15))',
                      border: '2px solid #00F3FF',
                      display: 'flex', alignItems: 'center', justifyContent: 'center',
                      flexShrink: 0,
                      color: '#00F3FF', fontWeight: 'bold', fontSize: '0.85rem',
                    }}>
                      {step.step}
                    </div>
                    {i < JOURNEY_STEPS.length - 1 && (
                      <div className={styles.journeyConnector} />
                    )}
                  </div>
                  <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>{step.icon}</div>
                  <h3 style={{ color: '#00F3FF', fontSize: '1.1rem', marginBottom: '0.5rem' }}>{step.title}</h3>
                  <p style={{ color: '#A0A0B0', fontSize: '0.875rem', lineHeight: 1.6, marginBottom: '1rem' }}>{step.desc}</p>
                  <Link to={step.link} style={{ color: '#00F3FF', fontSize: '0.875rem', fontWeight: 'bold', textDecoration: 'none' }}>
                    {step.linkLabel}
                  </Link>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── CTA Banner ── */}
        <section className={styles.section}>
          <div className="container">
            <div className={styles.ctaBanner}>
              <h2 style={{ color: '#00F3FF', fontSize: '2rem', marginBottom: '1rem', textShadow: '0 0 20px rgba(0,243,255,0.4)' }}>
                Ready to build the future?
              </h2>
              <p style={{ color: '#A0A0B0', fontSize: '1.05rem', marginBottom: '2rem', maxWidth: '500px', margin: '0 auto 2rem' }}>
                Join thousands of engineers mastering Physical AI — start free, no hardware required for the first 4 weeks.
              </p>
              <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
                <Link className="cyber-button cyber-button-primary" to="/signup">
                  ✨ Create Free Account
                </Link>
                <Link className="cyber-button cyber-button-secondary" to="/docs/introduction-to-physical-ai">
                  📚 Browse Curriculum
                </Link>
              </div>
            </div>
          </div>
        </section>

      </main>
      <CyberFooter />
    </Layout>
  );
}
