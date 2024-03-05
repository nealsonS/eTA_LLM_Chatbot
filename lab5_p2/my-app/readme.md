# OpenLayers + Vite

This app is modified from the following example, it demonstrates how the `ol` package can be used with [Vite](https://vitejs.dev/).

To get started, install node.js:

    sudo apt update
    sudo apt install nodejs
Check that the install was successful by querying node for its version number:

    node -v

Install npm:

    sudo apt install npm

OpenLayers require node version of 14.0 or later, therefore we update npm:

    sudo npm cache clean -f
    sudo npm install -g n
    sudo n stable
    
Then change into your new `my-app` directory and start a development server (available at http://localhost:5173):

    cd my-app
    npm start

To generate a build ready for production:

    npm run build

Then deploy the contents of the `dist` directory to your server.  You can also run `npm run serve` to serve the results of the `dist` directory for preview.
