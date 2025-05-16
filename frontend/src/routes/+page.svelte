<!-- src/routes/+page.svelte -->
<script>
  import { redirect } from '@sveltejs/kit';
  export function load() {
    throw redirect(302, '/dm');
  }
</script>
