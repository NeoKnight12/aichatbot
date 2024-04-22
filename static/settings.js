document.addEventListener('DOMContentLoaded', function () {
    // Function to apply settings
    function applySettings(settings) {
        // Apply font color
        document.body.style.color = settings['font-color'];
        
        // Apply font size
        document.body.style.fontSize = settings['font-size'];
        
        // Apply background color
        document.body.style.backgroundColor = settings['background-color'];
        
        // Apply font family
        document.body.style.fontFamily = settings['font-family'];
    }

    // Function to save settings to localStorage
    function saveSettingsToStorage(settings) {
        localStorage.setItem('settings', JSON.stringify(settings));
    }

    // Function to load settings from localStorage
    function loadSettingsFromStorage() {
        const settingsJson = localStorage.getItem('settings');
        if (settingsJson) {
            return JSON.parse(settingsJson);
        } else {
            // Return default settings if not found in storage
            return {
                'font-color': '#000000',
                'font-size': '16px',
                'background-color': '#ffffff',
                'font-family': 'Arial, sans-serif'
            };
        }
    }

    // Retrieve settings from localStorage or use default settings
    const settings = loadSettingsFromStorage();

    // Apply settings when the page loads
    applySettings(settings);

    // Listen for form submission
    document.getElementById('settings-form').addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent form submission
        
        // Get form data
        const formData = new FormData(event.target);
        
        // Convert form data to JSON
        const updatedSettings = {
            'font-color': formData.get('font-color'),
            'font-size': formData.get('font-size'),
            'background-color': formData.get('background-color'),
            'font-family': formData.get('font-family')
        };

        // Apply settings
        applySettings(updatedSettings);

        // Save updated settings to localStorage
        saveSettingsToStorage(updatedSettings);
    });
});
