<script>
    import Clock from "../components/clock.svelte";
    import Warning from "../components/warning.svelte";
    let response;
</script>

<div class="page">
    <div class="page-title">Log your time</div>

    <!-- <div class="container-title">Clock in/out</div> -->
    <div class="clock-container">
        <Clock bind:response type="in" />
        <Clock bind:response type="out" />
    </div>
    {#if response}
        <div class="warning-container">
            <Warning>{response}</Warning>
        </div>
    {/if}
</div>

<style>
    .clock-container {
        margin-top: 30px;
        display: flex;
        flex-direction: row;
        gap: 200px;
        justify-content: center;
    }
    .warning-container {
        color: #333;
    }
</style>
