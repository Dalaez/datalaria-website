import React from 'react';
import { useSearchParams } from 'react-router-dom';
import { KanbanBoard } from '../components/Professional/KanbanBoard';
import { ProjectsManager } from '../components/Professional/ProjectsManager';
import { CheckSquare, FolderKanban } from 'lucide-react';
import './ProfessionalPage.css';

export function ProfessionalPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const currentTab = searchParams.get('tab') || 'kanban';

  const setTab = (tab) => {
    setSearchParams({ tab });
  };

  return (
    <div className="professional-page">
      {/* Header */}
      <div className="page-header-title">
        <h1>📋 Área Profesional</h1>
        <p>Gestión de proyectos, prioridades y tablero Kanban de tareas operativas.</p>
      </div>

      {/* Tab Switcher */}
      <div className="tab-switcher glass-panel">
        <button 
          className={`tab-btn ${currentTab === 'kanban' ? 'active' : ''}`}
          onClick={() => setTab('kanban')}
        >
          <CheckSquare size={17} />
          <span>Tablero Kanban (Tareas)</span>
        </button>

        <button 
          className={`tab-btn ${currentTab === 'projects' ? 'active' : ''}`}
          onClick={() => setTab('projects')}
        >
          <FolderKanban size={17} />
          <span>Portafolio de Proyectos</span>
        </button>
      </div>

      {/* Tab Content */}
      <div className="tab-content animate-fade-in">
        {currentTab === 'kanban' && <KanbanBoard />}
        {currentTab === 'projects' && <ProjectsManager />}
      </div>
    </div>
  );
}
