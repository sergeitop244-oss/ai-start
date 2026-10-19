document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('orderModal');
    const closeBtn = document.querySelector('.close-btn');
    const modalDishName = document.getElementById('modalDishName');
    const orderForm = document.getElementById('orderForm');
    const buttons = document.querySelectorAll('.order-button');

    let currentDish = ""; 

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            currentDish = button.parentElement.querySelector('h3').innerText;
            modalDishName.innerText = "Вы заказываете: " + currentDish;
            modal.classList.add('active');
        });
    });

    closeBtn.addEventListener('click', () => {
        modal.classList.remove('active');
    });

    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.classList.remove('active');
        }
    });

    orderForm.addEventListener('submit', (event) => {
        event.preventDefault(); 

        const name = document.getElementById('clientName').value;
        const phone = document.getElementById('clientPhone').value;
        const address = document.getElementById('clientAddress').value;

        // Собираем текст без сложных кавычек, чтобы точно не было ошибок
        const text = "Новый заказ!%0AБлюдо: " + currentDish + "%0AИмя: " + name + "%0AТелефон: " + phone + "%0AАдрес: " + address;
        
        const token = "8822338809:AAHbKvPOXwQKwh6z_UKHm5lI4gIjpvyEU8g"; 
        const chatId = "6149757783"; 
        
        fetch("https://api.telegram.org/bot" + token + "/sendMessage?chat_id=" + chatId + "&text=" + text)
            .then(response => {
                if (response.ok) {
                    alert("Спасибо, " + name + "! Ваш заказ на " + currentDish + " принят.");
                    orderForm.reset();
                    modal.classList.remove('active');
                } else {
                    alert("Ошибка Telegram. Проверь токен, ID и нажми /start у бота.");
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
                alert("Ошибка сети.");
            });
    });
});