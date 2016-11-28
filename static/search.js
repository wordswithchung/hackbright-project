// 'use strict';

function loop(sortedResults) {

  for (i = 0; i < sortedResults.length; i++) {
    $('#box-arrival-city'+i).html(sortedResults[i].arrival_city);
    $('#box-average-price'+i).html(sortedResults[i].avg_price);
    $('#box-airport-code'+i).html(sortedResults[i].airport_code);
    $('#box-distance'+i).html(sortedResults[i].distance);
    $('#box-kayak-url'+i).html('<a href=\"' + sortedResults[i].kayak_url
                                            + '\" class="btn btn-default btn-sm kayak-button">Buy on Kayak</a>');
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