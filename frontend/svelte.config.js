import adapter from '@sveltejs/adapter-auto';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

const config = {
	preprocess: vitePreprocess(),
	kit: {
		adapter: adapter(),
		alias: {
			$stores: 'src/lib/stores',
			$services: 'src/lib/services',
			$types: 'src/lib/types'
		}
	}
};

export default config;
