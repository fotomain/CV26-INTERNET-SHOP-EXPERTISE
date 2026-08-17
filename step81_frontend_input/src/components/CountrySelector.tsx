import React from 'react';
import { Globe2 } from 'lucide-react';
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
      border: '1px solid rgba(0, 0, 0, 0.08)',
      padding: '24px',
      boxShadow: '0 1px 3px rgba(0, 0, 0, 0.02), 0 6px 24px -4px rgba(0, 0, 0, 0.04)',
      display: 'flex',
      flexDirection: 'column',
      gap: '12px'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Globe2 size={16} color="#09090b" />
          <h2 style={{ fontSize: '15px', fontWeight: 700, color: '#09090b', letterSpacing: '-0.02em', margin: 0 }}>
            Target Country Market Lookbook
          </h2>
        </div>
        <span style={{
          background: '#f4f4f5',
          color: '#18181b',
          border: '1px solid #e4e4e7',
          fontSize: '11px',
          fontWeight: 700,
          padding: '2px 7px',
          borderRadius: '6px'
        }}>
          ISO: {current.code}
        </span>
      </div>

      <p style={{ fontSize: '12px', color: '#71717a', margin: 0 }}>
        Select target country to evaluate consumer color preferences against 3 reference fashion palettes.
      </p>

      <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginTop: '4px' }}>
        <div style={{
          fontSize: '24px',
          background: '#fafafa',
          padding: '6px 10px',
          borderRadius: '8px',
          border: '1px solid #e4e4e7',
          lineHeight: 1
        }}>
          {current.flag}
        </div>
        <select
          value={selectedCountry}
          onChange={(e) => onChangeCountry(e.target.value)}
          style={{
            flex: 1,
            padding: '10px 14px',
            borderRadius: '10px',
            border: '1px solid #d4d4d8',
            background: '#ffffff',
            fontSize: '13px',
            fontWeight: 600,
            color: '#09090b',
            cursor: 'pointer',
            outline: 'none',
            boxShadow: '0 1px 2px rgba(0, 0, 0, 0.02)'
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
