const header = $('.generation')
const submit = $('.button__submit');

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

if (submit.length) {
    const button = submit[0];
    button.addEventListener('click', (event) => {
        button.innerHTML = '';
        button.className = 'loader';
        button.disabled = true;
        let nextEpoch = $('.generation').length + 1;

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
                button.className = 'button button__submit';
                button.disabled = false;
            }
        })
    });
}