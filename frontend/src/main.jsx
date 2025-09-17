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
import { AuthProvider } from './Pages/Components/Contexts/AuthContext.jsx';
import { ThemeProvider} from './Pages/Components/Contexts/ThemeContext.jsx';
import { SideBarProvider } from './Pages/Components/Contexts/SideBarContext.jsx';
import { ProjectsProvider } from './Pages/Components/Contexts/ProjectsContext.jsx';
import ProjectViewerPage from './Pages/ProjectViewerPage.jsx';
import "./main.css"

//Add Project Viewer Page
/**
 * Main.jsx is the main file that is used to render the app.
 * To Run the frontend go to the VIEW folder in the terminal and run "npm run dev"
 */
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AuthProvider>
      <BrowserRouter>
        <ThemeProvider>
          <SideBarProvider>
          <ProjectsProvider>
            <Routes>
              <Route path="/" element={<LoginPage />} />

              <Route element = {<ProtectedRoutes/>}>
              <Route path= "/home" element={<HomePage />} />
              <Route path = "/home/library" element = {<LibraryPage/>}/>
              <Route path = "/home/library/project/:projectId/:title" element = {<ProjectViewerPage/>}/>
              <Route path = "/home/library/document/:documentId" element = {<DocumentViewerPage/>}/>
              <Route path = "/home/chat-chatbot" element = {<ChatPage/>}/>
              <Route path = "/home/chat/:conversationId" element={<ChatPage />} />
              <Route path = "/home/chat-history" element = {<ChatHistoryPage/>}/>
              </Route>

            </Routes>
            </ProjectsProvider>
          </SideBarProvider>
        </ThemeProvider>
      </BrowserRouter>
    </AuthProvider>
  </StrictMode>,
)
