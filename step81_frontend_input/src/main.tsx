import React from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';
import { TamaguiProvider } from '@tamagui/core';
import { store } from './store';
import tamaguiConfig from './tamagui.config';
import App from './App';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Provider store={store}>
      <TamaguiProvider config={tamaguiConfig} defaultTheme="light">
        <App />
      </TamaguiProvider>
    </Provider>
  </React.StrictMode>
);
