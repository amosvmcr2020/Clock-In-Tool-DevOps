<script>
	import { Router, Route } from "svelte-navigator";

	import Home from "./pages/Home.svelte";
	import Teams from "./pages/Teams.svelte";
	import TopBar from "./components/TopBar.svelte";
	import ClockIn from "./pages/clock-in.svelte";
	import User from "./pages/user.svelte";

	import { current_user_id } from "./store";
	import { get } from "svelte/store";
</script>

<Router primary={false}>
	<TopBar />
	<Route path="/">
		<Home />
	</Route>
	<Route bind:user_id={$current_user_id} path="user">
		<User />
	</Route>
	<Route path="/team">
		<Teams />
	</Route>
	<Route path="/clocks">
		<ClockIn />
	</Route>
</Router>
