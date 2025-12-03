function openModal(imageSrc, captionText) {
    var modal = document.getElementById("imageModal");
    var modalImg = document.getElementById("modalImage");
    var caption = document.getElementById("caption");
    
    modal.style.display = "block";
    modalImg.src = imageSrc;
    caption.innerHTML = captionText;
}

function closeModal() {
    var modal = document.getElementById("imageModal");
    modal.style.display = "none";
}

// Добавьте обработчик событий для изображений
document.querySelectorAll('.card-body_comments img').forEach(function(img) {
    img.addEventListener('click', function() {
        openModal(this.src, this.alt);
    });
});