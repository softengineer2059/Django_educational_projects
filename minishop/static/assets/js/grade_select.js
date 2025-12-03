document.addEventListener('DOMContentLoaded', function () {
					const stars = document.querySelectorAll('.rating-star');
					const ratingInput = document.querySelector('input[name="grade"]');

					stars.forEach((star, index) => {
						star.addEventListener('click', () => {
							// Устанавливаем рейтинг
							const rating = index + 1;
							ratingInput.value = rating;

							// Обновляем визуальное состояние звезд
							stars.forEach((s, i) => {
								if (i < rating) {
									s.classList.add('selected');
								} else {
									s.classList.remove('selected');
								}
							});
						});
					});
				});