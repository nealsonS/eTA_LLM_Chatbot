import { defineConfig } from 'vite';
import nodePolyfills from 'rollup-plugin-polyfill-node';

export default defineConfig({
  plugins: [nodePolyfills()],
  resolve: {
    alias: {
      'buffer': 'buffer/'
    }
  }
});
