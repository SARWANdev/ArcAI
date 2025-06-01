import "./SettingsButton.css"
export default function SettingsButton(){
    return(
        <div className="settings-button">
            <button className="settings-button-button">
                <img src="../../../images/settings.png" alt="settings" className="settings-button-image"/>
            </button>
        </div>
    )
}