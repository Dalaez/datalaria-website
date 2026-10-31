import React, { useState, useEffect, useMemo, useRef } from 'react';
import {
  Activity,
  BarChart3,
  Table as TableIcon,
  Columns3,
  Calendar as CalendarIcon,
  ShieldCheck,
  Search,
  Upload,
  RefreshCw,
  ExternalLink,
  Sparkles,
  FileSpreadsheet,
  Globe,
  TrendingUp,
  X,
  ChevronLeft,
  ChevronRight,
  ArrowUpDown,
  ArrowUp,
  ArrowDown,
  Layers,
  DollarSign,
  Clock,
  Target,
  Award,
  Zap,
  Plus,
  Download,
  Trash2,
  Edit3,
  Cloud,
  LogIn,
  LogOut,
  CheckCircle2
} from 'lucide-react';
import type { User } from '@supabase/supabase-js';
import { ContentAsset, PublicPulseDataset, AssetType, AssetStatus } from './types';
import { i18n } from './lib/i18n';
import { parseNotionCsv } from './lib/notionImporter';
import { DEMO_SYNTHETIC_ASSETS } from './lib/demoData';
import {
  supabase,
  getCurrentUser,
  signInWithDemo,
  signOut as supabaseSignOut,
  fetchUserIdeas,
  insertUserIdea,
  updateUserIdea,
  deleteUserIdea,
  isSupabaseConfigured
} from './lib/supabase';
import './App.css';

type SortField =
  | 'title'
  | 'type'
  | 'status'
  | 'publish_date'
  | 'word_count'
  | 'language_parity'
  | 'seo_score'
  | 'traffic_index'
  | 'rank_pct';

export function App() {
  const [lang, setLang] = useState<'es' | 'en'>('es');
  const t = i18n[lang];

  // Vistas: Dashboard, Tabla, Kanban, Calendario, Salud & ROI (con soporte para deep linking URL ?tab=...)
  const [activeTab, setActiveTab] = useState<'dashboard' | 'table' | 'kanban' | 'calendar' | 'health'>(() => {
    if (typeof window !== 'undefined') {
      const p = new URLSearchParams(window.location.search).get('tab');
      if (p === 'table' || p === 'kanban' || p === 'calendar' || p === 'health') return p;
    }
    return 'dashboard';
  });
  const [dataset, setDataset] = useState<PublicPulseDataset | null>(null);
  const [customAssets, setCustomAssets] = useState<ContentAsset[] | null>(null);

  // Filtros interactivos
  const [search, setSearch] = useState('');
  const [typeFilter, setTypeFilter] = useState<string>('all');
  const [statusFilter, setStatusFilter] = useState<string>('all');

  // Ordenación interactiva de la tabla
  const [sortField, setSortField] = useState<SortField>('publish_date');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');

  // Paginación de la tabla
  const [pageSize, setPageSize] = useState<number>(25);
  const [currentPage, setCurrentPage] = useState<number>(1);

  // Kanban: filtro temporal por defecto (soporte URL ?kanbanWindow=all)
  const [kanbanTimeWindow, setKanbanTimeWindow] = useState<'recent' | 'all'>(() => {
    if (typeof window !== 'undefined') {
      const kw = new URLSearchParams(window.location.search).get('kanbanWindow');
      if (kw === 'all') return 'all';
    }
    return 'recent';
  });

  // Dashboard: modos de vista de categorías y cadencia
  const [categoryViewMode, setCategoryViewMode] = useState<'ecosystem' | 'themes' | 'categories'>('ecosystem');
  const [cadenceMode, setCadenceMode] = useState<'monthly' | 'yearly'>('monthly');

  // Modal para detalle y consulta de apertura de contenido
  const [selectedAssetForModal, setSelectedAssetForModal] = useState<ContentAsset | null>(null);

  // Calendario mensual estilo Notion
  const [calendarDate, setCalendarDate] = useState<Date>(() => {
    // Si estamos en 2026 usar noviembre 2026 como referencia o mes actual
    return new Date(2026, 10, 1); // Noviembre 2026 (mes 10 es Noviembre)
  });

  // Modal importador Notion
  const [isNotionModalOpen, setIsNotionModalOpen] = useState(false);
  const [notionSuccessMsg, setNotionSuccessMsg] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Ideas Locales (capturadas en el navegador)
  const STORAGE_KEY_IDEAS = 'datalaria_pulse_custom_ideas';
  const [localIdeas, setLocalIdeas] = useState<ContentAsset[]>(() => {
    try {
      const saved = localStorage.getItem('datalaria_pulse_custom_ideas');
      if (saved) return JSON.parse(saved);
    } catch (e) {
      console.warn('Error leyendo localStorage de ideas:', e);
    }
    return [];
  });

  // Guardar ideas locales en localStorage
  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY_IDEAS, JSON.stringify(localIdeas));
    } catch (e) {
      console.warn('Error guardando en localStorage:', e);
    }
  }, [localIdeas]);

  // Modal para captura / edición de Idea
  const [isIdeaModalOpen, setIsIdeaModalOpen] = useState(false);
  const [editingIdeaId, setEditingIdeaId] = useState<string | null>(null);
  const [ideaTitle, setIdeaTitle] = useState('');
  const [ideaType, setIdeaType] = useState<AssetType>('post');
  const [ideaCategory, setIdeaCategory] = useState('Inteligencia Artificial');
  const [ideaDate, setIdeaDate] = useState('');
  const [ideaBrief, setIdeaBrief] = useState('');
  const [ideaStatus, setIdeaStatus] = useState<AssetStatus>('idea');
  const [ideaSuccessMsg, setIdeaSuccessMsg] = useState('');

  // Supabase Cloud & Auth Estados (ADR-015)
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [cloudIdeas, setCloudIdeas] = useState<ContentAsset[]>([]);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [authEmail, setAuthEmail] = useState('');
  const [authPassword, setAuthPassword] = useState('');
  const [authLoading, setAuthLoading] = useState(false);
  const [authError, setAuthError] = useState('');
  const [authSuccessMsg, setAuthSuccessMsg] = useState('');

  // Estado del botón de refresco HTTP
  const [isRefreshing, setIsRefreshing] = useState(false);

  // Cargar ideas desde Supabase Cloud
  const loadCloudIdeas = async () => {
    try {
      const rows = await fetchUserIdeas();
      const mapped: ContentAsset[] = rows.map((r) => ({
        id: r.id,
        slug: `cloud-idea-${r.id.slice(0, 8)}`,
        asset_type: (r.category === 'Aplicaciones' ? 'app' : r.category === 'Kits' ? 'kit' : 'post') as AssetType,
        status: (r.status || 'idea') as AssetStatus,
        visibility: 'private',
        title_es: r.title,
        title_en: r.title,
        category: r.category || 'General',
        categories: [r.category || 'General'],
        tags: r.tags || ['idea', 'cloud'],
        publish_date: r.target_date || null,
        brief_es: r.notes || null,
        language_parity: 'complete',
        word_count_es: 0,
        word_count_en: 0,
        reading_time_min: 0,
        seo_audit: {
          score_0_100: 70,
          title_ok: true,
          description_ok: Boolean(r.notes),
          parity_ok: true,
          taxonomy_ok: true,
          internal_links_ok: false,
          issues: ['Idea sincronizada en Supabase PostgreSQL']
        },
        freshness_status: 'fresh',
        owner: r.user_id,
        social_channels: [],
        is_cloud_idea: true
      }));
      setCloudIdeas(mapped);
    } catch (e) {
      console.warn('Error cargando ideas de Supabase Cloud:', e);
    }
  };

  // Carga de datos pública y suscripción Supabase Auth
  useEffect(() => {
    fetch('./data/public.json')
      .then((res) => res.json())
      .then((data: PublicPulseDataset) => setDataset(data))
      .catch((err) => console.error('Error cargando public.json:', err));

    if (isSupabaseConfigured) {
      getCurrentUser().then((u) => {
        setCurrentUser(u);
        if (u) loadCloudIdeas();
      });

      const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
        const u = session?.user || null;
        setCurrentUser(u);
        if (u) {
          loadCloudIdeas();
        } else {
          setCloudIdeas([]);
        }
      });

      return () => {
        subscription.unsubscribe();
      };
    }
  }, []);

  // Control de roles de usuario y permisos de catálogo (ADR-015)
  const ADMIN_EMAILS = ['dalaez1@gmail.com', 'datalaria@gmail.com'];
  const userEmail = currentUser?.email?.toLowerCase() || '';
  const isAdmin = Boolean(currentUser && ADMIN_EMAILS.includes(userEmail));
  const isDemo = Boolean(currentUser && userEmail === 'demo@datalaria.com');
  const isClientUser = Boolean(currentUser && !isAdmin && !isDemo);

  const datasetAssets = dataset?.assets;
  const currentAssets = useMemo(() => {
    // 1. Si el usuario arrastró o importó un CSV de Notion, siempre tiene prioridad
    if (customAssets) return customAssets;

    // 2. Si no hay usuario logueado: Catálogo público oficial de Datalaria (135 activos)
    if (!currentUser) {
      return datasetAssets || [];
    }

    // 3. Si es el Administrador de Datalaria (dalaez1@gmail.com o datalaria@gmail.com):
    // Ve el catálogo oficial de Datalaria + sus ideas privadas en la nube
    if (isAdmin) {
      const extras = [...cloudIdeas, ...localIdeas];
      return [...extras, ...(datasetAssets || [])];
    }

    // 4. Si es la cuenta Demo (demo@datalaria.com):
    // Ve los 10 activos sintéticos interactivos + cualquier idea que cree en Supabase
    if (isDemo) {
      const userCreatedIds = new Set(cloudIdeas.map((c) => c.id));
      const demoFiltered = DEMO_SYNTHETIC_ASSETS.filter((d) => !userCreatedIds.has(d.id));
      return [...cloudIdeas, ...localIdeas, ...demoFiltered];
    }

    // 5. Si es un nuevo usuario o cliente Pro (ej. dalaez@hotmail.com o empresa externa):
    // Empieza con SU PROPIO espacio limpio (cero activos de Datalaria)
    return [...cloudIdeas, ...localIdeas];
  }, [customAssets, datasetAssets, currentUser, isAdmin, isDemo, cloudIdeas, localIdeas]);

  // Cargar plantilla de datos de ejemplo para clientes que quieran explorar inmediatamente
  const handleLoadSampleData = () => {
    setCustomAssets(DEMO_SYNTHETIC_ASSETS);
  };

  // Handlers para filtros y paginación
  const handleSearchChange = (val: string) => {
    setSearch(val);
    setCurrentPage(1);
  };

  const handleTypeChange = (val: string) => {
    setTypeFilter(val);
    setCurrentPage(1);
  };

  const handleStatusChange = (val: string) => {
    setStatusFilter(val);
    setCurrentPage(1);
  };

  const handlePageSizeChange = (val: number) => {
    setPageSize(val);
    setCurrentPage(1);
  };

  // Manejador carga CSV Notion
  const handleNotionFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      const text = event.target?.result as string;
      if (text) {
        const parsed = parseNotionCsv(text);
        if (parsed.length > 0) {
          setCustomAssets(parsed);
          setNotionSuccessMsg(t.notion_loaded_success.replace('{count}', parsed.length.toString()));
          setTimeout(() => {
            setIsNotionModalOpen(false);
            setNotionSuccessMsg('');
          }, 1500);
        }
      }
    };
    reader.readAsText(file);
  };

  const resetToDefault = () => {
    setCustomAssets(null);
  };

  // Refrescar dataset con bypass de caché HTTP y sincronización Cloud
  const handleRefreshData = async () => {
    setIsRefreshing(true);
    try {
      const res = await fetch(`./data/public.json?t=${Date.now()}`, { cache: 'no-store' });
      if (res.ok) {
        const data: PublicPulseDataset = await res.json();
        setDataset(data);
      }
      if (currentUser) {
        await loadCloudIdeas();
      }
    } catch (e) {
      console.error('Error al refrescar datos:', e);
    } finally {
      setTimeout(() => setIsRefreshing(false), 500);
    }
  };

  // Abrir modal de nueva idea (con fecha o estado predeterminado opcional)
  const openNewIdeaModal = (defaultDate?: string, defaultStatus: AssetStatus = 'idea') => {
    setEditingIdeaId(null);
    setIdeaTitle('');
    setIdeaType('post');
    setIdeaCategory('Inteligencia Artificial');
    setIdeaDate(defaultDate || '');
    setIdeaBrief('');
    setIdeaStatus(defaultStatus);
    setIdeaSuccessMsg('');
    setIsIdeaModalOpen(true);
  };

  // Abrir modal de edición para una idea local o de Cloud
  const openEditIdeaModal = (asset: ContentAsset) => {
    setEditingIdeaId(asset.id);
    setIdeaTitle(asset.title_es || asset.title_en || '');
    setIdeaType(asset.asset_type);
    setIdeaCategory(asset.category || 'Inteligencia Artificial');
    setIdeaDate(asset.publish_date || '');
    setIdeaBrief(asset.brief_es || asset.brief_en || '');
    setIdeaStatus(asset.status);
    setIdeaSuccessMsg('');
    setSelectedAssetForModal(null);
    setIsIdeaModalOpen(true);
  };

  // Guardar nueva idea o actualizar idea existente (Cloud en Supabase o Local en localStorage)
  const handleSaveIdea = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!ideaTitle.trim()) return;

    if (currentUser) {
      // Modo Pro / Cloud: sincronización directa con Supabase
      if (editingIdeaId) {
        const isCloud = cloudIdeas.some((c) => c.id === editingIdeaId);
        if (isCloud) {
          const updated = await updateUserIdea(editingIdeaId, {
            title: ideaTitle.trim(),
            category: ideaCategory || 'General',
            status: ideaStatus,
            target_date: ideaDate || null,
            notes: ideaBrief.trim() || ''
          });
          if (updated) {
            setCloudIdeas((prev) =>
              prev.map((item) =>
                item.id === editingIdeaId
                  ? {
                      ...item,
                      title_es: ideaTitle.trim(),
                      title_en: ideaTitle.trim(),
                      asset_type: ideaType,
                      status: ideaStatus,
                      category: ideaCategory || 'General',
                      categories: [ideaCategory || 'General'],
                      publish_date: ideaDate || null,
                      brief_es: ideaBrief.trim() || null
                    }
                  : item
              )
            );
            setIdeaSuccessMsg(t.idea_updated_success);
          }
        } else {
          // Idea local en modo autenticado
          setLocalIdeas((prev) =>
            prev.map((item) =>
              item.id === editingIdeaId
                ? {
                    ...item,
                    title_es: ideaTitle.trim(),
                    title_en: ideaTitle.trim(),
                    asset_type: ideaType,
                    status: ideaStatus,
                    category: ideaCategory || 'General',
                    categories: [ideaCategory || 'General'],
                    publish_date: ideaDate || null,
                    brief_es: ideaBrief.trim() || null
                  }
                : item
            )
          );
          setIdeaSuccessMsg(t.idea_updated_success);
        }
      } else {
        // Inserción de nueva idea en Supabase Cloud
        const created = await insertUserIdea({
          title: ideaTitle.trim(),
          category: ideaCategory || 'General',
          status: ideaStatus,
          target_date: ideaDate || null,
          notes: ideaBrief.trim() || ''
        });
        if (created) {
          const newCloudAsset: ContentAsset = {
            id: created.id,
            slug: `cloud-idea-${created.id.slice(0, 8)}`,
            asset_type: ideaType,
            status: ideaStatus,
            visibility: 'private',
            title_es: created.title,
            title_en: created.title,
            category: created.category || 'General',
            categories: [created.category || 'General'],
            tags: ['idea', 'cloud'],
            publish_date: created.target_date || null,
            brief_es: created.notes || null,
            language_parity: 'complete',
            word_count_es: 0,
            word_count_en: 0,
            reading_time_min: 0,
            seo_audit: {
              score_0_100: 70,
              title_ok: true,
              description_ok: Boolean(created.notes),
              parity_ok: true,
              taxonomy_ok: true,
              internal_links_ok: false,
              issues: ['Idea sincronizada en Supabase PostgreSQL']
            },
            freshness_status: 'fresh',
            owner: currentUser.id,
            social_channels: [],
            is_cloud_idea: true
          };
          setCloudIdeas((prev) => [newCloudAsset, ...prev]);
          setIdeaSuccessMsg(t.idea_saved_success);
        }
      }
    } else {
      // Modo Sandbox Offline (localStorage)
      if (editingIdeaId) {
        setLocalIdeas((prev) =>
          prev.map((item) => {
            if (item.id === editingIdeaId) {
              return {
                ...item,
                title_es: ideaTitle.trim(),
                title_en: ideaTitle.trim(),
                asset_type: ideaType,
                status: ideaStatus,
                category: ideaCategory || 'General',
                categories: [ideaCategory || 'General'],
                publish_date: ideaDate || null,
                brief_es: ideaBrief.trim() || null
              };
            }
            return item;
          })
        );
        setIdeaSuccessMsg(t.idea_updated_success);
      } else {
        const newIdea: ContentAsset = {
          id: `local-idea-${Date.now()}`,
          slug: `idea-${ideaTitle.toLowerCase().replace(/[^a-z0-9]+/g, '-').slice(0, 40)}`,
          asset_type: ideaType,
          status: ideaStatus,
          visibility: 'private',
          title_es: ideaTitle.trim(),
          title_en: ideaTitle.trim(),
          category: ideaCategory || 'General',
          categories: [ideaCategory || 'General'],
          tags: ['idea', 'backlog'],
          publish_date: ideaDate || null,
          brief_es: ideaBrief.trim() || null,
          language_parity: 'missing_en',
          word_count_es: 0,
          word_count_en: 0,
          reading_time_min: 0,
          seo_audit: {
            score_0_100: 50,
            title_ok: true,
            description_ok: false,
            parity_ok: false,
            taxonomy_ok: true,
            internal_links_ok: false,
            issues: ['Idea local pendiente de redacción de borrador']
          },
          freshness_status: 'fresh',
          owner: 'Daniel Alaez',
          social_channels: [],
          is_local_idea: true
        };

        setLocalIdeas((prev) => [newIdea, ...prev]);
        setIdeaSuccessMsg(t.idea_saved_success);
      }
    }

    setTimeout(() => {
      setIsIdeaModalOpen(false);
      setIdeaSuccessMsg('');
      setEditingIdeaId(null);
    }, 800);
  };

  // Eliminar idea (Cloud o Local)
  const handleDeleteLocalIdea = async (id: string) => {
    if (window.confirm(t.confirm_delete_idea)) {
      const isCloud = cloudIdeas.some((c) => c.id === id);
      if (isCloud && currentUser) {
        const ok = await deleteUserIdea(id);
        if (ok) {
          setCloudIdeas((prev) => prev.filter((item) => item.id !== id));
        }
      } else {
        setLocalIdeas((prev) => prev.filter((item) => item.id !== id));
      }
      if (selectedAssetForModal?.id === id) {
        setSelectedAssetForModal(null);
      }
    }
  };

  // Handlers de Autenticación Supabase Pro / Demo
  const handleDemoLogin = async () => {
    setAuthLoading(true);
    setAuthError('');
    const { user, error } = await signInWithDemo();
    setAuthLoading(false);
    if (error) {
      setAuthError(error.message);
    } else if (user) {
      setCurrentUser(user);
      setAuthSuccessMsg(t.auth_success);
      setTimeout(() => {
        setIsAuthModalOpen(false);
        setAuthSuccessMsg('');
      }, 1000);
    }
  };

  const handlePasswordLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!authEmail || !authPassword) return;
    setAuthLoading(true);
    setAuthError('');
    try {
      const { data, error } = await supabase.auth.signInWithPassword({
        email: authEmail,
        password: authPassword,
      });
      setAuthLoading(false);
      if (error) {
        setAuthError(error.message);
      } else if (data.user) {
        setCurrentUser(data.user);
        setAuthSuccessMsg(t.auth_success);
        setTimeout(() => {
          setIsAuthModalOpen(false);
          setAuthSuccessMsg('');
        }, 1000);
      }
    } catch (err: unknown) {
      setAuthLoading(false);
      setAuthError(err instanceof Error ? err.message : String(err));
    }
  };

  const handleSignUp = async () => {
    if (!authEmail || !authPassword) return;
    setAuthLoading(true);
    setAuthError('');
    try {
      const { data, error } = await supabase.auth.signUp({
        email: authEmail,
        password: authPassword,
      });
      setAuthLoading(false);
      if (error) {
        setAuthError(error.message);
      } else if (data.user) {
        setCurrentUser(data.user);
        setAuthSuccessMsg('¡Cuenta creada y sesión iniciada!');
        setTimeout(() => {
          setIsAuthModalOpen(false);
          setAuthSuccessMsg('');
        }, 1000);
      }
    } catch (err: unknown) {
      setAuthLoading(false);
      setAuthError(err instanceof Error ? err.message : String(err));
    }
  };

  const handleLogout = async () => {
    await supabaseSignOut();
    setCurrentUser(null);
    setCloudIdeas([]);
  };

  // Exportar ideas a YAML compatible con data/editorial/backlog.yaml
  const handleExportIdeasYaml = () => {
    const ideasToExport = currentUser ? (cloudIdeas.length > 0 ? cloudIdeas : localIdeas) : localIdeas;
    if (ideasToExport.length === 0) return;

    let yaml = '# Backlog de Ideas y Propuestas Editoriales\n# Generado desde Datalaria Pulse\nitems:\n';
    ideasToExport.forEach((item) => {
      yaml += `  - id: "${item.id}"\n`;
      yaml += `    title_es: "${(item.title_es || '').replace(/"/g, '\\"')}"\n`;
      yaml += `    type: "${item.asset_type}"\n`;
      yaml += `    status: "${item.status}"\n`;
      yaml += `    category: "${item.category}"\n`;
      if (item.publish_date) yaml += `    target_date: "${item.publish_date}"\n`;
      if (item.brief_es) yaml += `    brief: "${item.brief_es.replace(/"/g, '\\"')}"\n`;
      yaml += `    visibility: "private"\n\n`;
    });

    const blob = new Blob([yaml], { type: 'text/yaml;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    const filename = `backlog_${currentUser?.email?.split('@')[0] || 'ideas'}.yaml`;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  // Filtrado reactivo de activos
  const filteredAssets = useMemo(() => {
    return currentAssets.filter((a) => {
      // Búsqueda
      const q = search.toLowerCase();
      const matchSearch =
        !q ||
        (a.title_es && a.title_es.toLowerCase().includes(q)) ||
        (a.title_en && a.title_en.toLowerCase().includes(q)) ||
        a.id.toLowerCase().includes(q) ||
        a.category.toLowerCase().includes(q) ||
        a.tags.some((tag) => tag.toLowerCase().includes(q));

      // Tipo
      const matchType =
        typeFilter === 'all' ||
        (typeFilter === 'kit'
          ? a.asset_type === 'kit' || a.asset_type === 'suite' || a.asset_type === 'mega_bundle'
          : a.asset_type === typeFilter);

      // Estado
      const matchStatus = statusFilter === 'all' || a.status === statusFilter;

      return matchSearch && matchType && matchStatus;
    });
  }, [currentAssets, search, typeFilter, statusFilter]);

  // Ordenación de la tabla
  const sortedAssets = useMemo(() => {
    return [...filteredAssets].sort((a, b) => {
      let valA: string | number = '';
      let valB: string | number = '';

      switch (sortField) {
        case 'title':
          valA = (lang === 'es' ? a.title_es : a.title_en) || a.id;
          valB = (lang === 'es' ? b.title_es : b.title_en) || b.id;
          break;
        case 'type':
          valA = a.asset_type;
          valB = b.asset_type;
          break;
        case 'status':
          valA = a.status;
          valB = b.status;
          break;
        case 'publish_date':
          valA = a.publish_date || '0000-00-00';
          valB = b.publish_date || '0000-00-00';
          break;
        case 'word_count':
          valA = lang === 'es' ? a.word_count_es : a.word_count_en;
          valB = lang === 'es' ? b.word_count_es : b.word_count_en;
          break;
        case 'language_parity':
          valA = a.language_parity;
          valB = b.language_parity;
          break;
        case 'seo_score':
          valA = a.seo_audit?.score_0_100 ?? 0;
          valB = b.seo_audit?.score_0_100 ?? 0;
          break;
        case 'traffic_index':
          valA = a.metrics_relative?.index_100 ?? -1;
          valB = b.metrics_relative?.index_100 ?? -1;
          break;
        case 'rank_pct':
          valA = a.metrics_relative?.rank_pct ?? -1;
          valB = b.metrics_relative?.rank_pct ?? -1;
          break;
      }

      if (typeof valA === 'string') {
        const cmp = (valA as string).localeCompare(valB as string);
        return sortOrder === 'asc' ? cmp : -cmp;
      } else {
        const numA = Number(valA);
        const numB = Number(valB);
        return sortOrder === 'asc' ? numA - numB : numB - numA;
      }
    });
  }, [filteredAssets, sortField, sortOrder, lang]);

  // Paginación
  const totalPages = Math.max(1, Math.ceil(sortedAssets.length / pageSize));
  const pagedAssets = useMemo(() => {
    const start = (currentPage - 1) * pageSize;
    return sortedAssets.slice(start, start + pageSize);
  }, [sortedAssets, currentPage, pageSize]);

  const handleSortToggle = (field: SortField) => {
    if (sortField === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      // Por defecto descendente para números/fechas, ascendente para texto
      setSortOrder(field === 'title' || field === 'type' || field === 'status' ? 'asc' : 'desc');
    }
  };

  // KPIs agregados
  const totalWords = useMemo(() => {
    return currentAssets.reduce((acc, a) => acc + (lang === 'es' ? a.word_count_es : a.word_count_en), 0);
  }, [currentAssets, lang]);

  const avgWordsPerPost = useMemo(() => {
    const posts = currentAssets.filter((a) => a.asset_type === 'post');
    if (posts.length === 0) return 0;
    const postWords = posts.reduce((acc, a) => acc + (lang === 'es' ? a.word_count_es : a.word_count_en), 0);
    return Math.round(postWords / posts.length);
  }, [currentAssets, lang]);

  const avgSeoScore = useMemo(() => {
    if (currentAssets.length === 0) return 0;
    const sum = currentAssets.reduce((acc, a) => acc + (a.seo_audit?.score_0_100 ?? 0), 0);
    return Math.round(sum / currentAssets.length);
  }, [currentAssets]);

  const topTrafficAsset = useMemo(() => {
    const published = currentAssets.filter((a) => a.metrics_relative);
    if (published.length === 0) return null;
    return [...published].sort(
      (a, b) => (b.metrics_relative?.index_100 ?? 0) - (a.metrics_relative?.index_100 ?? 0)
    )[0];
  }, [currentAssets]);

  // Conteo por tipología
  const countsByType = useMemo(() => {
    const posts = currentAssets.filter((a) => a.asset_type === 'post').length;
    const apps = currentAssets.filter((a) => a.asset_type === 'app').length;
    const kits = currentAssets.filter(
      (a) => a.asset_type === 'kit' || a.asset_type === 'suite' || a.asset_type === 'mega_bundle'
    ).length;
    return { posts, apps, kits, total: currentAssets.length };
  }, [currentAssets]);

  // 1. Grupos del Ecosistema Web (Artículos, Kits, Apps)
  const ecosystemGroups = useMemo(() => {
    return [
      { key: t.type_posts, count: countsByType.posts, color: '#06b6d4', icon: '📝' },
      { key: t.type_kits, count: countsByType.kits, color: '#8b5cf6', icon: '📦' },
      { key: t.type_apps, count: countsByType.apps, color: '#10b981', icon: '⚡' }
    ];
  }, [countsByType, t]);

  // 2. Las 4 Temáticas Troncales del Blog Oficial (según datalaria.com)
  const blogThemes = useMemo(() => {
    const counts = {
      tecnicos: 0,
      proyectos: 0,
      startups: 0,
      biografias: 0
    };

    currentAssets.forEach((a) => {
      const c = (a.category || '').toLowerCase();
      if (c.includes('téc') || c.includes('tec') || c.includes('software') || c.includes('operativo') || c.includes('estrategia') || c.includes('finanzas')) {
        counts.tecnicos += 1;
      } else if (c.includes('proyect')) {
        counts.proyectos += 1;
      } else if (c.includes('startup') || c.includes('casos') || c.includes('éxito')) {
        counts.startups += 1;
      } else if (c.includes('biograf')) {
        counts.biografias += 1;
      } else if (a.asset_type === 'post') {
        counts.tecnicos += 1;
      }
    });

    return [
      { key: '🧠 Artículos Técnicos', count: counts.tecnicos, color: '#06b6d4' },
      { key: '🛠️ Proyectos Tech', count: counts.proyectos, color: '#10b981' },
      { key: '🚀 Startups & Casos', count: counts.startups, color: '#8b5cf6' },
      { key: '🏛️ Biografías', count: counts.biografias, color: '#f59e0b' }
    ];
  }, [currentAssets]);

  // 3. Taxonomía Temática Detallada (12 principales categorías)
  const detailedCategories = useMemo(() => {
    const map = new Map<string, number>();
    currentAssets.forEach((a) => {
      const list = a.categories && a.categories.length > 0 ? a.categories : [a.category || 'General'];
      list.forEach((cat) => {
        let label = cat;
        if (label === 'casos_exito') label = 'Casos de Éxito';
        if (label === 'IA') label = 'Inteligencia Artificial';
        map.set(label, (map.get(label) || 0) + 1);
      });
    });
    return Array.from(map.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10);
  }, [currentAssets]);

  // 4. Profundidad Editorial & Tiempo de Lectura (Nuevo Gráfico de Valor)
  const editorialDepth = useMemo(() => {
    const posts = currentAssets.filter((a) => a.asset_type === 'post');
    const master = posts.filter((p) => (lang === 'es' ? p.word_count_es : p.word_count_en) >= 4000).length;
    const deep = posts.filter((p) => {
      const w = lang === 'es' ? p.word_count_es : p.word_count_en;
      return w >= 2500 && w < 4000;
    }).length;
    const standard = posts.filter((p) => {
      const w = lang === 'es' ? p.word_count_es : p.word_count_en;
      return w >= 1500 && w < 2500;
    }).length;
    const brief = posts.filter((p) => {
      const w = lang === 'es' ? p.word_count_es : p.word_count_en;
      return w < 1500;
    }).length;

    const totalHours = Math.round(
      posts.reduce((acc, p) => acc + (p.reading_time_min || 0), 0) / 60
    );

    return { master, deep, standard, brief, total: posts.length, totalHours };
  }, [currentAssets, lang]);

  // Segmentación por cuartiles de tráfico
  const trafficTiers = useMemo(() => {
    const withTraffic = currentAssets.filter((a) => a.metrics_relative);
    const top = withTraffic.filter((a) => (a.metrics_relative?.index_100 ?? 0) >= 300).length;
    const high = withTraffic.filter((a) => {
      const idx = a.metrics_relative?.index_100 ?? 0;
      return idx >= 150 && idx < 300;
    }).length;
    const medium = withTraffic.filter((a) => {
      const idx = a.metrics_relative?.index_100 ?? 0;
      return idx >= 75 && idx < 150;
    }).length;
    const baseline = withTraffic.filter((a) => (a.metrics_relative?.index_100 ?? 0) < 75).length;
    return { top, high, medium, baseline, total: withTraffic.length };
  }, [currentAssets]);

  // Cadencia histórica por año
  const cadenceByYear = useMemo(() => {
    const map = new Map<string, number>();
    currentAssets.forEach((a) => {
      if (a.publish_date) {
        const year = a.publish_date.split('-')[0];
        if (year && year.length === 4) {
          map.set(year, (map.get(year) || 0) + 1);
        }
      }
    });
    return Array.from(map.entries()).sort((a, b) => a[0].localeCompare(b[0]));
  }, [currentAssets]);

  // Cadencia histórica por mes (últimos 14 meses con publicados y programados)
  const cadenceByMonth = useMemo(() => {
    const map = new Map<string, { published: number; scheduled: number }>();
    currentAssets.forEach((a) => {
      if (a.publish_date && a.publish_date.length >= 7) {
        const ym = a.publish_date.substring(0, 7);
        const cur = map.get(ym) || { published: 0, scheduled: 0 };
        if (a.status === 'published') cur.published += 1;
        else if (a.status === 'scheduled') cur.scheduled += 1;
        map.set(ym, cur);
      }
    });
    const monthAbbr: Record<string, string> = {
      '01': 'Ene', '02': 'Feb', '03': 'Mar', '04': 'Abr', '05': 'May', '06': 'Jun',
      '07': 'Jul', '08': 'Ago', '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dic'
    };
    return Array.from(map.entries())
      .sort((a, b) => a[0].localeCompare(b[0]))
      .slice(-14)
      .map(([ym, data]) => {
        const parts = ym.split('-');
        const label = `${monthAbbr[parts[1]] || parts[1]} '${parts[0].slice(2)}`;
        return { ym, label, ...data, total: data.published + data.scheduled };
      });
  }, [currentAssets]);

  // Serie temporal mensual real desde GA4 (relativizada en base 100)
  const monthlyGa4Trend = dataset?.monthly_traffic_index || [];

  // Valor de Reemplazo Editorial ($0.10 / palabra técnica)
  const contentEquityUSD = useMemo(() => {
    return Math.round(totalWords * 0.1);
  }, [totalWords]);

  // Matriz de Oportunidades (Salud & ROI)
  const healthMatrix = useMemo(() => {
    // 1. Joyas SEO Ocultas: Score >= 80, Tráfico medio o bajo (< 150)
    const gems = currentAssets.filter(
      (a) =>
        a.status === 'published' &&
        (a.seo_audit?.score_0_100 ?? 0) >= 80 &&
        (a.metrics_relative?.index_100 ?? 0) < 150
    );

    // 2. Motores de Tráfico: Percentil >= 80%
    const cashCows = currentAssets.filter(
      (a) => a.status === 'published' && (a.metrics_relative?.rank_pct ?? 0) >= 80
    );

    // 3. Candidatos a Refresh: Publicados antes de mediados de 2026 con tráfico bajo (< mediana 100)
    const decay = currentAssets.filter((a) => {
      if (a.status !== 'published' || !a.publish_date) return false;
      return a.publish_date < '2026-06-01' && (a.metrics_relative?.index_100 ?? 0) < 100;
    });

    // 4. Brecha de Monetización: Posts publicados sin app ni kit relacionado
    const monetizationGap = currentAssets.filter(
      (a) => a.asset_type === 'post' && a.status === 'published' && !a.related_app && !a.related_kit
    );

    return { gems, cashCows, decay, monetizationGap };
  }, [currentAssets]);

  // Calendario mensual: funciones de navegación
  const handlePrevMonth = () => {
    setCalendarDate(new Date(calendarDate.getFullYear(), calendarDate.getMonth() - 1, 1));
  };

  const handleNextMonth = () => {
    setCalendarDate(new Date(calendarDate.getFullYear(), calendarDate.getMonth() + 1, 1));
  };

  const handleToday = () => {
    // Si la referencia del blog es 2026-10-28, fijar en octubre/noviembre 2026
    setCalendarDate(new Date(2026, 10, 1));
  };

  // Generador de celdas del mes
  const calendarGrid = useMemo(() => {
    const year = calendarDate.getFullYear();
    const month = calendarDate.getMonth();

    const firstDayOfMonth = new Date(year, month, 1);
    const lastDayOfMonth = new Date(year, month + 1, 0);

    // Día de inicio (Lunes = 0, Domingo = 6)
    let startDay = firstDayOfMonth.getDay() - 1;
    if (startDay === -1) startDay = 6;

    const daysInMonth = lastDayOfMonth.getDate();
    const prevMonthLastDay = new Date(year, month, 0).getDate();

    const cells: { day: number; isCurrentMonth: boolean; dateStr: string }[] = [];

    // Días del mes previo
    for (let i = startDay - 1; i >= 0; i--) {
      const d = prevMonthLastDay - i;
      const prevDate = new Date(year, month - 1, d);
      const str = `${prevDate.getFullYear()}-${String(prevDate.getMonth() + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
      cells.push({ day: d, isCurrentMonth: false, dateStr: str });
    }

    // Días del mes actual
    for (let d = 1; d <= daysInMonth; d++) {
      const str = `${year}-${String(month + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
      cells.push({ day: d, isCurrentMonth: true, dateStr: str });
    }

    // Relleno mes siguiente hasta completar múltiplos de 7 (35 o 42 celdas)
    const remaining = (7 - (cells.length % 7)) % 7;
    for (let d = 1; d <= remaining; d++) {
      const nextDate = new Date(year, month + 1, d);
      const str = `${nextDate.getFullYear()}-${String(nextDate.getMonth() + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
      cells.push({ day: d, isCurrentMonth: false, dateStr: str });
    }

    return cells;
  }, [calendarDate]);

  // Mapa de eventos por fecha para el calendario (respeta filtros de búsqueda, tipo y estado)
  const calendarEventsMap = useMemo(() => {
    const map = new Map<string, ContentAsset[]>();
    filteredAssets.forEach((a) => {
      if (a.publish_date) {
        const dateKey = a.publish_date.slice(0, 10);
        const arr = map.get(dateKey) || [];
        arr.push(a);
        map.set(dateKey, arr);
      }
    });
    return map;
  }, [filteredAssets]);

  // Render Sort Indicator Icon
  const renderSortIcon = (field: SortField) => {
    if (sortField !== field) {
      return <ArrowUpDown size={13} style={{ opacity: 0.35, marginLeft: '0.25rem' }} />;
    }
    return sortOrder === 'asc' ? (
      <ArrowUp size={13} style={{ color: '#10b981', marginLeft: '0.25rem' }} />
    ) : (
      <ArrowDown size={13} style={{ color: '#10b981', marginLeft: '0.25rem' }} />
    );
  };

  return (
    <div className="app-container">
      {/* HEADER */}
      <header className="pulse-header">
        <div className="header-inner">
          <div className="brand-section">
            <div className="brand-icon">
              <Activity size={24} />
            </div>
            <div>
              <div className="brand-title">Datalaria Pulse</div>
              <div className="brand-sub">{t.brand_subtitle}</div>
            </div>
          </div>

          <div className="header-actions">
            {/* Botón Refrescar Datos con bypass de caché */}
            <button
              className="btn btn-outline"
              onClick={handleRefreshData}
              disabled={isRefreshing}
              title={t.btn_refresh_data}
            >
              <RefreshCw size={15} className={isRefreshing ? 'spin-animation' : ''} />
              <span>{isRefreshing ? t.btn_refreshing : t.btn_refresh_data}</span>
            </button>

            {/* Botón Nueva Idea */}
            <button
              className="btn btn-outline"
              onClick={() => openNewIdeaModal()}
              style={{ borderColor: 'rgba(16, 185, 129, 0.4)', color: '#34d399' }}
              title={t.btn_new_idea}
            >
              <Plus size={16} />
              <span>{t.btn_new_idea}</span>
            </button>

            {/* Botón Exportar Ideas a YAML */}
            {((currentUser ? (cloudIdeas.length > 0 ? cloudIdeas : localIdeas) : localIdeas).length > 0) && (
              <button
                className="btn btn-ghost"
                onClick={handleExportIdeasYaml}
                title={t.btn_export_ideas}
                style={{ color: '#c084fc', border: '1px solid rgba(168, 85, 247, 0.3)' }}
              >
                <Download size={15} />
                <span>YAML ({(currentUser ? (cloudIdeas.length > 0 ? cloudIdeas : localIdeas) : localIdeas).length})</span>
              </button>
            )}

            <button
              className="btn btn-outline"
              onClick={() => setIsNotionModalOpen(true)}
              title={t.btn_import_notion}
            >
              <Upload size={16} />
              <span>{t.btn_import_notion}</span>
            </button>

            {customAssets && (
              <button className="btn btn-ghost" onClick={resetToDefault}>
                <RefreshCw size={15} />
                <span>{currentUser ? t.btn_back_to_my_data : t.btn_reset_dataset}</span>
              </button>
            )}

            {/* Botón / Píldora de Autenticación Supabase Pro Cloud (ADR-015) */}
            {currentUser ? (
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.45rem',
                  background: isAdmin
                    ? 'rgba(234, 179, 8, 0.12)'
                    : isDemo
                    ? 'rgba(6, 182, 212, 0.12)'
                    : 'rgba(16, 185, 129, 0.12)',
                  border: `1px solid ${
                    isAdmin
                      ? 'rgba(234, 179, 8, 0.35)'
                      : isDemo
                      ? 'rgba(6, 182, 212, 0.35)'
                      : 'rgba(16, 185, 129, 0.35)'
                  }`,
                  borderRadius: '9999px',
                  padding: '0.25rem 0.65rem'
                }}
                title={t.cloud_synced_msg}
              >
                <Cloud
                  size={14}
                  color={isAdmin ? '#facc15' : isDemo ? '#22d3ee' : '#34d399'}
                />
                <span style={{ fontSize: '0.8rem', fontWeight: 600, color: '#e0f2fe' }}>
                  {isAdmin
                    ? 'dalaez1 (Admin)'
                    : isDemo
                    ? t.badge_demo_user
                    : currentUser.email?.split('@')[0]}
                </span>
                <span
                  style={{
                    fontSize: '0.7rem',
                    padding: '0.1rem 0.35rem',
                    background: isAdmin
                      ? 'rgba(234, 179, 8, 0.2)'
                      : isDemo
                      ? 'rgba(6, 182, 212, 0.2)'
                      : 'rgba(16, 185, 129, 0.2)',
                    color: isAdmin ? '#facc15' : isDemo ? '#22d3ee' : '#34d399',
                    borderRadius: '4px',
                    fontWeight: 700
                  }}
                >
                  {isAdmin ? 'ADMIN' : isDemo ? 'DEMO' : 'PRO'}
                </span>
                <button
                  onClick={handleLogout}
                  className="btn btn-ghost"
                  style={{ padding: '0.15rem 0.3rem', minHeight: 'unset', height: 'auto', color: '#94a3b8' }}
                  title={t.btn_logout}
                >
                  <LogOut size={13} />
                </button>
              </div>
            ) : (
              <button
                className="btn btn-outline"
                onClick={() => setIsAuthModalOpen(true)}
                style={{ borderColor: 'rgba(6, 182, 212, 0.5)', color: '#22d3ee' }}
                title={t.btn_pro_login}
              >
                <Zap size={15} />
                <span>{t.btn_pro_login}</span>
              </button>
            )}

            <a
              href="https://datalaria.com/es/recursos/#pack-pulse"
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-primary"
            >
              <FileSpreadsheet size={16} />
              <span>{t.btn_get_kit}</span>
            </a>

            <button
              className="btn btn-ghost"
              onClick={() => setLang(lang === 'es' ? 'en' : 'es')}
              style={{ fontWeight: 700 }}
            >
              <Globe size={16} />
              <span>{lang.toUpperCase()}</span>
            </button>
          </div>
        </div>
      </header>

      {/* CONTENIDO PRINCIPAL */}
      <main className="main-content">
        {/* Banner Upsell Kit */}
        <div className="kit-cta-banner">
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
              <Sparkles size={18} color="#10b981" />
              <strong style={{ fontSize: '1.05rem', color: '#f9fafb', fontFamily: 'var(--font-heading)' }}>
                {t.kit_banner_title}
              </strong>
            </div>
            <p style={{ fontSize: '0.875rem', color: '#9ca3af', margin: 0 }}>
              {t.kit_banner_desc}
            </p>
          </div>
          <a
            href="https://datalaria.com/es/recursos/#pack-pulse"
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-primary"
          >
            {t.btn_get_kit}
          </a>
        </div>

        {/* Banner de Contexto de Espacio de Trabajo */}
        {!currentUser && (
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              background: 'rgba(15, 23, 42, 0.75)',
              border: '1px solid rgba(51, 65, 85, 0.6)',
              borderRadius: '8px',
              padding: '0.65rem 1rem',
              marginBottom: '1.25rem',
              fontSize: '0.85rem',
              color: '#94a3b8'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span style={{ fontSize: '1.1rem' }}>👁️</span>
              <span>{t.banner_public_showcase}</span>
            </div>
            <button
              className="btn btn-ghost"
              onClick={() => setIsAuthModalOpen(true)}
              style={{ color: '#22d3ee', fontSize: '0.8rem', padding: '0.2rem 0.5rem', whiteSpace: 'nowrap' }}
            >
              <Zap size={14} />
              <span>{t.btn_pro_login}</span>
            </button>
          </div>
        )}

        {isAdmin && (
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.6rem',
              background: 'rgba(234, 179, 8, 0.08)',
              border: '1px solid rgba(234, 179, 8, 0.25)',
              borderRadius: '8px',
              padding: '0.6rem 1rem',
              marginBottom: '1.25rem',
              fontSize: '0.82rem',
              color: '#fef08a'
            }}
          >
            <span style={{ fontSize: '1.1rem' }}>🛠️</span>
            <span>
              <strong>Modo Administrador Datalaria ({currentUser?.email}):</strong> Catálogo maestro de {datasetAssets?.length || 135} activos sincronizado con el repositorio Git + {cloudIdeas.length} ideas privadas en Supabase Cloud.
            </span>
          </div>
        )}

        {isDemo && (
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              background: 'rgba(6, 182, 212, 0.08)',
              border: '1px solid rgba(6, 182, 212, 0.25)',
              borderRadius: '8px',
              padding: '0.6rem 1rem',
              marginBottom: '1.25rem',
              fontSize: '0.82rem',
              color: '#a5f3fc'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Zap size={16} color="#22d3ee" />
              <span>
                <strong>Modo Demostración ({t.badge_demo_user}):</strong> Espacio interactivo con {currentAssets.length} activos sintéticos en Supabase Cloud. Prueba a crear, editar o mover ideas.
              </span>
            </div>
            <button
              className="btn btn-ghost"
              onClick={() => openNewIdeaModal()}
              style={{ color: '#22d3ee', fontSize: '0.78rem', padding: '0.2rem 0.5rem' }}
            >
              + {t.btn_new_idea}
            </button>
          </div>
        )}

        {isClientUser && currentAssets.length === 0 && (
          <div
            style={{
              background: 'rgba(15, 23, 42, 0.85)',
              border: '1px solid rgba(56, 189, 248, 0.2)',
              borderRadius: '12px',
              padding: '2.5rem 1.5rem',
              textAlign: 'center',
              marginBottom: '1.5rem'
            }}
          >
            <div style={{ fontSize: '2.5rem', marginBottom: '0.75rem' }}>🚀</div>
            <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#f8fafc', marginBottom: '0.5rem', fontFamily: 'var(--font-heading)' }}>
              {t.banner_client_empty_title}
            </h3>
            <p style={{ fontSize: '0.875rem', color: '#94a3b8', maxWidth: '640px', margin: '0 auto 1.5rem auto', lineHeight: 1.5 }}>
              {t.banner_client_empty_desc}
            </p>
            <div style={{ display: 'flex', justifyContent: 'center', gap: '0.75rem', flexWrap: 'wrap' }}>
              <button className="btn btn-primary" onClick={() => openNewIdeaModal()}>
                <Plus size={16} />
                <span>+ {t.btn_new_idea}</span>
              </button>
              <button className="btn btn-outline" onClick={() => setIsNotionModalOpen(true)}>
                <Upload size={16} />
                <span>{t.btn_import_notion}</span>
              </button>
              <button className="btn btn-outline" onClick={handleLoadSampleData}>
                <Sparkles size={16} />
                <span>{t.btn_load_sample_data}</span>
              </button>
            </div>
          </div>
        )}

        {isClientUser && currentAssets.length > 0 && (
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              background: 'rgba(16, 185, 129, 0.08)',
              border: '1px solid rgba(16, 185, 129, 0.25)',
              borderRadius: '8px',
              padding: '0.6rem 1rem',
              marginBottom: '1.25rem',
              fontSize: '0.82rem',
              color: '#a7f3d0'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Cloud size={16} color="#34d399" />
              <span>
                <strong>{t.badge_client_user} ({currentUser?.email}):</strong> {currentAssets.length} activos gestionados en tu base de datos privada Supabase.
              </span>
            </div>
            {customAssets ? (
              <button
                className="btn btn-ghost"
                onClick={resetToDefault}
                style={{ color: '#34d399', fontSize: '0.78rem', padding: '0.2rem 0.5rem' }}
              >
                <RefreshCw size={13} />
                <span>{t.btn_back_to_my_data}</span>
              </button>
            ) : (
              <button
                className="btn btn-ghost"
                onClick={() => openNewIdeaModal()}
                style={{ color: '#34d399', fontSize: '0.78rem', padding: '0.2rem 0.5rem' }}
              >
                + {t.btn_new_idea}
              </button>
            )}
          </div>
        )}

        {/* Encabezado de Sección: KPIs Generales Macro */}
        <div className="kpi-section-header">
          <div>
            <div className="kpi-section-title">
              <Layers size={18} color="#06b6d4" />
              <span>{t.kpi_macro_section_title}</span>
            </div>
            <div className="kpi-section-sub">{t.kpi_macro_section_sub}</div>
          </div>
        </div>

        {/* KPIs Principales (Macro Ecosistema) */}
        <div className="kpi-grid">
          <div className="kpi-card macro-total">
            <div className="kpi-label">
              <span style={{ display: 'flex', alignItems: 'center', gap: '0.45rem' }}>
                <span className="macro-tag-pill" style={{ background: 'rgba(6, 182, 212, 0.15)', color: '#22d3ee', border: '1px solid rgba(6, 182, 212, 0.35)' }}>
                  {t.badge_inventory}
                </span>
                <span>{t.stat_total_assets}</span>
              </span>
              <Layers size={18} color="#06b6d4" />
            </div>
            <div className="kpi-value">{currentAssets.length}</div>
            <div className="kpi-subtitle">
              {countsByType.posts} posts · {countsByType.apps} apps · {countsByType.kits} kits
            </div>
          </div>

          <div className="kpi-card macro-published">
            <div className="kpi-label">
              <span style={{ display: 'flex', alignItems: 'center', gap: '0.45rem' }}>
                <span className="macro-tag-pill" style={{ background: 'rgba(16, 185, 129, 0.15)', color: '#34d399', border: '1px solid rgba(16, 185, 129, 0.35)' }}>
                  {t.badge_live}
                </span>
                <span>{t.stat_published}</span>
              </span>
              <Award size={18} color="#10b981" />
            </div>
            <div className="kpi-value" style={{ color: '#10b981' }}>
              {currentAssets.filter((a) => a.status === 'published').length}
            </div>
            <div className="kpi-subtitle">
              {Math.round((currentAssets.filter((a) => a.status === 'published').length / (currentAssets.length || 1)) * 100)}% del total indexado
            </div>
          </div>

          <div className="kpi-card macro-scheduled">
            <div className="kpi-label">
              <span style={{ display: 'flex', alignItems: 'center', gap: '0.45rem' }}>
                <span className="macro-tag-pill" style={{ background: 'rgba(56, 189, 248, 0.15)', color: '#38bdf8', border: '1px solid rgba(56, 189, 248, 0.35)' }}>
                  {t.badge_roadmap}
                </span>
                <span>{t.stat_scheduled}</span>
              </span>
              <Clock size={18} color="#38bdf8" />
            </div>
            <div className="kpi-value" style={{ color: '#38bdf8' }}>
              {currentAssets.filter((a) => a.status === 'scheduled').length}
            </div>
            <div className="kpi-subtitle">
              Lanzamientos programados hasta Dic 2026
            </div>
          </div>

          <div className="kpi-card macro-parity">
            <div className="kpi-label">
              <span style={{ display: 'flex', alignItems: 'center', gap: '0.45rem' }}>
                <span className="macro-tag-pill" style={{ background: 'rgba(168, 85, 247, 0.15)', color: '#c084fc', border: '1px solid rgba(168, 85, 247, 0.35)' }}>
                  {t.badge_parity}
                </span>
                <span>{t.stat_parity}</span>
              </span>
              <Globe size={18} color="#a855f7" />
            </div>
            <div className="kpi-value" style={{ color: '#c084fc' }}>
              {currentAssets.filter((a) => a.language_parity === 'complete').length} / {currentAssets.length}
            </div>
            <div className="kpi-subtitle">
              100% Emparejamiento ES ⇔ EN determinista
            </div>
          </div>
        </div>

        {/* Barra de Navegación entre Vistas (Deck Segmentado) */}
        <div className="view-nav-wrapper">
          <div className="view-nav">
            <button
              className={`tab-btn ${activeTab === 'dashboard' ? 'active' : ''}`}
              onClick={() => setActiveTab('dashboard')}
            >
              <BarChart3 size={18} />
              <span>{t.view_dashboard}</span>
            </button>
            <button
              className={`tab-btn ${activeTab === 'table' ? 'active' : ''}`}
              onClick={() => setActiveTab('table')}
            >
              <TableIcon size={18} />
              <span>{t.view_table}</span>
            </button>
            <button
              className={`tab-btn ${activeTab === 'kanban' ? 'active' : ''}`}
              onClick={() => setActiveTab('kanban')}
            >
              <Columns3 size={18} />
              <span>{t.view_kanban}</span>
            </button>
            <button
              className={`tab-btn ${activeTab === 'calendar' ? 'active' : ''}`}
              onClick={() => setActiveTab('calendar')}
            >
              <CalendarIcon size={18} />
              <span>{t.view_calendar}</span>
            </button>
            <button
              className={`tab-btn ${activeTab === 'health' ? 'active' : ''}`}
              onClick={() => setActiveTab('health')}
            >
              <ShieldCheck size={18} />
              <span>{t.view_health}</span>
            </button>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <span style={{ fontSize: '0.78rem', color: '#64748b', fontWeight: 600, letterSpacing: '0.04em', textTransform: 'uppercase' }}>
              {activeTab === 'dashboard' && t.view_dashboard}
              {activeTab === 'table' && t.view_table}
              {activeTab === 'kanban' && t.view_kanban}
              {activeTab === 'calendar' && t.view_calendar}
              {activeTab === 'health' && t.view_health}
            </span>
            <span style={{ background: 'rgba(16, 185, 129, 0.12)', color: '#34d399', border: '1px solid rgba(16, 185, 129, 0.3)', borderRadius: '9999px', padding: '0.2rem 0.55rem', fontSize: '0.72rem', fontWeight: 700 }}>
              {currentAssets.length} activos
            </span>
          </div>
        </div>

        {/* Barra de Filtros Interactivos Tipo Píldora (Visible en Tabla, Kanban y Calendario) */}
        {(activeTab === 'table' || activeTab === 'kanban' || activeTab === 'calendar') && (
          <div className="controls-bar">
            <div className="controls-row-top">
              <div className="search-box">
                <Search size={16} className="search-icon" />
                <input
                  type="text"
                  className="search-input"
                  placeholder={t.search_placeholder}
                  value={search}
                  onChange={(e) => handleSearchChange(e.target.value)}
                />
              </div>

              {/* Botón rápido reset de filtros si hay alguno aplicado */}
              {(search || typeFilter !== 'all' || statusFilter !== 'all') && (
                <button
                  className="btn btn-ghost"
                  onClick={() => {
                    handleSearchChange('');
                    handleTypeChange('all');
                    handleStatusChange('all');
                  }}
                  style={{ fontSize: '0.78rem', padding: '0.4rem 0.75rem' }}
                >
                  <X size={14} />
                  <span>Limpiar Filtros</span>
                </button>
              )}
            </div>

            <div className="filter-pills-container">
              {/* Filtro Tipo de Activo */}
              <div className="filter-pill-block">
                <span className="filter-pill-label">{t.filter_type}:</span>
                <div className="pills-group">
                  <button
                    className={`pill-item ${typeFilter === 'all' ? 'active' : ''}`}
                    onClick={() => handleTypeChange('all')}
                  >
                    <span>{t.filter_all}</span>
                    <span className="pill-count">{currentAssets.length}</span>
                  </button>
                  <button
                    className={`pill-item ${typeFilter === 'post' ? 'active' : ''}`}
                    onClick={() => handleTypeChange('post')}
                  >
                    <span style={{ color: '#06b6d4' }}>📝</span>
                    <span>{t.type_posts}</span>
                    <span className="pill-count">{countsByType.posts}</span>
                  </button>
                  <button
                    className={`pill-item ${typeFilter === 'app' ? 'active' : ''}`}
                    onClick={() => handleTypeChange('app')}
                  >
                    <span style={{ color: '#10b981' }}>⚡</span>
                    <span>{t.type_apps}</span>
                    <span className="pill-count">{countsByType.apps}</span>
                  </button>
                  <button
                    className={`pill-item ${typeFilter === 'kit' ? 'active' : ''}`}
                    onClick={() => handleTypeChange('kit')}
                  >
                    <span style={{ color: '#8b5cf6' }}>📦</span>
                    <span>{t.type_kits}</span>
                    <span className="pill-count">{countsByType.kits}</span>
                  </button>
                </div>
              </div>

              {/* Filtro Estado */}
              <div className="filter-pill-block">
                <span className="filter-pill-label">{t.filter_status}:</span>
                <div className="pills-group">
                  <button
                    className={`pill-item ${statusFilter === 'all' ? 'active' : ''}`}
                    onClick={() => handleStatusChange('all')}
                  >
                    <span>{t.filter_all}</span>
                  </button>
                  <button
                    className={`pill-item ${statusFilter === 'published' ? 'active' : ''}`}
                    onClick={() => handleStatusChange('published')}
                  >
                    <span className="pill-dot" style={{ background: '#10b981' }} />
                    <span>{t.status_published}</span>
                    <span className="pill-count">
                      {currentAssets.filter((a) => a.status === 'published').length}
                    </span>
                  </button>
                  <button
                    className={`pill-item ${statusFilter === 'scheduled' ? 'active' : ''}`}
                    onClick={() => handleStatusChange('scheduled')}
                  >
                    <span className="pill-dot" style={{ background: '#06b6d4' }} />
                    <span>{t.status_scheduled}</span>
                    <span className="pill-count">
                      {currentAssets.filter((a) => a.status === 'scheduled').length}
                    </span>
                  </button>
                  <button
                    className={`pill-item ${statusFilter === 'draft' ? 'active' : ''}`}
                    onClick={() => handleStatusChange('draft')}
                  >
                    <span className="pill-dot" style={{ background: '#f59e0b' }} />
                    <span>{t.status_draft}</span>
                    <span className="pill-count">
                      {currentAssets.filter((a) => a.status === 'draft').length}
                    </span>
                  </button>
                  <button
                    className={`pill-item ${statusFilter === 'idea' ? 'active' : ''}`}
                    onClick={() => handleStatusChange('idea')}
                  >
                    <span className="pill-dot" style={{ background: '#8b5cf6' }} />
                    <span>{t.status_idea}</span>
                    <span className="pill-count">
                      {currentAssets.filter((a) => a.status === 'idea').length}
                    </span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* 1. VISTA DASHBOARD / ANALYTICS */}
        {activeTab === 'dashboard' && (
          <div className="analytics-wrapper">
            {/* Encabezado temático para KPIs Específicos de la Vista Analytics */}
            <div className="section-header-analytics">
              <div>
                <div className="section-header-title">
                  <BarChart3 size={18} color="#10b981" />
                  <span>{t.kpi_analytics_section_title}</span>
                </div>
                <div className="kpi-section-sub">{t.kpi_analytics_section_sub}</div>
              </div>
            </div>

            {/* Top Métricas Específicas de Rendimiento y SEO */}
            <div className="kpi-grid">
              <div className="kpi-card specific-card">
                <div className="kpi-label">
                  <span>{t.kpi_total_words}</span>
                  <div className="icon-box-badge" style={{ background: 'rgba(16, 185, 129, 0.12)', color: '#10b981' }}>
                    <FileSpreadsheet size={18} />
                  </div>
                </div>
                <div className="kpi-value">{totalWords.toLocaleString()}</div>
                <div className="kpi-subtitle">
                  {avgWordsPerPost.toLocaleString()} {t.kpi_avg_words}
                </div>
              </div>

              <div className="kpi-card specific-card">
                <div className="kpi-label">
                  <span>{t.kpi_avg_seo}</span>
                  <div className="icon-box-badge" style={{ background: 'rgba(6, 182, 212, 0.12)', color: '#06b6d4' }}>
                    <Target size={18} />
                  </div>
                </div>
                <div className="kpi-value" style={{ color: '#06b6d4' }}>
                  {avgSeoScore} <span style={{ fontSize: '1.1rem', color: '#6b7280' }}>/ 100</span>
                </div>
                <div className="kpi-subtitle">
                  {currentAssets.filter((a) => (a.seo_audit?.score_0_100 ?? 0) >= 80).length} activos con score excelente (≥80)
                </div>
              </div>

              <div className="kpi-card specific-card">
                <div className="kpi-label">
                  <span>{t.kpi_content_equity}</span>
                  <div className="icon-box-badge" style={{ background: 'rgba(16, 185, 129, 0.12)', color: '#10b981' }}>
                    <DollarSign size={18} />
                  </div>
                </div>
                <div className="kpi-value" style={{ color: '#10b981' }}>
                  ${contentEquityUSD.toLocaleString()}
                </div>
                <div className="kpi-subtitle">
                  Valor de reemplazo estimado @ $0.10/palabra
                </div>
              </div>

              <div className="kpi-card specific-card specific-featured">
                <div className="kpi-label">
                  <span style={{ display: 'flex', alignItems: 'center', gap: '0.45rem' }}>
                    <span style={{ fontSize: '0.62rem', fontWeight: 800, background: 'rgba(168, 85, 247, 0.2)', color: '#c084fc', border: '1px solid rgba(168, 85, 247, 0.4)', borderRadius: '4px', padding: '0.1rem 0.35rem' }}>
                      TOP GA4
                    </span>
                    <span>{t.kpi_top_performer}</span>
                  </span>
                  <div className="icon-box-badge" style={{ background: 'rgba(168, 85, 247, 0.15)', color: '#a855f7' }}>
                    <TrendingUp size={18} />
                  </div>
                </div>
                <div style={{ fontSize: '0.95rem', fontWeight: 700, color: '#f9fafb', marginTop: '0.4rem', lineHeight: 1.3 }}>
                  {topTrafficAsset ? (lang === 'es' ? topTrafficAsset.title_es : topTrafficAsset.title_en) : '—'}
                </div>
                <div className="kpi-subtitle" style={{ color: '#c084fc', fontWeight: 700 }}>
                  Índice {topTrafficAsset?.metrics_relative?.index_100} · Percentil 100%
                </div>
              </div>
            </div>

            {/* Grid de Gráficos y Distribuciones (Gráficos ampliados y apilados en ancho completo) */}
            <div className="analytics-charts-grid">
              
              {/* Gráfico 1: Clasificación de Contenidos (Selector de 3 Modos: Ecosistema / 4 Temáticas Web / Categorías) */}
              <div className="chart-card-full">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.75rem' }}>
                  <div className="chart-title">
                    <BarChart3 size={20} color="#10b981" />
                    <span>{t.section_top_categories}</span>
                  </div>
                  <div className="pills-group" style={{ padding: '0.2rem' }}>
                    <button
                      className={`pill-item ${categoryViewMode === 'ecosystem' ? 'active' : ''}`}
                      onClick={() => setCategoryViewMode('ecosystem')}
                    >
                      {t.view_mode_ecosystem}
                    </button>
                    <button
                      className={`pill-item ${categoryViewMode === 'themes' ? 'active' : ''}`}
                      onClick={() => setCategoryViewMode('themes')}
                    >
                      {t.view_mode_themes}
                    </button>
                    <button
                      className={`pill-item ${categoryViewMode === 'categories' ? 'active' : ''}`}
                      onClick={() => setCategoryViewMode('categories')}
                    >
                      {t.view_mode_categories}
                    </button>
                  </div>
                </div>

                <div className="chart-desc">
                  {categoryViewMode === 'ecosystem' &&
                    'Macro-distribución de activos de Datalaria: Artículos editoriales vs Suites descargables vs Aplicaciones interactivas.'}
                  {categoryViewMode === 'themes' &&
                    'Las 4 temáticas troncales de conocimiento del Blog oficial (como en datalaria.com): Artículos Técnicos, Proyectos Tech, Startups y Biografías.'}
                  {categoryViewMode === 'categories' &&
                    'Taxonomía temática detallada indexada en el repositorio (Inteligencia Artificial, Estrategia C-Level, Control Operativo, DevOps, Python, etc.).'}
                </div>

                <div className="progress-bar-container">
                  {categoryViewMode === 'ecosystem' &&
                    ecosystemGroups.map((g) => {
                      const pct = Math.round((g.count / currentAssets.length) * 100);
                      return (
                        <div key={g.key} className="progress-bar-row">
                          <div className="progress-bar-meta">
                            <span style={{ fontWeight: 600, color: '#f9fafb', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                              <span>{g.icon}</span>
                              <span>{g.key}</span>
                            </span>
                            <span style={{ color: '#9ca3af', fontFamily: 'var(--font-mono)', fontSize: '0.8rem' }}>
                              {g.count} activos ({pct}%)
                            </span>
                          </div>
                          <div className="progress-bar-track">
                            <div
                              className="progress-bar-fill"
                              style={{ width: `${pct}%`, background: g.color }}
                            />
                          </div>
                        </div>
                      );
                    })}

                  {categoryViewMode === 'themes' &&
                    blogThemes.map((th) => {
                      const totalPosts = countsByType.posts || 1;
                      const pct = Math.round((th.count / totalPosts) * 100);
                      return (
                        <div key={th.key} className="progress-bar-row">
                          <div className="progress-bar-meta">
                            <span style={{ fontWeight: 600, color: '#f9fafb' }}>{th.key}</span>
                            <span style={{ color: '#9ca3af', fontFamily: 'var(--font-mono)', fontSize: '0.8rem' }}>
                              {th.count} artículos ({pct}%)
                            </span>
                          </div>
                          <div className="progress-bar-track">
                            <div
                              className="progress-bar-fill"
                              style={{ width: `${pct}%`, background: th.color }}
                            />
                          </div>
                        </div>
                      );
                    })}

                  {categoryViewMode === 'categories' &&
                    detailedCategories.map(([cat, count]) => {
                      const pct = Math.round((count / currentAssets.length) * 100);
                      return (
                        <div key={cat} className="progress-bar-row">
                          <div className="progress-bar-meta">
                            <span style={{ fontWeight: 600, color: '#f9fafb' }}>{cat}</span>
                            <span style={{ color: '#9ca3af', fontFamily: 'var(--font-mono)', fontSize: '0.8rem' }}>
                              {count} activos ({pct}%)
                            </span>
                          </div>
                          <div className="progress-bar-track">
                            <div
                              className="progress-bar-fill"
                              style={{
                                width: `${pct}%`,
                                background: 'linear-gradient(90deg, #10b981 0%, #06b6d4 100%)'
                              }}
                            />
                          </div>
                        </div>
                      );
                    })}
                </div>
              </div>

              {/* Gráfico 2: Evolución de Tráfico Orgánico Mensual (GA4 — Base 100, Ancho Completo) */}
              <div className="chart-card-full">
                <div className="chart-title">
                  <TrendingUp size={20} color="#10b981" />
                  <span>{t.section_monthly_seo}</span>
                </div>
                <div className="chart-desc">
                  {t.section_monthly_seo_desc}
                </div>
                <div style={{ display: 'flex', alignItems: 'flex-end', gap: '0.75rem', height: '210px', paddingTop: '1.5rem', width: '100%', overflowX: 'auto' }}>
                  {monthlyGa4Trend.map((pt) => {
                    const maxIdx = Math.max(...monthlyGa4Trend.map((p) => p.index_100), 1);
                    const heightPct = Math.round((pt.index_100 / maxIdx) * 100);
                    const isPeak = pt.index_100 === maxIdx;
                    return (
                      <div
                        key={pt.month}
                        style={{
                          flex: 1,
                          minWidth: '40px',
                          display: 'flex',
                          flexDirection: 'column',
                          alignItems: 'center',
                          gap: '0.45rem',
                          height: '100%',
                          justifyContent: 'flex-end'
                        }}
                        title={`${pt.label}: Índice ${pt.index_100}`}
                      >
                        <span
                          style={{
                            fontFamily: 'var(--font-mono)',
                            fontSize: '0.78rem',
                            fontWeight: 700,
                            color: isPeak ? '#10b981' : '#06b6d4'
                          }}
                        >
                          {pt.index_100}
                        </span>
                        <div
                          style={{
                            width: '100%',
                            maxWidth: '46px',
                            height: `${Math.max(8, heightPct)}%`,
                            background: isPeak
                              ? 'linear-gradient(180deg, #10b981 0%, #059669 100%)'
                              : 'linear-gradient(180deg, #06b6d4 0%, #0284c7 100%)',
                            borderRadius: '5px 5px 0 0',
                            transition: 'height 0.4s ease',
                            boxShadow: isPeak ? '0 0 16px rgba(16, 185, 129, 0.45)' : 'none'
                          }}
                        />
                        <span style={{ fontSize: '0.72rem', color: '#9ca3af', fontWeight: 600, whiteSpace: 'nowrap' }}>
                          {pt.label}
                        </span>
                      </div>
                    );
                  })}
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: '#6b7280', borderTop: '1px solid var(--border-color)', paddingTop: '0.75rem' }}>
                  <span>Mediana histórica del portal = 100</span>
                  <span style={{ color: '#10b981', fontWeight: 700 }}>Último mes: Índice 481 (+381% vs mediana histórica)</span>
                </div>
              </div>

              {/* Gráfico 3: Cadencia Histórica de Lanzamientos (Ancho Completo) */}
              <div className="chart-card-full">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.75rem' }}>
                  <div className="chart-title">
                    <Clock size={20} color="#8b5cf6" />
                    <span>{t.section_publication_cadence}</span>
                  </div>
                  <div className="pills-group" style={{ padding: '0.2rem' }}>
                    <button
                      className={`pill-item ${cadenceMode === 'monthly' ? 'active' : ''}`}
                      onClick={() => setCadenceMode('monthly')}
                    >
                      {t.cadence_view_monthly}
                    </button>
                    <button
                      className={`pill-item ${cadenceMode === 'yearly' ? 'active' : ''}`}
                      onClick={() => setCadenceMode('yearly')}
                    >
                      {t.cadence_view_yearly}
                    </button>
                  </div>
                </div>

                <div className="chart-desc">
                  {cadenceMode === 'monthly'
                    ? 'Distribución mensual de entregas editoriales (verde: publicados en producción, azul: programados a futuro).'
                    : 'Evolución anual acumulada de activos entregados en producción.'}
                </div>

                {cadenceMode === 'monthly' ? (
                  <div style={{ display: 'flex', alignItems: 'flex-end', gap: '0.75rem', height: '210px', paddingTop: '1.5rem', width: '100%', overflowX: 'auto' }}>
                    {cadenceByMonth.map((m) => {
                      const maxTotal = Math.max(...cadenceByMonth.map((x) => x.total), 1);
                      const heightPct = Math.round((m.total / maxTotal) * 100);
                      const isScheduledOnly = m.published === 0 && m.scheduled > 0;
                      return (
                        <div
                          key={m.ym}
                          style={{
                            flex: 1,
                            minWidth: '40px',
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                            gap: '0.45rem',
                            height: '100%',
                            justifyContent: 'flex-end'
                          }}
                          title={`${m.label}: ${m.published} publicados, ${m.scheduled} programados`}
                        >
                          <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', fontWeight: 700, color: isScheduledOnly ? '#06b6d4' : '#10b981' }}>
                            {m.total}
                          </span>
                          <div
                            style={{
                              width: '100%',
                              maxWidth: '46px',
                              height: `${Math.max(10, heightPct)}%`,
                              background: isScheduledOnly
                                ? 'linear-gradient(180deg, #06b6d4 0%, #0284c7 100%)'
                                : 'linear-gradient(180deg, #10b981 0%, #059669 100%)',
                              borderRadius: '5px 5px 0 0',
                              transition: 'height 0.4s ease'
                            }}
                          />
                          <span style={{ fontSize: '0.72rem', color: '#9ca3af', fontWeight: 600, whiteSpace: 'nowrap' }}>
                            {m.label}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                ) : (
                  <div style={{ display: 'flex', alignItems: 'flex-end', gap: '3rem', height: '210px', paddingTop: '1.5rem', justifyContent: 'center' }}>
                    {cadenceByYear.map(([year, count]) => {
                      const maxCount = Math.max(...cadenceByYear.map((c) => c[1]), 1);
                      const heightPct = Math.round((count / maxCount) * 100);
                      return (
                        <div
                          key={year}
                          style={{
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                            gap: '0.6rem',
                            height: '100%',
                            justifyContent: 'flex-end',
                            minWidth: '100px'
                          }}
                        >
                          <span style={{ fontFamily: 'var(--font-mono)', fontSize: '1.05rem', fontWeight: 800, color: '#10b981' }}>
                            {count} activos
                          </span>
                          <div
                            style={{
                              width: '80px',
                              height: `${Math.max(18, heightPct)}%`,
                              background: year === '2026' ? 'var(--grad-primary)' : 'rgba(255, 255, 255, 0.15)',
                              borderRadius: '8px 8px 0 0',
                              transition: 'height 0.4s ease'
                            }}
                          />
                          <span style={{ fontSize: '0.95rem', color: '#9ca3af', fontWeight: 700 }}>{year}</span>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>

              {/* Fila Dividida: Segmentación de Tráfico + Profundidad Editorial */}
              <div className="chart-cards-split">
                
                {/* 4A: Segmentación de Tráfico Orgánico */}
                <div className="chart-card">
                  <div className="chart-title">
                    <TrendingUp size={18} color="#06b6d4" />
                    <span>{t.section_traffic_tiers}</span>
                  </div>
                  <div className="chart-desc">
                    Distribución relativa de visitas de GA4 respecto a la mediana del sitio.
                  </div>
                  <div className="progress-bar-container">
                    <div className="progress-bar-row">
                      <div className="progress-bar-meta">
                        <span style={{ color: '#10b981', fontWeight: 600 }}>{t.tier_top}</span>
                        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', color: '#9ca3af' }}>
                          {trafficTiers.top} activos ({Math.round((trafficTiers.top / (trafficTiers.total || 1)) * 100)}%)
                        </span>
                      </div>
                      <div className="progress-bar-track">
                        <div
                          className="progress-bar-fill"
                          style={{
                            width: `${(trafficTiers.top / (trafficTiers.total || 1)) * 100}%`,
                            background: '#10b981'
                          }}
                        />
                      </div>
                    </div>

                    <div className="progress-bar-row">
                      <div className="progress-bar-meta">
                        <span style={{ color: '#06b6d4', fontWeight: 600 }}>{t.tier_high}</span>
                        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', color: '#9ca3af' }}>
                          {trafficTiers.high} activos ({Math.round((trafficTiers.high / (trafficTiers.total || 1)) * 100)}%)
                        </span>
                      </div>
                      <div className="progress-bar-track">
                        <div
                          className="progress-bar-fill"
                          style={{
                            width: `${(trafficTiers.high / (trafficTiers.total || 1)) * 100}%`,
                            background: '#06b6d4'
                          }}
                        />
                      </div>
                    </div>

                    <div className="progress-bar-row">
                      <div className="progress-bar-meta">
                        <span style={{ color: '#8b5cf6', fontWeight: 600 }}>{t.tier_medium}</span>
                        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', color: '#9ca3af' }}>
                          {trafficTiers.medium} activos ({Math.round((trafficTiers.medium / (trafficTiers.total || 1)) * 100)}%)
                        </span>
                      </div>
                      <div className="progress-bar-track">
                        <div
                          className="progress-bar-fill"
                          style={{
                            width: `${(trafficTiers.medium / (trafficTiers.total || 1)) * 100}%`,
                            background: '#8b5cf6'
                          }}
                        />
                      </div>
                    </div>

                    <div className="progress-bar-row">
                      <div className="progress-bar-meta">
                        <span style={{ color: '#6b7280', fontWeight: 600 }}>{t.tier_baseline}</span>
                        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', color: '#9ca3af' }}>
                          {trafficTiers.baseline} activos ({Math.round((trafficTiers.baseline / (trafficTiers.total || 1)) * 100)}%)
                        </span>
                      </div>
                      <div className="progress-bar-track">
                        <div
                          className="progress-bar-fill"
                          style={{
                            width: `${(trafficTiers.baseline / (trafficTiers.total || 1)) * 100}%`,
                            background: '#6b7280'
                          }}
                        />
                      </div>
                    </div>
                  </div>
                </div>

                {/* 4B: Profundidad Editorial & Tiempo de Lectura (Nuevo gráfico solicitado) */}
                <div className="chart-card">
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div className="chart-title">
                      <Zap size={18} color="#f59e0b" />
                      <span>{t.section_reading_depth}</span>
                    </div>
                    <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#f59e0b', background: 'rgba(245, 158, 11, 0.12)', padding: '0.2rem 0.6rem', borderRadius: '6px' }}>
                      ~{editorialDepth.totalHours}h lectura total
                    </span>
                  </div>
                  <div className="chart-desc">
                    {t.section_reading_depth_desc}
                  </div>
                  <div className="progress-bar-container">
                    <div className="progress-bar-row">
                      <div className="progress-bar-meta">
                        <span style={{ color: '#10b981', fontWeight: 600 }}>{t.depth_tier_master}</span>
                        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', color: '#9ca3af' }}>
                          {editorialDepth.master} ({Math.round((editorialDepth.master / (editorialDepth.total || 1)) * 100)}%)
                        </span>
                      </div>
                      <div className="progress-bar-track">
                        <div
                          className="progress-bar-fill"
                          style={{
                            width: `${(editorialDepth.master / (editorialDepth.total || 1)) * 100}%`,
                            background: '#10b981'
                          }}
                        />
                      </div>
                    </div>

                    <div className="progress-bar-row">
                      <div className="progress-bar-meta">
                        <span style={{ color: '#06b6d4', fontWeight: 600 }}>{t.depth_tier_deep}</span>
                        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', color: '#9ca3af' }}>
                          {editorialDepth.deep} ({Math.round((editorialDepth.deep / (editorialDepth.total || 1)) * 100)}%)
                        </span>
                      </div>
                      <div className="progress-bar-track">
                        <div
                          className="progress-bar-fill"
                          style={{
                            width: `${(editorialDepth.deep / (editorialDepth.total || 1)) * 100}%`,
                            background: '#06b6d4'
                          }}
                        />
                      </div>
                    </div>

                    <div className="progress-bar-row">
                      <div className="progress-bar-meta">
                        <span style={{ color: '#8b5cf6', fontWeight: 600 }}>{t.depth_tier_standard}</span>
                        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', color: '#9ca3af' }}>
                          {editorialDepth.standard} ({Math.round((editorialDepth.standard / (editorialDepth.total || 1)) * 100)}%)
                        </span>
                      </div>
                      <div className="progress-bar-track">
                        <div
                          className="progress-bar-fill"
                          style={{
                            width: `${(editorialDepth.standard / (editorialDepth.total || 1)) * 100}%`,
                            background: '#8b5cf6'
                          }}
                        />
                      </div>
                    </div>

                    <div className="progress-bar-row">
                      <div className="progress-bar-meta">
                        <span style={{ color: '#6b7280', fontWeight: 600 }}>{t.depth_tier_brief}</span>
                        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', color: '#9ca3af' }}>
                          {editorialDepth.brief} ({Math.round((editorialDepth.brief / (editorialDepth.total || 1)) * 100)}%)
                        </span>
                      </div>
                      <div className="progress-bar-track">
                        <div
                          className="progress-bar-fill"
                          style={{
                            width: `${(editorialDepth.brief / (editorialDepth.total || 1)) * 100}%`,
                            background: '#6b7280'
                          }}
                        />
                      </div>
                    </div>
                  </div>
                </div>

              </div>
            </div>
          </div>
        )}

        {/* 2. VISTA TABLA EJECUTIVA (Ordenable & Paginada) */}
        {activeTab === 'table' && (
          <div className="table-wrapper">
            <table className="pulse-table">
              <thead>
                <tr>
                  <th className="sortable" onClick={() => handleSortToggle('title')} title={t.sort_tooltip}>
                    {t.col_asset} {renderSortIcon('title')}
                  </th>
                  <th className="sortable" onClick={() => handleSortToggle('type')} title={t.sort_tooltip}>
                    {t.col_type} {renderSortIcon('type')}
                  </th>
                  <th className="sortable" onClick={() => handleSortToggle('status')} title={t.sort_tooltip}>
                    {t.col_status} {renderSortIcon('status')}
                  </th>
                  <th className="sortable" onClick={() => handleSortToggle('publish_date')} title={t.sort_tooltip}>
                    {t.col_date} {renderSortIcon('publish_date')}
                  </th>
                  <th className="sortable" onClick={() => handleSortToggle('word_count')} title={t.sort_tooltip}>
                    {t.col_words} {renderSortIcon('word_count')}
                  </th>
                  <th className="sortable" onClick={() => handleSortToggle('language_parity')} title={t.sort_tooltip}>
                    {t.col_parity} {renderSortIcon('language_parity')}
                  </th>
                  <th className="sortable" onClick={() => handleSortToggle('seo_score')} title={t.sort_tooltip}>
                    {t.col_seo} {renderSortIcon('seo_score')}
                  </th>
                  <th className="sortable" onClick={() => handleSortToggle('traffic_index')} title={t.sort_tooltip}>
                    {t.col_relative_index} {renderSortIcon('traffic_index')}
                  </th>
                  <th className="sortable" onClick={() => handleSortToggle('rank_pct')} title={t.sort_tooltip}>
                    {t.col_rank_pct} {renderSortIcon('rank_pct')}
                  </th>
                </tr>
              </thead>
              <tbody>
                {pagedAssets.length === 0 ? (
                  <tr>
                    <td colSpan={9} style={{ textAlign: 'center', padding: '3rem', color: '#9ca3af' }}>
                      {t.empty_results}
                    </td>
                  </tr>
                ) : (
                  pagedAssets.map((a) => {
                    const title = lang === 'es' ? a.title_es || a.title_en : a.title_en || a.title_es;
                    const url = lang === 'es' ? a.url_es || a.url_en : a.url_en || a.url_es;
                    const words = lang === 'es' ? a.word_count_es : a.word_count_en;
                    const seoScore = a.seo_audit?.score_0_100 ?? 0;
                    const rel = a.metrics_relative;

                    return (
                      <tr key={a.id}>
                        <td>
                          <div style={{ fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.4rem', flexWrap: 'wrap' }}>
                            {url ? (
                              <a
                                href={url}
                                target="_blank"
                                rel="noopener noreferrer"
                                style={{
                                  color: '#f9fafb',
                                  textDecoration: 'none',
                                  display: 'inline-flex',
                                  alignItems: 'center',
                                  gap: '0.4rem'
                                }}
                              >
                                {title || a.id}
                                <ExternalLink size={13} color="#06b6d4" />
                              </a>
                            ) : (
                              <span
                                onClick={() => setSelectedAssetForModal(a)}
                                style={{ cursor: 'pointer', color: '#f9fafb' }}
                                title={t.modal_preview_title}
                              >
                                {title || a.id}
                              </span>
                            )}
                            {a.is_cloud_idea && (
                              <span className="badge badge-cloud" style={{ background: 'rgba(6, 182, 212, 0.15)', color: '#22d3ee', border: '1px solid rgba(6, 182, 212, 0.4)', marginLeft: '0.35rem' }}>
                                ☁️ {t.badge_cloud_idea}
                              </span>
                            )}
                            {a.is_local_idea && (
                              <span className="badge badge-local">{t.badge_local_idea}</span>
                            )}
                          </div>
                          <div style={{ fontSize: '0.75rem', color: '#6b7280', marginTop: '0.2rem' }}>
                            {a.category} {a.series && `· Serie: ${a.series}`}
                          </div>
                        </td>
                        <td>
                          <span className={`badge badge-${a.asset_type}`}>
                            {a.asset_type.toUpperCase()}
                          </span>
                        </td>
                        <td>
                          <span className={`badge badge-${a.status}`}>
                            {a.status.toUpperCase()}
                          </span>
                        </td>
                        <td style={{ fontSize: '0.8125rem', color: '#9ca3af', whiteSpace: 'nowrap', fontFamily: 'var(--font-mono)' }}>
                          {a.publish_date || '—'}
                        </td>
                        <td style={{ fontSize: '0.8125rem', fontFamily: 'var(--font-mono)' }}>
                          {words > 0 ? `${words.toLocaleString()} pal.` : '—'}
                        </td>
                        <td>
                          <span
                            className={`badge ${
                              a.language_parity === 'complete'
                                ? 'badge-complete'
                                : a.language_parity.includes('outdated')
                                ? 'badge-warn'
                                : 'badge-alert'
                            }`}
                          >
                            {a.language_parity}
                          </span>
                        </td>
                        <td>
                          <span
                            className={`badge ${
                              seoScore >= 80 ? 'badge-complete' : seoScore >= 60 ? 'badge-warn' : 'badge-alert'
                            }`}
                          >
                            {seoScore} / 100
                          </span>
                        </td>
                        <td>
                          {rel ? (
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                              <TrendingUp size={14} color="#06b6d4" />
                              <strong style={{ color: '#06b6d4', fontFamily: 'var(--font-mono)' }}>{rel.index_100}</strong>
                            </div>
                          ) : (
                            '—'
                          )}
                        </td>
                        <td style={{ fontFamily: 'var(--font-mono)' }}>{rel ? `${rel.rank_pct}%` : '—'}</td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>

            {/* Barra de Paginación */}
            <div className="pagination-bar">
              <div>
                {t.showing_items
                  .replace('{from}', (sortedAssets.length === 0 ? 0 : (currentPage - 1) * pageSize + 1).toString())
                  .replace('{to}', Math.min(currentPage * pageSize, sortedAssets.length).toString())
                  .replace('{total}', sortedAssets.length.toString())}
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
                <div className="page-size-selector">
                  <span>{t.rows_per_page}</span>
                  {[10, 25, 50].map((size) => (
                    <button
                      key={size}
                      className={`page-size-btn ${pageSize === size ? 'active' : ''}`}
                      onClick={() => handlePageSizeChange(size)}
                    >
                      {size}
                    </button>
                  ))}
                </div>

                <div className="pagination-controls">
                  <button
                    className="page-btn"
                    disabled={currentPage === 1}
                    onClick={() => setCurrentPage(1)}
                    title={t.page_first}
                  >
                    «
                  </button>
                  <button
                    className="page-btn"
                    disabled={currentPage === 1}
                    onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
                    title={t.page_prev}
                  >
                    <ChevronLeft size={14} style={{ display: 'inline' }} />
                  </button>

                  <span style={{ padding: '0 0.5rem', fontWeight: 600 }}>
                    {currentPage} / {totalPages}
                  </span>

                  <button
                    className="page-btn"
                    disabled={currentPage >= totalPages}
                    onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
                    title={t.page_next}
                  >
                    <ChevronRight size={14} style={{ display: 'inline' }} />
                  </button>
                  <button
                    className="page-btn"
                    disabled={currentPage >= totalPages}
                    onClick={() => setCurrentPage(totalPages)}
                    title={t.page_last}
                  >
                    »
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* 3. VISTA TABLERO KANBAN (5 Columnas Horizontales con Filtro Temporal) */}
        {activeTab === 'kanban' && (
          <div className="kanban-wrapper">
            <div className="kanban-top-bar">
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <span style={{ fontSize: '0.85rem', color: '#9ca3af', fontWeight: 600 }}>Filtro de Horizonte:</span>
                <div className="pills-group">
                  <button
                    className={`pill-item ${kanbanTimeWindow === 'recent' ? 'active' : ''}`}
                    onClick={() => setKanbanTimeWindow('recent')}
                  >
                    <Clock size={14} />
                    <span>{t.kanban_filter_active}</span>
                  </button>
                  <button
                    className={`pill-item ${kanbanTimeWindow === 'all' ? 'active' : ''}`}
                    onClick={() => setKanbanTimeWindow('all')}
                  >
                    <Globe size={14} />
                    <span>{t.kanban_filter_all}</span>
                  </button>
                </div>
              </div>
            </div>

            <div className="kanban-board">
              {(['idea', 'draft', 'review', 'scheduled', 'published'] as const).map((colStatus) => {
                const allColAssets = filteredAssets.filter((a) => a.status === colStatus);

                // Aplicar filtro de ventana activa (último mes publicado o próximo mes programado)
                const visibleAssets =
                  kanbanTimeWindow === 'all'
                    ? allColAssets
                    : allColAssets.filter((a) => {
                        if (colStatus === 'published') {
                          // Último mes publicado (posteriores a 2026-09-15)
                          return !a.publish_date || a.publish_date >= '2026-09-15';
                        }
                        if (colStatus === 'scheduled') {
                          // Próximo mes programado (hasta 2026-11-30)
                          return !a.publish_date || a.publish_date <= '2026-11-30';
                        }
                        return true;
                      });

                return (
                  <div key={colStatus} className="kanban-column">
                    <div className="kanban-col-head">
                      <span className="kanban-col-title">
                        <span>{colStatus}</span>
                      </span>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                        {(colStatus === 'idea' || colStatus === 'draft') && (
                          <button
                            className="btn-icon-add"
                            onClick={() => openNewIdeaModal(undefined, colStatus)}
                            title={`+ Añadir ${colStatus}`}
                          >
                            +
                          </button>
                        )}
                        <span className="badge badge-post">
                          {visibleAssets.length}
                          {visibleAssets.length !== allColAssets.length && ` / ${allColAssets.length}`}
                        </span>
                      </div>
                    </div>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                      {visibleAssets.length === 0 ? (
                        <div style={{ textAlign: 'center', padding: '2rem 1rem', color: '#6b7280', fontSize: '0.78rem' }}>
                          Sin activos en esta vista
                        </div>
                      ) : (
                        visibleAssets.map((a) => {
                          const title = lang === 'es' ? a.title_es || a.title_en : a.title_en || a.title_es;
                          return (
                            <div
                              key={a.id}
                              className="kanban-card"
                              onClick={() => setSelectedAssetForModal(a)}
                              style={{ cursor: 'pointer' }}
                              title={t.modal_preview_confirm}
                            >
                              <div style={{ display: 'flex', justifyContent: 'space-between', gap: '0.5rem', alignItems: 'center' }}>
                                <div style={{ display: 'flex', gap: '0.35rem', alignItems: 'center' }}>
                                  <span className={`badge badge-${a.asset_type}`} style={{ fontSize: '0.6875rem' }}>
                                    {a.asset_type.toUpperCase()}
                                  </span>
                                  {a.is_cloud_idea && (
                                    <span className="badge badge-cloud" style={{ fontSize: '0.6875rem', background: 'rgba(6, 182, 212, 0.15)', color: '#22d3ee', border: '1px solid rgba(6, 182, 212, 0.4)' }}>
                                      ☁️ {t.badge_cloud_idea}
                                    </span>
                                  )}
                                  {a.is_local_idea && (
                                    <span className="badge badge-local">{t.badge_local_idea}</span>
                                  )}
                                </div>
                                <span style={{ fontSize: '0.6875rem', color: '#9ca3af', fontFamily: 'var(--font-mono)' }}>
                                  {a.publish_date || 'Sin fecha'}
                                </span>
                              </div>
                              <div className="card-title">{title || a.id}</div>
                              <div className="card-meta">
                                <span>{a.category}</span>
                                <span style={{ color: '#06b6d4', fontWeight: 700 }}>
                                  Score: {a.seo_audit?.score_0_100 ?? 0}
                                </span>
                              </div>
                            </div>
                          );
                        })
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* 4. VISTA CALENDARIO MENSUAL ESTILO NOTION */}
        {activeTab === 'calendar' && (
          <div className="calendar-wrapper">
            <div className="calendar-header">
              <div>
                <div className="calendar-month-title">
                  {t.cal_month_names[calendarDate.getMonth()]} {calendarDate.getFullYear()}
                </div>
                <div style={{ fontSize: '0.82rem', color: '#9ca3af', marginTop: '0.2rem' }}>
                  Planificación editorial mensual interactiva con navegación cronológica.
                </div>
              </div>

              <div className="calendar-nav-group">
                <button className="btn btn-outline" onClick={handlePrevMonth} title={t.cal_prev_month}>
                  <ChevronLeft size={16} />
                </button>
                <button className="btn btn-outline" onClick={handleToday}>
                  {t.cal_today}
                </button>
                <button className="btn btn-outline" onClick={handleNextMonth} title={t.cal_next_month}>
                  <ChevronRight size={16} />
                </button>
              </div>
            </div>

            <div className="calendar-grid">
              {/* Encabezados Días de la Semana */}
              {t.cal_day_names.map((dayName) => (
                <div key={dayName} className="calendar-weekday-head">
                  {dayName}
                </div>
              ))}

              {/* Celdas de Días */}
              {calendarGrid.map((cell, idx) => {
                const dayAssets = calendarEventsMap.get(cell.dateStr) || [];
                const isToday = cell.dateStr === '2026-10-28';

                return (
                  <div
                    key={`${cell.dateStr}-${idx}`}
                    className={`calendar-day-cell ${!cell.isCurrentMonth ? 'other-month' : ''}`}
                  >
                    <div className="day-header">
                      <span className={`day-number ${isToday ? 'is-today' : ''}`}>
                        {cell.day}
                      </span>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                        {cell.isCurrentMonth && (
                          <button
                            className="btn-icon-add"
                            style={{ width: '16px', height: '16px', fontSize: '0.65rem', padding: 0 }}
                            onClick={() => openNewIdeaModal(cell.dateStr, 'scheduled')}
                            title={`+ Planificar idea para ${cell.dateStr}`}
                          >
                            +
                          </button>
                        )}
                        {dayAssets.length > 0 && (
                          <span style={{ fontSize: '0.6875rem', color: '#10b981', fontWeight: 700 }}>
                            {dayAssets.length}
                          </span>
                        )}
                      </div>
                    </div>

                    <div className="day-events-list">
                      {dayAssets.map((a) => {
                        const title = lang === 'es' ? a.title_es || a.title_en : a.title_en || a.title_es;
                        const isScheduled = a.status === 'scheduled';
                        const isIdea = a.status === 'idea';
                        const isDraft = a.status === 'draft';
                        const chipClass = isScheduled
                          ? 'chip-scheduled'
                          : isIdea
                          ? 'chip-idea'
                          : isDraft
                          ? 'chip-draft'
                          : 'chip-published';
                        const chipIcon = isScheduled ? '🔵' : isIdea ? '💡' : isDraft ? '📝' : '🟢';

                        return (
                          <div
                            key={a.id}
                            className={`day-chip ${chipClass}`}
                            title={`${title} (${a.status.toUpperCase()})`}
                            onClick={() => setSelectedAssetForModal(a)}
                            style={{ cursor: 'pointer' }}
                          >
                            <span style={{ fontSize: '0.65rem' }}>{chipIcon}</span>
                            <span style={{ overflow: 'hidden', textOverflow: 'ellipsis' }}>{title || a.id}</span>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* 5. VISTA SALUD & ROI EXTENDIDO */}
        {activeTab === 'health' && (
          <div className="health-wrapper">
            {/* Hero Card: Patrimonio Editorial */}
            <div className="equity-hero-card">
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.4rem' }}>
                  <Award size={22} color="#10b981" />
                  <span style={{ fontFamily: 'var(--font-heading)', fontWeight: 700, fontSize: '1.1rem', color: '#f9fafb' }}>
                    {t.kpi_content_equity}
                  </span>
                </div>
                <div className="equity-number">${contentEquityUSD.toLocaleString()} USD</div>
                <p style={{ color: '#9ca3af', fontSize: '0.85rem', marginTop: '0.5rem', maxWidth: '750px' }}>
                  {t.equity_explanation.replace('{words}', totalWords.toLocaleString())}
                </p>
              </div>

              <a
                href="https://datalaria.com/es/recursos/#pack-pulse"
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-primary"
                style={{ padding: '0.85rem 1.5rem', fontSize: '0.95rem' }}
              >
                <Zap size={18} />
                <span>Rentabilizar con Pulse Kit</span>
              </a>
            </div>

            {/* Matriz de 4 Cuadrantes de Oportunidad */}
            <div>
              <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.25rem', marginBottom: '1rem', color: '#f9fafb' }}>
                {t.health_matrix_title}
              </h3>

              <div className="quadrants-grid">
                {/* Cuadrante 1: Joyas Ocultas */}
                <div className="quadrant-card">
                  <div className="quadrant-header">
                    <Sparkles size={18} color="#06b6d4" />
                    <span style={{ color: '#06b6d4' }}>{t.quadrant_gems_title}</span>
                  </div>
                  <div className="quadrant-count" style={{ color: '#06b6d4' }}>
                    {healthMatrix.gems.length}
                  </div>
                  <p style={{ fontSize: '0.8rem', color: '#9ca3af', lineHeight: 1.45 }}>
                    {t.quadrant_gems_desc}
                  </p>
                </div>

                {/* Cuadrante 2: Motores de Tráfico */}
                <div className="quadrant-card">
                  <div className="quadrant-header">
                    <TrendingUp size={18} color="#10b981" />
                    <span style={{ color: '#10b981' }}>{t.quadrant_cash_title}</span>
                  </div>
                  <div className="quadrant-count" style={{ color: '#10b981' }}>
                    {healthMatrix.cashCows.length}
                  </div>
                  <p style={{ fontSize: '0.8rem', color: '#9ca3af', lineHeight: 1.45 }}>
                    {t.quadrant_cash_desc}
                  </p>
                </div>

                {/* Cuadrante 3: Candidatos a Refresh */}
                <div className="quadrant-card">
                  <div className="quadrant-header">
                    <RefreshCw size={18} color="#f59e0b" />
                    <span style={{ color: '#f59e0b' }}>{t.quadrant_decay_title}</span>
                  </div>
                  <div className="quadrant-count" style={{ color: '#f59e0b' }}>
                    {healthMatrix.decay.length}
                  </div>
                  <p style={{ fontSize: '0.8rem', color: '#9ca3af', lineHeight: 1.45 }}>
                    {t.quadrant_decay_desc}
                  </p>
                </div>

                {/* Cuadrante 4: Brecha de Monetización */}
                <div className="quadrant-card">
                  <div className="quadrant-header">
                    <DollarSign size={18} color="#8b5cf6" />
                    <span style={{ color: '#8b5cf6' }}>{t.quadrant_gap_title}</span>
                  </div>
                  <div className="quadrant-count" style={{ color: '#8b5cf6' }}>
                    {healthMatrix.monetizationGap.length}
                  </div>
                  <p style={{ fontSize: '0.8rem', color: '#9ca3af', lineHeight: 1.45 }}>
                    {t.quadrant_gap_desc}
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* MODAL DETALLE DE ACTIVO (CONSULTA DE APERTURA WEB) */}
      {selectedAssetForModal && (
        <div className="modal-overlay" onClick={() => setSelectedAssetForModal(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '600px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '1rem' }}>
              <div>
                <span className={`badge badge-${selectedAssetForModal.asset_type}`} style={{ textTransform: 'uppercase', marginBottom: '0.4rem' }}>
                  {selectedAssetForModal.asset_type}
                </span>
                <h3 style={{ fontSize: '1.15rem', fontWeight: 800, margin: '0.35rem 0', color: '#f9fafb', lineHeight: 1.35, fontFamily: 'var(--font-heading)' }}>
                  {lang === 'es'
                    ? selectedAssetForModal.title_es || selectedAssetForModal.title_en
                    : selectedAssetForModal.title_en || selectedAssetForModal.title_es}
                </h3>
                <div style={{ fontSize: '0.8rem', color: '#9ca3af' }}>
                  {selectedAssetForModal.category} {selectedAssetForModal.series && `· Serie: ${selectedAssetForModal.series}`}
                </div>
              </div>
              <button
                className="btn btn-ghost"
                onClick={() => setSelectedAssetForModal(null)}
                style={{ padding: '0.35rem' }}
              >
                <X size={20} />
              </button>
            </div>

            {/* Metadatos en Grid */}
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(2, 1fr)',
                gap: '0.75rem',
                background: 'rgba(15, 23, 42, 0.7)',
                padding: '1rem',
                borderRadius: '10px',
                border: '1px solid var(--border-color)',
                fontSize: '0.82rem'
              }}
            >
              <div>
                <span style={{ color: '#9ca3af', display: 'block', fontSize: '0.72rem', textTransform: 'uppercase', fontWeight: 700 }}>
                  {t.col_status}
                </span>
                <span className={`badge badge-${selectedAssetForModal.status}`} style={{ marginTop: '0.25rem' }}>
                  {selectedAssetForModal.status.toUpperCase()}
                </span>
              </div>
              <div>
                <span style={{ color: '#9ca3af', display: 'block', fontSize: '0.72rem', textTransform: 'uppercase', fontWeight: 700 }}>
                  {t.col_date}
                </span>
                <strong style={{ color: '#f9fafb', display: 'block', marginTop: '0.25rem' }}>
                  {selectedAssetForModal.publish_date || 'Sin fecha'}
                </strong>
              </div>
              <div>
                <span style={{ color: '#9ca3af', display: 'block', fontSize: '0.72rem', textTransform: 'uppercase', fontWeight: 700 }}>
                  {t.col_words}
                </span>
                <strong style={{ color: '#f9fafb', display: 'block', marginTop: '0.25rem' }}>
                  {(lang === 'es' ? selectedAssetForModal.word_count_es : selectedAssetForModal.word_count_en).toLocaleString()} pal.
                  <span style={{ color: '#9ca3af', fontSize: '0.72rem', fontWeight: 400, marginLeft: '0.3rem' }}>
                    (~{selectedAssetForModal.reading_time_min} min)
                  </span>
                </strong>
              </div>
              <div>
                <span style={{ color: '#9ca3af', display: 'block', fontSize: '0.72rem', textTransform: 'uppercase', fontWeight: 700 }}>
                  {t.col_seo}
                </span>
                <strong
                  style={{
                    color: (selectedAssetForModal.seo_audit?.score_0_100 ?? 0) >= 80 ? '#10b981' : '#f59e0b',
                    display: 'block',
                    marginTop: '0.25rem'
                  }}
                >
                  {selectedAssetForModal.seo_audit?.score_0_100 ?? 0} / 100
                </strong>
              </div>
              <div>
                <span style={{ color: '#9ca3af', display: 'block', fontSize: '0.72rem', textTransform: 'uppercase', fontWeight: 700 }}>
                  {t.col_relative_index}
                </span>
                <strong style={{ color: '#06b6d4', display: 'block', marginTop: '0.25rem' }}>
                  {selectedAssetForModal.metrics_relative ? `Índice ${selectedAssetForModal.metrics_relative.index_100}` : '—'}
                </strong>
              </div>
              <div>
                <span style={{ color: '#9ca3af', display: 'block', fontSize: '0.72rem', textTransform: 'uppercase', fontWeight: 700 }}>
                  {t.col_parity}
                </span>
                <span
                  className={`badge badge-${selectedAssetForModal.language_parity === 'complete' ? 'complete' : 'alert'}`}
                  style={{ marginTop: '0.25rem' }}
                >
                  {selectedAssetForModal.language_parity === 'complete' ? t.badge_parity_complete : t.badge_parity_missing}
                </span>
              </div>
            </div>

            {selectedAssetForModal.status === 'scheduled' && (
              <div
                style={{
                  background: 'rgba(56, 189, 248, 0.08)',
                  border: '1px solid rgba(56, 189, 248, 0.25)',
                  padding: '0.75rem 1rem',
                  borderRadius: '8px',
                  fontSize: '0.8rem',
                  color: '#38bdf8'
                }}
              >
                📅 {t.status_scheduled_note}
              </div>
            )}

            {/* Notas / Briefing de la Idea o Contenido */}
            {(selectedAssetForModal.brief_es || selectedAssetForModal.brief_en) && (
              <div
                style={{
                  background: 'rgba(15, 23, 42, 0.65)',
                  border: '1px solid var(--border-color)',
                  padding: '0.85rem 1rem',
                  borderRadius: '8px',
                  fontSize: '0.82rem',
                  color: '#e5e7eb',
                  lineHeight: 1.5
                }}
              >
                <span style={{ color: '#9ca3af', display: 'block', fontSize: '0.72rem', textTransform: 'uppercase', fontWeight: 700, marginBottom: '0.35rem' }}>
                  {t.field_idea_brief}
                </span>
                {selectedAssetForModal.brief_es || selectedAssetForModal.brief_en}
              </div>
            )}

            <div
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                flexWrap: 'wrap',
                marginTop: '0.5rem',
                gap: '0.75rem',
                borderTop: '1px solid var(--border-color)',
                paddingTop: '1rem'
              }}
            >
              <span style={{ fontSize: '0.85rem', color: '#9ca3af' }}>
                {selectedAssetForModal.is_cloud_idea
                  ? '☁️ ' + t.badge_cloud_idea
                  : selectedAssetForModal.is_local_idea
                  ? '💡 ' + t.badge_local_idea
                  : t.modal_preview_confirm}
              </span>
              <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                {(selectedAssetForModal.is_local_idea || selectedAssetForModal.is_cloud_idea) && (
                  <>
                    <button
                      className="btn btn-outline"
                      style={{ borderColor: 'rgba(56, 189, 248, 0.4)', color: '#38bdf8' }}
                      onClick={() => openEditIdeaModal(selectedAssetForModal)}
                      title={t.btn_edit_idea}
                    >
                      <Edit3 size={15} />
                      <span>{t.btn_edit_idea}</span>
                    </button>
                    <button
                      className="btn btn-outline"
                      style={{ borderColor: 'rgba(239, 68, 68, 0.4)', color: '#f87171' }}
                      onClick={() => handleDeleteLocalIdea(selectedAssetForModal.id)}
                      title={t.btn_delete_idea}
                    >
                      <Trash2 size={15} />
                      <span>{t.btn_delete_idea}</span>
                    </button>
                  </>
                )}
                <button className="btn btn-ghost" onClick={() => setSelectedAssetForModal(null)}>
                  {t.btn_close}
                </button>
                {!(selectedAssetForModal.is_local_idea || selectedAssetForModal.is_cloud_idea) && (
                  <button
                    className="btn btn-primary"
                    onClick={() => {
                      const slugUrl = selectedAssetForModal.url_es || `/es/posts/${selectedAssetForModal.slug}/`;
                      const fullUrl = slugUrl.startsWith('http') ? slugUrl : `https://datalaria.com${slugUrl}`;
                      window.open(fullUrl, '_blank', 'noopener,noreferrer');
                      setSelectedAssetForModal(null);
                    }}
                  >
                    <ExternalLink size={16} />
                    <span>{t.btn_open_article}</span>
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* MODAL REGISTRAR / EDITAR IDEA */}
      {isIdeaModalOpen && (
        <div className="modal-overlay" onClick={() => setIsIdeaModalOpen(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '540px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Sparkles size={20} color="#10b981" />
                <h3 style={{ fontSize: '1.15rem', fontWeight: 800, margin: 0, color: '#f9fafb', fontFamily: 'var(--font-heading)' }}>
                  {editingIdeaId ? t.modal_edit_idea_title : t.modal_idea_title}
                </h3>
              </div>
              <button
                className="btn btn-ghost"
                onClick={() => setIsIdeaModalOpen(false)}
                style={{ padding: '0.35rem' }}
              >
                <X size={20} />
              </button>
            </div>

            <p style={{ fontSize: '0.82rem', color: '#9ca3af', margin: 0 }}>
              {t.modal_idea_desc}
            </p>

            <form onSubmit={handleSaveIdea} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div className="form-group">
                <label className="form-label">{t.field_idea_title}</label>
                <input
                  type="text"
                  required
                  className="form-input"
                  placeholder="Ej: Análisis Cuantitativo de Churn con Cohortes en SaaS..."
                  value={ideaTitle}
                  onChange={(e) => setIdeaTitle(e.target.value)}
                  autoFocus
                />
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
                <div className="form-group">
                  <label className="form-label">{t.field_idea_type}</label>
                  <select
                    className="form-select"
                    value={ideaType}
                    onChange={(e) => setIdeaType(e.target.value as AssetType)}
                  >
                    <option value="post">{t.type_posts} (Post / Guía)</option>
                    <option value="app">{t.type_apps} (Web Sandbox)</option>
                    <option value="kit">{t.type_kits} (Plantilla / Pack)</option>
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">{t.field_idea_status}</label>
                  <select
                    className="form-select"
                    value={ideaStatus}
                    onChange={(e) => setIdeaStatus(e.target.value as AssetStatus)}
                  >
                    <option value="idea">💡 Idea</option>
                    <option value="draft">📝 Borrador (Draft)</option>
                    <option value="scheduled">📅 Programado</option>
                  </select>
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
                <div className="form-group">
                  <label className="form-label">{t.field_idea_category}</label>
                  <select
                    className="form-select"
                    value={ideaCategory}
                    onChange={(e) => setIdeaCategory(e.target.value)}
                  >
                    <option value="Inteligencia Artificial">Inteligencia Artificial</option>
                    <option value="Estrategia Empresarial">Estrategia Empresarial</option>
                    <option value="Control Operativo">Control Operativo & S&OP</option>
                    <option value="Finanzas Corporativas">Finanzas & Decisiones</option>
                    <option value="Ingeniería de Software & SDD">Ingeniería & DevOps</option>
                    <option value="Casos de Éxito">Casos de Éxito</option>
                    <option value="Biografías">Biografías</option>
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">{t.field_idea_date}</label>
                  <input
                    type="date"
                    className="form-input"
                    value={ideaDate}
                    onChange={(e) => setIdeaDate(e.target.value)}
                  />
                </div>
              </div>

              <div className="form-group">
                <label className="form-label">{t.field_idea_brief}</label>
                <textarea
                  className="form-textarea"
                  rows={3}
                  placeholder="Objetivo del artículo, fórmulas matemáticas a incluir, público objetivo (C-Level, Product, Data)..."
                  value={ideaBrief}
                  onChange={(e) => setIdeaBrief(e.target.value)}
                />
              </div>

              {ideaSuccessMsg && (
                <div
                  style={{
                    background: 'rgba(16, 185, 129, 0.15)',
                    border: '1px solid #10b981',
                    color: '#34d399',
                    padding: '0.65rem',
                    borderRadius: '8px',
                    fontSize: '0.85rem',
                    textAlign: 'center',
                    fontWeight: 600
                  }}
                >
                  {ideaSuccessMsg}
                </div>
              )}

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '0.5rem' }}>
                <button
                  type="button"
                  className="btn btn-ghost"
                  onClick={() => setIsIdeaModalOpen(false)}
                >
                  {t.btn_close}
                </button>
                <button type="submit" className="btn btn-primary">
                  <Sparkles size={16} />
                  <span>{editingIdeaId ? t.btn_update_idea : t.btn_save_idea}</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* MODAL IMPORTADOR DE NOTION */}
      {isNotionModalOpen && (
        <div className="modal-overlay" onClick={() => setIsNotionModalOpen(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h3 style={{ fontSize: '1.2rem', fontWeight: 700, fontFamily: 'var(--font-heading)' }}>
                {t.notion_modal_title}
              </h3>
              <button
                className="btn-ghost"
                onClick={() => setIsNotionModalOpen(false)}
                style={{ padding: '0.25rem', cursor: 'pointer', borderRadius: '6px' }}
              >
                <X size={20} />
              </button>
            </div>

            <p style={{ fontSize: '0.875rem', color: '#9ca3af', lineHeight: 1.5 }}>
              {t.notion_modal_desc}
            </p>

            <input
              type="file"
              accept=".csv"
              ref={fileInputRef}
              style={{ display: 'none' }}
              onChange={handleNotionFileUpload}
            />

            <div className="drop-zone" onClick={() => fileInputRef.current?.click()}>
              <Upload size={38} color="#10b981" style={{ margin: '0 auto 0.75rem auto' }} />
              <div style={{ fontWeight: 600, fontSize: '0.95rem', color: '#f9fafb' }}>
                {t.notion_drop_here}
              </div>
              <div style={{ fontSize: '0.75rem', color: '#6b7280', marginTop: '0.4rem' }}>
                Formatos soportados: CSV exportado de Notion (con columnas Title, Status, Category, Date...)
              </div>
            </div>

            {notionSuccessMsg && (
              <div
                style={{
                  background: 'rgba(16, 185, 129, 0.15)',
                  border: '1px solid #10b981',
                  color: '#34d399',
                  padding: '0.85rem',
                  borderRadius: '8px',
                  fontSize: '0.875rem',
                  textAlign: 'center',
                  fontWeight: 600
                }}
              >
                {notionSuccessMsg}
              </div>
            )}
          </div>
        </div>
      )}

      {/* MODAL AUTENTICACIÓN SUPABASE PRO CLOUD (ADR-015) */}
      {isAuthModalOpen && (
        <div className="modal-overlay" onClick={() => setIsAuthModalOpen(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '440px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <div style={{ background: 'rgba(6, 182, 212, 0.2)', padding: '0.4rem', borderRadius: '8px' }}>
                  <Cloud size={20} color="#22d3ee" />
                </div>
                <h3 style={{ fontSize: '1.2rem', fontWeight: 700, fontFamily: 'var(--font-heading)' }}>
                  {t.modal_auth_title}
                </h3>
              </div>
              <button
                className="btn-ghost"
                onClick={() => setIsAuthModalOpen(false)}
                style={{ padding: '0.25rem', cursor: 'pointer', borderRadius: '6px' }}
              >
                <X size={20} />
              </button>
            </div>

            <p style={{ fontSize: '0.85rem', color: '#94a3b8', lineHeight: 1.5, marginTop: '0.5rem' }}>
              {t.modal_auth_desc}
            </p>

            {/* Acceso Rápido Demo 1-Clic */}
            <div style={{ background: 'rgba(6, 182, 212, 0.08)', border: '1px solid rgba(6, 182, 212, 0.3)', borderRadius: '10px', padding: '1rem', marginTop: '1rem' }}>
              <div style={{ fontSize: '0.8rem', color: '#22d3ee', fontWeight: 600, marginBottom: '0.5rem' }}>
                {t.demo_login_hint}
              </div>
              <button
                type="button"
                className="btn btn-primary"
                onClick={handleDemoLogin}
                disabled={authLoading}
                style={{ width: '100%', justifyContent: 'center', background: 'linear-gradient(135deg, #0891b2 0%, #06b6d4 100%)' }}
              >
                <Zap size={16} />
                <span>{authLoading ? 'Iniciando...' : t.btn_demo_login_1click}</span>
              </button>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', margin: '1.25rem 0', color: '#64748b', fontSize: '0.8rem' }}>
              <div style={{ flex: 1, height: '1px', background: '#334155' }} />
              <span>{t.auth_divider}</span>
              <div style={{ flex: 1, height: '1px', background: '#334155' }} />
            </div>

            {/* Formulario de Login Personal */}
            <form onSubmit={handlePasswordLogin} style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', color: '#94a3b8', marginBottom: '0.3rem' }}>
                  {t.field_email}
                </label>
                <input
                  type="email"
                  className="search-input"
                  value={authEmail}
                  onChange={(e) => setAuthEmail(e.target.value)}
                  placeholder="tu-email@empresa.com"
                  required
                  style={{ width: '100%', background: '#0f172a' }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', color: '#94a3b8', marginBottom: '0.3rem' }}>
                  {t.field_password}
                </label>
                <input
                  type="password"
                  className="search-input"
                  value={authPassword}
                  onChange={(e) => setAuthPassword(e.target.value)}
                  placeholder="••••••••"
                  required
                  style={{ width: '100%', background: '#0f172a' }}
                />
              </div>

              {authError && (
                <div style={{ background: 'rgba(239, 68, 68, 0.15)', border: '1px solid #ef4444', color: '#f87171', padding: '0.6rem', borderRadius: '6px', fontSize: '0.8rem' }}>
                  {authError}
                </div>
              )}

              {authSuccessMsg && (
                <div style={{ background: 'rgba(16, 185, 129, 0.15)', border: '1px solid #10b981', color: '#34d399', padding: '0.6rem', borderRadius: '6px', fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                  <CheckCircle2 size={16} />
                  <span>{authSuccessMsg}</span>
                </div>
              )}

              <div style={{ display: 'flex', gap: '0.6rem', marginTop: '0.5rem' }}>
                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={authLoading}
                  style={{ flex: 1, justifyContent: 'center' }}
                >
                  <LogIn size={15} />
                  <span>{t.btn_sign_in}</span>
                </button>
                <button
                  type="button"
                  className="btn btn-outline"
                  onClick={handleSignUp}
                  disabled={authLoading}
                  style={{ flex: 1, justifyContent: 'center' }}
                >
                  <span>{t.btn_sign_up}</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
