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

// If the user is not logged in, set the ifLogged to false
if (!localStorage.getItem("ifLogged")) {
    localStorage.setItem("ifLogged", "false"); 
}
//Add Project Viewer Page
/**
 * Main.jsx is the main file that is used to render the app.
 * To Run the frontend go to the VIEW folder in the terminal and run "npm run dev"
 */
createRoot(document.getElementById('root')).render(
  <StrictMode>
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
  </StrictMode>,
)
