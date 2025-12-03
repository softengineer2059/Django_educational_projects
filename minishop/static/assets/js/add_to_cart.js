function add_to_cart(button) {
    const productId = button.dataset.productId; // Получаем ID продукта из атрибута data

    fetch(`/cart/add/${productId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Получаем CSRF-токен
        },
        body: JSON.stringify({}) // Отправляем пустой объект
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message); // Показываем сообщение об успехе
            // Обновите счетчик товаров в корзине, если нужно
            document.getElementById('cart-count').innerText = data.cart_count;
        } else {
            alert('Ошибка при добавлении товара в корзину.');
        }
    })
    .catch(error => console.error('Ошибка:', error));
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Проверяем, начинается ли cookie с нужного имени
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}