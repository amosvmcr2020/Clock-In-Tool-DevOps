<script>
	import { Router, Route } from "svelte-navigator";

	import Home from "./pages/Home.svelte";
	import Teams from "./pages/Teams.svelte";
	import TopBar from "./components/TopBar.svelte";
	import User from "./pages/user.svelte";
	import Warning from "./components/warning.svelte";
	import Success from "./components/success.svelte";
	import Login from "./pages/login.svelte";
	import PrivateRouteGuard from "./components/PrivateRouteGuard.svelte";
	import Database from "./pages/database.svelte";

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
	<PrivateRouteGuard>
		<Route path="/">
			<Login bind:alerts />
		</Route>
		<Route path="/home">
			<Home bind:alerts />
		</Route>
		<Route path="/user">
			<User bind:alerts />
		</Route>
		<Route path="/team">
			<Teams bind:alerts />
		</Route>
		<Route path="/database">
			<Database />
		</Route>
	</PrivateRouteGuard>
	<Route path="/login">
		<Login bind:alerts />
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
		padding-bottom: 20px;
	}

	.notification {
		height: 60px;
	}
</style>
