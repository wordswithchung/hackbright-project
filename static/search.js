// http://stackoverflow.com/a/33319433

'use strict';

$(document).ready(function() {
    console.log( "ready!" );

var resultsAsHTML;

function showResults(results) {

    console.log('starting showResults');

    for (var key in results) {
    var result = results[key];

    resultsAsHTML = (
    '<div class="search-result-box">' +
        '<h1>' + result.arrival_city + '</h1>' +
        '<p>Average Price: $' + result.avg_price + '</p><br>' +
        '<p>Airport Code: ' + result.arrival_code + '</p><br>' +
        '<p>Distance in miles: ' + result.distance + '</p><br>' +
        '<a href=\"' + result.kayak_url + '\"> Buy on Kayak!</a><br>' +
    '</div>')};

    console.log(resultsAsHTML);

    $('#display-search-results').load(resultsAsHTML);
};

function getData() {

    var formData = {
        'depart'    : $('#input-from').val(),
        'month'     : $('#input-month').val(),
        'duration'  : $('#input-duration').val()
    };

    $.post('/search.json', formData, showResults);
};

getData();

});