<script>
    import Clock from "../components/clock.svelte";
    export let alerts = [];
</script>

<!-- <div class="container-title">Clock in/out</div> -->
<div class="clock-container">
    <Clock bind:alerts type="in" />
    <Clock bind:alerts type="out" />
</div>

<style>
    .clock-container {
        margin-top: 30px;
        display: flex;
        flex-direction: row;
        gap: 200px;
        justify-content: center;
    }
</style>
