import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { FilingSummary } from './components/FilingSummary';
import { TickerDetail } from './components/TickerDetail';
import { AppContainer } from './styles/AppStyles';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <AppContainer>
        <Routes>
          <Route path="/" element={<FilingSummary />} />
          <Route path="/:dataset/:ticker" element={<TickerDetail />} />
        </Routes>
      </AppContainer>
    </BrowserRouter>
  );
};

export default App;