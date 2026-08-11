<script>
	let value = $state(3);
	const baseValues = [4, 7, 5, 8, 3, 6, 9, 2, 7, 5];

	function getChartValues() {
		return baseValues.map((n) => n ^ value);
	}
</script>

<h1>This is a test tool page</h1>

<div class="graph-panel">
	<div class="chart">
		<div class="chart-header">
			<span>Slider value:</span>
			<strong>{value}</strong>
		</div>
		<svg viewBox="0 0 100 50" preserveAspectRatio="none" aria-label="Graph showing values multiplied by slider value">
			<polyline
				fill="none"
				stroke="#ff3e00"
				stroke-width="2"
				points={getChartValues().map((y, i) => `${i * 10 + 5},${50 - (y / Math.max(...getChartValues())) * 40}`).join(' ')}
			/>
			{#each getChartValues() as y, i}
				<circle cx={i * 10 + 5} cy={50 - (y / Math.max(...getChartValues())) * 40} r="1.6" fill="#ff3e00" />
			{/each}
		</svg>
	</div>
	<div class="slider-row">
		<label for="valueRange">Choose a value</label>
		<input
			type="range"
			id="valueRange"
			min="1"
			max="10"
			step="1"
			bind:value
		/>
	</div>
</div>

<div class="wrap">
	<div class="card">
		<p>Let's get you back from here.</p>
		<p><a class="btn" href="/">Home page</a></p>
	</div>
</div>

<style>
    h1 {
        color: #ff3e00;
        margin-bottom: 1rem;
        text-align: center;
    }

    .graph-panel {
        display: flex;
        flex-direction: column;
        align-items: center;
        max-width: 42rem;
        margin: 0 auto 2rem;
        padding: 1rem;
    }

    .chart {
        width: 100%;
        max-width: 42rem;
        background: #fff7f0;
        border: 1px solid #ffd1b3;
        border-radius: 1rem;
        padding: 1rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.04);
    }

    .chart-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.8rem;
        font-size: 1rem;
        color: #333;
    }

    svg {
        width: 100%;
        height: 200px;
        overflow: visible;
        border-radius: 0.75rem;
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.9), rgba(255, 243, 237, 0.95));
    }

    .slider-row {
        width: 100%;
        margin-top: 1rem;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    label {
        font-size: 0.95rem;
        color: #555;
    }

    input[type="range"] {
        width: 100%;
        accent-color: #ff3e00;
    }

    p {
        color: #333;
        font-size: 1.2rem;
    }

    .btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 0.75rem 1.4rem;
        margin-top: 1rem;
        background: #ff3e00;
        color: white;
        text-decoration: none;
        border-radius: 0.5rem;
        transition: background 0.2s ease;
    }

    .btn:hover {
        background: #e63700;
    }

    .wrap {
        display: flex;
        justify-content: center;
        margin-top: 2rem;
    }

    .card {
        max-width: 28rem;
    }
</style>
