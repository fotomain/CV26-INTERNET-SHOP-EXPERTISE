import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../store';
import {
  setCategoryFilter,
  setTierFilter,
  setApprovalFilter,
  setSearchQuery,
} from '../store/slices/resultSlice';
import {
  TrendingUp,
  Check,
  X,
  Layers,
  Palette,
  Search,
  BarChart3,
  Award,
  Sparkles,
  Download,
  CheckCircle2,
  SlidersHorizontal,
  Flame,
  FileCode2
} from 'lucide-react';

export const CapstoneReportComponent: React.FC = () => {
  const dispatch = useDispatch();
  const {
    resultData,
    selectedCategoryFilter,
    selectedTierFilter,
    selectedApprovalFilter,
    searchQuery,
  } = useSelector((state: RootState) => state.result);

  const [activeTab, setActiveTab] = useState<'catalog' | 'palettes' | 'categories' | 'json'>('catalog');

  if (!resultData || !resultData.kpis) {
    return null;
  }

  const { kpis, targetCountry, products = [], categoryBreakdown = [], metadata, mlModelStats } = resultData;

  // Filter products
  const filteredProducts = products.filter((p: any) => {
    const matchesSearch = !searchQuery || p.name.toLowerCase().includes(searchQuery.toLowerCase()) || p.categoryName.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategoryFilter === 'ALL' || p.categoryName === selectedCategoryFilter;
    const matchesTier = selectedTierFilter === 'ALL' || p.priorityTier.includes(selectedTierFilter);
    const matchesApproval = selectedApprovalFilter === 'ALL' || (selectedApprovalFilter === 'APPROVED' ? p.isGoodForMarketing : !p.isGoodForMarketing);
    return matchesSearch && matchesCategory && matchesTier && matchesApproval;
  });

  const categoriesList = Array.from(new Set(products.map((p: any) => p.categoryName)));

  const handleExportJSON = () => {
    const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(resultData, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute('href', dataStr);
    downloadAnchor.setAttribute('download', `cv26_dss_results_${metadata?.userSessionGUID || 'session'}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  return (
    <div style={{
      background: '#ffffff',
      borderRadius: '24px',
      border: '2px solid #fed7aa',
      boxShadow: '0 12px 36px -4px rgba(245, 158, 11, 0.1), 0 4px 12px rgba(0, 0, 0, 0.04)',
      overflow: 'hidden',
      display: 'flex',
      flexDirection: 'column',
      gap: '24px',
      padding: '30px',
      position: 'relative'
    }}>
      {/* Decorative top rainbow bar */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        height: '6px',
        background: 'linear-gradient(90deg, #f59e0b 0%, #ea580c 25%, #e11d48 50%, #8b5cf6 75%, #0ea5e9 100%)'
      }} />

      {/* Banner Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '16px',
        borderBottom: '2px solid #fff7ed',
        paddingBottom: '20px',
        marginTop: '6px'
      }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <span style={{
              background: 'linear-gradient(135deg, #f59e0b 0%, #ea580c 100%)',
              color: '#ffffff',
              padding: '4px 10px',
              borderRadius: '999px',
              fontSize: '11px',
              fontWeight: 800,
              display: 'flex',
              alignItems: 'center',
              gap: '4px',
              boxShadow: '0 2px 8px rgba(245, 158, 11, 0.35)'
            }}>
              <Sparkles size={12} />
              CAPSTONE DSS ENGINE
            </span>
            <h2 style={{ fontSize: '20px', fontWeight: 900, color: '#0f172a', letterSpacing: '-0.03em', margin: 0 }}>
              Executive Decision Report
            </h2>
          </div>
          <p style={{ fontSize: '13px', color: '#64748b', margin: '4px 0 0 0' }}>
            Target Country: <strong style={{ color: '#0f172a' }}>{targetCountry?.name} ({targetCountry?.isoCode})</strong> &bull; Duration: <strong style={{ color: '#ea580c' }}>{metadata?.executionDuration || '00:00'}</strong>
          </p>
        </div>

        <div style={{ display: 'flex', gap: '10px' }}>
          <button
            onClick={handleExportJSON}
            style={{
              background: 'linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)',
              border: '1.5px solid #cbd5e1',
              color: '#334155',
              padding: '8px 16px',
              borderRadius: '12px',
              fontSize: '13px',
              fontWeight: 700,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              boxShadow: '0 2px 6px rgba(0,0,0,0.05)',
              transition: 'all 0.15s ease'
            }}
          >
            <Download size={14} color="#0ea5e9" />
            Export resultDataJSON
          </button>
        </div>
      </div>

      {/* 4 Colorful KPI Cards Grid (Directly matching CAPSTONE_REPORT) */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(210px, 1fr))',
        gap: '16px'
      }}>
        {/* Card 1: Total SKUs (Blue) */}
        <div style={{
          background: 'linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%)',
          border: '2px solid #bae6fd',
          borderRadius: '16px',
          padding: '18px 20px',
          boxShadow: '0 4px 14px rgba(14, 165, 233, 0.08)'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', color: '#0284c7', fontSize: '11.5px', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            <span>Catalog Items</span>
            <Layers size={18} color="#0284c7" />
          </div>
          <div style={{ fontSize: '32px', fontWeight: 900, color: '#0369a1', letterSpacing: '-0.03em', marginTop: '4px' }}>
            {kpis.totalItems}
          </div>
          <div style={{ fontSize: '12px', color: '#0284c7', marginTop: '2px', fontWeight: 600 }}>
            Candidate products evaluated
          </div>
        </div>

        {/* Card 2: Approved % (Emerald Green) */}
        <div style={{
          background: 'linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)',
          border: '2px solid #bbf7d0',
          borderRadius: '16px',
          padding: '18px 20px',
          boxShadow: '0 4px 14px rgba(22, 163, 74, 0.08)'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', color: '#15803d', fontSize: '11.5px', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            <span>Approved for Market</span>
            <CheckCircle2 size={18} color="#16a34a" />
          </div>
          <div style={{ fontSize: '32px', fontWeight: 900, color: '#14532d', letterSpacing: '-0.03em', marginTop: '4px' }}>
            {kpis.goodForMarketingPct}%
          </div>
          <div style={{ fontSize: '12px', color: '#15803d', marginTop: '2px', fontWeight: 600 }}>
            {kpis.goodForMarketingCount} of {kpis.totalItems} match {targetCountry?.name} styles
          </div>
        </div>

        {/* Card 3: Compatibility Score (Warm Amber / Orange) */}
        <div style={{
          background: 'linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%)',
          border: '2px solid #fde68a',
          borderRadius: '16px',
          padding: '18px 20px',
          boxShadow: '0 4px 14px rgba(245, 158, 11, 0.1)'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', color: '#b45309', fontSize: '11.5px', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            <span>Compatibility Score</span>
            <TrendingUp size={18} color="#d97706" />
          </div>
          <div style={{ fontSize: '32px', fontWeight: 900, color: '#78350f', letterSpacing: '-0.03em', marginTop: '4px' }}>
            {kpis.averageCompatibilityScore}
          </div>
          <div style={{ fontSize: '12px', color: '#b45309', marginTop: '2px', fontWeight: 600 }}>
            Avg &Delta;E: <strong>{kpis.averageDeltaEDistance}</strong> (&le; 13.5 target)
          </div>
        </div>

        {/* Card 4: Quality Ready (Purple) */}
        <div style={{
          background: 'linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%)',
          border: '2px solid #e9d5ff',
          borderRadius: '16px',
          padding: '18px 20px',
          boxShadow: '0 4px 14px rgba(124, 58, 237, 0.08)'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', color: '#7c3aed', fontSize: '11.5px', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            <span>Quality Ready</span>
            <Award size={18} color="#7c3aed" />
          </div>
          <div style={{ fontSize: '32px', fontWeight: 900, color: '#581c87', letterSpacing: '-0.03em', marginTop: '4px' }}>
            {kpis.readyToSalePct}%
          </div>
          <div style={{ fontSize: '12px', color: '#7c3aed', marginTop: '2px', fontWeight: 600 }}>
            {kpis.readyToSaleCount} pass title &amp; image checks
          </div>
        </div>
      </div>

      {/* Colorful Navigation Tabs */}
      <div style={{ display: 'flex', gap: '8px', borderBottom: '2px solid #f1f5f9', paddingBottom: '10px' }}>
        <button
          onClick={() => setActiveTab('catalog')}
          style={{
            background: activeTab === 'catalog' ? 'linear-gradient(135deg, #f59e0b 0%, #ea580c 100%)' : '#f8fafc',
            color: activeTab === 'catalog' ? '#ffffff' : '#64748b',
            border: activeTab === 'catalog' ? 'none' : '1px solid #e2e8f0',
            padding: '8px 18px',
            borderRadius: '999px',
            fontSize: '13px',
            fontWeight: 800,
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            boxShadow: activeTab === 'catalog' ? '0 4px 14px rgba(245, 158, 11, 0.35)' : 'none',
            transition: 'all 0.15s ease'
          }}
        >
          <Layers size={14} />
          Candidate Products ({filteredProducts.length})
        </button>

        <button
          onClick={() => setActiveTab('palettes')}
          style={{
            background: activeTab === 'palettes' ? 'linear-gradient(135deg, #f59e0b 0%, #ea580c 100%)' : '#f8fafc',
            color: activeTab === 'palettes' ? '#ffffff' : '#64748b',
            border: activeTab === 'palettes' ? 'none' : '1px solid #e2e8f0',
            padding: '8px 18px',
            borderRadius: '999px',
            fontSize: '13px',
            fontWeight: 800,
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            boxShadow: activeTab === 'palettes' ? '0 4px 14px rgba(245, 158, 11, 0.35)' : 'none',
            transition: 'all 0.15s ease'
          }}
        >
          <Palette size={14} />
          Target Market 3-Palettes
        </button>

        <button
          onClick={() => setActiveTab('categories')}
          style={{
            background: activeTab === 'categories' ? 'linear-gradient(135deg, #f59e0b 0%, #ea580c 100%)' : '#f8fafc',
            color: activeTab === 'categories' ? '#ffffff' : '#64748b',
            border: activeTab === 'categories' ? 'none' : '1px solid #e2e8f0',
            padding: '8px 18px',
            borderRadius: '999px',
            fontSize: '13px',
            fontWeight: 800,
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            boxShadow: activeTab === 'categories' ? '0 4px 14px rgba(245, 158, 11, 0.35)' : 'none',
            transition: 'all 0.15s ease'
          }}
        >
          <BarChart3 size={14} />
          Category Breakdown
        </button>

        <button
          onClick={() => setActiveTab('json')}
          style={{
            background: activeTab === 'json' ? 'linear-gradient(135deg, #f59e0b 0%, #ea580c 100%)' : '#f8fafc',
            color: activeTab === 'json' ? '#ffffff' : '#64748b',
            border: activeTab === 'json' ? 'none' : '1px solid #e2e8f0',
            padding: '8px 18px',
            borderRadius: '999px',
            fontSize: '13px',
            fontWeight: 800,
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            boxShadow: activeTab === 'json' ? '0 4px 14px rgba(245, 158, 11, 0.35)' : 'none',
            transition: 'all 0.15s ease'
          }}
        >
          <FileCode2 size={14} />
          Raw JSON Log
        </button>
      </div>

      {/* TAB 1: Products Catalog Table */}
      {activeTab === 'catalog' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {/* Filters Bar */}
          <div style={{
            display: 'flex',
            gap: '12px',
            flexWrap: 'wrap',
            alignItems: 'center',
            background: 'linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%)',
            padding: '14px 18px',
            borderRadius: '14px',
            border: '1.5px solid #fde68a'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flex: 1, minWidth: '200px', background: '#ffffff', border: '1.5px solid #fcd34d', borderRadius: '10px', padding: '6px 12px' }}>
              <Search size={16} color="#d97706" />
              <input
                type="text"
                placeholder="Search products..."
                value={searchQuery}
                onChange={(e) => dispatch(setSearchQuery(e.target.value))}
                style={{ border: 'none', outline: 'none', width: '100%', fontSize: '13px', color: '#0f172a', fontWeight: 600 }}
              />
            </div>

            <select
              value={selectedCategoryFilter}
              onChange={(e) => dispatch(setCategoryFilter(e.target.value))}
              style={{ padding: '8px 12px', borderRadius: '10px', border: '1.5px solid #fcd34d', background: '#ffffff', fontSize: '13px', fontWeight: 600, color: '#0f172a' }}
            >
              <option value="ALL">All Categories</option>
              {categoriesList.map((cat: any) => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>

            <select
              value={selectedApprovalFilter}
              onChange={(e) => dispatch(setApprovalFilter(e.target.value))}
              style={{ padding: '8px 12px', borderRadius: '10px', border: '1.5px solid #fcd34d', background: '#ffffff', fontSize: '13px', fontWeight: 600, color: '#0f172a' }}
            >
              <option value="ALL">All Decisions</option>
              <option value="APPROVED">Approved Only (Good for Marketing)</option>
              <option value="EXCLUDED">Non-Priority Only</option>
            </select>

            <select
              value={selectedTierFilter}
              onChange={(e) => dispatch(setTierFilter(e.target.value))}
              style={{ padding: '8px 12px', borderRadius: '10px', border: '1.5px solid #fcd34d', background: '#ffffff', fontSize: '13px', fontWeight: 600, color: '#0f172a' }}
            >
              <option value="ALL">All Tiers</option>
              <option value="Tier 1">Tier 1 (Prime Candidates)</option>
              <option value="Tier 2">Tier 2 (Standard Candidates)</option>
              <option value="Tier 3">Tier 3 (Non-Priority)</option>
            </select>
          </div>

          {/* Table */}
          <div style={{ overflowX: 'auto', border: '1.5px solid #e2e8f0', borderRadius: '14px' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px', textAlign: 'left' }}>
              <thead>
                <tr style={{ background: '#f8fafc', borderBottom: '2px solid #e2e8f0' }}>
                  <th style={{ padding: '12px 14px', color: '#475569', fontWeight: 800 }}>ID</th>
                  <th style={{ padding: '12px 14px', color: '#475569', fontWeight: 800 }}>Product Name</th>
                  <th style={{ padding: '12px 14px', color: '#475569', fontWeight: 800 }}>Category</th>
                  <th style={{ padding: '12px 14px', color: '#475569', fontWeight: 800 }}>Extracted Palette</th>
                  <th style={{ padding: '12px 14px', color: '#475569', fontWeight: 800 }}>Target Match</th>
                  <th style={{ padding: '12px 14px', color: '#475569', fontWeight: 800 }}>&Delta;E / Score</th>
                  <th style={{ padding: '12px 14px', color: '#475569', fontWeight: 800 }}>Decision</th>
                  <th style={{ padding: '12px 14px', color: '#475569', fontWeight: 800 }}>Campaign Tier</th>
                </tr>
              </thead>
              <tbody>
                {filteredProducts.map((p: any) => (
                  <tr key={p.itemId} style={{ borderBottom: '1px solid #f1f5f9', background: p.isGoodForMarketing ? '#ffffff' : '#fafafa' }}>
                    <td style={{ padding: '12px 14px', fontFamily: 'JetBrains Mono, monospace', color: '#64748b', fontWeight: 600 }}>
                      #{p.itemId}
                    </td>
                    <td style={{ padding: '12px 14px', fontWeight: 700, color: '#0f172a' }}>
                      {p.name}
                    </td>
                    <td style={{ padding: '12px 14px', color: '#475569' }}>
                      <span style={{ background: '#eff6ff', color: '#1d4ed8', border: '1px solid #bfdbfe', padding: '2px 8px', borderRadius: '6px', fontSize: '11.5px', fontWeight: 700 }}>
                        {p.categoryName}
                      </span>
                    </td>
                    <td style={{ padding: '12px 14px' }}>
                      <div style={{ display: 'flex', gap: '4px' }}>
                        {(p.palette || []).map((hex: string, idx: number) => (
                          <span
                            key={idx}
                            title={hex}
                            style={{
                              display: 'inline-block',
                              width: '16px',
                              height: '16px',
                              borderRadius: '4px',
                              backgroundColor: hex,
                              border: '1px solid rgba(0,0,0,0.15)',
                              boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
                            }}
                          />
                        ))}
                      </div>
                    </td>
                    <td style={{ padding: '12px 14px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                        <span
                          style={{
                            display: 'inline-block',
                            width: '14px',
                            height: '14px',
                            borderRadius: '4px',
                            backgroundColor: p.matchedColorHex || '#808080',
                            border: '1px solid rgba(0,0,0,0.2)'
                          }}
                        />
                        <span style={{ fontSize: '11.5px', color: '#334155', fontWeight: 600 }}>
                          {p.matchedPaletteTheme?.split('(')[0] || 'Theme'}
                        </span>
                      </div>
                    </td>
                    <td style={{ padding: '12px 14px', fontFamily: 'JetBrains Mono, monospace' }}>
                      <strong style={{ color: '#0f172a' }}>{p.deltaEDistance?.toFixed(1)}</strong>
                      <span style={{ fontSize: '11.5px', color: '#64748b', marginLeft: '4px' }}>
                        ({p.compatibilityScore?.toFixed(2)})
                      </span>
                    </td>
                    <td style={{ padding: '12px 14px' }}>
                      {p.isGoodForMarketing ? (
                        <span style={{
                          background: 'linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%)',
                          color: '#14532d',
                          border: '1px solid #86efac',
                          padding: '3px 9px',
                          borderRadius: '8px',
                          fontSize: '11.5px',
                          fontWeight: 800,
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '4px',
                          boxShadow: '0 2px 6px rgba(22, 163, 74, 0.15)'
                        }}>
                          <Check size={13} strokeWidth={3} /> Approved
                        </span>
                      ) : (
                        <span style={{
                          background: '#f1f5f9',
                          color: '#64748b',
                          border: '1px solid #cbd5e1',
                          padding: '3px 9px',
                          borderRadius: '8px',
                          fontSize: '11.5px',
                          fontWeight: 700,
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '4px'
                        }}>
                          <X size={13} /> Non-Priority
                        </span>
                      )}
                    </td>
                    <td style={{ padding: '12px 14px' }}>
                      <span style={{
                        fontSize: '11.5px',
                        background: p.priorityTier?.includes('Tier 1') ? '#fef3c7' : p.priorityTier?.includes('Tier 2') ? '#e0f2fe' : '#f1f5f9',
                        color: p.priorityTier?.includes('Tier 1') ? '#92400e' : p.priorityTier?.includes('Tier 2') ? '#0369a1' : '#475569',
                        border: `1px solid ${p.priorityTier?.includes('Tier 1') ? '#fde68a' : p.priorityTier?.includes('Tier 2') ? '#bae6fd' : '#cbd5e1'}`,
                        padding: '3px 8px',
                        borderRadius: '6px',
                        fontWeight: 800
                      }}>
                        {p.priorityTier}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* TAB 2: Target Country Palettes */}
      {activeTab === 'palettes' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '18px' }}>
          <div style={{
            background: 'linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%)',
            padding: '16px 20px',
            borderRadius: '14px',
            border: '1.5px solid #fde68a'
          }}>
            <h3 style={{ fontSize: '15px', fontWeight: 800, color: '#78350f', margin: 0 }}>
              🇺🇸 {targetCountry?.name} Multi-Palette Style DNA (NUMBER_PALLETS_OF_NEWCOUNTRY_REQUIRED = 3)
            </h3>
            <p style={{ fontSize: '12.5px', color: '#92400e', margin: '3px 0 0 0', fontWeight: 500 }}>
              YOLOv8 + OpenCV extracted color palettes representing Core Neutrals, Contemporary Street, and Vibrant Statement tones.
            </p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '16px' }}>
            {/* Men Palettes */}
            <div style={{ border: '2px solid #bae6fd', borderRadius: '16px', padding: '18px', background: '#f0f9ff' }}>
              <h4 style={{ fontSize: '14px', fontWeight: 800, color: '#0369a1', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                👔 Men's Collection Palettes
              </h4>
              {(targetCountry?.manPalettes || []).map((pal: string[], idx: number) => (
                <div key={idx} style={{ marginBottom: '16px' }}>
                  <div style={{ fontSize: '12px', fontWeight: 700, color: '#0284c7', marginBottom: '6px' }}>
                    {targetCountry?.paletteThemes?.[idx] || `Palette ${idx+1}`}
                  </div>
                  <div style={{ display: 'flex', gap: '8px' }}>
                    {pal.map((hex, i) => (
                      <div key={i} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '4px' }}>
                        <div style={{ width: '40px', height: '40px', borderRadius: '10px', backgroundColor: hex, border: '1.5px solid rgba(0,0,0,0.15)', boxShadow: '0 2px 6px rgba(0,0,0,0.1)' }} />
                        <span style={{ fontSize: '10px', color: '#0369a1', fontFamily: 'JetBrains Mono, monospace', fontWeight: 700 }}>{hex}</span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            {/* Women Palettes */}
            <div style={{ border: '2px solid #e9d5ff', borderRadius: '16px', padding: '18px', background: '#faf5ff' }}>
              <h4 style={{ fontSize: '14px', fontWeight: 800, color: '#6b21a8', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                👗 Women's Collection Palettes
              </h4>
              {(targetCountry?.womanPalettes || []).map((pal: string[], idx: number) => (
                <div key={idx} style={{ marginBottom: '16px' }}>
                  <div style={{ fontSize: '12px', fontWeight: 700, color: '#7c3aed', marginBottom: '6px' }}>
                    {targetCountry?.paletteThemes?.[idx] || `Palette ${idx+1}`}
                  </div>
                  <div style={{ display: 'flex', gap: '8px' }}>
                    {pal.map((hex, i) => (
                      <div key={i} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '4px' }}>
                        <div style={{ width: '40px', height: '40px', borderRadius: '10px', backgroundColor: hex, border: '1.5px solid rgba(0,0,0,0.15)', boxShadow: '0 2px 6px rgba(0,0,0,0.1)' }} />
                        <span style={{ fontSize: '10px', color: '#6b21a8', fontFamily: 'JetBrains Mono, monospace', fontWeight: 700 }}>{hex}</span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* TAB 3: Category Breakdown */}
      {activeTab === 'categories' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div style={{ overflowX: 'auto', border: '1.5px solid #e2e8f0', borderRadius: '14px' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px', textAlign: 'left' }}>
              <thead>
                <tr style={{ background: '#f8fafc', borderBottom: '2px solid #e2e8f0' }}>
                  <th style={{ padding: '12px 14px', color: '#475569', fontWeight: 800 }}>Category Name</th>
                  <th style={{ padding: '12px 14px', color: '#475569', fontWeight: 800 }}>Total Items</th>
                  <th style={{ padding: '12px 14px', color: '#475569', fontWeight: 800 }}>Approved Count</th>
                  <th style={{ padding: '12px 14px', color: '#475569', fontWeight: 800 }}>Approval Rate (%)</th>
                  <th style={{ padding: '12px 14px', color: '#475569', fontWeight: 800 }}>Avg &Delta;E</th>
                  <th style={{ padding: '12px 14px', color: '#475569', fontWeight: 800 }}>Avg Score</th>
                </tr>
              </thead>
              <tbody>
                {categoryBreakdown.map((cat: any, idx: number) => (
                  <tr key={idx} style={{ borderBottom: '1px solid #f1f5f9' }}>
                    <td style={{ padding: '12px 14px', fontWeight: 700, color: '#0f172a' }}>{cat.categoryName}</td>
                    <td style={{ padding: '12px 14px' }}>{cat.total}</td>
                    <td style={{ padding: '12px 14px', color: '#16a34a', fontWeight: 700 }}>{cat.approvedCount}</td>
                    <td style={{ padding: '12px 14px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <div style={{ width: '60px', height: '8px', background: '#e2e8f0', borderRadius: '4px', overflow: 'hidden' }}>
                          <div style={{ width: `${cat.approvedPercentage}%`, height: '100%', background: 'linear-gradient(90deg, #f59e0b 0%, #10b981 100%)' }} />
                        </div>
                        <strong style={{ color: '#0f172a' }}>{cat.approvedPercentage}%</strong>
                      </div>
                    </td>
                    <td style={{ padding: '12px 14px', fontFamily: 'JetBrains Mono, monospace' }}>{cat.avgDeltaE}</td>
                    <td style={{ padding: '12px 14px', fontFamily: 'JetBrains Mono, monospace' }}>{cat.avgScore}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* TAB 4: Raw JSON Log */}
      {activeTab === 'json' && (
        <pre style={{
          background: '#0f172a',
          color: '#38bdf8',
          padding: '20px',
          borderRadius: '14px',
          fontFamily: 'JetBrains Mono, monospace',
          fontSize: '12px',
          lineHeight: 1.5,
          maxHeight: '450px',
          overflowY: 'auto'
        }}>
          {JSON.stringify(resultData, null, 2)}
        </pre>
      )}
    </div>
  );
};
