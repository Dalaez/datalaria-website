import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { Header } from './Header';
import { BottomNav } from './BottomNav';

export function MainLayout() {
  const [collapsed, setCollapsed] = useState(() => {
    return localStorage.getItem('lifeops_sidebar_collapsed') === 'true';
  });
  const [mobileDrawerOpen, setMobileDrawerOpen] = useState(false);

  const toggleSidebar = () => {
    // If on mobile (screen <= 768px), toggle drawer
    if (window.innerWidth <= 768) {
      setMobileDrawerOpen((prev) => !prev);
    } else {
      setCollapsed((prev) => {
        const next = !prev;
        localStorage.setItem('lifeops_sidebar_collapsed', String(next));
        return next;
      });
    }
  };

  const closeMobileDrawer = () => {
    setMobileDrawerOpen(false);
  };

  return (
    <div className={`app-container ${collapsed ? 'sidebar-collapsed' : ''}`}>
      {/* Mobile Drawer Overlay Backdrop */}
      {mobileDrawerOpen && (
        <div 
          className="mobile-drawer-backdrop" 
          onClick={closeMobileDrawer}
          aria-hidden="true"
        />
      )}

      {/* Sidebar (Desktop Collapsible / Mobile Off-Canvas Drawer) */}
      <Sidebar 
        collapsed={collapsed} 
        toggleSidebar={toggleSidebar} 
        mobileOpen={mobileDrawerOpen}
        closeMobile={closeMobileDrawer}
      />

      <div className="main-content">
        <Header 
          collapsed={collapsed} 
          toggleSidebar={toggleSidebar} 
          mobileDrawerOpen={mobileDrawerOpen}
        />
        <main className="page-wrapper animate-fade-in">
          <Outlet />
        </main>
      </div>

      {/* Mobile Bottom Navigation Bar */}
      <BottomNav />
    </div>
  );
}
