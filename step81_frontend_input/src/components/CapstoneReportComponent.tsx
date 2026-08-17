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
  Clock,
  Layers,
  Palette,
  Search,
  BarChart3,
  Award,
  Sparkles,
  Download,
  CheckCircle2
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
      border: '1px solid rgba(0, 0, 0, 0.08)',
      boxShadow: '0 1px 3px rgba(0, 0, 0, 0.02), 0 12px 36px -4px rgba(0, 0, 0, 0.06)',
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
        borderBottom: '1px solid #f4f4f5',
        paddingBottom: '20px'
      }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{
              background: '#09090b',
              color: '#ffffff',
              padding: '3px 8px',
              borderRadius: '6px',
              fontSize: '11px',
              fontWeight: 700,
              display: 'flex',
              alignItems: 'center',
              gap: '4px'
            }}>
              <Sparkles size={12} color="#fbbf24" />
              DSS VERIFIED
            </span>
            <h2 style={{ fontSize: '18px', fontWeight: 800, color: '#09090b', letterSpacing: '-0.03em', margin: 0 }}>
              Capstone Executive Decision Report
            </h2>
          </div>
          <p style={{ fontSize: '12px', color: '#71717a', margin: '4px 0 0 0' }}>
            Target Country: <strong>{targetCountry?.name} ({targetCountry?.isoCode})</strong> &bull; Execution Duration: {metadata?.executionDuration || '00:00'}
          </p>
        </div>

        <div style={{ display: 'flex', gap: '8px' }}>
          <button
            onClick={handleExportJSON}
            style={{
              background: '#ffffff',
              border: '1px solid #d4d4d8',
              color: '#18181b',
              padding: '6px 14px',
              borderRadius: '8px',
              fontSize: '12px',
              fontWeight: 600,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              boxShadow: '0 1px 2px rgba(0,0,0,0.04)'
            }}
          >
            <Download size={14} />
            Export resultDataJSON
          </button>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(190px, 1fr))',
        gap: '14px'
      }}>
        <div style={{
          background: '#fafafa',
          border: '1px solid #e4e4e7',
          borderRadius: '12px',
          padding: '16px 18px'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', color: '#71717a', fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.04em' }}>
            <span>Catalog Items</span>
            <Layers size={15} color="#71717a" />
          </div>
          <div style={{ fontSize: '26px', fontWeight: 800, color: '#09090b', letterSpacing: '-0.03em', marginTop: '4px' }}>
            {kpis.totalItems}
          </div>
          <div style={{ fontSize: '11px', color: '#a1a1aa', marginTop: '2px' }}>
            Candidate SKUs evaluated
          </div>
        </div>

        <div style={{
          background: '#fafafa',
          border: '1px solid #e4e4e7',
          borderRadius: '12px',
          padding: '16px 18px'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', color: '#16a34a', fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.04em' }}>
            <span>Approved for Market</span>
            <CheckCircle2 size={15} color="#16a34a" />
          </div>
          <div style={{ fontSize: '26px', fontWeight: 800, color: '#09090b', letterSpacing: '-0.03em', marginTop: '4px' }}>
            {kpis.goodForMarketingPct}%
          </div>
          <div style={{ fontSize: '11px', color: '#71717a', marginTop: '2px' }}>
            {kpis.goodForMarketingCount} of {kpis.totalItems} match {targetCountry?.name}
          </div>
        </div>

        <div style={{
          background: '#fafafa',
          border: '1px solid #e4e4e7',
          borderRadius: '12px',
          padding: '16px 18px'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', color: '#0284c7', fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.04em' }}>
            <span>Compatibility Score</span>
            <TrendingUp size={15} color="#0284c7" />
          </div>
          <div style={{ fontSize: '26px', fontWeight: 800, color: '#09090b', letterSpacing: '-0.03em', marginTop: '4px' }}>
            {kpis.averageCompatibilityScore}
          </div>
          <div style={{ fontSize: '11px', color: '#71717a', marginTop: '2px' }}>
            Avg &Delta;E: {kpis.averageDeltaEDistance} (&le; 13.5 target)
          </div>
        </div>

        <div style={{
          background: '#fafafa',
          border: '1px solid #e4e4e7',
          borderRadius: '12px',
          padding: '16px 18px'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', color: '#7c3aed', fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.04em' }}>
            <span>Quality Ready</span>
            <Award size={15} color="#7c3aed" />
          </div>
          <div style={{ fontSize: '26px', fontWeight: 800, color: '#09090b', letterSpacing: '-0.03em', marginTop: '4px' }}>
            {kpis.readyToSalePct}%
          </div>
          <div style={{ fontSize: '11px', color: '#71717a', marginTop: '2px' }}>
            {kpis.readyToSaleCount} pass title &amp; image audit
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div style={{ display: 'flex', gap: '6px', borderBottom: '1px solid #e4e4e7', paddingBottom: '8px' }}>
        <button
          onClick={() => setActiveTab('catalog')}
          style={{
            background: activeTab === 'catalog' ? '#09090b' : 'transparent',
            color: activeTab === 'catalog' ? '#ffffff' : '#71717a',
            border: 'none',
            padding: '6px 14px',
            borderRadius: '8px',
            fontSize: '12px',
            fontWeight: 700,
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            transition: 'all 0.15s ease'
          }}
        >
          <Layers size={13} />
          Candidate Products ({filteredProducts.length})
        </button>

        <button
          onClick={() => setActiveTab('palettes')}
          style={{
            background: activeTab === 'palettes' ? '#09090b' : 'transparent',
            color: activeTab === 'palettes' ? '#ffffff' : '#71717a',
            border: 'none',
            padding: '6px 14px',
            borderRadius: '8px',
            fontSize: '12px',
            fontWeight: 700,
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            transition: 'all 0.15s ease'
          }}
        >
          <Palette size={13} />
          Target Market 3-Palettes
        </button>

        <button
          onClick={() => setActiveTab('categories')}
          style={{
            background: activeTab === 'categories' ? '#09090b' : 'transparent',
            color: activeTab === 'categories' ? '#ffffff' : '#71717a',
            border: 'none',
            padding: '6px 14px',
            borderRadius: '8px',
            fontSize: '12px',
            fontWeight: 700,
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            transition: 'all 0.15s ease'
          }}
        >
          <BarChart3 size={13} />
          Category Breakdown
        </button>

        <button
          onClick={() => setActiveTab('json')}
          style={{
            background: activeTab === 'json' ? '#09090b' : 'transparent',
            color: activeTab === 'json' ? '#ffffff' : '#71717a',
            border: 'none',
            padding: '6px 14px',
            borderRadius: '8px',
            fontSize: '12px',
            fontWeight: 700,
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            transition: 'all 0.15s ease'
          }}
        >
          Raw JSON Log
        </button>
      </div>

      {/* TAB 1: Products Catalog Table */}
      {activeTab === 'catalog' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          {/* Filters Bar */}
          <div style={{
            display: 'flex',
            gap: '10px',
            flexWrap: 'wrap',
            alignItems: 'center',
            background: '#fafafa',
            padding: '12px',
            borderRadius: '10px',
            border: '1px solid #e4e4e7'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flex: 1, minWidth: '180px', background: '#ffffff', border: '1px solid #d4d4d8', borderRadius: '8px', padding: '5px 10px' }}>
              <Search size={14} color="#a1a1aa" />
              <input
                type="text"
                placeholder="Search products..."
                value={searchQuery}
                onChange={(e) => dispatch(setSearchQuery(e.target.value))}
                style={{ border: 'none', outline: 'none', width: '100%', fontSize: '12px', color: '#09090b' }}
              />
            </div>

            <select
              value={selectedCategoryFilter}
              onChange={(e) => dispatch(setCategoryFilter(e.target.value))}
              style={{ padding: '6px 10px', borderRadius: '8px', border: '1px solid #d4d4d8', background: '#ffffff', fontSize: '12px', color: '#09090b' }}
            >
              <option value="ALL">All Categories</option>
              {categoriesList.map((cat: any) => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>

            <select
              value={selectedApprovalFilter}
              onChange={(e) => dispatch(setApprovalFilter(e.target.value))}
              style={{ padding: '6px 10px', borderRadius: '8px', border: '1px solid #d4d4d8', background: '#ffffff', fontSize: '12px', color: '#09090b' }}
            >
              <option value="ALL">All Decisions</option>
              <option value="APPROVED">Approved Only (Good for Marketing)</option>
              <option value="EXCLUDED">Non-Priority Only</option>
            </select>

            <select
              value={selectedTierFilter}
              onChange={(e) => dispatch(setTierFilter(e.target.value))}
              style={{ padding: '6px 10px', borderRadius: '8px', border: '1px solid #d4d4d8', background: '#ffffff', fontSize: '12px', color: '#09090b' }}
            >
              <option value="ALL">All Tiers</option>
              <option value="Tier 1">Tier 1 (Prime Candidates)</option>
              <option value="Tier 2">Tier 2 (Standard Candidates)</option>
              <option value="Tier 3">Tier 3 (Non-Priority)</option>
            </select>
          </div>

          {/* Table */}
          <div style={{ overflowX: 'auto', border: '1px solid #e4e4e7', borderRadius: '10px' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '12px', textAlign: 'left' }}>
              <thead>
                <tr style={{ background: '#fafafa', borderBottom: '1px solid #e4e4e7' }}>
                  <th style={{ padding: '10px 12px', color: '#71717a', fontWeight: 700 }}>ID</th>
                  <th style={{ padding: '10px 12px', color: '#71717a', fontWeight: 700 }}>Product Name</th>
                  <th style={{ padding: '10px 12px', color: '#71717a', fontWeight: 700 }}>Category</th>
                  <th style={{ padding: '10px 12px', color: '#71717a', fontWeight: 700 }}>Extracted Palette</th>
                  <th style={{ padding: '10px 12px', color: '#71717a', fontWeight: 700 }}>Target Match</th>
                  <th style={{ padding: '10px 12px', color: '#71717a', fontWeight: 700 }}>&Delta;E / Score</th>
                  <th style={{ padding: '10px 12px', color: '#71717a', fontWeight: 700 }}>Decision</th>
                  <th style={{ padding: '10px 12px', color: '#71717a', fontWeight: 700 }}>Campaign Tier</th>
                </tr>
              </thead>
              <tbody>
                {filteredProducts.map((p: any) => (
                  <tr key={p.itemId} style={{ borderBottom: '1px solid #f4f4f5', background: p.isGoodForMarketing ? '#ffffff' : '#fafafa' }}>
                    <td style={{ padding: '10px 12px', fontFamily: 'JetBrains Mono, monospace', color: '#71717a' }}>
                      #{p.itemId}
                    </td>
                    <td style={{ padding: '10px 12px', fontWeight: 600, color: '#09090b' }}>
                      {p.name}
                    </td>
                    <td style={{ padding: '10px 12px', color: '#52525b' }}>
                      <span style={{ background: '#f4f4f5', padding: '2px 6px', borderRadius: '4px', fontSize: '11px' }}>
                        {p.categoryName}
                      </span>
                    </td>
                    <td style={{ padding: '10px 12px' }}>
                      <div style={{ display: 'flex', gap: '3px' }}>
                        {(p.palette || []).map((hex: string, idx: number) => (
                          <span
                            key={idx}
                            title={hex}
                            style={{
                              display: 'inline-block',
                              width: '14px',
                              height: '14px',
                              borderRadius: '3px',
                              backgroundColor: hex,
                              border: '1px solid rgba(0,0,0,0.1)'
                            }}
                          />
                        ))}
                      </div>
                    </td>
                    <td style={{ padding: '10px 12px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                        <span
                          style={{
                            display: 'inline-block',
                            width: '12px',
                            height: '12px',
                            borderRadius: '3px',
                            backgroundColor: p.matchedColorHex || '#808080'
                          }}
                        />
                        <span style={{ fontSize: '11px', color: '#52525b' }}>
                          {p.matchedPaletteTheme?.split('(')[0] || 'Theme'}
                        </span>
                      </div>
                    </td>
                    <td style={{ padding: '10px 12px', fontFamily: 'JetBrains Mono, monospace' }}>
                      <strong>{p.deltaEDistance?.toFixed(1)}</strong>
                      <span style={{ fontSize: '11px', color: '#71717a', marginLeft: '4px' }}>
                        ({p.compatibilityScore?.toFixed(2)})
                      </span>
                    </td>
                    <td style={{ padding: '10px 12px' }}>
                      {p.isGoodForMarketing ? (
                        <span style={{
                          background: '#f0fdf4',
                          color: '#166534',
                          border: '1px solid #bbf7d0',
                          padding: '2px 7px',
                          borderRadius: '6px',
                          fontSize: '11px',
                          fontWeight: 700,
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '3px'
                        }}>
                          <Check size={11} /> Approved
                        </span>
                      ) : (
                        <span style={{
                          background: '#fafafa',
                          color: '#71717a',
                          border: '1px solid #e4e4e7',
                          padding: '2px 7px',
                          borderRadius: '6px',
                          fontSize: '11px',
                          fontWeight: 600,
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '3px'
                        }}>
                          <X size={11} /> Non-Priority
                        </span>
                      )}
                    </td>
                    <td style={{ padding: '10px 12px' }}>
                      <span style={{
                        fontSize: '11px',
                        color: p.priorityTier?.includes('Tier 1') ? '#b45309' : p.priorityTier?.includes('Tier 2') ? '#0284c7' : '#71717a',
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
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div style={{ background: '#fafafa', padding: '14px', borderRadius: '10px', border: '1px solid #e4e4e7' }}>
            <h3 style={{ fontSize: '14px', fontWeight: 700, color: '#09090b', margin: 0 }}>
              🇺🇸 {targetCountry?.name} Multi-Palette Style DNA (NUMBER_PALLETS_OF_NEWCOUNTRY_REQUIRED = 3)
            </h3>
            <p style={{ fontSize: '12px', color: '#71717a', margin: '2px 0 0 0' }}>
              Extracted from authentic lookbook images via YOLOv8 and OpenCV background exclusion.
            </p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '14px' }}>
            {/* Men Palettes */}
            <div style={{ border: '1px solid #e4e4e7', borderRadius: '10px', padding: '14px', background: '#ffffff' }}>
              <h4 style={{ fontSize: '13px', fontWeight: 700, color: '#09090b', marginBottom: '10px' }}>
                👔 Men's Collection Palettes
              </h4>
              {(targetCountry?.manPalettes || []).map((pal: string[], idx: number) => (
                <div key={idx} style={{ marginBottom: '12px' }}>
                  <div style={{ fontSize: '11px', fontWeight: 600, color: '#71717a', marginBottom: '4px' }}>
                    {targetCountry?.paletteThemes?.[idx] || `Palette ${idx+1}`}
                  </div>
                  <div style={{ display: 'flex', gap: '6px' }}>
                    {pal.map((hex, i) => (
                      <div key={i} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '3px' }}>
                        <div style={{ width: '32px', height: '32px', borderRadius: '6px', backgroundColor: hex, border: '1px solid rgba(0,0,0,0.1)' }} />
                        <span style={{ fontSize: '9px', color: '#71717a', fontFamily: 'JetBrains Mono, monospace' }}>{hex}</span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            {/* Women Palettes */}
            <div style={{ border: '1px solid #e4e4e7', borderRadius: '10px', padding: '14px', background: '#ffffff' }}>
              <h4 style={{ fontSize: '13px', fontWeight: 700, color: '#09090b', marginBottom: '10px' }}>
                👗 Women's Collection Palettes
              </h4>
              {(targetCountry?.womanPalettes || []).map((pal: string[], idx: number) => (
                <div key={idx} style={{ marginBottom: '12px' }}>
                  <div style={{ fontSize: '11px', fontWeight: 600, color: '#71717a', marginBottom: '4px' }}>
                    {targetCountry?.paletteThemes?.[idx] || `Palette ${idx+1}`}
                  </div>
                  <div style={{ display: 'flex', gap: '6px' }}>
                    {pal.map((hex, i) => (
                      <div key={i} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '3px' }}>
                        <div style={{ width: '32px', height: '32px', borderRadius: '6px', backgroundColor: hex, border: '1px solid rgba(0,0,0,0.1)' }} />
                        <span style={{ fontSize: '9px', color: '#71717a', fontFamily: 'JetBrains Mono, monospace' }}>{hex}</span>
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
        <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          <div style={{ overflowX: 'auto', border: '1px solid #e4e4e7', borderRadius: '10px' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '12px', textAlign: 'left' }}>
              <thead>
                <tr style={{ background: '#fafafa', borderBottom: '1px solid #e4e4e7' }}>
                  <th style={{ padding: '10px 12px', color: '#71717a', fontWeight: 700 }}>Category Name</th>
                  <th style={{ padding: '10px 12px', color: '#71717a', fontWeight: 700 }}>Total Items</th>
                  <th style={{ padding: '10px 12px', color: '#71717a', fontWeight: 700 }}>Approved Count</th>
                  <th style={{ padding: '10px 12px', color: '#71717a', fontWeight: 700 }}>Approval Rate (%)</th>
                  <th style={{ padding: '10px 12px', color: '#71717a', fontWeight: 700 }}>Avg &Delta;E</th>
                  <th style={{ padding: '10px 12px', color: '#71717a', fontWeight: 700 }}>Avg Score</th>
                </tr>
              </thead>
              <tbody>
                {categoryBreakdown.map((cat: any, idx: number) => (
                  <tr key={idx} style={{ borderBottom: '1px solid #f4f4f5' }}>
                    <td style={{ padding: '10px 12px', fontWeight: 600, color: '#09090b' }}>{cat.categoryName}</td>
                    <td style={{ padding: '10px 12px' }}>{cat.total}</td>
                    <td style={{ padding: '10px 12px', color: '#16a34a', fontWeight: 600 }}>{cat.approvedCount}</td>
                    <td style={{ padding: '10px 12px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                        <div style={{ width: '50px', height: '5px', background: '#e4e4e7', borderRadius: '3px', overflow: 'hidden' }}>
                          <div style={{ width: `${cat.approvedPercentage}%`, height: '100%', background: '#09090b' }} />
                        </div>
                        <span>{cat.approvedPercentage}%</span>
                      </div>
                    </td>
                    <td style={{ padding: '10px 12px', fontFamily: 'JetBrains Mono, monospace' }}>{cat.avgDeltaE}</td>
                    <td style={{ padding: '10px 12px', fontFamily: 'JetBrains Mono, monospace' }}>{cat.avgScore}</td>
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
          background: '#fafafa',
          color: '#09090b',
          border: '1px solid #e4e4e7',
          padding: '16px',
          borderRadius: '10px',
          fontFamily: 'JetBrains Mono, monospace',
          fontSize: '11px',
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
