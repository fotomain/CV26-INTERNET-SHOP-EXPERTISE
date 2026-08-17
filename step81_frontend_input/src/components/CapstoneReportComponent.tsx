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
  CheckCircle,
  XCircle,
  Clock,
  Layers,
  Palette,
  Search,
  Filter,
  BarChart3,
  Award,
  Sparkles,
  Download
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
      borderRadius: '20px',
      border: '1px solid #e2e8f0',
      boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.05)',
      overflow: 'hidden',
      display: 'flex',
      flexDirection: 'column',
      gap: '24px',
      padding: '28px'
    }}>
      {/* Banner Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '16px',
        borderBottom: '1px solid #f1f5f9',
        paddingBottom: '20px'
      }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <span style={{
              background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
              color: '#ffffff',
              padding: '4px 10px',
              borderRadius: '8px',
              fontSize: '12px',
              fontWeight: 800,
              display: 'flex',
              alignItems: 'center',
              gap: '4px'
            }}>
              <Sparkles size={14} />
              DSS VERIFIED
            </span>
            <h2 style={{ fontSize: '22px', fontWeight: 800, color: '#0f172a', margin: 0 }}>
              Capstone Executive Decision Report
            </h2>
          </div>
          <p style={{ fontSize: '13px', color: '#64748b', margin: '4px 0 0 0' }}>
            Target Country: <strong>{targetCountry?.name} ({targetCountry?.isoCode})</strong> &bull; Duration: {metadata?.executionDuration || '00:00'}
          </p>
        </div>

        <div style={{ display: 'flex', gap: '10px' }}>
          <button
            onClick={handleExportJSON}
            style={{
              background: '#f8fafc',
              border: '1px solid #cbd5e1',
              color: '#334155',
              padding: '8px 16px',
              borderRadius: '10px',
              fontSize: '13px',
              fontWeight: 600,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px'
            }}
          >
            <Download size={15} />
            Export resultDataJSON
          </button>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '16px'
      }}>
        <div style={{
          background: '#f8fafc',
          border: '1px solid #e2e8f0',
          borderRadius: '14px',
          padding: '18px 20px'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', color: '#64748b', fontSize: '12px', fontWeight: 600 }}>
            <span>Catalog Items</span>
            <Layers size={16} />
          </div>
          <div style={{ fontSize: '28px', fontWeight: 800, color: '#0f172a', marginTop: '6px' }}>
            {kpis.totalItems}
          </div>
          <div style={{ fontSize: '11px', color: '#64748b', marginTop: '4px' }}>
            Candidate products evaluated
          </div>
        </div>

        <div style={{
          background: '#f0fdf4',
          border: '1px solid #bbf7d0',
          borderRadius: '14px',
          padding: '18px 20px'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', color: '#15803d', fontSize: '12px', fontWeight: 600 }}>
            <span>Approved for Marketing</span>
            <CheckCircle size={16} />
          </div>
          <div style={{ fontSize: '28px', fontWeight: 800, color: '#14532d', marginTop: '6px' }}>
            {kpis.goodForMarketingPct}%
          </div>
          <div style={{ fontSize: '11px', color: '#166534', marginTop: '4px' }}>
            {kpis.goodForMarketingCount} of {kpis.totalItems} SKUs match {targetCountry?.name} styles
          </div>
        </div>

        <div style={{
          background: '#eff6ff',
          border: '1px solid #bfdbfe',
          borderRadius: '14px',
          padding: '18px 20px'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', color: '#1d4ed8', fontSize: '12px', fontWeight: 600 }}>
            <span>Avg Compatibility Score</span>
            <TrendingUp size={16} />
          </div>
          <div style={{ fontSize: '28px', fontWeight: 800, color: '#1e3a8a', marginTop: '6px' }}>
            {kpis.averageCompatibilityScore}
          </div>
          <div style={{ fontSize: '11px', color: '#1e40af', marginTop: '4px' }}>
            Average &Delta;E: {kpis.averageDeltaEDistance} (Threshold &le; 13.5)
          </div>
        </div>

        <div style={{
          background: '#faf5ff',
          border: '1px solid #e9d5ff',
          borderRadius: '14px',
          padding: '18px 20px'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', color: '#7e22ce', fontSize: '12px', fontWeight: 600 }}>
            <span>Quality Ready</span>
            <Award size={16} />
          </div>
          <div style={{ fontSize: '28px', fontWeight: 800, color: '#581c87', marginTop: '6px' }}>
            {kpis.readyToSalePct}%
          </div>
          <div style={{ fontSize: '11px', color: '#6b21a8', marginTop: '4px' }}>
            {kpis.readyToSaleCount} items meet title &amp; image quality
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div style={{ display: 'flex', gap: '8px', borderBottom: '2px solid #f1f5f9', paddingBottom: '8px' }}>
        <button
          onClick={() => setActiveTab('catalog')}
          style={{
            background: activeTab === 'catalog' ? '#3b82f6' : 'transparent',
            color: activeTab === 'catalog' ? '#ffffff' : '#64748b',
            border: 'none',
            padding: '8px 16px',
            borderRadius: '8px',
            fontSize: '13px',
            fontWeight: 700,
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '6px'
          }}
        >
          <Layers size={15} />
          Candidate Products ({filteredProducts.length})
        </button>

        <button
          onClick={() => setActiveTab('palettes')}
          style={{
            background: activeTab === 'palettes' ? '#3b82f6' : 'transparent',
            color: activeTab === 'palettes' ? '#ffffff' : '#64748b',
            border: 'none',
            padding: '8px 16px',
            borderRadius: '8px',
            fontSize: '13px',
            fontWeight: 700,
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '6px'
          }}
        >
          <Palette size={15} />
          Target Market 3-Palettes
        </button>

        <button
          onClick={() => setActiveTab('categories')}
          style={{
            background: activeTab === 'categories' ? '#3b82f6' : 'transparent',
            color: activeTab === 'categories' ? '#ffffff' : '#64748b',
            border: 'none',
            padding: '8px 16px',
            borderRadius: '8px',
            fontSize: '13px',
            fontWeight: 700,
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '6px'
          }}
        >
          <BarChart3 size={15} />
          Category Breakdown
        </button>

        <button
          onClick={() => setActiveTab('json')}
          style={{
            background: activeTab === 'json' ? '#3b82f6' : 'transparent',
            color: activeTab === 'json' ? '#ffffff' : '#64748b',
            border: 'none',
            padding: '8px 16px',
            borderRadius: '8px',
            fontSize: '13px',
            fontWeight: 700,
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '6px'
          }}
        >
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
            background: '#f8fafc',
            padding: '14px',
            borderRadius: '12px',
            border: '1px solid #e2e8f0'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flex: 1, minWidth: '200px', background: '#ffffff', border: '1px solid #cbd5e1', borderRadius: '8px', padding: '6px 12px' }}>
              <Search size={16} color="#94a3b8" />
              <input
                type="text"
                placeholder="Search products..."
                value={searchQuery}
                onChange={(e) => dispatch(setSearchQuery(e.target.value))}
                style={{ border: 'none', outline: 'none', width: '100%', fontSize: '13px' }}
              />
            </div>

            <select
              value={selectedCategoryFilter}
              onChange={(e) => dispatch(setCategoryFilter(e.target.value))}
              style={{ padding: '8px 12px', borderRadius: '8px', border: '1px solid #cbd5e1', background: '#ffffff', fontSize: '13px' }}
            >
              <option value="ALL">All Categories</option>
              {categoriesList.map((cat: any) => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>

            <select
              value={selectedApprovalFilter}
              onChange={(e) => dispatch(setApprovalFilter(e.target.value))}
              style={{ padding: '8px 12px', borderRadius: '8px', border: '1px solid #cbd5e1', background: '#ffffff', fontSize: '13px' }}
            >
              <option value="ALL">All Decisions</option>
              <option value="APPROVED">Approved Only (Good for Marketing)</option>
              <option value="EXCLUDED">Non-Priority Only</option>
            </select>

            <select
              value={selectedTierFilter}
              onChange={(e) => dispatch(setTierFilter(e.target.value))}
              style={{ padding: '8px 12px', borderRadius: '8px', border: '1px solid #cbd5e1', background: '#ffffff', fontSize: '13px' }}
            >
              <option value="ALL">All Tiers</option>
              <option value="Tier 1">Tier 1 (Prime Candidates)</option>
              <option value="Tier 2">Tier 2 (Standard Candidates)</option>
              <option value="Tier 3">Tier 3 (Non-Priority)</option>
            </select>
          </div>

          {/* Table */}
          <div style={{ overflowX: 'auto', border: '1px solid #e2e8f0', borderRadius: '12px' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px', textAlign: 'left' }}>
              <thead>
                <tr style={{ background: '#f8fafc', borderBottom: '2px solid #e2e8f0' }}>
                  <th style={{ padding: '12px 14px', color: '#64748b', fontWeight: 700 }}>ID</th>
                  <th style={{ padding: '12px 14px', color: '#64748b', fontWeight: 700 }}>Product Name</th>
                  <th style={{ padding: '12px 14px', color: '#64748b', fontWeight: 700 }}>Category</th>
                  <th style={{ padding: '12px 14px', color: '#64748b', fontWeight: 700 }}>Extracted Palette</th>
                  <th style={{ padding: '12px 14px', color: '#64748b', fontWeight: 700 }}>Target Match</th>
                  <th style={{ padding: '12px 14px', color: '#64748b', fontWeight: 700 }}>&Delta;E / Score</th>
                  <th style={{ padding: '12px 14px', color: '#64748b', fontWeight: 700 }}>Decision</th>
                  <th style={{ padding: '12px 14px', color: '#64748b', fontWeight: 700 }}>Campaign Tier</th>
                </tr>
              </thead>
              <tbody>
                {filteredProducts.map((p: any) => (
                  <tr key={p.itemId} style={{ borderBottom: '1px solid #f1f5f9', background: p.isGoodForMarketing ? '#ffffff' : '#fafafa' }}>
                    <td style={{ padding: '12px 14px', fontFamily: 'JetBrains Mono, monospace', color: '#64748b' }}>
                      #{p.itemId}
                    </td>
                    <td style={{ padding: '12px 14px', fontWeight: 600, color: '#0f172a' }}>
                      {p.name}
                    </td>
                    <td style={{ padding: '12px 14px', color: '#475569' }}>
                      <span style={{ background: '#f1f5f9', padding: '2px 8px', borderRadius: '4px', fontSize: '11px' }}>
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
                              border: '1px solid rgba(0,0,0,0.1)'
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
                            borderRadius: '3px',
                            backgroundColor: p.matchedColorHex || '#808080'
                          }}
                        />
                        <span style={{ fontSize: '11px', color: '#475569' }}>
                          {p.matchedPaletteTheme?.split('(')[0] || 'Theme'}
                        </span>
                      </div>
                    </td>
                    <td style={{ padding: '12px 14px', fontFamily: 'JetBrains Mono, monospace' }}>
                      <strong>{p.deltaEDistance?.toFixed(1)}</strong>
                      <span style={{ fontSize: '11px', color: '#64748b', marginLeft: '4px' }}>
                        ({p.compatibilityScore?.toFixed(2)})
                      </span>
                    </td>
                    <td style={{ padding: '12px 14px' }}>
                      {p.isGoodForMarketing ? (
                        <span style={{
                          background: '#dcfce7',
                          color: '#15803d',
                          padding: '3px 8px',
                          borderRadius: '6px',
                          fontSize: '11px',
                          fontWeight: 700,
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '4px'
                        }}>
                          <CheckCircle size={12} /> Approved
                        </span>
                      ) : (
                        <span style={{
                          background: '#f1f5f9',
                          color: '#64748b',
                          padding: '3px 8px',
                          borderRadius: '6px',
                          fontSize: '11px',
                          fontWeight: 600,
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '4px'
                        }}>
                          <XCircle size={12} /> Non-Priority
                        </span>
                      )}
                    </td>
                    <td style={{ padding: '12px 14px' }}>
                      <span style={{
                        fontSize: '11px',
                        color: p.priorityTier?.includes('Tier 1') ? '#b45309' : p.priorityTier?.includes('Tier 2') ? '#1d4ed8' : '#64748b',
                        fontWeight: 600
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
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div style={{ background: '#f8fafc', padding: '16px', borderRadius: '12px', border: '1px solid #e2e8f0' }}>
            <h3 style={{ fontSize: '15px', fontWeight: 700, color: '#0f172a', marginBottom: '4px' }}>
              🇺🇸 {targetCountry?.name} Multi-Palette Style DNA (NUMBER_PALLETS_OF_NEWCOUNTRY_REQUIRED = 3)
            </h3>
            <p style={{ fontSize: '13px', color: '#64748b', margin: 0 }}>
              YOLOv8 + OpenCV extracted color palettes representing Core Neutrals, Contemporary Street, and Vibrant Statement tones.
            </p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '16px' }}>
            {/* Men Palettes */}
            <div style={{ border: '1px solid #e2e8f0', borderRadius: '12px', padding: '16px', background: '#ffffff' }}>
              <h4 style={{ fontSize: '14px', fontWeight: 700, color: '#1e293b', marginBottom: '12px' }}>
                👔 Men's Collection Palettes
              </h4>
              {(targetCountry?.manPalettes || []).map((pal: string[], idx: number) => (
                <div key={idx} style={{ marginBottom: '14px' }}>
                  <div style={{ fontSize: '12px', fontWeight: 600, color: '#475569', marginBottom: '6px' }}>
                    {targetCountry?.paletteThemes?.[idx] || `Palette ${idx+1}`}
                  </div>
                  <div style={{ display: 'flex', gap: '8px' }}>
                    {pal.map((hex, i) => (
                      <div key={i} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '4px' }}>
                        <div style={{ width: '38px', height: '38px', borderRadius: '8px', backgroundColor: hex, border: '1px solid rgba(0,0,0,0.1)' }} />
                        <span style={{ fontSize: '10px', color: '#64748b', fontFamily: 'JetBrains Mono, monospace' }}>{hex}</span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            {/* Women Palettes */}
            <div style={{ border: '1px solid #e2e8f0', borderRadius: '12px', padding: '16px', background: '#ffffff' }}>
              <h4 style={{ fontSize: '14px', fontWeight: 700, color: '#1e293b', marginBottom: '12px' }}>
                👗 Women's Collection Palettes
              </h4>
              {(targetCountry?.womanPalettes || []).map((pal: string[], idx: number) => (
                <div key={idx} style={{ marginBottom: '14px' }}>
                  <div style={{ fontSize: '12px', fontWeight: 600, color: '#475569', marginBottom: '6px' }}>
                    {targetCountry?.paletteThemes?.[idx] || `Palette ${idx+1}`}
                  </div>
                  <div style={{ display: 'flex', gap: '8px' }}>
                    {pal.map((hex, i) => (
                      <div key={i} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '4px' }}>
                        <div style={{ width: '38px', height: '38px', borderRadius: '8px', backgroundColor: hex, border: '1px solid rgba(0,0,0,0.1)' }} />
                        <span style={{ fontSize: '10px', color: '#64748b', fontFamily: 'JetBrains Mono, monospace' }}>{hex}</span>
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
          <div style={{ overflowX: 'auto', border: '1px solid #e2e8f0', borderRadius: '12px' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px', textAlign: 'left' }}>
              <thead>
                <tr style={{ background: '#f8fafc', borderBottom: '2px solid #e2e8f0' }}>
                  <th style={{ padding: '12px 14px', color: '#64748b', fontWeight: 700 }}>Category Name</th>
                  <th style={{ padding: '12px 14px', color: '#64748b', fontWeight: 700 }}>Total Items</th>
                  <th style={{ padding: '12px 14px', color: '#64748b', fontWeight: 700 }}>Approved Count</th>
                  <th style={{ padding: '12px 14px', color: '#64748b', fontWeight: 700 }}>Approval Rate (%)</th>
                  <th style={{ padding: '12px 14px', color: '#64748b', fontWeight: 700 }}>Avg &Delta;E</th>
                  <th style={{ padding: '12px 14px', color: '#64748b', fontWeight: 700 }}>Avg Score</th>
                </tr>
              </thead>
              <tbody>
                {categoryBreakdown.map((cat: any, idx: number) => (
                  <tr key={idx} style={{ borderBottom: '1px solid #f1f5f9' }}>
                    <td style={{ padding: '12px 14px', fontWeight: 600, color: '#0f172a' }}>{cat.categoryName}</td>
                    <td style={{ padding: '12px 14px' }}>{cat.total}</td>
                    <td style={{ padding: '12px 14px', color: '#15803d', fontWeight: 600 }}>{cat.approvedCount}</td>
                    <td style={{ padding: '12px 14px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <div style={{ width: '60px', height: '6px', background: '#e2e8f0', borderRadius: '3px', overflow: 'hidden' }}>
                          <div style={{ width: `${cat.approvedPercentage}%`, height: '100%', background: '#10b981' }} />
                        </div>
                        <span>{cat.approvedPercentage}%</span>
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
          color: '#e2e8f0',
          padding: '20px',
          borderRadius: '12px',
          fontFamily: 'JetBrains Mono, monospace',
          fontSize: '12px',
          lineHeight: 1.5,
          maxHeight: '500px',
          overflowY: 'auto'
        }}>
          {JSON.stringify(resultData, null, 2)}
        </pre>
      )}
    </div>
  );
};
