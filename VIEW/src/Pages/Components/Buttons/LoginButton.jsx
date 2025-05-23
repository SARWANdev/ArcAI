
//For google authentication
import { useGoogleLogin } from '@react-oauth/google';
import { useNavigate } from 'react-router-dom';
import "./LoginButton.css"
/**
 * LoginButton is the component that is used to display the login button.
 * @returns {JSX} - The React component for the login button.
 */
function LoginButton() {
  const URL_GET_USER_INFO = import.meta.env.VITE_GOOGLE_URL_GET_USER_INFO;
  const URL_SEND_USER_INFO = "http://127.0.0.1:5000/logged";
  const navigate = useNavigate()
  /**
   * login is the function that is used to login the user.
   */
  const login = useGoogleLogin({
    onSuccess: async (tokenResponse) => {
      try {
        const response = await fetch(URL_GET_USER_INFO, {
          headers: {
            Authorization: `Bearer ${tokenResponse.access_token}`,
          },
        });
        const userInfo = await response.json();
        sendUserInfo(userInfo);
        navigate("/workspace");
        localStorage.setItem("ifLogged", "true");
      } catch (e) {
        console.log(`An error occurred: ${e}`);
      }
    },
    onError: (error) => console.log('Login Failed:', error),
  });

  /**
   * sendUserInfo is the function that is used to send the user info to the server.
   * @param {Object} userInfo - The user info.
   * @returns {Promise} - The promise that is used to send the user info to the server.
   */
  const sendUserInfo = async(userInfo) => {
    const data = {"given_name":userInfo.given_name, "family_name": userInfo.family_name, "email":userInfo.email}
    const options = {
      method : ["POST"],
      headers : {"Content-Type": "application/json"},
      body: JSON.stringify(data)
    }
    try {
      const response = await fetch(URL_SEND_USER_INFO, options);
      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }
      return response.json();
    }catch(e){
      console.log(e);
    }
  }
    
  
  return(
        <button className="arcai-login-button" onClick={()=> login()}>Log in</button>
    )
}
export default LoginButton