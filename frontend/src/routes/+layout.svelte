<!-- src/routes/+layout.svelte -->
<script>
  import { page } from '$app/stores';
</script>
<nav style="padding: 1rem; background: #f0f0f0;">
  <a href="/dm" style="margin-right: 1rem;">DM Workspace</a>
  <a href="/plan">Plan-Making Workspace</a>
</nav>
<slot />
