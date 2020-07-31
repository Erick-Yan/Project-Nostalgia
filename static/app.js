const navLinks = document.querySelectorAll('.AB ul li');

document.querySelector('#plus').onclick = function() {
    document.querySelector('.AB').classList.toggle('move');

    navLinks.forEach((link, index) =>{
            if(link.style.animation){
                    link.style.animation = '';
            } else{
                    link.style.animation = `fadein 0.7s ease forwards ${index / 10 + 0.1}s`;
            }
    });
}