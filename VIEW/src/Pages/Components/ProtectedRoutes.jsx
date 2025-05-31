import { Navigate, Outlet } from "react-router-dom";
/**
 * ProtectedRoutes is the component that is used to protect the routes.
 * @returns {JSX} - The React component for the protected routes.
 */
function ProtectedRoutes() {
    const user = localStorage.getItem("ifLogged");
    return user == "true" ? <Outlet/> : <Navigate to = "/"/>
}
export default ProtectedRoutes