<script>
	import { Router, Route } from "svelte-navigator";

	import Home from "./pages/Home.svelte";
	import Teams from "./pages/Teams.svelte";
	import TopBar from "./components/TopBar.svelte";
	import User from "./pages/user.svelte";
	import Warning from "./components/warning.svelte";

	// TODO: Change response to be a list of alerts etc. and stack them.
	export let alerts = [];

	$: alerts,
		console.log(alerts),
		setTimeout(() => {
			alerts.pop();
		}, 3000),
		(alerts = alerts);
</script>

<!-- TODO: FIX THIS -->
<div class="warningContainer">
	{#each alerts as alert}
		<div class="notification">
			<Warning>{alert[1]}</Warning>
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
		position: absolute;
		top: 0;
		display: flex;
		flex-direction: column;
		gap: 5px;
		width: 100%;
		/* height: 100%; */
	}

	.notification {
		height: 60px;
	}
</style>
