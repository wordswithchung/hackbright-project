
function loadSortByAirportCode(evt) {

    evt.preventDefault();

    var sortByAirportCode = info.sort(function(a, b) {
        if (a.airport_code > b.airport_code) { return 1 }
        else if (a.airport_code < b.airport_code) { return -1 }
        else {return 0}});

    for (i = 0; i < sortByAirportCode.length; i++) {
        $('#box_arrival_city'+i).html(sortByAirportCode[i].arrival_city);
        $('#box_average_price'+i).html(sortByAirportCode[i].avg_price);
        $('#box_airport_code'+i).html(sortByAirportCode[i].airport_code);
        $('#box_distance'+i).html(sortByAirportCode[i].distance);
        $('#box_kayak_url'+i).html('<a href=\"' + sortByAirportCode[i].kayak_url + '\">Buy on Kayak!</a>');};
    };

$('#sort-by-airport-code').on('click', loadSortByAirportCode);

function loadSortByValue(evt) {
    // http://stackoverflow.com/a/979289
    var sortByValue = info.sort(function(a, b) {return parseFloat(a.avg_price / a.distance) - parseFloat(b.avg_price / b.distance)});

    for (i = 0; i < sortByValue.length; i++) {
        $('#box_arrival_city'+i).html(sortByValue[i].arrival_city);
        $('#box_average_price'+i).html(sortByValue[i].avg_price);
        $('#box_airport_code'+i).html(sortByValue[i].airport_code);
        $('#box_distance'+i).html(sortByValue[i].distance);
        $('#box_kayak_url'+i).html('<a href=\"' + sortByValue[i].kayak_url + '\">Buy on Kayak!</a>');};
    };

$('#sort-by-value').on('click', loadSortByValue);

function loadSortByPrice(evt) {
    // http://stackoverflow.com/a/979289
    var sortByPrice = info.sort(function(a, b) {return parseFloat(a.avg_price) - parseFloat(b.avg_price)});

    for (i = 0; i < sortByPrice.length; i++) {
        $('#box_arrival_city'+i).html(sortByPrice[i].arrival_city);
        $('#box_average_price'+i).html(sortByPrice[i].avg_price);
        $('#box_airport_code'+i).html(sortByPrice[i].airport_code);
        $('#box_distance'+i).html(sortByPrice[i].distance);
        $('#box_kayak_url'+i).html('<a href=\"' + sortByPrice[i].kayak_url + '\">Buy on Kayak!</a>');};
    };

$('#sort-by-avg-price').on('click', loadSortByPrice);

function loadSortByDistance(evt) {
    // http://stackoverflow.com/a/979289
    var sortByDistance = info.sort(function(a, b) {return parseFloat(a.distance) - parseFloat(b.distance)});

    for (i = 0; i < sortByDistance.length; i++) {
        $('#box_arrival_city'+i).html(sortByDistance[i].arrival_city);
        $('#box_average_price'+i).html(sortByDistance[i].avg_price);
        $('#box_airport_code'+i).html(sortByDistance[i].airport_code);
        $('#box_distance'+i).html(sortByDistance[i].distance);
        $('#box_kayak_url'+i).html('<a href=\"' + sortByDistance[i].kayak_url + '\">Buy on Kayak!</a>');};
    };

$('#sort-by-distance').on('click', loadSortByDistance);

function loadSortByCity() {

    var sortByCity = info.sort(function(a, b) {
        if (a.arrival_city > b.arrival_city) { return 1 }
        else if (a.arrival_city < b.arrival_city) { return -1 }
        else {return 0}});

    for (i = 0; i < sortByCity.length; i++) {
    $('#box_arrival_city'+i).html(sortByCity[i].arrival_city);
    $('#box_average_price'+i).html(sortByCity[i].avg_price);
    $('#box_airport_code'+i).html(sortByCity[i].airport_code);
    $('#box_distance'+i).html(sortByCity[i].distance);
    $('#box_kayak_url'+i).html('<a href=\"' + sortByCity[i].kayak_url + '\">Buy on Kayak!</a>');
    };
};

$('#sort-by-city-name').on('click', loadSortByCity);

loadSortByCity();