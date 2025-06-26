import { StrictMode} from 'react'
import { createRoot } from 'react-dom/client'
import {BrowserRouter, Route,Routes} from "react-router-dom";
import LoginPage from "./Pages/LoginPage.jsx"
import HomePage from "./Pages/HomePage.jsx"
import LibraryPage from "./Pages/LibraryPage.jsx"
import ChatPage from './Pages/ChatPage.jsx'
import ChatHistoryPage from './Pages/ChatHistoryPage.jsx'
import ProtectedRoutes from './Pages/Components/ProtectedRoutes.jsx'
import DocumentViewerPage from './Pages/DocumentViewerPage.jsx'
import { AuthProvider } from './Pages/Components/AuthContext.jsx';
import "./main.css"

//Add Project Viewer Page
// Make the taking of data so that from backend we get if email is verified and the link of the user picture
// Position the arcai image and the user menu and hide the overflown content arc-ai and change the color of the toggle button

/**
 * Main.jsx is the main file that is used to render the app.
 * To Run the frontend go to the VIEW folder in the terminal and run "npm run dev"
 */
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AuthProvider>
      <BrowserRouter>
          <Routes>
            <Route path="/" element={<LoginPage />} />

            <Route element = {<ProtectedRoutes/>}>
            <Route path= "/home" element={<HomePage />} />
            <Route path = "/home/library" element = {<LibraryPage/>}/>
            <Route path = "/home/library/document-viewer" element = {<DocumentViewerPage/>}/>
            <Route path = "/home/chat-chatbot" element = {<ChatPage/>}/>
            <Route path = "/home/chat-history" element = {<ChatHistoryPage/>}/>
            </Route>

          </Routes>
      </BrowserRouter>
    </AuthProvider>
  </StrictMode>,
)
