import React, {useState} from 'react';
import {createRoot} from 'react-dom/client';
import axios from 'axios';
import './styles.css';

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

function App(){
  const [lang,setLang]=useState('en');
  const [symptoms,setSymptoms]=useState('');
  const [result,setResult]=useState(null);
  const [loading,setLoading]=useState(false);
  const [error,setError]=useState('');

  async function triage(){
    setLoading(true); setError('');
    try{
      const {data}=await axios.post(`${API}/triage/`,{symptoms,language:lang});
      setResult(data);
    }catch(e){setError('API unavailable. Check VITE_API_URL and backend deployment.');}
    finally{setLoading(false);}
  }

  return <main>
    <header><div className="brand">🩺 Sanjivni</div><span>Emergency Coordination Network</span></header>
    <section className="hero">
      <p className="badge">AI-powered • Hindi + English • Real-time coordination</p>
      <h1>Every second matters.</h1>
      <p>AI-assisted emergency triage and capability-matched hospital coordination.</p>
    </section>
    <section className="grid">
      <div className="card">
        <h2>Emergency Triage</h2>
        <div className="lang">
          <button className={lang==='en'?'active':''} onClick={()=>setLang('en')}>English</button>
          <button className={lang==='hi'?'active':''} onClick={()=>setLang('hi')}>हिंदी</button>
        </div>
        <textarea value={symptoms} onChange={e=>setSymptoms(e.target.value)}
          placeholder={lang==='hi'?'लक्षण लिखें, जैसे: सीने में तेज दर्द और सांस लेने में कठिनाई':'Describe symptoms, e.g. severe chest pain and difficulty breathing'}
          rows="6"/>
        <button className="primary" disabled={!symptoms||loading} onClick={triage}>{loading?'Analysing…':'Get AI Triage'}</button>
        {error && <p className="error">{error}</p>}
        {result && <div className={`result ${result.priority?.toLowerCase()}`}>
          <h3>{result.priority} — {result.recommendation}</h3>
          <p>{result.reasoning}</p>
          {result.red_flags?.length>0 && <p><b>Red flags:</b> {result.red_flags.join(', ')}</p>}
          {result.nearest_hospitals?.length>0 && <ul>{result.nearest_hospitals.map(h=><li key={h.id}>{h.name} — {h.available_beds} beds available</li>)}</ul>}
        </div>}
      </div>
      <div className="card">
        <h2>Live Network</h2>
        <div className="stat"><b>&lt; 200 ms</b><span>availability lookup target</span></div>
        <div className="stat"><b>2 sec</b><span>AI triage target</span></div>
        <div className="stat"><b>3 roles</b><span>patients, hospitals, ambulances</span></div>
        <p className="note">In a real emergency, call India's emergency services (112/108) immediately.</p>
      </div>
    </section>
  </main>
}
createRoot(document.getElementById('root')).render(<App/>);
