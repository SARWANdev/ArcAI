import "./SettingsButton.css"
import PopUpBoxProjectOptions from "../PopUpBoxProjectOptions"
export default function SettingsButton(){
    return(
        <div className="settings-button">
            <button className="settings-button" title="Settings">
                <img src="../../../images/settings.png" alt="settings" className="settings-image"/>
            </button>
        </div>
        
    )
}