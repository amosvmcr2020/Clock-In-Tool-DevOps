<script>
	export let name;
	import { Router, Route, Link } from "svelte-navigator";

	import Teams from "./pages/Teams.svelte";
</script>
<Router primary={false}>
	<div class="topBar">
		<div class="title">
			Clock In Tool
		</div>
		<Link  to="/" class="menu-item">
			Home
		</Link>
		<Link  to="/team" class="menu-item">
			Clock-In
		</Link>
		<Link  to="/team" class="menu-item">
			Teams
		</Link>
	</div>
	
	<!-- <main> -->
		<Route path="/">
			<div class="page">

				<h1>Hello {name}!</h1>
				<p>Visit the <a href="https://svelte.dev/tutorial">Svelte tutorial</a> to learn how to build Svelte apps.</p>
			</div>
		</Route>
		<Route path="/team">

				<Teams/>

		</Route>
	<!-- </main> -->


</Router>


<style>
	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	.topBar {
	position: absolute;
	width: 100%;
	height: 80px;
	position: fixed;
	/* background: linear-gradient(90deg, var(--primary) 10%, var(--secondary) 100%); */
	background-color: var(--secondary);
	color: var(--text);
	font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
	
	box-shadow: .1px .1px .1px 1px #FFFFFF;

	z-index: 0;

	display: flex;
	align-items: center;
	justify-content: left;
	border-radius: 0 0 1% 1%;
	flex-direction: row;
	gap: 40px;
	}

	.title {
		font-size: 32px;
		padding: 20px;
		text-transform: uppercase;
	}

	.menu-item {
		width: fit-content;
		overflow: hidden;
	}
</style>