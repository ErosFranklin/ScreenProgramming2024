document.addEventListener('DOMContentLoaded', function() {
    const selecionarFotoInput = document.getElementById('mudarFotoA');
    const fotoContainer = document.getElementById('fotoContainer');
    const foto = document.getElementById('fotoAluno');

    selecionarFotoInput.addEventListener('change', function(event) {
        const arquivo = event.target.files[0];
        if (arquivo) {

            const url = URL.createObjectURL(arquivo);

            foto.src = url;

            fotoContainer.style.display = 'block';
        }
        
    });
});