
 ///////////////
 // basic map //
 ///////////////

"use strict";

function initMap() {
  var eastAustralia = {lat: -34.397, lng: 150.644};

  var map = new google.maps.Map(document.getElementById('map'), {
    center: eastAustralia,
    zoom: 8,
// Note: the following are marked the opposite of the default setting
// (that is, they're marked "false" if they're true by
// default, and "true" if they're false by default) so that
// uncommenting the following lines will actually change the map

// mapTypeControl: false,
// zoomControl: false,
// scaleControl: true,
// streetViewControl: false,
// rotateControl: true, // only available for locations with 45° imagery
// fullscreenControl: true

});
};

////////////
// marker //
////////////

function addMarker() {
  var myImageURL = 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png';
  var image = myImageURL;
  var nearSydney = new google.maps.LatLng(-34.788666, 150.41146)
  var marker = new google.maps.Marker({
      position: nearSydney,
      map: map,
      title: 'Hover text',
      icon: image
  });
  return marker;
}

// var marker = addMarker();

/////////////////
// info window //
/////////////////

function addInfoWindow() {

  var contentString = '<div id="content">' +
    '<h1>All my custom content</h1>' +
    '</div>';

  var infoWindow = new google.maps.InfoWindow({
    content: contentString,
    maxWidth: 200
  });

  marker.addListener('click', function() {
    infoWindow.open(map, marker);
  });
}

// addInfoWindow()


////////////
// styles //
////////////

function addStyles() {

  var styles = [
  {
      "featureType": "water",
      "stylers": [
        { "color": "#2529da" }
      ]
    }
  ];

  var styledMapOptions = {
      name: 'Custom Style'
  };

  var customMapType = new google.maps.StyledMapType(
          styles,
          styledMapOptions);

  map.mapTypes.set('map_style', customMapType);
  map.setMapTypeId('map_style');

}

// addStyles();

//////////////////////////
// geocoding by address //
//////////////////////////

function addHackbrightByAddress() {
  var hackbright = new google.maps.Geocoder();
  var address = "683 Sutter Street, San Francisco, CA";

  hackbright.geocode({'address': address},
    function(results, status) {
      if (status === google.maps.GeocoderStatus.OK) {
        map.setCenter(results[0].geometry.location);
        var marker = new google.maps.Marker({
          map: map,
          position: results[0].geometry.location
        });
      } else {
        alert('Geocode was not successful for the following reason: ' + status);
      }
  });
}

// addHackbrightByAddress();

/////////////////////////////
// geocoding by place name //
/////////////////////////////

function addGoldenGateBridgeByName() {

  var beautifulBridge = new google.maps.Geocoder();
  var premise = "Golden Gate Bridge"

  beautifulBridge.geocode({'address': premise}, function(results, status) {
      if (status === google.maps.GeocoderStatus.OK) {
        map.setCenter(results[0].geometry.location);
        var marker = new google.maps.Marker({
          map: map,
          position: results[0].geometry.location
        });
      } else {
        alert('Geocode was not successful for the following reason: ' + status);
      }
    });
}

// addGoldenGateBridgeByName();

///////////////
// polyLines //
///////////////

function addTripPath() {
  var sydney = {lat: -33.8675, lng: 151.2070}
  var bathurst = {lat: -33.4177, lng: 149.5810}
  var canberra = {lat: -35.2820, lng: 149.1287}

  var roadTripStops = [
      sydney,
      bathurst,
      canberra
  ];

  var tripPath = new google.maps.Polyline({
      path: roadTripStops,
      geodesic: true,
      strokeColor: '#ff0000',
      strokeOpacity: 1.0,
      strokeWeight: 5
  });

  tripPath.setMap(map);
}

// addTripPath();

////////////////
// directions //
////////////////

function displayDirections() {

  var sydney = {lat: -33.8675, lng: 151.2070}
  var bathurst = {lat: -33.4177, lng: 149.5810}
  var canberra = {lat: -35.2820, lng: 149.1287}

  var bathurstWaypoint = {
          location: bathurst,
          stopover: true
  }

  var routeOptions = {
      origin: sydney,
      destination: canberra,
      waypoints: [bathurstWaypoint],
      travelMode: google.maps.TravelMode.DRIVING
    }

  var directionsService = new google.maps.DirectionsService;
  directionsService.route(routeOptions, function(response, status) {
      if (status === google.maps.DirectionsStatus.OK) {
        directionsDisplay.setDirections(response);
      } else {
        window.alert('Directions request failed due to ' + status);
      }
    });

  var directionsDisplay = new google.maps.DirectionsRenderer;
  directionsDisplay.setMap(map);
}

// displayDirections();
