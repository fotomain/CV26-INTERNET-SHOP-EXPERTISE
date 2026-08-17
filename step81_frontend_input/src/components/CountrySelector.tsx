import React from 'react';
import { Globe, MapPin, Compass } from 'lucide-react';
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
      borderRadius: '20px',
      border: '2px solid #fed7aa',
      padding: '24px',
      boxShadow: '0 8px 24px -4px rgba(245, 158, 11, 0.06)',
      display: 'flex',
      flexDirection: 'column',
      gap: '14px',
      position: 'relative',
      overflow: 'hidden'
    }}>
      {/* Decorative top amber bar */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        height: '5px',
        background: 'linear-gradient(135deg, #f59e0b 0%, #ea580c 100%)'
      }} />

      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: '4px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Compass size={18} color="#ea580c" />
          <h2 style={{ fontSize: '16px', fontWeight: 800, color: '#0f172a', letterSpacing: '-0.02em', margin: 0 }}>
            Target Country Market Lookbook
          </h2>
        </div>
        <span style={{
          background: '#fef3c7',
          color: '#b45309',
          border: '1.5px solid #fde68a',
          fontSize: '11px',
          fontWeight: 800,
          padding: '2px 9px',
          borderRadius: '999px'
        }}>
          ISO: {current.code}
        </span>
      </div>

      <p style={{ fontSize: '13px', color: '#64748b', margin: 0 }}>
        Select target country to evaluate consumer color preferences against 3 reference fashion palettes.
      </p>

      <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginTop: '4px' }}>
        <div style={{
          fontSize: '28px',
          background: 'linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%)',
          padding: '8px 14px',
          borderRadius: '12px',
          border: '1.5px solid #fde68a',
          boxShadow: '0 2px 8px rgba(245, 158, 11, 0.15)',
          lineHeight: 1
        }}>
          {current.flag}
        </div>
        <select
          value={selectedCountry}
          onChange={(e) => onChangeCountry(e.target.value)}
          style={{
            flex: 1,
            padding: '12px 16px',
            borderRadius: '12px',
            border: '2px solid #fed7aa',
            background: '#ffffff',
            fontSize: '14px',
            fontWeight: 700,
            color: '#0f172a',
            cursor: 'pointer',
            outline: 'none',
            boxShadow: '0 2px 6px rgba(0, 0, 0, 0.04)'
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
