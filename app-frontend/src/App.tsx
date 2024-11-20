import React from 'react';
import { FilingSummary } from './components/FilingSummary';
import { AppContainer } from './styles/AppStyles';

const App: React.FC = () => {
  return (
    <AppContainer>
      <FilingSummary />
    </AppContainer>
  );
};

export default App;