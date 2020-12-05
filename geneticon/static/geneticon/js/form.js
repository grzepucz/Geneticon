const BINARY_REPRESENTATION = 'BINARY';
const REAL_REPRESENTATION = 'REAL';
 //
 // ('EDGE', 'Edge'),
 //        ('SINGLE', 'Single point'),
 //        ('DOUBLE', 'Double point'),
 //        ('EVEN', 'Even'),
 //        ('INDEX', 'Index change')
/*
        ('SINGLE', 'Single point'),
        ('DOUBLE', 'Double point'),
        ('TRIPLE', 'Triple point'),
        ('HOMO', 'Homogeneous'),
        ('ARITHMETIC', 'Arithmetic'),
        ('HEURISTIC', 'Heuristic'),
 */

const REAL_FIELDS = [
    'EVEN', 'INDEX', 'ARITHMETIC', 'HEURISTIC'
];

const BINARY_FIELDS = [
    'EDGE', 'SINGLE', 'DOUBLE', 'TRIPLE', 'HOMO'
];

const resetFields = () => {
    $('[id$="_type"]').each((index, element) => element.value = null);
}

const toggleRealFields = (isDisabled) => {
    REAL_FIELDS.forEach(field => {
        $(`[value=${field}]`).each((index, element) => element.disabled = isDisabled);
    });
};

const toggleBinaryFields = (isDisabled) => {
    BINARY_FIELDS.forEach(field => {
        $(`[value=${field}]`).each((index, element) => element.disabled = isDisabled);
    });
};

const toggleInversion = (isDisabled) => {
    const $inversion = $('#id_inversion_probability');

    if (isDisabled) {
        $inversion[0].disabled = true;
        $inversion[0].value = 0;
    } else {
        $inversion[0].disabled = false;
    }
}

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

$('#id_representation')[0].addEventListener('input', (event) => {
    resetFields();

    if (event.target.value === BINARY_REPRESENTATION) {
        toggleBinaryFields(false);
        toggleRealFields(true);
        toggleInversion(false);
    }

    if (event.target.value === REAL_REPRESENTATION) {
        toggleBinaryFields(true);
        toggleRealFields(false);
        toggleInversion(true);
    }
});

// Initial is real
$(document).on('ready', () => {
    resetFields();
    toggleBinaryFields(true);
    toggleInversion(true);
});