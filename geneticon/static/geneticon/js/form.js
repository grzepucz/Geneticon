const SELECTION_TYPE_ID = 'id_selection_type'

/**
 * fix of course
 * @param event
 */
const changeVisibility = (event) => {
    if (document.getElementById(SELECTION_TYPE_ID).value !== 'BEST') {
        document.getElementById('id_selection_settings').style.display = 'none';
        console.log(document.getElementsByTagName(`label[for=${SELECTION_TYPE_ID}]`));
        for (let element in document.getElementsByTagName(`label[for=${SELECTION_TYPE_ID}]`)) {
            element.style.display = 'none';
        }
    } else {
        document.getElementById('id_selection_settings').style.display = 'flex';
        for (let element in document.getElementsByTagName(`label[for=${SELECTION_TYPE_ID}]`)) {
            element.style.display = 'flex';
        }
    }
};

document.getElementById(SELECTION_TYPE_ID).addEventListener('change', changeVisibility);

