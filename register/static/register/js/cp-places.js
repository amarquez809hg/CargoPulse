(function () {
  function extractCity(components) {
    if (!components) return "";
    var locality = "";
    var admin2 = "";
    components.forEach(function (c) {
      var types = c.types || [];
      var name = c.longText || c.long_name || "";
      if (types.indexOf("locality") !== -1) locality = name;
      if (types.indexOf("administrative_area_level_2") !== -1) admin2 = name;
    });
    return locality || admin2;
  }

  function syncHiddenFromWidget(widget, hiddenInput) {
    if (!hiddenInput || !widget) return;
    var value = widget.value || widget.getAttribute("value") || "";
    if (value) hiddenInput.value = value;
  }

  async function initPlacesAutocomplete() {
    var placesLib = await google.maps.importLibrary("places");
    var PlaceAutocompleteElement = placesLib.PlaceAutocompleteElement;

    document.querySelectorAll("[data-cp-places-field]").forEach(function (wrap) {
      if (wrap.dataset.cpPlacesReady === "1") return;
      wrap.dataset.cpPlacesReady = "1";

      var hiddenInput = wrap.querySelector('input[type="hidden"]');
      var cityTarget = wrap.dataset.cpPlacesCityTarget;
      var form = wrap.closest("form");
      var initial = wrap.dataset.cpPlacesInitial || "";

      var widget = new PlaceAutocompleteElement({
        includedRegionCodes: ["mx", "us"],
      });
      widget.classList.add("cp-places-widget");

      if (initial) {
        widget.setAttribute("placeholder", wrap.dataset.cpPlacesPlaceholder || "");
        if ("value" in widget) widget.value = initial;
      }

      wrap.appendChild(widget);

      widget.addEventListener("gmp-select", async function (event) {
        try {
          var place = event.placePrediction.toPlace();
          await place.fetchFields({
            fields: ["formattedAddress", "addressComponents"],
          });

          if (hiddenInput && place.formattedAddress) {
            hiddenInput.value = place.formattedAddress;
          }

          if (cityTarget && form && place.addressComponents) {
            var cityInput = form.querySelector('[name="' + cityTarget + '"]');
            if (cityInput) {
              var city = extractCity(place.addressComponents);
              if (city) cityInput.value = city;
            }
          }
        } catch (err) {
          console.warn("Cargo Pulse: place select failed", err);
        }
      });

      widget.addEventListener("input", function () {
        syncHiddenFromWidget(widget, hiddenInput);
      });

      if (form) {
        form.addEventListener("submit", function () {
          syncHiddenFromWidget(widget, hiddenInput);
        });
      }
    });
  }

  window.cpPlacesBootstrap = function () {
    initPlacesAutocomplete().catch(function (err) {
      console.warn("Cargo Pulse: Places init failed", err);
    });
  };
})();
