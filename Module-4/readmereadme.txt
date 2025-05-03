I am building a mobile-based campus navigation assistant. I already have a trained deep learning model that recognizes buildings from images and a distance estimation module. Now, I need help creating a mobile app that allows the user to:

Capture an image of their surroundings.

Send the image to a backend server (Flask API) for:

Building recognition

Distance estimation

Receive the estimated location coordinates from the backend.

Display the user's estimated position on a campus map.

Requirements:

Use React Native (preferred) or Kivy for the mobile front-end.

Include a simple UI: image capture button, preview of captured image, loading spinner while processing, and a campus map showing the user's position.

Communicate with a backend using HTTP POST (send image, receive JSON with building name, distance, and estimated coordinates).

Use Leaflet.js (or alternative) to render the interactive campus map and plot user's position.

Please generate:

Full React Native app code (front-end only).

Comments in code for clarity.

Sample backend request and response formats.

Do not include model training, backend code, or dataset processing. Focus only on building the mobile app and its interaction with the backend.