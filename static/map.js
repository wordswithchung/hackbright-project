// 'use strict';

function initMap() {
  var originalMapCenter = new google.maps.LatLng(14.0583, 108.2772);
  map = new google.maps.Map(document.getElementById('map'), {
        center: originalMapCenter,
        zoom: 3,
        });
};

function newCenter() {
  var mapCenter = new google.maps.LatLng(31.7917, 7.0926);
  newMap = new google.maps.Map(document.getElementById('map'), {
           center: mapCenter,
           zoom: 2,
           });
};

function loadDestinations(evt) {
  evt.preventDefault();

  airport = $('#airport-search-field').val().slice(0, 3);
  var m = airfares[airport];

  newCenter();

  for (i = 0; i < m.length; i++) {

    var name = m[i].city_name;
    var between = ": Average Price $";
    var avgPrice = m[i].avg_price;
    var cheapMonth = m[i].cheapest_month;
    var spot = new google.maps.LatLng(m[i].arrival_lat, m[i].arrival_lng);

    var marker = new google.maps.Marker({
        position: spot,
        map: newMap,
        title: name.concat(between,avgPrice),
        });

    };
};

$('#airport-search-form').on('submit', loadDestinations);