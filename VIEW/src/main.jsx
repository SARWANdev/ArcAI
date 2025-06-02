import { StrictMode} from 'react'
import { createRoot } from 'react-dom/client'
import {BrowserRouter, Route,Routes} from "react-router-dom";
import {GoogleOAuthProvider} from "@react-oauth/google";
import GuestHomePage from "./Pages/GuestHomePage.jsx"
import HomePage from "./Pages/HomePage.jsx"
import LibraryPage from "./Pages/LibraryPage.jsx"
import ChatPage from './Pages/ChatPage.jsx'
import ChatHistoryPage from './Pages/ChatHistoryPage.jsx'
import ProtectedRoutes from './Pages/Components/ProtectedRoutes.jsx'
import DocumentViewerPage from './Pages/DocumentViewerPage.jsx'

// If the user is not logged in, set the ifLogged to false
if (!localStorage.getItem("ifLogged")) {
    localStorage.setItem("ifLogged", "false"); 
}


/**
 * Main.jsx is the main file that is used to render the app.
 * To Run the frontend go to the VIEW folder in the terminal and run "npm run dev"
 */
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <GoogleOAuthProvider clientId={import.meta.env.VITE_GOOGLE_CLIENT_ID}>
    <BrowserRouter>
        <Routes>
          <Route path="/" element={<GuestHomePage />} />

          <Route element = {<ProtectedRoutes/>}>
          <Route path= "/workspace" element={<HomePage />} />
          <Route path = "/workspace/library" element = {<LibraryPage/>}/>
          <Route path = "/workspace/document-viewer" element = {<DocumentViewerPage/>}/>
          <Route path = "/workspace/chat-chatbot" element = {<ChatPage/>}/>
          <Route path = "/workspace/chat-history" element = {<ChatHistoryPage/>}/>
          </Route>

        </Routes>
    </BrowserRouter>
    </GoogleOAuthProvider>
  </StrictMode>,
)
