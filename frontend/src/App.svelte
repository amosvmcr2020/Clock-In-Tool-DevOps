<script>
	export let name;
	import { Router, Route } from "svelte-navigator";

	import Teams from "./pages/Teams.svelte";
	import TopBar from "./components/TopBar.svelte";
	import Clocks from "./pages/clocks.svelte";
	import User from "./pages/user.svelte";
</script>

<Router primary={false}>
	<TopBar />
	<Route path="/">
		<div class="page">
			<h1>Hello {name}!</h1>
			<p>
				Visit the <a href="https://svelte.dev/tutorial"
					>Svelte tutorial</a
				> to learn how to build Svelte apps.
			</p>
		</div>
	</Route>
	<Route path="user">
		<User />
	</Route>
	<Route path="/team">
		<Teams />
	</Route>
	<Route path="/clocks">
		<Clocks />
	</Route>
</Router>

<style>
	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}
</style>
