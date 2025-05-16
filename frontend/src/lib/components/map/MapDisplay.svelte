<script lang="ts">
	import { onMount } from 'svelte';
	import type { Site, Constraint } from '$types/models';

	export let site: Site | null = null;
	export let constraintsToDisplay: Constraint[] = []; // Constraints relevant to the site/area
    export let interactive: boolean = true;

	let mapContainer: HTMLElement;

	onMount(() => {
		// In a real implementation, initialize your mapping library here
		// e.g., L.map(mapContainer).setView([site?.coordinates?.lat || 51.505, site?.coordinates?.lon || -0.09], 13);
		console.log('MapDisplay mounted. Site:', site, 'Constraints:', constraintsToDisplay);
        if (mapContainer && site) {
            mapContainer.innerHTML = `
                <div class="p-4 bg-gray-200 rounded text-center">
                    <p class="font-semibold">Map Placeholder</p>
                    <p>Site: ${site.name || site.id}</p>
                    ${site.coordinates ? `<p class="text-xs">Coords: Lat ${site.coordinates.lat?.toFixed(3)}, Lon ${site.coordinates.lon?.toFixed(3)}</p>` : ''}
                    <p class="text-xs mt-2">${constraintsToDisplay.length} constraint layers to display.</p>
                </div>
            `;
        } else if (mapContainer) {
            mapContainer.innerHTML = `<div class="p-4 bg-gray-200 rounded text-center font-semibold">Map Placeholder - No site selected</div>`;
        }
		return () => {
			// Cleanup map instance if necessary
		};
	});
</script>

<div bind:this={mapContainer} class="w-full h-full bg-gray-300 min-h-[300px] shadow-inner rounded">
	</div>