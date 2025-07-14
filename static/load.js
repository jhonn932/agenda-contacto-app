//Cuando la pagina se haya cargado completamente, ocultamos el loader
window.addEventListener('load', () => {
    const loader = document.getElementById('loader');
    loader.classList.add('hidden');
});
