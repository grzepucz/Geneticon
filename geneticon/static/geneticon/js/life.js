const header = $('.generation__header')
const next = $('.button__next');
const live = $('.button__live');

const checkEpochLimit = () => $('.property__epoch').find('.property__value')[0]?.innerText >= $('.generation').length;
const disableButtons = () => $('.manage-buttons').children().attr("disabled", true);

const addClickExpandListener = (element) => {
    let currentEpoch = $(element).parent();

    element.addEventListener('click', (event) => {
        if (currentEpoch.hasClass('generation--extended')) {
            currentEpoch.removeClass('generation--extended');
            currentEpoch.find('.generation__population').each((ind, elem) => {
                $(elem).addClass('generation__population--hidden').removeClass('generation__population');
            });
        } else {
            currentEpoch.addClass('generation--extended');
            currentEpoch.find('.generation__population--hidden').each((ind, elem) => {
                $(elem).addClass('generation__population').removeClass('generation__population--hidden');
            });
        }
    });
}

const updateResultValue = () => {
    const resultSelector = $('.life-configuration__result__value');
    const generationSelector = $('.generation').last();
    const bestKidSelector = generationSelector.find('.property').first();
    resultSelector.find('.result__name')[0].innerText = bestKidSelector.find('.property__label')[0].innerText;
    resultSelector.find('.result__genes')[0].innerHTML = bestKidSelector.find('.chromosome__gene')[0].innerText;
    resultSelector.find('.result__chromosome')[0].innerText = bestKidSelector.find('.chromosome__gene_value')[0].innerText;
    resultSelector.find('.result__genes')[1].innerHTML = bestKidSelector.find('.chromosome__gene')[1].innerText;
    resultSelector.find('.result__chromosome')[1].innerText = bestKidSelector.find('.chromosome__gene_value')[1].innerText;
    resultSelector.find('.result__value')[0].innerText = bestKidSelector.find('.function__value')[0].innerText;
}

const addManageButtonsListeners = () => {
    if (next.length) {
        next[0].addEventListener('click', (event) => {
            let manageButtons = $('.manage-buttons');
            let loader = $('.loader--hidden');
            let nextEpoch = $('.generation').length + 1;

            manageButtons.addClass('hidden');
            loader.addClass('loader').removeClass('loader--hidden');

            $.ajax({
                url: `${window.location.href.split('?')[0]}/epoch/${nextEpoch}`,
                type: 'GET',
                success: (data) => {
                    const serializer = new XMLSerializer();
                    const xmlStr = serializer.serializeToString(data);
                    const generations = $('.generations');
                    generations.append(xmlStr);
                    addClickExpandListener(generations.children().last().find('.generation__header')[0]);
                },
                error: (error) => {
                    manageButtons.removeClass('hidden');
                    loader.addClass('loader--hidden').removeClass('loader');
                },
                complete: () => {
                    updateResultValue();
                    manageButtons.removeClass('hidden');
                    loader.addClass('loader--hidden').removeClass('loader');

                    if (!checkEpochLimit()) {
                        disableButtons();
                    }
                }
            });
        });
    }

    if (live.length) {
        live[0].addEventListener('click', (event) => {
            let manageButtons = $('.manage-buttons');
            let loader = $('.loader--hidden');
            let nextEpoch = $('.generation').length + 1;
            let epochNumbers = $('.property__epoch').find('.property__value')[0]?.innerText

            manageButtons.addClass('hidden');
            loader.addClass('loader').removeClass('loader--hidden');

            if (epochNumbers) {
                const requestData = (epoch, limit) => {
                    $.ajax({
                        url:  `${window.location.href.split('?')[0]}/epoch/${epoch}`,
                        type: 'GET',
                        success: (data) => {
                            const serializer = new XMLSerializer();
                            const xmlStr = serializer.serializeToString(data);
                            const generations = $('.generations');
                            generations.append(xmlStr);
                            addClickExpandListener(generations.children().last().find('.generation__header')[0]);
                        },
                        error: (error) => {
                            manageButtons.removeClass('hidden');
                            loader.addClass('loader--hidden').removeClass('loader');
                        },
                        complete: () => {
                            updateResultValue();
                            if (epoch + 1 < limit) {
                                requestData(epoch+1, limit);
                            }
                            if (!checkEpochLimit()) {
                                manageButtons.removeClass('hidden');
                                loader.addClass('loader--hidden').removeClass('loader');
                                disableButtons();
                            }
                        }
                    });
                }

                requestData(nextEpoch, epochNumbers);
            }
        });
    }
}

const toggleResultVisibility = () => {
    const currentResultSelector = $('.life-configuration__result__value');
    if (currentResultSelector[0].classList.contains(HIDDEN_CLASS)) {
        currentResultSelector.removeClass(HIDDEN_CLASS);
    } else {
        currentResultSelector.addClass(HIDDEN_CLASS)
    }
}

const addResultListeners = () => {
    $('.life-configuration__result')[0].addEventListener('click', (event) => {
        toggleResultVisibility();
    })
}

addManageButtonsListeners();
addResultListeners();

if (header.length) {
    header.each((index, element) => addClickExpandListener(element));
}