const HIDDEN_CLASS = 'hidden';

window.infoLayer = (message, timeout, callback) => {
    const MESSAGE_CLASS = 'info-layer__message';
    const LAYER_CLASS = 'info-layer';

    $(`.${MESSAGE_CLASS}`).text(message);
    $(`.${LAYER_CLASS}`).removeClass(HIDDEN_CLASS)

    if (typeof callback === 'function') {
        callback();
    }

    setTimeout(() => {
        $(`.${LAYER_CLASS}`).addClass(HIDDEN_CLASS);
    }, timeout);
}

window.loadingLayer = (toggle, timeout, callback) => {
    const LAYER_CLASS = 'loading-layer';

    if (toggle === 'on') {
        $(`.${LAYER_CLASS}`).removeClass(HIDDEN_CLASS)

        if (timeout) {
            setTimeout(() => {
                $(`.${LAYER_CLASS}`).addClass(HIDDEN_CLASS);
            }, timeout);
        }
    }

    if (toggle === 'off') {
        $(`.${LAYER_CLASS}`).addClass(HIDDEN_CLASS)
    }

    if (typeof callback === 'function') {
        callback();
    }
}