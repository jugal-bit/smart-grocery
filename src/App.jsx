import React, { useState, useRef } from 'react';

// WCAG Contrast Helper
const getContrastTextColor = (shade) => {
    const r = Math.round(230 - (shade * 230));
    const g = Math.round(240 - (shade * 190));
    const b = Math.round(255 - (shade * 105));
    
    const rs = r / 255, gs = g / 255, bs = b / 255;
    const R = rs <= 0.03928 ? rs / 12.92 : Math.pow(((rs + 0.055) / 1.055), 2.4);
    const G = gs <= 0.03928 ? gs / 12.92 : Math.pow(((gs + 0.055) / 1.055), 2.4);
    const B = bs <= 0.03928 ? bs / 12.92 : Math.pow(((bs + 0.055) / 1.055), 2.4);
    const luminance = 0.2126 * R + 0.7152 * G + 0.0722 * B;
    
    return luminance > 0.179 ? '#000000' : '#FFFFFF';
};

const getAisleColor = (aisle) => {
    const colors = {
        produce: '#4ade80',  
        dairy: '#fef08a',    
        bakery: '#fdba74',   
        frozen: '#93c5fd',   
        household: '#d8b4fe' 
    };
    return colors[aisle] || '#e5e7eb';
};

export default function App() {
    const [email, setEmail] = useState('');
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [error, setError] = useState('');
    
    const [input, setInput] = useState('');
    const [items, setItems] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const inputRef = useRef(null);

    const handleLogin = (e) => {
        e.preventDefault();
        if (email.trim().endsWith('@petasight.com')) {
            setIsAuthenticated(true);
            setError('');
        } else {
            setError('Access restricted to @petasight.com emails only.');
        }
    };

    const handleAddItem = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        const currentItem = input.trim();
        setInput('');
        setIsLoading(true);

        try {
            const res = await fetch('/api/classify', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ item: currentItem })
            });
            
            if (!res.ok) throw new Error('API Error');
            const data = await res.json();
            
            setItems(prev => [...prev, { text: currentItem, ...data }]);
        } catch (err) {
            console.error("Classification failed", err);
        } finally {
            setIsLoading(false);
            inputRef.current?.focus(); 
        }
    };

    if (!isAuthenticated) {
        return (
            <div style={{ padding: '2rem', maxWidth: '400px', margin: '0 auto', fontFamily: 'system-ui, sans-serif' }}>
                <h2>Petasight Login</h2>
                <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    <input 
                        type="email" 
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="yourname@petasight.com"
                        style={{ padding: '0.75rem', borderRadius: '4px', border: '1px solid #ccc' }}
                        required
                    />
                    <button type="submit" style={{ padding: '0.75rem', background: '#000', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                        Enter App
                    </button>
                </form>
                {error && <p style={{ color: 'red', marginTop: '1rem' }}>{error}</p>}
            </div>
        );
    }

    return (
        <div style={{ padding: '2rem', maxWidth: '600px', margin: '0 auto', fontFamily: 'system-ui, sans-serif' }}>
            <h2>Smart Grocery List</h2>
            <form onSubmit={handleAddItem} style={{ display: 'flex', gap: '1rem', marginBottom: '2rem' }}>
                <input 
                    ref={inputRef}
                    type="text" 
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="E.g., 2 kg rice, frozen pizza..."
                    style={{ flex: 1, padding: '0.75rem', borderRadius: '4px', border: '1px solid #ccc' }}
                    disabled={isLoading}
                    aria-label="Grocery item input"
                />
                <button type="submit" disabled={isLoading} aria-label="Add item" style={{ padding: '0.75rem 1.5rem', background: '#000', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                    {isLoading ? '...' : 'Add'}
                </button>
            </form>

            <ul style={{ listStyle: 'none', padding: 0 }} aria-live="polite">
                {items.map((item, idx) => {
                    let bgColor = '#e5e7eb';
                    let textColor = '#000000';

                    if (item.rule === 1) {
                        const r = Math.round(230 - (item.shade * 230));
                        const g = Math.round(240 - (item.shade * 190));
                        const b = Math.round(255 - (item.shade * 105));
                        bgColor = `rgb(${r}, ${g}, ${b})`;
                        textColor = getContrastTextColor(item.shade);
                    } else if (item.rule === 2) {
                        bgColor = '#9ca3af'; 
                    } else if (item.rule === 3) {
                        bgColor = getAisleColor(item.tag);
                    }

                    return (
                        <li key={idx} style={{ padding: '1rem', borderBottom: '1px solid #eee', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }} tabIndex="0">
                            <span style={{ fontSize: '1.1rem' }}>{item.text}</span>
                            <span style={{ 
                                backgroundColor: bgColor, 
                                color: textColor, 
                                padding: '0.25rem 0.75rem', 
                                borderRadius: '9999px',
                                fontSize: '0.875rem',
                                fontWeight: 'bold',
                                textTransform: 'capitalize'
                            }}>
                                {item.tag}
                            </span>
                        </li>
                    );
                })}
            </ul>
        </div>
    );
}