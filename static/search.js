function loop(sortedResults) {

  for (i = 0; i < sortedResults.length; i++) {
    $('#box_arrival_city'+i).html(sortedResults[i].arrival_city);
    $('#box_average_price'+i).html(sortedResults[i].avg_price);
    $('#box_airport_code'+i).html(sortedResults[i].airport_code);
    $('#box_distance'+i).html(sortedResults[i].distance);
    $('#box_kayak_url'+i).html('<a href=\"' + sortedResults[i].kayak_url
                                            + '\">Buy on Kayak!</a>');
  };
};

function loadSortByAirportCode(evt) {

  sortByAirportCode = info.sort(function(a, b) {
                      if (a.airport_code > b.airport_code) { return 1 }
                      else if (a.airport_code < b.airport_code) { return -1 }
                      else {return 0}});

  loop(sortByAirportCode);
};

$('#sort-by-airport-code').on('click', loadSortByAirportCode);

function loadSortByValue(evt) {

  // http://stackoverflow.com/a/979289
  sortByValue = info.sort(function(a, b) {return parseFloat(a.avg_price / a.distance) - parseFloat(b.avg_price / b.distance)});

  loop(sortByValue);
};

$('#sort-by-value').on('click', loadSortByValue);

function loadSortByPrice(evt) {

  // http://stackoverflow.com/a/979289
  sortByPrice = info.sort(function(a, b) {return parseFloat(a.avg_price) - parseFloat(b.avg_price)});

  loop(sortByPrice);
};

$('#sort-by-avg-price').on('click', loadSortByPrice);

function loadSortByDistance(evt) {

  // http://stackoverflow.com/a/979289
  sortByDistance = info.sort(function(a, b) {return parseFloat(a.distance) - parseFloat(b.distance)});

  loop(sortByDistance);
};

$('#sort-by-distance').on('click', loadSortByDistance);

function loadSortByCity() {

  sortByCity = info.sort(function(a, b) {
               if (a.arrival_city > b.arrival_city) { return 1 }
               else if (a.arrival_city < b.arrival_city) { return -1 }
               else {return 0}});

  loop(sortByCity);
};

$('#sort-by-city-name').on('click', loadSortByCity);

loadSortByCity();