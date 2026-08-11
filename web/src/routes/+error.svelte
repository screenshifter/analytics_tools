<script lang="ts">
	import { page } from '$app/state';
</script>

<svelte:head>
	<title>{page.status} — {page.error?.message ?? 'Not Found'}</title>
</svelte:head>

<div class="wrap">
	<div class="card">
		<h1>{page.status}</h1>
		<p>Sorry — we couldn't find the page you were looking for.</p>
		<p><a class="btn" href="/">Home page</a></p>
	</div>
</div>

<style>
	:global(html, body) {
		height: 100%;
		margin: 0;
		font-family: Inter, system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
	}

	.wrap {
		height: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		background: #f7f7fb;
		color: #222;
	}

	.card {
		max-width: 720px;
		padding: 32px;
		border-radius: 12px;
		background: #fff;
		box-shadow: 0 6px 24px rgba(15, 15, 25, 0.06);
		text-align: center;
	}

	h1 {
		margin: 0 0 8px;
		font-size: 48px;
	}

	p {
		margin: 0 0 16px;
		color: #555;
	}

	a.btn {
		display: inline-block;
		padding: 10px 16px;
		background: #0b63ff;
		color: #fff;
		border-radius: 8px;
		text-decoration: none;
	}
</style>
