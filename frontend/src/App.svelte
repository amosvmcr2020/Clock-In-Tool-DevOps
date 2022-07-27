<script lang="ts">
    import { Router, Route, Link } from "svelte-navigator";
    import Teams from "./pages/Teams.svelte";
    import Home from "./pages/Home.svelte";
    import TopBar from "./components/TopBar.svelte";
    import SideBar from "./components/SideBar.svelte";

    export let showSide = false;
</script>

<Router>
    <header>
        <div class="topBarContainer">
            <TopBar bind:showSide />
            <SideBar bind:show={showSide} />
        </div>
    </header>
    <main>
        <Route path="/">
            <Home />
        </Route>
        <Route path="teams">
            <Teams />
        </Route>
    </main>
</Router>

<style>
    main {
        margin: 1%;
        margin-top: 0;
        height: 100%;
        z-index: 99999;
    }

    .topBarContainer {
        top: 0;
        margin-top: 0;
    }
</style>
