<script>
	export let name;
	import { Router, Route } from "svelte-navigator";

	import Teams from "./pages/Teams.svelte";
	import TopBar from "./components/TopBar.svelte";
	import ClockIn from "./pages/clock-in.svelte";
	import User from "./pages/user.svelte";
	import Clock from "./components/clock.svelte";
	import Warning from "./components/warning.svelte";
</script>

<Router primary={false}>
	<TopBar />
	<Route path="/">
		<Home />
	</Route>
	<Route path="user">
		<User />
	</Route>
	<Route path="/team">
		<Teams />
	</Route>
	<Route path="/clocks">
		<ClockIn />
	</Route>
</Router>

<style>
	.clock-container {
		display: flex;
		flex-direction: row;
		gap: 200px;
		justify-content: center;
	}
	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}
</style>
