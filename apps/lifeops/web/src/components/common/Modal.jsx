import React, { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { X } from 'lucide-react';
import './Modal.css';

export function Modal({ isOpen, onClose, title, children, maxWidth = '550px' }) {
  const [dragOffset, setDragOffset] = useState(0);
  const [isDragging, setIsDragging] = useState(false);
  const touchStartY = useRef(0);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') onClose();
    };
    if (isOpen) {
      document.body.classList.add('modal-open');
      window.addEventListener('keydown', handleKeyDown);
    }
    return () => {
      document.body.classList.remove('modal-open');
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [isOpen, onClose]);

  // Touch Drag on Handle/Header to slide down & close
  const handleTouchStart = (e) => {
    touchStartY.current = e.touches[0].clientY;
    setIsDragging(true);
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
    
    // If dragged down more than 80px, close modal
    if (dragOffset > 80) {
      onClose();
    }
    setDragOffset(0);
  };

  if (!isOpen) return null;

  // Use createPortal to render directly into document.body
  // This bypasses any ancestor transform / animation / overflow constraints!
  return createPortal(
    <div className="modal-backdrop" onClick={onClose}>
      <div 
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
          title="Desliza hacia abajo para cerrar"
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

        {/* Modal Body with guaranteed flexbox scrolling */}
        <div className="modal-body">
          {children}
        </div>
      </div>
    </div>,
    document.body
  );
}
