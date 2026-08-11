<script lang="ts">
	import app_icon from '../../static/logo.svg';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={app_icon} />
</svelte:head>

{@render children()}
