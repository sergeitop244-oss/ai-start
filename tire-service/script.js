document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('bookingForm');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        var name = document.getElementById('clientName').value;
        var phone = document.getElementById('clientPhone').value;
        var car = document.getElementById('carModel').value;

        var text = "Заявка: " + name + ", " + phone + ", Авто: " + car;
        
        // ВСТАВЬ СВОИ ДАННЫЕ НИЖЕ (в кавычках)
        var token = "8866205722:AAG_7hTmwzEtiwf9C7Yjt5Sug7j38hxwcus"; 
        var chatId = "8866205722"; 

        var url = "https://api.telegram.org/bot" + token + "/sendMessage?chat_id=" + chatId + "&text=" + encodeURIComponent(text);

        fetch(url)
            .then(function(response) {
                if (response.ok) {
                    alert("Спасибо, " + name + "! Заявка принята.");
                    form.reset();
                } else {
                    alert("Ошибка отправки.");
                }
            })
            .catch(function(error) {
                alert("Ошибка сети.");
            });
    });
});