document.addEventListener('DOMContentLoaded', function() {
					// Получаем итоговую оценку

					const totalGrade = document.querySelector('#product_grade').textContent;
					const starElements = document.querySelectorAll('#star-rating .fa-star, #star-rating .fa-star-o');

					// Определяем количество звезд, которые нужно окрасить
					const filledStars = Math.round(totalGrade); // Округляем до ближайшего целого

					// Окрашиваем звезды
					for (let i = 0; i < starElements.length; i++) {
						if (i < filledStars) {
							starElements[i].classList.remove('fa-star-o');
							starElements[i].classList.add('fa-star', 'text-warning');
						} else {
							starElements[i].classList.remove('fa-star');
							starElements[i].classList.add('fa-star-o');
						}
					}
				});