<script>
	import { Router, Route } from "svelte-navigator";

	import Home from "./pages/Home.svelte";
	import Teams from "./pages/Teams.svelte";
	import TopBar from "./components/TopBar.svelte";
	import User from "./pages/user.svelte";
	import Warning from "./components/warning.svelte";
	import Success from "./components/success.svelte";

	// TODO: Change response to be a list of alerts etc. and stack them.
	export let alerts = [];
</script>

<div class="warningContainer">
	{#each alerts as alert}
		<div class="notification">
			{#if alert[0] == "Success"}
				<Success>{alert[1]}</Success>
			{:else if alert[0] == "Error"}
				<Warning>{alert[1]}</Warning>
			{/if}
		</div>
	{/each}
</div>
<Router primary={false}>
	<TopBar />
	<Route path="/">
		<Home bind:alerts />
	</Route>
	<Route path="user">
		<User bind:alerts />
	</Route>
	<Route path="/team">
		<Teams bind:alerts />
	</Route>
</Router>

<style>
	.warningContainer {
		overflow: hidden;
		position: fixed;
		top: 0;
		display: flex;
		flex-direction: column-reverse;
		gap: 10px;
		width: 100%;
		z-index: 9999;
		pointer-events: none;
		min-height: 10%;
	}

	.notification {
		height: 60px;
	}
</style>
