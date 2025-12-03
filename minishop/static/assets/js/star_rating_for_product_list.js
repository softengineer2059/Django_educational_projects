document.addEventListener('DOMContentLoaded', function() {
    const starRatings = document.querySelectorAll('.star-rating');

    starRatings.forEach(rating => {
        // Ищем элемент с оценкой внутри текущего рейтинга
        const gradeElement = rating.querySelector('h4');

        // Если нет элемента с оценкой, пропускаем этот блок
        if (!gradeElement) {
            // Оставляем все звезды пустыми (как в исходном HTML)
            return;
        }

        // Извлекаем числовое значение оценки
        const totalGradeText = gradeElement.textContent;
        const totalGrade = parseFloat(totalGradeText.replace(/[^0-9.]/g, ''));

        // Получаем все звезды только в текущем блоке
        const starElements = rating.querySelectorAll('i');

        // Определяем количество заполненных звезд
        const filledStars = Math.round(totalGrade);

        // Окрашиваем звезды
        starElements.forEach((star, index) => {
            if (index < filledStars) {
                star.classList.remove('fa-star-o');
                star.classList.add('fa-star', 'text-warning');
            } else {
                star.classList.remove('fa-star', 'text-warning');
                star.classList.add('fa-star-o');
            }
        });
    });
});