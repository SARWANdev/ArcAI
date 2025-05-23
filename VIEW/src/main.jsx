import { StrictMode} from 'react'
import { createRoot } from 'react-dom/client'
import GuestHomePage from "./Pages/GuestHomePage.jsx"
import HomePage from "./Pages/HomePage.jsx"
import LibraryPage from "./Pages/LibraryPage.jsx"
import ChatPage from './Pages/ChatPage.jsx'
import {BrowserRouter, Route,Routes} from "react-router-dom";
import {GoogleOAuthProvider} from "@react-oauth/google";
import ProtectedRoutes from './Pages/Components/ProtectedRoutes.jsx'

// If the user is not logged in, set the ifLogged to false
if (!localStorage.getItem("ifLogged")) {
    localStorage.setItem("ifLogged", "false"); 
}
//TODO: When the side bar is clicked, accordingly change the size of the container
/**
 * Main.jsx is the main file that is used to render the app.
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
          <Route path = "/workspace/chat" element = {<ChatPage/>}/>
          </Route>

        </Routes>
    </BrowserRouter>
    </GoogleOAuthProvider>
  </StrictMode>,
)
