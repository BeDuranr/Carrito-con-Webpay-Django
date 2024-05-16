if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
        var lat = position.coords.latitude;
        var lon = position.coords.longitude;
        
        // Llamada AJAX para enviar las coordenadas al servidor Django
        $.ajax({
            url: '/get-weather/',
            method: 'GET',
            data: {
                'lat': lat,
                'lon': lon
            },
            success: function(response) {
                $('#weather-info').html(response);
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
    });
} else {
    console.log("La geolocalización no está disponible en este navegador.");
}
