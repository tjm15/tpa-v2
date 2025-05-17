<script lang="ts">
	import { onMount } from 'svelte';
	import type { Site, Constraint } from '$types/models';

	// Accept either a Site object (preferred) or explicit coordinates/boundary/constraints
	export let site: Site | null = null;
	export let constraintsToDisplay: Constraint[] = [];
	export let siteCoordinates: { lat: number; lon: number } | null = null;
	export let siteBoundary: any | null = null; // GeoJSON polygon
	export let constraints: any[] = []; // Array of GeoJSON constraint features
	export let interactive: boolean = true;

	let mapContainer: HTMLElement;
	let map: any = null;
	let marker: any = null;
	let boundaryLayer: any = null;
	let constraintLayers: any = null;

	function getCoords(): [number, number] {
		if (site && site.coordinates) return [site.coordinates.lat, site.coordinates.lon];
		if (siteCoordinates) return [siteCoordinates.lat, siteCoordinates.lon];
		return [51.505, -0.09]; // Default
	}

	onMount(() => {
		let L: any;
		let leafletCssLoaded = false;
		let destroyed = false;
		(async () => {
			if (typeof window === 'undefined') return;
			L = await import('leaflet');
			if (!leafletCssLoaded) {
				await import('leaflet/dist/leaflet.css');
				leafletCssLoaded = true;
			}
			if (!mapContainer || destroyed) return;
			map = L.map(mapContainer, { zoomControl: interactive }).setView(getCoords(), 15);
			L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
				attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
				maxZoom: 19,
				tileSize: 256,
			}).addTo(map);

			if (site && site.coordinates) {
				marker = L.marker([site.coordinates.lat, site.coordinates.lon]).addTo(map);
			}
			if (siteBoundary) {
				boundaryLayer = L.geoJSON(siteBoundary, { style: () => ({ color: 'blue', weight: 2 }) }).addTo(map);
			}
			if (constraintsToDisplay && constraintsToDisplay.length > 0) {
				constraintLayers = L.layerGroup();
				for (const c of constraintsToDisplay) {
					if (c.geometry) {
						L.geoJSON(c.geometry, { style: () => ({ color: 'red', weight: 1, fillOpacity: 0.2 }) }).addTo(constraintLayers);
					}
				}
				constraintLayers.addTo(map);
			}
			if (constraints && constraints.length > 0) {
				constraintLayers = constraintLayers || L.layerGroup();
				for (const g of constraints) {
					L.geoJSON(g, { style: () => ({ color: 'red', weight: 1, fillOpacity: 0.2 }) }).addTo(constraintLayers);
				}
				constraintLayers.addTo(map);
			}
		})();
		return () => {
			destroyed = true;
			if (map) map.remove();
		};
	});

	$: if (map && site && site.coordinates) {
		map.setView([site.coordinates.lat, site.coordinates.lon], map.getZoom());
	}
</script>

<div bind:this={mapContainer} class="h-full w-full bg-gray-200 min-h-[300px] rounded shadow-inner">
	<!-- Map will be rendered here by Leaflet -->
</div>
