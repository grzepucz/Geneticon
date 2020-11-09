const header = document.getElementsByClassName('generation__header')

if (header.length) {
    header[0].addEventListener('click', (event) => {
        if (document.getElementsByClassName('generation__population--hidden').length) {
            const subjects = document.getElementsByClassName('generation__population--hidden');
            subjects[0].classList.add('generation__population');
            subjects[0].classList.remove('generation__population--hidden');
        } else {
            const subjects = document.getElementsByClassName('generation__population');
            subjects[0].classList.add('generation__population--hidden');
            subjects[0].classList.remove('generation__population');
        }
    });
}
