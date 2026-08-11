# analytics_tools
A set of tools for all sorts of analytics.

Tools are divided by categories and are contained in the respective folders. Currenly there are the next categories:
- Financial (./finance)

## Web app
A simple static Svelte web app lives in `web/`.

This app uses an explicit Svelte config file at `web/svelte.config.js`.

### Run locally
1. `cd web`
2. `npm install`
3. `npm run dev`

### Preview production build locally
1. `cd web`
2. `npm run build`
3. `npm run preview`

### Build for production
1. `cd web`
2. `npm run build`
3. Serve the `dist/` output as a static site, or publish with GitHub Pages.
