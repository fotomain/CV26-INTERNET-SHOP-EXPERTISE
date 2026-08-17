import React from 'react';
import { Globe } from 'lucide-react';
import { SUPPORTED_COUNTRIES } from '../constants/config';

interface CountrySelectorProps {
  selectedCountry: string;
  onChangeCountry: (countryName: string) => void;
}

export const CountrySelector: React.FC<CountrySelectorProps> = ({
  selectedCountry,
  onChangeCountry,
}) => {
  const current = SUPPORTED_COUNTRIES.find((c) => c.name === selectedCountry) || SUPPORTED_COUNTRIES[0];

  return (
    <div style={{
      background: '#ffffff',
      borderRadius: '16px',
      border: '1px solid #e2e8f0',
      padding: '24px',
      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)',
      display: 'flex',
      flexDirection: 'column',
      gap: '12px'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Globe size={18} color="#0284c7" />
          <h2 style={{ fontSize: '16px', fontWeight: 700, color: '#0f172a', margin: 0 }}>
            Target Country Market Lookbook
          </h2>
        </div>
        <span style={{
          background: '#f0fdf4',
          color: '#15803d',
          border: '1px solid #bbf7d0',
          fontSize: '11px',
          fontWeight: 700,
          padding: '2px 8px',
          borderRadius: '999px'
        }}>
          ISO: {current.code}
        </span>
      </div>

      <p style={{ fontSize: '13px', color: '#64748b', margin: 0 }}>
        Select the target country to evaluate consumer color preferences against 3 reference fashion palettes.
      </p>

      <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginTop: '4px' }}>
        <div style={{
          fontSize: '28px',
          background: '#f8fafc',
          padding: '4px 10px',
          borderRadius: '8px',
          border: '1px solid #e2e8f0'
        }}>
          {current.flag}
        </div>
        <select
          value={selectedCountry}
          onChange={(e) => onChangeCountry(e.target.value)}
          style={{
            flex: 1,
            padding: '12px 16px',
            borderRadius: '10px',
            border: '1px solid #cbd5e1',
            background: '#ffffff',
            fontSize: '14px',
            fontWeight: 600,
            color: '#0f172a',
            cursor: 'pointer',
            outline: 'none'
          }}
        >
          {SUPPORTED_COUNTRIES.map((c) => (
            <option key={c.code} value={c.name}>
              {c.flag} {c.name} ({c.code})
            </option>
          ))}
        </select>
      </div>
    </div>
  );
};
