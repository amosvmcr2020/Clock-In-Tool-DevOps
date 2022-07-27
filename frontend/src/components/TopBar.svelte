<script>
    let sidebar_show = false;
    import Button from "./Button.svelte";

    export let showSide;
</script>

<div class="main">
    <Button func={() => (showSide = !showSide)}>Menu</Button>
    <h1>Clocker</h1>
</div>

<style>
    h1 {
        color: white;
        text-transform: uppercase;
        font-size: 4em;
        font-weight: 100;
        height: 100%;
        margin: 0;
    }

    .main {
        background-color: rgb(32, 142, 194);
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        align-items: center;
        gap: 10px;
    }
</style>
