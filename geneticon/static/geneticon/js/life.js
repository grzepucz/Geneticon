const header = $('.generation')
const next = $('.button__next');
const live = $('.button__live');

const addClickExpandListener = (element) => {
    element.addEventListener('click', (event) => {
        let currentEpoch = $(element);
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
    })
}
if (header.length) {
    header.each((index, element) => addClickExpandListener(element));
}

if (next.length) {
     next[0].addEventListener('click', (event) => {
        let manageButtons = $('.manage-buttons');
        let loader = $('.loader--hidden');
        let nextEpoch = $('.generation').length + 1;

        manageButtons.addClass('hidden');
        loader.addClass('loader').removeClass('loader--hidden');

        $.ajax({
            url: `${window.location.href}/epoch/${nextEpoch}`,
            type: 'GET',
            success: (data) => {
                const serializer = new XMLSerializer();
                const xmlStr = serializer.serializeToString(data);
                const generations = $('.generations');
                generations.append(xmlStr);
                addClickExpandListener(generations.children().last()[0]);
            },
            error: (error) => {
                console.log('errors');
                console.log(error);
            },
            complete: () => {
                manageButtons.removeClass('hidden');
                loader.addClass('loader--hidden').removeClass('loader');
            }
        })
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
            const requestData = async (epoch, limit) => {
                $.ajax({
                    url: `${window.location.href}/epoch/${epoch}`,
                    type: 'GET',
                    success: (data) => {
                        const serializer = new XMLSerializer();
                        const xmlStr = serializer.serializeToString(data);
                        const generations = $('.generations');
                        generations.append(xmlStr);
                        addClickExpandListener(generations.children().last()[0]);
                    },
                    error: (error) => {
                        manageButtons.removeClass('hidden');
                        loader.addClass('loader--hidden').removeClass('loader');
                    },
                    complete: async () => {
                        if (epoch + 1 <= limit) {
                            await requestData(epoch+1, limit);
                        }
                    }
                });
            }

            requestData(nextEpoch, epochNumbers);
        }
    });
}