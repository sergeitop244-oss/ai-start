// Ждем, пока загрузится вся страница
document.addEventListener('DOMContentLoaded', () => {
    // Находим все кнопки с классом "order-button"
    const buttons = document.querySelectorAll('.order-button');

    // Для каждой кнопки добавляем обработчик клика
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            // Находим название блюда, чтобы показать его в уведомлении
            const itemName = button.parentElement.querySelector('h3').innerText;
            // Показываем всплывающее окно (попап)
            alert(`Вы добавили "${itemName}" в корзину!`);
        });
    });
});