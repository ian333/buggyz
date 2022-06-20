import { createRoot } from 'react-dom/client';
import React from "react"
import App from "./App"
import "bulma/css/bulma.min.css"
import { UserProvider } from './context/UserContext';

const root = createRoot(document.getElementById('root'));
root.render(<UserProvider>
    <App/>
    </UserProvider>);
