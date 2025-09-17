import "./SettingsButton.css"
/**
 * SettingsButton is the component that is used to display the settings button.
 * @returns {JSX} - The React component for the settings button.
 */
export default function SettingsButton(){
    return(
        <div className="settings-button">
            <button className="settings-button" title="Settings">
                <img src="/images/settings.png" alt="settings" className="settings-image"/>
            </button>
        </div>
    )
}