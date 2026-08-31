import React, { useEffect, useRef, useState } from 'react';
import { X } from 'lucide-react';
import './Modal.css';

export function Modal({ isOpen, onClose, title, children, maxWidth = '550px' }) {
  const [dragOffset, setDragOffset] = useState(0);
  const [isDragging, setIsDragging] = useState(false);
  const touchStartY = useRef(0);
  const modalContentRef = useRef(null);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') onClose();
    };
    if (isOpen) {
      document.body.style.overflow = 'hidden';
      window.addEventListener('keydown', handleKeyDown);
    }
    return () => {
      document.body.style.overflow = 'unset';
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [isOpen, onClose]);

  // Touch Drag down to dismiss (Mobile UX)
  const handleTouchStart = (e) => {
    // Only allow dragging if initiated at the top handle / header or when scroll is at top
    const modalBody = modalContentRef.current?.querySelector('.modal-body');
    const isAtTop = !modalBody || modalBody.scrollTop <= 0;
    
    if (isAtTop) {
      touchStartY.current = e.touches[0].clientY;
      setIsDragging(true);
    }
  };

  const handleTouchMove = (e) => {
    if (!isDragging) return;
    const currentY = e.touches[0].clientY;
    const diff = currentY - touchStartY.current;

    // Only allow pulling downwards
    if (diff > 0) {
      setDragOffset(diff);
    } else {
      setDragOffset(0);
    }
  };

  const handleTouchEnd = () => {
    if (!isDragging) return;
    setIsDragging(false);
    
    // If dragged down more than 110px, close modal
    if (dragOffset > 110) {
      onClose();
    }
    setDragOffset(0);
  };

  if (!isOpen) return null;

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div 
        ref={modalContentRef}
        className={`modal-content glass-panel ${isDragging ? 'is-dragging' : ''}`} 
        style={{ 
          maxWidth,
          transform: dragOffset > 0 ? `translateY(${dragOffset}px)` : undefined,
          transition: isDragging ? 'none' : 'transform 0.25s cubic-bezier(0.16, 1, 0.3, 1)'
        }} 
        onClick={(e) => e.stopPropagation()}
      >
        {/* Mobile Drag Handle Bar */}
        <div 
          className="modal-drag-handle-area"
          onTouchStart={handleTouchStart}
          onTouchMove={handleTouchMove}
          onTouchEnd={handleTouchEnd}
        >
          <div className="modal-drag-pill" />
        </div>

        {/* Modal Header */}
        <div 
          className="modal-header"
          onTouchStart={handleTouchStart}
          onTouchMove={handleTouchMove}
          onTouchEnd={handleTouchEnd}
        >
          <h3 className="modal-title">{title}</h3>
          <button className="modal-close-btn" onClick={onClose} title="Cerrar (Esc)">
            <X size={18} />
          </button>
        </div>

        {/* Modal Body with guaranteed flex scrolling */}
        <div className="modal-body">
          {children}
        </div>
      </div>
    </div>
  );
}
