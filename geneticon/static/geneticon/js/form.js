const validateSettingsInput = () => {
    try {
        return JSON.parse($('#id_selection_settings')[0].value);
    } catch (error) {
        return false;
    }
}

$('.configuration__submit')[0].addEventListener('click', (event) => {
    window.loadingLayer('on');
    if (!validateSettingsInput()) {
        event.preventDefault();
        window.loadingLayer('off');
        window.infoLayer('Settings input value is not in JSON format', 5000);
    }
})