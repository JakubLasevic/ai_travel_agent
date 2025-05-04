// --- Global Variables ---
// Google Maps API elements (initialized in initMap)
let map;
let AdvancedMarkerElement;
let PinElement;
let LatLngBounds;
let InfoWindow; // Added for hover popups

// Map state variables
let currentMapMarker = null; // Holds the marker for the main selected location
let currentPOIMarkers = []; // Holds markers for the displayed POIs
let infoWindowInstance = null; // Single InfoWindow instance

// Constants
const LOCATIONS_PER_PAGE = 5; // How many location buttons to show at once

// DOM Elements (initialized in initializeChat)
let chatLog;
let userInput;
let sendButton;


// --- Initialization Function ---
/**
 * Initializes the Google Map instance and loads necessary libraries.
 * Called after the DOM is fully loaded.
 */
async function initMap() {
    console.log("initMap called.");
    const position = { lat: 50.0755, lng: 14.4378 }; // Default position (Prague)
    const mapDiv = document.getElementById("map");

    if (!mapDiv) {
        console.error("Map container element with ID 'map' not found.");
        const logEl = chatLog || document.getElementById('chat-log');
        if (logEl) displayMessage({ response: "Internal Error: Map container element not found on page." }, 'ai');
        return;
    }

    try {
        console.log("Attempting to import Google Maps libraries...");
        // Import necessary classes using object destructuring
        const mapsLibrary = await google.maps.importLibrary("maps");
        const markerLibrary = await google.maps.importLibrary("marker");
        const coreLibrary = await google.maps.importLibrary("core");

        // Assign constructors/classes to variables
        const Map = mapsLibrary.Map;
        InfoWindow = mapsLibrary.InfoWindow;
        AdvancedMarkerElement = markerLibrary.AdvancedMarkerElement;
        PinElement = markerLibrary.PinElement;
        LatLngBounds = coreLibrary.LatLngBounds;
        console.log("Google Maps libraries imported successfully.");

        // --- Define Map Styles ---
        const mapStyles = [
          { featureType: "poi", elementType: "labels", stylers: [{ visibility: "off" }] },
          { featureType: "poi", elementType: "geometry", stylers: [{ visibility: "off" }] },
          { featureType: "poi.restaurant", elementType: "labels", stylers: [{ visibility: "on" }] },
          { featureType: "poi.restaurant", elementType: "geometry", stylers: [{ visibility: "on" }] }
        ];
        // --- End Map Styles ---

        // Create the map instance
        map = new Map(mapDiv, {
            zoom: 5,
            center: position,
            mapId: "9da1cfb76407c827", 
            gestureHandling: 'greedy',
            styles: mapStyles, 
            clickableIcons: false 
        });
        console.log("Map initialized successfully with Map ID and styles.");

        // Create a single InfoWindow instance to reuse
        infoWindowInstance = new InfoWindow({
             pixelOffset: new google.maps.Size(0, -25) 
        });
        console.log("InfoWindow instance created with pixelOffset.");

        map.addListener('click', () => {
             if (infoWindowInstance) {
                console.log("Map clicked, closing InfoWindow.");
                infoWindowInstance.close();
             }
        });
        console.log("Map click listener added to close InfoWindows.");


    } catch (error) {
        console.error("Error during Google Map library import or instantiation:", error);
        mapDiv.innerHTML = '<p style="padding: 20px; text-align: center; color: red;">Could not load map. Check API key/Map ID config.</p>';
        const logEl = chatLog || document.getElementById('chat-log');
        if(logEl) displayMessage({ response: "Error initializing map. Map features unavailable." }, 'ai');
    }
}

// --- POI Marker Customization ---
/**
 * Returns customized marker options based on POI type.
 */
function getPOIMarkerOptions(type) {
    let glyph = '📍'; let background = '#777777'; let borderColor = '#555555';
    const typeLower = type ? type.toLowerCase().trim() : '';
    switch (typeLower) {
        case 'sight': case 'viewpoint': glyph = '👀'; background = '#FF9800'; borderColor = '#F57C00'; break;
        case 'museum': glyph = '🏛️'; background = '#9C27B0'; borderColor = '#7B1FA2'; break;
        case 'park': case 'forest': case 'garden': glyph = '🌳'; background = '#4CAF50'; borderColor = '#388E3C'; break;
        case 'activity': case 'trail': glyph = '🚶'; background = '#00BCD4'; borderColor = '#0097A7'; break;
        case 'town': glyph = '🏘️'; background = '#607D8B'; borderColor = '#455A64'; break;
        case 'beach': glyph = '🏖️'; background = '#2196F3'; borderColor = '#1976D2'; break;
        case 'lake': glyph = '💧'; background = '#03A9F4'; borderColor = '#0288D1'; break;
        case 'mountain peak': glyph = '⛰️'; background = '#A1887F'; borderColor = '#795548'; break;
        case 'region': glyph = '🗺️'; background = '#BDBDBD'; borderColor = '#9E9E9E'; break;
        case 'winery/region': glyph = '🍇'; background = '#8E24AA'; borderColor = '#6A1B9A'; break;
        case 'castle': glyph = '🏰'; background = '#FFC107'; borderColor = '#FFA000'; break;
        case 'restaurant': glyph = '🍴'; background = '#E91E63'; borderColor = '#C2185B'; break;
    }
    return { glyph: glyph, glyphColor: 'white', background: background, borderColor: borderColor };
}


// --- Message Display Functions ---

/** Displays a message in the chat log. */
function displayMessage(data, sender) {
    const chatLogElement = chatLog || document.getElementById('chat-log');
    if (!chatLogElement) { console.error("Chat log missing."); return; }
    const messageContainer = document.createElement('div');
    messageContainer.classList.add('message', sender);
    const textToShow = (sender === 'ai') ? data.response : data.text;
    if (textToShow) {
        const textElement = document.createElement('div');
        textElement.classList.add('message-text');
        textElement.innerHTML = textToShow.replace(/\n/g, '<br>');
        messageContainer.appendChild(textElement);
    } else if (sender === 'ai' && !(data.locations && data.locations.length > 0)) {
        console.warn("Empty AI message.", data); return;
    }
    chatLogElement.appendChild(messageContainer);
    if (sender === 'ai' && data.locations && data.locations.length > 0) {
        const locationsElement = document.createElement('div');
        locationsElement.classList.add('locations-container'); // Container for buttons
        try { locationsElement.dataset.allDestinations = JSON.stringify(data.locations); }
        catch (e) { console.error("Stringify error:", e); locationsElement.dataset.allDestinations = '[]'; }
        locationsElement.dataset.shownCount = "0";
        appendLocationButtons(locationsElement, 0); // Add initial buttons
        chatLogElement.appendChild(locationsElement); // Add button container to chat
    }
    chatLogElement.scrollTop = chatLogElement.scrollHeight;
}

/** Appends a batch of location buttons. */
function appendLocationButtons(parentElement, startIndex) {
    if (!parentElement) { console.error("Parent missing for buttons."); return; }
    let allDestinations = [];
    try { allDestinations = JSON.parse(parentElement.dataset.allDestinations || '[]'); }
    catch (e) { console.error("Parse destinations error:", e); }
    let shownCount = parseInt(parentElement.dataset.shownCount || "0");
    const existingShowMore = parentElement.querySelector('.show-more-locations');
    if (existingShowMore) parentElement.removeChild(existingShowMore);
    const endIndex = Math.min(startIndex + LOCATIONS_PER_PAGE, allDestinations.length);
    for (let i = startIndex; i < endIndex; i++) {
        const dest = allDestinations[i];
        if (dest && typeof dest.lat === 'number' && typeof dest.lng === 'number' && dest.name) {
            const button = document.createElement('button');
            button.classList.add('location-button'); button.textContent = dest.name;
            button.dataset.lat = dest.lat; button.dataset.lng = dest.lng; button.dataset.name = dest.name;
            if (dest.id) { button.dataset.id = dest.id; }
            parentElement.appendChild(button); shownCount++;
        } else { console.warn(`Skipping button index ${i}:`, dest); }
    }
    parentElement.dataset.shownCount = shownCount.toString();
    if (shownCount < allDestinations.length) {
        const showMoreButton = document.createElement('button');
        showMoreButton.classList.add('show-more-locations');
        const remaining = allDestinations.length - shownCount;
        showMoreButton.textContent = `Show ${Math.min(remaining, LOCATIONS_PER_PAGE)} More (${remaining} total remaining)`;
        parentElement.appendChild(showMoreButton);
    }
}


// --- Map Interaction Functions ---

/** Clears markers and shows a single main location marker. */
async function showSingleLocationOnMap(lat, lng, name) {
     return new Promise((resolve, reject) => {
        if (!map || !AdvancedMarkerElement || !PinElement) { return reject(new Error("Map components not ready")); }
        clearAllMarkers();
        if (isNaN(lat) || isNaN(lng)) { return reject(new Error("Invalid coordinates")); }
        const position = { lat: lat, lng: lng };
        try {
            const pin = new PinElement({ background: "#FF0000", borderColor: "#8B0000", glyphColor: "white", scale: 1.2 });
            currentMapMarker = new AdvancedMarkerElement({ map: map, position: position, title: name, content: pin.element, zIndex: 10 });
            map.setCenter(position); map.setZoom(12);
            console.log(`Map centered on: ${name}`, position); resolve();
        } catch (error) { console.error("Error creating main marker:", error); reject(error); }
    });
}

/**
 * Displays markers for POIs with custom icons and info windows on click.
 */
async function displayPOIMarkers(pois) {
    if (!map || !AdvancedMarkerElement || !PinElement || !LatLngBounds || !infoWindowInstance) {
        console.error("displayPOIMarkers: Map components not ready."); return;
    }
    if (!pois || !Array.isArray(pois) || pois.length === 0) {
        console.log("displayPOIMarkers: No valid POIs provided."); clearPOIMarkers(); return;
    }

    clearPOIMarkers();
    const bounds = new LatLngBounds();

    if (currentMapMarker && currentMapMarker.position) { bounds.extend(currentMapMarker.position); }
    else { const firstPOI = pois.find(p => p && typeof p.lat === 'number' && typeof p.lng === 'number'); if (firstPOI) bounds.extend({ lat: firstPOI.lat, lng: firstPOI.lng }); }

    console.log(`Attempting to display ${pois.length} POI markers.`);
    let validPoisAdded = 0;
    for (const poi of pois) {
        if (poi && typeof poi.lat === 'number' && typeof poi.lng === 'number' && poi.name) {
            const poiPosition = { lat: poi.lat, lng: poi.lng };
            try {
                const markerOptions = getPOIMarkerOptions(poi.type);
                const poiPin = new PinElement(markerOptions); // Create the visual element

                // Create the Advanced Marker, passing the pin element as content
                const poiMarker = new AdvancedMarkerElement({
                    map: map,
                    position: poiPosition,
                    content: poiPin.element, 
                    zIndex: 5
                });

                // --- Create InfoWindow Content (Reverted Layout, Adjusted Padding/Margins) ---
                const descriptionText = poi.description || '';
                const infoContent = `
                    <div style="font-family: 'Inter', system-ui, sans-serif; font-size: 14px; max-width: 260px; padding: 10px 12px; line-height: 1.4;">
                        <div style="font-size: 16px; font-weight: 600; color: #222; margin: 0 0 3px 0;">${poi.name}</div>
                        <div style="font-size: 13px; color: #555; margin: 0 0 8px 0; font-style: italic;">Category: ${poi.type || 'Info'}</div>
                        <div style="font-size: 13px; color: #333; margin: 0;">${descriptionText}</div>
                    </div>`;
                // --- End InfoWindow Content ---

                // --- Attach standard DOM CLICK listener directly to the pin's element ---
                if (poiPin.element) { // Check if element exists
                    poiPin.element.classList.add('custom-poi-marker'); // Add class for CSS cursor

                    poiPin.element.addEventListener('click', (event) => { 
                        event.stopPropagation(); 

                        console.log(`DOM click fired for POI: ${poi.name}`);
                        if (!infoWindowInstance) return;
                        infoWindowInstance.close(); 
                        infoWindowInstance.setContent(infoContent);
                        // Anchor the InfoWindow to the AdvancedMarkerElement
                        infoWindowInstance.open(map, poiMarker);
                    });

                } else {
                    console.error(`PinElement element missing for POI: ${poi.name}`);
                }
                // --- End DOM listeners ---

                currentPOIMarkers.push(poiMarker);
                bounds.extend(poiPosition);
                validPoisAdded++;

            } catch(error) {
                console.error(`Error creating POI marker or adding listener for: ${poi.name}`, error);
            }
        } else {
            console.warn("Skipping POI due to missing/invalid data:", poi);
        }
    }
    console.log(`Finished loop. Added ${validPoisAdded} valid POI markers.`);

    // Adjust map view
    if (validPoisAdded > 0 && !bounds.isEmpty()) {
        if (bounds.getNorthEast().equals(bounds.getSouthWest())) { map.setCenter(bounds.getCenter()); map.setZoom(14); }
        else { map.fitBounds(bounds, 50); }
    } else if (currentMapMarker) { map.setCenter(currentMapMarker.position); map.setZoom(12); }
}

/** Clears all POI markers */
function clearPOIMarkers() {
    if (currentPOIMarkers.length > 0) { for (let marker of currentPOIMarkers) { marker.map = null; } currentPOIMarkers = []; }
}

/** Clears all markers (main location and POIs) */
function clearAllMarkers() {
     if (currentMapMarker) { currentMapMarker.map = null; currentMapMarker = null; } clearPOIMarkers();
}


// --- Chat Logic ---

/** Sends user message to backend /chat */
async function sendMessage() {
    const msg = userInput.value.trim(); if (msg === '') return;
    displayMessage({ text: msg }, 'user'); userInput.value = '';
    userInput.disabled = true; sendButton.disabled = true;
    try {
        const resp = await fetch('/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message: msg }), });
        if (!resp.ok) { let err = `Err ${resp.status}`; try { const d = await resp.json(); err = `Err ${resp.status}: ${d.error||'?'}`; } catch(e){} displayMessage({ response: err }, 'ai'); return; }
        const data = await resp.json(); displayMessage(data, 'ai');
    } catch (err) { console.error('Send msg err:', err); displayMessage({ response: 'Network error.' }, 'ai'); }
    finally { userInput.disabled = false; sendButton.disabled = false; userInput.focus(); }
}

// --- Event Listener Setup ---

/** Initializes chat elements and event listeners */
function initializeChat() {
    console.log("Initializing chat...");
    chatLog = document.getElementById('chat-log');
    userInput = document.getElementById('user-input');
    sendButton = document.getElementById('send-button');

    if (!chatLog || !userInput || !sendButton) { console.error("Chat UI elements missing!"); return; }

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') sendMessage(); });

    // Event Delegation for dynamic buttons in chat log
    chatLog.addEventListener('click', function(event) {
        const target = event.target;

        if (target.classList.contains('location-button')) {
            const lat = target.dataset.lat;
            const lng = target.dataset.lng;
            const name = target.dataset.name;
            if (!name || !lat || !lng) { console.error("Button data missing.", target); return; }
            console.log(`Location button clicked: ${name}`);

            // *** ADDED: Remove button container on click ***
            const buttonContainer = target.closest('.locations-container');
            if (buttonContainer) {
                 console.log("Removing location button container.");
                 buttonContainer.remove();
            }
            // *** End Added Code ***

            // Fetch location details from the backend
            fetch('/location_details', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', },
                body: JSON.stringify({ location_name: name }), // Send name to identify
            })
            .then(response => { // Handle HTTP errors
                if (!response.ok) {
                    // Try to parse JSON error from backend, else use status text
                    return response.json()
                        .then(err => { throw new Error(`HTTP ${response.status}: ${err.error || response.statusText}`); })
                        .catch(() => { throw new Error(`HTTP ${response.status}: ${response.statusText}`); });
                }
                return response.json(); // Parse successful response
            })
            .then(data => { // Process successful response data
                console.log("Received details:", data);
                if (data.error) {
                    displayMessage({ response: `Error getting details: ${data.error}` }, 'ai');
                    return; // Stop if backend reported an error
                }

                // Display description
                if (data.description) { displayMessage({ response: data.description }, 'ai'); }
                else { displayMessage({ response: `Okay, showing map for ${name}:` }, 'ai'); } // Fallback

                // Update map (returns promise)
                return showSingleLocationOnMap(parseFloat(lat), parseFloat(lng), name)
                    .then(() => { 
                        // Display POIs
                        if (data.points_of_interest && Array.isArray(data.points_of_interest)) {
                            displayPOIMarkers(data.points_of_interest);
                        } else {
                            console.log("No POIs provided in details response.");
                            clearPOIMarkers(); 
                        }
                    });
            })
            .catch(error => { // Catch network errors or errors thrown above
                console.error('Fetch location details error:', error);
                displayMessage({ response: `Failed to get details for ${name}. ${error.message}` }, 'ai');
            });
        }
        // --- Handle clicks on "Show More" buttons ---
        else if (target.classList.contains('show-more-locations')) {
             const el = target.closest('.locations-container'); // Find parent container
             if (el) {
                 const count = parseInt(el.dataset.shownCount || "0");
                 appendLocationButtons(el, count); // Append next batch
             } else {
                 console.error("Parent container not found for show more.", target);
             }
        }
    });
    console.log("Chat UI initialized.");
}


// --- Main Initialization Logic ---
// Waits for the DOM to be ready, then initializes Map and Chat functionality
document.addEventListener('DOMContentLoaded', () => {
    console.log("DOMContentLoaded fired.");
    // Basic check if Google Maps API script loaded successfully
    if (typeof google !== 'undefined' && typeof google.maps !== 'undefined') {
        initMap(); // Initialize map first
        initializeChat(); // Initialize chat UI and listeners after map setup starts
    } else {
        // Handle critical failure: Google Maps API didn't load
        console.error("google.maps object not found on DOMContentLoaded. Maps API script failed to load.");
        const mapDiv = document.getElementById("map");
        if(mapDiv) { mapDiv.innerHTML = '<p style="padding:20px; text-align:center; color:red;">Error: Google Maps API failed to load.</p>'; }
        const chatLogElement = document.getElementById('chat-log');
        // Use displayMessage if chat log exists, otherwise alert
        if (chatLogElement) { displayMessage({ response: "Error: Map features unavailable due to API loading failure." }, 'ai'); }
        else { alert("Error: Failed to load Google Maps API."); } // Fallback alert
    }
});
console.log("script.js loaded."); 
